"""032V24D — non-removable vector-to-universal-metric bridge gate.

PURPOSE
-------
V24C established:

- a clean Dirac hook source;
- an exact hook-to-torsion-like representation map;
- survival of the particle/antiparticle source-addition witness;
- no healthy-vector action match yet;
- the Marzo 2026 vector-graviton theory only as a bridge template.

V24D now asks the decisive question:

    Is either protected-vector route actually a non-removable
    *linear* source-to-universal-metric bridge?

The two routes tested are:

1. the BMS 2025 universal IR pair-antisymmetric/torsion-like vector theories;

2. the Marzo 2026 quadratically mixed vector-graviton action.

The run uses:

- an exact Stückelberg completion-of-square identity;
- gradient invariance of the Maxwell kinetic term;
- the shared gauge-source Ward identity;
- source diagonalization under the same local field redefinition;
- the published absence of a metric perturbation in the BMS universal IR
  torsion-like action.

No parameter scan is authorized.

CLAIM_CLASSIFICATION=
PROJECT_DERIVED_FIELD_REDEFINITION_AND_SOURCE_WARD_THEOREM_PREFLIGHT
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.nonremovable_vector_metric_bridge import (
    bms_2025_torsionlike_ir_metric_gate,
    marzo_2026_linear_bridge_gate,
    persist_v24d_region_rules,
    v24d_frontier_rerank,
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

V24C = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24c_dirac_hook_vector_bridge_summary.json"
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
    "data"
    /
    "032v24d_nonremovable_vector_metric_bridge_summary.json"
)

RERANK_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24d_crosspropagator_frontier_rerank.csv"
)

STRICT_TARGET_J = 1.0e7


# ===========================================================================
# 0. PROVENANCE / POLICY
# ===========================================================================

policy = current_energy_policy()

assert float(
    policy[
        "limit_j"
    ]
) == STRICT_TARGET_J

assert str(
    policy[
        "comparison"
    ]
) == "LT"

if not V24C.exists():
    raise FileNotFoundError(
        str(
            V24C
        )
    )

v24c = json.loads(
    V24C.read_text(
        encoding=
            "utf-8"
    )
)

assert v24c[
    "promotion_status"
][
    "hook_torsionlike_representation_map_established"
] is True

assert v24c[
    "promotion_status"
][
    "hook_torsionlike_healthy_action_match_established"
] is False

assert v24c[
    "promotion_status"
][
    "marzo_bridge_template_identified"
] is True

assert v24c[
    "promotion_status"
][
    "marzo_vector_dirac_source_match_established"
] is False

assert v24c[
    "promotion_status"
][
    "universal_physical_metric_bridge_established"
] is False

assert v24c[
    "promotion_status"
][
    "physical_antigravity_model_found"
] is False


# ===========================================================================
# 1. MARZO 2026 FIELD-REDEFINITION + SOURCE WARD GATE
# ===========================================================================

marzo = marzo_2026_linear_bridge_gate()

assert marzo[
    "mixed_block_is_exact_stueckelberg_square"
] is True

assert marzo[
    "maxwell_term_gradient_shift_invariant"
] is True

assert marzo[
    "redefined_vector_gauge_invariant"
] is True

assert marzo[
    "conserved_vector_current_ward_pass"
] is True

assert marzo[
    "conserved_vector_current_transformed_metric_source_zero"
] is True

assert marzo[
    "nonconserved_current_minimal_compensator_ward_pass"
] is True

assert marzo[
    "nonconserved_current_compensator_transforms_to_zero_metric_source"
] is True

assert marzo[
    "nonremovable_linear_vector_to_metric_cross_source"
] is False

assert marzo[
    "cubic_quartic_interactions_closed"
] is False

assert marzo[
    "full_marzo_model_closed"
] is False


# ===========================================================================
# 2. BMS 2025 UNIVERSAL IR TORSION-LIKE METRIC GATE
# ===========================================================================

bms = bms_2025_torsionlike_ir_metric_gate()

assert bms[
    "healthy_vector_torsion_modes_exist"
] is True

assert bms[
    "metric_perturbation_present_as_dynamical_field"
] is False

assert bms[
    "direct_universal_physical_metric_bridge_in_declared_ir_action"
] is False

assert bms[
    "nonlinear_poincare_completion_closed"
] is False

assert bms[
    "nonlinear_metric_affine_completion_closed"
] is False

assert bms[
    "dirac_hook_source_closed"
] is False


# ===========================================================================
# 3. FRONTIER RERANK
# ===========================================================================

rerank = v24d_frontier_rerank()

by_branch = {
    row[
        "branch"
    ]:
        row
    for row
    in rerank
}

assert by_branch[
    "MARZO_2026_LINEAR_VECTOR_GRAVITON_CROSS_PORTAL"
][
    "status"
] == "CLOSED_AS_NONREMOVABLE_LINEAR_SOURCE_TO_METRIC_BRIDGE"

assert by_branch[
    "BMS_2025_UNIVERSAL_IR_TORSIONLIKE_VECTOR_AS_METRIC_BRIDGE"
][
    "status"
] == "CLOSED_WITHIN_DECLARED_UNIVERSAL_IR_ACTION"

assert by_branch[
    "NONREMOVABLE_INTRINSIC_SOURCE_TO_UNIVERSAL_METRIC_CROSS_PROPAGATOR"
][
    "status"
] == "HIGHEST_PRIORITY_GLOBAL_AGMINER_TARGET"

assert by_branch[
    "DIRAC_HOOK_TORSIONLIKE_SOURCE"
][
    "status"
] == "PRESERVED_AS_SOURCE_KNOWLEDGE_NOT_ACTIVE_MODEL"


# ===========================================================================
# 4. AGMINER FAILURE MEMORY
# ===========================================================================

storage = Storage(
    DB
)

try:
    tables = (
        "models",
        "rejections",
        "region_rules",
        "action_oracles",
        "mechanism_metrics",
    )

    before = {
        table:
            int(
                storage.connection.execute(
                    f"SELECT COUNT(*) AS count FROM {table}"
                ).fetchone()[
                    "count"
                ]
            )
        for table
        in tables
    }

    inserted_rules = persist_v24d_region_rules(
        storage
    )

    metadata = {
        "032v24d_marzo_stueckelberg_square":
            "1",

        "032v24d_marzo_linear_vector_metric_crossprop_nonremovable":
            "0",

        "032v24d_marzo_nonlinear_completion_closed":
            "0",

        "032v24d_bms_universal_ir_metric_bridge":
            "0",

        "032v24d_bms_nonlinear_completion_closed":
            "0",

        "032v24d_dirac_hook_source_closed":
            "0",

        "032v24d_universal_physical_metric_bridge_established":
            "0",

        "032v24d_blind_parameter_scan_authorized":
            "0",

        "agminer_next_family":
            (
                "NONREMOVABLE_INTRINSIC_SOURCE_TO_"
                "UNIVERSAL_METRIC_CROSS_PROPAGATOR"
            ),
    }

    for key, value in metadata.items():
        storage.set_metadata(
            key,
            value,
        )

    after = {
        table:
            int(
                storage.connection.execute(
                    f"SELECT COUNT(*) AS count FROM {table}"
                ).fetchone()[
                    "count"
                ]
            )
        for table
        in tables
    }

finally:
    storage.close()


for table in (
    "models",
    "rejections",
    "action_oracles",
    "mechanism_metrics",
):
    assert before[
        table
    ] == after[
        table
    ]

assert (
    after[
        "region_rules"
    ]
    -
    before[
        "region_rules"
    ]
    ==
    inserted_rules
)


# ===========================================================================
# 5. OUTPUTS
# ===========================================================================

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

fields = sorted(
    {
        key
        for row
        in rerank
        for key
        in row
        if not isinstance(
            row[
                key
            ],
            list,
        )
    }
)

csv_rows = []

for row in rerank:
    csv_rows.append(
        {
            key:
                value
            for key, value
            in row.items()
            if key in fields
        }
    )

with RERANK_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            fields,
    )

    writer.writeheader()
    writer.writerows(
        csv_rows
    )


decision = (
    "RED_PARTIAL_032V24D_MARZO_2026_QUADRATIC_VECTOR_METRIC_"
    "PORTAL_IS_STUECKELBERG_REMOVABLE_AND_SOURCE_WARD_"
    "DIAGONALIZABLE__BMS_2025_UNIVERSAL_IR_TORSIONLIKE_VECTOR_"
    "HAS_NO_DYNAMICAL_METRIC_BRIDGE__DIRAC_HOOK_SOURCE_PRESERVED_"
    "BUT_TESTED_PROTECTED_VECTOR_LINEAR_BRIDGES_CLOSED"
)

next_step = (
    "032V25_AGMINER_GLOBAL_RERANK_FOR_NONREMOVABLE_"
    "INTRINSIC_SOURCE_TO_UNIVERSAL_METRIC_CROSS_PROPAGATOR"
)

summary = {
    "branch":
        "032V24D_NONREMOVABLE_VECTOR_METRIC_BRIDGE_GATE",

    "energy_policy": {
        "limit_j":
            STRICT_TARGET_J,

        "comparison":
            "LT",

        "exactly_10mj_passes":
            False,

        "energy_evaluated_in_v24d":
            False,
    },

    "v24c_provenance": {
        "dirac_hook_torsionlike_source_exists":
            True,

        "healthy_action_match_pre_v24d":
            False,

        "universal_metric_bridge_pre_v24d":
            False,
    },

    "marzo_2026_gate":
        marzo,

    "bms_2025_ir_gate":
        bms,

    "frontier_rerank":
        rerank,

    "database": {
        "models_mutated":
            before[
                "models"
            ]
            !=
            after[
                "models"
            ],

        "rejections_mutated":
            before[
                "rejections"
            ]
            !=
            after[
                "rejections"
            ],

        "action_oracles_mutated":
            before[
                "action_oracles"
            ]
            !=
            after[
                "action_oracles"
            ],

        "mechanism_metrics_mutated":
            before[
                "mechanism_metrics"
            ]
            !=
            after[
                "mechanism_metrics"
            ],

        "region_rules_inserted":
            inserted_rules,

        "region_rules_before":
            before[
                "region_rules"
            ],

        "region_rules_after":
            after[
                "region_rules"
            ],
    },

    "promotion_status": {
        "blind_parameter_scan_authorized":
            False,

        "action_oracle_created":
            False,

        "dirac_hook_source_closed":
            False,

        "marzo_linear_nonremovable_metric_bridge":
            False,

        "marzo_nonlinear_completion_closed":
            False,

        "bms_ir_universal_metric_bridge":
            False,

        "bms_nonlinear_completion_closed":
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

    "closed_now": [
        (
            "MARZO_2026_EQ18_AS_NONREMOVABLE_LINEAR_VECTOR_"
            "SOURCE_TO_METRIC_PORTAL"
        ),
        (
            "BMS_2025_UNIVERSAL_FLAT_IR_TORSIONLIKE_ACTION_"
            "AS_DIRECT_UNIVERSAL_METRIC_BRIDGE"
        ),
    ],

    "explicitly_open": [
        "DIRAC_HOOK_TORSIONLIKE_MICROSCOPIC_SOURCE_KNOWLEDGE",
        "MARZO_2026_NONLINEAR_CUBIC_QUARTIC_COMPLETION",
        "BMS_NONLINEAR_POINCARE_OR_METRIC_AFFINE_COMPLETIONS",
        "BACKGROUND_DEPENDENT_PROTECTED_METRIC_TORSION_MIXING",
        (
            "NEW_ACTION_WITH_NONREMOVABLE_INTRINSIC_SOURCE_TO_"
            "UNIVERSAL_METRIC_CROSS_PROPAGATOR"
        ),
    ],

    "new_agminer_tier0_bridge_rule": {
        "required":
            True,

        "statement":
            (
                "APPARENT_SOURCE_TO_METRIC_MIXING_MUST_SURVIVE_"
                "LOCAL_INVERTIBLE_FIELD_REDEFINITIONS_AND_"
                "GAUGE_SOURCE_WARD_DIAGONALIZATION"
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


# ===========================================================================
# 6. TERMINAL REPORT
# ===========================================================================

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
    "ENERGY_EVALUATED_IN_V24D=False"
)

print(
    "DIRAC_HOOK_SOURCE_CLOSED=False"
)

print(
    "MARZO_EQ18_STUECKELBERG_SQUARE="
    +
    str(
        marzo[
            "mixed_block_is_exact_stueckelberg_square"
        ]
    )
)

print(
    "MARZO_MAXWELL_GRADIENT_SHIFT_INVARIANT="
    +
    str(
        marzo[
            "maxwell_term_gradient_shift_invariant"
        ]
    )
)

print(
    "MARZO_REDEFINED_VECTOR_GAUGE_INVARIANT="
    +
    str(
        marzo[
            "redefined_vector_gauge_invariant"
        ]
    )
)

print(
    "MARZO_CONSERVED_VECTOR_CURRENT_LINEAR_METRIC_SOURCE_ZERO="
    +
    str(
        marzo[
            "conserved_vector_current_transformed_metric_source_zero"
        ]
    )
)

print(
    "MARZO_NONCONSERVED_CURRENT_WARD_COMPENSATOR_PASS="
    +
    str(
        marzo[
            "nonconserved_current_minimal_compensator_ward_pass"
        ]
    )
)

print(
    "MARZO_NONCONSERVED_CURRENT_COMPENSATOR_METRIC_SOURCE_ZERO="
    +
    str(
        marzo[
            "nonconserved_current_compensator_transforms_to_zero_metric_source"
        ]
    )
)

print(
    "MARZO_NONREMOVABLE_LINEAR_VECTOR_METRIC_CROSS_SOURCE=False"
)

print(
    "MARZO_CUBIC_QUARTIC_COMPLETION_CLOSED=False"
)

print(
    "MARZO_FULL_MODEL_CLOSED=False"
)

print(
    "BMS_HEALTHY_TORSIONLIKE_VECTOR_MODES_EXIST=True"
)

print(
    "BMS_UNIVERSAL_IR_DYNAMICAL_METRIC_PRESENT=False"
)

print(
    "BMS_UNIVERSAL_IR_DIRECT_METRIC_BRIDGE=False"
)

print(
    "BMS_NONLINEAR_COMPLETION_CLOSED=False"
)

print(
    "NEW_TIER0_REQUIREMENT=NONREMOVABLE_SOURCE_TO_PHYSICAL_METRIC_CROSSPROPAGATOR"
)

print(
    "BLIND_PARAMETER_SCAN_AUTHORIZED=False"
)

print(
    "DB_MODELS_MUTATED="
    +
    str(
        before[
            "models"
        ]
        !=
        after[
            "models"
        ]
    )
)

print(
    "DB_REJECTIONS_MUTATED="
    +
    str(
        before[
            "rejections"
        ]
        !=
        after[
            "rejections"
        ]
    )
)

print(
    "DB_REGION_RULES_INSERTED="
    +
    str(
        inserted_rules
    )
)

print(
    "DB_ACTION_ORACLES_MUTATED="
    +
    str(
        before[
            "action_oracles"
        ]
        !=
        after[
            "action_oracles"
        ]
    )
)

print(
    "DB_MECHANISM_METRICS_MUTATED="
    +
    str(
        before[
            "mechanism_metrics"
        ]
        !=
        after[
            "mechanism_metrics"
        ]
    )
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
