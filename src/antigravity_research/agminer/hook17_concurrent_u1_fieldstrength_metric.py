"""032H17A12C — exact-massless concurrent-U(1) field-strength metric gate.

PURPOSE
-------
A12B established a classical same-action exact massless vector with an exact
massive-Dirac vector Noether current. That result cannot inherit A10E's
quadratic vector-potential metric because Q_mu Q_nu is gauge variant under

    delta Q_mu = partial_mu lambda.

This branch therefore tests the shortest physically decisive continuation:

1. identify a useful local quadratic metric that respects exact A12B U(1);
2. impose A11A's exact direct-silence theorem for stable ordinary e/p/n matter;
3. solve a finite 1 kg / 1 m massless field-strength-metric BVP;
4. reconstruct an optimistic canonical ordinary source cost;
5. compare the resulting physical-EM-aligned portal with an existing,
   documented laboratory magnetic-field gradient before expensive loaded
   payload or complete-energy work.

MINIMAL GAUGE-INVARIANT MAGNETOSTATIC METRIC
--------------------------------------------
Use

    g_phys = exp(2 sigma) g

with

    sigma = F_X^{mu nu} F^X_{mu nu} / (2 M_X^4).

For a static purely magnetic configuration,

    F_X^2 = 2 B_X^2

so

    sigma = B_X^2 / M_X^4.

This metric:

- is exactly U(1)-gauge invariant;
- has zero first variation at F_X=0;
- has a nonzero active-state response;
- can produce nonzero invariant tidal curvature;
- gives outward acceleration when B_X^2 decreases in +z.

ORDINARY SOURCE THEOREM
-----------------------
A11A proved that a renormalizable vector charge on stable ordinary e/p/n
number currents is directly silent on every neutral atomic composition only
when

    q_n = 0
    q_p = -q_e.

Thus that current is electromagnetic-like up to normalization.

For two exactly massless canonical U(1)s coupling to the same J_EM,

    e0 A_mu J_EM^mu + gX X_mu J_EM^mu,

an orthogonal field rotation gives one physical coupled photon-like field and
one sterile field. Therefore, with no independent sterile background,

    F_X = (gX/e_phys) F_phys

and the geometric metric is equivalently an F_EM^2 portal with

    M_EM = M_X / sqrt(abs(gX/e_phys)).

IMPORTANT CORRECTION
--------------------
The A11A electron g-2 bound belonged to an independent ultralight massive
vector. It is NOT blindly transferred here. In the exactly massless
proportional-current limit, the second vector is a gauge-basis redundancy
until the metric portal distinguishes an orientation.

The metric portal instead makes ordinary electromagnetic fields themselves
an empirical probe.

FINITE BVP
----------
Reuse the A10F1 finite geometry:

    source radius = 2 m
    source J_phi = J0*(rho/Rs)*(1-r^2/Rs^2)^2
    payload = 1 kg torus
    major radius = 1 m
    minor radius = 0.2 m
    true external source/payload surface gap = 1 m.

Solve the canonical massless axisymmetric Maxwell equation

    [-d_rho^2 -(1/rho)d_rho -d_z^2 +1/rho^2] A_phi = J_phi.

With

    u = sqrt(rho) A_phi,

the sparse operator contains +3/(4 rho^2).

The source amplitude is rescaled until the least-accelerated resolved payload
point equals exactly 9.80665 m/s^2.

EMPIRICAL SANITY REFERENCE
--------------------------
FDA PMA P130029S002C reports nonclinical ASTM F2052 magnetic-force testing of
the Fluency Plus Endovascular Stent Graft in a GE Signa HDx MR system:

    B = 1.7 T
    spatial gradient = 4.7 T/m
    observed deflection < 2 degrees.

For sigma proportional to B^2, the universal acceleration scales with

    grad(B^2) = 2 B grad(B).

This is used as a high-margin empirical sanity falsifier, not claimed to be a
dedicated precision gravity experiment.

CLAIM LIMITS
------------
A red result closes only:

    A12B
    +
    stable ordinary e/p/n directly-silent source
    +
    minimal analytic magnetostatic F_X^2 universal metric.

It does NOT close:

- the exact A12B massless carrier itself;
- a genuinely source-selective microscopic current absent from payload matter;
- higher-derivative/composite/curvature portals;
- electric or parity-odd field-strength portals;
- other protected torsion/vector families;
- HOOK17 globally.

A partial energy may reject but never certify a device.
"""

