"""032V25 — global AGMINER rerank for a non-removable metric bridge.

This run does not search parameters.

It integrates the completed V21-V24 falsification sequence into the current
AGMINER scheduler while preserving V20 as historical state.

The new Tier-0 chain is:

    intrinsic/source-side leverage
        ->
    healthy canonical mediator
        ->
    ONE universal physical metric
        ->
    NON-REMOVABLE cross-propagator
        ->
    source Ward compatibility
        ->
    protection/naturalness

before an action oracle, energy optimization, PDE, or blind parameter scan
is authorized.

CLAIM_CLASSIFICATION=
CURRENT_FRONTIER_RERANK_AND_TIER0_ARCHITECTURE_UPDATE
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.nonremovable_frontier_rerank import (
    active_frontier_rows,
    closed_frontier_rows,
    historical_reference_lessons,
    persist_v25_metadata,
    tier0_promotion_policy,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.storage import (
    Storage,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]


V20 = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v20_global_candidate_family_rerank_summary.json"
)

V24D = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24d_nonremovable_vector_metric_bridge_summary.json"
)

DB = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "agminer.sqlite3"
)

OUT = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v25_nonremovable_crosspropagator_rerank_summary.json"
)

RANK_OUT = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v25_nonremovable_crosspropagator_rerank.csv"
)

POLICY_OUT = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v25_tier0_bridge_requirements.csv"
)


TARGET_J = 1.0e7


# ============================================================
# 0. ENERGY POLICY
# ============================================================

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


# ============================================================
# 1. HISTORICAL V20 + CURRENT V24D PROVENANCE
# ============================================================

if not V20.exists():
    raise FileNotFoundError(
        str(
            V20
        )
    )

if not V24D.exists():
    raise FileNotFoundError(
        str(
            V24D
        )
    )


v20 = json.loads(
    V20.read_text(
        encoding=
            "utf-8"
    )
)

v24d = json.loads(
    V24D.read_text(
        encoding=
            "utf-8"
    )
)


# Historical V20 must remain reproducible.
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
        "frontier"
    ][
        "second_family"
    ]
    ==
    "PROPAGATING_NONMETRICITY_HEALTHY_SINGLE_MODE"
)


# V24D supersedes V20 as current frontier evidence.
promotion = (
    v24d[
        "promotion_status"
    ]
)

assert (
    promotion[
        "dirac_hook_source_closed"
    ]
    is False
)

assert (
    promotion[
        "marzo_linear_nonremovable_metric_bridge"
    ]
    is False
)

assert (
    promotion[
        "bms_ir_universal_metric_bridge"
    ]
    is False
)

assert (
    promotion[
        "nonremovable_crosspropagator_model_identified"
    ]
    is False
)

assert (
    promotion[
        "universal_physical_metric_bridge_established"
    ]
    is False
)

assert (
    promotion[
        "physical_antigravity_model_found"
    ]
    is False
)

assert (
    promotion[
        "certified_sub10mj_model_found"
    ]
    is False
)

assert (
    v24d[
        "next"
    ]
    ==
    (
        "032V25_AGMINER_GLOBAL_RERANK_FOR_NONREMOVABLE_"
        "INTRINSIC_SOURCE_TO_UNIVERSAL_METRIC_CROSS_PROPAGATOR"
    )
)


# ============================================================
# 2. BUILD CURRENT FRONTIER
# ============================================================

active = (
    active_frontier_rows()
)

closed = (
    closed_frontier_rows()
)

bridge_policy = (
    tier0_promotion_policy()
)

lessons = (
    historical_reference_lessons()
)


assert (
    active[
        0
    ].family_id
    ==
    "INTRINSIC_SOURCE_ACTIVE_STATE_UNIVERSAL_METRIC_SYNTHESIS"
)

assert (
    active[
        1
    ].family_id
    ==
    "ACTIVE_STATE_DEPENDENT_KINETIC_METRIC_DESCREENING"
)

assert (
    active[
        2
    ].family_id
    ==
    "SHIFT_PROTECTED_GOLDSTONE_KINETIC_METRIC_WITH_R5_EVASION"
)

assert all(
    not row.action_oracle_authorized
    for row
    in active
)

assert (
    bridge_policy[
        "blind_parameter_scan_authorized"
    ]
    is False
)

assert (
    bridge_policy[
        "energy_optimization_before_tier0"
    ]
    is False
)


# ============================================================
# 3. DATABASE — METADATA ONLY
# ============================================================

TABLES = (
    "models",
    "rejections",
    "survivors",
    "region_rules",
    "action_oracles",
    "collective_scaling",
    "mechanism_metrics",
)


def table_count(
    storage: Storage,
    table: str,
) -> int:
    if table not in TABLES:
        raise ValueError(
            "unsupported table"
        )

    row = storage.connection.execute(
        f"""
        SELECT COUNT(*) AS count
        FROM {table}
        """
    ).fetchone()

    return int(
        row[
            "count"
        ]
    )


storage = Storage(
    DB
)

try:
    counts_before = {
        table:
            table_count(
                storage,
                table,
            )
        for table
        in TABLES
    }

    persist_v25_metadata(
        storage
    )

    counts_after = {
        table:
            table_count(
                storage,
                table,
            )
        for table
        in TABLES
    }

finally:
    storage.close()


assert (
    counts_after
    ==
    counts_before
)


# ============================================================
# 4. WRITE CURRENT RANKING
# ============================================================

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


ranking_rows = []

for row in (
    *active,
    *closed,
):
    item = (
        row.as_row()
    )

    item[
        "tier0_missing"
    ] = ";".join(
        item[
            "tier0_missing"
        ]
    )

    ranking_rows.append(
        item
    )


rank_fields = list(
    ranking_rows[
        0
    ].keys()
)


with RANK_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            rank_fields,
    )

    writer.writeheader()

    writer.writerows(
        ranking_rows
    )


# ============================================================
# 5. WRITE TIER-0 REQUIREMENTS
# ============================================================

policy_rows = []

for field in bridge_policy[
    "required_fields"
]:
    policy_rows.append(
        {
            "requirement":
                field,

            "required_before_action_oracle":
                True,

            "required_before_energy_optimization":
                True,

            "v25_current_model_satisfies":
                False,
        }
    )


policy_rows.extend(
    [
        {
            "requirement":
                "active_offstate_separation_not_failed",

            "required_before_action_oracle":
                True,

            "required_before_energy_optimization":
                True,

            "v25_current_model_satisfies":
                False,
        },
        {
            "requirement":
                "finite_payload_and_response_per_joule",

            "required_before_action_oracle":
                False,

            "required_before_energy_optimization":
                False,

            "v25_current_model_satisfies":
                False,
        },
    ]
)


with POLICY_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                policy_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()

    writer.writerows(
        policy_rows
    )


# ============================================================
# 6. SUMMARY
# ============================================================

decision = (
    "GREEN_032V25_AGMINER_GLOBAL_RERANK_UPDATED_TO_NONREMOVABLE_"
    "INTRINSIC_SOURCE_TO_UNIVERSAL_METRIC_GATE__NO_ACTION_ORACLE_"
    "PROMOTED__NO_BLIND_SCAN__A1_SYNTHESIS_TARGET_IS_INTRINSIC_SOURCE_"
    "PLUS_ACTIVE_STATE_UNIVERSAL_METRIC_PORTAL"
)


next_step = (
    "032V25A_EXPLICIT_SYMMETRY_PROTECTED_ACTIVE_STATE_NONREMOVABLE_"
    "PHYSICAL_METRIC_ACTION_EXISTENCE_GATE"
)


summary = {
    "branch":
        "032V25_AGMINER_NONREMOVABLE_CROSSPROPAGATOR_GLOBAL_RERANK",

    "claim_class":
        "CURRENT_FRONTIER_RERANK_AND_TIER0_ARCHITECTURE_UPDATE",

    "energy_policy": {
        "policy_id":
            str(
                policy[
                    "policy_id"
                ]
            ),

        "limit_j":
            float(
                policy[
                    "limit_j"
                ]
            ),

        "comparison":
            str(
                policy[
                    "comparison"
                ]
            ),

        "exactly_10mj_passes":
            False,

        "energy_optimization_run":
            False,
    },

    "historical_v20_preserved": {
        "top_family_at_v20":
            v20[
                "frontier"
            ][
                "top_family"
            ],

        "second_family_at_v20":
            v20[
                "frontier"
            ][
                "second_family"
            ],

        "historical_module_rewritten":
            False,
    },

    "v24d_input": {
        "decision":
            v24d[
                "decision"
            ],

        "dirac_hook_source_preserved":
            not promotion[
                "dirac_hook_source_closed"
            ],

        "marzo_linear_nonremovable_bridge":
            promotion[
                "marzo_linear_nonremovable_metric_bridge"
            ],

        "bms_ir_universal_metric_bridge":
            promotion[
                "bms_ir_universal_metric_bridge"
            ],

        "nonremovable_model_identified":
            promotion[
                "nonremovable_crosspropagator_model_identified"
            ],
    },

    "new_tier0_policy":
        bridge_policy,

    "active_frontier": [
        row.as_row()
        for row
        in active
    ],

    "closed_preserved": [
        row.as_row()
        for row
        in closed
    ],

    "historical_reference_lessons":
        lessons,

    "database": {
        "counts_before":
            counts_before,

        "counts_after":
            counts_after,

        "science_tables_mutated":
            counts_after
            !=
            counts_before,

        "region_rules_inserted":
            0,

        "metadata_updated":
            True,
    },

    "promotion_status": {
        "action_oracle_created":
            False,

        "action_oracle_authorized":
            False,

        "blind_parameter_scan_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "explicit_v25a_action_exists":
            False,

        "nonremovable_crosspropagator_model_identified":
            False,

        "universal_physical_metric_bridge_established":
            False,

        "source_charge_per_joule_established":
            False,

        "finite_payload_outward_response_established":
            False,

        "complete_operating_energy_established":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,
    },

    "a1_design_target": {
        "name":
            active[
                0
            ].family_id,

        "is_physical_model":
            False,

        "is_action_oracle":
            False,

        "required_combination": [
            "INTRINSIC_HIGH_CHARGE_SOURCE",
            "SYMMETRY_PROTECTED_ACTIVE_STATE_PORTAL",
            "ONE_UNIVERSAL_PHYSICAL_METRIC",
            "NONREMOVABLE_CROSSPROPAGATOR",
            "WARD_COMPATIBLE_SOURCE",
            "ACTIVE_OFFSTATE_SEPARATION",
        ],

        "why_ranked_first":
            (
                "SYNTHESIZES_V24_SOURCE_LESSON_WITH_"
                "V17_RESPONSE_PER_JOULE_AND_R5_R6_"
                "OFFSTATE_EMPIRICAL_LESSON_WITH_V24D_"
                "FIELD_REDEFINITION_WARD_GATE"
            ),
    },

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
    +
    "\n",
    encoding="utf-8",
)


# ============================================================
# 7. TERMINAL REPORT
# ============================================================

print(
    "BRANCH="
    +
    summary[
        "branch"
    ]
)

print(
    "STRICT_COMPLETE_OPERATING_ENERGY_LT_10MJ=True"
)

print(
    "HISTORICAL_V20_RANKING_PRESERVED=True"
)

print(
    "HISTORICAL_V20_MODULE_REWRITTEN=False"
)

print(
    "V24D_DIRAC_HOOK_SOURCE_PRESERVED=True"
)

print(
    "V24D_TESTED_PROTECTED_LINEAR_VECTOR_BRIDGES_CLOSED=True"
)

print(
    "NEW_TIER0_NONREMOVABLE_CROSSPROPAGATOR_REQUIRED=True"
)

print(
    "NEW_TIER0_SOURCE_WARD_COMPATIBILITY_REQUIRED=True"
)

print(
    "NEW_TIER0_ONE_UNIVERSAL_PHYSICAL_METRIC_REQUIRED=True"
)

print(
    "NEW_TIER0_CANONICAL_NORMALIZATION_REQUIRED=True"
)

print(
    "TOP_CURRENT_DESIGN_TARGET="
    +
    active[
        0
    ].family_id
)

print(
    "SECOND_CURRENT_TARGET="
    +
    active[
        1
    ].family_id
)

print(
    "THIRD_CURRENT_TARGET="
    +
    active[
        2
    ].family_id
)

print(
    "TOP_TARGET_IS_PHYSICAL_MODEL=False"
)

print(
    "ACTION_ORACLE_AUTHORIZED=False"
)

print(
    "ACTION_ORACLE_CREATED=False"
)

print(
    "ENERGY_OPTIMIZATION_AUTHORIZED=False"
)

print(
    "BLIND_PARAMETER_SCAN_AUTHORIZED=False"
)

print(
    "V17_HISTORICAL_PARTIAL_J="
    f"{lessons['v17']['partial_energy_j']:.12e}"
)

print(
    "DESIRED_FUTURE_EARLY_PARTIAL_MIN_J="
    f"{lessons['desired_future_early_partial_j']['preferred_min']:.12e}"
)

print(
    "DESIRED_FUTURE_EARLY_PARTIAL_MAX_J="
    f"{lessons['desired_future_early_partial_j']['preferred_max']:.12e}"
)

for table in TABLES:
    print(
        f"DB_{table.upper()}_BEFORE="
        +
        str(
            counts_before[
                table
            ]
        )
    )

    print(
        f"DB_{table.upper()}_AFTER="
        +
        str(
            counts_after[
                table
            ]
        )
    )

print(
    "DB_SCIENCE_TABLES_MUTATED=False"
)

print(
    "DB_REGION_RULES_INSERTED=0"
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=False"
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND=False"
)

print(
    "DECISION="
    +
    decision
)

print(
    "NEXT="
    +
    next_step
)
