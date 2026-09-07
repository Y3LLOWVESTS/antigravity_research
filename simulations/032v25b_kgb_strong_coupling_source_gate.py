"""032V25B — minimal-cubic KGB source-scale / strong-coupling gate.

PURPOSE
-------
V25A established an explicit active-state KGB action but did not establish
whether the historical hidden-axial source can inhabit a controlled KGB
background.

V25B cross-checks the historical V16 selected loop-0.30 source scale against
the local canonically normalized cubic fluctuation scale.

This is deliberately a cheap falsification before:

- a new KGB hidden-source PDE;
- full tensor Horndeski projection;
- RG/UV matching;
- finite-payload gravity;
- source optimization;
- energy optimization.

A RED result closes only the unchanged V16 -> minimal cubic KGB transplant.

CLAIM_CLASSIFICATION=
LOCAL_CANONICAL_CUBIC_EFT_AND_HISTORICAL_SOURCE_SCALE_FALSIFICATION
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.kgb_strong_coupling_source_gate import (
    V16_B_AXIAL_EV,
    V16_CUTOFF_EV,
    V16_F_PSI_EV,
    V16_HARD_MARGIN,
    V16_M_PSI_EV,
    V16_MU_EV,
    V16_SOURCE_A_M,
    V16_SOURCE_C_M,
    cubic_scale_from_gradient_y,
    gain_to_y,
    historical_source_compatibility,
    local_canonical_cubic_scale,
    persist_v25b_metadata,
    persist_v25b_region_rule,
    positive_2x2_mixing_diagnostics,
    protection_rg_scope,
    required_gradient_for_control,
    v25b_gate,
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


V25A = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25a_active_state_kgb_action_summary.json"
)

V15 = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v15_axial_shift_source_morphology_summary.json"
)

V16 = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v16_axial_dirac_meanfield_self_consistency_summary.json"
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
    "032v25b_kgb_strong_coupling_source_summary.json"
)

GAIN_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25b_kgb_gain_control_scan.csv"
)

REQUIRED_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25b_kgb_required_gradient_scan.csv"
)

MIXING_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25b_quadratic_mixing_health_scan.csv"
)


TARGET_J = 1.0e7


# ===========================================================================
# 0. POLICY / PROVENANCE
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


for path in (
    V25A,
    V15,
    V16,
):
    if not path.exists():
        raise FileNotFoundError(
            str(
                path
            )
        )


v25a = json.loads(
    V25A.read_text(
        encoding="utf-8"
    )
)

v15 = json.loads(
    V15.read_text(
        encoding="utf-8"
    )
)

v16 = json.loads(
    V16.read_text(
        encoding="utf-8"
    )
)


assert v25a[
    "promotion_status"
][
    "explicit_action_exists"
] is True

assert v25a[
    "promotion_status"
][
    "action_oracle_authorized"
] is False

assert v25a[
    "promotion_status"
][
    "blind_parameter_scan_authorized"
] is False

assert v25a[
    "promotion_status"
][
    "full_tensor_nonremovable_crosspropagator_certified"
] is False


# ===========================================================================
# 1. RECONSTRUCT HISTORICAL V15/V16 SOURCE SCALE
# ===========================================================================

morphology = v15[
    "optimized_morphology"
]

selected = v16[
    "selected_positive_band_partial_corridor"
]


pairs = (
    (
        float(
            morphology[
                "a_m"
            ]
        ),
        V16_SOURCE_A_M,
    ),
    (
        float(
            morphology[
                "c_m"
            ]
        ),
        V16_SOURCE_C_M,
    ),
    (
        float(
            selected[
                "f_psi_ev"
            ]
        ),
        V16_F_PSI_EV,
    ),
    (
        float(
            selected[
                "axial_b_ev"
            ]
        ),
        V16_B_AXIAL_EV,
    ),
    (
        float(
            selected[
                "m_psi_ev"
            ]
        ),
        V16_M_PSI_EV,
    ),
    (
        float(
            selected[
                "chemical_potential_ev"
            ]
        ),
        V16_MU_EV,
    ),
    (
        float(
            selected[
                "nda_cutoff_ev"
            ]
        ),
        V16_CUTOFF_EV,
    ),
    (
        float(
            selected[
                "hard_scale_margin"
            ]
        ),
        V16_HARD_MARGIN,
    ),
)


for observed, expected in pairs:
    assert (
        abs(
            observed
            /
            expected
            -
            1.0
        )
        <
        2.0e-12
    )


compatibility = (
    historical_source_compatibility()
)

gate = (
    v25b_gate()
)

protection = (
    protection_rg_scope()
)


assert gate[
    "unchanged_v16_minimal_cubic_transplant_closed"
] is True

assert gate[
    "generalized_kx_g3_closed"
] is False

assert gate[
    "wbg_multiscale_kgb_closed"
] is False


# ===========================================================================
# 2. GAIN / LOCAL CUBIC CONTROL SCAN
# ===========================================================================

gain_rows = []

for gain in (
    1.0e-5,
    1.0e-4,
    1.0e-3,
    1.0e-2,
    1.0e-1,
    1.0,
    10.0,
    1000.0,
):
    y = gain_to_y(
        gain
    )

    lambda_3 = (
        cubic_scale_from_gradient_y(
            gradient_ev2=
                compatibility[
                    "gradient_ev2"
                ],

            y=
                y,
        )
    )

    lambda_eff = (
        local_canonical_cubic_scale(
            gradient_ev2=
                compatibility[
                    "gradient_ev2"
                ],

            y=
                y,
        )
    )

    ratio = (
        lambda_eff
        /
        compatibility[
            "source_variation_momentum_ev"
        ]
    )

    gain_rows.append(
        {
            "gain_times_planck":
                gain,

            "y":
                y,

            "z_min":
                1.0
                -
                y,

            "lambda3_ev":
                lambda_3,

            "lambda_eff_ev":
                lambda_eff,

            "source_k_ev":
                compatibility[
                    "source_variation_momentum_ev"
                ],

            "lambda_eff_over_k":
                ratio,

            "local_control_pass":
                ratio
                >=
                1.0,
        }
    )


assert (
    next(
        row
        for row
        in gain_rows
        if row[
            "gain_times_planck"
        ]
        ==
        1.0e-3
    )[
        "lambda_eff_over_k"
    ]
    <
    0.20
)


# ===========================================================================
# 3. REQUIRED GRADIENT / AXIAL-SCALE SCAN
# ===========================================================================

required_rows = []

for margin in (
    1.0,
    5.0,
):
    for gain in (
        1.0e-3,
        1.0e-2,
        1.0e-1,
        1.0,
        10.0,
        1000.0,
    ):
        required_gradient = (
            required_gradient_for_control(
                length_m=
                    compatibility[
                        "source_c_m"
                    ],

                gain_times_planck=
                    gain,

                control_margin=
                    margin,
            )
        )

        required_rows.append(
            {
                "control_margin":
                    margin,

                "gain_times_planck":
                    gain,

                "required_gradient_ev2":
                    required_gradient,

                "required_b_at_historical_fpsi_ev":
                    (
                        required_gradient
                        /
                        compatibility[
                            "f_psi_ev"
                        ]
                    ),

                "historical_gradient_ratio_required_over_actual":
                    (
                        required_gradient
                        /
                        compatibility[
                            "gradient_ev2"
                        ]
                    ),
            }
        )


# ===========================================================================
# 4. GENERAL POSITIVE 2x2 MIXING IDENTITY
# ===========================================================================

mixing_rows = []

for rho in (
    0.0,
    0.1,
    0.5,
    0.9,
    0.99,
    0.999,
):
    result = (
        positive_2x2_mixing_diagnostics(
            metric_kinetic=
                1.0,

            scalar_kinetic=
                1.0,

            mixing=
                rho,
        )
    )

    mixing_rows.append(
        {
            "input_rho":
                rho,

            **result,
        }
    )


assert all(
    row[
        "healthy"
    ]
    for row
    in mixing_rows
)

assert all(
    (
        row[
            "normalized_inverse_cross"
        ]
        is not None
        and
        row[
            "normalized_inverse_cross"
        ]
        <
        1.0
    )
    or
    row[
        "input_rho"
    ]
    ==
    0.0
    for row
    in mixing_rows
)


# ===========================================================================
# 5. AGMINER FAILURE MEMORY
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
        persist_v25b_region_rule(
            storage
        )
    )

    persist_v25b_metadata(
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
        GAIN_OUT,
        gain_rows,
    ),
    (
        REQUIRED_OUT,
        required_rows,
    ),
    (
        MIXING_OUT,
        mixing_rows,
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
        "032V25B_KGB_STRONG_COUPLING_SOURCE_GATE",

    "claim_class":
        (
            "LOCAL_CANONICAL_CUBIC_EFT_AND_"
            "HISTORICAL_SOURCE_SCALE_FALSIFICATION"
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

    "v25a_provenance": {
        "explicit_action_exists":
            True,

        "preserved":
            True,
    },

    "historical_v16_source_compatibility":
        compatibility,

    "protection_rg_scope":
        protection,

    "quadratic_mixing_bound": {
        "identity":
            (
                "ABS_G12_OVER_SQRT_G11_G22_"
                "EQUALS_ABS_RHO_LT1_FOR_POSITIVE_2X2_KINETIC_BLOCK"
            ),

        "full_kgb_no_go":
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
        "unchanged_v16_minimal_cubic_transplant_closed":
            True,

        "generalized_kgb_closed":
            False,

        "wbg_multiscale_kgb_closed":
            False,

        "full_tensor_nonremovable_crosspropagator_certified":
            False,

        "full_source_rg_uv_certified":
            False,

        "new_selfconsistent_kgb_hidden_source_solved":
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
    "V25A_EXPLICIT_ACTION_PRESERVED=True"
)

print(
    "V16_HISTORICAL_SOURCE_IS_CURRENT_PHYSICAL_MODEL=False"
)

print(
    "V16_HISTORICAL_GRADIENT_EV2="
    f"{compatibility['gradient_ev2']:.12e}"
)

print(
    "V16_SOURCE_MOMENTUM_EV="
    f"{compatibility['source_variation_momentum_ev']:.12e}"
)

print(
    "V16_A1E3_LAMBDA_EFF_OVER_K="
    f"{compatibility['a1e3_lambda_eff_over_source_k']:.12e}"
)

print(
    "V16_ACTUAL_GRADIENT_MAX_CONTROLLED_A="
    f"{compatibility['actual_gradient_max_controlled_gain_times_planck']:.12e}"
)

print(
    "V16_HARD_MARGIN_PROXY_MAX_CONTROLLED_A="
    f"{compatibility['hard_margin_proxy_max_controlled_gain_times_planck']:.12e}"
)

print(
    "V16_RELAXED_CUTOFF_MAX_CONTROLLED_A="
    f"{compatibility['relaxed_cutoff_max_controlled_gain_times_planck']:.12e}"
)

print(
    "V16_HARD_MARGIN_PROXY_MARGIN5_MAX_A="
    f"{compatibility['hard_margin_proxy_margin5_max_gain_times_planck']:.12e}"
)

print(
    "V16_RELAXED_CUTOFF_MARGIN5_MAX_A="
    f"{compatibility['relaxed_cutoff_margin5_max_gain_times_planck']:.12e}"
)

print(
    "UNCHANGED_V16_TO_MINIMAL_CUBIC_KGB_TRANSPLANT_CLOSED=True"
)

print(
    "GENERALIZED_KGB_CLOSED=False"
)

print(
    "WBG_MULTISCALE_KGB_CLOSED=False"
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
    "NEW_SELFCONSISTENT_KGB_HIDDEN_SOURCE_SOLVED=False"
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
