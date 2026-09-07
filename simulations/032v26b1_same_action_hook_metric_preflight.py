"""032V26B1 — same-action compatibility and nonlinear hook-metric preflight.

PURPOSE
-------
Test the strongest post-V26A MAG idea without violating the project's
same-action requirement.

The run:

1. reconstructs the actual V24 rest-pair hook;
2. proves the zero-derivative linear rank-two parity obstruction;
3. constructs the simplest quadratic rank-two hook tensors;
4. checks whether the actual hook has a nonzero g00 numerator;
5. checks exact active/off-state linearization;
6. checks weak-field metric invertibility;
7. audits published action families for a complete same-action chain;
8. refuses action-oracle or energy promotion if the chain is missing.

No database mutation is performed.
No energy optimization is performed.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from antigravity_research.agminer.nonlinear_hook_metric_bridge import (
    active_offstate_numerator_gate,
    normalized_metric_signature,
    proposed_same_action_scaffold,
    quadratic_metric_descendant,
    rest_pair_hook,
    rest_pair_hook_metric_atlas,
    same_action_compatibility_atlas,
    v26b1_gate,
    weak_field_lapse_variation,
    zero_derivative_linear_metric_descendant_gate,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

SUMMARY_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26b1_same_action_hook_metric_summary.json"
)

TENSOR_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26b1_hook_metric_tensor_atlas.csv"
)

LOAD_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26b1_hook_metric_load_scan.csv"
)

COMPAT_OUT = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v26b1_same_action_compatibility.csv"
)


# ===========================================================================
# 0. HARD POLICY PROVENANCE
# ===========================================================================

policy = (
    current_energy_policy()
)

assert float(
    policy[
        "limit_j"
    ]
) == 1.0e7

assert str(
    policy[
        "comparison"
    ]
) == "LT"


# ===========================================================================
# 1. ZERO-DERIVATIVE LINEAR RANK-PARITY GATE
# ===========================================================================

parity = (
    zero_derivative_linear_metric_descendant_gate()
)

assert (
    parity[
        "zero_derivative_linear_rank2_descendant_exists"
    ]
    is False
)

assert (
    parity[
        "derivative_linear_rank2_descendants_closed"
    ]
    is False
)


# ===========================================================================
# 2. ACTUAL V24 HOOK QUADRATIC METRIC ATLAS
# ===========================================================================

atlas = (
    rest_pair_hook_metric_atlas()
)

assert (
    atlas[
        "rest_pair_hook_nonzero"
    ]
    is True
)

assert (
    atlas[
        "representation_map_invertible"
    ]
    is True
)

assert (
    atlas[
        "at_least_one_quadratic_g00_numerator_nonzero"
    ]
    is True
)

tensor_rows = []

for name, row in atlas[
    "basis"
].items():
    tensor = np.asarray(
        row[
            "tensor"
        ],
        dtype=float,
    )

    tensor_rows.append(
        {
            "basis":
                name,

            "tensor_norm":
                row[
                    "tensor_norm"
                ],

            "g00_numerator":
                row[
                    "g00_numerator"
                ],

            "g00_numerator_nonzero":
                row[
                    "g00_numerator_nonzero"
                ],

            "maximum_offdiagonal_component":
                row[
                    "maximum_offdiagonal_component"
                ],

            "diag_00":
                float(
                    tensor[
                        0,
                        0
                    ]
                ),

            "diag_11":
                float(
                    tensor[
                        1,
                        1
                    ]
                ),

            "diag_22":
                float(
                    tensor[
                        2,
                        2
                    ]
                ),

            "diag_33":
                float(
                    tensor[
                        3,
                        3
                    ]
                ),
        }
    )


# ===========================================================================
# 3. ACTIVE/OFF-STATE NUMERATOR
# ===========================================================================

active = (
    active_offstate_numerator_gate()
)

assert (
    active[
        "offstate_linear_metric_response_zero"
    ]
    is True
)

assert (
    active[
        "active_background_numerator_present"
    ]
    is True
)

assert (
    active[
        "small_principal_eigenvalue_required_by_this_algebra"
    ]
    is False
)


# ===========================================================================
# 4. WEAK-FIELD METRIC LOAD / SIGNATURE SCOUT
# ===========================================================================

hook = (
    rest_pair_hook()
)

selected_tensor = (
    quadratic_metric_descendant(
        hook,
        coefficient_b=
            1.0,
    )
)

weak_lapse = (
    weak_field_lapse_variation()
)

load_values = [
    -0.9,
    -0.5,
    -0.1,
    -1.0e-6,
    -weak_lapse[
        "absolute_delta_g00"
    ],
    weak_lapse[
        "absolute_delta_g00"
    ],
    1.0e-6,
    0.1,
    0.5,
    0.9,
]

load_rows = []

for load in load_values:
    result = (
        normalized_metric_signature(
            selected_tensor,
            delta_g00=
                load,
        )
    )

    load_rows.append(
        {
            "delta_g00":
                load,

            "determinant":
                result[
                    "determinant"
                ],

            "negative_eigenvalue_count":
                result[
                    "negative_eigenvalue_count"
                ],

            "positive_eigenvalue_count":
                result[
                    "positive_eigenvalue_count"
                ],

            "lorentzian_signature":
                result[
                    "lorentzian_signature"
                ],

            "invertible":
                result[
                    "invertible"
                ],

            "minimum_absolute_eigenvalue":
                min(
                    abs(
                        float(
                            value
                        )
                    )
                    for value
                    in result[
                        "eigenvalues"
                    ]
                ),
        }
    )

assert all(
    row[
        "lorentzian_signature"
    ]
    and
    row[
        "invertible"
    ]
    for row
    in load_rows
)


# ===========================================================================
# 5. SAME-ACTION LITERATURE / PROJECT COMPATIBILITY
# ===========================================================================

compatibility = (
    same_action_compatibility_atlas()
)

assert compatibility

assert not any(
    row[
        "current_same_action_survivor"
    ]
    for row
    in compatibility
)


# ===========================================================================
# 6. FINAL CONSERVATIVE GATE
# ===========================================================================

scaffold = (
    proposed_same_action_scaffold()
)

gate = (
    v26b1_gate()
)

assert (
    gate[
        "algebraic_design_witness"
    ]
    is True
)

assert (
    gate[
        "published_same_action_v26b1_survivor"
    ]
    is False
)

assert (
    gate[
        "full_symmetry_protected_action_established"
    ]
    is False
)

assert (
    gate[
        "action_oracle_authorized"
    ]
    is False
)

assert (
    gate[
        "energy_optimization_authorized"
    ]
    is False
)

assert (
    gate[
        "agminer_database_mutation_authorized"
    ]
    is False
)


# ===========================================================================
# 7. PERSIST READ-ONLY SCIENTIFIC ARTIFACTS
# ===========================================================================

SUMMARY_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

COMPAT_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with TENSOR_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            tensor_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        tensor_rows
    )

with LOAD_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            load_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        load_rows
    )

with COMPAT_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            compatibility[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        compatibility
    )

summary = {
    "phase":
        "032V26B1",

    "energy_policy":
        {
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
        },

    "zero_derivative_linear_metric_gate":
        parity,

    "rest_pair_hook_metric_atlas":
        atlas,

    "active_offstate_numerator_gate":
        active,

    "weak_field_payload_lapse":
        weak_lapse,

    "metric_load_scan":
        load_rows,

    "same_action_compatibility":
        compatibility,

    "proposed_same_action_scaffold":
        scaffold,

    "promotion_status":
        gate,

    "claim_limits":
        {
            "explicit_healthy_v26_action":
                False,

            "microscopic_v26_field":
                False,

            "finite_payload_antigravity":
                False,

            "complete_sub10mj_model":
                False,

            "practical_device":
                False,

            "new_physics_discovery":
                False,
        },
}

SUMMARY_OUT.write_text(
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
# 8. TERMINAL DECISION MARKERS
# ===========================================================================

print(
    "032V26B1_SAME_ACTION_HOOK_METRIC_PREFLIGHT=COMPLETED"
)

print(
    "INTRINSIC_DIRAC_HOOK_SOURCE="
    +
    (
        "PRESERVED"
        if gate[
            "intrinsic_dirac_hook_source_preserved"
        ]
        else "LOST"
    )
)

print(
    "HOOK_ZERO_DERIVATIVE_LINEAR_METRIC_DESCENDANT="
    +
    (
        "YES"
        if gate[
            "hook_zero_derivative_linear_metric_descendant"
        ]
        else "NO"
    )
)

print(
    "HOOK_DERIVATIVE_LINEAR_DESCENDANTS_CLOSED="
    +
    (
        "YES"
        if gate[
            "hook_derivative_linear_metric_descendants_closed"
        ]
        else "NO"
    )
)

print(
    "HOOK_QUADRATIC_RANK2_METRIC_DESCENDANT="
    +
    (
        "PRESENT"
        if gate[
            "hook_quadratic_rank2_metric_descendant_exists"
        ]
        else "ABSENT"
    )
)

print(
    "HOOK_QUADRATIC_ACTIVE_BACKGROUND_G00_NUMERATOR="
    +
    (
        "PRESENT"
        if gate[
            "hook_quadratic_active_background_g00_numerator"
        ]
        else "ABSENT"
    )
)

print(
    "OFFSTATE_LINEAR_HOOK_METRIC_RESPONSE_ZERO="
    +
    str(
        gate[
            "offstate_linear_hook_metric_response_zero"
        ]
    )
)

print(
    "NUMERATOR_REQUIRES_PRINCIPAL_MARGIN_COLLAPSE="
    +
    str(
        gate[
            "numerator_requires_principal_margin_collapse_at_algebraic_level"
        ]
    )
)

print(
    "ONE_G_0P1M_ABS_DELTA_G00="
    +
    format(
        weak_lapse[
            "absolute_delta_g00"
        ],
        ".12e",
    )
)

for row in tensor_rows:
    print(
        "HOOK_METRIC_BASIS_"
        +
        row[
            "basis"
        ]
        +
        "_G00="
        +
        format(
            float(
                row[
                    "g00_numerator"
                ]
            ),
            ".12e",
        )
    )

print(
    "PUBLISHED_SAME_ACTION_SURVIVOR_COUNT="
    +
    str(
        gate[
            "published_same_action_survivor_count"
        ]
    )
)

print(
    "PUBLISHED_SAME_ACTION_V26B1_SURVIVOR="
    +
    str(
        gate[
            "published_same_action_v26b1_survivor"
        ]
    )
)

print(
    "ALGEBRAIC_DESIGN_WITNESS="
    +
    str(
        gate[
            "algebraic_design_witness"
        ]
    )
)

print(
    "FULL_SYMMETRY_PROTECTED_ACTION_ESTABLISHED="
    +
    str(
        gate[
            "full_symmetry_protected_action_established"
        ]
    )
)

print(
    "HEALTHY_MODE_PROJECTION_AUTHORIZED="
    +
    str(
        gate[
            "healthy_mode_projection_authorized"
        ]
    )
)

print(
    "ACTION_ORACLE_AUTHORIZED="
    +
    str(
        gate[
            "action_oracle_authorized"
        ]
    )
)

print(
    "ENERGY_OPTIMIZATION_AUTHORIZED="
    +
    str(
        gate[
            "energy_optimization_authorized"
        ]
    )
)

print(
    "AGMINER_DATABASE_MUTATION_AUTHORIZED="
    +
    str(
        gate[
            "agminer_database_mutation_authorized"
        ]
    )
)

print(
    "NEXT_PRIMARY="
    +
    str(
        gate[
            "next_primary"
        ]
    )
)

print(
    "FALLBACK_IF_SAME_ACTION_CANNOT_BE_CONSTRUCTED="
    +
    str(
        gate[
            "fallback_if_same_action_cannot_be_constructed"
        ]
    )
)

print(
    "SUMMARY="
    +
    str(
        SUMMARY_OUT
    )
)

print(
    "TENSOR_ATLAS="
    +
    str(
        TENSOR_OUT
    )
)

print(
    "LOAD_SCAN="
    +
    str(
        LOAD_OUT
    )
)

print(
    "SAME_ACTION_COMPATIBILITY="
    +
    str(
        COMPAT_OUT
    )
)
