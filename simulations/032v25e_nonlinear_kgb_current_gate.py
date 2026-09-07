"""032V25E — nonlinear KGB source-current / canonical-response gate.

V25D closed constant large K_X as a free fixed-source rescue.

V25E derives the exact static spherical G2+G3 shift-current Jacobian and
classifies monotone versus non-monotone nonlinear response.

No arbitrary K(X),G3(X) blind scan is performed.

CLAIM_CLASSIFICATION=
NONLINEAR_SHIFT_CURRENT_JACOBIAN_AND_STATIC_CANONICAL_RESPONSE_FALSIFICATION
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.nonlinear_kgb_current_gate import (
    local_static_response,
    monotone_source_aligned_theorem,
    persist_v25e_metadata,
    persist_v25e_region_rule,
    pure_k_linear_in_s,
    required_static_margin_for_response_gain,
    v25e_gate,
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

V25D = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25d_kx_source_reaction_summary.json"
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
    "032v25e_nonlinear_kgb_current_summary.json"
)

MONOTONE_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25e_monotone_current_scan.csv"
)

NONMONOTONE_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25e_nonmonotone_kx_branch_scan.csv"
)

GAIN_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25e_response_gain_margin_scan.csv"
)


TARGET_J = 1.0e7


# ===========================================================================
# 0. POLICY / V25D PROVENANCE
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


if not V25D.exists():
    raise FileNotFoundError(
        str(
            V25D
        )
    )


v25d = json.loads(
    V25D.read_text(
        encoding="utf-8"
    )
)


promotion_d = v25d[
    "promotion_status"
]


assert promotion_d[
    "large_constant_kx_fixed_source_rescue_closed"
] is True

assert promotion_d[
    "nonlinear_kxx_closed"
] is False

assert promotion_d[
    "nonlinear_g3xx_closed"
] is False

assert promotion_d[
    "action_oracle_authorized"
] is False


# ===========================================================================
# 1. MONOTONE SOURCE-ALIGNED THEOREM SCOUT
# ===========================================================================

monotone_rows = []

for a_s in (
    0.0,
    0.1,
    0.5,
    1.0,
):
    for b_value in (
        0.0,
        0.1,
        0.5,
    ):
        for b_s in (
            0.0,
            0.2,
        ):
            row = (
                monotone_source_aligned_theorem(
                    u=
                        1.0,

                    radius=
                        2.0,

                    a_value=
                        1.0
                        +
                        0.5
                        *
                        a_s,

                    a_s=
                        a_s,

                    b_value=
                        b_value,

                    b_s=
                        b_s,
                )
            )

            monotone_rows.append(
                {
                    "a_s":
                        a_s,

                    "b_value":
                        b_value,

                    "b_s":
                        b_s,

                    **row,
                }
            )


assert all(
    row[
        "monotone_branch_cannot_antiscreen_source_current"
    ]
    for row
    in monotone_rows
)


assert all(
    row[
        "elasticity"
    ]
    >=
    1.0
    for row
    in monotone_rows
)


# ===========================================================================
# 2. NON-MONOTONE PURE-K WITNESS
# ===========================================================================

nonmonotone_rows = []

for alpha in (
    0.0,
    0.2,
    0.4,
    0.5,
    0.6,
    0.65,
    0.66,
    0.665,
    0.666,
    2.0 / 3.0,
    0.67,
):
    row = (
        pure_k_linear_in_s(
            alpha=
                alpha,
        )
    )

    nonmonotone_rows.append(
        row
    )


alpha_066 = next(
    row
    for row
    in nonmonotone_rows
    if abs(
        row[
            "alpha"
        ]
        -
        0.66
    )
    <
    1.0e-14
)


assert abs(
    alpha_066[
        "jacobian"
    ]
    -
    0.01
) < 2.0e-15


assert abs(
    alpha_066[
        "response_gain_over_canonical_baseline"
    ]
    -
    100.0
) < 1.0e-10


# ===========================================================================
# 3. RESPONSE-GAIN / STATIC-MARGIN SCAN
# ===========================================================================

gain_rows = [
    required_static_margin_for_response_gain(
        gain
    )
    for gain
    in (
        1.0,
        3.0,
        10.0,
        100.0,
        1000.0,
        10000.0,
    )
]


gain_1000 = next(
    row
    for row
    in gain_rows
    if row[
        "response_gain"
    ]
    ==
    1000.0
)


assert (
    gain_1000[
        "required_static_radial_jacobian"
    ]
    ==
    1.0e-3
)


# ===========================================================================
# 4. CLAIM GATE
# ===========================================================================

gate = (
    v25e_gate()
)


assert gate[
    "monotone_source_aligned_no_antiscreen_theorem"
] is True

assert gate[
    "nonmonotone_source_response_algebraically_possible"
] is True

assert gate[
    "large_response_requires_small_static_jacobian"
] is True

assert gate[
    "nonmonotone_kxx_closed"
] is False

assert gate[
    "nonmonotone_g3xx_closed"
] is False

assert gate[
    "metric_braiding_numerator_analyzed"
] is False

assert gate[
    "full_tensor_stability_certified"
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
        persist_v25e_region_rule(
            storage
        )
    )

    persist_v25e_metadata(
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
    MONOTONE_OUT,
    monotone_rows,
)

write_rows(
    NONMONOTONE_OUT,
    nonmonotone_rows,
)

write_rows(
    GAIN_OUT,
    gain_rows,
)


summary = {
    "branch":
        "032V25E_NONLINEAR_KGB_SOURCE_CURRENT_GATE",

    "claim_class":
        (
            "NONLINEAR_SHIFT_CURRENT_JACOBIAN_AND_"
            "STATIC_CANONICAL_RESPONSE_FALSIFICATION"
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

    "v25d_provenance": {
        "large_constant_kx_fixed_source_closed":
            True,

        "nonlinear_kxx_open_pre_v25e":
            True,

        "nonlinear_g3xx_open_pre_v25e":
            True,
    },

    "exact_current_structure": {
        "source_aligned_current":
            "F=u*A(s)+2*u^2*B(s)/r",

        "s":
            "u^2/2=-X",

        "source_charge":
            "Q=4*pi*r^2*F",

        "current_jacobian":
            (
                "D=A+u^2*A_s+4*u*B/r+2*u^3*B_s/r"
            ),

        "static_source_susceptibility":
            "du/dQ=1/(4*pi*r^2*D)",
    },

    "monotone_theorem": {
        "assumptions":
            [
                "A>0",
                "A_s>=0",
                "B>=0",
                "B_s>=0",
            ],

        "identity":
            (
                "D-F/u="
                "u^2*A_s+2*u*B/r+2*u^3*B_s/r"
            ),

        "conclusion":
            "u*D/F>=1",

        "source_current_antiscreening":
            False,
    },

    "nonmonotone_witness": {
        "physical_model":
            False,

        "family":
            "PURE_K_A_EQUALS_1_MINUS_ALPHA_S",

        "alpha_066_jacobian":
            alpha_066[
                "jacobian"
            ],

        "alpha_066_response_gain":
            alpha_066[
                "response_gain_over_canonical_baseline"
            ],

        "interpretation":
            (
                "ANTISCREENING_IS_ALGEBRAICALLY_POSSIBLE_"
                "BUT_LARGE_RESPONSE_APPROACHES_CURRENT_JACOBIAN_ZERO"
            ),
    },

    "gain1000_margin": {
        "required_static_radial_jacobian":
            gain_1000[
                "required_static_radial_jacobian"
            ],

        "radial_static_canonical_source_coupling_relative":
            gain_1000[
                "radial_static_canonical_source_coupling_relative"
            ],

        "full_dynamic_stability_certified":
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
        "monotone_source_current_antiscreen_closed":
            True,

        "nonmonotone_kxx_closed":
            False,

        "nonmonotone_g3xx_closed":
            False,

        "metric_braiding_numerator_analyzed":
            False,

        "full_tensor_stability_certified":
            False,

        "oblate_source_solution_solved":
            False,

        "full_source_rg_uv_certified":
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
    "V25D_CONSTANT_KX_CLOSURE_PRESERVED=True"
)

print(
    "EXACT_STATIC_SPHERICAL_G2_G3_SHIFT_CURRENT_USED=True"
)

print(
    "SOURCE_CURRENT_FORM=F_EQUALS_U_A_PLUS_2_U2_B_OVER_R"
)

print(
    "SOURCE_CHARGE_FORM=Q_EQUALS_4PI_R2_F"
)

print(
    "CURRENT_JACOBIAN_FORM=D_EQUALS_A_PLUS_U2_AS_PLUS_4UB_OVER_R_PLUS_2U3BS_OVER_R"
)

print(
    "MONOTONE_SOURCE_ALIGNED_NO_ANTISCREEN_THEOREM=True"
)

print(
    "MONOTONE_CURRENT_ELASTICITY_MIN_GE_1=True"
)

print(
    "NONMONOTONE_SOURCE_RESPONSE_ALGEBRAICALLY_POSSIBLE=True"
)

print(
    "PURE_K_ALPHA066_STATIC_JACOBIAN="
    f"{alpha_066['jacobian']:.12e}"
)

print(
    "PURE_K_ALPHA066_RESPONSE_GAIN="
    f"{alpha_066['response_gain_over_canonical_baseline']:.12e}"
)

print(
    "GAIN1000_REQUIRED_STATIC_RADIAL_JACOBIAN="
    f"{gain_1000['required_static_radial_jacobian']:.12e}"
)

print(
    "GAIN1000_RADIAL_CANONICAL_SOURCE_COUPLING_RELATIVE="
    f"{gain_1000['radial_static_canonical_source_coupling_relative']:.12e}"
)

print(
    "LARGE_RESPONSE_APPROACHES_STATIC_CURRENT_DEGENERACY=True"
)

print(
    "NONMONOTONE_KXX_CLOSED=False"
)

print(
    "NONMONOTONE_G3XX_CLOSED=False"
)

print(
    "METRIC_BRAIDING_NUMERATOR_ANALYZED=False"
)

print(
    "FULL_TENSOR_STABILITY_CERTIFIED=False"
)

print(
    "OBLATE_SOURCE_SOLUTION_SOLVED=False"
)

print(
    "FULL_SOURCE_RG_UV_CERTIFIED=False"
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
