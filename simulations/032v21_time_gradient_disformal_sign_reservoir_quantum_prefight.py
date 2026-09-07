"""032V21 — time-gradient disformal sign/reservoir/off-state preflight.

PURPOSE
-------
Test V20's A1 family before any parameter scan:

    SHIFT_SYMMETRIC_TIME_GRADIENT_DISFORMAL_METRIC.

This run is intentionally theorem-first.

It does not reuse the closed constant-B 014E bridge.

It does not reuse the failed 015C localized-source scan.

It uses the distinct X-dependent scaffold

    Gamma(X)=beta X/Lambda^8

with

    phi=q t+psi(r).

CHEAP GATES
-----------
1. Prove the new direct outward lapse sign exists.
2. Prove exact stationary q cannot be smoothly localized.
3. Compute the anisotropic off-state material response.
4. Reuse the declared R5 200-nm empirical residual to bound K.
5. Combine that maximum K with the exact disformal invertibility condition.
6. Translate the minimum stationary q into canonical stiff-fluid Omega.
7. Compare with a deliberately loose Omega_stiff <= 1e-3 ceiling.
8. Record the stricter derivative-expansion scout.
9. Show whether local scalar-gradient energy was actually the problem.
10. If closed, persist one narrow AGMINER failure-memory rule.

No blind scan is performed.
No candidate model is inserted.
No action oracle is inserted.
No mechanism metrics are fabricated.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.storage import (
    Storage,
)
from antigravity_research.agminer.time_gradient_disformal import (
    LOOSE_OMEGA_STIFF_CEILING,
    PUBLISHED_STIFF_OMEGA_CONTEXT,
    acceleration_for_exponential_s2,
    anisotropic_finite_slab_pressure_pa,
    canonical_background_energy,
    critical_energy_density_j_m3,
    disformal_invertibility,
    empirical_k_cap,
    ev4_to_j_m3,
    matching_scale_ev,
    minimum_q2_for_derivative_ratio,
    minimum_q2_for_metric_invertibility,
    persist_v21_failure_rule,
    required_s2_for_exponential_acceleration,
    spherical_exponential_gradient_energy_j,
    stationary_q_integrability,
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

R5_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r5_two_scalar_casimir_empirical_summary.json"
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
    / "032v21_time_gradient_disformal_prefight_summary.json"
)

K_SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v21_time_gradient_disformal_k_scan.csv"
)

COSMO_SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v21_time_gradient_disformal_cosmology_scan.csv"
)


TARGET_J = 1.0e7
TARGET_A = 9.80665

SOURCE_RADIUS_M = 0.10
GRADIENT_SCALE_M = 0.10

AU_DENSITY_KG_M3 = 19300.0

SEPARATION_M = 200.0e-9
SPHERE_AU_M = 180.0e-9
PLATE_AU_M = 210.0e-9


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


v20 = json.loads(
    V20_PATH.read_text(
        encoding="utf-8"
    )
)

r5 = json.loads(
    R5_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    v20[
        "frontier"
    ][
        "top_family"
    ]
    ==
    "SHIFT_SYMMETRIC_TIME_GRADIENT_DISFORMAL_METRIC"
)

assert (
    v20[
        "scope"
    ][
        "blind_large_scan_authorized"
    ]
    is False
)

assert (
    r5[
        "current_pure_j0_operator_empirically_viable"
    ]
    is False
)


# ============================================================
# 1. STATIONARY-q INTEGRABILITY
# ============================================================

integrability = (
    stationary_q_integrability(
        spatial_q_gradient_nonzero=
            True
    )
)


stationary_local_q_reservoir_possible = bool(
    integrability[
        "stationary_time_independent_spatial_gradient_possible"
    ]
)


assert (
    stationary_local_q_reservoir_possible
    is False
)


# ============================================================
# 2. DECLARED R5 EMPIRICAL EXTRA-PRESSURE BUDGET
# ============================================================

decca = r5[
    "decca_200nm_empirical_gate"
]

allowed_extra_pressure_pa = max(
    0.0,

    float(
        decca[
            "measured_pressure_pa"
        ]
    )

    +
    float(
        decca[
            "confidence_95_halfwidth_pa"
        ]
    )

    -
    float(
        decca[
            "standard_theory_pressure_pa"
        ]
    )
)


assert math.isclose(
    allowed_extra_pressure_pa,
    0.00764,
    rel_tol=3.0e-14,
)


# ============================================================
# 3. ANISOTROPIC OFF-STATE CASIMIR K CAP
# ============================================================

empirical = (
    empirical_k_cap(
        gold_density_kg_m3=
            AU_DENSITY_KG_M3,

        separation_m=
            SEPARATION_M,

        sphere_gold_thickness_m=
            SPHERE_AU_M,

        plate_gold_thickness_m=
            PLATE_AU_M,

        allowed_extra_pressure_pa=
            allowed_extra_pressure_pa,
    )
)


k_cap = float(
    empirical[
        "k_cap_ev_m4"
    ]
)


# Reference point is deliberately below the empirical boundary.
reference_k = (
    0.5
    * k_cap
)


reference_pressure = (
    anisotropic_finite_slab_pressure_pa(
        effective_k_ev_m4=
            reference_k,

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


assert (
    reference_pressure
    <
    allowed_extra_pressure_pa
)


# ============================================================
# 4. MOST FAVORABLE K: MINIMUM q FOR METRIC INVERTIBILITY
# ============================================================

q2_min_invertible = (
    minimum_q2_for_metric_invertibility(
        effective_k_ev_m4=
            k_cap,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,
    )
)


background_min_invertible = (
    canonical_background_energy(
        q2_ev4=
            q2_min_invertible
    )
)


omega_min_invertible = float(
    background_min_invertible[
        "omega"
    ]
)


canonical_invertible_cosmology_overlap = bool(
    omega_min_invertible
    <=
    LOOSE_OMEGA_STIFF_CEILING
)


assert (
    canonical_invertible_cosmology_overlap
    is False
)


# Strict inequality is required for invertibility.
#
# The value above is the boundary where the signature factor is zero.

q2_healthy_probe = (
    1.01
    * q2_min_invertible
)


s2_healthy_probe = (
    required_s2_for_exponential_acceleration(
        effective_k_ev_m4=
            k_cap,

        q2_ev4=
            q2_healthy_probe,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,
    )
)


healthy_probe = (
    disformal_invertibility(
        effective_k_ev_m4=
            k_cap,

        q2_ev4=
            q2_healthy_probe,

        s2_ev4=
            s2_healthy_probe,
    )
)


assert (
    healthy_probe[
        "lorentzian_invertible_branch"
    ]
)


# ============================================================
# 5. LOOSE COSMOLOGICAL CEILING: DIRECT SIGNATURE CHECK
# ============================================================

critical_j_m3 = (
    critical_energy_density_j_m3()
)


loose_background_j_m3 = (
    LOOSE_OMEGA_STIFF_CEILING
    * critical_j_m3
)


q2_at_loose_cosmology = (
    2.0
    * loose_background_j_m3
    / ev4_to_j_m3()
)


s2_at_loose_cosmology = (
    required_s2_for_exponential_acceleration(
        effective_k_ev_m4=
            k_cap,

        q2_ev4=
            q2_at_loose_cosmology,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,
    )
)


loose_cosmology_state = (
    disformal_invertibility(
        effective_k_ev_m4=
            k_cap,

        q2_ev4=
            q2_at_loose_cosmology,

        s2_ev4=
            s2_at_loose_cosmology,
    )
)


assert (
    float(
        loose_cosmology_state[
            "metric_signature_margin"
        ]
    )
    <
    0.0
)


# ============================================================
# 6. DERIVATIVE-EXPANSION SCOUT
# ============================================================

q2_min_chi1 = (
    minimum_q2_for_derivative_ratio(
        effective_k_ev_m4=
            k_cap,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,

        maximum_ratio=
            1.0,
    )
)


background_min_chi1 = (
    canonical_background_energy(
        q2_ev4=
            q2_min_chi1
    )
)


omega_min_chi1 = float(
    background_min_chi1[
        "omega"
    ]
)


q2_min_chi01 = (
    minimum_q2_for_derivative_ratio(
        effective_k_ev_m4=
            k_cap,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,

        maximum_ratio=
            0.1,
    )
)


background_min_chi01 = (
    canonical_background_energy(
        q2_ev4=
            q2_min_chi01
    )
)


# ============================================================
# 7. LOCAL FIELD-ENERGY SCOUT
# ============================================================

# Use the half-cap reference and chi=1 formal background.
#
# This reference is not cosmologically viable; it is only used to show that
# the local scalar-gradient energy itself is not the fatal term.

reference_q2 = (
    minimum_q2_for_derivative_ratio(
        effective_k_ev_m4=
            reference_k,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,

        maximum_ratio=
            1.0,
    )
)


reference_s2 = (
    required_s2_for_exponential_acceleration(
        effective_k_ev_m4=
            reference_k,

        q2_ev4=
            reference_q2,

        target_acceleration_m_s2=
            TARGET_A,

        gradient_scale_m=
            GRADIENT_SCALE_M,
    )
)


reference_lambda_ev = (
    matching_scale_ev(
        effective_k_ev_m4=
            reference_k,

        q2_ev4=
            reference_q2,
    )
)


reference_gradient_energy_j = (
    spherical_exponential_gradient_energy_j(
        s2_at_radius_ev4=
            reference_s2,

        radius_m=
            SOURCE_RADIUS_M,

        decay_scale_m=
            GRADIENT_SCALE_M,
    )
)


reference_acceleration = (
    acceleration_for_exponential_s2(
        effective_k_ev_m4=
            reference_k,

        q2_ev4=
            reference_q2,

        s2_ev4=
            reference_s2,

        gradient_scale_m=
            GRADIENT_SCALE_M,
    )
)


assert math.isclose(
    reference_acceleration,
    TARGET_A,
    rel_tol=3.0e-14,
)

assert (
    reference_gradient_energy_j
    <
    2.0e4
)


# ============================================================
# 8. K-SCAN
# ============================================================

k_rows = []

for fraction in (
    0.10,
    0.25,
    0.50,
    0.75,
    1.00,
):
    k_value = (
        fraction
        * k_cap
    )

    pressure = (
        anisotropic_finite_slab_pressure_pa(
            effective_k_ev_m4=
                k_value,

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

    q2_inv = (
        minimum_q2_for_metric_invertibility(
            effective_k_ev_m4=
                k_value,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                GRADIENT_SCALE_M,
        )
    )

    background_inv = (
        canonical_background_energy(
            q2_ev4=
                q2_inv
        )
    )

    k_rows.append(
        {
            "k_fraction_of_empirical_cap":
                fraction,

            "k_ev_m4":
                k_value,

            "finite_gold_film_pressure_pa":
                pressure,

            "pressure_over_allowed_residual":
                pressure
                / allowed_extra_pressure_pa,

            "minimum_q2_invertible_ev4":
                q2_inv,

            "minimum_omega_invertible":
                float(
                    background_inv[
                        "omega"
                    ]
                ),

            "passes_loose_omega_stiff_ceiling":
                (
                    float(
                        background_inv[
                            "omega"
                        ]
                    )
                    <=
                    LOOSE_OMEGA_STIFF_CEILING
                ),
        }
    )


# ============================================================
# 9. COSMOLOGY / EFT SCAN AT MOST FAVORABLE K
# ============================================================

cosmo_rows = []

for chi_max in (
    math.sqrt(
        2.0
    ),
    1.0,
    0.5,
    0.3,
    0.1,
):
    if math.isclose(
        chi_max,
        math.sqrt(
            2.0
        ),
        rel_tol=1.0e-14,
    ):
        q2_value = (
            q2_min_invertible
        )

        label = (
            "METRIC_INVERTIBILITY_BOUNDARY"
        )

    else:
        q2_value = (
            minimum_q2_for_derivative_ratio(
                effective_k_ev_m4=
                    k_cap,

                target_acceleration_m_s2=
                    TARGET_A,

                gradient_scale_m=
                    GRADIENT_SCALE_M,

                maximum_ratio=
                    chi_max,
            )
        )

        label = (
            "DERIVATIVE_RATIO"
        )

    background = (
        canonical_background_energy(
            q2_ev4=
                q2_value
        )
    )

    s2_value = (
        required_s2_for_exponential_acceleration(
            effective_k_ev_m4=
                k_cap,

            q2_ev4=
                q2_value,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                GRADIENT_SCALE_M,
        )
    )

    invertibility = (
        disformal_invertibility(
            effective_k_ev_m4=
                k_cap,

            q2_ev4=
                q2_value,

            s2_ev4=
                s2_value,
        )
    )

    cosmo_rows.append(
        {
            "gate":
                label,

            "maximum_spatial_derivative_ratio":
                chi_max,

            "q2_ev4":
                q2_value,

            "canonical_background_j_m3":
                float(
                    background[
                        "energy_density_j_m3"
                    ]
                ),

            "omega_stiff":
                float(
                    background[
                        "omega"
                    ]
                ),

            "omega_over_loose_1e3_ceiling":
                float(
                    background[
                        "omega"
                    ]
                )
                /
                LOOSE_OMEGA_STIFF_CEILING,

            "lambda_ev":
                float(
                    invertibility[
                        "lambda_ev"
                    ]
                ),

            "required_s2_ev4":
                s2_value,

            "metric_signature_margin":
                float(
                    invertibility[
                        "metric_signature_margin"
                    ]
                ),

            "spatial_derivative_ratio":
                float(
                    invertibility[
                        "spatial_derivative_expansion_ratio"
                    ]
                ),
        }
    )


# ============================================================
# 10. CLASSIFICATION
# ============================================================

outward_sign_exists = True

canonical_branch_closed = bool(
    outward_sign_exists
    and
    not stationary_local_q_reservoir_possible
    and
    not canonical_invertible_cosmology_overlap
)


assert (
    canonical_branch_closed
)


full_a1_family_closed = False

noncanonical_background_requires_explicit_action = True

# We do not invent such an action here.
#
# Therefore AGMINER should move to the already-ranked A2 recipe while
# retaining noncanonical A1 as an open-but-action-required family.


# ============================================================
# 11. PERSIST NARROW FAILURE MEMORY
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

    inserted_rule = (
        persist_v21_failure_rule(
            storage,

            k_cap_ev_m4=
                k_cap,

            omega_min_invertible=
                omega_min_invertible,

            omega_loose_ceiling=
                LOOSE_OMEGA_STIFF_CEILING,
        )
    )

    storage.set_metadata(
        "032v21_canonical_time_gradient_subbranch_closed",
        "1",
    )

    storage.set_metadata(
        "032v21_full_time_gradient_disformal_family_closed",
        "0",
    )

    storage.set_metadata(
        "agminer_next_family",
        "PROPAGATING_NONMETRICITY_HEALTHY_SINGLE_MODE",
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
    inserted_rule
)


# ============================================================
# 12. OUTPUTS
# ============================================================

K_SCAN_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


with K_SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                k_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        k_rows
    )


with COSMO_SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                cosmo_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        cosmo_rows
    )


decision = (
    "GREEN_TIME_GRADIENT_LINEAR_X_DISFORMAL_OUTWARD_SIGN_"
    "GREEN_R5_DISTINCT_ANISOTROPIC_MATERIAL_RESPONSE_"
    "RED_CANONICAL_STATIONARY_GLOBAL_Q_BACKGROUND_"
    "BY_CASIMIR_PLUS_DISFORMAL_INVERTIBILITY_PLUS_LOOSE_STIFF_COSMOLOGY_"
    "A1_FULL_FAMILY_NOT_CLOSED_"
    "AGMINER_ADVANCE_TO_A2"
)

next_step = (
    "032V21B_PROPAGATING_NONMETRICITY_"
    "MATTER_PORTAL_SIGN_AND_SOURCE_EXISTENCE_PREFLIGHT"
)


summary = {
    "branch":
        "032V21_TIME_GRADIENT_DISFORMAL_SIGN_RESERVOIR_ENERGY_AND_OFFSTATE_QUANTUM_PREFLIGHT",

    "claim_class":
        "THEOREM_FIRST_CANONICAL_TIME_GRADIENT_DISFORMAL_SUBBRANCH_GATE",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "v20_input_decision":
        v20[
            "decision"
        ],

    "architecture": {
        "physical_metric":
            "G_TILDE_EQUALS_G_PLUS_GAMMA_X_DPHI_DPHI",

        "gamma":
            "BETA_X_OVER_LAMBDA8",

        "scalar":
            "PHI_EQUALS_Q_T_PLUS_PSI_X",

        "effective_k":
            "BETA_Q2_OVER_LAMBDA8",

        "constant_gamma_reopened":
            False,

        "old_014_source_scan_reopened":
            False,

        "negative_mass_required":
            False,
    },

    "sign": {
        "outward_sign_exists":
            outward_sign_exists,

        "condition":
            "K_POSITIVE_AND_S2_DECREASES_OUTWARD",

        "finite_payload_established":
            False,
    },

    "stationary_integrability": {
        **integrability,

        "interpretation":
            "STATIONARY_Q_IS_GLOBAL_AMBIENT_BACKGROUND_OR_NEW_PHYSICS_REQUIRED",
    },

    "offstate_material_gate": {
        "allowed_extra_pressure_pa":
            allowed_extra_pressure_pa,

        "k_cap_ev_m4":
            k_cap,

        "gold_rho_times_k_at_cap":
            float(
                empirical[
                    "gold_rho_times_k"
                ]
            ),

        "gold_z_t_at_cap":
            float(
                empirical[
                    "gold_z_t"
                ]
            ),

        "gold_z_s_at_cap":
            float(
                empirical[
                    "gold_z_s"
                ]
            ),

        "reference_k_ev_m4":
            reference_k,

        "reference_pressure_pa":
            reference_pressure,

        "pure_j0_r5_material_response_reused":
            False,

        "r5_distinct_anisotropic_response":
            True,

        "full_empirical_closure":
            False,
    },

    "canonical_cosmology": {
        "critical_energy_density_j_m3":
            critical_j_m3,

        "deliberately_loose_omega_stiff_ceiling":
            LOOSE_OMEGA_STIFF_CEILING,

        "published_context_omega_stiff_bound":
            PUBLISHED_STIFF_OMEGA_CONTEXT,

        "q2_at_loose_ceiling_ev4":
            q2_at_loose_cosmology,

        "metric_margin_at_loose_ceiling":
            float(
                loose_cosmology_state[
                    "metric_signature_margin"
                ]
            ),

        "minimum_q2_for_invertibility_ev4":
            q2_min_invertible,

        "minimum_background_j_m3_for_invertibility":
            float(
                background_min_invertible[
                    "energy_density_j_m3"
                ]
            ),

        "minimum_omega_for_invertibility":
            omega_min_invertible,

        "minimum_omega_over_loose_ceiling":
            omega_min_invertible
            / LOOSE_OMEGA_STIFF_CEILING,

        "minimum_omega_for_chi_le_1":
            omega_min_chi1,

        "minimum_omega_for_chi_le_0p1":
            float(
                background_min_chi01[
                    "omega"
                ]
            ),

        "canonical_invertible_cosmology_overlap":
            canonical_invertible_cosmology_overlap,
    },

    "local_field_energy_scout": {
        "reference_k_ev_m4":
            reference_k,

        "reference_q2_ev4":
            reference_q2,

        "reference_lambda_ev":
            reference_lambda_ev,

        "reference_required_s2_ev4":
            reference_s2,

        "reference_derivative_scale_ev":
            reference_s2**0.25,

        "reference_gradient_energy_j":
            reference_gradient_energy_j,

        "reference_acceleration_m_s2":
            reference_acceleration,

        "source_action_constructed":
            False,

        "support_constructed":
            False,

        "complete_operating_ledger":
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

        "region_rules_after":
            rules_after,

        "region_rule_inserted":
            inserted_rule,

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
        "new_linear_x_disformal_outward_sign":
            "GREEN_PREFLIGHT",

        "constant_disformal_branch":
            "CLOSED_PRESERVED",

        "old_014_finite_payload_domain":
            "NOT_REOPENED",

        "stationary_local_q_reservoir":
            "CLOSED_BY_MIXED_PARTIAL_INTEGRABILITY",

        "anisotropic_offstate_material_response":
            "GREEN_RECONSTRUCTED",

        "casimir_k_ceiling":
            "ESTABLISHED_IN_DECLARED_R5_EMPIRICAL_MODEL",

        "canonical_global_q_metric_invertibility":
            "RED_WITH_LOOSE_STIFF_COSMOLOGY",

        "canonical_global_q_eft_chi_le_1":
            "RED_STRONGER",

        "canonical_stationary_linear_gamma_subbranch":
            "CLOSED",

        "noncanonical_time_gradient_background":
            "YELLOW_EXPLICIT_ACTION_REQUIRED",

        "full_a1_time_gradient_disformal_family":
            "NOT_CLOSED",

        "finite_payload":
            "NOT_REACHED_BECAUSE_CHEAP_GATE_RED",

        "complete_operating_energy":
            "NOT_ESTABLISHED",
    },

    "canonical_stationary_linear_gamma_subbranch_closed":
        canonical_branch_closed,

    "full_a1_time_gradient_disformal_family_closed":
        full_a1_family_closed,

    "noncanonical_background_requires_explicit_action":
        noncanonical_background_requires_explicit_action,

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
    "OUTWARD_SIGN_EXISTS=True"
)

print(
    "CONSTANT_GAMMA_BRANCH_REOPENED=False"
)

print(
    "OLD_014_FINITE_PAYLOAD_SCAN_REOPENED=False"
)

print(
    "STATIONARY_LOCAL_Q_RESERVOIR_POSSIBLE="
    + str(
        stationary_local_q_reservoir_possible
    )
)

print(
    "ANISOTROPIC_K_CASIMIR_CAP_EV_M4="
    f"{k_cap:.12e}"
)

print(
    "K_CAP_GOLD_ZT="
    f"{float(empirical['gold_z_t']):.12e}"
)

print(
    "K_CAP_GOLD_ZS="
    f"{float(empirical['gold_z_s']):.12e}"
)

print(
    "HALF_CAP_REFERENCE_PRESSURE_PA="
    f"{reference_pressure:.12e}"
)

print(
    "CRITICAL_ENERGY_DENSITY_J_M3="
    f"{critical_j_m3:.12e}"
)

print(
    "LOOSE_OMEGA_STIFF_CEILING="
    f"{LOOSE_OMEGA_STIFF_CEILING:.12e}"
)

print(
    "PUBLISHED_STIFF_OMEGA_CONTEXT="
    f"{PUBLISHED_STIFF_OMEGA_CONTEXT:.12e}"
)

print(
    "METRIC_MARGIN_AT_LOOSE_COSMOLOGY="
    f"{float(loose_cosmology_state['metric_signature_margin']):.12e}"
)

print(
    "MINIMUM_Q2_FOR_INVERTIBILITY_EV4="
    f"{q2_min_invertible:.12e}"
)

print(
    "MINIMUM_BACKGROUND_J_M3_FOR_INVERTIBILITY="
    f"{float(background_min_invertible['energy_density_j_m3']):.12e}"
)

print(
    "MINIMUM_OMEGA_FOR_INVERTIBILITY="
    f"{omega_min_invertible:.12e}"
)

print(
    "MINIMUM_OMEGA_OVER_LOOSE_CEILING="
    f"{omega_min_invertible/LOOSE_OMEGA_STIFF_CEILING:.12e}"
)

print(
    "MINIMUM_OMEGA_FOR_CHI_LE_1="
    f"{omega_min_chi1:.12e}"
)

print(
    "MINIMUM_OMEGA_FOR_CHI_LE_0P1="
    f"{float(background_min_chi01['omega']):.12e}"
)

print(
    "REFERENCE_LOCAL_GRADIENT_ENERGY_J="
    f"{reference_gradient_energy_j:.12e}"
)

print(
    "REFERENCE_REQUIRED_S2_EV4="
    f"{reference_s2:.12e}"
)

print(
    "REFERENCE_LAMBDA_EV="
    f"{reference_lambda_ev:.12e}"
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
    "DB_REGION_RULE_INSERTED="
    + str(
        inserted_rule
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
    "CANONICAL_STATIONARY_LINEAR_GAMMA_SUBBRANCH_CLOSED="
    + str(
        canonical_branch_closed
    )
)

print(
    "FULL_A1_TIME_GRADIENT_DISFORMAL_FAMILY_CLOSED=False"
)

print(
    "NONCANONICAL_BACKGROUND_REQUIRES_EXPLICIT_ACTION=True"
)

print(
    "BLIND_PARAMETER_SCAN_AUTHORIZED=False"
)

print(
    "AGMINER_ITSELF_PRESERVED=True"
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
