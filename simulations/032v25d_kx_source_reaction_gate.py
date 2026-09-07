"""032V25D — large-KX source reaction / canonical scale gate.

V25C closed WBG parent-scale relabeling for locally linear G3.

V25D tests whether large positive local K_X can rescue that same branch.

Two physically distinct ledgers are kept separate:

1. unchanged microscopic source drive;
2. artificially fixed scalar background gradient, with the required source
   reaction explicitly recorded.

No energy multiplier is inferred from the source-drive multiplier.

CLAIM_CLASSIFICATION=
LOCAL_CONSTANT_KX_SOURCE_REACTION_AND_CANONICAL_NORMALIZATION_FALSIFICATION
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.kx_source_reaction_gate import (
    fixed_gradient_gain_preserving_scaling,
    fixed_source_gain_preserving_scaling,
    historical_v16_kx_gate,
    local_constant_kx_theorem,
    persist_v25d_metadata,
    persist_v25d_region_rule,
    required_kappa_for_fixed_gradient_control,
    v25d_gate,
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

V25C = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25c_wbg_multiscale_summary.json"
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
    "032v25d_kx_source_reaction_summary.json"
)

FIXED_SOURCE_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25d_fixed_source_kx_scan.csv"
)

FIXED_GRADIENT_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25d_fixed_gradient_kx_scan.csv"
)

TARGET_J = 1.0e7


# ===========================================================================
# 0. POLICY / V25C PROVENANCE
# ===========================================================================

policy = current_energy_policy()

assert float(
    policy[
        "limit_j"
    ]
) == TARGET_J

assert str(
    policy[
        "comparison"
    ]
) == "LT"


if not V25C.exists():
    raise FileNotFoundError(
        str(
            V25C
        )
    )


v25c = json.loads(
    V25C.read_text(
        encoding="utf-8"
    )
)


promotion_c = v25c[
    "promotion_status"
]


assert promotion_c[
    "locally_linear_g3_parent_scale_rescue_closed"
] is True

assert promotion_c[
    "generalized_nonlinear_g3_closed"
] is False

assert promotion_c[
    "large_healthy_kx_closed"
] is False

assert promotion_c[
    "action_oracle_authorized"
] is False


# ===========================================================================
# 1. HISTORICAL BASELINE / THEOREM
# ===========================================================================

historical = (
    historical_v16_kx_gate()
)

theorem = (
    local_constant_kx_theorem()
)

gate = (
    v25d_gate()
)


baseline = float(
    historical[
        "baseline_control_ratio"
    ]
)


assert abs(
    baseline
    -
    0.19423543641148613
) < 1.0e-14


assert theorem[
    "fixed_source_local_scale_exponent"
] == (
    -1.0
    /
    3.0
)


assert theorem[
    "nonlinear_kxx_closed"
] is False

assert theorem[
    "nonlinear_g3xx_closed"
] is False


# ===========================================================================
# 2. FIXED-SOURCE LARGE-KX SCAN
# ===========================================================================

fixed_source_rows = []

for kappa in (
    1.0,
    2.0,
    5.0,
    10.0,
    100.0,
    1000.0,
    10000.0,
):
    row = (
        fixed_source_gain_preserving_scaling(
            kappa=
                kappa,

            baseline_control_ratio=
                baseline,
        )
    )

    fixed_source_rows.append(
        row
    )


assert fixed_source_rows[
    0
][
    "control_ratio"
] == baseline


assert all(
    fixed_source_rows[
        index + 1
    ][
        "control_ratio"
    ]
    <
    fixed_source_rows[
        index
    ][
        "control_ratio"
    ]
    for index
    in range(
        len(
            fixed_source_rows
        )
        -
        1
    )
)


# ===========================================================================
# 3. FIXED-GRADIENT SOURCE-REACTION SCAN
# ===========================================================================

fixed_gradient_rows = []

for kappa in (
    1.0,
    2.0,
    5.0,
    10.0,
    100.0,
    1000.0,
    10000.0,
):
    row = (
        fixed_gradient_gain_preserving_scaling(
            kappa=
                kappa,

            baseline_control_ratio=
                baseline,
        )
    )

    fixed_gradient_rows.append(
        row
    )


unit_control = (
    required_kappa_for_fixed_gradient_control(
        baseline_control_ratio=
            baseline,

        target_control_ratio=
            1.0,
    )
)


margin5 = (
    required_kappa_for_fixed_gradient_control(
        baseline_control_ratio=
            baseline,

        target_control_ratio=
            5.0,
    )
)


assert (
    unit_control[
        "required_source_drive_multiplier"
    ]
    >
    136.0
)


assert (
    margin5[
        "required_source_drive_multiplier"
    ]
    >
    1.7e4
)


# ===========================================================================
# 4. CLAIM BOUNDARIES
# ===========================================================================

assert gate[
    "large_constant_kx_fixed_source_rescue_closed"
] is True

assert gate[
    "fixed_gradient_rescue_requires_source_reaction"
] is True

assert gate[
    "source_energy_cost_established"
] is False

assert gate[
    "nonlinear_kxx_closed"
] is False

assert gate[
    "nonlinear_g3xx_closed"
] is False

assert gate[
    "full_wbg_g4_g5_closed"
] is False

assert gate[
    "action_oracle_authorized"
] is False

assert gate[
    "blind_parameter_scan_authorized"
] is False


# ===========================================================================
# 5. DATABASE FAILURE MEMORY
# ===========================================================================

TABLES = (
    "models",
    "rejections",
    "survivors",
    "region_rules",
    "action_oracles",
    "collective_scaling",
    "mechanism_metrics",
)


storage = Storage(
    DB
)

try:
    before = {
        table:
            int(
                storage.connection.execute(
                    f"""
                    SELECT COUNT(*) AS count
                    FROM {table}
                    """
                ).fetchone()[
                    "count"
                ]
            )
        for table
        in TABLES
    }

    inserted_rules = (
        persist_v25d_region_rule(
            storage
        )
    )

    persist_v25d_metadata(
        storage
    )

    after = {
        table:
            int(
                storage.connection.execute(
                    f"""
                    SELECT COUNT(*) AS count
                    FROM {table}
                    """
                ).fetchone()[
                    "count"
                ]
            )
        for table
        in TABLES
    }

finally:
    storage.close()


for table in (
    "models",
    "rejections",
    "survivors",
    "action_oracles",
    "collective_scaling",
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
# 6. OUTPUTS
# ===========================================================================

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


for path, rows in (
    (
        FIXED_SOURCE_OUT,
        fixed_source_rows,
    ),
    (
        FIXED_GRADIENT_OUT,
        fixed_gradient_rows,
    ),
):
    fields = sorted(
        {
            key
            for row
            in rows
            for key
            in row
        }
    )

    with path.open(
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
            rows
        )


summary = {
    "branch":
        "032V25D_KX_SOURCE_REACTION_CANONICAL_GATE",

    "claim_class":
        (
            "LOCAL_CONSTANT_KX_SOURCE_REACTION_AND_"
            "CANONICAL_NORMALIZATION_FALSIFICATION"
        ),

    "energy_policy": {
        "limit_j":
            TARGET_J,

        "comparison":
            "LT",

        "exactly_10mj_passes":
            False,

        "energy_optimization_run":
            False,
    },

    "v25c_provenance": {
        "locally_linear_parent_rescaling_closed":
            True,

        "large_healthy_kx_open_pre_v25d":
            True,
    },

    "local_constant_kx_theorem":
        theorem,

    "historical_v16_gate":
        historical,

    "source_reaction_control_requirements": {
        "unit_control":
            unit_control,

        "margin5_control":
            margin5,

        "source_drive_is_energy":
            False,
    },

    "database": {
        "counts_before":
            before,

        "counts_after":
            after,

        "region_rules_inserted":
            inserted_rules,

        "science_tables_mutated":
            any(
                before[
                    table
                ]
                !=
                after[
                    table
                ]
                for table
                in (
                    "models",
                    "rejections",
                    "survivors",
                    "action_oracles",
                    "collective_scaling",
                    "mechanism_metrics",
                )
            ),
    },

    "promotion_status": {
        "large_constant_kx_fixed_source_rescue_closed":
            True,

        "fixed_gradient_control_requires_source_reaction":
            True,

        "source_energy_multiplier_established":
            False,

        "nonlinear_kxx_closed":
            False,

        "nonlinear_g3xx_closed":
            False,

        "full_wbg_g4_g5_closed":
            False,

        "alternative_hidden_source_closed":
            False,

        "full_tensor_nonremovable_crosspropagator_certified":
            False,

        "full_source_rg_uv_certified":
            False,

        "new_selfconsistent_source_solved":
            False,

        "outward_sign_established":
            False,

        "finite_payload_response_established":
            False,

        "source_charge_per_joule_established":
            False,

        "complete_operating_energy_established":
            False,

        "action_oracle_authorized":
            False,

        "blind_parameter_scan_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,
    },

    "decision":
        gate[
            "decision"
        ],

    "next":
        gate[
            "next"
        ],
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
# 7. TERMINAL REPORT
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
    "V25C_LOCALLY_LINEAR_PARENT_RESCALING_CLOSURE_PRESERVED=True"
)

print(
    "LOCAL_CONSTANT_KX_THEOREM_ACTIVE=True"
)

print(
    "BASELINE_A1E3_CONTROL_RATIO="
    f"{baseline:.12e}"
)

print(
    "FIXED_SOURCE_KAPPA10_CONTROL_RATIO="
    f"{historical['fixed_source_kappa10_control_ratio']:.12e}"
)

print(
    "FIXED_SOURCE_KAPPA1000_CONTROL_RATIO="
    f"{historical['fixed_source_kappa1000_control_ratio']:.12e}"
)

print(
    "FIXED_SOURCE_KAPPA1000_REQUIRED_G3_MULTIPLIER="
    f"{historical['fixed_source_kappa1000_required_g3_multiplier']:.12e}"
)

print(
    "LARGE_CONSTANT_KX_FIXED_SOURCE_RESCUE_CLOSED=True"
)

print(
    "FIXED_GRADIENT_UNIT_CONTROL_REQUIRED_KAPPA="
    f"{historical['fixed_gradient_unit_control_required_kappa']:.12e}"
)

print(
    "FIXED_GRADIENT_UNIT_CONTROL_SOURCE_DRIVE_MULTIPLIER="
    f"{historical['fixed_gradient_unit_control_source_drive_multiplier']:.12e}"
)

print(
    "FIXED_GRADIENT_MARGIN5_REQUIRED_KAPPA="
    f"{historical['fixed_gradient_margin5_required_kappa']:.12e}"
)

print(
    "FIXED_GRADIENT_MARGIN5_SOURCE_DRIVE_MULTIPLIER="
    f"{historical['fixed_gradient_margin5_source_drive_multiplier']:.12e}"
)

print(
    "SOURCE_DRIVE_MULTIPLIER_IS_ENERGY_MULTIPLIER=False"
)

print(
    "NONLINEAR_KXX_CLOSED=False"
)

print(
    "NONLINEAR_G3XX_CLOSED=False"
)

print(
    "FULL_WBG_G4_G5_CLOSED=False"
)

print(
    "ALTERNATIVE_HIDDEN_SOURCE_CLOSED=False"
)

print(
    "FULL_TENSOR_CROSSPROP_CERTIFIED=False"
)

print(
    "FULL_SOURCE_RG_UV_CERTIFIED=False"
)

print(
    "NEW_SELFCONSISTENT_SOURCE_SOLVED=False"
)

print(
    "OUTWARD_SIGN_ESTABLISHED=False"
)

print(
    "FINITE_PAYLOAD_RESPONSE_ESTABLISHED=False"
)

print(
    "SOURCE_CHARGE_PER_JOULE_ESTABLISHED=False"
)

print(
    "ENERGY_OPTIMIZATION_RUN=False"
)

print(
    "ACTION_ORACLE_AUTHORIZED=False"
)

print(
    "ACTION_ORACLE_CREATED=False"
)

print(
    "BLIND_PARAMETER_SCAN_AUTHORIZED=False"
)

print(
    "DB_REGION_RULES_INSERTED="
    +
    str(
        inserted_rules
    )
)

print(
    "DB_SCIENCE_TABLES_MUTATED=False"
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
    gate[
        "decision"
    ]
)

print(
    "NEXT="
    +
    gate[
        "next"
    ]
)
