"""032V23 — derivative-hypermomentum multipole practical preflight.

PURPOSE
-------
V22 repaired the frontier so that the genuinely open MAG branch is no longer
the already-tested minimal healthy nonmetricity model.

The open branch from 032U is:

    ORDINARY T DERIVATIVE MULTIPOLES
    OR
    GENUINELY NEW INTRINSIC HYPERMOMENTUM.

V23 tests the first option as generously as possible before spending compute
on a microscopic intrinsic-hypermomentum model.

GATES
-----
1. Reproduce the zero-monopole / fixed-first-moment derivative-source result.
2. Grant a healthy massive longitudinal mode.
3. Grant the favorable REPULSIVE reciprocal Yukawa sign.
4. Reconstruct the complete 10-cm payload surface.
5. Use the strict 10-MJ source-energy budget.
6. Compare with a deliberately loose shape-only inverse-square-law scout over
   the Goodkind 0.2-2.0 m Yukawa range.
7. Record response-per-joule, source-energy floor and scalarized portal-scale
   mismatch.
8. Do not claim a physical metric bridge.
9. If red, preserve intrinsic/Dirac hypermomentum as the genuinely new MAG
   frontier.

No blind scan is authorized.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.derivative_hypermomentum_multipole import (
    derivative_gaussian_moments,
    longitudinal_derivative_oracle,
    persist_v23_failure_rule,
    practical_range_gate,
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

V22_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v22_localized_disformal_naturalness_frontier_summary.json"
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
    / "032v23_derivative_hypermomentum_multipole_summary.json"
)

SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v23_derivative_hypermomentum_yukawa_range_scan.csv"
)


TARGET_J = 1.0e7
TARGET_A = 9.80665

PAYLOAD_RADIUS_M = 0.10
PAYLOAD_CENTER_Z_M = 0.20

RANGE_MIN_M = 0.20
RANGE_MAX_M = 2.00

REFERENCE_RANGE_M = 0.20


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


for path in (
    V22_PATH,
    U_PATH,
):
    if not path.exists():
        raise FileNotFoundError(
            str(
                path
            )
        )


v22 = json.loads(
    V22_PATH.read_text(
        encoding="utf-8"
    )
)

u = json.loads(
    U_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    v22[
        "gate_status"
    ][
        "derivative_hypermomentum_multipole"
    ]
    ==
    "OPEN_NEXT"
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
# 1. SOURCE MOMENT RECONSTRUCTION
# ============================================================

moments = (
    derivative_gaussian_moments(
        source_energy_j=
            TARGET_J
    )
)


assert (
    moments[
        "zero_monopole"
    ]
    is True
)

assert (
    moments[
        "fixed_first_moment"
    ]
    is True
)

assert (
    moments[
        "charge_per_joule_free_parameter"
    ]
    is False
)


# ============================================================
# 2. GENEROUS HEALTHY LONGITUDINAL RESPONSE ORACLE
# ============================================================

oracle = (
    longitudinal_derivative_oracle()
)


assert (
    oracle[
        "separated_massive_cross_potential_sign"
    ]
    ==
    "REPULSIVE"
)

assert (
    oracle[
        "positive_quadratic_hamiltonian_assumed"
    ]
    is True
)

assert (
    oracle[
        "universal_physical_metric_bridge_established"
    ]
    is False
)


# ============================================================
# 3. RANGE SCAN
# ============================================================

ranges = np.geomspace(
    RANGE_MIN_M,
    RANGE_MAX_M,
    41,
)


rows = []

for range_m in ranges:
    state = (
        practical_range_gate(
            source_energy_j=
                TARGET_J,

            target_acceleration_m_s2=
                TARGET_A,

            payload_center_z_m=
                PAYLOAD_CENTER_Z_M,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            range_m=
                float(
                    range_m
                ),
        )
    )

    rows.append(
        state
    )


reference = (
    practical_range_gate(
        source_energy_j=
            TARGET_J,

        target_acceleration_m_s2=
            TARGET_A,

        payload_center_z_m=
            PAYLOAD_CENTER_Z_M,

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        range_m=
            REFERENCE_RANGE_M,
    )
)


least_bad = min(
    rows,
    key=lambda row:
        float(
            row[
                "required_over_shape_scout"
            ]
        ),
)


least_bad_gap = float(
    least_bad[
        "required_over_shape_scout"
    ]
)

least_bad_energy_floor_j = float(
    least_bad[
        "source_energy_floor_j_at_shape_scout"
    ]
)


assert (
    least_bad_gap
    >
    7.0e20
)

assert (
    least_bad_energy_floor_j
    >
    7.0e27
)


# ============================================================
# 4. CLAIM CLASSIFICATION
# ============================================================

ordinary_stress_derivative_practical_route_closed = True

all_derivative_tensor_structures_closed = False
intrinsic_hypermomentum_closed = False
dirac_hypermomentum_closed = False
full_metric_affine_gravity_closed = False

physical_metric_bridge_established = False


# ============================================================
# 5. AGMINER FAILURE MEMORY
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
        persist_v23_failure_rule(
            storage,

            least_bad_gap=
                least_bad_gap,

            least_bad_source_energy_floor_j=
                least_bad_energy_floor_j,
        )
    )

    storage.set_metadata(
        "032v23_ordinary_stress_derivative_practical_route_closed",
        "1",
    )

    storage.set_metadata(
        "032v23_intrinsic_hypermomentum_closed",
        "0",
    )

    storage.set_metadata(
        "032v23_full_metric_affine_gravity_closed",
        "0",
    )

    storage.set_metadata(
        "agminer_next_family",
        (
            "DIRAC_INTRINSIC_HYPERMOMENTUM_HEALTHY_PROPAGATING_"
            "NONMETRICITY_UNIVERSAL_METRIC_BRIDGE"
        ),
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
# 6. OUTPUTS
# ============================================================

SCAN_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
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
                rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        rows
    )


decision = (
    "RED_ORDINARY_STRESS_ONE_DERIVATIVE_MULTIPOLE_"
    "AS_PRACTICAL_UNIVERSAL_RECIPROCAL_YUKAWA_ROUTE_"
    "BY_FIXED_FIRST_MOMENT_FINITE_PAYLOAD_AND_"
    "INVERSE_SQUARE_SHAPE_GAP_GT7E20_"
    "INTRINSIC_DIRAC_HYPERMOMENTUM_FRONTIER_OPEN_"
    "FULL_MAG_NOT_CLOSED"
)

next_step = (
    "032V24_DIRAC_INTRINSIC_HYPERMOMENTUM_SOURCE_"
    "HEALTHY_PROPAGATING_NONMETRICITY_MODE_AND_"
    "UNIVERSAL_METRIC_BRIDGE_PREFLIGHT"
)


summary = {
    "branch":
        "032V23_DERIVATIVE_HYPERMOMENTUM_MULTIPOLE_FINITE_PAYLOAD_PREFLIGHT",

    "claim_class":
        "ORDINARY_STRESS_DERIVATIVE_MULTIPOLE_RESPONSE_PER_JOULE_NO_GO",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "v22_input_decision":
        v22[
            "decision"
        ],

    "u_input_decision":
        u[
            "decision"
        ],

    "source_moment": {
        **moments,

        "interpretation":
            (
                "ZERO_MONOPOLE_BUT_FIRST_MOMENT_FIXED_BY_TOTAL_SOURCE_ENERGY"
            ),
    },

    "generous_response_oracle":
        oracle,

    "finite_payload_geometry": {
        "source_point_z_m":
            0.0,

        "payload_center_z_m":
            PAYLOAD_CENTER_Z_M,

        "payload_radius_m":
            PAYLOAD_RADIUS_M,

        "near_surface_gap_m":
            PAYLOAD_CENTER_Z_M
            -
            PAYLOAD_RADIUS_M,

        "far_surface_distance_m":
            PAYLOAD_CENTER_Z_M
            +
            PAYLOAD_RADIUS_M,

        "point_source_is_optimistic":
            True,

        "physical_source_support_included":
            False,
    },

    "reference_0p2m": {
        **reference,

        "goodkind_empirical_input":
            (
                "PUBLIC_PLUS_MINUS_1PCT_ISL_SHAPE_0P4_TO_1P4M"
            ),

        "published_exact_95pct_alpha_likelihood_used":
            False,
    },

    "range_scan": {
        "range_min_m":
            RANGE_MIN_M,

        "range_max_m":
            RANGE_MAX_M,

        "points":
            len(
                rows
            ),

        "least_bad_range_m":
            float(
                least_bad[
                    "range_m"
                ]
            ),

        "least_bad_required_over_shape_scout":
            least_bad_gap,

        "least_bad_source_energy_floor_j":
            least_bad_energy_floor_j,

        "any_strict_lt10mj_point":
            any(
                bool(
                    row[
                        "strict_lt10mj_possible_under_shape_scout"
                    ]
                )
                for row in rows
            ),
    },

    "literature_frontier": {
        "mikura_percacci_2025_healthy_propagating_nonmetricity_exists":
            True,

        "mikura_percacci_matter_interactions_supplied":
            False,

        "wheeler_2026_explicit_dirac_hypermomentum_source_exists":
            True,

        "wheeler_source_matched_to_mikura_healthy_mode":
            False,

        "universal_neutral_payload_metric_bridge_constructed":
            False,

        "source_mode_overlap":
            "OPEN",

        "next_frontier_is_genuinely_new":
            True,
    },

    "gate_status": {
        "032u_zero_monopole":
            "PRESERVED",

        "032u_nonzero_derivative_first_moment":
            "PRESERVED",

        "source_charge_per_joule_free_lever":
            "CLOSED",

        "favorable_repulsive_yukawa_sign":
            "GRANTED",

        "finite_payload_sidedness":
            "GREEN_IN_ORACLE",

        "finite_payload_1g_response_per_joule":
            "RED",

        "inverse_square_empirical_shape":
            "RED_BY_ENORMOUS_MARGIN",

        "ordinary_stress_derivative_practical_route":
            "CLOSED",

        "all_derivative_tensor_projectors":
            "NOT_CLOSED",

        "intrinsic_hypermomentum":
            "OPEN",

        "dirac_hypermomentum":
            "OPEN_NEW_SOURCE_PROVENANCE",

        "universal_physical_metric_bridge":
            "NOT_ESTABLISHED",

        "full_metric_affine_gravity":
            "NOT_CLOSED",

        "complete_operating_energy":
            "NOT_ESTABLISHED",
    },

    "ordinary_stress_derivative_practical_route_closed":
        ordinary_stress_derivative_practical_route_closed,

    "all_derivative_tensor_structures_closed":
        all_derivative_tensor_structures_closed,

    "intrinsic_hypermomentum_closed":
        intrinsic_hypermomentum_closed,

    "dirac_hypermomentum_closed":
        dirac_hypermomentum_closed,

    "full_metric_affine_gravity_closed":
        full_metric_affine_gravity_closed,

    "physical_metric_bridge_established":
        physical_metric_bridge_established,

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
    "DERIVATIVE_SOURCE_MONOPOLE_ZERO="
    + str(
        moments[
            "zero_monopole"
        ]
    )
)

print(
    "DERIVATIVE_FIRST_MOMENT_FIXED="
    + str(
        moments[
            "fixed_first_moment"
        ]
    )
)

print(
    "SOURCE_CHARGE_PER_JOULE_FREE_LEVER=False"
)

print(
    "GENEROUS_MASSIVE_YUKAWA_SIGN=REPULSIVE"
)

print(
    "PHYSICAL_METRIC_BRIDGE_ESTABLISHED=False"
)

print(
    "REFERENCE_RANGE_M="
    f"{REFERENCE_RANGE_M:.12e}"
)

print(
    "REFERENCE_ALPHA_REQUIRED_FINITE_PAYLOAD="
    f"{float(reference['alpha_required_finite_payload']):.12e}"
)

print(
    "REFERENCE_ALPHA_SHAPE_SCOUT_CEILING="
    f"{float(reference['alpha_shape_scout_ceiling']):.12e}"
)

print(
    "REFERENCE_REQUIRED_OVER_SHAPE_SCOUT="
    f"{float(reference['required_over_shape_scout']):.12e}"
)

print(
    "REFERENCE_FINITE_PAYLOAD_PENALTY_OVER_NEAREST="
    f"{float(reference['finite_payload_penalty_over_nearest_point']):.12e}"
)

print(
    "REFERENCE_ADVERSE_SURFACE_DISTANCE_M="
    f"{float(reference['surface_min_source_distance_m']):.12e}"
)

print(
    "REFERENCE_SOURCE_ENERGY_FLOOR_J="
    f"{float(reference['source_energy_floor_j_at_shape_scout']):.12e}"
)

print(
    "REFERENCE_MAX_10MJ_ACCEL_AT_SHAPE_SCOUT="
    f"{float(reference['max_surface_acceleration_for_declared_source_j']):.12e}"
)

print(
    "REFERENCE_TARGET_PORTAL_SCALE_MEV="
    f"{float(reference['target_portal_scale_ev_scalarized'])/1.0e6:.12e}"
)

print(
    "REFERENCE_EMPIRICAL_PORTAL_SCALE_MIN_GEV="
    f"{float(reference['empirical_portal_scale_min_ev_scalarized'])/1.0e9:.12e}"
)

print(
    "LEAST_BAD_RANGE_M="
    f"{float(least_bad['range_m']):.12e}"
)

print(
    "LEAST_BAD_REQUIRED_OVER_SHAPE_SCOUT="
    f"{least_bad_gap:.12e}"
)

print(
    "LEAST_BAD_SOURCE_ENERGY_FLOOR_J="
    f"{least_bad_energy_floor_j:.12e}"
)

print(
    "ORDINARY_STRESS_DERIVATIVE_PRACTICAL_ROUTE_CLOSED=True"
)

print(
    "ALL_DERIVATIVE_TENSOR_STRUCTURES_CLOSED=False"
)

print(
    "INTRINSIC_HYPERMOMENTUM_CLOSED=False"
)

print(
    "DIRAC_HYPERMOMENTUM_CLOSED=False"
)

print(
    "FULL_METRIC_AFFINE_GRAVITY_CLOSED=False"
)

print(
    "WHEELER_2026_DIRAC_HYPERMOMENTUM_SOURCE_PROVENANCE=OPEN_NEXT"
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
