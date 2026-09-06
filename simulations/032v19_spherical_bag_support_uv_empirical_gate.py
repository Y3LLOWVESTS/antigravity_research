"""032V19 — physical spherical bag support, vacuum, and UV/empirical gate.

PURPOSE
-------
Attack the physical blockers left by 032V18 rather than optimize the partial
energy again.

This run:

1. reconstructs the V18 spherical source from its persisted result;
2. replaces the abstract support floor with a Friedberg-Lee-type
   false-vacuum plus finite-wall action preflight;
3. quantifies the small axial pressure anisotropy;
4. constructs a finite quartic support wall and Yukawa mass barrier;
5. checks support-sector naturalness and trace loading;
6. checks the V18 spacelike-axial spectral gap;
7. performs conditional radial and l=2 stability scouts;
8. measures the natural Coleman-Weinberg vacuum scale without double-counting
   it as a physical energy;
9. preserves the V18 fixed-order RG failure;
10. classifies collider bounds according to EFT validity.

This run is deliberately NOT a generic energy optimizer.

CLAIM LIMITS
------------
A successful result is still not a microscopic coupled field and not a
complete sub-10-MJ antigravity model.

Promotion still requires a solved chi/Psi/phi bag, exact local conservation,
full mode stability, renormalized RG/UV matching, empirical closure,
activation/reset, radiation, and nonlinear metric backreaction.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.physical_spherical_bag import (
    axial_spacelike_gap,
    fermion_cw_magnitude_proxy_j,
    friedberg_lee_bag_support,
    l2_wall_stiffness_scout_j,
    quartic_wall_parameters,
    radial_gamma_threshold,
    sphere_volume_m3,
    support_loop_naturalness,
    tilted_wall_potential_ev4,
    trace_load_epsilon,
    yukawa_mass_barrier,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)


ROOT = Path(
    __file__
).resolve().parents[1]

V18_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v18_universal_metric_rg_support_ready_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19_spherical_bag_support_uv_empirical_summary.json"
)

SUPPORT_SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19_false_vacuum_support_scan.csv"
)

CW_SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19_fermion_vacuum_scale_scan.csv"
)


TARGET_J = 1.0e7

REFERENCE_BAG_FRACTION = 0.95
REFERENCE_M_CHI_EV = 100.0
REFERENCE_OUTSIDE_MASS_FACTOR = 1.05

LHC_REFERENCE_TRANSFER_EV = 1.0e12
MAX_PERTURBATIVE_GSTAR = (
    4.0
    * math.pi
)


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
    V18_PATH.read_text(
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


field_energy_j = float(
    sphere[
        "field_energy_j"
    ]
)

band_energy_j = float(
    sphere[
        "occupied_band_energy_j"
    ]
)

fermion_pressure_perp_j = float(
    sphere[
        "fermion_pressure_perp_inventory_j"
    ]
)

fermion_pressure_z_j = float(
    sphere[
        "fermion_pressure_z_inventory_j"
    ]
)

v18_support_floor_j = float(
    sphere[
        "support_energy_floor_j"
    ]
)

v18_partial_j = float(
    sphere[
        "partial_conservative_floor_j"
    ]
)

metric_scale_ev = float(
    sphere[
        "metric_scale_ev"
    ]
)

radius_m = float(
    meanfield[
        "source_radius_m"
    ]
)

flavors = int(
    physical[
        "flavors"
    ]
)

f_psi_ev = float(
    physical[
        "f_psi_ev"
    ]
)

b_axial_ev = float(
    physical[
        "axial_b_ev"
    ]
)

m_psi_ev = float(
    physical[
        "m_psi_ev"
    ]
)

mu_ev = float(
    physical[
        "chemical_potential_ev"
    ]
)

cutoff_ev = float(
    physical[
        "nda_cutoff_ev"
    ]
)

delta_z_ll = float(
    physical[
        "leading_log_delta_z_proxy"
    ]
)


scalar_pi_perp_j = (
    -3.0
    * field_energy_j
    / 5.0
)

scalar_pi_z_j = (
    field_energy_j
    / 5.0
)

total_pressure_perp_j = (
    fermion_pressure_perp_j
    +
    scalar_pi_perp_j
)

total_pressure_z_j = (
    fermion_pressure_z_j
    +
    scalar_pi_z_j
)


support_rows = []

for bag_fraction in (
    0.0,
    0.50,
    0.90,
    0.95,
    0.98,
    0.99,
    0.997,
):
    result = (
        friedberg_lee_bag_support(
            radius_m=
                radius_m,

            pressure_perp_j=
                total_pressure_perp_j,

            pressure_z_j=
                total_pressure_z_j,

            bag_fraction=
                bag_fraction,
        )
    )

    subtotal = (
        field_energy_j
        +
        band_energy_j
        +
        result[
            "support_preflight_j"
        ]
    )

    support_rows.append(
        {
            "bag_fraction":
                bag_fraction,

            "bag_energy_j":
                result[
                    "bag_energy_j"
                ],

            "wall_energy_j":
                result[
                    "wall_energy_j"
                ],

            "anisotropy_reserve_floor_j":
                result[
                    "anisotropy_reserve_floor_j"
                ],

            "support_preflight_j":
                result[
                    "support_preflight_j"
                ],

            "static_subtotal_j":
                subtotal,

            "remaining_to_strict_10mj_j":
                TARGET_J
                - subtotal,

            "tension_anisotropy_ratio":
                result[
                    "tension_anisotropy_ratio"
                ],

            "conditional_radial_gamma_threshold":
                radial_gamma_threshold(
                    bag_fraction
                ),
        }
    )


reference_support = (
    friedberg_lee_bag_support(
        radius_m=
            radius_m,

        pressure_perp_j=
            total_pressure_perp_j,

        pressure_z_j=
            total_pressure_z_j,

        bag_fraction=
            REFERENCE_BAG_FRACTION,
    )
)


reference_wall = (
    quartic_wall_parameters(
        wall_tension_j_m2=
            reference_support[
                "wall_tension_j_m2"
            ],

        mediator_mass_ev=
            REFERENCE_M_CHI_EV,
    )
)


potential_grid = np.linspace(
    -3.0
    * reference_wall[
        "vev_ev"
    ],
    3.0
    * reference_wall[
        "vev_ev"
    ],
    120001,
)

potential_values = (
    tilted_wall_potential_ev4(
        potential_grid,
        vev_ev=
            reference_wall[
                "vev_ev"
            ],
        lambda_=
            reference_wall[
                "lambda"
            ],
        bag_density_j_m3=
            reference_support[
                "bag_energy_density_j_m3"
            ],
    )
)

potential_min_ev4 = float(
    np.min(
        potential_values
    )
)

potential_positive_with_tolerance = (
    potential_min_ev4
    >
    -1.0e-8
    * reference_wall[
        "degenerate_barrier_ev4"
    ]
)


mass_barrier = (
    yukawa_mass_barrier(
        inside_mass_ev=
            m_psi_ev,

        chemical_potential_ev=
            mu_ev,

        vev_ev=
            reference_wall[
                "vev_ev"
            ],

        outside_mass_factor=
            REFERENCE_OUTSIDE_MASS_FACTOR,
    )
)


support_loops = (
    support_loop_naturalness(
        flavors=
            flavors,

        yukawa=
            mass_barrier[
                "yukawa"
            ],

        lambda_=
            reference_wall[
                "lambda"
            ],

        cutoff_ev=
            cutoff_ev,

        mediator_mass_ev=
            REFERENCE_M_CHI_EV,
    )
)


bag_trace_epsilon = (
    trace_load_epsilon(
        energy_density_j_m3=
            reference_support[
                "bag_energy_density_j_m3"
            ],

        metric_scale_ev=
            metric_scale_ev,
    )
)

wall_energy_density_j_m3 = (
    reference_support[
        "wall_tension_j_m2"
    ]
    /
    reference_wall[
        "wall_thickness_m"
    ]
)

wall_trace_epsilon = (
    trace_load_epsilon(
        energy_density_j_m3=
            wall_energy_density_j_m3,

        metric_scale_ev=
            metric_scale_ev,
    )
)


axial_gap = (
    axial_spacelike_gap(
        b_ev=
            b_axial_ev,

        mass_ev=
            m_psi_ev,
    )
)


l2_stiffness = (
    l2_wall_stiffness_scout_j(
        reference_support[
            "wall_energy_j"
        ]
    )
)

l2_to_anisotropy = (
    l2_stiffness
    /
    reference_support[
        "anisotropy_reserve_floor_j"
    ]
)


source_volume_m3 = (
    sphere_volume_m3(
        radius_m
    )
)


cw_rows = []

for outside_factor in (
    1.01,
    1.02,
    1.05,
    1.10,
    1.25,
    1.50,
    2.00,
):
    barrier = (
        yukawa_mass_barrier(
            inside_mass_ev=
                m_psi_ev,

            chemical_potential_ev=
                mu_ev,

            vev_ev=
                reference_wall[
                    "vev_ev"
                ],

            outside_mass_factor=
                outside_factor,
        )
    )

    cw_proxy_j = (
        fermion_cw_magnitude_proxy_j(
            flavors=
                flavors,

            inside_mass_ev=
                m_psi_ev,

            outside_mass_ev=
                barrier[
                    "outside_mass_ev"
                ],

            volume_m3=
                source_volume_m3,
        )
    )

    cw_rows.append(
        {
            "outside_mass_factor":
                outside_factor,

            "outside_mass_ev":
                barrier[
                    "outside_mass_ev"
                ],

            "yukawa":
                barrier[
                    "yukawa"
                ],

            "decay_length_m":
                barrier[
                    "decay_length_m"
                ],

            "cw_natural_scale_proxy_j":
                cw_proxy_j,

            "cw_to_reference_bag_energy_ratio":
                (
                    cw_proxy_j
                    /
                    reference_support[
                        "bag_energy_j"
                    ]
                ),
        }
    )


reference_cw_proxy_j = (
    fermion_cw_magnitude_proxy_j(
        flavors=
            flavors,

        inside_mass_ev=
            m_psi_ev,

        outside_mass_ev=
            mass_barrier[
                "outside_mass_ev"
            ],

        volume_m3=
            source_volume_m3,
    )
)


reference_static_subtotal_j = (
    field_energy_j
    +
    band_energy_j
    +
    reference_support[
        "support_preflight_j"
    ]
)

reference_additive_cw_stress_test_j = (
    reference_static_subtotal_j
    +
    reference_cw_proxy_j
)


max_lhc_eft_transfer_ev = (
    MAX_PERTURBATIVE_GSTAR
    * metric_scale_ev
)

lhc_transfer_over_validity = (
    LHC_REFERENCE_TRANSFER_EV
    /
    max_lhc_eft_transfer_ev
)


assert (
    reference_support[
        "support_preflight_j"
    ]
    <
    1.0e6
)

assert (
    reference_static_subtotal_j
    <
    4.0e6
)

assert (
    reference_additive_cw_stress_test_j
    <
    TARGET_J
)

assert (
    potential_positive_with_tolerance
)

assert (
    support_loops[
        "delta_lambda_over_lambda"
    ]
    <
    1.0e-6
)

assert (
    support_loops[
        "delta_m2_over_m2"
    ]
    <
    1.0e-4
)

assert (
    axial_gap[
        "strict_b_below_m"
    ]
)

assert (
    delta_z_ll
    >
    1.0
)

assert (
    lhc_transfer_over_validity
    >
    1.0e6
)


with SUPPORT_SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                support_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        support_rows
    )


with CW_SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                cw_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        cw_rows
    )


summary = {
    "branch":
        "032V19_SPHERICAL_BAG_SUPPORT_UV_MATCHING_AND_EMPIRICAL_GATE",

    "claim_class":
        "PHYSICAL_SUPPORT_ACTION_PREFLIGHT_AND_QUANTUM_UV_FALSIFICATION",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "v18_reconstruction": {
        "partial_conservative_floor_j":
            v18_partial_j,

        "support_floor_j":
            v18_support_floor_j,

        "field_energy_j":
            field_energy_j,

        "occupied_band_energy_j":
            band_energy_j,

        "metric_scale_ev":
            metric_scale_ev,

        "surface_min_m_s2":
            float(
                sphere[
                    "surface_min_m_s2"
                ]
            ),

        "surface_max_m_s2":
            float(
                sphere[
                    "surface_max_m_s2"
                ]
            ),

        "complete_operating_ledger":
            False,
    },

    "support_action": {
        "architecture":
            "FRIEDBERG_LEE_FALSE_VACUUM_FERMION_BAG",

        "canonical_positive_energy_scalar":
            True,

        "false_vacuum_positive_energy":
            True,

        "false_vacuum_negative_pressure":
            True,

        "finite_wall":
            True,

        "hidden_fermion_yukawa_mass_barrier":
            True,

        "known_action_class_has_soliton_literature":
            True,

        "full_coupled_solution_constructed":
            False,
    },

    "reference_support": {
        **reference_support,

        "support_over_v18_floor":
            (
                reference_support[
                    "support_preflight_j"
                ]
                /
                v18_support_floor_j
            ),

        "extra_above_v18_floor_j":
            (
                reference_support[
                    "support_preflight_j"
                ]
                -
                v18_support_floor_j
            ),
    },

    "reference_wall": {
        **reference_wall,

        "potential_min_ev4_on_scan":
            potential_min_ev4,

        "potential_positive_with_tolerance":
            potential_positive_with_tolerance,

        "mediator_below_axial_nda_cutoff":
            (
                REFERENCE_M_CHI_EV
                <
                cutoff_ev
            ),
    },

    "reference_mass_barrier": {
        **mass_barrier,

        "macroscopic_confinement_ratio":
            (
                radius_m
                /
                mass_barrier[
                    "decay_length_m"
                ]
            ),
    },

    "support_quantum_naturalness": {
        **support_loops,

        "cw_natural_scale_proxy_j":
            reference_cw_proxy_j,

        "cw_to_bag_energy_ratio":
            (
                reference_cw_proxy_j
                /
                reference_support[
                    "bag_energy_j"
                ]
            ),

        "cw_proxy_is_automatically_additive_energy":
            False,

        "renormalized_vacuum_sign_and_counterterm_matching":
            "OPEN",
    },

    "support_trace_loading": {
        "bag_epsilon":
            bag_trace_epsilon,

        "wall_local_epsilon":
            wall_trace_epsilon,

        "small_in_reference_scout":
            (
                bag_trace_epsilon
                <
                1.0e-6
                and
                wall_trace_epsilon
                <
                1.0e-3
            ),
    },

    "stability_scout": {
        "conditional_radial_gamma_threshold":
            radial_gamma_threshold(
                REFERENCE_BAG_FRACTION
            ),

        "exact_fixed_number_gamma_measured":
            False,

        "l2_wall_stiffness_j":
            l2_stiffness,

        "l2_stiffness_to_anisotropy_floor":
            l2_to_anisotropy,

        "translation_l1":
            "WHOLE_BAG_GOLDSTONE_EXPECTED_RELATIVE_MODES_OPEN",

        "radial_l0_certified":
            False,

        "shape_l2_certified":
            False,
    },

    "axial_quantum": {
        **axial_gap,

        "f_psi_ev":
            f_psi_ev,

        "flavors":
            flavors,

        "nda_cutoff_ev":
            cutoff_ev,

        "leading_log_delta_z_proxy":
            delta_z_ll,

        "fixed_order_rg_control":
            False,

        "renormalized_fermion_determinant_complete":
            False,
    },

    "empirical_uv": {
        "kinetic_conformal_contact_operator_has_collider_searches":
            True,

        "candidate_metric_scale_ev":
            metric_scale_ev,

        "max_reference_gstar":
            MAX_PERTURBATIVE_GSTAR,

        "max_contact_eft_transfer_ev":
            max_lhc_eft_transfer_ev,

        "one_tev_transfer_over_contact_validity":
            lhc_transfer_over_validity,

        "direct_tev_contact_bound_transfer_to_candidate":
            False,

        "uv_completion_must_be_confronted_with_collider_data":
            True,

        "low_energy_ep_fifth_force_clock_atomic":
            "OPEN",

        "stellar_supernova":
            "OPEN_REQUIRES_UV_ABOVE_CUTOFF",

        "bbn_cosmology_hidden_thermalization":
            "OPEN_REQUIRES_UV_MATCHING",

        "empirical_pass":
            False,
    },

    "energy": {
        "reference_static_preflight_j":
            reference_static_subtotal_j,

        "remaining_to_strict_10mj_j":
            TARGET_J
            - reference_static_subtotal_j,

        "cw_additive_worst_case_scout_j":
            reference_additive_cw_stress_test_j,

        "cw_is_not_to_be_double_counted_with_bag_constant":
            True,

        "complete_operating_ledger":
            False,

        "certified_sub10mj":
            False,
    },

    "gate_status": {
        "physical_support_action_prefight":
            "GREEN",

        "support_energy_corridor":
            "GREEN_PARTIAL",

        "support_trace_loading":
            "GREEN_SCOUT",

        "spacelike_axial_gap":
            "GREEN",

        "radial_stability":
            "YELLOW_CONDITIONAL",

        "l2_shape_stability":
            "YELLOW_SCOUT",

        "renormalized_axial_vacuum":
            "YELLOW_OPEN",

        "fixed_order_rg":
            "RED",

        "outward_c1_uv_completion":
            "OPEN_RED_BLOCKER",

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
        (
            "GREEN_FALSE_VACUUM_BAG_SUPPORT_ACTION_PREFLIGHT_"
            "GREEN_STATIC_SUB4MJ_CORRIDOR_"
            "GREEN_SPACELIKE_AXIAL_GAP_"
            "RED_FIXED_ORDER_RG_"
            "UV_RENORMALIZED_VACUUM_STABILITY_EMPIRICAL_OPEN"
        ),

    "next":
        (
            "032V19R1_COUPLED_CHI_PSI_PHI_SPHERICAL_BAG_"
            "EQUILIBRIUM_RG_AND_MODE_GATE"
        ),
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


print(
    "BRANCH="
    + summary[
        "branch"
    ]
)

print(
    "V18_PARTIAL_J="
    f"{v18_partial_j:.12e}"
)

print(
    "REFERENCE_SUPPORT_J="
    f"{reference_support['support_preflight_j']:.12e}"
)

print(
    "SUPPORT_OVER_V18_FLOOR="
    f"{summary['reference_support']['support_over_v18_floor']:.12e}"
)

print(
    "REFERENCE_STATIC_PREFLIGHT_J="
    f"{reference_static_subtotal_j:.12e}"
)

print(
    "REMAINING_TO_10MJ_J="
    f"{TARGET_J-reference_static_subtotal_j:.12e}"
)

print(
    "REFERENCE_CW_NATURAL_SCALE_J="
    f"{reference_cw_proxy_j:.12e}"
)

print(
    "CW_TO_BAG_RATIO="
    f"{summary['support_quantum_naturalness']['cw_to_bag_energy_ratio']:.12e}"
)

print(
    "B_OVER_M="
    f"{axial_gap['b_over_m']:.12e}"
)

print(
    "AXIAL_GAP_EV="
    f"{axial_gap['gap_ev']:.12e}"
)

print(
    "DELTA_Z_LL="
    f"{delta_z_ll:.12e}"
)

print(
    "L2_STIFFNESS_TO_ANISOTROPY="
    f"{l2_to_anisotropy:.12e}"
)

print(
    "LHC_1TEV_OVER_MAX_CONTACT_VALIDITY="
    f"{lhc_transfer_over_validity:.12e}"
)

print(
    "COMPLETE_OPERATING_LEDGER="
    f"{summary['energy']['complete_operating_ledger']}"
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND="
    f"{summary['physical_antigravity_model_found']}"
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND="
    f"{summary['certified_sub10mj_model_found']}"
)

print(
    "DECISION="
    + summary[
        "decision"
    ]
)

print(
    "NEXT="
    + summary[
        "next"
    ]
)
