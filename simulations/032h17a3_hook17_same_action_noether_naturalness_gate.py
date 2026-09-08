"""032H17A3 — HOOK17 single-action scaffold and protection stop-rule.

This run follows a successful 032H17A2 exact healthy-mode source projector.

It creates no AGMINER candidates and performs no energy optimization.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_same_action_naturalness import (
    field_redefinition_invariance_gate,
    h17a3_summary,
    protection_and_provenance_gate,
    rg_protection_gate,
    same_action_scaffold,
    universal_metric_active_offstate_gate,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

DATA = (
    ROOT
    /
    "results"
    /
    "data"
)

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

SUMMARY_OUT = (
    DATA
    /
    "032h17a3_hook17_same_action_naturalness_summary.json"
)

ACTION_OUT = (
    DATA
    /
    "032h17a3_hook17_same_action_scaffold_atlas.csv"
)

RG_OUT = (
    DATA
    /
    "032h17a3_hook17_protection_rg_atlas.csv"
)


two_scaffold = (
    same_action_scaffold(
        "HOOK_2_PLUS"
    )
)

one_scaffold = (
    same_action_scaffold(
        "HOOK_1_PLUS"
    )
)

two_protection = (
    protection_and_provenance_gate(
        "HOOK_2_PLUS"
    )
)

one_protection = (
    protection_and_provenance_gate(
        "HOOK_1_PLUS"
    )
)

two_rg = (
    rg_protection_gate(
        "HOOK_2_PLUS"
    )
)

one_rg = (
    rg_protection_gate(
        "HOOK_1_PLUS"
    )
)

portal = (
    universal_metric_active_offstate_gate()
)

redefinition = (
    field_redefinition_invariance_gate()
)

summary = (
    h17a3_summary()
)


payload = {
    "hook_2plus_scaffold":
        two_scaffold,

    "hook_1plus_scaffold":
        one_scaffold,

    "hook_2plus_protection":
        two_protection,

    "hook_1plus_protection":
        one_protection,

    "hook_2plus_rg":
        two_rg,

    "hook_1plus_rg":
        one_rg,

    "universal_metric":
        portal,

    "field_redefinition":
        redefinition,

    "summary":
        summary,
}

SUMMARY_OUT.write_text(
    json.dumps(
        payload,
        indent=2,
    )
    +
    "\n",
    encoding="utf-8",
)


with ACTION_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "mode",
            "tree_level_action_scaffold",
            "exact_v24_projector_nonzero",
            "free_healthy_mode",
            "active_metric_response",
            "field_redefinition_survival",
            "same_action_provenance_complete",
            "protection_gate_pass",
        ],
    )

    writer.writeheader()

    for (
        scaffold,
        protection,
    ) in (
        (
            two_scaffold,
            two_protection,
        ),
        (
            one_scaffold,
            one_protection,
        ),
    ):
        writer.writerow(
            {
                "mode":
                    scaffold[
                        "mode"
                    ],

                "tree_level_action_scaffold":
                    protection[
                        "tree_level_action_scaffold_exists"
                    ],

                "exact_v24_projector_nonzero":
                    scaffold[
                        "h17a2_exact_source_projector_nonzero"
                    ],

                "free_healthy_mode":
                    scaffold[
                        "free_healthy_mode"
                    ],

                "active_metric_response":
                    scaffold[
                        "universal_metric_active_response_nonzero"
                    ],

                "field_redefinition_survival":
                    scaffold[
                        "field_redefinition_linear_response_survives"
                    ],

                "same_action_provenance_complete":
                    scaffold[
                        "same_action_provenance_complete"
                    ],

                "protection_gate_pass":
                    protection[
                        "naturalness_protection_gate_pass"
                    ],
            }
        )


with RG_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "mode",
            "parameter_count",
            "constraint_count",
            "codimension",
            "tangent_nullity",
            "generic_beta_normal_drift_norm",
            "generic_beta_automatically_tangent",
            "actual_beta_functions_calculated",
            "protecting_symmetry_established",
        ],
    )

    writer.writeheader()

    for row in (
        two_rg,
        one_rg,
    ):
        writer.writerow(
            {
                "mode":
                    row[
                        "mode"
                    ],

                "parameter_count":
                    row[
                        "parameter_count"
                    ],

                "constraint_count":
                    row[
                        "constraint_count"
                    ],

                "codimension":
                    row[
                        "constraint_surface_local_codimension"
                    ],

                "tangent_nullity":
                    row[
                        "constraint_surface_tangent_nullity"
                    ],

                "generic_beta_normal_drift_norm":
                    row[
                        "generic_beta_normal_drift_norm"
                    ],

                "generic_beta_automatically_tangent":
                    row[
                        "generic_beta_automatically_tangent"
                    ],

                "actual_beta_functions_calculated":
                    row[
                        "actual_beta_functions_calculated"
                    ],

                "protecting_symmetry_established":
                    row[
                        "additional_protecting_symmetry_established"
                    ],
            }
        )


print(
    "032H17A3_DECISION="
    +
    summary[
        "decision"
    ]
)

print(
    "NEXT="
    +
    summary[
        "next"
    ]
)

print(
    "HOOK_2PLUS_TREE_LEVEL_ACTION_SCAFFOLD="
    +
    str(
        summary[
            "hook_2plus_tree_level_action_scaffold"
        ]
    )
)

print(
    "HOOK_1PLUS_TREE_LEVEL_ACTION_SCAFFOLD="
    +
    str(
        summary[
            "hook_1plus_tree_level_action_scaffold"
        ]
    )
)

print(
    "HOOK_2PLUS_HEALTHY_SURFACE_CODIMENSION="
    +
    str(
        summary[
            "hook_2plus_healthy_surface_codimension"
        ]
    )
)

print(
    "HOOK_1PLUS_HEALTHY_SURFACE_CODIMENSION="
    +
    str(
        summary[
            "hook_1plus_healthy_surface_codimension"
        ]
    )
)

print(
    "HOOK_2PLUS_PROTECTION_GATE_PASS="
    +
    str(
        summary[
            "hook_2plus_protection_gate_pass"
        ]
    )
)

print(
    "HOOK_1PLUS_PROTECTION_GATE_PASS="
    +
    str(
        summary[
            "hook_1plus_protection_gate_pass"
        ]
    )
)

print(
    "UNPROTECTED_2PLUS_1PLUS_PROMOTED="
    +
    str(
        summary[
            "unprotected_2plus_1plus_promoted"
        ]
    )
)

print(
    "ACTIVE_OFFSTATE_METRIC_STRUCTURE_PRESERVED="
    +
    str(
        summary[
            "active_offstate_metric_structure_preserved"
        ]
    )
)

print(
    "ACTIVE_METRIC_SOURCE_FEEDBACK_NONZERO="
    +
    str(
        summary[
            "active_metric_source_feedback_nonzero"
        ]
    )
)

print(
    "LINEAR_RESPONSE_FIELD_REDEFINITION_INVARIANT="
    +
    str(
        summary[
            "linear_response_field_redefinition_invariant"
        ]
    )
)

print(
    "SAME_ACTION_PROVENANCE_COMPLETE="
    +
    str(
        summary[
            "same_action_provenance_complete"
        ]
    )
)

print(
    "FULL_NOETHER_COMPLETION="
    +
    str(
        summary[
            "full_noether_completion"
        ]
    )
)

print(
    "TIER1_HOOK17_MECHANISM_CERTIFIED="
    +
    str(
        summary[
            "tier1_hook17_mechanism_certified"
        ]
    )
)

print(
    "H17B_AUTHORIZED="
    +
    str(
        summary[
            "h17b_authorized"
        ]
    )
)

print(
    "ENERGY_OPTIMIZATION_AUTHORIZED="
    +
    str(
        summary[
            "energy_optimization_authorized"
        ]
    )
)

print(
    "HOOK17_REFERENCE_CAPACITY_RP1E12_J="
    +
    f"{summary['hook17_reference_capacity_rp1e12_j']:.12f}"
)

print(
    "HOOK17_COMPLETE_ENERGY_J=UNKNOWN"
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND="
    +
    (
        "YES"
        if
        summary[
            "physical_antigravity_model_found"
        ]
        else
        "NO"
    )
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND="
    +
    (
        "YES"
        if
        summary[
            "certified_sub10mj_model_found"
        ]
        else
        "NO"
    )
)

print(
    "PRACTICAL_DEVICE_FOUND="
    +
    (
        "YES"
        if
        summary[
            "practical_device_found"
        ]
        else
        "NO"
    )
)

print(
    "SUMMARY_JSON="
    +
    str(
        SUMMARY_OUT
    )
)

print(
    "ACTION_ATLAS_CSV="
    +
    str(
        ACTION_OUT
    )
)

print(
    "RG_ATLAS_CSV="
    +
    str(
        RG_OUT
    )
)
