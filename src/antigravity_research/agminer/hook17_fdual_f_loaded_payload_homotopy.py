"""032H17A12D1R3C — finite-payload loaded topological E/B homotopy.

PURPOSE
-------
R3A established that the linear topological physical-metric portal

    sigma = (F *F)/(2 M^4)

preserves the ideal A12C invariant-per-field-energy efficiency while removing
the fatal leading uniform-bulk F^2 matter loading.

R3B then established a globally realizable, net-neutral mixed E/B completion
with

    minimum whole-payload acceleration = 1 g
    true external stand-off = 1 m
    canonical field energy ~ 1.54 J

before finite same-action payload loading is solved.

R3C is the final exploratory run before session closeout.

It asks the decisive finite-matter question:

    With the R3B source configuration held fixed, what happens as the actual
    finite-payload topological matter coupling is turned continuously from
    zero to full strength?

The run is deliberately diagnostic.

It does NOT immediately optimize a new field.

Instead it tells us:

1. whether the simple R3B mirror survives full payload loading;
2. if not, at what loading fraction it fails;
3. whether failure is sign loss, energy amplification, or near-singularity;
4. how much interface-coupling suppression a polarization-node descendant
   would need;
5. whether the required suppression appears mild, severe, or extreme;
6. what the field + matter-interaction capacity would be if the loaded
   configuration remains outward.

----------------------------------------------------------------------
LEADING STATIC SAME-ACTION SYSTEM
----------------------------------------------------------------------

R3A gave, up to the declared sign convention,

    nabla_mu F^(mu nu)
        -
    (partial_mu beta) *F^(mu nu)
        =
    J^nu,

with

    beta = 2 exp(4 sigma) T / M^4.

For nonrelativistic matter,

    T ~= -rho_E.

At the A12C normalization sigma ~ 1e-16, so

    exp(4 sigma) - 1 ~ 1e-16,

and R3A explicitly found the exact nonlinear uniform-bulk residual at the
~1e-11 level.

R3C therefore solves the leading loaded system with beta fixed by the payload
density profile.

The omitted exp(4 sigma) feedback remains separately recorded and is far
below the interface effect being tested.

----------------------------------------------------------------------
AXISYMMETRIC STATIC POTENTIALS
----------------------------------------------------------------------

Use

    E = -grad Phi,

and

    A = A_phi e_phi,

so

    B_rho = -partial_z A_phi,

    B_z
        =
    partial_rho A_phi
        +
    A_phi/rho.

The scalar electric operator is

    K_E Phi = -laplacian Phi.

The azimuthal magnetic operator is

    K_B A_phi
        =
    -partial_rho^2 A_phi
    -partial_z^2 A_phi
    -(1/rho) partial_rho A_phi
    +A_phi/rho^2.

The topological coupling is localized entirely where grad(beta) != 0.

That is the key computational simplification.

----------------------------------------------------------------------
EXACT DISCRETE SAME-ACTION RECIPROCITY
----------------------------------------------------------------------

The electric-to-magnetic and magnetic-to-electric coupling blocks are not
constructed independently.

R3C first discretizes the Gauss-side topological operator C and then defines

    D = W_B^-1 C^T W_E,

where W_E and W_B are the cylindrical radial integration weights.

Therefore

    W_B D = C^T W_E

exactly at the discrete level.

This is the finite-grid same-action reciprocity identity.

It prevents a numerically convenient but action-inconsistent pair of loaded
equations from entering the result.

----------------------------------------------------------------------
LOW-RANK INTERFACE SOLVE
----------------------------------------------------------------------

The density is constant in the payload bulk and zero outside, with only a C1
transition layer.

Therefore C and D have nonzero rows only in that thin layer.

Let

    K0 = diag(K_E, K_B)

and

    L = [[0, C],
         [D, 0]].

The loaded deviation from the R3B field obeys

    (K0 + lambda L) delta_x
        =
    -lambda L x0,

where lambda is the payload-loading homotopy parameter.

Instead of factorizing the full coupled ~2N system for every lambda, R3C uses
the exact low-rank Woodbury reduction onto the active interface rows.

Thus the physically important loaded problem becomes a small dense Schur
system after two ordinary elliptic factorizations.

This makes it practical to inspect many loading strengths and also exposes
near-singular interface response directly through the reduced condition
number.

----------------------------------------------------------------------
LOADING HOMOTOPY
----------------------------------------------------------------------

The declared sequence is

    lambda =
        0
        1e-4
        3e-4
        1e-3
        3e-3
        1e-2
        3e-2
        1e-1
        3e-1
        1.

Interpretation:

    lambda = 0
        R3B unloaded global mirror.

    lambda = 1
        full optimistic finite 1 kg payload density.

If the minimum payload acceleration changes sign, amplitude rescaling cannot
repair the field morphology.

If the minimum remains positive, source amplitude can be rescaled because the
leading loaded equations remain linear in source amplitude:

    fields ~ s
    sigma ~ s^2
    acceleration ~ s^2
    canonical energy ~ s^2.

R3C reports the normalized 1-g capacity accordingly.

----------------------------------------------------------------------
ENERGY LEDGER REPORTED HERE
----------------------------------------------------------------------

Canonical field energy:

    E_field
        =
    integral
        (E^2 + B^2)/2
        dV.

The beta E dot B term changes constitutive response but does not contribute to
the canonical Maxwell field-energy density.

Leading finite-matter conformal interaction:

    Delta E_matter
        =
    integral rho_m c^2 [exp(sigma)-1] dV.

R3C reports:

    signed matter shift;
    absolute matter-interaction magnitude;
    E_field + |Delta E_matter|.

This is STILL NOT complete operating energy.

Missing terms include:

    microscopic charge/current source energy;
    source support/confinement;
    parity/CP completion;
    activation/control;
    radiation/reaction;
    quantum/RG/UV;
    empirical bounds;
    full nonlinear gravity;
    off-state implementation.

----------------------------------------------------------------------
IMPORTANT POLARIZATION-NODE CORRECTION
----------------------------------------------------------------------

R3B found

    B_normal^2 fraction   ~= 0.503
    B_tangent^2 fraction  ~= 0.497

in the density-gradient layer.

Therefore the existing R3B parallel-mirror field is roughly 45 degrees to
the interface normal in an RMS sense.

To establish the exact large-beta node geometry

    E normal,
    B tangent,

requires a gross field reorientation of roughly 45 degrees.

The previously reported

    4.59 degrees across the 0.1 m taper

is NOT that gross reorientation.

It is the additional node-centered polarization change needed across the
finite taper to generate a 1-g gradient once a near-orthogonal node texture
already exists.

R3C prints both numbers separately.

----------------------------------------------------------------------
INTERFACE-SUPPRESSION TARGET
----------------------------------------------------------------------

If the simple full-loading mirror fails, the homotopy still provides a highly
useful design number.

Suppose whole-payload outward sign survives only through

    lambda <= lambda_crit.

Then a future polarization-node realization needs, very roughly, to suppress
the effective dangerous interface coupling to

    q_interface <= lambda_crit

of the simple-mirror value.

The required cancellation fraction is then approximately

    1 - lambda_crit.

For intuition only, if residual interface coupling scales linearly with small
angular displacement from the exact node, R3C also reports

    delta_theta_node ~ asin(lambda_crit).

This is NOT a rigorous Maxwell construction.

It is a quantitative target for the next-session source design.

----------------------------------------------------------------------
SIGN-CONVENTION AUDIT
----------------------------------------------------------------------

The primary lane uses beta = 2T/M^4 with T<0 together with the declared
same-action discrete bilinear.

At full loading R3C also solves the opposite overall topological sign.

This does not replace derivation.

It checks that any claimed catastrophic or favorable result is not merely an
unnoticed sign-convention artifact.

----------------------------------------------------------------------
CLAIM LIMITS
----------------------------------------------------------------------

Even a green R3C does NOT establish:

- physicalized surface charge;
- microscopic source realization;
- parity/CP completion;
- complete interacting hyperbolicity;
- nonlinear stability;
- quantum naturalness;
- empirical viability;
- complete <10 MJ operating energy;
- replacement of 006D;
- a practical device.

CLAIM CLASSIFICATION
--------------------
PROJECT_FINITE_PAYLOAD_TOPOLOGICAL_LOADING_HOMOTOPY_PREFLIGHT
"""

