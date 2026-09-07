"""032V24C — Dirac hook / protected-vector bridge rerank.

PURPOSE
-------
V24A established explicit trace-free Dirac nonmetricity and a clean
particle/antiparticle source witness.

V24B closed:
- the direct uncompensated rest-pair Fronsdal spin-three realization;
- the declared extended-projective pseudoscalar as a direct sub-10-MJ
  universal metric bridge.

V24C now:
1. derives the exact total-symmetric trace overlap of the clean rest pair;
2. closes its direct protected homothetic spin-one source if that trace
   vanishes;
3. maps the surviving hook source exactly into a torsion-like
   pair-antisymmetric representation;
4. checks whether the clean particle/antiparticle addition witness survives;
5. reranks the 2025 protected torsion-like vector catalogue and the 2026
   quadratically mixed vector-graviton theory;
6. does not create a candidate or energy claim.

CLAIM_CLASSIFICATION=
THEOREM_LEVEL_SOURCE_OVERLAP_AND_REPRESENTATION_RERANK_PREFLIGHT
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.dirac_hook_vector_bridge import (
    generic_bms_spin1_trace_witness,
    hook_torsionlike_map_diagnostics,
    marzo_2026_vector_graviton_bridge_template,
    persist_v24c_region_rules,
    rest_pair_bms_spin1_trace_gate,
    v24c_frontier_rerank,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.protected_dirac_metric_bridge import (
    rest_pair_fronsdal_ward_scout,
)
from antigravity_research.agminer.storage import (
    Storage,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

V24B = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24b_protected_dirac_metric_bridge_summary.json"
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
    "032v24c_dirac_hook_vector_bridge_summary.json"
)

RERANK_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24c_vector_bridge_rerank.csv"
)

STRICT_TARGET_J = 1.0e7


# ===========================================================================
# 0. PROVENANCE
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

if not V24B.exists():
    raise FileNotFoundError(
        str(
            V24B
        )
    )

v24b = json.loads(
    V24B.read_text(
        encoding=
            "utf-8"
    )
)

assert v24b[
    "promotion_status"
][
    "direct_rest_pair_fronsdal_spin3_source_compatible"
] is False

assert v24b[
    "promotion_status"
][
    "fronsdal_compensating_current_closed"
] is False

assert v24b[
    "promotion_status"
][
    "universal_physical_metric_bridge_established"
] is False

assert v24b[
    "promotion_status"
][
    "physical_antigravity_model_found"
] is False


# ===========================================================================
# 1. EXACT CLEAN REST-PAIR TRACE-MODE GATE
# ===========================================================================

spin1_gate = rest_pair_bms_spin1_trace_gate()

assert spin1_gate[
    "rest_pair_total_symmetric_source_nonzero"
] is True

assert spin1_gate[
    "lorentz_trace_zero"
] is True

assert spin1_gate[
    "direct_trace_carrier_overlap_zero"
] is True

assert spin1_gate[
    "rest_pair_direct_bms_protected_spin1_source_closed"
] is True

assert spin1_gate[
    "generic_dirac_spin1_source_closed"
] is False


generic_spin1 = generic_bms_spin1_trace_witness()

assert generic_spin1[
    "generic_algebraic_trace_carrier_nonzero"
] is True

assert generic_spin1[
    "spinor_is_on_shell_localized_stationary_source"
] is False

assert generic_spin1[
    "generic_dirac_protected_spin1_closed"
] is False


# ===========================================================================
# 2. HOOK -> TORSION-LIKE REPRESENTATION MAP
# ===========================================================================

hook = hook_torsionlike_map_diagnostics()

assert hook[
    "rest_pair_hook_source_nonzero"
] is True

assert hook[
    "torsionlike_first_pair_antisymmetric"
] is True

assert hook[
    "representation_map_invertible_on_declared_hook_space"
] is True

assert hook[
    "electron_positron_hook_same_sign"
] is True

assert hook[
    "electron_positron_torsionlike_same_sign"
] is True

assert hook[
    "pair_torsionlike_equals_two_single"
] is True

assert abs(
    hook[
        "pair_torsionlike_component_norm_over_single"
    ]
    -
    2.0
) < 1.0e-12

assert hook[
    "representation_map_is_physical_action_match"
] is False

assert hook[
    "healthy_propagating_vector_match_established"
] is False


# ===========================================================================
# 3. PRESERVE V24B SPIN-3 SCOPE
# ===========================================================================

ward = rest_pair_fronsdal_ward_scout()

assert ward[
    "direct_factorized_localized_rest_pair_without_compensator_closed"
] is True

assert ward[
    "compensating_current_or_more_general_source_closed"
] is False


# ===========================================================================
# 4. 2026 QUADRATIC VECTOR-GRAVITON BRIDGE TEMPLATE
# ===========================================================================

marzo = marzo_2026_vector_graviton_bridge_template()

assert marzo[
    "quadratic_vector_graviton_mixing"
] is True

assert marzo[
    "massless_spin2_propagates"
] is True

assert marzo[
    "massive_spin1_propagates"
] is True

assert marzo[
    "unitary_open_region_reported"
] is True

assert marzo[
    "consistent_cubic_deformation_found"
] is True

assert marzo[
    "consistent_quartic_order_noether_test_passed"
] is True

assert marzo[
    "external_dirac_source_coupling_derived"
] is False

assert marzo[
    "vector_identified_with_v24c_hook_torsionlike_mode"
] is False

assert marzo[
    "promotion_status"
] == "BRIDGE_TEMPLATE_ONLY"


# ===========================================================================
# 5. RERANK
# ===========================================================================

rerank = v24c_frontier_rerank()

by_branch = {
    row[
        "branch"
    ]:
        row
    for row
    in rerank
}

assert by_branch[
    "DIRAC_HOOK_TO_TORSIONLIKE_PROTECTED_VECTOR_ACTION_MATCH"
][
    "status"
] == "HIGHEST_PRIORITY_OPEN_SOURCE_SIDE"

assert by_branch[
    "MARZO_2026_QUADRATIC_VECTOR_GRAVITON_MIXING"
][
    "status"
] == "HIGHEST_PRIORITY_OPEN_BRIDGE_SIDE"

assert by_branch[
    "BMS_PROTECTED_TS_SPIN1_CLEAN_REST_PAIR_DIRECT"
][
    "status"
] == "CLOSED_ZERO_TRACE_SOURCE_OVERLAP"

assert by_branch[
    "BMS_PROTECTED_TS_SPIN3_CLEAN_REST_PAIR_DIRECT_NO_COMPENSATOR"
][
    "status"
] == "CLOSED_BY_V24B_WARD_GATE"

assert by_branch[
    "GENERIC_ONSHELL_DIRAC_BMS_TS_SPIN1"
][
    "status"
] == "OPEN_BUT_SOURCE_REALIZATION_NOT_ESTABLISHED"


# ===========================================================================
# 6. AGMINER FAILURE MEMORY
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

    inserted_rules = persist_v24c_region_rules(
        storage
    )

    metadata = {
        "032v24c_rest_pair_bms_spin1_trace_overlap":
            "0",

        "032v24c_rest_pair_hook_source":
            "1",

        "032v24c_hook_torsionlike_representation_map":
            "1",

        "032v24c_hook_torsionlike_action_match":
            "0",

        "032v24c_marzo_2026_quadratic_vector_graviton_bridge_template":
            "1",

        "032v24c_marzo_vector_dirac_hook_match":
            "0",

        "032v24c_universal_physical_metric_bridge_established":
            "0",

        "agminer_next_family":
            (
                "DIRAC_HOOK_TORSIONLIKE_VECTOR_TO_"
                "QUADRATIC_GRAVITON_MIXING_ACTION_MATCH"
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
# 7. OUTPUTS
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
        rerank
    )


decision = (
    "GREEN_PARTIAL_032V24C_CLEAN_REST_PAIR_PROTECTED_TS_SPIN1_"
    "ZERO_TRACE_OVERLAP_CLOSED__DIRAC_HOOK_MAPS_EXACTLY_TO_"
    "TORSIONLIKE_CARRIER_AND_PAIR_SOURCE_ADDITION_SURVIVES__"
    "MARZO_2026_QUADRATIC_VECTOR_GRAVITON_MODEL_RERANKED_AS_"
    "BRIDGE_TEMPLATE__ACTION_MATCH_REQUIRED"
)

next_step = (
    "032V24D_DIRAC_HOOK_TORSIONLIKE_VECTOR_TO_QUADRATIC_"
    "GRAVITON_MIXING_ACTION_MATCH"
)

summary = {
    "branch":
        "032V24C_DIRAC_HOOK_VECTOR_BRIDGE_RERANK",

    "energy_policy": {
        "limit_j":
            STRICT_TARGET_J,

        "comparison":
            "LT",

        "exactly_10mj_passes":
            False,

        "energy_evaluated_in_v24c":
            False,
    },

    "rest_pair_protected_spin1_gate":
        spin1_gate,

    "generic_spin1_witness":
        generic_spin1,

    "hook_torsionlike_map":
        hook,

    "v24b_fronsdal_scope":
        {
            "direct_rest_pair_without_compensator_closed":
                ward[
                    "direct_factorized_localized_rest_pair_without_compensator_closed"
                ],

            "compensating_or_general_source_closed":
                ward[
                    "compensating_current_or_more_general_source_closed"
                ],
        },

    "marzo_2026_bridge_template":
        marzo,

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

        "clean_rest_pair_protected_ts_spin1_closed":
            True,

        "clean_rest_pair_direct_ts_spin3_no_compensator_closed":
            True,

        "hook_torsionlike_representation_map_established":
            True,

        "hook_torsionlike_healthy_action_match_established":
            False,

        "marzo_bridge_template_identified":
            True,

        "marzo_vector_dirac_source_match_established":
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
            "CLEAN_REST_PARTICLE_ANTIPARTICLE_SOURCE_DIRECT_TO_"
            "BMS_HOMOTHETIC_PROTECTED_SPIN1"
        ),
    ],

    "explicitly_open": [
        (
            "DIRAC_HOOK_TO_SYMMETRY_PROTECTED_TORSIONLIKE_VECTOR_"
            "ACTION_MATCH"
        ),
        (
            "DIRAC_HOOK_OR_TORSIONLIKE_VECTOR_TO_MARZO_2026_"
            "QUADRATIC_VECTOR_GRAVITON_MODE"
        ),
        (
            "GENERIC_ONSHELL_DIRAC_TOTALLY_SYMMETRIC_SPIN1"
        ),
        (
            "COMPENSATED_OR_MORE_GENERAL_WARD_COMPATIBLE_SPIN3"
        ),
    ],

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
# 8. TERMINAL REPORT
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
    "ENERGY_EVALUATED_IN_V24C=False"
)

print(
    "REST_PAIR_TOTAL_SYMMETRIC_TRACE_ZERO="
    +
    str(
        spin1_gate[
            "lorentz_trace_zero"
        ]
    )
)

print(
    "REST_PAIR_DIRECT_TRACE_CARRIER_OVERLAP_ZERO="
    +
    str(
        spin1_gate[
            "direct_trace_carrier_overlap_zero"
        ]
    )
)

print(
    "REST_PAIR_PROTECTED_TS_SPIN1_DIRECT_SOURCE_CLOSED="
    +
    str(
        spin1_gate[
            "rest_pair_direct_bms_protected_spin1_source_closed"
        ]
    )
)

print(
    "GENERIC_DIRAC_TS_TRACE_CARRIER_NONZERO="
    +
    str(
        generic_spin1[
            "generic_algebraic_trace_carrier_nonzero"
        ]
    )
)

print(
    "GENERIC_DIRAC_TS_SPIN1_CLOSED=False"
)

print(
    "REST_PAIR_HOOK_SOURCE_NONZERO="
    +
    str(
        hook[
            "rest_pair_hook_source_nonzero"
        ]
    )
)

print(
    "HOOK_TO_TORSIONLIKE_PAIR_ANTISYMMETRIC="
    +
    str(
        hook[
            "torsionlike_first_pair_antisymmetric"
        ]
    )
)

print(
    "HOOK_TORSIONLIKE_REPRESENTATION_MAP_INVERTIBLE="
    +
    str(
        hook[
            "representation_map_invertible_on_declared_hook_space"
        ]
    )
)

print(
    "PAIR_TORSIONLIKE_SOURCE_ADDS="
    +
    str(
        hook[
            "pair_torsionlike_equals_two_single"
        ]
    )
)

print(
    "PAIR_TORSIONLIKE_COMPONENT_NORM_OVER_SINGLE="
    f"{hook['pair_torsionlike_component_norm_over_single']:.12e}"
)

print(
    "HOOK_TORSIONLIKE_ACTION_MATCH_ESTABLISHED=False"
)

print(
    "MARZO_2026_QUADRATIC_VECTOR_GRAVITON_MIXING=True"
)

print(
    "MARZO_2026_MASSLESS_SPIN2=True"
)

print(
    "MARZO_2026_MASSIVE_SPIN1=True"
)

print(
    "MARZO_2026_UNITARY_OPEN_REGION_REPORTED=True"
)

print(
    "MARZO_2026_QUARTIC_NOETHER_TEST_PASSED=True"
)

print(
    "MARZO_2026_EXTERNAL_DIRAC_SOURCE_MATCH=False"
)

print(
    "MARZO_2026_VECTOR_EQUALS_DIRAC_HOOK_MODE=False"
)

print(
    "UNIVERSAL_PHYSICAL_METRIC_BRIDGE_ESTABLISHED=False"
)

print(
    "SOURCE_CHARGE_PER_JOULE_ESTABLISHED=False"
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
