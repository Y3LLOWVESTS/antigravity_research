"""032V19R6 — companion positivity and exact empirical/energy overlap gate.

PURPOSE
-------
R5 falsified the current pure-j=0 coefficient through a low-energy,
off-state two-scalar Casimir force.

R6 now determines:

1. whether the healthy matter j=2 companion can cancel that force;
2. the maximum empirically allowed static C_s;
3. the corresponding minimum metric scale M;
4. the EXACT V17 finite-payload partial energy at that scale;
5. the exact V17 metric-scale ceiling imposed by the strict <10-MJ partial
   objective.

The result decides whether the known V17 energy-leading oblate source retains
any overlap between empirical viability and the strict partial-energy target.

No generic source optimization is performed.

No AGMINER database mutation is performed in this gate.  If the overlap is
empty, the result should be carried into AGMINER failure memory during the
subsequent model-family rerank rather than prematurely creating another action
oracle.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from scipy.optimize import brentq

from antigravity_research.agminer.axial_dirac_meanfield import (
    payload_trace_load,
)
from antigravity_research.agminer.c1_payload_matching import (
    c1_from_metric_scale_ev,
    corrected_laue_trace_support_floor_j,
    payload_surface_acceleration_metrics,
    required_q2_for_payload_surface,
    spheroid_incident_legendre_coefficients,
)
from antigravity_research.agminer.companion_operator_empirical import (
    finite_gold_film_static_c_cap,
    material_j0_j2_kinetic_factors,
    normalized_finite_slab_reflection,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.two_scalar_quantum_force import (
    matter_loading_from_c1,
)


ROOT = Path(
    __file__
).resolve().parents[1]

V15_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v15_axial_shift_source_morphology_summary.json"
)

V16_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v16_axial_dirac_meanfield_self_consistency_summary.json"
)

V17_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v17_c1_payload_quantum_control_summary.json"
)

R5_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r5_two_scalar_casimir_empirical_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r6_companion_positivity_empirical_energy_summary.json"
)

REFLECTION_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r6_j2_reflection_scan.csv"
)

OVERLAP_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r6_v17_empirical_energy_overlap_scan.csv"
)


TARGET_J = 1.0e7
G = 9.80665

REFERENCE_SCALE_EV = 1.0e5

PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10
PAYLOAD_CENTER_Z_M = 0.20

AU_DENSITY_KG_M3 = 19300.0

CASIMIR_SEPARATION_M = 200.0e-9
SPHERE_AU_M = 180.0e-9
PLATE_AU_M = 210.0e-9

MEASURED_PRESSURE_PA = 0.51050
STANDARD_THEORY_PRESSURE_PA = 0.51126
CONFIDENCE_95_HALFWIDTH_PA = 0.00840


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


v15 = json.loads(
    V15_PATH.read_text(
        encoding="utf-8"
    )
)

v16 = json.loads(
    V16_PATH.read_text(
        encoding="utf-8"
    )
)

v17 = json.loads(
    V17_PATH.read_text(
        encoding="utf-8"
    )
)

r5 = json.loads(
    R5_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    r5[
        "current_pure_j0_operator_empirically_viable"
    ]
    is False
)

assert (
    r5[
        "kinetic_conformal_class_closed"
    ]
    is False
)


current_c = float(
    r5[
        "target"
    ][
        "c1_ev_m4"
    ]
)


# ============================================================
# 1. POSITIVITY-COMPATIBLE j=2 CANCELLATION THEOREM SCOUT
# ============================================================

gold_rho_ev4 = float(
    matter_loading_from_c1(
        c1_ev_m4=
            current_c,

        density_kg_m3=
            AU_DENSITY_KG_M3,
    )[
        "rho_ev4"
    ]
)


reflection_rows = []

for c2_ratio in (
    -0.50,
    -0.25,
    0.0,
    0.25,
    1.0,
    4.0,
    12.0,
):
    c2 = (
        c2_ratio
        * current_c
    )

    factors = (
        material_j0_j2_kinetic_factors(
            rho_ev4=
                gold_rho_ev4,

            static_spatial_c_ev_m4=
                current_c,

            j2_c_ev_m4=
                c2,
        )
    )

    for u in (
        0.0,
        0.25,
        0.50,
        0.75,
        1.0,
    ):
        if (
            factors[
                "z_t"
            ]
            <=
            0.0
        ):
            continue

        state = (
            normalized_finite_slab_reflection(
                z_t=
                    float(
                        factors[
                            "z_t"
                        ]
                    ),

                z_s=
                    float(
                        factors[
                            "z_s"
                        ]
                    ),

                xi_over_kappa0=
                    u,

                kappa0_times_thickness=
                    1.0,
            )
        )

        reflection_rows.append(
            {
                "c2_over_static_cs":
                    c2_ratio,

                "xi_over_kappa0":
                    u,

                "jiang_forward_positivity_compatible":
                    bool(
                        factors[
                            "jiang_forward_positivity_compatible"
                        ]
                    ),

                "z_t":
                    float(
                        factors[
                            "z_t"
                        ]
                    ),

                "z_s":
                    float(
                        factors[
                            "z_s"
                        ]
                    ),

                "interface_reflection":
                    float(
                        state[
                            "reflection"
                        ]
                    ),

                "pure_j0_interface_reflection":
                    float(
                        state[
                            "pure_j0_reflection_at_same_static_cs"
                        ]
                    ),

                "finite_slab_reflection":
                    float(
                        state[
                            "finite_slab_reflection"
                        ]
                    ),
            }
        )


positive_rows = [
    row
    for row in reflection_rows
    if (
        row[
            "jiang_forward_positivity_compatible"
        ]
        and
        row[
            "c2_over_static_cs"
        ]
        >= 0.0
    )
]


pure_by_u = {
    row[
        "xi_over_kappa0"
    ]:
    row[
        "finite_slab_reflection"
    ]
    for row in reflection_rows
    if (
        row[
            "c2_over_static_cs"
        ]
        ==
        0.0
    )
}


positive_j2_never_reduces_reflection = all(
    float(
        row[
            "finite_slab_reflection"
        ]
    )
    >=
    float(
        pure_by_u[
            row[
                "xi_over_kappa0"
            ]
        ]
    )
    -
    1.0e-13
    for row in positive_rows
)


assert (
    positive_j2_never_reduces_reflection
)


# ============================================================
# 2. EXACT R5 FINITE-FILM EMPIRICAL STATIC-C_s CAP
# ============================================================

empirical_cap = (
    finite_gold_film_static_c_cap(
        current_c_ev_m4=
            current_c,

        gold_density_kg_m3=
            AU_DENSITY_KG_M3,

        separation_m=
            CASIMIR_SEPARATION_M,

        sphere_gold_thickness_m=
            SPHERE_AU_M,

        plate_gold_thickness_m=
            PLATE_AU_M,

        measured_pressure_pa=
            MEASURED_PRESSURE_PA,

        standard_theory_pressure_pa=
            STANDARD_THEORY_PRESSURE_PA,

        confidence_halfwidth_pa=
            CONFIDENCE_95_HALFWIDTH_PA,
    )
)


empirical_c_cap = float(
    empirical_cap[
        "static_c_cap_ev_m4"
    ]
)

empirical_metric_min_ev = float(
    empirical_cap[
        "metric_scale_min_ev"
    ]
)


assert (
    empirical_metric_min_ev
    >
    1.0e5
)


# ============================================================
# 3. RECONSTRUCT EXACT V17 OBLATE FINITE-PAYLOAD EVALUATOR
# ============================================================

morph = v15[
    "optimized_morphology"
]

selected = v16[
    "selected_positive_band_partial_corridor"
]

source_a_m = float(
    morph[
        "a_m"
    ]
)

source_c_m = float(
    morph[
        "c_m"
    ]
)

q_reference = float(
    morph[
        "q"
    ]
)


field_reference_j = float(
    selected[
        "field_energy_j"
    ]
)

band_reference_j = float(
    selected[
        "occupied_band_energy_j"
    ]
)

pressure_mean_reference_j = float(
    selected[
        "pressure_mean_inventory_j"
    ]
)


corrected_support_reference_j = (
    corrected_laue_trace_support_floor_j(
        fermion_mean_pressure_inventory_j=
            pressure_mean_reference_j,

        scalar_field_energy_j=
            field_reference_j,
    )
)


corrected_vacuum_partial_reference_j = (
    band_reference_j
    +
    field_reference_j
    +
    corrected_support_reference_j
)


assert math.isclose(
    corrected_vacuum_partial_reference_j,
    float(
        v17[
            "v16_ledger_repair"
        ][
            "corrected_vacuum_partial_reference_j"
        ]
    ),
    rel_tol=
        2.0e-13,
)


coefficients = (
    spheroid_incident_legendre_coefficients(
        a_m=
            source_a_m,

        c_m=
            source_c_m,

        payload_center_z_m=
            PAYLOAD_CENTER_Z_M,

        fit_radius_m=
            PAYLOAD_RADIUS_M,

        lmax=
            20,

        n_t=
            56,

        n_phi=
            84,

        fit_order=
            180,
    )
)


def exact_v17_partial(
    metric_scale_ev: float,
    *,
    surface_count: int,
):
    scale = float(
        metric_scale_ev
    )

    trace = (
        payload_trace_load(
            payload_mass_kg=
                PAYLOAD_MASS_KG,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            metric_scale_ev=
                scale,
        )
    )

    epsilon = float(
        trace[
            "epsilon_trace_load"
        ]
    )

    requirement = (
        required_q2_for_payload_surface(
            coefficients=
                coefficients,

            epsilon_trace_load=
                epsilon,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            target_acceleration_m_s2=
                G,

            surface_count=
                surface_count,
        )
    )

    q2_required = float(
        requirement[
            "q2"
        ]
    )

    q2_factor = (
        q2_required
        / q_reference**2
    )

    partial_energy = (
        corrected_vacuum_partial_reference_j
        * (
            scale
            / REFERENCE_SCALE_EV
        )**4
        * q2_factor
    )

    return {
        "metric_scale_ev":
            scale,

        "c1_ev_m4":
            c1_from_metric_scale_ev(
                scale
            ),

        "epsilon_trace_load":
            epsilon,

        "q2_required":
            q2_required,

        "q2_factor_from_vacuum_source":
            q2_factor,

        "partial_energy_j":
            partial_energy,

        "limiting_surface_cosine":
            float(
                requirement[
                    "limiting_surface_cosine"
                ]
            ),
    }


# Validate exact reconstruction at the historical 100-keV point.

v17_at_100 = (
    exact_v17_partial(
        1.0e5,
        surface_count=
            1601,
    )
)


assert math.isclose(
    float(
        v17_at_100[
            "partial_energy_j"
        ]
    ),
    4386155.960285911,
    rel_tol=
        5.0e-10,
)


# ============================================================
# 4. V17 EXACT PARTIAL ENERGY AT EMPIRICAL C_s CAP
# ============================================================

v17_at_empirical_cap = (
    exact_v17_partial(
        empirical_metric_min_ev,
        surface_count=
            1601,
    )
)


surface_at_empirical = (
    payload_surface_acceleration_metrics(
        coefficients=
            coefficients,

        epsilon_trace_load=
            float(
                v17_at_empirical_cap[
                    "epsilon_trace_load"
                ]
            ),

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        q2=
            float(
                v17_at_empirical_cap[
                    "q2_required"
                ]
            ),

        surface_count=
            1601,
    )
)


assert (
    float(
        surface_at_empirical[
            "surface_min_m_s2"
        ]
    )
    >=
    G
    * (
        1.0
        -
        2.0e-12
    )
)


# ============================================================
# 5. EXACT V17 STRICT-10-MJ METRIC-SCALE CEILING
# ============================================================

coarse_energy_metric_max = (
    brentq(
        lambda scale:
            float(
                exact_v17_partial(
                    scale,
                    surface_count=
                        601,
                )[
                    "partial_energy_j"
                ]
            )
            -
            TARGET_J,

        1.0e5,
        1.5e5,
        xtol=
            1.0e-3,
        rtol=
            1.0e-12,
    )
)


fine_low = (
    coarse_energy_metric_max
    * 0.998
)

fine_high = (
    coarse_energy_metric_max
    * 1.002
)


v17_energy_metric_max_ev = (
    brentq(
        lambda scale:
            float(
                exact_v17_partial(
                    scale,
                    surface_count=
                        1601,
                )[
                    "partial_energy_j"
                ]
            )
            -
            TARGET_J,

        fine_low,
        fine_high,
        xtol=
            1.0e-4,
        rtol=
            1.0e-12,
    )
)


v17_at_energy_ceiling = (
    exact_v17_partial(
        v17_energy_metric_max_ev,
        surface_count=
            1601,
    )
)


v17_energy_boundary_c = float(
    v17_at_energy_ceiling[
        "c1_ev_m4"
    ]
)


# Strict energy requires

#     M < M_energy_max

# while the empirical Casimir bound requires

#     M >= M_empirical_min.

# Equality to 10 MJ does not pass.

empirical_energy_overlap_exists = bool(
    empirical_metric_min_ev
    <
    v17_energy_metric_max_ev
)


metric_gap_ev = (
    empirical_metric_min_ev
    -
    v17_energy_metric_max_ev
)


metric_gap_fraction = (
    metric_gap_ev
    /
    v17_energy_metric_max_ev
)


# ============================================================
# 6. SCALE SCAN AROUND THE NEAR-MISS
# ============================================================

scan_scales = sorted(
    {
        1.0e5,
        1.10e5,
        1.20e5,
        v17_energy_metric_max_ev,
        empirical_metric_min_ev,
        1.25e5,
        1.30e5,
    }
)


overlap_rows = []

for scale in scan_scales:
    state = (
        exact_v17_partial(
            scale,
            surface_count=
                1201,
        )
    )

    overlap_rows.append(
        {
            **state,

            "passes_strict_partial_energy":
                float(
                    state[
                        "partial_energy_j"
                    ]
                )
                <
                TARGET_J,

            "passes_r5_empirical_c_cap":
                float(
                    state[
                        "c1_ev_m4"
                    ]
                )
                <=
                empirical_c_cap,

            "simultaneous_empirical_and_partial_energy_pass":
                (
                    float(
                        state[
                            "partial_energy_j"
                        ]
                    )
                    <
                    TARGET_J

                    and

                    float(
                        state[
                            "c1_ev_m4"
                        ]
                    )
                    <=
                    empirical_c_cap
                ),

            "complete_operating_energy":
                False,

            "physical_anisotropic_support_constructed":
                False,
        }
    )


# ============================================================
# 7. CLASSIFICATION
# ============================================================

matter_j2_cancellation_closed = bool(
    positive_j2_never_reduces_reflection
)


known_v17_empirical_energy_corridor = bool(
    empirical_energy_overlap_exists
)


if (
    matter_j2_cancellation_closed
    and
    not known_v17_empirical_energy_corridor
):
    current_032_implementation_closed = True

    decision = (
        "RED_CURRENT_032_KINETIC_CONFORMAL_AXIAL_IMPLEMENTATION_"
        "PURE_J0_CASIMIR_RED_"
        "POSITIVITY_COMPATIBLE_MATTER_J2_CANCELLATION_CLOSED_"
        "V17_EXACT_EMPIRICAL_ENERGY_CORRIDOR_EMPTY_"
        "AGMINER_MODEL_FAMILY_RERANK_AUTHORIZED"
    )

    next_step = (
        "032V20_AGMINER_GLOBAL_CANDIDATE_FAMILY_RERANK_"
        "WITH_V19R3_R4_R5_R6_FAILURE_MEMORY"
    )

else:
    current_032_implementation_closed = False

    decision = (
        "YELLOW_CURRENT_032_KINETIC_CONFORMAL_AXIAL_IMPLEMENTATION_"
        "MATTER_J2_CANCELLATION_CLOSED_"
        "V17_EMPIRICAL_ENERGY_OVERLAP_REMAINS_"
        "PHYSICAL_ANISOTROPIC_SUPPORT_REQUIRED"
    )

    next_step = (
        "032V19R7_PHYSICALLY_MOTIVATED_V17_ANISOTROPIC_SUPPORT_"
        "AT_EMPIRICALLY_ALLOWED_SCALE"
    )


summary = {
    "branch":
        "032V19R6_COMPANION_OPERATOR_POSITIVITY_AND_EMPIRICAL_SCALE_GATE",

    "claim_class":
        "LOW_ENERGY_COMPANION_NO_GO_AND_EXACT_EMPIRICAL_ENERGY_OVERLAP",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "r5_input_decision":
        r5[
            "decision"
        ],

    "companion_operator": {
        "basis":
            "J0_PLUS_TRACELESS_MATTER_J2",

        "static_coefficient":
            "C_S_EQUALS_C0_MINUS_C2_OVER_4",

        "temporal_coefficient_at_fixed_static_cs":
            "C_T_EQUALS_C_S_PLUS_C2",

        "jiang_forward_positivity":
            "C2_GE_0",

        "positive_j2_never_reduces_pointwise_reflection":
            positive_j2_never_reduces_reflection,

        "positive_j2_finite_slab_cancellation":
            False,

        "reflection_reduction_requires_negative_c2":
            True,

        "negative_c2_forward_positivity_compatible":
            False,

        "scope":
            "UNIVERSAL_DIM8_MATTER_J2_SECTOR_ONLY",
    },

    "r5_empirical_static_coefficient_cap": {
        **empirical_cap,

        "current_c_ev_m4":
            current_c,

        "empirical_metric_min_kev":
            empirical_metric_min_ev
            / 1.0e3,
    },

    "v17_exact_reconstruction": {
        "historical_100kev_partial_j":
            float(
                v17_at_100[
                    "partial_energy_j"
                ]
            ),

        "historical_100kev_q2_factor":
            float(
                v17_at_100[
                    "q2_factor_from_vacuum_source"
                ]
            ),

        "empirical_boundary":
            {
                **v17_at_empirical_cap,

                "surface_min_m_s2":
                    float(
                        surface_at_empirical[
                            "surface_min_m_s2"
                        ]
                    ),

                "surface_max_m_s2":
                    float(
                        surface_at_empirical[
                            "surface_max_m_s2"
                        ]
                    ),

                "passes_strict_10mj_partial":
                    float(
                        v17_at_empirical_cap[
                            "partial_energy_j"
                        ]
                    )
                    <
                    TARGET_J,
            },

        "strict_energy_boundary": {
            **v17_at_energy_ceiling,

            "metric_scale_max_ev":
                v17_energy_metric_max_ev,

            "metric_scale_max_kev":
                v17_energy_metric_max_ev
                / 1.0e3,

            "c1_at_energy_boundary_ev_m4":
                v17_energy_boundary_c,

            "exactly_10mj_fails_policy":
                True,
        },

        "empirical_min_metric_ev":
            empirical_metric_min_ev,

        "energy_max_metric_ev":
            v17_energy_metric_max_ev,

        "metric_gap_ev":
            metric_gap_ev,

        "metric_gap_fraction":
            metric_gap_fraction,

        "empirical_energy_overlap_exists":
            empirical_energy_overlap_exists,

        "physical_anisotropic_support_constructed":
            False,

        "complete_operating_ledger":
            False,
    },

    "gate_status": {
        "r5_pure_j0_operator":
            "RED_PRESERVED",

        "matter_j2_forward_positivity":
            "GREEN_LITERATURE_BOUND_C2_GE_0",

        "matter_j2_casimir_cancellation":
            (
                "CLOSED"
                if matter_j2_cancellation_closed
                else "OPEN"
            ),

        "empirical_static_coefficient_cap":
            "ESTABLISHED_R5_FINITE_FILM_MODEL",

        "v17_exact_finite_payload_reconstruction":
            "GREEN",

        "v17_strict_partial_energy_at_empirical_cap":
            (
                "GREEN_LT10MJ"
                if
                float(
                    v17_at_empirical_cap[
                        "partial_energy_j"
                    ]
                )
                <
                TARGET_J
                else
                "RED_GE10MJ"
            ),

        "v17_empirical_energy_overlap":
            (
                "GREEN_NONEMPTY"
                if empirical_energy_overlap_exists
                else "RED_EMPTY"
            ),

        "v17_physical_anisotropic_support":
            "OPEN",

        "general_companion_operator_cancellation":
            "NOT_MATHEMATICALLY_CLOSED",

        "nonlinear_material_descreening":
            "NEW_PHYSICS_NOT_TESTED",

        "complete_operating_energy":
            "NOT_ESTABLISHED",
    },

    "current_032_kinetic_conformal_axial_implementation_closed":
        current_032_implementation_closed,

    "all_possible_kinetic_conformal_theories_closed":
        False,

    "agminer_itself_preserved":
        True,

    "agminer_model_family_rerank_authorized":
        bool(
            current_032_implementation_closed
        ),

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


with REFLECTION_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                reflection_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        reflection_rows
    )


with OVERLAP_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                overlap_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        overlap_rows
    )


print(
    "BRANCH="
    + summary[
        "branch"
    ]
)

print(
    "CURRENT_STATIC_C_EV_M4="
    f"{current_c:.12e}"
)

print(
    "EMPIRICAL_STATIC_C_CAP_EV_M4="
    f"{empirical_c_cap:.12e}"
)

print(
    "CURRENT_C_OVER_EMPIRICAL_CAP="
    f"{current_c/empirical_c_cap:.12e}"
)

print(
    "EMPIRICAL_METRIC_MIN_KEV="
    f"{empirical_metric_min_ev/1.0e3:.12e}"
)

print(
    "EMPIRICAL_CAP_GOLD_EPSILON="
    f"{float(empirical_cap['cap_gold_epsilon']):.12e}"
)

print(
    "POSITIVE_J2_NEVER_REDUCES_REFLECTION="
    + str(
        positive_j2_never_reduces_reflection
    )
)

print(
    "J2_REFLECTION_REDUCTION_REQUIRES_C2_LT_0=True"
)

print(
    "JIANG_FORWARD_POSITIVITY_REQUIRES_C2_GE_0=True"
)

print(
    "V17_100KEV_EXACT_PARTIAL_J="
    f"{float(v17_at_100['partial_energy_j']):.12e}"
)

print(
    "V17_EMPIRICAL_BOUNDARY_PARTIAL_J="
    f"{float(v17_at_empirical_cap['partial_energy_j']):.12e}"
)

print(
    "V17_EMPIRICAL_BOUNDARY_Q2_FACTOR="
    f"{float(v17_at_empirical_cap['q2_factor_from_vacuum_source']):.12e}"
)

print(
    "V17_EMPIRICAL_BOUNDARY_SURFACE_MIN="
    f"{float(surface_at_empirical['surface_min_m_s2']):.12e}"
)

print(
    "V17_STRICT_10MJ_METRIC_MAX_KEV="
    f"{v17_energy_metric_max_ev/1.0e3:.12e}"
)

print(
    "EMPIRICAL_MINUS_ENERGY_METRIC_GAP_EV="
    f"{metric_gap_ev:.12e}"
)

print(
    "EMPIRICAL_MINUS_ENERGY_METRIC_GAP_FRACTION="
    f"{metric_gap_fraction:.12e}"
)

print(
    "V17_EMPIRICAL_ENERGY_OVERLAP_EXISTS="
    + str(
        empirical_energy_overlap_exists
    )
)

print(
    "CURRENT_032_KINETIC_CONFORMAL_AXIAL_IMPLEMENTATION_CLOSED="
    + str(
        current_032_implementation_closed
    )
)

print(
    "ALL_POSSIBLE_KINETIC_CONFORMAL_THEORIES_CLOSED=False"
)

print(
    "AGMINER_ITSELF_PRESERVED=True"
)

print(
    "AGMINER_MODEL_FAMILY_RERANK_AUTHORIZED="
    + str(
        current_032_implementation_closed
    )
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
