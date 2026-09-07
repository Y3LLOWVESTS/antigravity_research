"""032V25F — full KGB metric numerator / radial principal-symbol gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.kgb_metric_numerator_stability_gate import (
    INV_SQRT_6,
    local_kgb_components,
    persist_v25f_metadata,
    persist_v25f_region_rule,
    planar_local_components,
    radial_braiding_bound,
    required_radial_margin_for_transfer,
    source_aligned_efficiency_theorem,
    v25f_gate,
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

V25E = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25e_nonlinear_kgb_current_summary.json"
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
    "032v25f_kgb_metric_numerator_stability_summary.json"
)

PLANAR_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25f_planar_radial_braiding_scan.csv"
)

SPHERICAL_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25f_spherical_source_efficiency_scan.csv"
)

TRANSFER_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25f_transfer_margin_requirements.csv"
)

TARGET_J = 1.0e7


# ===========================================================================
# 0. POLICY / V25E PROVENANCE
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


if not V25E.exists():
    raise FileNotFoundError(
        str(
            V25E
        )
    )


v25e = json.loads(
    V25E.read_text(
        encoding="utf-8"
    )
)


promotion_e = v25e[
    "promotion_status"
]


assert promotion_e[
    "monotone_source_current_antiscreen_closed"
] is True

assert promotion_e[
    "nonmonotone_kxx_closed"
] is False

assert promotion_e[
    "nonmonotone_g3xx_closed"
] is False

assert promotion_e[
    "metric_braiding_numerator_analyzed"
] is False

assert promotion_e[
    "action_oracle_authorized"
] is False


# ===========================================================================
# 1. PLANAR PRINCIPAL-SYMBOL SCAN
# ===========================================================================

planar_rows = []

for d_value in (
    1.0,
    0.1,
    0.01,
    0.001,
    0.0,
):
    for q_value in (
        0.05,
        0.10,
        0.25,
        0.50,
        1.00,
    ):
        state = (
            planar_local_components(
                a_value=
                    2.0,

                d_value=
                    d_value,

                q_value=
                    q_value,
            )
        )

        bound = (
            radial_braiding_bound(
                d_value=
                    d_value,

                q_value=
                    q_value,
            )
        )

        planar_rows.append(
            {
                **state,

                "n2_over_zr":
                    bound[
                        "numerator_squared_over_z_radial"
                    ],

                "one_sixth_bound_pass":
                    bound[
                        "bound_one_sixth"
                    ],
            }
        )


assert all(
    row[
        "one_sixth_bound_pass"
    ]
    for row
    in planar_rows
)


assert max(
    row[
        "radial_canonical_braiding"
    ]
    for row
    in planar_rows
) <= (
    INV_SQRT_6
    +
    1.0e-14
)


# ===========================================================================
# 2. SPHERICAL SOURCE-EFFICIENCY SCAN
# ===========================================================================

spherical_rows = []

for a_value in (
    0.1,
    1.0,
    10.0,
):
    for b_value in (
        0.01,
        0.10,
        0.50,
        1.00,
    ):
        efficiency = (
            source_aligned_efficiency_theorem(
                u=
                    1.0,

                radius=
                    1.0,

                mpl=
                    1.0,

                a_value=
                    a_value,

                b_value=
                    b_value,
            )
        )

        state = (
            local_kgb_components(
                u=
                    1.0,

                radius=
                    1.0,

                mpl=
                    1.0,

                a_value=
                    a_value,

                a_s=
                    0.0,

                b_value=
                    b_value,

                b_s=
                    0.0,

                u_prime=
                    0.0,
            )
        )

        spherical_rows.append(
            {
                "a_value":
                    a_value,

                "b_value":
                    b_value,

                "geometry_normalized_efficiency":
                    efficiency[
                        "geometry_normalized_efficiency"
                    ],

                "efficiency_bound_pass":
                    efficiency[
                        "efficiency_bound_pass"
                    ],

                "z_time":
                    state[
                        "z_time"
                    ],

                "z_angular":
                    state[
                        "z_angular"
                    ],

                "z_radial":
                    state[
                        "z_radial"
                    ],

                "scalar_principal_healthy":
                    state[
                        "scalar_principal_healthy"
                    ],
            }
        )


assert all(
    row[
        "efficiency_bound_pass"
    ]
    for row
    in spherical_rows
)


# ===========================================================================
# 3. TRANSFER-MARGIN NECESSARY CONDITIONS
# ===========================================================================

transfer_rows = [
    required_radial_margin_for_transfer(
        gain
    )
    for gain
    in (
        1.0,
        10.0,
        100.0,
        1000.0,
        10000.0,
    )
]


gain1000 = next(
    row
    for row
    in transfer_rows
    if row[
        "transfer_gain"
    ]
    ==
    1000.0
)


assert abs(
    gain1000[
        "necessary_maximum_z_radial"
    ]
    -
    1.0
    /
    6.0e6
) < 1.0e-20


# ===========================================================================
# 4. CLAIM GATE
# ===========================================================================

gate = (
    v25f_gate()
)


assert gate[
    "exact_metric_braiding_numerator_analyzed"
] is True

assert gate[
    "full_radial_principal_backreaction_analyzed"
] is True

assert gate[
    "source_aligned_radial_canonical_braiding_bound"
] is True

assert gate[
    "source_aligned_nonmonotone_current_tuning_free_metric_gain_closed"
] is True

assert gate[
    "sign_reversed_b_branch_closed"
] is False

assert gate[
    "g4_g5_wbg_closed"
] is False

assert gate[
    "alternative_hidden_source_closed"
] is False

assert gate[
    "action_oracle_authorized"
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
        persist_v25f_region_rule(
            storage
        )
    )

    persist_v25f_metadata(
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


def write_rows(
    path: Path,
    rows: list[dict],
) -> None:
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


write_rows(
    PLANAR_OUT,
    planar_rows,
)

write_rows(
    SPHERICAL_OUT,
    spherical_rows,
)

write_rows(
    TRANSFER_OUT,
    transfer_rows,
)


summary = {
    "branch":
        "032V25F_KGB_METRIC_NUMERATOR_RADIAL_STABILITY_GATE",

    "claim_class":
        (
            "FULL_KGB_RADIAL_PRINCIPAL_SYMBOL_AND_"
            "METRIC_NUMERATOR_FALSIFICATION"
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

    "v25e_provenance": {
        "monotone_current_antiscreen_closed":
            True,

        "nonmonotone_kxx_open_pre_v25f":
            True,

        "nonmonotone_g3xx_open_pre_v25f":
            True,
    },

    "literature_oracle": {
        "reference":
            "Deffayet_et_al_arXiv_1008_0048_Eqs_12_18",

        "characteristic_factorization":
            True,

        "scalar_effective_metric_after_debraiding":
            True,

        "pure_gravitational_characteristic_factor":
            True,
    },

    "exact_local_relations": {
        "radial_principal":
            "Z_r=D+3*q^2/2",

        "metric_numerator_times_mpl":
            "N=q/2",

        "regular_source_branch":
            "D>=0",

        "canonical_bound":
            "N^2/Z_r<=1/6",

        "radial_canonical_braiding_max":
            INV_SQRT_6,

        "source_efficiency_bound":
            "(abs(N)/F)*(4*Mpl/r)<=1",
    },

    "gain1000_requirement": {
        "necessary_maximum_z_radial":
            gain1000[
                "necessary_maximum_z_radial"
            ],

        "required_collapse_factor":
            gain1000[
                "required_radial_collapse_factor_from_unit_margin"
            ],
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
        "metric_braiding_numerator_analyzed":
            True,

        "full_radial_principal_backreaction_analyzed":
            True,

        "source_aligned_nonmonotone_free_metric_gain_closed":
            True,

        "sign_reversed_b_branch_closed":
            False,

        "cancellation_branch_closed":
            False,

        "g4_g5_wbg_closed":
            False,

        "alternative_hidden_source_closed":
            False,

        "oblate_nonlinear_source_closed":
            False,

        "full_finite_payload_crosspropagator_certified":
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

        "global_rerank_recommended":
            True,
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
    "V25E_MONOTONE_CURRENT_CLOSURE_PRESERVED=True"
)

print(
    "KGB_CHARACTERISTIC_FACTORIZATION_USED=True"
)

print(
    "EXACT_METRIC_BRAIDING_NUMERATOR_ANALYZED=True"
)

print(
    "FULL_RADIAL_PRINCIPAL_BACKREACTION_ANALYZED=True"
)

print(
    "RADIAL_PRINCIPAL_IDENTITY=Z_R_EQUALS_D_PLUS_3_Q2_OVER_2"
)

print(
    "METRIC_NUMERATOR_IDENTITY=N_EQUALS_Q_OVER_2"
)

print(
    "SOURCE_ALIGNED_CANONICAL_BOUND=N2_OVER_ZR_LE_1_OVER_6"
)

print(
    "RADIAL_CANONICAL_BRAIDING_MAX="
    f"{INV_SQRT_6:.12e}"
)

print(
    "GAIN1000_NECESSARY_MAX_Z_RADIAL="
    f"{gain1000['necessary_maximum_z_radial']:.12e}"
)

print(
    "GAIN1000_REQUIRED_RADIAL_COLLAPSE_FACTOR="
    f"{gain1000['required_radial_collapse_factor_from_unit_margin']:.12e}"
)

print(
    "SOURCE_ALIGNED_NONMONOTONE_FREE_METRIC_GAIN_CLOSED=True"
)

print(
    "SIGN_REVERSED_B_BRANCH_CLOSED=False"
)

print(
    "CANCELLATION_BRANCH_CLOSED=False"
)

print(
    "G4_G5_WBG_CLOSED=False"
)

print(
    "ALTERNATIVE_HIDDEN_SOURCE_CLOSED=False"
)

print(
    "OBLATE_NONLINEAR_SOURCE_CLOSED=False"
)

print(
    "FULL_FINITE_PAYLOAD_CROSSPROP_CERTIFIED=False"
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
    "GLOBAL_RERANK_RECOMMENDED=True"
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