from __future__ import annotations

import math
from functools import lru_cache
from typing import Any

import numpy as np
from scipy.optimize import brentq
from scipy.sparse import diags, eye, kron
from scipy.sparse.linalg import spsolve

from .hook17_concurrent_iw_exact_source import (
    h17a12b_summary,
)
from .hook17_exact_current_protection_atlas import (
    h17a11a_summary,
)


C_LIGHT_M_S = 299792458.0
HBAR_C_EV_M = 1.973269804e-7
EV_J = 1.602176634e-19

# Natural-unit conversion used only to express the field in familiar tesla.
TESLA_TO_EV2 = 195.3527712

# Low-energy electromagnetic coupling sqrt(4*pi*alpha).
ELECTROMAGNETIC_COUPLING = 0.30282212087175264
ELECTRON_MASS_EV = 510998.95

TARGET_ACCELERATION_M_S2 = 9.80665
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

REFERENCE_PORTAL_SCALE_EV = 1000.0

SOURCE_RADIUS_M = 2.0

PAYLOAD_MASS_KG = 1.0
PAYLOAD_MAJOR_RADIUS_M = 1.0
PAYLOAD_MINOR_RADIUS_M = 0.2
PAYLOAD_STANDOFF_M = 1.0

# This run is a kill-or-promote preflight rather than a promotion-quality
# final BVP. The empirical margin found below is intentionally required to be
# orders of magnitude larger than the modest numerical-discretization error.
PRODUCTION_GRID_M = 0.050
PRODUCTION_RHO_MAX_M = 12.0
PRODUCTION_Z_MIN_M = -10.0
PRODUCTION_Z_MAX_M = 13.0

COARSE_GRID_M = 0.075

LARGER_RHO_MAX_M = 14.0
LARGER_Z_MIN_M = -12.0
LARGER_Z_MAX_M = 15.0

# FDA PMA P130029S002C, Fluency Plus Endovascular Stent Graft.
FDA_MRI_B_T = 1.7
FDA_MRI_GRAD_T_PER_M = 4.7
FDA_REPORTED_DEFLECTION_DEG_MAX = 2.0

FDA_EMPIRICAL_SOURCE = (
    "FDA_PMA_P130029S002C_FLUENCY_PLUS_STENT_"
    "NONCLINICAL_ASTM_F2052_GE_SIGNA_HDX"
)

FDA_EMPIRICAL_URL = (
    "https://www.accessdata.fda.gov/"
    "cdrh_docs/pdf13/p130029s002c.pdf"
)


def payload_center_z_m() -> float:
    """Return torus center giving exactly 1 m source-surface standoff."""

    centerline_radius = (
        SOURCE_RADIUS_M
        +
        PAYLOAD_STANDOFF_M
        +
        PAYLOAD_MINOR_RADIUS_M
    )

    return math.sqrt(
        centerline_radius**2
        -
        PAYLOAD_MAJOR_RADIUS_M**2
    )


def geometric_standoff_m() -> float:
    """Return exact spherical-source to toroidal-payload minimum gap."""

    centerline_distance = math.sqrt(
        PAYLOAD_MAJOR_RADIUS_M**2
        +
        payload_center_z_m()**2
    )

    return (
        centerline_distance
        -
        PAYLOAD_MINOR_RADIUS_M
        -
        SOURCE_RADIUS_M
    )


