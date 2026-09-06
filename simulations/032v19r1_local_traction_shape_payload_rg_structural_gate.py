"""032V19R1 — local traction, support shape, payload, and structural RG gate.

PURPOSE
-------
Strengthen the successful 032V19 support-action preflight without performing
generic energy optimization.

V19 established an explicit positive-energy false-vacuum support action class.

This run asks whether that support survives the LOCAL angular traction of the
V18 scalar dipole and whether the resulting wall shape still supports the
finite 1kg payload at at least 1g.

It also converts the existing Delta-Z warning into a stronger structural
fixed-order RG test.

WORK PERFORMED
--------------
1. Reconstruct V18 exact spherical source.
2. Derive exact local l=0 and l=2 wall traction.
3. Check several physically motivated false-vacuum/wall support fractions.
4. Let an isotropic wall respond through its first-order l=2 curvature mode.
5. Re-solve the exact occupied positive-band mean field at fixed particle
   number after each geometry change.
6. Recompute exact finite-payload acceleration with spheroidal multipoles.
7. Construct one nearby reference retune with:
       bag fraction = 0.75
       loop proxy   = the V18 loop proxy
       hard margin  > 5
       surface min  = 1g within numerical tolerance
8. Check fixed-number spherical radial equilibrium.
9. Prove whether any valid fixed-order cutoff above the occupied hard scale
   can make Delta Z smaller than one.

CLAIM LIMITS
------------
The l=2 wall treatment is first-order.

This run does not solve the nonlinear chi/Psi/phi wall profile.

It does not calculate the renormalized axial determinant.

It does not provide an outward-sign UV completion.

It does not establish complete operating energy or a practical device.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from scipy.optimize import (
    brentq,
    minimize_scalar,
)

from antigravity_research.agminer.axial_dirac_meanfield import (
    payload_trace_load,
)
from antigravity_research.agminer.c1_payload_matching import (
    payload_surface_acceleration_metrics,
    required_q2_for_payload_surface,
    spheroid_incident_legendre_coefficients,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.spherical_bag_shape_coupling import (
    false_vacuum_l0_support,
    f_for_declared_loop_cap,
    fixed_number_meanfield_state,
    fixed_order_rg_structural_gate,
    linear_l2_shape_response,
    local_spherical_traction_multipoles,
    particle_number_from_state,
    sphere_volume_m3,
)


ROOT = Path(
    __file__
).resolve().parents[1]

V18 = (
    ROOT
    / "results"
    / "data"
    / "032v18_universal_metric_rg_support_ready_summary.json"
)

V19 = (
    ROOT
    / "results"
    / "data"
    / "032v19_spherical_bag_support_uv_empirical_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r1_local_traction_shape_payload_rg_summary.json"
)

SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r1_support_shape_fraction_scan.csv"
)

RG_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r1_rg_window_scan.csv"
)


TARGET_J = 1.0e7
G = 9.80665

PAYLOAD_RADIUS_M = 0.10
PAYLOAD_CENTER_Z_M = 0.20

BAG_FRACTIONS = (
    0.00,
    0.25,
    0.50,
    0.75,
    0.90,
    0.95,
)

SELECTED_BAG_FRACTION = 0.75

# Two additional flavors are not used as an energy-saving shortcut.
#
# f is changed simultaneously so that the declared loop proxy remains fixed.
# The purpose is only to recover the hard-scale margin after support-induced
# geometry changes.
RETUNED_FLAVORS = 118


policy = current_energy_policy()

assert math.isclose(
    float(
        policy[
            "limit_j"
        ]
    ),
    TARGET_J,
    rel_tol=0.0,
    abs_tol=0.0,
)

assert (
    str(
        policy[
            "comparison"
        ]
    )
    ==
    "LT"
)


v18 = json.loads(
    V18.read_text(
        encoding="utf-8"
    )
)

v19 = json.loads(
    V19.read_text(
        encoding="utf-8"
    )
)


sphere = v18[
    "sphere_exact_payload_optimum"
]

physical = v18[
    "sphere_physical_source"
]

meanfield = v18[
    "sphere_meanfield"
]


radius_m = float(
    meanfield[
        "source_radius_m"
    ]
)

source_volume_m3 = (
    sphere_volume_m3(
        radius_m
    )
)

metric_scale_ev = float(
    sphere[
        "metric_scale_ev"
    ]
)

reference_q = float(
    sphere[
        "q"
    ]
)

reference_flavors = int(
    physical[
        "flavors"
    ]
)

reference_f_ev = float(
    physical[
        "f_psi_ev"
    ]
)

reference_b_ev = float(
    physical[
        "axial_b_ev"
    ]
)

mass_ev = float(
    physical[
        "m_psi_ev"
    ]
)

reference_mu_ev = float(
    physical[
        "chemical_potential_ev"
    ]
)

reference_cutoff_ev = float(
    physical[
        "nda_cutoff_ev"
    ]
)

loop_proxy = float(
    meanfield[
        "loop_proxy"
    ]
)


trace = payload_trace_load(
    payload_mass_kg=
        1.0,

    payload_radius_m=
        PAYLOAD_RADIUS_M,

    metric_scale_ev=
        metric_scale_ev,
)

epsilon_trace_load = float(
    trace[
        "epsilon_trace_load"
    ]
)


reference_particle_number = (
    particle_number_from_state(
        mass_ev=
            mass_ev,

        axial_b_ev=
            reference_b_ev,

        chemical_potential_ev=
            reference_mu_ev,

        flavors=
            reference_flavors,

        volume_m3=
            source_volume_m3,

        order=
            128,
    )
)


reference_state = (
    fixed_number_meanfield_state(
        particle_number=
            reference_particle_number,

        volume_m3=
            source_volume_m3,

        demag_z=
            1.0
            / 3.0,

        mass_ev=
            mass_ev,

        f_psi_ev=
            reference_f_ev,

        flavors=
            reference_flavors,

        metric_scale_ev=
            metric_scale_ev,

        initial_b_ev=
            reference_b_ev,

        initial_mu_ev=
            reference_mu_ev,

        order=
            128,
    )
)


reference_q_relative_error = (
    abs(
        reference_state[
            "q"
        ]
        - reference_q
    )
    / reference_q
)

assert (
    reference_q_relative_error
    <
    5.0e-8
)


def payload_for_shape(
    *,
    shape,
    q_value: float,
    lmax: int,
    n_t: int,
    n_phi: int,
    fit_order: int,
    surface_count: int,
):
    coefficients = (
        spheroid_incident_legendre_coefficients(
            a_m=
                shape[
                    "a_m"
                ],

            c_m=
                shape[
                    "c_m"
                ],

            payload_center_z_m=
                PAYLOAD_CENTER_Z_M,

            fit_radius_m=
                PAYLOAD_RADIUS_M,

            lmax=
                lmax,

            n_t=
                n_t,

            n_phi=
                n_phi,

            fit_order=
                fit_order,
        )
    )

    requirement = (
        required_q2_for_payload_surface(
            coefficients=
                coefficients,

            epsilon_trace_load=
                epsilon_trace_load,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            target_acceleration_m_s2=
                G,

            surface_count=
                surface_count,
        )
    )

    surface = (
        payload_surface_acceleration_metrics(
            coefficients=
                coefficients,

            epsilon_trace_load=
                epsilon_trace_load,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            q2=
                q_value**2,

            surface_count=
                surface_count,
        )
    )

    return (
        coefficients,
        requirement,
        surface,
    )


def build_supported_state(
    *,
    particle_number: float,
    flavors: int,
    f_psi_ev: float,
    bag_fraction: float,
    order: int,
    lmax: int,
    n_t: int,
    n_phi: int,
    fit_order: int,
    surface_count: int,
):
    # --------------------------------------------------------
    # Spherical precursor.
    # --------------------------------------------------------

    precursor = (
        fixed_number_meanfield_state(
            particle_number=
                particle_number,

            volume_m3=
                source_volume_m3,

            demag_z=
                1.0
                / 3.0,

            mass_ev=
                mass_ev,

            f_psi_ev=
                f_psi_ev,

            flavors=
                flavors,

            metric_scale_ev=
                metric_scale_ev,

            initial_b_ev=
                reference_b_ev,

            initial_mu_ev=
                reference_mu_ev,

            order=
                order,
        )
    )

    # --------------------------------------------------------
    # Exact spherical local traction.
    # --------------------------------------------------------

    traction = (
        local_spherical_traction_multipoles(
            fermion_pressure_perp_inventory_j=
                precursor[
                    "pressure_perp_inventory_j"
                ],

            fermion_pressure_z_inventory_j=
                precursor[
                    "pressure_z_inventory_j"
                ],

            scalar_field_energy_j=
                precursor[
                    "field_energy_j"
                ],

            sphere_volume_m3_value=
                source_volume_m3,
        )
    )

    # --------------------------------------------------------
    # l=0 positive-energy bag support.
    # --------------------------------------------------------

    support = (
        false_vacuum_l0_support(
            radius_m=
                radius_m,

            l0_pressure_pa=
                traction[
                    "total_l0_pressure_pa"
                ],

            bag_fraction=
                bag_fraction,
        )
    )

    # --------------------------------------------------------
    # First-order physical l=2 shape response.
    # --------------------------------------------------------

    shape = (
        linear_l2_shape_response(
            radius_m=
                radius_m,

            l2_pressure_pa=
                traction[
                    "total_l2_pressure_pa"
                ],

            wall_tension_j_m2=
                support[
                    "wall_tension_j_m2"
                ],
        )
    )

    # --------------------------------------------------------
    # Re-solve source in deformed geometry at fixed N.
    # --------------------------------------------------------

    deformed = (
        fixed_number_meanfield_state(
            particle_number=
                particle_number,

            volume_m3=
                source_volume_m3,

            demag_z=
                shape[
                    "demag_z"
                ],

            mass_ev=
                mass_ev,

            f_psi_ev=
                f_psi_ev,

            flavors=
                flavors,

            metric_scale_ev=
                metric_scale_ev,

            initial_b_ev=
                precursor[
                    "axial_b_ev"
                ],

            initial_mu_ev=
                precursor[
                    "chemical_potential_ev"
                ],

            order=
                order,
        )
    )

    (
        _,
        requirement,
        surface,
    ) = (
        payload_for_shape(
            shape=
                shape,

            q_value=
                deformed[
                    "q"
                ],

            lmax=
                lmax,

            n_t=
                n_t,

            n_phi=
                n_phi,

            fit_order=
                fit_order,

            surface_count=
                surface_count,
        )
    )

    required_q = math.sqrt(
        float(
            requirement[
                "q2"
            ]
        )
    )

    support_deformed_j = (
        support[
            "bag_energy_density_j_m3"
        ]
        * source_volume_m3
        +
        support[
            "wall_tension_j_m2"
        ]
        * shape[
            "surface_area_m2"
        ]
    )

    static_preflight_j = (
        deformed[
            "band_energy_j"
        ]
        +
        deformed[
            "field_energy_j"
        ]
        +
        support_deformed_j
    )

    return {
        "precursor":
            precursor,

        "traction":
            traction,

        "support":
            support,

        "shape":
            shape,

        "deformed":
            deformed,

        "required_q":
            required_q,

        "q_ratio":
            (
                deformed[
                    "q"
                ]
                /
                required_q
            ),

        "surface":
            surface,

        "deformed_support_energy_j":
            support_deformed_j,

        "static_preflight_j":
            static_preflight_j,
    }


# ============================================================
# 1. ORIGINAL V18 PARTICLE NUMBER — SUPPORT FRACTION SCAN
# ============================================================

scan_rows = []

for fraction in BAG_FRACTIONS:
    state = (
        build_supported_state(
            particle_number=
                reference_particle_number,

            flavors=
                reference_flavors,

            f_psi_ev=
                reference_f_ev,

            bag_fraction=
                fraction,

            order=
                96,

            lmax=
                24,

            n_t=
                56,

            n_phi=
                84,

            fit_order=
                180,

            surface_count=
                1001,
        )
    )

    scan_rows.append(
        {
            "bag_fraction":
                fraction,

            "epsilon_l2":
                state[
                    "shape"
                ][
                    "epsilon_l2"
                ],

            "pole_to_equator_aspect":
                state[
                    "shape"
                ][
                    "pole_to_equator_aspect"
                ],

            "demag_z":
                state[
                    "shape"
                ][
                    "demag_z"
                ],

            "actual_q":
                state[
                    "deformed"
                ][
                    "q"
                ],

            "required_q":
                state[
                    "required_q"
                ],

            "q_over_required":
                state[
                    "q_ratio"
                ],

            "surface_min_m_s2":
                state[
                    "surface"
                ][
                    "surface_min_m_s2"
                ],

            "surface_max_m_s2":
                state[
                    "surface"
                ][
                    "surface_max_m_s2"
                ],

            "hard_scale_margin":
                state[
                    "deformed"
                ][
                    "hard_scale_margin"
                ],

            "support_energy_j":
                state[
                    "deformed_support_energy_j"
                ],

            "static_preflight_j":
                state[
                    "static_preflight_j"
                ],
        }
    )


# ============================================================
# 2. NEARBY RETUNE — PRESERVE LOOP CAP AND HARD MARGIN
# ============================================================

retuned_f_ev = (
    f_for_declared_loop_cap(
        mass_ev=
            mass_ev,

        flavors=
            RETUNED_FLAVORS,

        loop_proxy=
            loop_proxy,
    )
)


def retuned_ratio_fast(
    particle_scale: float,
) -> float:
    state = (
        build_supported_state(
            particle_number=
                reference_particle_number
                * float(
                    particle_scale
                ),

            flavors=
                RETUNED_FLAVORS,

            f_psi_ev=
                retuned_f_ev,

            bag_fraction=
                SELECTED_BAG_FRACTION,

            order=
                64,

            lmax=
                16,

            n_t=
                32,

            n_phi=
                48,

            fit_order=
                80,

            surface_count=
                301,
        )
    )

    return (
        state[
            "q_ratio"
        ]
        - 1.0
    )


coarse_particle_scale = (
    brentq(
        retuned_ratio_fast,
        0.95,
        1.15,
        xtol=
            2.0e-5,
    )
)


def retuned_ratio_exact(
    particle_scale: float,
) -> float:
    state = (
        build_supported_state(
            particle_number=
                reference_particle_number
                * float(
                    particle_scale
                ),

            flavors=
                RETUNED_FLAVORS,

            f_psi_ev=
                retuned_f_ev,

            bag_fraction=
                SELECTED_BAG_FRACTION,

            order=
                96,

            lmax=
                28,

            n_t=
                64,

            n_phi=
                96,

            fit_order=
                200,

            surface_count=
                1201,
        )
    )

    return (
        state[
            "q_ratio"
        ]
        - 1.0
    )


retuned_particle_scale = (
    brentq(
        retuned_ratio_exact,
        coarse_particle_scale
        * 0.99,
        coarse_particle_scale
        * 1.01,
        xtol=
            2.0e-7,
    )
)


retuned_particle_number = (
    reference_particle_number
    * retuned_particle_scale
)


retuned = (
    build_supported_state(
        particle_number=
            retuned_particle_number,

        flavors=
            RETUNED_FLAVORS,

        f_psi_ev=
            retuned_f_ev,

        bag_fraction=
            SELECTED_BAG_FRACTION,

        order=
            112,

        lmax=
            32,

        n_t=
            80,

        n_phi=
            120,

        fit_order=
            240,

        surface_count=
            1601,
    )
)


retuned_loop_proxy = (
    RETUNED_FLAVORS
    * mass_ev**2
    /
    (
        4.0
        * math.pi**2
        * retuned_f_ev**2
    )
)


assert math.isclose(
    retuned_loop_proxy,
    loop_proxy,
    rel_tol=2.0e-13,
)

assert (
    retuned[
        "deformed"
    ][
        "hard_scale_margin"
    ]
    >
    5.0
)

assert (
    abs(
        retuned[
            "surface"
        ][
            "surface_min_m_s2"
        ]
        - G
    )
    / G
    <
    1.0e-6
)

assert (
    retuned[
        "static_preflight_j"
    ]
    <
    4.0e6
)


# ============================================================
# 3. FIXED-NUMBER SPHERICAL RADIAL EQUILIBRIUM SCOUT
# ============================================================

bag_density_j_m3 = (
    retuned[
        "support"
    ][
        "bag_energy_density_j_m3"
    ]
)

wall_tension_j_m2 = (
    retuned[
        "support"
    ][
        "wall_tension_j_m2"
    ]
)


def radial_energy_j(
    radius: float,
) -> float:
    r_value = float(
        radius
    )

    volume = sphere_volume_m3(
        r_value
    )

    state = (
        fixed_number_meanfield_state(
            particle_number=
                retuned_particle_number,

            volume_m3=
                volume,

            demag_z=
                1.0
                / 3.0,

            mass_ev=
                mass_ev,

            f_psi_ev=
                retuned_f_ev,

            flavors=
                RETUNED_FLAVORS,

            metric_scale_ev=
                metric_scale_ev,

            initial_b_ev=
                retuned[
                    "precursor"
                ][
                    "axial_b_ev"
                ],

            initial_mu_ev=
                retuned[
                    "precursor"
                ][
                    "chemical_potential_ev"
                ],

            order=
                72,
        )
    )

    return (
        state[
            "band_energy_j"
        ]
        +
        state[
            "field_energy_j"
        ]
        +
        bag_density_j_m3
        * volume
        +
        wall_tension_j_m2
        * 4.0
        * math.pi
        * r_value**2
    )


radial_optimization = (
    minimize_scalar(
        radial_energy_j,

        bounds=(
            0.095,
            0.105,
        ),

        method=
            "bounded",

        options={
            "xatol":
                1.0e-9,
        },
    )
)


radial_equilibrium_m = float(
    radial_optimization.x
)

radial_h = 1.0e-4

radial_minus = radial_energy_j(
    radial_equilibrium_m
    * math.exp(
        -radial_h
    )
)

radial_center = radial_energy_j(
    radial_equilibrium_m
)

radial_plus = radial_energy_j(
    radial_equilibrium_m
    * math.exp(
        radial_h
    )
)

radial_log_curvature_j = (
    radial_plus
    -
    2.0
    * radial_center
    +
    radial_minus
) / radial_h**2


assert (
    abs(
        radial_equilibrium_m
        / radius_m
        - 1.0
    )
    <
    0.01
)

assert (
    radial_log_curvature_j
    >
    0.0
)


# ============================================================
# 4. STRUCTURAL FIXED-ORDER RG TEST
# ============================================================

reference_rg = (
    fixed_order_rg_structural_gate(
        loop_proxy=
            loop_proxy,

        cutoff_ev=
            reference_cutoff_ev,

        mass_ev=
            mass_ev,

        hard_scale_ev=
            max(
                reference_mu_ev,
                mass_ev,
                reference_b_ev,
            ),
    )
)


retuned_rg = (
    fixed_order_rg_structural_gate(
        loop_proxy=
            retuned_loop_proxy,

        cutoff_ev=
            4.0
            * math.pi
            * retuned_f_ev,

        mass_ev=
            mass_ev,

        hard_scale_ev=
            retuned[
                "deformed"
            ][
                "hard_scale_ev"
            ],
    )
)


assert (
    reference_rg[
        "fixed_order_window_exists_above_hard_scale"
    ]
    is False
)

assert (
    retuned_rg[
        "fixed_order_window_exists_above_hard_scale"
    ]
    is False
)

assert (
    retuned_rg[
        "minimum_delta_z_with_cutoff_at_hard_scale"
    ]
    >
    1.0
)


rg_rows = []

for cutoff_over_hard in (
    1.0,
    1.5,
    2.0,
    3.0,
    5.0,
):
    cutoff = (
        retuned[
            "deformed"
        ][
            "hard_scale_ev"
        ]
        * cutoff_over_hard
    )

    delta_z = (
        4.0
        * retuned_loop_proxy
        * math.log(
            cutoff
            / mass_ev
        )
    )

    rg_rows.append(
        {
            "cutoff_over_hard":
                cutoff_over_hard,

            "cutoff_ev":
                cutoff,

            "delta_z_ll":
                delta_z,

            "fixed_order_lt1":
                (
                    delta_z
                    <
                    1.0
                ),
        }
    )


# ============================================================
# 5. OUTPUT
# ============================================================

reference_local_traction = (
    local_spherical_traction_multipoles(
        fermion_pressure_perp_inventory_j=
            float(
                sphere[
                    "fermion_pressure_perp_inventory_j"
                ]
            ),

        fermion_pressure_z_inventory_j=
            float(
                sphere[
                    "fermion_pressure_z_inventory_j"
                ]
            ),

        scalar_field_energy_j=
            float(
                sphere[
                    "field_energy_j"
                ]
            ),

        sphere_volume_m3_value=
            source_volume_m3,
    )
)


decision = (
    "GREEN_LOCAL_TRACTION_AND_NEARBY_SUPPORTED_1G_RETUNE_LT4MJ_"
    "RED_STRUCTURAL_FIXED_ORDER_RG_"
    "UV_MATCHING_MANDATORY"
)

next_step = (
    "032V19R2_RG_RESUMMED_UV_MATCHING_AND_RENORMALIZED_AXIAL_VACUUM_GATE"
)


summary = {
    "branch":
        "032V19R1_LOCAL_TRACTION_SHAPE_PAYLOAD_AND_RG_STRUCTURAL_GATE",

    "claim_class":
        "LOCAL_SUPPORT_AND_FIXED_ORDER_RG_FALSIFICATION_PREFLIGHT",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "v19_input_decision":
        v19[
            "decision"
        ],

    "reference_reconstruction": {
        "particle_number":
            reference_particle_number,

        "q_relative_error":
            reference_q_relative_error,
    },

    "local_traction_reference":
        reference_local_traction,

    "selected_retuned_reference": {
        "bag_fraction":
            SELECTED_BAG_FRACTION,

        "flavors":
            RETUNED_FLAVORS,

        "f_psi_ev":
            retuned_f_ev,

        "loop_proxy":
            retuned_loop_proxy,

        "particle_number_scale_from_v18":
            retuned_particle_scale,

        "particle_number":
            retuned_particle_number,

        "epsilon_l2":
            retuned[
                "shape"
            ][
                "epsilon_l2"
            ],

        "pole_to_equator_aspect":
            retuned[
                "shape"
            ][
                "pole_to_equator_aspect"
            ],

        "demag_z":
            retuned[
                "shape"
            ][
                "demag_z"
            ],

        "axial_b_ev":
            retuned[
                "deformed"
            ][
                "axial_b_ev"
            ],

        "chemical_potential_ev":
            retuned[
                "deformed"
            ][
                "chemical_potential_ev"
            ],

        "hard_scale_margin":
            retuned[
                "deformed"
            ][
                "hard_scale_margin"
            ],

        "surface_min_m_s2":
            retuned[
                "surface"
            ][
                "surface_min_m_s2"
            ],

        "surface_max_m_s2":
            retuned[
                "surface"
            ][
                "surface_max_m_s2"
            ],

        "q_over_required":
            retuned[
                "q_ratio"
            ],

        "band_energy_j":
            retuned[
                "deformed"
            ][
                "band_energy_j"
            ],

        "field_energy_j":
            retuned[
                "deformed"
            ][
                "field_energy_j"
            ],

        "support_energy_j":
            retuned[
                "deformed_support_energy_j"
            ],

        "static_preflight_j":
            retuned[
                "static_preflight_j"
            ],

        "remaining_to_strict_10mj_j":
            TARGET_J
            -
            retuned[
                "static_preflight_j"
            ],

        "full_coupled_wall_solution":
            False,
    },

    "radial_l0_scout": {
        "equilibrium_radius_m":
            radial_equilibrium_m,

        "radius_shift_fraction":
            (
                radial_equilibrium_m
                / radius_m
                - 1.0
            ),

        "log_radius_energy_curvature_j":
            radial_log_curvature_j,

        "positive_curvature":
            (
                radial_log_curvature_j
                >
                0.0
            ),
    },

    "rg_reference_v18":
        reference_rg,

    "rg_retuned_reference":
        retuned_rg,

    "gate_status": {
        "local_spherical_traction":
            "GREEN_ANALYTICAL",

        "isotropic_false_vacuum_l0_support":
            "GREEN_PREFLIGHT",

        "l2_shape_response":
            "YELLOW_LINEARIZED",

        "finite_payload_after_shape":
            "GREEN_AFTER_NEARBY_RETUNE",

        "hard_margin":
            "GREEN_REFERENCE",

        "loop_cap":
            "GREEN_REFERENCE",

        "radial_l0":
            "GREEN_SCOUT",

        "fixed_order_rg":
            "RED_STRUCTURAL",

        "fixed_order_cutoff_tuning_escape":
            "CLOSED",

        "renormalized_axial_vacuum":
            "OPEN",

        "uv_completion":
            "OPEN_RED_BLOCKER",

        "full_coupled_chi_psi_phi_modes":
            "OPEN",

        "empirical_closure":
            "OPEN",

        "complete_operating_energy":
            "NOT_ESTABLISHED",
    },

    "physical_antigravity_model_found":
        False,

    "certified_sub10mj_model_found":
        False,

    "decision":
        decision,

    "next":
        next_step,
}


OUT.write_text(
    json.dumps(
        summary,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


with SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                scan_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        scan_rows
    )


with RG_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                rg_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        rg_rows
    )


print(
    "BRANCH="
    + summary[
        "branch"
    ]
)

print(
    "REFERENCE_PARTICLE_NUMBER="
    f"{reference_particle_number:.12e}"
)

print(
    "LOCAL_TRACTION_L0_J="
    f"{reference_local_traction['total_l0_inventory_j']:.12e}"
)

print(
    "LOCAL_TRACTION_L2_J="
    f"{reference_local_traction['total_l2_inventory_j']:.12e}"
)

print(
    "RETUNED_NF="
    + str(
        RETUNED_FLAVORS
    )
)

print(
    "RETUNED_PARTICLE_SCALE="
    f"{retuned_particle_scale:.12e}"
)

print(
    "RETUNED_ASPECT="
    f"{retuned['shape']['pole_to_equator_aspect']:.12e}"
)

print(
    "RETUNED_HARD_MARGIN="
    f"{retuned['deformed']['hard_scale_margin']:.12e}"
)

print(
    "RETUNED_SURFACE_MIN="
    f"{retuned['surface']['surface_min_m_s2']:.12e}"
)

print(
    "RETUNED_STATIC_PREFLIGHT_J="
    f"{retuned['static_preflight_j']:.12e}"
)

print(
    "REMAINING_TO_10MJ_J="
    f"{TARGET_J-retuned['static_preflight_j']:.12e}"
)

print(
    "RADIAL_EQ_RADIUS_M="
    f"{radial_equilibrium_m:.12e}"
)

print(
    "RADIAL_CURVATURE_J="
    f"{radial_log_curvature_j:.12e}"
)

print(
    "RG_MIN_DELTA_AT_HARD="
    f"{retuned_rg['minimum_delta_z_with_cutoff_at_hard_scale']:.12e}"
)

print(
    "RG_DELTA_AT_DECLARED_CUTOFF="
    f"{retuned_rg['delta_z_at_declared_cutoff']:.12e}"
)

print(
    "RG_FIXED_ORDER_WINDOW_EXISTS="
    + str(
        retuned_rg[
            "fixed_order_window_exists_above_hard_scale"
        ]
    )
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=False"
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND=False"
)

print(
    "DECISION="
    + decision
)

print(
    "NEXT="
    + next_step
)