from __future__ import annotations

import gc
import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from scipy.sparse import (
    coo_matrix,
    csr_matrix,
    diags,
    eye,
    kron,
)
from scipy.sparse.linalg import (
    splu,
    spsolve,
)

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
    TARGET_ACCELERATION_M_S2,
    _payload_mask,
    _source_profile,
)

from .hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    loading_coefficient_z,
    payload_density_profile_kg_m3,
)

from .hook17_fdual_f_global_mirror_prefight import (
    PRIMARY_FIT_RADIUS_M,
    PRIMARY_LMAX,
    PRODUCTION_RHO_MAX_M,
    PRODUCTION_Z_MAX_M,
    PRODUCTION_Z_MIN_M,
    fit_exterior_multipoles,
)


BRANCH = "032H17A12D1R3C"

GRID_SPACINGS_M = (
    0.075,
    0.050,
)

LOADING_HOMOTOPY = (
    0.0,
    1.0e-4,
    3.0e-4,
    1.0e-3,
    3.0e-3,
    1.0e-2,
    3.0e-2,
    1.0e-1,
    3.0e-1,
    1.0,
)

GREEN_FIELD_PLUS_ABS_MATTER_J = 100.0
YELLOW_FIELD_PLUS_ABS_MATTER_J = 10000.0

REDUCED_CONDITION_WARN = 1.0e10
REDUCED_CONDITION_FAIL = 1.0e14

COUPLING_GRADIENT_RELATIVE_THRESHOLD = 1.0e-10

GREEN_SOLVE_RELATIVE_RESIDUAL = 1.0e-8

R3A_EXACT_BULK_RESIDUAL_MAX = 1.0e-8


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
def r3a_artifact() -> dict[str, Any]:
    return _load_json(
        "032h17a12d1r3a_hook17_fdual_f_topological_loading_summary.json"
    )


@lru_cache(maxsize=1)
def r3b_artifact() -> dict[str, Any]:
    return _load_json(
        "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json"
    )


def provenance_gate() -> dict[str, Any]:
    r3a = (
        r3a_artifact()
    )

    r3b = (
        r3b_artifact()
    )

    fine = (
        r3b[
            "grid_results"
        ][
            "0.05"
        ]
    )

    pass_gate = bool(
        r3a[
            "structural_rescue_survives_cheap_gate"
        ]
        is True

        and

        r3a[
            "loading_structure"
        ][
            "exact_uniform_bulk_nonlinear_principal_proxy_peak"
        ]
        <
        R3A_EXACT_BULK_RESIDUAL_MAX

        and

        r3b[
            "r3c_authorized"
        ]
        is True

        and

        r3b[
            "low_joule_class_preserved"
        ]
        is True

        and

        r3b[
            "whole_payload_outward_on_both_grids"
        ]
        is True

        and

        fine[
            "surface_charge"
        ][
            "net_charge_zero_analytic"
        ]
        is True
    )

    return {
        "pass":
            pass_gate,

        "r3a_structural_rescue_survives":
            r3a[
                "structural_rescue_survives_cheap_gate"
            ],

        "r3a_exact_bulk_residual":
            r3a[
                "loading_structure"
            ][
                "exact_uniform_bulk_nonlinear_principal_proxy_peak"
            ],

        "r3b_low_joule_class_preserved":
            r3b[
                "low_joule_class_preserved"
            ],

        "r3b_fine_preloaded_field_energy_j":
            fine[
                "payload_reconstruction"
            ][
                "normalized_mixed_global_field_energy_j"
            ],

        "r3b_fine_whole_payload_outward":
            fine[
                "payload_reconstruction"
            ][
                "whole_payload_outward_before_renormalization"
            ],

        "r3b_net_electric_charge_zero":
            fine[
                "surface_charge"
            ][
                "net_charge_zero_analytic"
            ],

        "r3b_parity_completed":
            r3b[
                "parity_cp_completed"
            ],

        "r3b_surface_charge_physicalized":
            r3b[
                "surface_charge_physicalized"
            ],
    }


def node_geometry_burden() -> dict[str, Any]:
    r3b = (
        r3b_artifact()
    )

    fine = (
        r3b[
            "grid_results"
        ][
            "0.05"
        ]
    )

    interface = (
        fine[
            "interface_orientation"
        ]
    )

    node = (
        r3b[
            "polarization_node_corridor"
        ]
    )

    normal_fraction = float(
        interface[
            "gradient_weighted_Bnormal2_fraction"
        ]
    )

    tangent_fraction = float(
        interface[
            "gradient_weighted_Btangent2_fraction"
        ]
    )

    rms_cos_normal = math.sqrt(
        max(
            min(
                normal_fraction,
                1.0,
            ),
            0.0,
        )
    )

    b_to_normal_rad = math.acos(
        rms_cos_normal
    )

    b_rotation_to_tangent_rad = (
        math.pi
        /
        2.0
        -
        b_to_normal_rad
    )

    e_rotation_to_normal_rad = (
        b_to_normal_rad
    )

    gross_rotation_deg = max(
        math.degrees(
            b_rotation_to_tangent_rad
        ),
        math.degrees(
            e_rotation_to_normal_rad
        ),
    )

    return {
        "r3b_gradient_weighted_Bnormal2_fraction":
            normal_fraction,

        "r3b_gradient_weighted_Btangent2_fraction":
            tangent_fraction,

        "r3b_rms_B_angle_to_interface_normal_deg":
            math.degrees(
                b_to_normal_rad
            ),

        "r3b_B_rotation_needed_to_be_tangent_deg":
            math.degrees(
                b_rotation_to_tangent_rad
            ),

        "r3b_E_rotation_needed_to_be_normal_deg":
            math.degrees(
                e_rotation_to_normal_rad
            ),

        "approx_gross_reorientation_to_establish_node_deg":
            gross_rotation_deg,

        "node_centered_additional_rotation_across_taper_deg":
            node[
                "rotation_angle_across_taper_deg"
            ],

        "important_interpretation":
            (
                "THE_4P59_DEG_NUMBER_IS_THE_ADDITIONAL_NODE_CENTERED_"
                "CHANGE_ACROSS_THE_TAPER_NOT_THE_GROSS_ROTATION_FROM_"
                "THE_R3B_PARALLEL_MIRROR_TO_THE_NULL_GEOMETRY"
            ),
    }