@lru_cache(maxsize=1)
def a12c_provenance_gate() -> dict[str, Any]:
    """Require A12B green and recover A11A's ordinary-current theorem."""

    a12b = (
        h17a12b_summary()
    )

    a11a = (
        h17a11a_summary()
    )

    theorem = (
        a11a[
            "em_like_exact_ordinary_current"
        ][
            "ordinary_current_theorem"
        ]
    )

    passed = bool(
        a12b[
            "branch"
        ]
        ==
        "032H17A12B"
        and
        a12b[
            "classical_protected_same_action_massless_source_corridor_exists"
        ]
        is True
        and
        a12b[
            "canonical_source_empirical_gate_authorized"
        ]
        is True
        and
        a12b[
            "metric_gate_authorized"
        ]
        is False
        and
        a12b[
            "payload_gate_authorized"
        ]
        is False
        and
        a12b[
            "hook17_closed"
        ]
        is False
        and
        theorem[
            "q_n_zero"
        ]
        is True
        and
        theorem[
            "q_p_equals_minus_q_e"
        ]
        is True
        and
        theorem[
            "solution_em_like_up_to_overall_normalization"
        ]
        is True
    )

    return {
        "pass":
            passed,

        "a12b_branch":
            a12b[
                "branch"
            ],

        "neutral_atom_direct_silence_theorem":
            theorem,

        "ordinary_stable_payload_silent_current":
            "EM_LIKE_ONLY",
    }


@lru_cache(maxsize=1)
def exact_massless_u1_rotation_gate() -> dict[str, Any]:
    """Record the exact basis rotation for two massless U(1)s on one current."""

    return {
        "two_exactly_massless_canonical_u1s":
            True,

        "ordinary_current_direction":
            "J_EM",

        "physical_coupled_field":
            (
                "A_phys=(e0*A+gX*X)/"
                "sqrt(e0^2+gX^2)"
            ),

        "sterile_field":
            (
                "X_sterile=(-gX*A+e0*X)/"
                "sqrt(e0^2+gX^2)"
            ),

        "ordinary_source_excites_sterile_field":
            False,

        "geometric_x_component_of_physical_field":
            (
                "F_X=(gX/e_phys)*F_phys_"
                "WHEN_F_STERILE=0"
            ),

        "effective_metric_scale":
            (
                "M_EM=M_X/"
                "sqrt(abs(gX/e_phys))"
            ),

        # Important correction to the older massive-vector lane.
        "a11a_massive_vector_gminus2_bound_reused":
            False,

        "reason_massive_gminus2_not_reused":
            (
                "EXACTLY_MASSLESS_PROPORTIONAL_CURRENT_DIRECTION_"
                "IS_A_GAUGE_BASIS_ROTATION;_THE_METRIC_PORTAL_"
                "MAKES_THE_ORIENTATION_PHYSICAL_BUT_THE_PRIOR_"
                "MASSIVE_VECTOR_GMINUS2_FORMULA_DOES_NOT_TRANSFER"
            ),

        "metric_portal_turns_rotation_into_physical_em_field_portal":
            True,
    }


@lru_cache(maxsize=1)
def gauge_invariant_metric_gate() -> dict[str, Any]:
    """Identify the minimal useful magnetostatic A12B metric."""

    return {
        "a10e_q_mu_q_nu_portal_transferable_to_exact_massless_a12b":
            False,

        "failure_reason":
            (
                "Q_mu_Q_nu_IS_GAUGE_VARIANT_"
                "UNDER_DELTA_Q=PARTIAL_LAMBDA"
            ),

        "algebraic_invariant_zc_plus_cq_on_massless_null_direction":
            "ZERO",

        "minimal_magnetostatic_quadratic_gauge_invariant":
            "F_X_mn*F_X^mn",

        "metric":
            "g_phys=exp(2*sigma)*g",

        "sigma":
            "F_X^2/(2*M_X^4)",

        "static_magnetic_sigma":
            "B_X^2/M_X^4",

        "gauge_invariant":
            True,

        "off_state_first_variation_zero":
            True,

        "active_state_response_nonzero":
            True,

        "outward_sign_if_b_squared_decreases_with_plus_z":
            True,

        "field_redefinition_invariant_curvature_possible":
            True,

        "full_loaded_same_action_bvp_established":
            False,
    }


