"""032V19R3 — outward-sign scalar UV completion and companion falsification.

PURPOSE
-------
R2 preserved the supported 1g state and showed that:

- fixed-order axial RG remains structurally red;
- large-Nf determinant organization is available;
- no bulk multi-MJ axial-vacuum catastrophe was found;
- the published Jiang positive-C1 spin-2 template is not a pure j=0
  completion.

R3 therefore attacks the required outward-sign universal UV completion
directly.

TEMPLATE
--------
Test one new, genuinely different healthy UV template:

    ONE CANONICAL REAL SCALAR sigma

with

    sigma T/F_T

through one universal conformal matter metric and

    - sigma X/F_X,

where

    X = (partial phi)^2.

Tree-level matching generates

    - C1 X T

with the required positive C1 but necessarily also

    D_X X^2
    +
    D_T T^2.

The same sigma T coupling produces an off-state mass-coupled Yukawa force.

CHEAP FALSIFICATION ORDER
-------------------------
1. Prove tree-level sign.
2. Prove rank-one companion relation.
3. Derive weakest possible matter coupling on the optimistic NDA boundary.
4. Derive payload-only positive mediator field inventory.
5. Use strict 10-MJ policy to derive an optimistic mediator-mass ceiling.
6. Map the resulting entire practical mediator window to published
   nanometer-range fifth-force constraints.
7. Only if this survives would a nonlinear sigma PDE be justified.

This is not a generic energy optimization.

CLAIM LIMIT
-----------
A red result closes only the single canonical linear unscreened universal
trace scalar-exchange UV template.

It does not close the kinetic-conformal class.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.c1_payload_matching import (
    c1_from_metric_scale_ev,
)
from antigravity_research.agminer.kinetic_conformal import (
    HBARC_EV_M,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.scalar_trace_uv_completion import (
    KAMIYA_GRAPHICAL_SCOUT_MAX_NM,
    KAMIYA_GRAPHICAL_SCOUT_MIN_NM,
    KAMIYA_LIMIT_0P1_NM_GEV_M2,
    KAMIYA_LIMIT_1P0_NM_GEV_M2,
    KAMIYA_RANGE_MAX_NM,
    KAMIYA_RANGE_MIN_NM,
    KAMIYA_ULTRACONSERVATIVE_GRAPHICAL_ENVELOPE_GEV_M2,
    graphical_empirical_scout,
    kamiya_exact_anchor,
    practical_mediator_mass_ceiling_ev,
    scalar_trace_tree_match,
    uniform_source_x_field_energy_j,
    uniform_sphere_trace_field_energy_j,
    weak_single_scalar_best_case,
)


ROOT = Path(
    __file__
).resolve().parents[1]

R1_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r1_local_traction_shape_payload_rg_summary.json"
)

R2_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r2_large_nf_rg_axial_vacuum_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r3_scalar_trace_uv_completion_summary.json"
)

SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r3_scalar_uv_scan.csv"
)

EMPIRICAL_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r3_empirical_anchor_scan.csv"
)


TARGET_J = 1.0e7

PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10
SOURCE_RADIUS_M = 0.10


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


r1 = json.loads(
    R1_PATH.read_text(
        encoding="utf-8"
    )
)

r2 = json.loads(
    R2_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    r2[
        "decision"
    ]
    ==
    "GREEN_LARGE_NF_AXIAL_REORGANIZATION_AVAILABLE_GREEN_NONCATASTROPHIC_BULK_VACUUM_SCOUT_RED_DIRECT_JIANG_SPIN2_TEMPLATE_FOR_PURE_J0_OUTWARD_SIGN_UV_COMPLETION_BOUNDARY_VACUUM_AND_FULL_RGE_OPEN"
)


selected = r1[
    "selected_retuned_reference"
]

source = r2[
    "source"
]


metric_scale_ev = float(
    source[
        "metric_scale_ev"
    ]
)

target_c1 = (
    c1_from_metric_scale_ev(
        metric_scale_ev
    )
)

hard_scale_ev = float(
    source[
        "hard_scale_ev"
    ]
)

declared_cutoff_ev = float(
    source[
        "declared_cutoff_ev"
    ]
)

static_preflight_j = float(
    source[
        "static_preflight_j"
    ]
)

axial_b_ev = float(
    source[
        "axial_b_ev"
    ]
)

f_psi_ev = float(
    source[
        "f_psi_ev"
    ]
)


# ============================================================
# 1. BEST POSSIBLE WEAK SINGLE-SCALAR ENDPOINT
# ============================================================

weak_floor = (
    weak_single_scalar_best_case(
        mediator_mass_ev=
            hard_scale_ev,

        target_c1_ev_m4=
            target_c1,

        nda_margin=
            1.0,
    )
)


floor_match = (
    scalar_trace_tree_match(
        mediator_mass_ev=
            hard_scale_ev,

        f_x_ev=
            float(
                weak_floor[
                    "f_x_ev"
                ]
            ),

        f_t_ev=
            float(
                weak_floor[
                    "f_t_ev"
                ]
            ),
    )
)


assert (
    floor_match[
        "positive_c1"
    ]
)

assert (
    floor_match[
        "static_outward_sign_target"
    ]
)

assert (
    floor_match[
        "tree_spin2_companion"
    ]
    is False
)

assert (
    floor_match[
        "negative_mass_required"
    ]
    is False
)

assert (
    floor_match[
        "rank_one_psd_companion_identity"
    ]
)


# ============================================================
# 2. PAYLOAD-ONLY POSITIVE MEDIATOR FIELD FLOOR
# ============================================================

floor_payload_field = (
    uniform_sphere_trace_field_energy_j(
        mediator_mass_ev=
            hard_scale_ev,

        f_t_ev=
            float(
                weak_floor[
                    "f_t_ev"
                ]
            ),

        source_mass_kg=
            PAYLOAD_MASS_KG,

        source_radius_m=
            PAYLOAD_RADIUS_M,
    )
)


floor_total_lower_bound_j = (
    static_preflight_j
    +
    float(
        floor_payload_field[
            "conservative_ledger_charge_j"
        ]
    )
)


# ============================================================
# 3. OPTIMISTIC STRICT-10-MJ MEDIATOR MASS CEILING
# ============================================================

mass_ceiling = (
    practical_mediator_mass_ceiling_ev(
        minimum_mass_ev=
            hard_scale_ev,

        target_c1_ev_m4=
            target_c1,

        base_static_energy_j=
            static_preflight_j,

        energy_limit_j=
            TARGET_J,

        payload_mass_kg=
            PAYLOAD_MASS_KG,

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        nda_margin=
            1.0,
    )
)


assert (
    mass_ceiling[
        "window_exists"
    ]
)


mass_ceiling_ev = float(
    mass_ceiling[
        "mass_ceiling_ev"
    ]
)

minimum_practical_range_nm = float(
    mass_ceiling[
        "mass_ceiling_range_nm"
    ]
)

maximum_practical_range_nm = float(
    weak_floor[
        "interaction_range_nm"
    ]
)


# Because the payload-only lower bound hits exactly 10 MJ at the ceiling,
# strict policy requires the actual mediator mass to lie BELOW this value.

assert (
    minimum_practical_range_nm
    >
    KAMIYA_GRAPHICAL_SCOUT_MIN_NM
)

assert (
    maximum_practical_range_nm
    <
    KAMIYA_GRAPHICAL_SCOUT_MAX_NM
)


# ============================================================
# 4. EMPIRICAL FLOOR ACROSS THE ENTIRE PRACTICAL WINDOW
# ============================================================

floor_empirical = (
    graphical_empirical_scout(
        interaction_range_nm=
            maximum_practical_range_nm,

        predicted_g2_gev_m2=
            float(
                weak_floor[
                    "mass_force_g2_gev_m2"
                ]
            ),
    )
)


# On the optimistic NDA boundary:
#
#     F_T,max ~ m^-3
#     g_min^2 ~ m^6.
#
# Therefore this lowest-mass endpoint has the weakest fifth force in the
# entire practical mediator window.

assert (
    floor_empirical[
        "excluded_by_graphical_envelope_scout"
    ]
)

assert (
    floor_empirical[
        "predicted_over_graphical_envelope"
    ]
    >
    400.0
)


entire_practical_window_graphically_excluded = bool(
    floor_empirical[
        "excluded_by_graphical_envelope_scout"
    ]
    and
    minimum_practical_range_nm
    >=
    KAMIYA_GRAPHICAL_SCOUT_MIN_NM
    and
    maximum_practical_range_nm
    <=
    KAMIYA_GRAPHICAL_SCOUT_MAX_NM
)


# ============================================================
# 5. EXACT PUBLISHED EMPIRICAL ANCHORS
# ============================================================

empirical_rows = []

for range_nm in (
    1.0,
    0.1,
):
    anchor = (
        kamiya_exact_anchor(
            range_nm
        )
    )

    mediator_mass = float(
        anchor[
            "mediator_mass_ev"
        ]
    )

    weak = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                mediator_mass,

            target_c1_ev_m4=
                target_c1,

            nda_margin=
                1.0,
        )
    )

    field = (
        uniform_sphere_trace_field_energy_j(
            mediator_mass_ev=
                mediator_mass,

            f_t_ev=
                float(
                    weak[
                        "f_t_ev"
                    ]
                ),

            source_mass_kg=
                PAYLOAD_MASS_KG,

            source_radius_m=
                PAYLOAD_RADIUS_M,
        )
    )

    predicted_g2 = float(
        weak[
            "mass_force_g2_gev_m2"
        ]
    )

    published_limit = float(
        anchor[
            "limit_g2_gev_m2"
        ]
    )

    empirical_rows.append(
        {
            "range_nm":
                range_nm,

            "mediator_mass_ev":
                mediator_mass,

            "predicted_best_case_g2_gev_m2":
                predicted_g2,

            "published_95cl_limit_g2_gev_m2":
                published_limit,

            "predicted_over_limit":
                predicted_g2
                / published_limit,

            "payload_mediator_field_j":
                float(
                    field[
                        "conservative_ledger_charge_j"
                    ]
                ),

            "static_plus_payload_mediator_j":
                static_preflight_j
                +
                float(
                    field[
                        "conservative_ledger_charge_j"
                    ]
                ),

            "inside_strict_10mj_payload_only":
                (
                    static_preflight_j
                    +
                    float(
                        field[
                            "conservative_ledger_charge_j"
                        ]
                    )
                    <
                    TARGET_J
                ),
        }
    )


one_nm = empirical_rows[
    0
]

assert (
    one_nm[
        "predicted_over_limit"
    ]
    >
    6.0e9
)

assert (
    one_nm[
        "inside_strict_10mj_payload_only"
    ]
    is True
)


# ============================================================
# 6. DECLARED R2-CUTOFF MEDIATOR REFERENCE
# ============================================================

declared = (
    weak_single_scalar_best_case(
        mediator_mass_ev=
            declared_cutoff_ev,

        target_c1_ev_m4=
            target_c1,

        nda_margin=
            1.0,
    )
)


declared_payload_field = (
    uniform_sphere_trace_field_energy_j(
        mediator_mass_ev=
            declared_cutoff_ev,

        f_t_ev=
            float(
                declared[
                    "f_t_ev"
                ]
            ),

        source_mass_kg=
            PAYLOAD_MASS_KG,

        source_radius_m=
            PAYLOAD_RADIUS_M,
    )
)


declared_x_field = (
    uniform_source_x_field_energy_j(
        mediator_mass_ev=
            declared_cutoff_ev,

        f_x_ev=
            float(
                declared[
                    "f_x_ev"
                ]
            ),

        axial_b_ev=
            axial_b_ev,

        f_psi_ev=
            f_psi_ev,

        source_radius_m=
            SOURCE_RADIUS_M,
    )
)


declared_total_lower_bound_j = (
    static_preflight_j
    +
    float(
        declared_payload_field[
            "conservative_ledger_charge_j"
        ]
    )
    +
    float(
        declared_x_field[
            "positive_x_field_inventory_j"
        ]
    )
)


# The equality F_X = f_psi here is not a new invariant.
#
# It occurs because the R2 declared cutoff was 4 pi f_psi and we have chosen
# m_sigma equal to that declared cutoff while saturating 4 pi F_X=m_sigma.

declared_fx_to_fpsi = (
    float(
        declared[
            "f_x_ev"
        ]
    )
    / f_psi_ev
)


# ============================================================
# 7. PHYSICALLY MOTIVATED MASS SCAN
# ============================================================

one_nm_mass_ev = (
    HBARC_EV_M
    / 1.0e-9
)

point_one_nm_mass_ev = (
    HBARC_EV_M
    / 1.0e-10
)

candidate_masses = sorted(
    {
        hard_scale_ev,
        75.0,
        100.0,
        150.0,
        one_nm_mass_ev,
        250.0,
        declared_cutoff_ev,
        mass_ceiling_ev,
        400.0,
        point_one_nm_mass_ev,
    }
)


scan_rows = []

for mediator_mass in candidate_masses:
    weak = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                mediator_mass,

            target_c1_ev_m4=
                target_c1,

            nda_margin=
                1.0,
        )
    )

    field = (
        uniform_sphere_trace_field_energy_j(
            mediator_mass_ev=
                mediator_mass,

            f_t_ev=
                float(
                    weak[
                        "f_t_ev"
                    ]
                ),

            source_mass_kg=
                PAYLOAD_MASS_KG,

            source_radius_m=
                PAYLOAD_RADIUS_M,
        )
    )

    total = (
        static_preflight_j
        +
        float(
            field[
                "conservative_ledger_charge_j"
            ]
        )
    )

    graphical = (
        graphical_empirical_scout(
            interaction_range_nm=
                float(
                    weak[
                        "interaction_range_nm"
                    ]
                ),

            predicted_g2_gev_m2=
                float(
                    weak[
                        "mass_force_g2_gev_m2"
                    ]
                ),
        )
    )

    scan_rows.append(
        {
            "mediator_mass_ev":
                mediator_mass,

            "interaction_range_nm":
                float(
                    weak[
                        "interaction_range_nm"
                    ]
                ),

            "f_x_ev":
                float(
                    weak[
                        "f_x_ev"
                    ]
                ),

            "f_t_gev":
                float(
                    weak[
                        "f_t_gev"
                    ]
                ),

            "predicted_mass_force_g2_gev_m2":
                float(
                    weak[
                        "mass_force_g2_gev_m2"
                    ]
                ),

            "payload_positive_mediator_field_j":
                float(
                    field[
                        "conservative_ledger_charge_j"
                    ]
                ),

            "static_plus_payload_mediator_j":
                total,

            "strict_sub10mj_payload_only":
                (
                    total
                    <
                    TARGET_J
                ),

            "within_graphical_empirical_scope":
                bool(
                    graphical[
                        "within_graphical_scout_scope"
                    ]
                ),

            "predicted_over_loose_graphical_envelope":
                float(
                    graphical[
                        "predicted_over_graphical_envelope"
                    ]
                ),

            "graphical_empirical_scout_excluded":
                bool(
                    graphical[
                        "excluded_by_graphical_envelope_scout"
                    ]
                ),
        }
    )


# ============================================================
# 8. CLASSIFICATION
# ============================================================

single_scalar_template_rejected = bool(
    floor_match[
        "rank_one_psd_companion_identity"
    ]
    and
    entire_practical_window_graphically_excluded
    and
    one_nm[
        "predicted_over_limit"
    ]
    >
    1.0e6
)


assert (
    single_scalar_template_rejected
)


decision = (
    "RED_WEAK_SINGLE_CANONICAL_LINEAR_UNIVERSAL_TRACE_SCALAR_UV_TEMPLATE_"
    "GREEN_TREE_J0_OUTWARD_MATCH_"
    "RED_RANKONE_COMPANIONS_"
    "RED_NANOMETER_OFFSTATE_FIFTH_FORCE_"
    "KINETIC_CONFORMAL_CLASS_NOT_CLOSED"
)

next_step = (
    "032V19R4_UV_COMPLETION_ATLAS_"
    "SCREENED_LOOP_GENERATED_AND_COLLECTIVE_J0_RERANK"
)


summary = {
    "branch":
        "032V19R3_OUTWARD_SIGN_UV_COMPLETION_AND_COMPANION_OPERATOR_FALSIFICATION_GATE",

    "claim_class":
        "SINGLE_SCALAR_UV_TEMPLATE_TREE_MATCH_AND_EMPIRICAL_FALSIFICATION",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "r2_input_decision":
        r2[
            "decision"
        ],

    "target": {
        "metric_scale_ev":
            metric_scale_ev,

        "c1_ev_m4":
            target_c1,

        "hard_scale_ev":
            hard_scale_ev,

        "declared_source_cutoff_ev":
            declared_cutoff_ev,

        "static_preflight_j":
            static_preflight_j,
    },

    "uv_action_template": {
        "mediator":
            "ONE_CANONICAL_REAL_SCALAR_SIGMA",

        "matter_metric":
            "EXP_2SIGMA_OVER_FT_TIMES_G",

        "x_interaction":
            "MINUS_SIGMA_X_OVER_FX",

        "canonical_positive_energy":
            True,

        "positive_mass_squared":
            True,

        "negative_mass_required":
            False,

        "universal_metric_at_action_level":
            True,

        "tree_spin2_companion":
            False,

        "tree_j2_companion":
            False,

        "screening_present":
            False,

        "linear_unscreened_template":
            True,
    },

    "tree_matching": {
        "c1_ev_m4":
            floor_match[
                "c1_ev_m4"
            ],

        "cross_xt_coefficient_ev_m4":
            floor_match[
                "cross_xt_coefficient_ev_m4"
            ],

        "d_x_ev_m4":
            floor_match[
                "d_x_ev_m4"
            ],

        "d_t_ev_m4":
            floor_match[
                "d_t_ev_m4"
            ],

        "rank_one_identity":
            "C1_SQUARED_EQUALS_4_DX_DT",

        "rank_one_identity_relative_error":
            floor_match[
                "rank_one_identity_relative_error"
            ],

        "positive_outward_c1":
            True,
    },

    "optimistic_weak_floor": {
        **weak_floor,

        "payload_positive_mediator_field_j":
            floor_payload_field[
                "conservative_ledger_charge_j"
            ],

        "static_plus_payload_mediator_j":
            floor_total_lower_bound_j,

        "this_is_complete_operating_energy":
            False,
    },

    "strict_energy_window": {
        **mass_ceiling,

        "maximum_practical_range_nm":
            maximum_practical_range_nm,

        "minimum_practical_range_nm":
            minimum_practical_range_nm,

        "entire_window_inside_kamiya_reported_0p04_to_4nm_range":
            (
                minimum_practical_range_nm
                >=
                KAMIYA_RANGE_MIN_NM
                and
                maximum_practical_range_nm
                <=
                KAMIYA_RANGE_MAX_NM
            ),

        "source_support_trace_costs_included":
            False,

        "mass_ceiling_is_optimistic":
            True,
    },

    "empirical": {
        "interaction":
            "OFFSTATE_MASS_COUPLED_YUKAWA",

        "mapping":
            "G2_EQUALS_1_OVER_FT_GEV_SQUARED",

        "cosmological_background_required":
            False,

        "collider_contact_extrapolation_required":
            False,

        "kamiya_reported_range_min_nm":
            KAMIYA_RANGE_MIN_NM,

        "kamiya_reported_range_max_nm":
            KAMIYA_RANGE_MAX_NM,

        "kamiya_exact_0p1nm_limit_g2_gev_m2":
            KAMIYA_LIMIT_0P1_NM_GEV_M2,

        "kamiya_exact_1nm_limit_g2_gev_m2":
            KAMIYA_LIMIT_1P0_NM_GEV_M2,

        "ultraconservative_graphical_envelope_g2_gev_m2":
            KAMIYA_ULTRACONSERVATIVE_GRAPHICAL_ENVELOPE_GEV_M2,

        "graphical_envelope_is_tabulated_limit":
            False,

        "graphical_scout_range_nm": [
            KAMIYA_GRAPHICAL_SCOUT_MIN_NM,
            KAMIYA_GRAPHICAL_SCOUT_MAX_NM,
        ],

        "weakest_practical_point_over_graphical_envelope":
            floor_empirical[
                "predicted_over_graphical_envelope"
            ],

        "entire_practical_window_graphically_excluded":
            entire_practical_window_graphically_excluded,

        "exact_1nm_predicted_over_limit":
            one_nm[
                "predicted_over_limit"
            ],

        "single_linear_scalar_template_empirically_viable":
            False,
    },

    "declared_cutoff_reference": {
        **declared,

        "f_x_over_r1_fpsi":
            declared_fx_to_fpsi,

        "payload_positive_mediator_field_j":
            declared_payload_field[
                "conservative_ledger_charge_j"
            ],

        "source_x_positive_field_j":
            declared_x_field[
                "positive_x_field_inventory_j"
            ],

        "static_plus_payload_and_x_lower_bound_j":
            declared_total_lower_bound_j,

        "remaining_to_10mj_before_other_omissions_j":
            TARGET_J
            -
            declared_total_lower_bound_j,

        "complete_operating_ledger":
            False,
    },

    "gate_status": {
        "positive_c1_tree_match":
            "GREEN",

        "one_universal_metric":
            "GREEN_TEMPLATE",

        "negative_mass":
            "NOT_USED",

        "tree_spin2_companions":
            "ABSENT",

        "rank_one_scalar_companions":
            "RED_UNAVOIDABLE",

        "strict_energy_window":
            "GREEN_AS_OPTIMISTIC_LOWER_BOUND_ONLY",

        "offstate_mass_force":
            "RED",

        "exact_1nm_empirical_anchor":
            "RED_BY_MORE_THAN_1E9",

        "entire_practical_window_empirical_curve":
            "RED_GRAPHICAL_SCOUT",

        "single_linear_scalar_uv_template":
            "CLOSED",

        "kinetic_conformal_class":
            "NOT_CLOSED",

        "large_nf_r2_result":
            "PRESERVED",

        "boundary_axial_vacuum":
            "OPEN",

        "full_c1_f_mass_rge":
            "OPEN",

        "full_coupled_chi_psi_phi_modes":
            "OPEN",

        "complete_operating_energy":
            "NOT_ESTABLISHED",

        "empirical_closure_of_other_uv_templates":
            "OPEN",
    },

    "physical_antigravity_model_found":
        False,

    "certified_sub10mj_model_found":
        False,

    "single_scalar_uv_template_rejected":
        single_scalar_template_rejected,

    "kinetic_conformal_class_closed":
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


with EMPIRICAL_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                empirical_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        empirical_rows
    )


print(
    "BRANCH="
    + summary[
        "branch"
    ]
)

print(
    "TARGET_C1_EV_M4="
    f"{target_c1:.12e}"
)

print(
    "HARD_SCALE_EV="
    f"{hard_scale_ev:.12e}"
)

print(
    "BEST_CASE_FX_EV="
    f"{float(weak_floor['f_x_ev']):.12e}"
)

print(
    "BEST_CASE_FT_GEV="
    f"{float(weak_floor['f_t_gev']):.12e}"
)

print(
    "BEST_CASE_G2_GEV_M2="
    f"{float(weak_floor['mass_force_g2_gev_m2']):.12e}"
)

print(
    "BEST_CASE_RANGE_NM="
    f"{maximum_practical_range_nm:.12e}"
)

print(
    "BEST_CASE_PAYLOAD_SIGMA_FIELD_J="
    f"{float(floor_payload_field['conservative_ledger_charge_j']):.12e}"
)

print(
    "OPTIMISTIC_MASS_CEILING_EV="
    f"{mass_ceiling_ev:.12e}"
)

print(
    "OPTIMISTIC_MIN_RANGE_NM="
    f"{minimum_practical_range_nm:.12e}"
)

print(
    "WEAKEST_POINT_OVER_LOOSE_EMPIRICAL_ENVELOPE="
    f"{float(floor_empirical['predicted_over_graphical_envelope']):.12e}"
)

print(
    "ONE_NM_PREDICTED_OVER_EXACT_LIMIT="
    f"{float(one_nm['predicted_over_limit']):.12e}"
)

print(
    "DECLARED_MEDIATOR_PAYLOAD_FIELD_J="
    f"{float(declared_payload_field['conservative_ledger_charge_j']):.12e}"
)

print(
    "DECLARED_MEDIATOR_SOURCE_X_FIELD_J="
    f"{float(declared_x_field['positive_x_field_inventory_j']):.12e}"
)

print(
    "DECLARED_STATIC_PLUS_MEDIATOR_LOWER_BOUND_J="
    f"{declared_total_lower_bound_j:.12e}"
)

print(
    "TREE_SPIN2_COMPANION=False"
)

print(
    "NEGATIVE_MASS_REQUIRED=False"
)

print(
    "RANK_ONE_COMPANION_IDENTITY=C1^2=4_DX_DT"
)

print(
    "ENTIRE_PRACTICAL_WINDOW_GRAPHICALLY_EXCLUDED="
    + str(
        entire_practical_window_graphically_excluded
    )
)

print(
    "SINGLE_SCALAR_UV_TEMPLATE_REJECTED="
    + str(
        single_scalar_template_rejected
    )
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
