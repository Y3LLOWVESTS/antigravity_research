"""032V25C — WBG multiscale / locally-linear G3 invariance gate.

V25B closed the unchanged V16 source in the minimal cubic KGB action.

V25C tests whether placing that same local cubic physics into a much larger
weakly-broken-Galileon parent hierarchy actually changes the canonical
source-scale bound.

It does not, for the locally linear G3 sector.

The result is analytical and no parameter optimization is authorized.

CLAIM_CLASSIFICATION=
WBG_PARENT_SCALE_AND_LOCAL_LINEAR_G3_CANONICAL_INVARIANCE_FALSIFICATION
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.kgb_strong_coupling_source_gate import (
    V16_SOURCE_C_M,
    historical_source_compatibility,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.storage import (
    Storage,
)
from antigravity_research.agminer.wbg_multiscale_gate import (
    historical_v16_wbg_corridor,
    parent_rescaling_invariance_scout,
    persist_v25c_metadata,
    persist_v25c_region_rule,
    required_linear_g3_coefficient,
    v25c_gate,
    wbg_parent_scales,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

V25B = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25b_kgb_strong_coupling_source_summary.json"
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
    "032v25c_wbg_multiscale_summary.json"
)

PARENT_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25c_wbg_parent_scale_scan.csv"
)

GAIN_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25c_wbg_gain_coefficient_scan.csv"
)


TARGET_J = 1.0e7


# ===========================================================================
# 0. POLICY / V25B PROVENANCE
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


if not V25B.exists():
    raise FileNotFoundError(
        str(
            V25B
        )
    )


v25b = json.loads(
    V25B.read_text(
        encoding="utf-8"
    )
)


assert v25b[
    "promotion_status"
][
    "unchanged_v16_minimal_cubic_transplant_closed"
] is True

assert v25b[
    "promotion_status"
][
    "generalized_kgb_closed"
] is False

assert v25b[
    "promotion_status"
][
    "wbg_multiscale_kgb_closed"
] is False

assert v25b[
    "promotion_status"
][
    "action_oracle_authorized"
] is False


# ===========================================================================
# 1. HISTORICAL SOURCE / WBG PARENT CORRIDOR
# ===========================================================================

historical = (
    historical_source_compatibility()
)

corridor = (
    historical_v16_wbg_corridor()
)

gate = (
    v25c_gate()
)


assert (
    abs(
        float(
            v25b[
                "historical_v16_source_compatibility"
            ][
                "gradient_ev2"
            ]
        )
        -
        float(
            historical[
                "gradient_ev2"
            ]
        )
    )
    <
    1.0e-10
)

assert gate[
    "wbg_two_scale_parent_corridor_exists"
] is True

assert gate[
    "locally_linear_g3_parent_scale_rescue_closed"
] is True

assert gate[
    "generalized_nonlinear_g3_closed"
] is False

assert gate[
    "large_healthy_kx_closed"
] is False


# ===========================================================================
# 2. PARENT-SCALE SCAN
# ===========================================================================

parent_rows = []

for z_value in (
    0.001,
    0.01,
    0.1,
    1.0,
):
    row = (
        wbg_parent_scales(
            gradient_ev2=
                historical[
                    "gradient_ev2"
                ],

            length_m=
                V16_SOURCE_C_M,

            hessian_z=
                z_value,
        )
    )

    parent_rows.append(
        row
    )


assert (
    parent_rows[
        -1
    ][
        "lambda3_parent_over_source_k"
    ]
    >
    5.0e4
)

assert (
    parent_rows[
        -1
    ][
        "x_wbg"
    ]
    <
    2.0e-19
)


# ===========================================================================
# 3. FIXED-PHYSICAL-GAIN COEFFICIENT MATCHING
# ===========================================================================

gain_rows = []

for z_value in (
    0.01,
    0.1,
    1.0,
):
    for gain in (
        1.0e-6,
        1.0e-5,
        1.0e-4,
        1.0e-3,
        1.0e-2,
        0.1,
        1.0,
    ):
        row = (
            required_linear_g3_coefficient(
                gradient_ev2=
                    historical[
                        "gradient_ev2"
                    ],

                length_m=
                    V16_SOURCE_C_M,

                hessian_z=
                    z_value,

                gain_times_planck=
                    gain,
            )
        )

        gain_rows.append(
            row
        )


invariance = (
    parent_rescaling_invariance_scout(
        gradient_ev2=
            historical[
                "gradient_ev2"
            ],

        length_m=
            V16_SOURCE_C_M,

        gain_times_planck=
            1.0e-3,

        z_values=
            (
                0.01,
                0.1,
                1.0,
            ),
    )
)


assert invariance[
    "parent_rescaling_invariant"
] is True

assert (
    corridor[
        "a1e3_matches_v25b_ratio_error"
    ]
    <
    1.0e-14
)

assert (
    corridor[
        "a1e3_local_scale_over_k"
    ]
    <
    1.0
)


# ===========================================================================
# 4. DATABASE FAILURE MEMORY
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
        persist_v25c_region_rule(
            storage
        )
    )

    persist_v25c_metadata(
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
# 5. OUTPUTS
# ===========================================================================

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


for path, rows in (
    (
        PARENT_OUT,
        parent_rows,
    ),
    (
        GAIN_OUT,
        gain_rows,
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
        "032V25C_WBG_MULTISCALE_LOCAL_LINEAR_G3_GATE",

    "claim_class":
        (
            "WBG_PARENT_SCALE_AND_LOCAL_LINEAR_G3_"
            "CANONICAL_INVARIANCE_FALSIFICATION"
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

    "v25b_provenance": {
        "minimal_cubic_v16_transplant_closed":
            True,

        "generalized_kgb_open":
            True,

        "wbg_multiscale_open_pre_v25c":
            True,
    },

    "historical_wbg_corridor":
        corridor,

    "parent_rescaling_invariance": {
        "relative_spread":
            invariance[
                "relative_spread"
            ],

        "invariant":
            invariance[
                "parent_rescaling_invariant"
            ],

        "interpretation":
            (
                "MATCHING_FIXED_PHYSICAL_GAIN_CANCELS_"
                "ARBITRARY_PARENT_LAMBDA3_ADVANTAGE"
            ),
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
        "wbg_two_scale_parent_corridor_exists":
            True,

        "locally_linear_g3_parent_scale_rescue_closed":
            True,

        "generalized_nonlinear_g3_closed":
            False,

        "large_healthy_kx_closed":
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
    "V25B_MINIMAL_CUBIC_CLOSURE_PRESERVED=True"
)

print(
    "WBG_PARENT_SCALE_CORRIDOR_EXISTS=True"
)

print(
    "WBG_ZSOURCE_1_PARENT_LAMBDA3_EV="
    f"{corridor['lambda3_parent_ev']:.12e}"
)

print(
    "WBG_ZSOURCE_1_PARENT_LAMBDA3_OVER_K="
    f"{corridor['lambda3_parent_over_source_k']:.12e}"
)

print(
    "WBG_ZSOURCE_1_LAMBDA2_EV="
    f"{corridor['lambda2_ev']:.12e}"
)

print(
    "WBG_ZSOURCE_1_X="
    f"{corridor['x_wbg']:.12e}"
)

print(
    "WBG_ORDER_ONE_G3_CANONICAL_GAIN_TIMES_MPL="
    f"{corridor['order_one_g3_gain_times_planck']:.12e}"
)

print(
    "WBG_A1E3_REQUIRED_ABS_G3X="
    f"{corridor['a1e3_required_abs_g3x']:.12e}"
)

print(
    "WBG_A1E3_EFFECTIVE_LAMBDA3_EV="
    f"{corridor['a1e3_effective_lambda3_ev']:.12e}"
)

print(
    "WBG_A1E3_LOCAL_SCALE_OVER_K="
    f"{corridor['a1e3_local_scale_over_k']:.12e}"
)

print(
    "WBG_A1_LOCAL_SCALE_OVER_K="
    f"{corridor['a1_local_scale_over_k']:.12e}"
)

print(
    "WBG_A1E3_MATCHES_V25B_RATIO_ERROR="
    f"{corridor['a1e3_matches_v25b_ratio_error']:.12e}"
)

print(
    "WBG_PARENT_RESCALING_INVARIANT="
    +
    str(
        corridor[
            "parent_rescaling_invariant"
        ]
    )
)

print(
    "LOCALLY_LINEAR_G3_PARENT_SCALE_RESCALING_RESCUE_CLOSED=True"
)

print(
    "GENERALIZED_NONLINEAR_G3_CLOSED=False"
)

print(
    "LARGE_HEALTHY_KX_CLOSED=False"
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