def _payload_mask(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """Return finite toroidal payload mask."""

    return (
        (
            rho
            -
            PAYLOAD_MAJOR_RADIUS_M
        ) ** 2
        +
        (
            z
            -
            payload_center_z_m()
        ) ** 2
        <=
        PAYLOAD_MINOR_RADIUS_M**2
    )


def _source_profile(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """Return compact C1 A10F1 azimuthal-current morphology."""

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


def _solve_massless_f2_bvp(
    h: float,
    rho_max_m: float,
    z_min_m: float,
    z_max_m: float,
) -> dict[str, Any]:
    """Solve massless A_phi BVP and rescale least payload point to 1 g."""

    h = float(
        h
    )

    rhos = np.arange(
        0.0,
        rho_max_m + 0.5 * h,
        h,
    )

    zs = np.arange(
        z_min_m,
        z_max_m + 0.5 * h,
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

    # After u=sqrt(rho) A_phi:
    #
    #   -u_rr -u_zz + 3/(4 rho^2) u = sqrt(rho) J_phi.
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
            nr - 1
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
            nz - 1
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

    payload = (
        _payload_mask(
            rho_grid,
            z_grid,
        )
    )

    if not np.any(
        payload
    ):
        raise RuntimeError(
            "payload unresolved on grid"
        )

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
            rho_grid > 0.0,
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

    payload_unit = (
        acceleration_unit[
            payload
        ]
    )

    local_minimum_unit = float(
        np.min(
            payload_unit
        )
    )

    if local_minimum_unit <= 0.0:
        raise RuntimeError(
            "F2 portal failed one-sided outward sign"
        )

    source_scale = math.sqrt(
        TARGET_ACCELERATION_M_S2
        /
        local_minimum_unit
    )

    acceleration = (
        source_scale**2
        *
        acceleration_unit
    )

    payload_acceleration = (
        acceleration[
            payload
        ]
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

    b_squared_scaled = (
        source_scale**2
        *
        b_squared
    )

    weights = (
        rho_grid
        *
        payload
    )

    weight_sum = float(
        np.sum(
            weights
        )
    )

    com_acceleration = float(
        np.sum(
            weights
            *
            acceleration
        )
        /
        weight_sum
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
                b_squared_scaled
            )
        )
        *
        h**2
        /
        HBAR_C_EV_M
        *
        EV_J
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

    integrated_source_ev_m = (
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

    b_tesla = (
        HBAR_C_EV_M
        *
        np.sqrt(
            b_squared_scaled
        )
        /
        TESLA_TO_EV2
    )

    b2_tesla = (
        b_tesla**2
    )

    d_b2_dz, _ = np.gradient(
        b2_tesla,
        h,
        h,
        edge_order=2,
    )

    outward_b2_gradient = (
        -d_b2_dz[
            payload
        ]
    )

    d2_sigma_dz2, _ = np.gradient(
        d_sigma_dz
        *
        source_scale**2,
        h,
        h,
        edge_order=2,
    )

    return {
        "grid_spacing_m":
            h,

        "rho_max_m":
            rho_max_m,

        "z_min_m":
            z_min_m,

        "z_max_m":
            z_max_m,

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
            (
                "J_phi=J0*(rho/Rs)*"
                "(1-r^2/Rs^2)^2"
            ),

        "source_compact":
            True,

        "source_divergence_zero_by_axisymmetry":
            True,

        "payload_mass_kg":
            PAYLOAD_MASS_KG,

        "payload_kind":
            "TORUS",

        "geometric_external_standoff_m":
            geometric_standoff_m(),

        "reference_portal_scale_ev":
            REFERENCE_PORTAL_SCALE_EV,

        "source_amplitude_e_v_per_m2":
            source_scale,

        "payload_local_acceleration_min_m_s2":
            float(
                np.min(
                    payload_acceleration
                )
            ),

        "payload_local_acceleration_max_m_s2":
            float(
                np.max(
                    payload_acceleration
                )
            ),

        "payload_com_acceleration_m_s2":
            com_acceleration,

        "strict_whole_payload_1g_pass":
            bool(
                np.min(
                    payload_acceleration
                )
                >=
                TARGET_ACCELERATION_M_S2
                *
                (
                    1.0
                    -
                    1.0e-12
                )
            ),

        "field_energy_j":
            field_energy_j,

        "source_work_j":
            source_work_j,

        "source_work_relative_error":
            (
                abs(
                    source_work_j
                    -
                    field_energy_j
                )
                /
                field_energy_j
            ),

        "integrated_canonical_source_ev_m":
            integrated_source_ev_m,

        "payload_b_tesla_min":
            float(
                np.min(
                    b_tesla[
                        payload
                    ]
                )
            ),

        "payload_b_tesla_max":
            float(
                np.max(
                    b_tesla[
                        payload
                    ]
                )
            ),

        "payload_outward_grad_b2_t2_per_m_min":
            float(
                np.min(
                    outward_b2_gradient
                )
            ),

        "payload_outward_grad_b2_t2_per_m_max":
            float(
                np.max(
                    outward_b2_gradient
                )
            ),

        "payload_sigma_max":
            float(
                np.max(
                    (
                        source_scale**2
                    )
                    *
                    sigma_unit[
                        payload
                    ]
                )
            ),

        "payload_abs_d2_sigma_dz2_max_per_m2":
            float(
                np.max(
                    np.abs(
                        d2_sigma_dz2[
                            payload
                        ]
                    )
                )
            ),

        "invariant_tidal_response_nonzero":
            bool(
                np.max(
                    np.abs(
                        d2_sigma_dz2[
                            payload
                        ]
                    )
                )
                >
                0.0
            ),

        "loaded_matter_backreaction_included":
            False,

        "complete_energy_established":
            False,
    }


@lru_cache(maxsize=1)
def massless_f2_bvp_gate() -> dict[str, Any]:
    """Return finite BVP and deliberately modest kill-gate convergence."""

    production = (
        _solve_massless_f2_bvp(
            PRODUCTION_GRID_M,
            PRODUCTION_RHO_MAX_M,
            PRODUCTION_Z_MIN_M,
            PRODUCTION_Z_MAX_M,
        )
    )

    coarse = (
        _solve_massless_f2_bvp(
            COARSE_GRID_M,
            PRODUCTION_RHO_MAX_M,
            PRODUCTION_Z_MIN_M,
            PRODUCTION_Z_MAX_M,
        )
    )

    larger = (
        _solve_massless_f2_bvp(
            PRODUCTION_GRID_M,
            LARGER_RHO_MAX_M,
            LARGER_Z_MIN_M,
            LARGER_Z_MAX_M,
        )
    )

    grid_energy_relerr = (
        abs(
            production[
                "field_energy_j"
            ]
            -
            coarse[
                "field_energy_j"
            ]
        )
        /
        production[
            "field_energy_j"
        ]
    )

    grid_source_relerr = (
        abs(
            production[
                "integrated_canonical_source_ev_m"
            ]
            -
            coarse[
                "integrated_canonical_source_ev_m"
            ]
        )
        /
        production[
            "integrated_canonical_source_ev_m"
        ]
    )

    domain_energy_relerr = (
        abs(
            production[
                "field_energy_j"
            ]
            -
            larger[
                "field_energy_j"
            ]
        )
        /
        production[
            "field_energy_j"
        ]
    )

    preflight_converged = bool(
        grid_energy_relerr
        <
        0.06
        and
        grid_source_relerr
        <
        0.06
        and
        domain_energy_relerr
        <
        0.03
        and
        production[
            "source_work_relative_error"
        ]
        <
        1.0e-3
    )

    return {
        "production":
            production,

        "coarse":
            coarse,

        "larger_domain":
            larger,

        "grid_energy_relative_difference":
            grid_energy_relerr,

        "grid_source_relative_difference":
            grid_source_relerr,

        "domain_energy_relative_difference":
            domain_energy_relerr,

        "preflight_convergence_pass":
            preflight_converged,

        # This branch uses a >100x empirical kill margin.
        # It is not a promotion-quality precision BVP.
        "promotion_quality_precision_bvp":
            False,
    }


@lru_cache(maxsize=1)
def canonical_ordinary_source_cost_gate() -> dict[str, Any]:
    """Return optimistic charge-neutral EM-current kinematic lower bound."""

    production = (
        massless_f2_bvp_gate()[
            "production"
        ]
    )

    energy_reference = float(
        production[
            "field_energy_j"
        ]
    )

    current_reference = float(
        production[
            "integrated_canonical_source_ev_m"
        ]
    )

    def field_energy(
        scale_ev: float,
    ) -> float:
        return (
            energy_reference
            *
            (
                scale_ev
                /
                REFERENCE_PORTAL_SCALE_EV
            ) ** 4
        )

    def integrated_current(
        scale_ev: float,
    ) -> float:
        return (
            current_reference
            *
            (
                scale_ev
                /
                REFERENCE_PORTAL_SCALE_EV
            ) ** 2
        )

    # Charge-neutral counterstreaming e-/e+:
    #
    #   charge density cancels,
    #   spatial current adds.
    #
    # Pair current = 2 e beta.
    # Pair energy  = 2 gamma m_e.
    #
    # gamma/beta is minimized at beta=1/sqrt(2), with value 2.
    beta_opt = (
        1.0
        /
        math.sqrt(
            2.0
        )
    )

    gamma_opt = math.sqrt(
        2.0
    )

    gamma_over_beta_opt = 2.0

    def source_energy_floor(
        scale_ev: float,
    ) -> float:
        return (
            gamma_over_beta_opt
            *
            ELECTRON_MASS_EV
            *
            integrated_current(
                scale_ev
            )
            /
            (
                ELECTROMAGNETIC_COUPLING
                *
                HBAR_C_EV_M
            )
            *
            EV_J
        )

    # Field-only ceiling is intentionally the most generous possible
    # value of M_EM.  Any real source/support cost lowers it.
    field_only_scale = (
        REFERENCE_PORTAL_SCALE_EV
        *
        (
            STRICT_COMPLETE_OPERATING_TARGET_J
            /
            energy_reference
        ) ** 0.25
    )

    partial_scale = brentq(
        lambda scale_ev:
            (
                field_energy(
                    scale_ev
                )
                +
                source_energy_floor(
                    scale_ev
                )
                -
                STRICT_COMPLETE_OPERATING_TARGET_J
            ),
        REFERENCE_PORTAL_SCALE_EV,
        2.0e5,
    )

    current_at_partial = (
        integrated_current(
            partial_scale
        )
    )

    source_floor_at_partial = (
        source_energy_floor(
            partial_scale
        )
    )

    field_at_partial = (
        field_energy(
            partial_scale
        )
    )

    pair_count = (
        current_at_partial
        /
        (
            2.0
            *
            ELECTROMAGNETIC_COUPLING
            *
            beta_opt
            *
            HBAR_C_EV_M
        )
    )

    return {
        "source_model":
            (
                "OPTIMISTIC_COUNTERSTREAMING_"
                "ELECTRON_POSITRON_VECTOR_CURRENT"
            ),

        "source_net_charge_density_zero":
            True,

        "beta_kinematic_optimum":
            beta_opt,

        "gamma_kinematic_optimum":
            gamma_opt,

        "gamma_over_beta_minimum":
            gamma_over_beta_opt,

        "field_only_strict_10mj_portal_scale_ev":
            field_only_scale,

        "field_plus_kinematic_source_strict_10mj_portal_scale_ev":
            partial_scale,

        "field_energy_at_partial_ceiling_j":
            field_at_partial,

        "optimistic_source_energy_floor_at_partial_ceiling_j":
            source_floor_at_partial,

        "partial_total_j":
            (
                field_at_partial
                +
                source_floor_at_partial
            ),

        "optimistic_pair_count_at_partial_ceiling":
            pair_count,

        "support_confinement_annihilation_control_included":
            False,

        "complete_energy_established":
            False,

        "canonical_source_cost_itself_kills_sub10mj_preflight":
            False,
    }


@lru_cache(maxsize=1)
def fda_mri_empirical_sanity_gate() -> dict[str, Any]:
    """Compare weakest sub-10MJ EM-aligned portal with FDA MR field."""

    production = (
        massless_f2_bvp_gate()[
            "production"
        ]
    )

    source_cost = (
        canonical_ordinary_source_cost_gate()
    )

    # Deliberately choose FIELD-ONLY ceiling.
    # This maximizes M_EM and therefore minimizes the predicted ambient-field
    # effect. Any complete-energy accounting only strengthens the comparison.
    scale_ev = float(
        source_cost[
            "field_only_strict_10mj_portal_scale_ev"
        ]
    )

    scale_ratio = (
        scale_ev
        /
        REFERENCE_PORTAL_SCALE_EV
    )

    device_grad_b2_min = (
        production[
            "payload_outward_grad_b2_t2_per_m_min"
        ]
        *
        scale_ratio**4
    )

    device_b_min = (
        production[
            "payload_b_tesla_min"
        ]
        *
        scale_ratio**2
    )

    device_b_max = (
        production[
            "payload_b_tesla_max"
        ]
        *
        scale_ratio**2
    )

    fda_grad_b2 = (
        2.0
        *
        FDA_MRI_B_T
        *
        FDA_MRI_GRAD_T_PER_M
    )

    acceleration_ratio = (
        fda_grad_b2
        /
        device_grad_b2_min
    )

    predicted_universal_acceleration = (
        acceleration_ratio
        *
        TARGET_ACCELERATION_M_S2
    )

    universal_deflection_deg = math.degrees(
        math.atan(
            acceleration_ratio
        )
    )

    strong_inconsistency = bool(
        acceleration_ratio
        >
        100.0
        and
        device_b_max
        <
        0.2
        and
        FDA_REPORTED_DEFLECTION_DEG_MAX
        <=
        2.0
    )

    return {
        "candidate_scale_chosen_maximally_favorable_field_only":
            True,

        "candidate_effective_em_portal_scale_ev":
            scale_ev,

        "candidate_payload_b_tesla_min":
            device_b_min,

        "candidate_payload_b_tesla_max":
            device_b_max,

        "candidate_min_grad_b2_t2_per_m_for_1g":
            device_grad_b2_min,

        "fda_reference":
            FDA_EMPIRICAL_SOURCE,

        "fda_reference_url":
            FDA_EMPIRICAL_URL,

        "fda_b_tesla":
            FDA_MRI_B_T,

        "fda_spatial_gradient_t_per_m":
            FDA_MRI_GRAD_T_PER_M,

        "fda_grad_b2_t2_per_m":
            fda_grad_b2,

        "fda_reported_deflection_deg_less_than":
            FDA_REPORTED_DEFLECTION_DEG_MAX,

        "fda_grad_b2_over_candidate_1g_gradient":
            acceleration_ratio,

        "portal_predicted_universal_acceleration_m_s2_at_fda_field_gradient":
            predicted_universal_acceleration,

        "portal_predicted_universal_acceleration_in_g":
            acceleration_ratio,

        "diagnostic_universal_deflection_deg_if_transverse_to_gravity":
            universal_deflection_deg,

        "dedicated_gravity_experiment":
            False,

        "empirical_sanity_inconsistent_by_more_than_100x":
            strong_inconsistency,
    }


@lru_cache(maxsize=1)
def h17a12c_summary() -> dict[str, Any]:
    """Return conservative A12C decision."""

    provenance = (
        a12c_provenance_gate()
    )

    rotation = (
        exact_massless_u1_rotation_gate()
    )

    metric = (
        gauge_invariant_metric_gate()
    )

    bvp = (
        massless_f2_bvp_gate()
    )

    source = (
        canonical_ordinary_source_cost_gate()
    )

    empirical = (
        fda_mri_empirical_sanity_gate()
    )

    reduced_metric_green = bool(
        provenance[
            "pass"
        ]
        and
        metric[
            "gauge_invariant"
        ]
        and
        metric[
            "off_state_first_variation_zero"
        ]
        and
        bvp[
            "preflight_convergence_pass"
        ]
        and
        bvp[
            "production"
        ][
            "strict_whole_payload_1g_pass"
        ]
        and
        math.isclose(
            bvp[
                "production"
            ][
                "geometric_external_standoff_m"
            ],
            1.0,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )
        and
        bvp[
            "production"
        ][
            "invariant_tidal_response_nonzero"
        ]
    )

    ordinary_minimal_route_closed = bool(
        reduced_metric_green
        and
        rotation[
            "metric_portal_turns_rotation_into_physical_em_field_portal"
        ]
        and
        empirical[
            "empirical_sanity_inconsistent_by_more_than_100x"
        ]
    )

    decision = (
        (
            "RED_SCOPED_A12C_A12B_MASSLESS_CARRIER_AND_"
            "GAUGE_INVARIANT_F2_METRIC_HAVE_A_FINITE_1G_1M_"
            "REDUCED_EFT_WITNESS__BUT_STABLE_ORDINARY_"
            "PAYLOAD_SILENT_SOURCE_IS_EM_LIKE_AND_THE_RESULTING_"
            "MINIMAL_F2_PHOTON_ALIGNED_PORTAL_FAILS_EXISTING_"
            "MRI_FIELD_GRADIENT_SANITY_BY_ORDERS_OF_MAGNITUDE__"
            "PIVOT_SOURCE_OR_FAMILY"
        )
        if ordinary_minimal_route_closed
        else
        "YELLOW_A12C_REQUIRES_REVIEW_OR_SURVIVING_ORDINARY_F2_CORRIDOR"
    )

    return {
        "branch":
            "032H17A12C",

        "decision":
            decision,

        "a12b_provenance":
            provenance,

        "exact_massless_u1_rotation":
            rotation,

        "gauge_invariant_metric":
            metric,

        "massless_f2_finite_payload_bvp":
            bvp,

        "canonical_ordinary_source_cost":
            source,

        "fda_mri_empirical_sanity":
            empirical,

        "gauge_invariant_massless_f2_reduced_eft_1g_1m_witness":
            reduced_metric_green,

        "stable_ordinary_payload_silent_current_is_em_like":
            True,

        "ordinary_em_like_minimal_f2_a12b_realization_closed":
            ordinary_minimal_route_closed,

        "a12b_exact_massless_carrier_closed":
            False,

        "nonordinary_source_a12b_completion_closed":
            False,

        "higher_derivative_or_composite_metric_portal_closed":
            False,

        "all_field_strength_metric_portals_closed":
            False,

        "metric_gate_authorized_for_closed_ordinary_route":
            False,

        "payload_gate_authorized_for_closed_ordinary_route":
            False,

        "complete_energy_optimization_authorized":
            False,

        "hook17_closed":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "next":
            (
                "032H17A12D_PROTECTED_SOURCE_FAMILY_RERANK_"
                "AFTER_ORDINARY_A12B_F2_CLOSEOUT"
                if ordinary_minimal_route_closed
                else
                "REVIEW_A12C_SURVIVING_SOURCE_METRIC_CORRIDOR"
            ),

        "stop_rule":
            (
                "DO_NOT_OPTIMIZE_THE_CLOSED_ORDINARY_EM_LIKE_A12B_F2_"
                "ROUTE;_PRESERVE_A12B_AS_CARRIER_KNOWLEDGE_AND_REQUIRE_"
                "A_GENUINELY_SOURCE_SELECTIVE_MICROSCOPIC_CURRENT_OR_"
                "DIFFERENT_PROTECTED_FAMILY_BEFORE_NEW_PAYLOAD_OR_"
                "ENERGY_WORK"
            ),
    }
