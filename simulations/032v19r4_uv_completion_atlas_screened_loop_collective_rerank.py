"""032V19R4 — theorem-first UV-completion atlas and rerank.

R3 closed the single canonical linear unscreened universal-trace scalar.

R4 tests:

- whether linear scalar species splitting rescues the current source;
- whether ordinary same-vertex screening rescues the coupling;
- whether a direct shift-protected Goldstone kinetic metric remains distinct;
- whether a Z2 loop-generated j=0 portal is worth a dedicated matching gate.

No generic energy optimization is performed.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.uv_completion_atlas import (
    atlas_records,
    narrow_band_linear_scalar_bound,
    same_vertex_screening_scout,
    z2_loop_generated_xt_scale,
)


ROOT = Path(
    __file__
).resolve().parents[1]

R3_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r3_scalar_trace_uv_completion_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r4_uv_completion_atlas_summary.json"
)

ATLAS_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r4_uv_completion_atlas.csv"
)

TARGET_J = 1.0e7

# This is deliberately a very loose graphical envelope above the
# Kamiya et al. 2020 Fig. 2(d) mass-coupled Yukawa exclusion curve
# throughout the R3 practical range ~0.6336 to ~3.4664 nm.
#
# It is NOT a digitized/tabulated experimental limit.
UPDATED_LOOSE_GRAPHICAL_G2_GEV_M2 = 1.0e-14


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


r3 = json.loads(
    R3_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    r3[
        "single_scalar_uv_template_rejected"
    ]
    is True
)

assert (
    r3[
        "kinetic_conformal_class_closed"
    ]
    is False
)


target = r3[
    "target"
]

declared = r3[
    "declared_cutoff_reference"
]

weak = r3[
    "optimistic_weak_floor"
]

energy_window = r3[
    "strict_energy_window"
]


c1 = float(
    target[
        "c1_ev_m4"
    ]
)

hard_scale_ev = float(
    target[
        "hard_scale_ev"
    ]
)

static_preflight_j = float(
    target[
        "static_preflight_j"
    ]
)

r3_declared_dx = float(
    declared[
        "d_x_ev_m4"
    ]
)

r3_declared_x_energy_j = float(
    declared[
        "source_x_positive_field_j"
    ]
)

source_x_inventory_j_per_ev_m4 = (
    r3_declared_x_energy_j
    / r3_declared_dx
)


# ============================================================
# 1. MULTI-SCALAR CAUCHY + EMPIRICAL + ENERGY GATE
# ============================================================

collective_bound = (
    narrow_band_linear_scalar_bound(
        target_c1_ev_m4=
            c1,

        minimum_mediator_mass_ev=
            hard_scale_ev,

        total_yukawa_g2_limit_gev_m2=
            UPDATED_LOOSE_GRAPHICAL_G2_GEV_M2,

        source_x_inventory_j_per_ev_m4=
            source_x_inventory_j_per_ev_m4,

        base_static_energy_j=
            static_preflight_j,

        energy_limit_j=
            TARGET_J,
    )
)


assert (
    collective_bound[
        "passes_strict_energy_limit"
    ]
    is False
)


# Lowest mass has the weakest R3 single-scalar off-state coupling.
# Compare its g^2 with the updated deliberately loose envelope.

r3_weakest_g2 = float(
    weak[
        "mass_force_g2_gev_m2"
    ]
)

species_splitting_strength_ratio = (
    r3_weakest_g2
    /
    UPDATED_LOOSE_GRAPHICAL_G2_GEV_M2
)


# ============================================================
# 2. SAME-VERTEX SCREENING GATE
# ============================================================

screening = (
    same_vertex_screening_scout(
        unscreened_g2_gev_m2=
            r3_weakest_g2,

        empirical_g2_limit_gev_m2=
            UPDATED_LOOSE_GRAPHICAL_G2_GEV_M2,
    )
)


assert (
    screening[
        "same_vertex_target_preserved_without_descreening"
    ]
    is False
)


# ============================================================
# 3. Z2 LOOP-GENERATED j=0 SCAFFOLD
# ============================================================

z2_loop = (
    z2_loop_generated_xt_scale(
        target_c1_ev_m4=
            c1
    )
)


assert (
    z2_loop[
        "equal_portal_scale_ev"
    ]
    >
    100.0
    * hard_scale_ev
)

assert (
    z2_loop[
        "complete_uv_origin"
    ]
    is False
)


# ============================================================
# 4. FAMILY ATLAS
# ============================================================

records = atlas_records()

for row in records:
    if (
        row[
            "family"
        ]
        ==
        "NARROW_BAND_LINEAR_SCALAR_TOWER_CURRENT_SOURCE"
    ):
        row[
            "status"
        ] = (
            "CLOSED_R4_CURRENT_SOURCE"
        )

        row[
            "reason"
        ] = (
            "CAUCHY_PLUS_NANOMETER_FIFTH_FORCE_FORCES_X2_ENERGY_ABOVE_10MJ"
        )


# ============================================================
# 5. CLASSIFICATION
# ============================================================

narrow_band_current_source_closed = bool(
    not collective_bound[
        "passes_strict_energy_limit"
    ]
)

ordinary_screening_direct_rescue_closed = bool(
    not screening[
        "same_vertex_target_preserved_without_descreening"
    ]
)

goldstone_route_open = True
z2_loop_scaffold_open = True

kinetic_conformal_class_closed = False


decision = (
    "RED_NARROW_BAND_LINEAR_SCALAR_TOWER_FOR_CURRENT_SOURCE_"
    "BY_CAUCHY_EMPIRICAL_ENERGY_BOUND_"
    "RED_DENSITY_ONLY_SAME_VERTEX_SCREENING_AS_DIRECT_RESCUE_"
    "YELLOW_Z2_LOOP_J0_MATCHING_SCAFFOLD_"
    "YELLOW_HIGHEST_PRIORITY_SHIFT_PROTECTED_GOLDSTONE_KINETIC_METRIC_UV_ORIGIN_"
    "KINETIC_CONFORMAL_CLASS_NOT_CLOSED"
)

next_step = (
    "032V19R5_SHIFT_PROTECTED_GOLDSTONE_UV_ORIGIN_"
    "AND_Z2_LOOP_MATCHING_SIGN_NATURALNESS_GATE"
)


summary = {
    "branch":
        "032V19R4_UV_COMPLETION_ATLAS_SCREENED_LOOP_GENERATED_AND_COLLECTIVE_J0_RERANK",

    "claim_class":
        "THEOREM_FIRST_UV_COMPLETION_FAMILY_RERANK",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "r3_input_decision":
        r3[
            "decision"
        ],

    "target": {
        "c1_ev_m4":
            c1,

        "hard_scale_ev":
            hard_scale_ev,

        "static_preflight_j":
            static_preflight_j,

        "r3_practical_range_min_nm":
            float(
                energy_window[
                    "minimum_practical_range_nm"
                ]
            ),

        "r3_practical_range_max_nm":
            float(
                energy_window[
                    "maximum_practical_range_nm"
                ]
            ),
    },

    "updated_neutron_empirical_scout": {
        "experiment":
            "KAMIYA_ET_AL_2020_SLOW_NEUTRON_XENON",

        "reported_improved_range_nm": [
            0.3,
            9.0,
        ],

        "graphical_envelope_g2_gev_m2":
            UPDATED_LOOSE_GRAPHICAL_G2_GEV_M2,

        "graphical_envelope_is_tabulated_limit":
            False,

        "graphical_envelope_is_deliberately_loose":
            True,

        "r3_practical_window_inside_scope":
            True,
    },

    "linear_scalar_collective_bound": {
        **collective_bound,

        "cauchy_identity":
            "C1_SQUARED_LE_4_DX_DT",

        "species_splitting_strength_ratio":
            species_splitting_strength_ratio,

        "narrow_band_current_source_closed":
            narrow_band_current_source_closed,

        "broad_spectral_tower_closed":
            False,

        "reason_broad_not_closed":
            "FULL_MULTI_YUKAWA_EXPERIMENTAL_LIKELIHOOD_NOT_RECONSTRUCTED",
    },

    "screening": {
        **screening,

        "density_only_same_vertex_direct_rescue_closed":
            ordinary_screening_direct_rescue_closed,

        "active_x_dependent_descreening_closed":
            False,

        "minimal_published_asymmetron_reopened":
            False,
    },

    "goldstone_kinetic_metric": {
        "published_global_abelian_goldstone_provenance":
            True,

        "shift_symmetry_forbids_direct_goldstone_yukawa":
            True,

        "universal_kinetic_conformal_metric_action_provenance":
            True,

        "published_models_can_have_repulsive_behavior":
            True,

        "project_required_static_outward_sign_uv_proved":
            False,

        "microscopic_derivative_portal_uv_origin_complete":
            False,

        "negative_mass_required":
            False,

        "status":
            "YELLOW_HIGHEST_PRIORITY_STRUCTURAL_SURVIVOR",
    },

    "z2_loop_generated_j0": {
        **z2_loop,

        "portal_scale_over_source_hard":
            (
                float(
                    z2_loop[
                        "equal_portal_scale_ev"
                    ]
                )
                / hard_scale_ev
            ),

        "negative_mass_required":
            False,

        "two_mediator_exchange_empirical_gate":
            "OPEN",
    },

    "gate_status": {
        "single_linear_scalar":
            "CLOSED_R3",

        "narrow_band_linear_scalar_tower_current_source":
            "CLOSED_R4",

        "broad_spectral_linear_scalar_tower":
            "YELLOW_LIKELIHOOD_REQUIRED",

        "density_only_same_trace_vertex_screening":
            "RED_AS_DIRECT_RESCUE",

        "active_x_descreening":
            "YELLOW_NEW_PHYSICS",

        "direct_shift_protected_goldstone_kinetic_metric":
            "YELLOW_HIGHEST_PRIORITY",

        "z2_loop_generated_j0":
            "YELLOW_SECOND_PRIORITY",

        "spin2_tree":
            "CLOSED_PRESERVED",

        "minimal_asymmetron":
            "CLOSED_PRESERVED",

        "boundary_axial_vacuum":
            "OPEN",

        "full_c1_f_mass_rge":
            "OPEN",

        "full_coupled_chi_psi_phi_modes":
            "OPEN",

        "complete_operating_energy":
            "NOT_ESTABLISHED",

        "empirical_closure":
            "OPEN",
    },

    "physical_antigravity_model_found":
        False,

    "certified_sub10mj_model_found":
        False,

    "kinetic_conformal_class_closed":
        kinetic_conformal_class_closed,

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


with ATLAS_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "family",
            "status",
            "reason",
        ],
    )

    writer.writeheader()
    writer.writerows(
        records
    )


print(
    "BRANCH="
    + summary[
        "branch"
    ]
)

print(
    "TARGET_C1_EV_M4="
    f"{c1:.12e}"
)

print(
    "SOURCE_X_INVENTORY_J_PER_EV_M4="
    f"{source_x_inventory_j_per_ev_m4:.12e}"
)

print(
    "UPDATED_LOOSE_NEUTRON_G2_ENVELOPE="
    f"{UPDATED_LOOSE_GRAPHICAL_G2_GEV_M2:.12e}"
)

print(
    "CAUCHY_DX_MIN_EV_M4="
    f"{float(collective_bound['d_x_min_ev_m4']):.12e}"
)

print(
    "CAUCHY_X_ENERGY_MIN_J="
    f"{float(collective_bound['x_companion_energy_min_j']):.12e}"
)

print(
    "CAUCHY_BASE_PLUS_X_FLOOR_J="
    f"{float(collective_bound['base_plus_x_floor_j']):.12e}"
)

print(
    "CAUCHY_X_OVER_REMAINING_BUDGET="
    f"{float(collective_bound['x_energy_over_remaining_budget']):.12e}"
)

print(
    "R3_WEAKEST_G2_OVER_UPDATED_ENVELOPE="
    f"{species_splitting_strength_ratio:.12e}"
)

print(
    "SAME_VERTEX_SCREENING_RETENTION_MAX="
    f"{float(screening['required_matter_amplitude_retention_max']):.12e}"
)

print(
    "Z2_LOOP_EQUAL_PORTAL_SCALE_EV="
    f"{float(z2_loop['equal_portal_scale_ev']):.12e}"
)

print(
    "Z2_LOOP_PORTAL_OVER_HARD="
    f"{float(z2_loop['equal_portal_scale_ev'])/hard_scale_ev:.12e}"
)

print(
    "NARROW_BAND_LINEAR_SCALAR_TOWER_CURRENT_SOURCE_CLOSED="
    + str(
        narrow_band_current_source_closed
    )
)

print(
    "BROAD_SPECTRAL_LINEAR_SCALAR_TOWER_CLOSED=False"
)

print(
    "DENSITY_ONLY_SAME_VERTEX_SCREENING_RESCUE="
    + str(
        not ordinary_screening_direct_rescue_closed
    )
)

print(
    "ACTIVE_X_DESCREENING_OPEN=True"
)

print(
    "DIRECT_SHIFT_PROTECTED_GOLDSTONE_ROUTE_OPEN="
    + str(
        goldstone_route_open
    )
)

print(
    "Z2_LOOP_J0_SCAFFOLD_OPEN="
    + str(
        z2_loop_scaffold_open
    )
)

print(
    "NEGATIVE_MASS_REQUIRED=False"
)

print(
    "KINETIC_CONFORMAL_CLASS_CLOSED=False"
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
