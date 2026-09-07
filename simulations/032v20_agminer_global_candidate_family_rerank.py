"""032V20 — AGMINER global candidate-family rerank.

PURPOSE
-------
032V19R6 closed the current hidden-axial pure-j0 kinetic-conformal
implementation.

This run does NOT replace AGMINER.

It does NOT launch a blind parameter campaign.

It performs the correct transition:

    CLOSED CANDIDATE IMPLEMENTATION

        ->

    FAILURE MEMORY

        ->

    TRANSPARENT FAMILY RERANK

        ->

    NEXT CHEAP PREFIELD GATE.

DATABASE POLICY
---------------
The existing AGMINER database is preserved.

V20 may add:

    region_rules
    metadata

because those are the existing scientific failure-memory/frontier-state
mechanisms.

V20 must NOT alter counts in:

    models
    rejections
    survivors
    action_oracles
    collective_scaling
    mechanism_metrics.

No prefield recipe earns MechanismMetrics merely by being highly ranked.

No action oracle is invented.

No certified model is created.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.frontier_rerank import (
    closed_recipes,
    failure_memory_rules,
    persist_failure_memory,
    persist_frontier_metadata,
    ranked_active_recipes,
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

V12_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v12_local_metric_active_operator_atlas_summary.json"
)

R4_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r4_uv_completion_atlas_summary.json"
)

R6_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r6_companion_positivity_empirical_energy_summary.json"
)

DB_PATH = (
    ROOT
    / "results"
    / "agminer"
    / "agminer.sqlite3"
)

SUMMARY_OUT = (
    ROOT
    / "results"
    / "agminer"
    / "032v20_global_candidate_family_rerank_summary.json"
)

RANK_OUT = (
    ROOT
    / "results"
    / "agminer"
    / "032v20_candidate_family_rerank.csv"
)

FAILURE_OUT = (
    ROOT
    / "results"
    / "agminer"
    / "032v20_family_failure_memory.csv"
)


TARGET_J = 1.0e7


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
    V12_PATH,
    R4_PATH,
    R6_PATH,
):
    if not path.exists():
        raise FileNotFoundError(
            str(
                path
            )
        )


v12 = json.loads(
    V12_PATH.read_text(
        encoding="utf-8"
    )
)

r4 = json.loads(
    R4_PATH.read_text(
        encoding="utf-8"
    )
)

r6 = json.loads(
    R6_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    v12[
        "decision"
    ]
    ==
    "GREEN_OPERATOR_ATLAS_KINETIC_CONFORMAL_X_METRIC_TOP_PREFIELD_CLASS"
)

assert (
    r4[
        "kinetic_conformal_class_closed"
    ]
    is False
)

assert (
    r6[
        "current_032_kinetic_conformal_axial_implementation_closed"
    ]
    is True
)

assert (
    r6[
        "all_possible_kinetic_conformal_theories_closed"
    ]
    is False
)

assert (
    r6[
        "agminer_itself_preserved"
    ]
    is True
)

assert (
    r6[
        "agminer_model_family_rerank_authorized"
    ]
    is True
)


# ============================================================
# 1. RECONSTRUCT THE DECISIVE R6 GAP
# ============================================================

empirical_metric_min_ev = float(
    r6[
        "v17_exact_reconstruction"
    ][
        "empirical_min_metric_ev"
    ]
)

energy_metric_max_ev = float(
    r6[
        "v17_exact_reconstruction"
    ][
        "energy_max_metric_ev"
    ]
)

metric_gap_ev = (
    empirical_metric_min_ev
    -
    energy_metric_max_ev
)

metric_gap_fraction = (
    metric_gap_ev
    / energy_metric_max_ev
)


assert (
    metric_gap_ev
    >
    0.0
)

assert (
    r6[
        "v17_exact_reconstruction"
    ][
        "empirical_energy_overlap_exists"
    ]
    is False
)


# ============================================================
# 2. BUILD TRANSPARENT FAMILY FRONTIER
# ============================================================

active = (
    ranked_active_recipes()
)

closed = (
    closed_recipes()
)

assert (
    active[
        0
    ].family_id
    ==
    "SHIFT_SYMMETRIC_TIME_GRADIENT_DISFORMAL_METRIC"
)

assert (
    active[
        1
    ].family_id
    ==
    "PROPAGATING_NONMETRICITY_HEALTHY_SINGLE_MODE"
)

assert any(
    row.family_id
    ==
    "CURRENT_HIDDEN_AXIAL_PURE_J0_KINETIC_CONFORMAL"
    for row in closed
)


# ============================================================
# 3. DATABASE COUNTS BEFORE FAILURE-MEMORY UPDATE
# ============================================================

TABLES_TO_PRESERVE = (
    "models",
    "rejections",
    "survivors",
    "action_oracles",
    "collective_scaling",
    "mechanism_metrics",
)


def table_count(
    storage: Storage,
    table: str,
) -> int:
    if table not in (
        "models",
        "rejections",
        "survivors",
        "region_rules",
        "action_oracles",
        "collective_scaling",
        "mechanism_metrics",
    ):
        raise ValueError(
            "unsupported table"
        )

    row = (
        storage.connection.execute(
            f"""
            SELECT COUNT(*) AS count
            FROM {table}
            """
        ).fetchone()
    )

    return int(
        row[
            "count"
        ]
    )


storage = Storage(
    DB_PATH
)

try:
    counts_before = {
        table:
            table_count(
                storage,
                table,
            )
        for table in (
            *TABLES_TO_PRESERVE,
            "region_rules",
        )
    }

    inserted_rules = (
        persist_failure_memory(
            storage
        )
    )

    persist_frontier_metadata(
        storage
    )

    counts_after = {
        table:
            table_count(
                storage,
                table,
            )
        for table in (
            *TABLES_TO_PRESERVE,
            "region_rules",
        )
    }

finally:
    storage.close()


for table in TABLES_TO_PRESERVE:
    assert (
        counts_after[
            table
        ]
        ==
        counts_before[
            table
        ]
    )


assert (
    counts_after[
        "region_rules"
    ]
    -
    counts_before[
        "region_rules"
    ]
    ==
    inserted_rules
)

assert (
    0
    <=
    inserted_rules
    <=
    len(
        failure_memory_rules()
    )
)


# ============================================================
# 4. WRITE FAMILY RANKING
# ============================================================

ranking_rows = []

for row in (
    active
    +
    closed
):
    output = (
        row.as_row()
    )

    output[
        "research_rank"
    ] = (
        ""
        if row.closed
        else
        (
            row.tier
            +
            str(
                row.priority
            )
        )
    )

    ranking_rows.append(
        output
    )


RANK_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


with RANK_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    fieldnames = [
        "research_rank",
        "family_id",
        "tier",
        "priority",
        "status",
        "closed",
        "action_readiness",
        "universal_metric_response",
        "stand_off_status",
        "protection_status",
        "source_burden",
        "support_control_burden",
        "mechanism_prior_alignment",
        "inherited_blockers",
        "next_gate",
        "provenance",
        "reason",
        "negative_mass_required",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=
            fieldnames,
    )

    writer.writeheader()

    writer.writerows(
        ranking_rows
    )


# ============================================================
# 5. WRITE FAILURE-MEMORY MANIFEST
# ============================================================

failure_rows = []

for record in failure_memory_rules():
    rule = (
        record[
            "rule"
        ]
    )

    failure_rows.append(
        {
            "family":
                record[
                    "family"
                ],

            "family_version":
                record[
                    "family_version"
                ],

            "rule_type":
                record[
                    "rule_type"
                ],

            "proof_reference":
                record[
                    "proof_reference"
                ],

            "policy_specific":
                bool(
                    rule.get(
                        "policy_specific",
                        False,
                    )
                ),

            "scope":
                str(
                    rule.get(
                        "scope",
                        "",
                    )
                ),

            "closed":
                bool(
                    rule.get(
                        "closed",
                        rule.get(
                            "closed_as_direct_rescue",
                            False,
                        ),
                    )
                ),

            "rule_json":
                json.dumps(
                    rule,
                    sort_keys=True,
                    separators=(
                        ",",
                        ":",
                    ),
                ),
        }
    )


with FAILURE_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "family",
            "family_version",
            "rule_type",
            "proof_reference",
            "policy_specific",
            "scope",
            "closed",
            "rule_json",
        ],
    )

    writer.writeheader()

    writer.writerows(
        failure_rows
    )


# ============================================================
# 6. SCIENTIFIC CLASSIFICATION
# ============================================================

decision = (
    "GREEN_AGMINER_PRESERVED_"
    "GREEN_R3_R6_FAILURE_MEMORY_INTEGRATED_"
    "RED_CURRENT_HIDDEN_AXIAL_PURE_J0_IMPLEMENTATION_PRESERVED_CLOSED_"
    "RERANK_A1_TIME_GRADIENT_DISFORMAL_"
    "A2_PROPAGATING_NONMETRICITY_"
    "NO_PHYSICAL_MODEL_FOUND"
)

next_step = (
    "032V21_TIME_GRADIENT_DISFORMAL_SIGN_"
    "RESERVOIR_ENERGY_AND_OFFSTATE_QUANTUM_PREFLIGHT"
)


summary = {
    "branch":
        "032V20_AGMINER_GLOBAL_CANDIDATE_FAMILY_RERANK",

    "claim_class":
        "FAMILY_LEVEL_RERANK_AND_PERSISTENT_FAILURE_MEMORY",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "r6_input_decision":
        r6[
            "decision"
        ],

    "r6_decisive_gap": {
        "empirical_metric_min_ev":
            empirical_metric_min_ev,

        "strict_partial_energy_metric_max_ev":
            energy_metric_max_ev,

        "metric_gap_ev":
            metric_gap_ev,

        "metric_gap_fraction":
            metric_gap_fraction,

        "empirical_energy_overlap_exists":
            False,
    },

    "agminer": {
        "preserved":
            True,

        "core_architecture_replaced":
            False,

        "candidate_database_deleted":
            False,

        "candidate_rows_added_by_rerank":
            0,

        "rejection_rows_added_by_rerank":
            0,

        "mechanism_metrics_added_by_rerank":
            0,

        "action_oracles_added_by_rerank":
            0,

        "family_region_rules_requested":
            len(
                failure_memory_rules()
            ),

        "family_region_rules_inserted_this_run":
            inserted_rules,

        "rerun_is_idempotent":
            True,
    },

    "database_counts_before":
        counts_before,

    "database_counts_after":
        counts_after,

    "frontier": {
        "ranking_method":
            "TRANSPARENT_TIER_AND_EXPLICIT_PRIORITY_NO_OPAQUE_SCORE",

        "tier_a":
            [
                row.family_id
                for row in active
                if (
                    row.tier
                    ==
                    "A"
                )
            ],

        "tier_b":
            [
                row.family_id
                for row in active
                if (
                    row.tier
                    ==
                    "B"
                )
            ],

        "tier_c":
            [
                row.family_id
                for row in active
                if (
                    row.tier
                    ==
                    "C"
                )
            ],

        "closed_preserved":
            [
                row.family_id
                for row in closed
            ],

        "top_family":
            active[
                0
            ].family_id,

        "second_family":
            active[
                1
            ].family_id,
    },

    "scope": {
        "current_hidden_axial_pure_j0_implementation_closed":
            True,

        "all_possible_kinetic_conformal_theories_closed":
            False,

        "agminer_itself_preserved":
            True,

        "negative_mass_required_by_active_frontier":
            False,

        "mechanism_metrics_population_authorized":
            False,

        "blind_large_scan_authorized":
            False,

        "next_theorem_first_prefight_authorized":
            True,
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


SUMMARY_OUT.write_text(
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
    "R6_EMPIRICAL_METRIC_MIN_KEV="
    f"{empirical_metric_min_ev/1.0e3:.12e}"
)

print(
    "R6_ENERGY_METRIC_MAX_KEV="
    f"{energy_metric_max_ev/1.0e3:.12e}"
)

print(
    "R6_METRIC_GAP_EV="
    f"{metric_gap_ev:.12e}"
)

print(
    "R6_METRIC_GAP_FRACTION="
    f"{metric_gap_fraction:.12e}"
)

print(
    "AGMINER_ITSELF_PRESERVED=True"
)

print(
    "AGMINER_CORE_ARCHITECTURE_REPLACED=False"
)

print(
    "DB_MODELS_BEFORE="
    + str(
        counts_before[
            "models"
        ]
    )
)

print(
    "DB_MODELS_AFTER="
    + str(
        counts_after[
            "models"
        ]
    )
)

print(
    "DB_REJECTIONS_BEFORE="
    + str(
        counts_before[
            "rejections"
        ]
    )
)

print(
    "DB_REJECTIONS_AFTER="
    + str(
        counts_after[
            "rejections"
        ]
    )
)

print(
    "DB_REGION_RULES_BEFORE="
    + str(
        counts_before[
            "region_rules"
        ]
    )
)

print(
    "DB_REGION_RULES_INSERTED="
    + str(
        inserted_rules
    )
)

print(
    "DB_REGION_RULES_AFTER="
    + str(
        counts_after[
            "region_rules"
        ]
    )
)

print(
    "DB_ACTION_ORACLES_MUTATED="
    + str(
        counts_before[
            "action_oracles"
        ]
        !=
        counts_after[
            "action_oracles"
        ]
    )
)

print(
    "DB_MECHANISM_METRICS_MUTATED="
    + str(
        counts_before[
            "mechanism_metrics"
        ]
        !=
        counts_after[
            "mechanism_metrics"
        ]
    )
)

print(
    "TOP_RERANKED_FAMILY="
    + active[
        0
    ].family_id
)

print(
    "SECOND_RERANKED_FAMILY="
    + active[
        1
    ].family_id
)

print(
    "CURRENT_HIDDEN_AXIAL_PURE_J0_IMPLEMENTATION_CLOSED=True"
)

print(
    "ALL_POSSIBLE_KINETIC_CONFORMAL_THEORIES_CLOSED=False"
)

print(
    "BLIND_LARGE_SCAN_AUTHORIZED=False"
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
