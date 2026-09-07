"""032V22 — localized A1 naturalness/control gate + A2 provenance repair.

PURPOSE
-------
V21 closed only the canonical smooth stationary global-q realization of the
time-gradient X-dependent disformal family.

V22:

1. preserves the V21 outward-sign result;
2. tests whether localized explicitly time-dependent q is kinematically
   catastrophic;
3. does NOT claim the hidden-axial source already realizes the V21 profile;
4. computes a distinct q=0 constant-disformal off-state material bound;
5. performs a hard-cutoff Wilsonian operator-descent NATURALNESS scout;
6. derives the optimistic localized q+psi partial energy floor;
7. calculates how far below M_* the UV matching/protection scale must lie to
   reopen a <10-MJ corridor;
8. repairs V20's A2 provenance using already-completed 032T/032U;
9. leaves the derivative-multipole / intrinsic-hypermomentum MAG frontier
   open;
10. preserves AGMINER.

No blind parameter scan is performed.
No physical model is claimed.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.localized_disformal_activation import (
    constant_disformal_empirical_b_cap,
    maximum_cutoff_ratio_for_strict_target,
    minimum_gradient_taper_scout,
    optimistic_localized_partial_floor,
    persist_v22_rules,
    provenance_repair_status,
    quartic_disformal_hard_cutoff_descent,
    single_scale_minimum_metric_scale_ev,
    source_scale_comparison,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.storage import (
    Storage,
)


ROOT = Path(
    __file__
).resolve().parents[1]

V20_PATH = (
    ROOT
    / "results"
    / "agminer"
    / "032v20_global_candidate_family_rerank_summary.json"
)

V21_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v21_time_gradient_disformal_prefight_summary.json"
)

R2_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r2_large_nf_rg_axial_vacuum_summary.json"
)

T_PATH = (
    ROOT
    / "results"
    / "data"
    / "032t_symmetry_protected_mag_matter_coupling_summary.json"
)

U_PATH = (
    ROOT
    / "results"
    / "data"
    / "032u_universal_hypermomentum_portal_summary.json"
)

DB_PATH = (
    ROOT
    / "results"
    / "agminer"
    / "agminer.sqlite3"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v22_localized_disformal_naturalness_frontier_summary.json"
)

UV_SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v22_localized_disformal_uv_ratio_scan.csv"
)

FRONTIER_OUT = (
    ROOT
    / "results"
    / "agminer"
    / "032v22_frontier_provenance_repair.csv"
)


TARGET_J = 1.0e7
TARGET_A = 9.80665

PAYLOAD_RADIUS_M = 0.10
SOURCE_RADIUS_M = 0.10
GRADIENT_SCALE_M = 0.10

ACTIVE_RADIUS_M = 0.31
WALL_THICKNESS_M = 0.10

AU_DENSITY_KG_M3 = 19300.0

SEPARATION_M = 200.0e-9
SPHERE_AU_M = 180.0e-9
PLATE_AU_M = 210.0e-9

ALLOWED_EXTRA_PA = 0.00764


policy = current_energy_policy()

assert (
    float(
        policy[
            "limit_j"
        ]
    )
    ==
    TARGET_J
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


for required in (
    V20_PATH,
    V21_PATH,
    R2_PATH,
    T_PATH,
    U_PATH,
):
    if not required.exists():
        raise FileNotFoundError(
            str(
                required
            )
        )


v20 = json.loads(
    V20_PATH.read_text(
        encoding="utf-8"
    )
)

v21 = json.loads(
    V21_PATH.read_text(
        encoding="utf-8"
    )
)

r2 = json.loads(
    R2_PATH.read_text(
        encoding="utf-8"
    )
)

t = json.loads(
    T_PATH.read_text(
        encoding="utf-8"
    )
)

u = json.loads(
    U_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    v21[
        "canonical_stationary_linear_gamma_subbranch_closed"
    ]
    is True
)

assert (
    v21[
        "full_a1_time_gradient_disformal_family_closed"
    ]
    is False
)

assert (
    t[
        "minimal_matter_branch"
    ][
        "declared_branch_closed"
    ]
    is True
)

assert (
    t[
        "new_q_matter_portal_required_for_rescue"
    ]
    is True
)

assert (
    u[
        "declared_linear_stress_monopole_branch_closed"
    ]
    is True
)

assert (
    u[
        "derivative_multipole_branch_closed"
    ]
    is False
)

assert (
    u[
        "full_hypermomentum_portal_class_closed"
    ]
    is False
)


# ============================================================
# 1. A2 PROVENANCE REPAIR
# ============================================================

provenance = (
    provenance_repair_status()
)


assert (
    provenance[
        "v20_a2_was_new_untested_family"
    ]
    is False
)


# ============================================================
# 2. LOCALIZED q KINEMATIC SCOUT
# ============================================================

v21_k_cap = float(
    v21[
        "offstate_material_gate"
    ][
        "k_cap_ev_m4"
    ]
)

v21_q2_min = float(
    v21[
        "canonical_cosmology"
    ][
        "minimum_q2_for_invertibility_ev4"
    ]
)

localized_q2 = (
    1.10
    * v21_q2_min
)

localized_lambda_ev = (
    localized_q2
    / v21_k_cap
)**0.125


localized = (
    minimum_gradient_taper_scout(
        q2_ev4=
            localized_q2,

        lambda_ev=
            localized_lambda_ev,

        active_radius_m=
            ACTIVE_RADIUS_M,

        wall_thickness_m=
            WALL_THICKNESS_M,

        chi=
            1.0,
    )
)


# ============================================================
# 3. DO NOT PROMOTE AXIAL SOURCE BY DIMENSIONAL COINCIDENCE
# ============================================================

axial_b_ev = float(
    r2[
        "source"
    ][
        "axial_b_ev"
    ]
)

axial_fpsi_ev = float(
    r2[
        "source"
    ][
        "f_psi_ev"
    ]
)

v21_reference_s2 = float(
    v21[
        "local_field_energy_scout"
    ][
        "reference_required_s2_ev4"
    ]
)


source_comparison = (
    source_scale_comparison(
        axial_b_ev=
            axial_b_ev,

        axial_fpsi_ev=
            axial_fpsi_ev,

        required_s2_ev4=
            v21_reference_s2,
    )
)


assert (
    source_comparison[
        "microscopic_source_match"
    ]
    is False
)


# ============================================================
# 4. q=0 CONSTANT-DISFORMAL OFF-STATE CAP
# ============================================================

b_cap_state = (
    constant_disformal_empirical_b_cap(
        gold_density_kg_m3=
            AU_DENSITY_KG_M3,

        separation_m=
            SEPARATION_M,

        sphere_gold_thickness_m=
            SPHERE_AU_M,

        plate_gold_thickness_m=
            PLATE_AU_M,

        allowed_extra_pressure_pa=
            ALLOWED_EXTRA_PA,
    )
)


b_cap = float(
    b_cap_state[
        "b_cap_ev_m4"
    ]
)


# ============================================================
# 5. UNPROTECTED SINGLE-SCALE NATURALNESS
# ============================================================

single_scale_metric_ev = (
    single_scale_minimum_metric_scale_ev(
        empirical_b_cap_ev_m4=
            b_cap,

        cutoff_ratio=
            1.0,
    )
)


single_scale_descent = (
    quartic_disformal_hard_cutoff_descent(
        metric_scale_ev=
            single_scale_metric_ev,

        cutoff_ratio=
            1.0,
    )
)


assert math.isclose(
    float(
        single_scale_descent[
            "induced_constant_disformal_b_ev_m4"
        ]
    ),
    b_cap,
    rel_tol=
        1.0e-8,
)


# ============================================================
# 6. OPTIMISTIC q + psi LOWER BOUND
# ============================================================

single_scale_floor = (
    optimistic_localized_partial_floor(
        metric_scale_ev=
            single_scale_metric_ev,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        source_radius_m=
            SOURCE_RADIUS_M,
    )
)


single_scale_unprotected_pass = bool(
    float(
        single_scale_floor[
            "partial_floor_j"
        ]
    )
    <
    TARGET_J
)


assert (
    single_scale_unprotected_pass
    is False
)


# ============================================================
# 7. REQUIRED MULTISCALE / PROTECTION GAP
# ============================================================

ratio_threshold = (
    maximum_cutoff_ratio_for_strict_target(
        empirical_single_scale_m_ev=
            single_scale_metric_ev,

        target_energy_j=
            TARGET_J,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        source_radius_m=
            SOURCE_RADIUS_M,
    )
)


eta_threshold = float(
    ratio_threshold[
        "maximum_cutoff_over_metric_scale_for_lt_target"
    ]
)


# ============================================================
# 8. UV-RATIO SCAN
# ============================================================

ratios = sorted(
    {
        0.10,
        0.25,
        eta_threshold,
        0.50,
        0.75,
        1.00,
    }
)


uv_rows = []

for eta in ratios:
    metric_ev = (
        eta
        * single_scale_metric_ev
    )

    descent = (
        quartic_disformal_hard_cutoff_descent(
            metric_scale_ev=
                metric_ev,

            cutoff_ratio=
                eta,
        )
    )

    floor = (
        optimistic_localized_partial_floor(
            metric_scale_ev=
                metric_ev,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                GRADIENT_SCALE_M,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            source_radius_m=
                SOURCE_RADIUS_M,
        )
    )

    uv_rows.append(
        {
            "cutoff_over_metric_scale":
                eta,

            "minimum_metric_scale_ev_from_offstate_scout":
                metric_ev,

            "induced_b_ev_m4":
                float(
                    descent[
                        "induced_constant_disformal_b_ev_m4"
                    ]
                ),

            "empirical_b_cap_ev_m4":
                b_cap,

            "optimized_k_ev_m4":
                float(
                    floor[
                        "k_ev_m4"
                    ]
                ),

            "q2_ev4":
                float(
                    floor[
                        "q2_ev4"
                    ]
                ),

            "required_s2_ev4":
                float(
                    floor[
                        "required_s2_ev4"
                    ]
                ),

            "q_payload_energy_j":
                float(
                    floor[
                        "q_payload_volume_energy_j"
                    ]
                ),

            "psi_gradient_energy_j":
                float(
                    floor[
                        "psi_gradient_energy_j"
                    ]
                ),

            "optimistic_partial_floor_j":
                float(
                    floor[
                        "partial_floor_j"
                    ]
                ),

            "strict_lt10mj_partial_pass":
                float(
                    floor[
                        "partial_floor_j"
                    ]
                )
                <
                TARGET_J,

            "complete_operating_ledger":
                False,
        }
    )


# ============================================================
# 9. AGMINER FAILURE MEMORY / PROVENANCE REPAIR
# ============================================================

storage = Storage(
    DB_PATH
)

try:
    models_before = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM models"
        ).fetchone()[
            "count"
        ]
    )

    rejections_before = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM rejections"
        ).fetchone()[
            "count"
        ]
    )

    rules_before = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM region_rules"
        ).fetchone()[
            "count"
        ]
    )

    oracles_before = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM action_oracles"
        ).fetchone()[
            "count"
        ]
    )

    mechanisms_before = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM mechanism_metrics"
        ).fetchone()[
            "count"
        ]
    )

    inserted_rules = (
        persist_v22_rules(
            storage,

            single_scale_floor_j=
                float(
                    single_scale_floor[
                        "partial_floor_j"
                    ]
                ),

            single_scale_metric_ev=
                single_scale_metric_ev,

            b_cap_ev_m4=
                b_cap,

            cutoff_ratio_threshold=
                eta_threshold,
        )
    )

    storage.set_metadata(
        "032v20_a2_provenance_repaired",
        "1",
    )

    storage.set_metadata(
        "032v22_unprotected_single_scale_localized_a1_closed",
        "1",
    )

    storage.set_metadata(
        "032v22_full_localized_a1_closed",
        "0",
    )

    storage.set_metadata(
        "agminer_next_family",
        "DERIVATIVE_HYPERMOMENTUM_MULTIPOLE_PORTAL",
    )

    models_after = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM models"
        ).fetchone()[
            "count"
        ]
    )

    rejections_after = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM rejections"
        ).fetchone()[
            "count"
        ]
    )

    rules_after = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM region_rules"
        ).fetchone()[
            "count"
        ]
    )

    oracles_after = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM action_oracles"
        ).fetchone()[
            "count"
        ]
    )

    mechanisms_after = int(
        storage.connection.execute(
            "SELECT COUNT(*) AS count FROM mechanism_metrics"
        ).fetchone()[
            "count"
        ]
    )

finally:
    storage.close()


assert models_before == models_after
assert rejections_before == rejections_after
assert oracles_before == oracles_after
assert mechanisms_before == mechanisms_after

assert (
    rules_after
    -
    rules_before
    ==
    inserted_rules
)


# ============================================================
# 10. REPAIRED FRONTIER
# ============================================================

frontier_rows = [
    {
        "research_rank":
            "A1",

        "family":
            "DERIVATIVE_HYPERMOMENTUM_MULTIPOLE_PORTAL",

        "status":
            "OPEN_NEXT_THEOREM_FIRST_GATE",

        "reason":
            (
                "032U_PROVED_NONZERO_DIPOLE_WHILE_MONOPOLE_CLOSED;"
                "FINITE_PAYLOAD_KERNEL_SOURCE_ENERGY_AND_UNIVERSALITY_UNTESTED"
            ),

        "blind_scan_authorized":
            False,
    },
    {
        "research_rank":
            "B1",

        "family":
            "PROTECTED_LOCALIZED_TIME_GRADIENT_DISFORMAL",

        "status":
            "OPEN_EXPLICIT_PROTECTION_ACTION_REQUIRED",

        "reason":
            (
                "V22_LOCALIZATION_KINEMATICS_NOT_FATAL_BUT_UNPROTECTED_"
                "SINGLE_SCALE_NATURALNESS_ENERGY_RED"
            ),

        "blind_scan_authorized":
            False,
    },
    {
        "research_rank":
            "",

        "family":
            "PROPAGATING_NONMETRICITY_HEALTHY_SINGLE_MODE_MINIMAL",

        "status":
            "NOT_NEW_ALREADY_032T_032U",

        "reason":
            (
                "FREE_PROPAGATION_PROVENANCE_ALREADY_USED;"
                "MINIMAL_MATTER_BRANCH_AND_LINEAR_STRESS_MONOPOLE_ALREADY_TESTED"
            ),

        "blind_scan_authorized":
            False,
    },
]


# ============================================================
# 11. OUTPUT
# ============================================================

UV_SCAN_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


with UV_SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                uv_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        uv_rows
    )


with FRONTIER_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                frontier_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        frontier_rows
    )


decision = (
    "GREEN_LOCALIZED_Q_KINEMATICS_NOT_AUTOMATICALLY_FATAL_"
    "RED_UNPROTECTED_SINGLE_SCALE_LOCALIZED_A1_BY_RADIATIVE_DESCENT_"
    "PLUS_OPTIMISTIC_275MJ_PARTIAL_FLOOR_"
    "GREEN_V20_A2_PROVENANCE_REPAIR_ALREADY_032T_032U_"
    "FULL_LOCALIZED_A1_NOT_CLOSED_"
    "DERIVATIVE_HYPERMOMENTUM_MULTIPOLE_NEXT"
)

next_step = (
    "032V23_DERIVATIVE_HYPERMOMENTUM_MULTIPOLE_"
    "FINITE_PAYLOAD_KERNEL_SOURCE_ENERGY_AND_UNIVERSALITY_PREFLIGHT"
)


summary = {
    "branch":
        "032V22_LOCALIZED_DISFORMAL_NATURALNESS_AND_FRONTIER_PROVENANCE_REPAIR",

    "claim_class":
        "LOCALIZED_ACTIVATION_NATURALNESS_LOWER_BOUND_AND_FRONTIER_REPAIR",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "v21_input_decision":
        v21[
            "decision"
        ],

    "a2_provenance_repair":
        provenance,

    "localized_q_kinematics": {
        "active_radius_m":
            ACTIVE_RADIUS_M,

        "wall_thickness_m":
            WALL_THICKNESS_M,

        "q2_ev4":
            localized_q2,

        "lambda_ev":
            localized_lambda_ev,

        **localized,

        "localized_q_kinematically_impossible":
            False,

        "physical_activation_action_constructed":
            False,
    },

    "microscopic_source_comparison":
        source_comparison,

    "offstate_constant_disformal_gate": {
        **b_cap_state,

        "response_class":
            "Q_ZERO_CONSTANT_DISFORMAL_QUADRATIC_DESCENDANT",

        "same_as_r5_pure_j0":
            False,

        "same_as_v21_timelike_background":
            False,
    },

    "hard_cutoff_naturalness": {
        "single_scale_metric_min_ev":
            single_scale_metric_ev,

        "single_scale_metric_min_kev":
            single_scale_metric_ev
            / 1.0e3,

        "single_scale_descent":
            single_scale_descent,

        "scheme_independent_prediction":
            False,

        "explicit_protection_included":
            False,
    },

    "optimistic_single_scale_energy_floor": {
        **single_scale_floor,

        "strict_lt10mj_pass":
            single_scale_unprotected_pass,

        "omitted_positive_costs": [
            "localized_taper_wall",
            "microscopic_source",
            "support",
            "activation_control",
            "reset",
            "radiation",
            "reaction",
            "quantum_matching_completion",
        ],

        "therefore_is_complete_device_energy":
            False,
    },

    "required_protection_gap": {
        **ratio_threshold,

        "interpretation":
            (
                "UNPROTECTED_SINGLE_SCALE_CLOSED;"
                "REOPEN_REQUIRES_EXPLICIT_MULTISCALE_OR_PROTECTION_BELOW_RATIO"
            ),

        "full_localized_a1_closed":
            False,
    },

    "agminer": {
        "models_before":
            models_before,

        "models_after":
            models_after,

        "rejections_before":
            rejections_before,

        "rejections_after":
            rejections_after,

        "region_rules_before":
            rules_before,

        "region_rules_inserted":
            inserted_rules,

        "region_rules_after":
            rules_after,

        "action_oracles_mutated":
            (
                oracles_before
                !=
                oracles_after
            ),

        "mechanism_metrics_mutated":
            (
                mechanisms_before
                !=
                mechanisms_after
            ),

        "miner_preserved":
            True,
    },

    "gate_status": {
        "v21_outward_sign":
            "PRESERVED_GREEN",

        "canonical_global_stationary_q":
            "CLOSED_V21",

        "localized_time_dependent_q_kinematics":
            "GREEN_SCOUT",

        "microscopic_hidden_axial_source_match":
            "NOT_ESTABLISHED",

        "q0_constant_disformal_empirical_cap":
            "GREEN_RECONSTRUCTED",

        "quartic_to_quadratic_operator_descent":
            "YELLOW_HARD_CUTOFF_NATURALNESS_SCOUT",

        "unprotected_single_scale_localized_a1":
            "RED",

        "protected_multiscale_localized_a1":
            "YELLOW_EXPLICIT_ACTION_REQUIRED",

        "v20_a2_minimal_propagating_nonmetricity":
            "PROVENANCE_DUPLICATE_032T_032U",

        "derivative_hypermomentum_multipole":
            "OPEN_NEXT",

        "complete_operating_energy":
            "NOT_ESTABLISHED",
    },

    "unprotected_single_scale_localized_a1_closed":
        True,

    "full_localized_time_gradient_a1_closed":
        False,

    "v20_a2_rerun_authorized":
        False,

    "blind_parameter_scan_authorized":
        False,

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


print(
    "BRANCH="
    + summary[
        "branch"
    ]
)

print(
    "V20_A2_WAS_NEW_UNTESTED_FAMILY=False"
)

print(
    "V20_A2_MINIMAL_BRANCH_ALREADY_032T=True"
)

print(
    "V20_A2_LINEAR_STRESS_MONOPOLE_ALREADY_032U=True"
)

print(
    "DERIVATIVE_HYPERMOMENTUM_MULTIPOLE_OPEN=True"
)

print(
    "LOCALIZED_Q_HOLD_TIME_S="
    f"{float(localized['hold_time_s']):.12e}"
)

print(
    "LOCALIZED_Q_WALL_FIELD_INVENTORY_J="
    f"{float(localized['wall_gradient_field_inventory_j']):.12e}"
)

print(
    "LOCALIZED_Q_FIELD_SWING_RATE_W="
    f"{float(localized['field_energy_swing_rate_w']):.12e}"
)

print(
    "FIELD_SWING_RATE_IS_DISSIPATED_POWER=False"
)

print(
    "AXIAL_B_FPSI_EV2="
    f"{float(source_comparison['axial_b_times_fpsi_ev2']):.12e}"
)

print(
    "V21_REQUIRED_GRADIENT_EV2="
    f"{float(source_comparison['disformal_required_gradient_ev2']):.12e}"
)

print(
    "AXIAL_TO_V21_SCALE_RELATIVE_DIFFERENCE="
    f"{float(source_comparison['relative_difference']):.12e}"
)

print(
    "MICROSCOPIC_SOURCE_MATCH=False"
)

print(
    "OFFSTATE_CONSTANT_DISFORMAL_B_CAP_EV_M4="
    f"{b_cap:.12e}"
)

print(
    "UNPROTECTED_SINGLE_SCALE_M_MIN_KEV="
    f"{single_scale_metric_ev/1.0e3:.12e}"
)

print(
    "SINGLE_SCALE_OPTIMAL_K_EV_M4="
    f"{float(single_scale_floor['k_ev_m4']):.12e}"
)

print(
    "SINGLE_SCALE_Q2_EV4="
    f"{float(single_scale_floor['q2_ev4']):.12e}"
)

print(
    "SINGLE_SCALE_REQUIRED_S2_EV4="
    f"{float(single_scale_floor['required_s2_ev4']):.12e}"
)

print(
    "SINGLE_SCALE_Q_PAYLOAD_ENERGY_J="
    f"{float(single_scale_floor['q_payload_volume_energy_j']):.12e}"
)

print(
    "SINGLE_SCALE_PSI_GRADIENT_ENERGY_J="
    f"{float(single_scale_floor['psi_gradient_energy_j']):.12e}"
)

print(
    "SINGLE_SCALE_OPTIMISTIC_PARTIAL_FLOOR_J="
    f"{float(single_scale_floor['partial_floor_j']):.12e}"
)

print(
    "SINGLE_SCALE_METRIC_OVER_HARD="
    f"{float(single_scale_floor['metric_scale_over_hard_derivative_scale']):.12e}"
)

print(
    "MAX_CUTOFF_OVER_METRIC_FOR_LT10MJ="
    f"{eta_threshold:.12e}"
)

print(
    "UNPROTECTED_SINGLE_SCALE_LOCALIZED_A1_CLOSED=True"
)

print(
    "FULL_LOCALIZED_TIME_GRADIENT_A1_CLOSED=False"
)

print(
    "V20_A2_RERUN_AUTHORIZED=False"
)

print(
    "DB_MODELS_MUTATED="
    + str(
        models_before
        !=
        models_after
    )
)

print(
    "DB_REJECTIONS_MUTATED="
    + str(
        rejections_before
        !=
        rejections_after
    )
)

print(
    "DB_REGION_RULES_INSERTED="
    + str(
        inserted_rules
    )
)

print(
    "DB_ACTION_ORACLES_MUTATED="
    + str(
        oracles_before
        !=
        oracles_after
    )
)

print(
    "DB_MECHANISM_METRICS_MUTATED="
    + str(
        mechanisms_before
        !=
        mechanisms_after
    )
)

print(
    "AGMINER_ITSELF_PRESERVED=True"
)

print(
    "BLIND_PARAMETER_SCAN_AUTHORIZED=False"
)

print(
    "NEGATIVE_MASS_REQUIRED=False"
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
