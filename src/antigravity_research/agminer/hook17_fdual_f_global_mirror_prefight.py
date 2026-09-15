"""032H17A12D1R3B — global mirror field and density-gradient transfer preflight.

PURPOSE
-------
R3A established that the linear topological portal

    sigma = (F *F)/(2 M^4)

has three unusually favorable properties:

1. its ideal invariant-per-canonical-energy optimum exactly matches A12C;
2. the leading uniform-matter bulk loading cancels by the Bianchi identity;
3. the exact residual uniform-bulk term is tiny at the A12C normalization.

The remaining cheap questions are now geometric rather than algebraic:

A. Can the actual A12C exterior magnetic field be mirrored by a globally
   realizable electrostatic field?

B. What is the minimum global canonical energy of that completion?

C. Can all electric sources remain inside the original 2 m source support
   without a net hidden charge?

D. How badly does the finite payload density-gradient layer couple to the
   simple E || B mirror?

E. Is there a polarization-rotation / P-node geometry that can suppress the
   large-beta interface mixing while retaining the required gradient of

       P = F *F = -4 E dot B ?

This run answers those questions before authorizing a fully loaded mixed-E/B
BVP.

----------------------------------------------------------------------
1. EXTERIOR MAGNETIC SCALAR POTENTIAL
----------------------------------------------------------------------

Outside the spherical current support r > R_s, the frozen A12C field obeys

    div B = 0
    curl B = 0.

The exterior of a sphere is simply connected, so

    B = -grad Psi.

For an axisymmetric localized current source with zero magnetic monopole,

    Psi(r,theta)
        =
    sum_{l>=1}
        a_l
        (R_s/r)^(l+1)
        P_l(cos theta),

where a_l is the scalar-potential amplitude at r=R_s.

The field components are

    B_r
        =
    sum_l
        (l+1)/r
        a_l
        (R_s/r)^(l+1)
        P_l,

    B_theta
        =
    sum_l
        1/r
        a_l
        (R_s/r)^(l+1)
        sin(theta)
        P'_l.

R3B fits these amplitudes independently at multiple exterior radii and
multiple l_max values.

This is both:

- an integrability test;
- an independent reconstruction of the A12C exterior field.

----------------------------------------------------------------------
2. GLOBAL ELECTROSTATIC MIRROR
----------------------------------------------------------------------

R3A's ideal payload-region construction is

    E_new = -B_A / sqrt(2)
    B_new = +B_A / sqrt(2).

Outside the source sphere we can therefore take

    Phi_out = -Psi / sqrt(2),

so

    E_out = -grad Phi_out = -B_A/sqrt(2).

A global electrostatic field still requires an interior completion.

For each exterior multipole, the minimum-energy regular harmonic interior
with the same boundary potential is

    Phi_in,l
        =
    Phi_l(R_s)
    (r/R_s)^l
    P_l(cos theta).

This needs only a surface charge on r=R_s.

Because the magnetic scalar expansion has no l=0 term, the resulting
electric surface charge has exactly zero net charge.

Thus the ideal mirror does NOT require a net hidden electric charge.

----------------------------------------------------------------------
3. ANALYTIC ENERGY OF THE MIRROR COMPLETION
----------------------------------------------------------------------

For one magnetic scalar boundary amplitude a_l,

    E_B,out,l
        =
    2*pi*R_s
    (l+1)/(2l+1)
    a_l^2
    * conversion.

The electric mirror exterior costs exactly one half of this.

The minimum-energy regular electric interior costs

    E_E,in,l
        =
    pi*R_s
    l/(2l+1)
    a_l^2
    * conversion.

Hence

    E_E,total,l
        =
    pi*R_s*a_l^2*conversion.

Relative to the original magnetic exterior energy,

    E_E,total,l / E_B,out,l
        =
    (2l+1)/(2(l+1)).

Examples:

    l=1 dipole: 3/4
    l=2:        5/6
    l -> inf:   1.

The full mixed-field capacity before payload loading is therefore

    E_mixed
        =
    1/2 E_B,A12C,total
        +
    E_E,mirror,total.

This is a real global field-energy estimate rather than R3A's local algebraic
2.656859-J equality.

It still excludes microscopic source/support energy.

----------------------------------------------------------------------
4. FINITE-PAYLOAD METRIC RECONSTRUCTION
----------------------------------------------------------------------

Using the fitted exterior field,

    E = -B_fit/sqrt(2)
    B = +B_A/sqrt(2),

gives

    P = 2 B_fit dot B_A

in the declared convention, and therefore

    sigma_P
        =
    (hbar c)^2
    (B_fit dot B_A)
    / M^4.

If B_fit reproduces B_A in the payload region,

    sigma_P -> sigma_A12C.

The run directly reconstructs the finite-payload acceleration and, if the
multipole fit changes the least payload point slightly, analytically rescales
both fields to restore exactly 1 g.

----------------------------------------------------------------------
5. INTERFACE ORIENTATION DIAGNOSTIC
----------------------------------------------------------------------

R3A found the large-beta interface quantities schematically enter as

    D_n = E_n - beta B_n
    H_t = B_t + beta E_t.

For the simple parallel mirror, E and B share a direction.

Define n as the local payload density-gradient normal and decompose the
original A12C field into

    B_n
    B_t.

For a general amplitude ratio

    r = |E|/|B|

while preserving the same local product E*B and therefore the same P,

    |B_new|
        =
    |B_A| / sqrt(2r),

    |E_new|
        =
    sqrt(r/2) |B_A|.

The canonical field-energy penalty relative to the ideal r=1 split is

    G_energy(r)
        =
    (r + 1/r)/2.

A large-beta interface-driver proxy scales as

    G_interface(r)
        ~
    B_n^2/(2r)
        +
    r B_t^2/2.

Thus an E/B amplitude imbalance can sometimes suppress the interface driver
at modest field-energy cost.

R3B computes the actual A12C density-gradient-weighted B_n/B_t fractions and
the resulting Pareto tradeoff.

----------------------------------------------------------------------
6. THE P-NODE / POLARIZATION-ROTATION CORRIDOR
----------------------------------------------------------------------

There is a particularly important local geometry.

At a density interface choose

    E parallel n
    B perpendicular n.

Then

    E_t = 0
    B_n = 0

and the large-beta interface pieces vanish exactly.

But simultaneously

    E dot B = 0
    P = 0.

This is not automatically fatal because acceleration depends on grad P, not
on P itself.

If equal-energy fields rotate through orthogonality,

    sigma
        =
    sigma_amp cos(gamma),

then at the P-node gamma=pi/2,

    |grad sigma|
        =
    sigma_amp |grad gamma|.

For a 1-g response,

    |grad sigma|required
        =
    g/c^2.

Therefore, using the A12C sigma amplitude,

    |grad gamma|
        =
    (g/c^2)/sigma_A12C.

R3B computes the corresponding angle change across the actual 0.1 m C1
density-taper scale.

If this angle is modest, the next loaded BVP should be designed around a
polarization node coincident with the strongest density-gradient region,
rather than around a globally parallel E/B mirror.

This is a kinematic design clue only.

Maxwell integrability and the fully coupled same-action BVP must still prove
that such a texture exists.

----------------------------------------------------------------------
CLAIM LIMITS
----------------------------------------------------------------------

R3B does NOT establish:

- a fully loaded mixed-E/B solution;
- microscopic electric charge realization;
- parity/CP completion;
- full source energy;
- hyperbolicity of the interacting loaded system;
- quantum naturalness;
- empirical viability;
- complete operating energy;
- replacement of 006D;
- a device.

CLAIM CLASSIFICATION
--------------------
PROJECT_GLOBAL_MIRROR_AND_INTERFACE_DESIGN_PREFLIGHT
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from scipy.interpolate import RegularGridInterpolator
from scipy.sparse import diags, eye, kron
from scipy.sparse.linalg import spsolve
from scipy.special import eval_legendre

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    PAYLOAD_MAJOR_RADIUS_M,
    PAYLOAD_MINOR_RADIUS_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
    TARGET_ACCELERATION_M_S2,
    _payload_mask,
    _source_profile,
    payload_center_z_m,
)

from .hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    payload_density_profile_kg_m3,
)


BRANCH = "032H17A12D1R3B"

PRODUCTION_RHO_MAX_M = 12.0
PRODUCTION_Z_MIN_M = -10.0
PRODUCTION_Z_MAX_M = 13.0

GRID_SPACINGS_M = (
    0.075,
    0.050,
)

FIT_RADII_M = (
    2.20,
    2.40,
    2.60,
)

FIT_LMAX_VALUES = (
    8,
    12,
    16,
)

PRIMARY_FIT_RADIUS_M = 2.40
PRIMARY_LMAX = 12

FIT_QUADRATURE_ORDER = 128

FIT_RMS_PASS_MAX = 0.05
EXTERIOR_ENERGY_RELERR_PASS_MAX = 0.10

LOW_J_STRONG_TARGET_J = 100.0
LOW_KJ_TARGET_J = 10000.0

A12C_REFERENCE_FIELD_ENERGY_J = 2.6568591420597114
A12C_REFERENCE_SIGMA_MAX = 1.3615723178022103e-16

TAPER_THICKNESS_M = 0.5 * PAYLOAD_MINOR_RADIUS_M


def _repo_root() -> Path:
    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


def _load_json(
    filename: str,
) -> dict[str, Any]:
    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        filename
    )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


@lru_cache(maxsize=1)
def a12c_artifact() -> dict[str, Any]:
    return _load_json(
        "032h17a12c_hook17_concurrent_u1_fieldstrength_metric_summary.json"
    )


@lru_cache(maxsize=1)
def r3a_artifact() -> dict[str, Any]:
    return _load_json(
        "032h17a12d1r3a_hook17_fdual_f_topological_loading_summary.json"
    )


def provenance_gate() -> dict[str, Any]:
    a12c = (
        a12c_artifact()
    )

    r3a = (
        r3a_artifact()
    )

    production = (
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ]
    )

    passed = bool(
        math.isclose(
            float(
                production[
                    "field_energy_j"
                ]
            ),
            A12C_REFERENCE_FIELD_ENERGY_J,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )

        and

        r3a[
            "structural_rescue_survives_cheap_gate"
        ]
        is True

        and

        r3a[
            "r3b_authorized"
        ]
        is True

        and

        r3a[
            "mixed_eb_topological_portal_closed"
        ]
        is False
    )

    return {
        "pass":
            passed,

        "a12c_field_energy_j":
            production[
                "field_energy_j"
            ],

        "a12c_payload_sigma_max":
            production[
                "payload_sigma_max"
            ],

        "a12c_standoff_m":
            production[
                "geometric_external_standoff_m"
            ],

        "r3a_structural_rescue_survives":
            r3a[
                "structural_rescue_survives_cheap_gate"
            ],

        "r3a_r3b_authorized":
            r3a[
                "r3b_authorized"
            ],

        "r3a_dominant_remaining_gate":
            r3a[
                "dominant_remaining_gate"
            ],
    }


def analytic_mode_energy_ratio(
    ell: int,
) -> dict[str, float]:
    if ell < 1:
        raise ValueError(
            "ell must be >= 1"
        )

    electric_total_over_original_magnetic_exterior = (
        (
            2.0
            *
            ell
            +
            1.0
        )
        /
        (
            2.0
            *
            (
                ell
                +
                1.0
            )
        )
    )

    return {
        "ell":
            float(
                ell
            ),

        "electric_exterior_over_original_magnetic_exterior":
            0.5,

        "electric_interior_over_original_magnetic_exterior":
            (
                ell
                /
                (
                    2.0
                    *
                    (
                        ell
                        +
                        1.0
                    )
                )
            ),

        "electric_total_over_original_magnetic_exterior":
            electric_total_over_original_magnetic_exterior,
    }


def field_energy_ratio_for_repartition(
    electric_over_magnetic: float,
) -> float:
    ratio = float(
        electric_over_magnetic
    )

    if ratio <= 0.0:
        raise ValueError(
            "electric_over_magnetic must be positive"
        )

    return (
        0.5
        *
        (
            ratio
            +
            1.0
            /
            ratio
        )
    )


def interface_null_geometry_gate() -> dict[str, Any]:
    return {
        "configuration":
            "E_normal_and_B_tangential",

        "E_tangential":
            0.0,

        "B_normal":
            0.0,

        "large_beta_Dn_mixing":
            0.0,

        "large_beta_Ht_mixing":
            0.0,

        "E_dot_B":
            0.0,

        "P":
            0.0,

        "exact_interface_mix_null":
            True,

        "metric_force_zero_if_configuration_constant":
            True,

        "usable_as_P_node_with_nonzero_gradient":
            True,
    }


def required_sigma_gradient_for_one_g_per_m() -> float:
    return (
        TARGET_ACCELERATION_M_S2
        /
        C_LIGHT_M_S**2
    )


def polarization_node_corridor() -> dict[str, Any]:
    sigma_gradient = (
        required_sigma_gradient_for_one_g_per_m()
    )

    sigma_amplitude = (
        A12C_REFERENCE_SIGMA_MAX
    )

    rotation_rate = (
        sigma_gradient
        /
        sigma_amplitude
    )

    angle = (
        rotation_rate
        *
        TAPER_THICKNESS_M
    )

    beta_peak = float(
        r3a_artifact()[
            "loading_structure"
        ][
            "topological_beta_peak_magnitude"
        ]
    )

    return {
        "required_sigma_gradient_per_m":
            sigma_gradient,

        "a12c_sigma_amplitude":
            sigma_amplitude,

        "payload_c1_taper_thickness_m":
            TAPER_THICKNESS_M,

        "sigma_change_required_across_taper":
            sigma_gradient
            *
            TAPER_THICKNESS_M,

        "sigma_change_over_a12c_sigma_max":
            (
                sigma_gradient
                *
                TAPER_THICKNESS_M
                /
                sigma_amplitude
            ),

        "rotation_rate_at_equal_field_P_node_rad_per_m":
            rotation_rate,

        "rotation_angle_across_taper_rad":
            angle,

        "rotation_angle_across_taper_deg":
            math.degrees(
                angle
            ),

        "beta_peak_times_rotation_angle":
            beta_peak
            *
            angle,

        "node_geometry_can_zero_leading_interface_mix_at_one_surface":
            True,

        "finite_width_taper_still_requires_loaded_solution":
            True,
    }


def claim_policy_gate() -> dict[str, Any]:
    return {
        "primary_goal_preserve_2p656859j_mechanism":
            True,

        "field_efficiency_optimization_for_headline_only":
            False,

        "global_mirror_is_source_completion_prefight":
            True,

        "surface_charge_physicalized":
            False,

        "parity_cp_completed":
            False,

        "full_loaded_BVP_completed":
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


def fit_configuration_gate() -> dict[str, Any]:
    return {
        "grid_spacings_m":
            list(
                GRID_SPACINGS_M
            ),

        "fit_radii_m":
            list(
                FIT_RADII_M
            ),

        "fit_lmax_values":
            list(
                FIT_LMAX_VALUES
            ),

        "primary_fit_radius_m":
            PRIMARY_FIT_RADIUS_M,

        "primary_lmax":
            PRIMARY_LMAX,

        "multipoles_begin_at_l1":
            True,

        "magnetic_monopole_included":
            False,

        "net_electric_mirror_charge_expected":
            0.0,
    }


def reconstruct_a12c_field(
    h: float,
) -> dict[str, Any]:
    h = float(
        h
    )

    rhos = np.arange(
        0.0,
        PRODUCTION_RHO_MAX_M
        +
        0.5
        *
        h,
        h,
    )

    zs = np.arange(
        PRODUCTION_Z_MIN_M,
        PRODUCTION_Z_MAX_M
        +
        0.5
        *
        h,
        h,
    )

    rho_i = (
        rhos[
            1:-1
        ]
    )

    z_i = (
        zs[
            1:-1
        ]
    )

    nr = len(
        rho_i
    )

    nz = len(
        z_i
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

    source_i = (
        _source_profile(
            rho_grid_i,
            z_grid_i,
        )
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

    a_phi = np.zeros(
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

    a_phi[
        1:-1,
        1:-1,
    ] = (
        u
        /
        np.sqrt(
            rho_grid_i
        )
    )

    rho_grid, z_grid = np.meshgrid(
        rhos,
        zs,
    )

    payload = (
        _payload_mask(
            rho_grid,
            z_grid,
        )
    )

    d_a_dz, d_a_drho = np.gradient(
        a_phi,
        h,
        h,
        edge_order=2,
    )

    b_rho_unit = (
        -d_a_dz
    )

    a_over_rho = np.zeros_like(
        a_phi
    )

    np.divide(
        a_phi,
        rho_grid,
        out=a_over_rho,
        where=
            rho_grid
            >
            0.0,
    )

    b_z_unit = (
        d_a_drho
        +
        a_over_rho
    )

    b_squared_unit = (
        b_rho_unit**2
        +
        b_z_unit**2
    )

    sigma_unit = (
        HBAR_C_EV_M**2
        *
        b_squared_unit
        /
        REFERENCE_PORTAL_SCALE_EV**4
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

    minimum_unit = float(
        np.min(
            acceleration_unit[
                payload
            ]
        )
    )

    if minimum_unit <= 0.0:
        raise RuntimeError(
            "A12C reconstruction lost outward sign"
        )

    scale = math.sqrt(
        TARGET_ACCELERATION_M_S2
        /
        minimum_unit
    )

    b_rho = (
        scale
        *
        b_rho_unit
    )

    b_z = (
        scale
        *
        b_z_unit
    )

    b_squared = (
        b_rho**2
        +
        b_z**2
    )

    sigma = (
        scale**2
        *
        sigma_unit
    )

    acceleration = (
        scale**2
        *
        acceleration_unit
    )

    field_energy_j = (
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
                b_squared
            )
        )
        *
        h**2
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    radius = np.sqrt(
        rho_grid**2
        +
        z_grid**2
    )

    outside = (
        radius
        >=
        SOURCE_RADIUS_M
    )

    exterior_energy_j = (
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
                b_squared
                *
                outside
            )
        )
        *
        h**2
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    return {
        "h":
            h,

        "rhos":
            rhos,

        "zs":
            zs,

        "rho_grid":
            rho_grid,

        "z_grid":
            z_grid,

        "payload":
            payload,

        "b_rho":
            b_rho,

        "b_z":
            b_z,

        "b_squared":
            b_squared,

        "sigma":
            sigma,

        "acceleration":
            acceleration,

        "field_energy_j":
            field_energy_j,

        "exterior_energy_j":
            exterior_energy_j,

        "payload_acceleration_min_m_s2":
            float(
                np.min(
                    acceleration[
                        payload
                    ]
                )
            ),

        "payload_acceleration_max_m_s2":
            float(
                np.max(
                    acceleration[
                        payload
                    ]
                )
            ),

        "payload_sigma_max":
            float(
                np.max(
                    sigma[
                        payload
                    ]
                )
            ),
    }


def _legendre_derivative(
    ell: int,
    x: np.ndarray,
) -> np.ndarray:
    if ell == 0:
        return np.zeros_like(
            x
        )

    p_l = eval_legendre(
        ell,
        x,
    )

    p_lm1 = eval_legendre(
        ell
        -
        1,
        x,
    )

    return (
        ell
        *
        (
            p_lm1
            -
            x
            *
            p_l
        )
        /
        (
            1.0
            -
            x**2
        )
    )


def fit_exterior_multipoles(
    field: dict[str, Any],
    fit_radius_m: float,
    lmax: int,
) -> dict[str, Any]:
    x, weights = np.polynomial.legendre.leggauss(
        FIT_QUADRATURE_ORDER
    )

    theta = np.arccos(
        x
    )

    sin_theta = np.sqrt(
        1.0
        -
        x**2
    )

    rho = (
        fit_radius_m
        *
        sin_theta
    )

    z = (
        fit_radius_m
        *
        x
    )

    points = np.column_stack(
        [
            z,
            rho,
        ]
    )

    interp_rho = RegularGridInterpolator(
        (
            field[
                "zs"
            ],
            field[
                "rhos"
            ],
        ),
        field[
            "b_rho"
        ],
        bounds_error=True,
    )

    interp_z = RegularGridInterpolator(
        (
            field[
                "zs"
            ],
            field[
                "rhos"
            ],
        ),
        field[
            "b_z"
        ],
        bounds_error=True,
    )

    b_rho = interp_rho(
        points
    )

    b_z = interp_z(
        points
    )

    b_r = (
        b_rho
        *
        sin_theta
        +
        b_z
        *
        x
    )

    b_theta = (
        b_rho
        *
        x
        -
        b_z
        *
        sin_theta
    )

    columns_r = []
    columns_theta = []

    for ell in range(
        1,
        lmax
        +
        1,
    ):
        p_l = eval_legendre(
            ell,
            x,
        )

        dp_l = (
            _legendre_derivative(
                ell,
                x,
            )
        )

        radial_factor = (
            (
                SOURCE_RADIUS_M
                /
                fit_radius_m
            ) ** (
                ell
                +
                1
            )
            /
            fit_radius_m
        )

        columns_r.append(
            (
                ell
                +
                1
            )
            *
            radial_factor
            *
            p_l
        )

        columns_theta.append(
            radial_factor
            *
            sin_theta
            *
            dp_l
        )

    matrix_r = np.column_stack(
        columns_r
    )

    matrix_theta = np.column_stack(
        columns_theta
    )

    sqrt_weights = np.sqrt(
        weights
    )

    matrix = np.vstack(
        [
            matrix_r
            *
            sqrt_weights[
                :,
                None
            ],
            matrix_theta
            *
            sqrt_weights[
                :,
                None
            ],
        ]
    )

    target = np.concatenate(
        [
            b_r
            *
            sqrt_weights,
            b_theta
            *
            sqrt_weights,
        ]
    )

    coefficients, _, _, _ = np.linalg.lstsq(
        matrix,
        target,
        rcond=None,
    )

    predicted = (
        matrix
        @
        coefficients
    )

    residual = (
        np.linalg.norm(
            predicted
            -
            target
        )
        /
        np.linalg.norm(
            target
        )
    )

    conversion = (
        EV_J
        /
        HBAR_C_EV_M
    )

    exterior_energy = 0.0
    electric_interior_energy = 0.0
    electric_exterior_energy = 0.0

    mode_rows = []

    for ell, amplitude in enumerate(
        coefficients,
        start=1,
    ):
        magnetic_exterior = (
            2.0
            *
            math.pi
            *
            SOURCE_RADIUS_M
            *
            (
                ell
                +
                1.0
            )
            /
            (
                2.0
                *
                ell
                +
                1.0
            )
            *
            amplitude**2
            *
            conversion
        )

        electric_exterior = (
            0.5
            *
            magnetic_exterior
        )

        electric_interior = (
            math.pi
            *
            SOURCE_RADIUS_M
            *
            ell
            /
            (
                2.0
                *
                ell
                +
                1.0
            )
            *
            amplitude**2
            *
            conversion
        )

        exterior_energy += (
            magnetic_exterior
        )

        electric_exterior_energy += (
            electric_exterior
        )

        electric_interior_energy += (
            electric_interior
        )

        mode_rows.append(
            {
                "ell":
                    ell,

                "boundary_scalar_amplitude":
                    float(
                        amplitude
                    ),

                "magnetic_exterior_energy_j":
                    magnetic_exterior,

                "electric_exterior_energy_j":
                    electric_exterior,

                "electric_interior_energy_j":
                    electric_interior,

                "electric_total_energy_j":
                    (
                        electric_exterior
                        +
                        electric_interior
                    ),
            }
        )

    electric_total = (
        electric_exterior_energy
        +
        electric_interior_energy
    )

    direct_exterior = float(
        field[
            "exterior_energy_j"
        ]
    )

    energy_relerr = (
        abs(
            exterior_energy
            -
            direct_exterior
        )
        /
        direct_exterior
    )

    return {
        "fit_radius_m":
            float(
                fit_radius_m
            ),

        "lmax":
            int(
                lmax
            ),

        "relative_rms_field_residual":
            float(
                residual
            ),

        "boundary_amplitudes":
            coefficients,

        "mode_rows":
            mode_rows,

        "multipole_magnetic_exterior_energy_j":
            float(
                exterior_energy
            ),

        "direct_numerical_magnetic_exterior_energy_j":
            direct_exterior,

        "exterior_energy_relative_error":
            float(
                energy_relerr
            ),

        "electric_exterior_energy_j":
            float(
                electric_exterior_energy
            ),

        "electric_interior_minimum_energy_j":
            float(
                electric_interior_energy
            ),

        "electric_total_minimum_energy_j":
            float(
                electric_total
            ),
    }


def evaluate_multipole_field(
    field: dict[str, Any],
    fit: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray]:
    rho = (
        field[
            "rho_grid"
        ]
    )

    z = (
        field[
            "z_grid"
        ]
    )

    radius = np.sqrt(
        rho**2
        +
        z**2
    )

    valid = (
        radius
        >=
        SOURCE_RADIUS_M
        *
        1.01
    )

    r_safe = np.where(
        valid,
        radius,
        SOURCE_RADIUS_M,
    )

    x = np.zeros_like(
        radius
    )

    np.divide(
        z,
        r_safe,
        out=x,
        where=
            r_safe
            >
            0.0,
    )

    x = np.clip(
        x,
        -0.999999999999,
        0.999999999999,
    )

    sin_theta = np.sqrt(
        np.maximum(
            0.0,
            1.0
            -
            x**2,
        )
    )

    b_r = np.zeros_like(
        radius
    )

    b_theta = np.zeros_like(
        radius
    )

    amplitudes = (
        fit[
            "boundary_amplitudes"
        ]
    )

    for ell, amplitude in enumerate(
        amplitudes,
        start=1,
    ):
        p_l = eval_legendre(
            ell,
            x,
        )

        dp_l = (
            _legendre_derivative(
                ell,
                x,
            )
        )

        radial_factor = (
            (
                SOURCE_RADIUS_M
                /
                r_safe
            ) ** (
                ell
                +
                1
            )
            /
            r_safe
        )

        b_r += (
            (
                ell
                +
                1
            )
            *
            amplitude
            *
            radial_factor
            *
            p_l
        )

        b_theta += (
            amplitude
            *
            radial_factor
            *
            sin_theta
            *
            dp_l
        )

    b_rho = (
        b_r
        *
        sin_theta
        +
        b_theta
        *
        x
    )

    b_z = (
        b_r
        *
        x
        -
        b_theta
        *
        sin_theta
    )

    b_rho = np.where(
        valid,
        b_rho,
        0.0,
    )

    b_z = np.where(
        valid,
        b_z,
        0.0,
    )

    return (
        b_rho,
        b_z,
    )


def mirror_global_energy_gate(
    field: dict[str, Any],
    fit: dict[str, Any],
) -> dict[str, Any]:
    original_total = float(
        field[
            "field_energy_j"
        ]
    )

    new_magnetic = (
        0.5
        *
        original_total
    )

    new_electric = float(
        fit[
            "electric_total_minimum_energy_j"
        ]
    )

    total = (
        new_magnetic
        +
        new_electric
    )

    return {
        "original_a12c_magnetic_energy_j":
            original_total,

        "new_magnetic_half_energy_j":
            new_magnetic,

        "new_electric_minimum_global_energy_j":
            new_electric,

        "new_electric_exterior_energy_j":
            fit[
                "electric_exterior_energy_j"
            ],

        "new_electric_interior_energy_j":
            fit[
                "electric_interior_minimum_energy_j"
            ],

        "mixed_global_field_energy_before_1g_renormalization_j":
            total,

        "mixed_global_energy_over_a12c":
            (
                total
                /
                original_total
            ),

        "electric_source_support_radius_m":
            SOURCE_RADIUS_M,

        "true_external_standoff_preserved":
            True,

        "surface_charge_net_zero_by_no_l0":
            True,

        "surface_charge_physicalization_completed":
            False,
    }


def surface_charge_diagnostics(
    fit: dict[str, Any],
) -> dict[str, Any]:
    x, weights = np.polynomial.legendre.leggauss(
        256
    )

    jump = np.zeros_like(
        x
    )

    for ell, amplitude in enumerate(
        fit[
            "boundary_amplitudes"
        ],
        start=1,
    ):
        jump += (
            -(
                2.0
                *
                ell
                +
                1.0
            )
            *
            amplitude
            /
            (
                math.sqrt(
                    2.0
                )
                *
                SOURCE_RADIUS_M
            )
            *
            eval_legendre(
                ell,
                x,
            )
        )

    net_flux_proxy = (
        2.0
        *
        math.pi
        *
        SOURCE_RADIUS_M**2
        *
        float(
            np.sum(
                weights
                *
                jump
            )
        )
    )

    absolute_flux_proxy = (
        2.0
        *
        math.pi
        *
        SOURCE_RADIUS_M**2
        *
        float(
            np.sum(
                weights
                *
                np.abs(
                    jump
                )
            )
        )
    )

    return {
        "net_surface_charge_flux_proxy":
            net_flux_proxy,

        "absolute_surface_charge_flux_proxy":
            absolute_flux_proxy,

        "net_over_absolute":
            (
                abs(
                    net_flux_proxy
                )
                /
                absolute_flux_proxy
                if absolute_flux_proxy
                >
                0.0
                else
                0.0
            ),

        "l0_mode_present":
            False,

        "net_charge_zero_analytic":
            True,
    }


def mirror_payload_reconstruction(
    field: dict[str, Any],
    fit: dict[str, Any],
    global_energy: dict[str, Any],
) -> dict[str, Any]:
    bfit_rho, bfit_z = (
        evaluate_multipole_field(
            field,
            fit,
        )
    )

    dot_product = (
        bfit_rho
        *
        field[
            "b_rho"
        ]
        +
        bfit_z
        *
        field[
            "b_z"
        ]
    )

    sigma_mixed = (
        HBAR_C_EV_M**2
        *
        dot_product
        /
        REFERENCE_PORTAL_SCALE_EV**4
    )

    d_sigma_dz, _ = np.gradient(
        sigma_mixed,
        field[
            "h"
        ],
        field[
            "h"
        ],
        edge_order=2,
    )

    acceleration = (
        -C_LIGHT_M_S**2
        *
        d_sigma_dz
    )

    payload = (
        field[
            "payload"
        ]
    )

    payload_acceleration = (
        acceleration[
            payload
        ]
    )

    minimum = float(
        np.min(
            payload_acceleration
        )
    )

    maximum = float(
        np.max(
            payload_acceleration
        )
    )

    reference_sigma = (
        field[
            "sigma"
        ][
            payload
        ]
    )

    mixed_sigma = (
        sigma_mixed[
            payload
        ]
    )

    sigma_relative_rms = (
        float(
            np.linalg.norm(
                mixed_sigma
                -
                reference_sigma
            )
            /
            np.linalg.norm(
                reference_sigma
            )
        )
    )

    sigma_ratio = (
        mixed_sigma
        /
        reference_sigma
    )

    if minimum > 0.0:
        normalization = (
            TARGET_ACCELERATION_M_S2
            /
            minimum
        )

        normalized_energy = (
            global_energy[
                "mixed_global_field_energy_before_1g_renormalization_j"
            ]
            *
            normalization
        )

        normalized_maximum = (
            maximum
            *
            normalization
        )

    else:
        normalization = None
        normalized_energy = None
        normalized_maximum = None

    return {
        "payload_sigma_relative_rms_error":
            sigma_relative_rms,

        "payload_sigma_ratio_min":
            float(
                np.min(
                    sigma_ratio
                )
            ),

        "payload_sigma_ratio_max":
            float(
                np.max(
                    sigma_ratio
                )
            ),

        "payload_acceleration_min_before_renormalization_m_s2":
            minimum,

        "payload_acceleration_max_before_renormalization_m_s2":
            maximum,

        "whole_payload_outward_before_renormalization":
            minimum
            >
            0.0,

        "amplitude_squared_normalization_to_1g":
            normalization,

        "normalized_mixed_global_field_energy_j":
            normalized_energy,

        "normalized_payload_acceleration_min_m_s2":
            (
                TARGET_ACCELERATION_M_S2
                if normalization
                is not None
                else
                None
            ),

        "normalized_payload_acceleration_max_m_s2":
            normalized_maximum,

        "sub100j_after_1g_normalization":
            bool(
                normalized_energy
                is not None
                and
                normalized_energy
                <
                LOW_J_STRONG_TARGET_J
            ),

        "sub10kj_after_1g_normalization":
            bool(
                normalized_energy
                is not None
                and
                normalized_energy
                <
                LOW_KJ_TARGET_J
            ),
    }


def interface_orientation_diagnostics(
    field: dict[str, Any],
) -> dict[str, Any]:
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

    d_density_dz, d_density_drho = np.gradient(
        density,
        field[
            "h"
        ],
        field[
            "h"
        ],
        edge_order=2,
    )

    gradient_magnitude = np.sqrt(
        d_density_drho**2
        +
        d_density_dz**2
    )

    threshold = (
        float(
            np.max(
                gradient_magnitude
            )
        )
        *
        1.0e-8
    )

    layer = (
        gradient_magnitude
        >
        threshold
    )

    n_rho = np.zeros_like(
        density
    )

    n_z = np.zeros_like(
        density
    )

    np.divide(
        d_density_drho,
        gradient_magnitude,
        out=n_rho,
        where=layer,
    )

    np.divide(
        d_density_dz,
        gradient_magnitude,
        out=n_z,
        where=layer,
    )

    b_n = (
        field[
            "b_rho"
        ]
        *
        n_rho
        +
        field[
            "b_z"
        ]
        *
        n_z
    )

    b_n_squared = (
        b_n**2
    )

    b_t_squared = np.maximum(
        field[
            "b_squared"
        ]
        -
        b_n_squared,
        0.0,
    )

    volume_weight = (
        2.0
        *
        math.pi
        *
        field[
            "rho_grid"
        ]
        *
        field[
            "h"
        ] ** 2
    )

    gradient_weight = (
        gradient_magnitude
        *
        volume_weight
        *
        layer
    )

    normal_measure = float(
        np.sum(
            gradient_weight
            *
            b_n_squared
        )
    )

    tangent_measure = float(
        np.sum(
            gradient_weight
            *
            b_t_squared
        )
    )

    total_measure = (
        normal_measure
        +
        tangent_measure
    )

    if (
        normal_measure
        >
        0.0
        and
        tangent_measure
        >
        0.0
    ):
        optimal_ratio = math.sqrt(
            normal_measure
            /
            tangent_measure
        )
    else:
        optimal_ratio = 1.0

    baseline_driver = (
        0.5
        *
        total_measure
    )

    optimal_driver = (
        0.5
        *
        (
            normal_measure
            /
            optimal_ratio
            +
            optimal_ratio
            *
            tangent_measure
        )
    )

    optimal_driver_ratio = (
        optimal_driver
        /
        baseline_driver
    )

    optimal_field_energy_ratio = (
        field_energy_ratio_for_repartition(
            optimal_ratio
        )
    )

    ratios = np.logspace(
        -3.0,
        3.0,
        4001,
    )

    energy_ratios = (
        0.5
        *
        (
            ratios
            +
            1.0
            /
            ratios
        )
    )

    drivers = (
        0.5
        *
        (
            normal_measure
            /
            ratios
            +
            ratios
            *
            tangent_measure
        )
    )

    driver_ratios = (
        drivers
        /
        baseline_driver
    )

    pareto = []

    for cap in (
        1.10,
        1.25,
        1.50,
        2.00,
        5.00,
        10.00,
    ):
        allowed = (
            energy_ratios
            <=
            cap
        )

        if np.any(
            allowed
        ):
            allowed_indices = np.flatnonzero(
                allowed
            )

            local_index = int(
                np.argmin(
                    driver_ratios[
                        allowed
                    ]
                )
            )

            global_index = int(
                allowed_indices[
                    local_index
                ]
            )

            pareto.append(
                {
                    "field_energy_ratio_cap":
                        cap,

                    "selected_E_over_B":
                        float(
                            ratios[
                                global_index
                            ]
                        ),

                    "actual_field_energy_ratio":
                        float(
                            energy_ratios[
                                global_index
                            ]
                        ),

                    "interface_driver_ratio_vs_equal_split":
                        float(
                            driver_ratios[
                                global_index
                            ]
                        ),
                }
            )

    beta_peak = float(
        r3a_artifact()[
            "loading_structure"
        ][
            "topological_beta_peak_magnitude"
        ]
    )

    return {
        "density_model":
            PRIMARY_DENSITY_MODEL,

        "density_gradient_layer_cell_count":
            int(
                np.count_nonzero(
                    layer
                )
            ),

        "gradient_weighted_Bnormal2_fraction":
            (
                normal_measure
                /
                total_measure
            ),

        "gradient_weighted_Btangent2_fraction":
            (
                tangent_measure
                /
                total_measure
            ),

        "equal_split_interface_driver_reference":
            baseline_driver,

        "optimal_global_E_over_B_ratio_for_driver":
            optimal_ratio,

        "optimal_driver_ratio_vs_equal_split":
            optimal_driver_ratio,

        "field_energy_ratio_at_driver_optimum":
            optimal_field_energy_ratio,

        "beta_peak":
            beta_peak,

        "pareto":
            pareto,

        "simple_parallel_mirror_eliminates_interface_problem":
            False,

        "amplitude_repartition_can_reduce_interface_driver":
            bool(
                optimal_driver_ratio
                <
                1.0
            ),
    }


def decision_from_results(
    fine_fit: dict[str, Any],
    fine_mirror: dict[str, Any],
    fine_payload: dict[str, Any],
    coarse_payload: dict[str, Any],
) -> dict[str, Any]:
    fit_pass = bool(
        fine_fit[
            "relative_rms_field_residual"
        ]
        <
        FIT_RMS_PASS_MAX

        and

        fine_fit[
            "exterior_energy_relative_error"
        ]
        <
        EXTERIOR_ENERGY_RELERR_PASS_MAX
    )

    low_j = bool(
        fine_payload[
            "normalized_mixed_global_field_energy_j"
        ]
        is not None

        and

        fine_payload[
            "normalized_mixed_global_field_energy_j"
        ]
        <
        LOW_J_STRONG_TARGET_J
    )

    low_kj = bool(
        fine_payload[
            "normalized_mixed_global_field_energy_j"
        ]
        is not None

        and

        fine_payload[
            "normalized_mixed_global_field_energy_j"
        ]
        <
        LOW_KJ_TARGET_J
    )

    both_outward = bool(
        fine_payload[
            "whole_payload_outward_before_renormalization"
        ]

        and

        coarse_payload[
            "whole_payload_outward_before_renormalization"
        ]
    )

    if (
        fit_pass
        and
        both_outward
        and
        low_j
    ):
        decision = (
            "GREEN_SCOPED_R3B_GLOBAL_NEUTRAL_ELECTROSTATIC_MIRROR_"
            "COMPLETION_PRESERVES_THE_A12C_LOW_JOULE_CLASS_AND_"
            "WHOLE_PAYLOAD_OUTWARD_RESPONSE__INTERFACE_POLARIZATION_"
            "NODE_CORRIDOR_IDENTIFIED__AUTHORIZE_LIMITED_LOADED_R3C"
        )

        next_branch = (
            "032H17A12D1R3C_FINITE_PAYLOAD_LOADED_"
            "TOPOLOGICAL_EB_POLARIZATION_NODE_BVP"
        )

        r3c_authorized = True

    elif (
        fit_pass
        and
        both_outward
        and
        low_kj
    ):
        decision = (
            "YELLOW_GREEN_R3B_GLOBAL_MIRROR_COMPLETION_REMAINS_"
            "SUB10KJ_AND_PRESERVES_WHOLE_PAYLOAD_OUTWARD_SIGN__"
            "AUTHORIZE_R3C_INTERFACE_LOADED_BVP"
        )

        next_branch = (
            "032H17A12D1R3C_FINITE_PAYLOAD_LOADED_"
            "TOPOLOGICAL_EB_POLARIZATION_NODE_BVP"
        )

        r3c_authorized = True

    elif fit_pass:
        decision = (
            "YELLOW_R3B_GLOBAL_MIRROR_IS_MATHEMATICALLY_REALIZABLE_"
            "BUT_LOW_CAPACITY_ADVANTAGE_IS_NOT_YET_PRESERVED__"
            "USE_INTERFACE_AND_MULTIPOLE_DIAGNOSTICS_BEFORE_FULL_BVP"
        )

        next_branch = (
            "032H17A12D1R3B1_MIRROR_AND_POLARIZATION_REDESIGN"
        )

        r3c_authorized = False

    else:
        decision = (
            "RED_SCOPED_R3B_A12C_EXTERIOR_GLOBAL_MIRROR_"
            "RECONSTRUCTION_FAILS_NUMERICAL_OR_INTEGRABILITY_PREFLIGHT"
        )

        next_branch = (
            "BUILD_CARRYOVER_NOTES_AND_RERANK_CROSS_TOPOLOGICAL_COMPLETION"
        )

        r3c_authorized = False

    return {
        "decision":
            decision,

        "next":
            next_branch,

        "r3c_authorized":
            r3c_authorized,

        "fit_pass":
            fit_pass,

        "low_joule_class_preserved":
            low_j,

        "sub10kj_preserved":
            low_kj,

        "whole_payload_outward_on_both_grids":
            both_outward,

        "fine_global_energy_before_renormalization_j":
            fine_mirror[
                "mixed_global_field_energy_before_1g_renormalization_j"
            ],

        "fine_global_energy_after_1g_renormalization_j":
            fine_payload[
                "normalized_mixed_global_field_energy_j"
            ],
    }