def source_amplitude_factor_for_one_g(
    minimum_acceleration_m_s2: float,
) -> float | None:
    minimum = float(
        minimum_acceleration_m_s2
    )

    if minimum <= 0.0:
        return None

    return math.sqrt(
        TARGET_ACCELERATION_M_S2
        /
        minimum
    )


def energy_factor_for_one_g(
    minimum_acceleration_m_s2: float,
) -> float | None:
    minimum = float(
        minimum_acceleration_m_s2
    )

    if minimum <= 0.0:
        return None

    return (
        TARGET_ACCELERATION_M_S2
        /
        minimum
    )


def critical_loading_fraction(
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    usable = [
        row
        for row in rows
        if row[
            "solve_success"
        ]
        and
        row[
            "minimum_payload_acceleration_m_s2"
        ]
        is not None
    ]

    if not usable:
        return {
            "full_loading_outward":
                False,

            "critical_loading_fraction":
                None,

            "critical_loading_is_lower_bound":
                False,

            "sign_crossing_found":
                False,
        }

    full = [
        row
        for row in usable
        if math.isclose(
            float(
                row[
                    "loading_fraction"
                ]
            ),
            1.0,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
    ]

    if (
        full
        and
        float(
            full[
                0
            ][
                "minimum_payload_acceleration_m_s2"
            ]
        )
        >
        0.0
    ):
        return {
            "full_loading_outward":
                True,

            "critical_loading_fraction":
                1.0,

            "critical_loading_is_lower_bound":
                True,

            "sign_crossing_found":
                False,
        }

    previous = None

    for row in usable:
        lam = float(
            row[
                "loading_fraction"
            ]
        )

        accel = float(
            row[
                "minimum_payload_acceleration_m_s2"
            ]
        )

        if previous is not None:
            prev_lam = float(
                previous[
                    "loading_fraction"
                ]
            )

            prev_accel = float(
                previous[
                    "minimum_payload_acceleration_m_s2"
                ]
            )

            if (
                prev_accel
                >
                0.0
                and
                accel
                <=
                0.0
            ):
                if accel == prev_accel:
                    crossing = prev_lam
                else:
                    crossing = (
                        prev_lam
                        +
                        (
                            0.0
                            -
                            prev_accel
                        )
                        *
                        (
                            lam
                            -
                            prev_lam
                        )
                        /
                        (
                            accel
                            -
                            prev_accel
                        )
                    )

                return {
                    "full_loading_outward":
                        False,

                    "critical_loading_fraction":
                        crossing,

                    "critical_loading_is_lower_bound":
                        False,

                    "sign_crossing_found":
                        True,

                    "bracket_low":
                        prev_lam,

                    "bracket_high":
                        lam,
                }

        previous = row

    positive_lambdas = [
        float(
            row[
                "loading_fraction"
            ]
        )
        for row in usable
        if float(
            row[
                "minimum_payload_acceleration_m_s2"
            ]
        )
        >
        0.0
    ]

    if positive_lambdas:
        return {
            "full_loading_outward":
                False,

            "critical_loading_fraction":
                max(
                    positive_lambdas
                ),

            "critical_loading_is_lower_bound":
                True,

            "sign_crossing_found":
                False,
        }

    return {
        "full_loading_outward":
            False,

        "critical_loading_fraction":
            0.0,

        "critical_loading_is_lower_bound":
            False,

        "sign_crossing_found":
            False,
    }


def suppression_target_from_critical_fraction(
    critical_fraction: float | None,
) -> dict[str, Any]:
    if critical_fraction is None:
        return {
            "effective_interface_fraction_target":
                None,

            "minimum_interface_cancellation_fraction":
                None,

            "heuristic_node_angular_tolerance_deg":
                None,
        }

    q = max(
        min(
            float(
                critical_fraction
            ),
            1.0,
        ),
        0.0,
    )

    return {
        "effective_interface_fraction_target":
            q,

        "minimum_interface_cancellation_fraction":
            1.0
            -
            q,

        "heuristic_node_angular_tolerance_deg":
            math.degrees(
                math.asin(
                    q
                )
            ),

        "angular_tolerance_is_rigorous":
            False,

        "interpretation":
            (
                "SMALL_ANGLE_LINEAR_COUPLING_HEURISTIC_ONLY;"
                "_NOT_A_MAXWELL_SOURCE_CONSTRUCTION"
            ),
    }


def claim_policy_gate() -> dict[str, Any]:
    return {
        "final_exploratory_run_before_session_notes":
            True,

        "same_action_discrete_reciprocity_required":
            True,

        "full_payload_loading_tested":
            True,

        "source_amplitude_only_cannot_fix_negative_acceleration_sign":
            True,

        "parity_cp_completed":
            False,

        "surface_charge_physicalized":
            False,

        "microscopic_source_completed":
            False,

        "full_interacting_hyperbolicity_certified":
            False,

        "nonlinear_stability_certified":
            False,

        "quantum_naturalness_certified":
            False,

        "empirical_consistency_certified":
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

        "session_closeout_ready_after_run":
            True,
    }


def _a12c_potential_field(
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

    a_phi_unit = np.zeros(
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

    a_phi_unit[
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
        a_phi_unit,
        h,
        h,
        edge_order=2,
    )

    b_rho_unit = (
        -d_a_dz
    )

    a_over_rho = np.zeros_like(
        a_phi_unit
    )

    np.divide(
        a_phi_unit,
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
            "A12C reconstruction lost whole-payload outward sign"
        )

    scale = math.sqrt(
        TARGET_ACCELERATION_M_S2
        /
        minimum_unit
    )

    a_phi = (
        scale
        *
        a_phi_unit
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

        "a_phi":
            a_phi,

        "b_rho":
            b_rho,

        "b_z":
            b_z,

        "b_squared":
            b_squared,

        "field_energy_j":
            field_energy_j,

        "exterior_energy_j":
            exterior_energy_j,
    }


def _construct_global_mirror_phi(
    field: dict[str, Any],
    fit: dict[str, Any],
) -> np.ndarray:
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

    x = np.ones_like(
        radius
    )

    np.divide(
        z,
        radius,
        out=x,
        where=
            radius
            >
            0.0,
    )

    x = np.clip(
        x,
        -1.0,
        1.0,
    )

    from scipy.special import eval_legendre

    phi = np.zeros_like(
        radius
    )

    amplitudes = (
        fit[
            "boundary_amplitudes"
        ]
    )

    exterior = (
        radius
        >=
        SOURCE_RADIUS_M
    )

    interior = (
        ~exterior
    )

    radius_safe = np.where(
        radius
        >
        0.0,
        radius,
        1.0,
    )

    for ell, amplitude in enumerate(
        amplitudes,
        start=1,
    ):
        p_l = eval_legendre(
            ell,
            x,
        )

        psi_mode = np.zeros_like(
            radius
        )

        psi_mode[
            exterior
        ] = (
            amplitude
            *
            (
                SOURCE_RADIUS_M
                /
                radius_safe[
                    exterior
                ]
            ) ** (
                ell
                +
                1
            )
            *
            p_l[
                exterior
            ]
        )

        psi_mode[
            interior
        ] = (
            amplitude
            *
            (
                radius[
                    interior
                ]
                /
                SOURCE_RADIUS_M
            ) ** ell
            *
            p_l[
                interior
            ]
        )

        phi += (
            -psi_mode
            /
            math.sqrt(
                2.0
            )
        )

    return phi


def _fields_from_potentials(
    phi: np.ndarray,
    a_phi: np.ndarray,
    rho_grid: np.ndarray,
    h: float,
) -> dict[str, np.ndarray]:
    d_phi_dz, d_phi_drho = np.gradient(
        phi,
        h,
        h,
        edge_order=2,
    )

    e_rho = (
        -d_phi_drho
    )

    e_z = (
        -d_phi_dz
    )

    d_a_dz, d_a_drho = np.gradient(
        a_phi,
        h,
        h,
        edge_order=2,
    )

    b_rho = (
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

    b_z = (
        d_a_drho
        +
        a_over_rho
    )

    return {
        "e_rho":
            e_rho,

        "e_z":
            e_z,

        "b_rho":
            b_rho,

        "b_z":
            b_z,
    }


def _state_diagnostics(
    phi: np.ndarray,
    a_phi: np.ndarray,
    field: dict[str, Any],
    density_kg_m3: np.ndarray,
) -> dict[str, Any]:
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

    d_sigma_dz, _ = np.gradient(
        sigma,
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

    e_squared = (
        fields[
            "e_rho"
        ] ** 2
        +
        fields[
            "e_z"
        ] ** 2
    )

    b_squared = (
        fields[
            "b_rho"
        ] ** 2
        +
        fields[
            "b_z"
        ] ** 2
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
        field[
            "h"
        ] ** 2
    )

    canonical_energy_j = (
        0.5
        *
        float(
            np.sum(
                volume
                *
                (
                    e_squared
                    +
                    b_squared
                )
            )
        )
        /
        HBAR_C_EV_M
        *
        EV_J
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

    payload_indices = np.argwhere(
        payload
    )

    local_min_index = int(
        np.argmin(
            payload_acceleration
        )
    )

    worst_j, worst_i = (
        payload_indices[
            local_min_index
        ]
    )

    payload_mass_kg = float(
        np.sum(
            density_kg_m3
            *
            volume
        )
    )

    matter_shift_density_j_m3 = (
        density_kg_m3
        *
        C_LIGHT_M_S**2
        *
        np.expm1(
            sigma
        )
    )

    matter_shift_signed_j = float(
        np.sum(
            matter_shift_density_j_m3
            *
            volume
        )
    )

    matter_shift_abs_j = float(
        np.sum(
            np.abs(
                matter_shift_density_j_m3
            )
            *
            volume
        )
    )

    amplitude_factor = (
        source_amplitude_factor_for_one_g(
            minimum
        )
    )

    energy_factor = (
        energy_factor_for_one_g(
            minimum
        )
    )

    if energy_factor is not None:
        normalized_field_energy_j = (
            canonical_energy_j
            *
            energy_factor
        )

        normalized_matter_signed_j = (
            matter_shift_signed_j
            *
            energy_factor
        )

        normalized_matter_abs_j = (
            matter_shift_abs_j
            *
            energy_factor
        )

        normalized_partial_capacity_j = (
            normalized_field_energy_j
            +
            normalized_matter_abs_j
        )
    else:
        normalized_field_energy_j = None
        normalized_matter_signed_j = None
        normalized_matter_abs_j = None
        normalized_partial_capacity_j = None

    return {
        "minimum_payload_acceleration_m_s2":
            minimum,

        "maximum_payload_acceleration_m_s2":
            maximum,

        "whole_payload_outward":
            minimum
            >
            0.0,

        "worst_payload_rho_m":
            float(
                field[
                    "rho_grid"
                ][
                    worst_j,
                    worst_i,
                ]
            ),

        "worst_payload_z_m":
            float(
                field[
                    "z_grid"
                ][
                    worst_j,
                    worst_i,
                ]
            ),

        "payload_sigma_min":
            float(
                np.min(
                    sigma[
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

        "canonical_field_energy_j":
            canonical_energy_j,

        "payload_mass_numerical_kg":
            payload_mass_kg,

        "matter_interaction_signed_j":
            matter_shift_signed_j,

        "matter_interaction_absolute_j":
            matter_shift_abs_j,

        "source_amplitude_factor_to_exact_1g":
            amplitude_factor,

        "energy_factor_to_exact_1g":
            energy_factor,

        "normalized_field_energy_j":
            normalized_field_energy_j,

        "normalized_matter_interaction_signed_j":
            normalized_matter_signed_j,

        "normalized_matter_interaction_absolute_j":
            normalized_matter_abs_j,

        "normalized_field_plus_abs_matter_j":
            normalized_partial_capacity_j,

        "sub100j_partial_capacity":
            bool(
                normalized_partial_capacity_j
                is not None
                and
                normalized_partial_capacity_j
                <
                GREEN_FIELD_PLUS_ABS_MATTER_J
            ),

        "sub10kj_partial_capacity":
            bool(
                normalized_partial_capacity_j
                is not None
                and
                normalized_partial_capacity_j
                <
                YELLOW_FIELD_PLUS_ABS_MATTER_J
            ),

        "complete_energy_established":
            False,
    }


def _build_elliptic_operators(
    rhos: np.ndarray,
    zs: np.ndarray,
    h: float,
) -> dict[str, Any]:
    nz_inner = (
        len(
            zs
        )
        -
        2
    )

    nr_phi = (
        len(
            rhos
        )
        -
        1
    )

    nr_a = (
        len(
            rhos
        )
        -
        2
    )

    radial_phi = np.zeros(
        (
            nr_phi,
            nr_phi,
        ),
        dtype=float,
    )

    radial_phi[
        0,
        0
    ] = (
        4.0
        /
        h**2
    )

    if nr_phi > 1:
        radial_phi[
            0,
            1
        ] = (
            -4.0
            /
            h**2
        )

    for i in range(
        1,
        nr_phi,
    ):
        rho = (
            rhos[
                i
            ]
        )

        radial_phi[
            i,
            i
        ] = (
            2.0
            /
            h**2
        )

        radial_phi[
            i,
            i
            -
            1
        ] = (
            -1.0
            /
            h**2
            +
            1.0
            /
            (
                2.0
                *
                rho
                *
                h
            )
        )

        if (
            i
            +
            1
            <
            nr_phi
        ):
            radial_phi[
                i,
                i
                +
                1
            ] = (
                -1.0
                /
                h**2
                -
                1.0
                /
                (
                    2.0
                    *
                    rho
                    *
                    h
                )
            )

    radial_phi = csr_matrix(
        radial_phi
    )

    rho_a = (
        rhos[
            1:-1
        ]
    )

    a_diag = (
        2.0
        /
        h**2
        +
        1.0
        /
        rho_a**2
    )

    a_lower = (
        -1.0
        /
        h**2
        +
        1.0
        /
        (
            2.0
            *
            rho_a[
                1:
            ]
            *
            h
        )
    )

    a_upper = (
        -1.0
        /
        h**2
        -
        1.0
        /
        (
            2.0
            *
            rho_a[
                :-1
            ]
            *
            h
        )
    )

    radial_a = diags(
        [
            a_lower,
            a_diag,
            a_upper,
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
            nz_inner
        )
        *
        2.0
        /
        h**2
    )

    z_off = (
        -np.ones(
            nz_inner
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

    k_phi = (
        kron(
            eye(
                nz_inner,
                format="csr",
            ),
            radial_phi,
        )
        +
        kron(
            z_operator,
            eye(
                nr_phi,
                format="csr",
            ),
        )
    ).tocsr()

    k_a = (
        kron(
            eye(
                nz_inner,
                format="csr",
            ),
            radial_a,
        )
        +
        kron(
            z_operator,
            eye(
                nr_a,
                format="csr",
            ),
        )
    ).tocsr()

    return {
        "k_phi":
            k_phi,

        "k_a":
            k_a,

        "nz_inner":
            nz_inner,

        "nr_phi":
            nr_phi,

        "nr_a":
            nr_a,
    }


def _build_same_action_coupling(
    rhos: np.ndarray,
    zs: np.ndarray,
    h: float,
    beta_full: np.ndarray,
    operators: dict[str, Any],
) -> dict[str, Any]:
    beta_z, beta_rho = np.gradient(
        beta_full,
        h,
        h,
        edge_order=2,
    )

    gradient_magnitude = np.sqrt(
        beta_rho**2
        +
        beta_z**2
    )

    max_gradient = float(
        np.max(
            gradient_magnitude
        )
    )

    threshold = (
        COUPLING_GRADIENT_RELATIVE_THRESHOLD
        *
        max_gradient
    )

    nz_inner = (
        operators[
            "nz_inner"
        ]
    )

    nr_phi = (
        operators[
            "nr_phi"
        ]
    )

    nr_a = (
        operators[
            "nr_a"
        ]
    )

    rows = []
    cols = []
    data = []

    def phi_index(
        j: int,
        i: int,
    ) -> int:
        return (
            (
                j
                -
                1
            )
            *
            nr_phi
            +
            i
        )

    def a_index(
        j: int,
        i: int,
    ) -> int:
        return (
            (
                j
                -
                1
            )
            *
            nr_a
            +
            (
                i
                -
                1
            )
        )

    for j in range(
        1,
        len(
            zs
        )
        -
        1,
    ):
        for i in range(
            1,
            len(
                rhos
            )
            -
            1,
        ):
            if (
                gradient_magnitude[
                    j,
                    i
                ]
                <=
                threshold
            ):
                continue

            beta_r = float(
                beta_rho[
                    j,
                    i
                ]
            )

            beta_z_local = float(
                beta_z[
                    j,
                    i
                ]
            )

            row = (
                phi_index(
                    j,
                    i,
                )
            )

            if (
                j
                +
                1
                <=
                len(
                    zs
                )
                -
                2
            ):
                rows.append(
                    row
                )

                cols.append(
                    a_index(
                        j
                        +
                        1,
                        i,
                    )
                )

                data.append(
                    beta_r
                    /
                    (
                        2.0
                        *
                        h
                    )
                )

            if (
                j
                -
                1
                >=
                1
            ):
                rows.append(
                    row
                )

                cols.append(
                    a_index(
                        j
                        -
                        1,
                        i,
                    )
                )

                data.append(
                    -beta_r
                    /
                    (
                        2.0
                        *
                        h
                    )
                )

            if (
                i
                +
                1
                <=
                len(
                    rhos
                )
                -
                2
            ):
                rows.append(
                    row
                )

                cols.append(
                    a_index(
                        j,
                        i
                        +
                        1,
                    )
                )

                data.append(
                    -beta_z_local
                    /
                    (
                        2.0
                        *
                        h
                    )
                )

            if (
                i
                -
                1
                >=
                1
            ):
                rows.append(
                    row
                )

                cols.append(
                    a_index(
                        j,
                        i
                        -
                        1,
                    )
                )

                data.append(
                    beta_z_local
                    /
                    (
                        2.0
                        *
                        h
                    )
                )

            rows.append(
                row
            )

            cols.append(
                a_index(
                    j,
                    i,
                )
            )

            data.append(
                -beta_z_local
                /
                rhos[
                    i
                ]
            )

    c_matrix = coo_matrix(
        (
            np.asarray(
                data,
                dtype=float,
            ),
            (
                np.asarray(
                    rows,
                    dtype=int,
                ),
                np.asarray(
                    cols,
                    dtype=int,
                ),
            ),
        ),
        shape=(
            nz_inner
            *
            nr_phi,
            nz_inner
            *
            nr_a,
        ),
    ).tocsr()

    phi_rho_weights = (
        rhos[
            :-1
        ].copy()
    )

    phi_rho_weights[
        0
    ] = (
        0.25
        *
        h
    )

    a_rho_weights = (
        rhos[
            1:-1
        ].copy()
    )

    w_phi = np.tile(
        phi_rho_weights,
        nz_inner,
    )

    w_a = np.tile(
        a_rho_weights,
        nz_inner,
    )

    d_matrix = (
        diags(
            1.0
            /
            w_a,
            format="csr",
        )
        @
        c_matrix.T
        @
        diags(
            w_phi,
            format="csr",
        )
    ).tocsr()

    reciprocity = (
        diags(
            w_a,
            format="csr",
        )
        @
        d_matrix
        -
        c_matrix.T
        @
        diags(
            w_phi,
            format="csr",
        )
    )

    if reciprocity.nnz:
        reciprocity_max_abs = float(
            np.max(
                np.abs(
                    reciprocity.data
                )
            )
        )
    else:
        reciprocity_max_abs = 0.0

    active_phi = np.unique(
        c_matrix.nonzero()[
            0
        ]
    )

    active_a = np.unique(
        d_matrix.nonzero()[
            0
        ]
    )

    return {
        "c":
            c_matrix,

        "d":
            d_matrix,

        "active_phi":
            active_phi,

        "active_a":
            active_a,

        "beta_gradient_max":
            max_gradient,

        "beta_gradient_threshold":
            threshold,

        "same_action_reciprocity_max_abs":
            reciprocity_max_abs,

        "same_action_discrete_reciprocity_exact":
            reciprocity_max_abs
            <
            1.0e-10,
    }


def _green_columns(
    matrix: csr_matrix,
    active_rows: np.ndarray,
    batch_size: int = 16,
) -> np.ndarray:
    active_rows = np.asarray(
        active_rows,
        dtype=int,
    )

    result = np.empty(
        (
            matrix.shape[
                0
            ],
            len(
                active_rows
            ),
        ),
        dtype=float,
    )

    factor = splu(
        matrix.tocsc()
    )

    for start in range(
        0,
        len(
            active_rows
        ),
        batch_size,
    ):
        stop = min(
            start
            +
            batch_size,
            len(
                active_rows
            ),
        )

        selected = (
            active_rows[
                start:stop
            ]
        )

        rhs = np.zeros(
            (
                matrix.shape[
                    0
                ],
                len(
                    selected
                ),
            ),
            dtype=float,
        )

        rhs[
            selected,
            np.arange(
                len(
                    selected
                )
            ),
        ] = 1.0

        result[
            :,
            start:stop,
        ] = (
            factor.solve(
                rhs
            )
        )

    del factor

    gc.collect()

    return result


def _prepare_low_rank_loaded_system(
    field: dict[str, Any],
    phi0: np.ndarray,
    a0: np.ndarray,
    beta_full: np.ndarray,
) -> dict[str, Any]:
    operators = (
        _build_elliptic_operators(
            field[
                "rhos"
            ],
            field[
                "zs"
            ],
            field[
                "h"
            ],
        )
    )

    coupling = (
        _build_same_action_coupling(
            field[
                "rhos"
            ],
            field[
                "zs"
            ],
            field[
                "h"
            ],
            beta_full,
            operators,
        )
    )

    nr_phi = (
        operators[
            "nr_phi"
        ]
    )

    nr_a = (
        operators[
            "nr_a"
        ]
    )

    phi0_vec = (
        phi0[
            1:-1,
            :-1,
        ].reshape(
            -1
        )
    )

    a0_vec = (
        a0[
            1:-1,
            1:-1,
        ].reshape(
            -1
        )
    )

    active_phi = (
        coupling[
            "active_phi"
        ]
    )

    active_a = (
        coupling[
            "active_a"
        ]
    )

    green_phi = (
        _green_columns(
            operators[
                "k_phi"
            ],
            active_phi,
        )
    )

    green_a = (
        _green_columns(
            operators[
                "k_a"
            ],
            active_a,
        )
    )

    c_active = (
        coupling[
            "c"
        ][
            active_phi,
            :
        ]
    )

    d_active = (
        coupling[
            "d"
        ][
            active_a,
            :
        ]
    )

    c_green_a = (
        c_active
        @
        green_a
    )

    d_green_phi = (
        d_active
        @
        green_phi
    )

    c_a0 = (
        c_active
        @
        a0_vec
    )

    d_phi0 = (
        d_active
        @
        phi0_vec
    )

    return {
        "operators":
            operators,

        "coupling":
            coupling,

        "phi0_vec":
            phi0_vec,

        "a0_vec":
            a0_vec,

        "green_phi":
            green_phi,

        "green_a":
            green_a,

        "c_active":
            c_active,

        "d_active":
            d_active,

        "c_green_a":
            np.asarray(
                c_green_a
            ),

        "d_green_phi":
            np.asarray(
                d_green_phi
            ),

        "c_a0":
            np.asarray(
                c_a0
            ).reshape(
                -1
            ),

        "d_phi0":
            np.asarray(
                d_phi0
            ).reshape(
                -1
            ),

        "nr_phi":
            nr_phi,

        "nr_a":
            nr_a,
    }


def _solve_loaded_deviation(
    prep: dict[str, Any],
    loading_fraction: float,
    coupling_sign: float = 1.0,
) -> dict[str, Any]:
    lam = float(
        loading_fraction
    )

    sign = float(
        coupling_sign
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

    if lam == 0.0:
        return {
            "success":
                True,

            "condition_number":
                1.0,

            "delta_phi_vec":
                np.zeros_like(
                    prep[
                        "phi0_vec"
                    ]
                ),

            "delta_a_vec":
                np.zeros_like(
                    prep[
                        "a0_vec"
                    ]
                ),

            "relative_residual":
                0.0,
        }

    reduced = np.eye(
        r_phi
        +
        r_a,
        dtype=float,
    )

    reduced[
        :r_phi,
        r_phi:
    ] = (
        lam
        *
        sign
        *
        prep[
            "c_green_a"
        ]
    )

    reduced[
        r_phi:,
        :r_phi
    ] = (
        lam
        *
        sign
        *
        prep[
            "d_green_phi"
        ]
    )

    rhs = (
        -lam
        *
        sign
        *
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

    condition_number = float(
        np.linalg.cond(
            reduced
        )
    )

    if (
        not math.isfinite(
            condition_number
        )
        or
        condition_number
        >
        REDUCED_CONDITION_FAIL
    ):
        return {
            "success":
                False,

            "condition_number":
                condition_number,

            "delta_phi_vec":
                None,

            "delta_a_vec":
                None,

            "relative_residual":
                None,
        }

    try:
        reduced_solution = np.linalg.solve(
            reduced,
            rhs,
        )

    except np.linalg.LinAlgError:
        return {
            "success":
                False,

            "condition_number":
                condition_number,

            "delta_phi_vec":
                None,

            "delta_a_vec":
                None,

            "relative_residual":
                None,
        }

    y_phi = (
        reduced_solution[
            :r_phi
        ]
    )

    y_a = (
        reduced_solution[
            r_phi:
        ]
    )

    delta_phi = (
        prep[
            "green_phi"
        ]
        @
        y_phi
    )

    delta_a = (
        prep[
            "green_a"
        ]
        @
        y_a
    )

    phi_total_vec = (
        prep[
            "phi0_vec"
        ]
        +
        delta_phi
    )

    a_total_vec = (
        prep[
            "a0_vec"
        ]
        +
        delta_a
    )

    residual_phi = (
        prep[
            "operators"
        ][
            "k_phi"
        ]
        @
        delta_phi
        +
        lam
        *
        sign
        *
        (
            prep[
                "coupling"
            ][
                "c"
            ]
            @
            a_total_vec
        )
    )

    residual_a = (
        prep[
            "operators"
        ][
            "k_a"
        ]
        @
        delta_a
        +
        lam
        *
        sign
        *
        (
            prep[
                "coupling"
            ][
                "d"
            ]
            @
            phi_total_vec
        )
    )

    driving_norm = (
        np.linalg.norm(
            lam
            *
            prep[
                "coupling"
            ][
                "c"
            ]
            @
            prep[
                "a0_vec"
            ]
        )
        +
        np.linalg.norm(
            lam
            *
            prep[
                "coupling"
            ][
                "d"
            ]
            @
            prep[
                "phi0_vec"
            ]
        )
        +
        1.0e-300
    )

    relative_residual = (
        np.linalg.norm(
            residual_phi
        )
        +
        np.linalg.norm(
            residual_a
        )
    ) / driving_norm

    return {
        "success":
            True,

        "condition_number":
            condition_number,

        "delta_phi_vec":
            delta_phi,

        "delta_a_vec":
            delta_a,

        "relative_residual":
            float(
                relative_residual
            ),
    }


def _vectors_to_full_potentials(
    prep: dict[str, Any],
    field: dict[str, Any],
    phi0: np.ndarray,
    a0: np.ndarray,
    solution: dict[str, Any],
) -> tuple[np.ndarray, np.ndarray]:
    phi = phi0.copy()

    a_phi = a0.copy()

    phi[
        1:-1,
        :-1,
    ] += (
        solution[
            "delta_phi_vec"
        ].reshape(
            (
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
    )

    a_phi[
        1:-1,
        1:-1,
    ] += (
        solution[
            "delta_a_vec"
        ].reshape(
            (
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
    )

    return (
        phi,
        a_phi,
    )


def _run_grid(
    h: float,
) -> dict[str, Any]:
    field = (
        _a12c_potential_field(
            h
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

    if (
        baseline[
            "minimum_payload_acceleration_m_s2"
        ]
        <=
        0.0
    ):
        raise RuntimeError(
            "R3B mirror baseline lost outward sign before loading"
        )

    baseline_scale = (
        source_amplitude_factor_for_one_g(
            baseline[
                "minimum_payload_acceleration_m_s2"
            ]
        )
    )

    phi0 = (
        baseline_scale
        *
        phi0
    )

    a0 = (
        baseline_scale
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

    # beta = 2 T/M^4 with T ~= -rho_E.
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

    homotopy_rows = []

    for lam in LOADING_HOMOTOPY:
        solution = (
            _solve_loaded_deviation(
                prep,
                lam,
                coupling_sign=1.0,
            )
        )

        if not solution[
            "success"
        ]:
            homotopy_rows.append(
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
                        None,

                    "minimum_payload_acceleration_m_s2":
                        None,

                    "maximum_payload_acceleration_m_s2":
                        None,

                    "whole_payload_outward":
                        False,

                    "normalized_field_energy_j":
                        None,

                    "normalized_matter_interaction_absolute_j":
                        None,

                    "normalized_field_plus_abs_matter_j":
                        None,

                    "source_amplitude_factor_to_1g":
                        None,
                }
            )

            continue

        phi, a_phi = (
            _vectors_to_full_potentials(
                prep,
                field,
                phi0,
                a0,
                solution,
            )
        )

        state = (
            _state_diagnostics(
                phi,
                a_phi,
                field,
                density,
            )
        )

        homotopy_rows.append(
            {
                "loading_fraction":
                    lam,

                "solve_success":
                    True,

                "reduced_condition_number":
                    solution[
                        "condition_number"
                    ],

                "condition_warning":
                    bool(
                        solution[
                            "condition_number"
                        ]
                        >
                        REDUCED_CONDITION_WARN
                    ),

                "relative_solve_residual":
                    solution[
                        "relative_residual"
                    ],

                "minimum_payload_acceleration_m_s2":
                    state[
                        "minimum_payload_acceleration_m_s2"
                    ],

                "maximum_payload_acceleration_m_s2":
                    state[
                        "maximum_payload_acceleration_m_s2"
                    ],

                "whole_payload_outward":
                    state[
                        "whole_payload_outward"
                    ],

                "worst_payload_rho_m":
                    state[
                        "worst_payload_rho_m"
                    ],

                "worst_payload_z_m":
                    state[
                        "worst_payload_z_m"
                    ],

                "canonical_field_energy_fixed_source_j":
                    state[
                        "canonical_field_energy_j"
                    ],

                "matter_interaction_signed_fixed_source_j":
                    state[
                        "matter_interaction_signed_j"
                    ],

                "matter_interaction_absolute_fixed_source_j":
                    state[
                        "matter_interaction_absolute_j"
                    ],

                "source_amplitude_factor_to_1g":
                    state[
                        "source_amplitude_factor_to_exact_1g"
                    ],

                "normalized_field_energy_j":
                    state[
                        "normalized_field_energy_j"
                    ],

                "normalized_matter_interaction_signed_j":
                    state[
                        "normalized_matter_interaction_signed_j"
                    ],

                "normalized_matter_interaction_absolute_j":
                    state[
                        "normalized_matter_interaction_absolute_j"
                    ],

                "normalized_field_plus_abs_matter_j":
                    state[
                        "normalized_field_plus_abs_matter_j"
                    ],

                "sub100j_partial_capacity":
                    state[
                        "sub100j_partial_capacity"
                    ],

                "sub10kj_partial_capacity":
                    state[
                        "sub10kj_partial_capacity"
                    ],
            }
        )

    opposite_solution = (
        _solve_loaded_deviation(
            prep,
            1.0,
            coupling_sign=-1.0,
        )
    )

    if opposite_solution[
        "success"
    ]:
        opposite_phi, opposite_a = (
            _vectors_to_full_potentials(
                prep,
                field,
                phi0,
                a0,
                opposite_solution,
            )
        )

        opposite_state = (
            _state_diagnostics(
                opposite_phi,
                opposite_a,
                field,
                density,
            )
        )

        opposite_sign_audit = {
            "solve_success":
                True,

            "condition_number":
                opposite_solution[
                    "condition_number"
                ],

            "relative_residual":
                opposite_solution[
                    "relative_residual"
                ],

            "minimum_payload_acceleration_m_s2":
                opposite_state[
                    "minimum_payload_acceleration_m_s2"
                ],

            "whole_payload_outward":
                opposite_state[
                    "whole_payload_outward"
                ],

            "normalized_field_plus_abs_matter_j":
                opposite_state[
                    "normalized_field_plus_abs_matter_j"
                ],
        }

    else:
        opposite_sign_audit = {
            "solve_success":
                False,

            "condition_number":
                opposite_solution[
                    "condition_number"
                ],

            "relative_residual":
                None,

            "minimum_payload_acceleration_m_s2":
                None,

            "whole_payload_outward":
                False,

            "normalized_field_plus_abs_matter_j":
                None,
        }

    critical = (
        critical_loading_fraction(
            homotopy_rows
        )
    )

    suppression = (
        suppression_target_from_critical_fraction(
            critical[
                "critical_loading_fraction"
            ]
        )
    )

    full_rows = [
        row
        for row in homotopy_rows
        if math.isclose(
            float(
                row[
                    "loading_fraction"
                ]
            ),
            1.0,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
    ]

    full_row = (
        full_rows[
            0
        ]
        if full_rows
        else
        None
    )

    return {
        "grid_spacing_m":
            h,

        "baseline":
            baseline,

        "payload_peak_beta_magnitude":
            float(
                np.max(
                    np.abs(
                        beta_full
                    )
                )
            ),

        "payload_mass_numerical_kg":
            baseline[
                "payload_mass_numerical_kg"
            ],

        "active_phi_interface_rows":
            int(
                len(
                    prep[
                        "coupling"
                    ][
                        "active_phi"
                    ]
                )
            ),

        "active_a_interface_rows":
            int(
                len(
                    prep[
                        "coupling"
                    ][
                        "active_a"
                    ]
                )
            ),

        "same_action_reciprocity_max_abs":
            prep[
                "coupling"
            ][
                "same_action_reciprocity_max_abs"
            ],

        "same_action_discrete_reciprocity_exact":
            prep[
                "coupling"
            ][
                "same_action_discrete_reciprocity_exact"
            ],

        "homotopy":
            homotopy_rows,

        "critical_loading":
            critical,

        "polarization_node_suppression_target":
            suppression,

        "full_loading":
            full_row,

        "opposite_sign_full_loading_audit":
            opposite_sign_audit,

        "exact_exp4sigma_bulk_feedback_included":
            False,

        "reason_exp4sigma_feedback_omitted":
            (
                "R3A_CERTIFIED_PEAK_NONLINEAR_UNIFORM_BULK_PROXY_"
                "ABOUT_1E-11_VERSUS_ORDER_1_INTERFACE_TEST"
            ),
    }


def final_decision(
    grid_results: dict[str, Any],
) -> dict[str, Any]:
    coarse = (
        grid_results[
            str(
                GRID_SPACINGS_M[
                    0
                ]
            )
        ]
    )

    fine = (
        grid_results[
            str(
                GRID_SPACINGS_M[
                    1
                ]
            )
        ]
    )

    coarse_full = (
        coarse[
            "full_loading"
        ]
    )

    fine_full = (
        fine[
            "full_loading"
        ]
    )

    both_solved = bool(
        coarse_full
        is not None
        and
        fine_full
        is not None
        and
        coarse_full[
            "solve_success"
        ]
        and
        fine_full[
            "solve_success"
        ]
    )

    both_outward = bool(
        both_solved
        and
        coarse_full[
            "whole_payload_outward"
        ]
        and
        fine_full[
            "whole_payload_outward"
        ]
    )

    fine_partial = (
        fine_full[
            "normalized_field_plus_abs_matter_j"
        ]
        if (
            fine_full
            is not None
            and
            fine_full[
                "solve_success"
            ]
        )
        else
        None
    )

    if (
        both_outward
        and
        fine_partial
        is not None
        and
        fine_partial
        <
        GREEN_FIELD_PLUS_ABS_MATTER_J
    ):
        decision = (
            "GREEN_SCOPED_R3C_FULL_OPTIMISTIC_FINITE_PAYLOAD_"
            "TOPOLOGICAL_LOADING_PRESERVES_WHOLE_PAYLOAD_OUTWARD_"
            "1G_RESPONSE_WITH_FIELD_PLUS_ABS_MATTER_BELOW_100J__"
            "LOW_JOULE_MECHANISM_SURVIVES_THIS_LOADING_GATE__"
            "SESSION_CLOSEOUT_AND_NEXT_SESSION_SOURCE_PARITY_STABILITY_GATES"
        )

        loaded_corridor_survives = True

    elif (
        both_outward
        and
        fine_partial
        is not None
        and
        fine_partial
        <
        YELLOW_FIELD_PLUS_ABS_MATTER_J
    ):
        decision = (
            "YELLOW_GREEN_SCOPED_R3C_FULL_OPTIMISTIC_FINITE_PAYLOAD_"
            "TOPOLOGICAL_LOADING_PRESERVES_OUTWARD_1G_WITH_SUB10KJ_"
            "PARTIAL_CAPACITY__LOW_CAPACITY_CORRIDOR_SURVIVES__"
            "SESSION_CLOSEOUT"
        )

        loaded_corridor_survives = True

    elif both_outward:
        decision = (
            "YELLOW_SCOPED_R3C_FULL_LOADING_PRESERVES_OUTWARD_SIGN_"
            "BUT_LOW_CAPACITY_ADVANTAGE_IS_DEGRADED__SESSION_CLOSEOUT_"
            "WITH_ENERGY_OBSTRUCTION_EXPLICIT"
        )

        loaded_corridor_survives = True

    else:
        fine_critical = (
            fine[
                "critical_loading"
            ][
                "critical_loading_fraction"
            ]
        )

        if (
            fine_critical
            is not None
            and
            fine_critical
            >=
            1.0e-2
        ):
            decision = (
                "YELLOW_SCOPED_R3C_SIMPLE_PARALLEL_MIRROR_FAILS_FULL_"
                "FINITE_PAYLOAD_LOADING_BUT_SURVIVES_A_NONTRIVIAL_"
                "INTERFACE_FRACTION__POLARIZATION_NODE_REMAINS_A_"
                "QUANTIFIED_RESCUE_TARGET__SESSION_CLOSEOUT"
            )

        else:
            decision = (
                "RED_YELLOW_SCOPED_R3C_SIMPLE_PARALLEL_MIRROR_IS_"
                "DESTROYED_AT_SMALL_INTERFACE_LOADING__POLARIZATION_"
                "NODE_WOULD_REQUIRE_STRONG_SUPPRESSION__DO_NOT_CLAIM_"
                "THE_TOPOLOGICAL_ROUTE_CLOSED__SESSION_CLOSEOUT"
            )

        loaded_corridor_survives = False

    return {
        "decision":
            decision,

        "both_grids_full_loading_solved":
            both_solved,

        "both_grids_full_loading_whole_payload_outward":
            both_outward,

        "fine_full_loading_partial_capacity_j":
            fine_partial,

        "simple_parallel_loaded_corridor_survives":
            loaded_corridor_survives,

        "fine_critical_loading_fraction":
            fine[
                "critical_loading"
            ][
                "critical_loading_fraction"
            ],

        "fine_interface_suppression_target":
            fine[
                "polarization_node_suppression_target"
            ],

        "session_closeout_ready":
            True,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "006d_replaced":
            False,

        "next":
            (
                "BUILD_COMPREHENSIVE_SESSION_CARRYOVER_NOTES_"
                "WITH_R3A_R3B_R3C_AS_ACTIVE_FRONTIER"
            ),
    }
