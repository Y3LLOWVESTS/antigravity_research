"""032V19R5 — universal two-scalar / material Casimir empirical gate.

PURPOSE
-------
R4 left two leading UV-completion families:

1. direct shift-protected Goldstone kinetic metric;
2. Z2-protected loop-generated j=0 matching.

Before promoting either family, test an unavoidable consequence of the
CURRENT pure-j=0 low-energy operator itself.

This run performs:

- independent two-scalar r^-7 coefficient derivation record;
- DBI literature normalization cross-check;
- weak-material pairwise half-space result;
- exact nonperturbative resummation of matter kinetic loading;
- finite Au-film scalar Casimir pressure;
- direct comparison with the 200-nm Decca Casimir data;
- EFT momentum-domain check;
- soft-mass range check.

No source-energy optimization is performed.

A red result blocks promotion of a UV completion that reproduces only the
current pure-j=0 operator.

It does not yet close kinetic-conformal theories containing additional
low-energy companion operators capable of changing the pair-emission /
reflection amplitude.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.two_scalar_quantum_force import (
    DBI_REFERENCE_COEFFICIENT,
    TRACE_PAIR_COEFFICIENT,
    born_halfspace_pressure_pa,
    empirical_pressure_gate,
    integrated_pairwise_pressure_coefficient,
    laboratory_momentum_scout,
    matter_loading_from_c1,
    metric_scale_from_c1_ev,
    scalar_casimir_pressure_pa,
    soft_mass_range_scout,
)


ROOT = Path(
    __file__
).resolve().parents[1]

R4_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r4_uv_completion_atlas_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r5_two_scalar_casimir_empirical_summary.json"
)

SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r5_scalar_casimir_layer_scan.csv"
)


TARGET_J = 1.0e7

AU_DENSITY_KG_M3 = 19300.0

SEPARATION_M = 200.0e-9

SPHERE_AU_M = 180.0e-9
PLATE_AU_M = 210.0e-9

SPHERE_RADIUS_M = 151.3e-6

MEASURED_PRESSURE_PA = 0.51050
STANDARD_THEORY_PRESSURE_PA = 0.51126
CONFIDENCE_95_HALFWIDTH_PA = 0.00840

DEVICE_RANGE_REFERENCE_M = 0.20


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


r4 = json.loads(
    R4_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    r4[
        "kinetic_conformal_class_closed"
    ]
    is False
)


target = r4[
    "target"
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

metric_scale_ev = (
    metric_scale_from_c1_ev(
        c1
    )
)


# ============================================================
# 1. ANALYTIC NORMALIZATION
# ============================================================

pair_coefficient = (
    TRACE_PAIR_COEFFICIENT
)

dbi_coefficient = (
    DBI_REFERENCE_COEFFICIENT
)

coefficient_ratio = (
    pair_coefficient
    / dbi_coefficient
)

halfspace_born_coefficient = (
    integrated_pairwise_pressure_coefficient()
)


assert math.isclose(
    coefficient_ratio,
    80.0,
    rel_tol=2.0e-15,
)

assert math.isclose(
    halfspace_born_coefficient,
    3.0
    / (
        16.0
        * math.pi**2
    ),
    rel_tol=2.0e-15,
)


# ============================================================
# 2. GOLD MATTER LOADING
# ============================================================

gold_loading = (
    matter_loading_from_c1(
        c1_ev_m4=
            c1,

        density_kg_m3=
            AU_DENSITY_KG_M3,
    )
)


assert (
    float(
        gold_loading[
            "epsilon"
        ]
    )
    >
    100.0
)

assert (
    gold_loading[
        "born_material_limit"
    ]
    is False
)


# ============================================================
# 3. WEAK-BORN RESULT — RECORDED BUT NOT USED FOR EXCLUSION
# ============================================================

gold_born_pressure_pa = (
    born_halfspace_pressure_pa(
        c1_ev_m4=
            c1,

        density1_kg_m3=
            AU_DENSITY_KG_M3,

        density2_kg_m3=
            AU_DENSITY_KG_M3,

        separation_m=
            SEPARATION_M,
    )
)


# ============================================================
# 4. EXACT NONPERTURBATIVE MATERIAL RESUMMATION
# ============================================================

halfspace = (
    scalar_casimir_pressure_pa(
        c1_ev_m4=
            c1,

        density1_kg_m3=
            AU_DENSITY_KG_M3,

        density2_kg_m3=
            AU_DENSITY_KG_M3,

        separation_m=
            SEPARATION_M,
    )
)


actual_films = (
    scalar_casimir_pressure_pa(
        c1_ev_m4=
            c1,

        density1_kg_m3=
            AU_DENSITY_KG_M3,

        density2_kg_m3=
            AU_DENSITY_KG_M3,

        separation_m=
            SEPARATION_M,

        thickness1_m=
            SPHERE_AU_M,

        thickness2_m=
            PLATE_AU_M,
    )
)


one_nm_films = (
    scalar_casimir_pressure_pa(
        c1_ev_m4=
            c1,

        density1_kg_m3=
            AU_DENSITY_KG_M3,

        density2_kg_m3=
            AU_DENSITY_KG_M3,

        separation_m=
            SEPARATION_M,

        thickness1_m=
            1.0e-9,

        thickness2_m=
            1.0e-9,
    )
)


# ============================================================
# 5. EMPIRICAL GATE
# ============================================================

empirical = (
    empirical_pressure_gate(
        extra_pressure_pa=
            float(
                actual_films[
                    "pressure_magnitude_pa"
                ]
            ),

        measured_pressure_pa=
            MEASURED_PRESSURE_PA,

        standard_theory_pressure_pa=
            STANDARD_THEORY_PRESSURE_PA,

        confidence_halfwidth_pa=
            CONFIDENCE_95_HALFWIDTH_PA,
    )
)


one_nm_over_residual = (
    float(
        one_nm_films[
            "pressure_magnitude_pa"
        ]
    )
    / CONFIDENCE_95_HALFWIDTH_PA
)


assert (
    empirical[
        "excluded_at_declared_95pct_interval"
    ]
)

assert (
    float(
        empirical[
            "mismatch_over_95pct_halfwidth"
        ]
    )
    >
    47.0
)

assert (
    one_nm_over_residual
    >
    13.0
)


# ============================================================
# 6. LOW-ENERGY VALIDITY
# ============================================================

momentum = (
    laboratory_momentum_scout(
        separation_m=
            SEPARATION_M,

        source_hard_scale_ev=
            hard_scale_ev,

        metric_scale_ev=
            metric_scale_ev,
    )
)


soft_mass = (
    soft_mass_range_scout(
        required_range_m=
            DEVICE_RANGE_REFERENCE_M,

        laboratory_separation_m=
            SEPARATION_M,
    )
)


pfa_ratio = (
    SEPARATION_M
    / SPHERE_RADIUS_M
)


assert (
    momentum[
        "below_source_hard_scale"
    ]
)

assert (
    momentum[
        "below_metric_scale"
    ]
)

assert (
    soft_mass[
        "massless_laboratory_limit"
    ]
)

assert (
    pfa_ratio
    <
    0.0014
)


# ============================================================
# 7. FILM-THICKNESS STRESS TEST
# ============================================================

layer_rows = []

for thickness_nm in (
    1.0,
    5.0,
    10.0,
    25.0,
    50.0,
    100.0,
    180.0,
    210.0,
):
    thickness_m = (
        thickness_nm
        * 1.0e-9
    )

    state = (
        scalar_casimir_pressure_pa(
            c1_ev_m4=
                c1,

            density1_kg_m3=
                AU_DENSITY_KG_M3,

            density2_kg_m3=
                AU_DENSITY_KG_M3,

            separation_m=
                SEPARATION_M,

            thickness1_m=
                thickness_m,

            thickness2_m=
                thickness_m,
        )
    )

    pressure = float(
        state[
            "pressure_magnitude_pa"
        ]
    )

    layer_rows.append(
        {
            "layer1_nm":
                thickness_nm,

            "layer2_nm":
                thickness_nm,

            "scalar_pressure_pa":
                pressure,

            "pressure_over_measured":
                pressure
                / MEASURED_PRESSURE_PA,

            "pressure_over_95pct_halfwidth":
                pressure
                / CONFIDENCE_95_HALFWIDTH_PA,

            "substrates_included":
                False,
        }
    )


layer_rows.append(
    {
        "layer1_nm":
            180.0,

        "layer2_nm":
            210.0,

        "scalar_pressure_pa":
            float(
                actual_films[
                    "pressure_magnitude_pa"
                ]
            ),

        "pressure_over_measured":
            float(
                actual_films[
                    "pressure_magnitude_pa"
                ]
            )
            / MEASURED_PRESSURE_PA,

        "pressure_over_95pct_halfwidth":
            float(
                actual_films[
                    "pressure_magnitude_pa"
                ]
            )
            / CONFIDENCE_95_HALFWIDTH_PA,

        "substrates_included":
            False,
    }
)


# ============================================================
# 8. CLASSIFICATION
# ============================================================

current_pure_j0_operator_empirically_viable = False

goldstone_pure_j0_promotion_authorized = False
z2_loop_pure_j0_promotion_authorized = False

kinetic_conformal_class_closed = False


decision = (
    "RED_CURRENT_PURE_J0_KINETIC_CONFORMAL_OPERATOR_"
    "BY_OFFSTATE_TWO_SCALAR_CASIMIR_FORCE_"
    "GREEN_DBI_NORMALIZATION_CROSSCHECK_"
    "GREEN_NONPERTURBATIVE_MATTER_LOADING_RESUMMATION_"
    "RED_DECCA_200NM_BY_GT47X_95PCT_RESIDUAL_"
    "COMPANION_OPERATOR_CANCELLATION_OPEN_"
    "KINETIC_CONFORMAL_CLASS_NOT_YET_CLOSED"
)

next_step = (
    "032V19R6_COMPANION_OPERATOR_TWO_SCALAR_"
    "SPECTRAL_POSITIVITY_AND_CANCELLATION_NO_GO_GATE"
)


summary = {
    "branch":
        "032V19R5_UNIVERSAL_TWO_SCALAR_QUANTUM_FORCE_AND_MATERIAL_CASIMIR_EMPIRICAL_GATE",

    "claim_class":
        "LOW_ENERGY_OPERATOR_LEVEL_QUANTUM_EMPIRICAL_FALSIFICATION",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "r4_input_decision":
        r4[
            "decision"
        ],

    "target": {
        "c1_ev_m4":
            c1,

        "metric_scale_ev":
            metric_scale_ev,

        "source_hard_scale_ev":
            hard_scale_ev,

        "static_preflight_j":
            static_preflight_j,
    },

    "two_scalar_analytic": {
        "trace_pair_coefficient_15_over_8pi3":
            pair_coefficient,

        "dbi_reference_coefficient_3_over_128pi3":
            dbi_coefficient,

        "coefficient_ratio":
            coefficient_ratio,

        "integrated_halfspace_born_coefficient":
            halfspace_born_coefficient,

        "pair_force_sign":
            "ATTRACTIVE",

        "long_range_nonanalytic_force":
            True,
    },

    "gold_material_loading": {
        **gold_loading,

        "density_kg_m3":
            AU_DENSITY_KG_M3,

        "weak_pairwise_born_pressure_pa":
            gold_born_pressure_pa,

        "weak_pairwise_born_result_used_for_empirical_exclusion":
            False,

        "reason":
            "GOLD_EPSILON_MUCH_GREATER_THAN_ONE_REQUIRES_RESUMMATION",
    },

    "exact_scalar_casimir": {
        "halfspace":
            halfspace,

        "actual_gold_films_only":
            actual_films,

        "ultraconservative_one_nm_each":
            one_nm_films,

        "sphere_gold_thickness_nm":
            180.0,

        "plate_gold_thickness_nm":
            210.0,

        "sapphire_and_polysilicon_scalar_reflection_included":
            False,
    },

    "decca_200nm_empirical_gate": {
        "separation_nm":
            200.0,

        "measured_pressure_pa":
            MEASURED_PRESSURE_PA,

        "standard_theory_pressure_pa":
            STANDARD_THEORY_PRESSURE_PA,

        "confidence_95_halfwidth_pa":
            CONFIDENCE_95_HALFWIDTH_PA,

        **empirical,

        "one_nm_each_pressure_over_95pct_halfwidth":
            one_nm_over_residual,

        "pfa_d_over_r":
            pfa_ratio,
    },

    "low_energy_validity": {
        "momentum":
            momentum,

        "soft_mass_range":
            soft_mass,

        "device_range_reference_m":
            DEVICE_RANGE_REFERENCE_M,

        "high_scale_uv_breakdown_required_for_gate":
            False,
    },

    "gate_status": {
        "r1_supported_1g_classical_state":
            "PRESERVED_MATHEMATICALLY",

        "r1_static_preflight_energy":
            "PRESERVED",

        "two_scalar_force_derivation":
            "GREEN_ANALYTICAL",

        "dbi_normalization_crosscheck":
            "GREEN",

        "weak_born_gold_estimate":
            "INVALID_FOR_EMPIRICAL_USE_BY_STRONG_MATTER_LOADING",

        "exact_material_loading_resummation":
            "GREEN",

        "actual_finite_gold_layer_empirical_gate":
            "RED",

        "one_nm_layer_stress_test":
            "RED",

        "low_energy_domain":
            "GREEN",

        "soft_mass_device_range_escape":
            "CLOSED_FOR_0P2M_RANGE",

        "current_pure_j0_operator":
            "RED_EMPIRICAL",

        "direct_goldstone_pure_j0_promotion":
            "BLOCKED_PENDING_COMPANION_TEST",

        "z2_loop_pure_j0_promotion":
            "BLOCKED_PENDING_COMPANION_TEST",

        "companion_operator_cancellation":
            "OPEN",

        "kinetic_conformal_class":
            "NOT_YET_CLOSED",

        "complete_operating_energy":
            "NOT_ESTABLISHED",
    },

    "current_pure_j0_operator_empirically_viable":
        current_pure_j0_operator_empirically_viable,

    "goldstone_pure_j0_promotion_authorized":
        goldstone_pure_j0_promotion_authorized,

    "z2_loop_pure_j0_promotion_authorized":
        z2_loop_pure_j0_promotion_authorized,

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


with SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                layer_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        layer_rows
    )


print(
    "BRANCH="
    + summary[
        "branch"
    ]
)

print(
    "TRACE_PAIR_COEFFICIENT="
    f"{pair_coefficient:.12e}"
)

print(
    "DBI_REFERENCE_COEFFICIENT="
    f"{dbi_coefficient:.12e}"
)

print(
    "TRACE_TO_DBI_COEFFICIENT_RATIO="
    f"{coefficient_ratio:.12e}"
)

print(
    "METRIC_SCALE_EV="
    f"{metric_scale_ev:.12e}"
)

print(
    "GOLD_EPSILON="
    f"{float(gold_loading['epsilon']):.12e}"
)

print(
    "GOLD_Z="
    f"{float(gold_loading['z_factor']):.12e}"
)

print(
    "GOLD_INTERFACE_REFLECTION="
    f"{float(gold_loading['interface_reflection']):.12e}"
)

print(
    "INVALID_WEAK_BORN_GOLD_PRESSURE_PA="
    f"{gold_born_pressure_pa:.12e}"
)

print(
    "EXACT_HALFSPACE_SCALAR_PRESSURE_PA="
    f"{float(halfspace['pressure_magnitude_pa']):.12e}"
)

print(
    "ACTUAL_GOLD_FILMS_SCALAR_PRESSURE_PA="
    f"{float(actual_films['pressure_magnitude_pa']):.12e}"
)

print(
    "ONE_NM_EACH_SCALAR_PRESSURE_PA="
    f"{float(one_nm_films['pressure_magnitude_pa']):.12e}"
)

print(
    "DECCA_PREDICTED_TOTAL_WITH_SCALAR_PA="
    f"{float(empirical['predicted_total_pressure_pa']):.12e}"
)

print(
    "DECCA_MISMATCH_OVER_95PCT_HALFWIDTH="
    f"{float(empirical['mismatch_over_95pct_halfwidth']):.12e}"
)

print(
    "ONE_NM_OVER_95PCT_HALFWIDTH="
    f"{one_nm_over_residual:.12e}"
)

print(
    "LAB_Q_EV="
    f"{float(momentum['q_ev']):.12e}"
)

print(
    "LAB_Q_OVER_SOURCE_HARD="
    f"{float(momentum['q_over_source_hard']):.12e}"
)

print(
    "MAX_SOFT_MASS_FOR_0P2M_RANGE_EV="
    f"{float(soft_mass['maximum_mass_ev_for_required_range']):.12e}"
)

print(
    "SOFT_MASS_MD_AT_200NM="
    f"{float(soft_mass['m_times_d_over_hbarc']):.12e}"
)

print(
    "PFA_D_OVER_R="
    f"{pfa_ratio:.12e}"
)

print(
    "CURRENT_PURE_J0_OPERATOR_EMPIRICALLY_VIABLE=False"
)

print(
    "GOLDSTONE_PURE_J0_PROMOTION_AUTHORIZED=False"
)

print(
    "Z2_LOOP_PURE_J0_PROMOTION_AUTHORIZED=False"
)

print(
    "COMPANION_OPERATOR_CANCELLATION_OPEN=True"
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
