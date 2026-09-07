"""032V24B — protected Dirac source and universal physical-metric bridge gate.

PURPOSE
-------
V24A established an explicit trace-free Dirac nonmetricity source and a clean
equal-amplitude rest particle/antiparticle witness whose published torsion
response cancels while its nonmetricity response adds.

V24B asks whether the simplest symmetry-protected propagating geometric routes
can actually use that source and deliver a universal neutral-matter metric
response before any PDE, energy optimization, or parameter scan.

CHEAP GATES
-----------
1. Keep the rest-frame SO(3) source decomposition as a diagnostic only.
2. Apply the exact standard Fronsdal spin-3 source Ward identity to the direct
   factorized localized rest-pair source.
3. Preserve compensating currents and more general on-shell Dirac sources if
   the simple direct source fails.
4. Record the symmetry-first dimension-five metric-distortion mixing power
   counting without turning it into a false no-go theorem.
5. Test the published extended-projective pseudoscalar reduced action as a
   direct universal antigravity bridge using a deliberately generous static
   Einstein-stress upper bound at the exact 10-MJ fail boundary.
6. Persist only narrow failure-memory rules.
7. Do not create candidates, rejections, action oracles, or mechanism metrics.

CLAIM_CLASSIFICATION=
THEOREM_LEVEL_SOURCE_COMPATIBILITY_AND_UNIVERSAL_BRIDGE_PREFLIGHT

Outputs:
- results/data/032v24b_protected_dirac_metric_bridge_summary.json
- results/data/032v24b_protected_mode_rerank.csv
- results/data/032v24b_fronsdal_ward_scout.csv
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.protected_dirac_metric_bridge import (
    bms_dimension5_metric_mixing_scout,
    einstein_stress_bridge_bound,
    extended_projective_bridge_gate,
    generic_dirac_algebraic_carrier_witness,
    persist_v24b_region_rules,
    protected_mode_rerank,
    rest_pair_fronsdal_ward_scout,
    rest_pair_so3_screen,
)
from antigravity_research.agminer.storage import (
    Storage,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

V24A = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24a_dirac_hypermomentum_irrep_summary.json"
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
    "032v24b_protected_dirac_metric_bridge_summary.json"
)

ATLAS_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24b_protected_mode_rerank.csv"
)

WARD_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24b_fronsdal_ward_scout.csv"
)

TARGET_J = 1.0e7
TARGET_A = 9.80665
REFERENCE_GAP_M = 0.10


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

if not V24A.exists():
    raise FileNotFoundError(
        str(
            V24A
        )
    )

v24a = json.loads(
    V24A.read_text(
        encoding=
            "utf-8"
    )
)

assert v24a[
    "wheeler_dirac_source"
][
    "explicit_nonmetricity_source_response_exists"
] is True

assert v24a[
    "wheeler_dirac_source"
][
    "weyl_dilation_trace_overlap_zero"
] is True

assert v24a[
    "rest_spinup_pair_witness"
][
    "torsion_response_cancels"
] is True

assert v24a[
    "rest_spinup_pair_witness"
][
    "nonmetricity_response_adds"
] is True

assert v24a[
    "promotion_status"
][
    "blind_parameter_scan_authorized"
] is False

assert v24a[
    "promotion_status"
][
    "universal_physical_metric_bridge_established"
] is False


# ===========================================================================
# 1. REST-PAIR SCREENING AND EXACT FRONSDAL SOURCE GATE
# ===========================================================================

rest = rest_pair_so3_screen()
ward = rest_pair_fronsdal_ward_scout()
generic = generic_dirac_algebraic_carrier_witness()

assert rest[
    "rest_frame_spin1_screen_zero"
] is True

assert rest[
    "rest_frame_spin3_screen_zero"
] is True

assert rest[
    "rest_frame_spin2_carrier_nonzero"
] is True

assert rest[
    "rest_frame_so3_screen_is_exact_pole_projection"
] is False

assert rest[
    "rest_frame_so3_screen_closes_protected_spin1_spin3"
] is False

assert ward[
    "all_tested_spatial_directions_pass"
] is False

assert ward[
    "direct_factorized_localized_rest_pair_without_compensator_closed"
] is True

assert ward[
    "compensating_current_or_more_general_source_closed"
] is False

assert ward[
    "all_massless_spin3_dirac_sources_closed"
] is False

assert generic[
    "algebraic_spin1_carrier_nonzero"
] is True

assert generic[
    "algebraic_spin3_carrier_nonzero"
] is True

assert generic[
    "spinor_is_claimed_on_shell_stationary_source"
] is False


# ===========================================================================
# 2. PROTECTED METRIC-MIXING POWER COUNTING
# ===========================================================================

mixing = bms_dimension5_metric_mixing_scout(
    length_m=
        REFERENCE_GAP_M,
)

assert mixing[
    "metric_distortion_mixing_first_dimension"
] == 5

assert mixing[
    "metric_distortion_mixing_derivative_order"
] == 3

assert mixing[
    "mixing_subleading_in_declared_eft"
] is True

assert mixing[
    "matched_bms_wilson_coefficient_established"
] is False

assert mixing[
    "naturalness_no_go_established"
] is False


# ===========================================================================
# 3. EXTENDED-PROJECTIVE DIRECT UNIVERSAL-BRIDGE GATE
# ===========================================================================

einstein_bound = einstein_stress_bridge_bound(
    energy_j=
        TARGET_J,

    stand_off_gap_m=
        REFERENCE_GAP_M,

    target_acceleration_m_s2=
        TARGET_A,
)

ep = extended_projective_bridge_gate()

assert einstein_bound[
    "acceleration_upper_bound_m_s2"
] < 1.0e-17

assert einstein_bound[
    "target_to_upper_bound_ratio"
] > 1.0e18

assert einstein_bound[
    "uses_exact_10mj_fail_boundary_as_optimistic_supremum"
] is True

assert einstein_bound[
    "nonminimal_metric_portal_closed_by_this_bound"
] is False

assert ep[
    "dirac_motivated_protecting_symmetry"
] is True

assert ep[
    "published_reduced_metric_form"
] == "EINSTEIN_HILBERT_PLUS_CANONICAL_PSEUDOSCALAR"

assert ep[
    "direct_universal_neutral_matter_metric_portal_identified"
] is False

assert ep[
    "universal_bridge_in_declared_reduced_action"
] == "EINSTEIN_STRESS_ENERGY_ONLY"

assert ep[
    "strict_sub10mj_reference_gap_reaches_1g"
] is False

assert ep[
    "declared_ep_pseudoscalar_direct_antigravity_bridge_closed"
] is True

assert ep[
    "all_extended_projective_or_iso_weyl_models_closed"
] is False


# ===========================================================================
# 4. RERANK
# ===========================================================================

atlas = protected_mode_rerank()

atlas_by_branch = {
    row[
        "branch"
    ]:
        row
    for row
    in atlas
}

assert atlas_by_branch[
    "STANDARD_FRONSDAL_F4_SPIN3_DIRECT_REST_PAIR"
][
    "status"
] == "CLOSED_WITHOUT_COMPENSATING_CURRENT"

assert atlas_by_branch[
    "BMS_PROTECTED_TOTALLY_SYMMETRIC_SPIN1_ONSHELL_DIRAC"
][
    "status"
] == "HIGHEST_PRIORITY_OPEN_PROTECTED_TS_ROUTE"

assert atlas_by_branch[
    "BARKER_ZELL_EXTENDED_PROJECTIVE_PSEUDOSCALAR"
][
    "status"
] == "CLOSED_AS_DECLARED_DIRECT_SUB10MJ_UNIVERSAL_BRIDGE"

assert atlas_by_branch[
    "BROADER_HOOK_OR_MIXED_SYMMETRY_MAG_WITH_PROTECTED_LOWER_SPIN_METRIC_ACTIVE_MODE"
][
    "status"
] == "OPEN_NEW_ACTION_REQUIRED"


# ===========================================================================
# 5. AGMINER FAILURE MEMORY ONLY
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

    inserted_rules = persist_v24b_region_rules(
        storage,
        energy_policy_id=
            str(
                policy[
                    "policy_id"
                ]
            ),
    )

    metadata = {
        "032v24b_rest_pair_so3_spin1_screen":
            "0",

        "032v24b_rest_pair_so3_spin3_screen":
            "0",

        "032v24b_so3_screen_is_hard_exclusion":
            "0",

        "032v24b_rest_pair_direct_fronsdal_spin3_ward_pass":
            "0",

        "032v24b_fronsdal_compensating_current_closed":
            "0",

        "032v24b_generic_dirac_spin1_algebraic_carrier":
            "1",

        "032v24b_generic_dirac_spin3_algebraic_carrier":
            "1",

        "032v24b_bms_exact_spin1_source_constraint_established":
            "0",

        "032v24b_bms_universal_metric_bridge_established":
            "0",

        "032v24b_ep_pseudoscalar_direct_sub10mj_bridge":
            "0",

        "agminer_next_family":
            "ON_SHELL_DIRAC_PROTECTED_SPIN1_SOURCE_WARD_AND_METRIC_BRIDGE",
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
    assert after[
        table
    ] == before[
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
# 6. PERSISTENT OUTPUTS
# ===========================================================================

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

fields = sorted(
    {
        key
        for row
        in atlas
        for key
        in row
    }
)

with ATLAS_OUT.open(
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
        atlas
    )


ward_rows = []

for name, row in ward[
    "direction_results"
].items():
    ward_rows.append(
        {
            "direction":
                name,

            "kx":
                row[
                    "spatial_wavevector"
                ][
                    0
                ],

            "ky":
                row[
                    "spatial_wavevector"
                ][
                    1
                ],

            "kz":
                row[
                    "spatial_wavevector"
                ][
                    2
                ],

            "normalized_ward_residual":
                row[
                    "normalized_ward_residual"
                ],

            "standard_fronsdal_source_ward_pass":
                row[
                    "standard_fronsdal_source_ward_pass"
                ],
        }
    )

with WARD_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                ward_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        ward_rows
    )


decision = (
    "RED_PARTIAL_032V24B_DIRECT_REST_PAIR_FRONSDAL_SPIN3_REQUIRES_"
    "COMPENSATOR__EP_PSEUDOSCALAR_DIRECT_UNIVERSAL_BRIDGE_STRESS_"
    "ONLY_FAILS_SUB10MJ__PROTECTED_SPIN1_ONSHELL_DIRAC_AND_BROADER_"
    "MAG_REMAIN_OPEN"
)

next_step = (
    "032V24C_ONSHELL_DIRAC_PROTECTED_SPIN1_SOURCE_WARD_"
    "AND_UNIVERSAL_METRIC_BRIDGE_GATE"
)

summary = {
    "branch":
        "032V24B_PROTECTED_DIRAC_METRIC_BRIDGE_GATE",

    "energy_policy": {
        "policy_id":
            str(
                policy[
                    "policy_id"
                ]
            ),

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

    "v24a_provenance": {
        "explicit_tracefree_dirac_nonmetricity":
            True,

        "torsion_cancelled_rest_pair_witness":
            True,

        "universal_metric_bridge_pre_v24b":
            False,
    },

    "rest_pair_so3_screen":
        rest,

    "rest_pair_fronsdal_ward_gate":
        ward,

    "generic_dirac_algebraic_witness":
        generic,

    "bms_dimension5_metric_mixing_scout":
        mixing,

    "einstein_stress_only_reference_bound":
        einstein_bound,

    "extended_projective_pseudoscalar_gate":
        ep,

    "protected_mode_rerank":
        atlas,

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

        "rest_so3_screen_is_exact_pole_projection":
            False,

        "direct_rest_pair_fronsdal_spin3_source_compatible":
            False,

        "fronsdal_compensating_current_closed":
            False,

        "exact_protected_spin1_source_constraint_established":
            False,

        "universal_physical_metric_bridge_established":
            False,

        "source_charge_per_joule_established":
            False,

        "outward_sign_established":
            False,

        "finite_payload_response_established":
            False,

        "complete_operating_energy_established":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,
    },

    "closed_now": [
        "WHEELER_REST_PAIR_TIMES_SINGLE_LOCALIZED_ENVELOPE_DIRECT_TO_STANDARD_FRONSDAL_SPIN3_WITHOUT_COMPENSATING_CURRENT",
        "BARKER_ZELL_2024_EP_PSEUDOSCALAR_AS_DIRECT_SUB10MJ_UNIVERSAL_METRIC_BRIDGE_WITHOUT_ADDED_PORTAL",
    ],

    "explicitly_open": [
        "PROTECTED_TOTALLY_SYMMETRIC_SPIN1_WITH_EXACT_ONSHELL_DIRAC_SOURCE_CONSTRAINT",
        "FRONSDAL_OR_OTHER_PROTECTED_SPIN3_WITH_COMPENSATING_OR_MORE_GENERAL_WARD_COMPATIBLE_SOURCE",
        "BROADER_HOOK_OR_MIXED_SYMMETRY_MAG_WITH_PROTECTED_LOWER_SPIN_METRIC_ACTIVE_MODE",
        "NEW_EP_OR_IW_EXTENSION_ONLY_IF_IT_ADDS_A_GENUINELY_UNIVERSAL_PHYSICAL_METRIC_PORTAL",
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
# 7. COMPACT TERMINAL REPORT
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
    "REST_PAIR_SO3_SPIN1_SCREEN_ZERO="
    +
    str(
        rest[
            "rest_frame_spin1_screen_zero"
        ]
    )
)

print(
    "REST_PAIR_SO3_SPIN3_SCREEN_ZERO="
    +
    str(
        rest[
            "rest_frame_spin3_screen_zero"
        ]
    )
)

print(
    "SO3_SCREEN_IS_HARD_EXCLUSION=False"
)

print(
    "REST_PAIR_SPIN2_SCREEN_CARRIER_NONZERO="
    +
    str(
        rest[
            "rest_frame_spin2_carrier_nonzero"
        ]
    )
)

print(
    "FRONSDAL_REST_PAIR_X_WARD_PASS="
    +
    str(
        ward[
            "direction_results"
        ][
            "x"
        ][
            "standard_fronsdal_source_ward_pass"
        ]
    )
)

print(
    "FRONSDAL_REST_PAIR_Y_WARD_PASS="
    +
    str(
        ward[
            "direction_results"
        ][
            "y"
        ][
            "standard_fronsdal_source_ward_pass"
        ]
    )
)

print(
    "FRONSDAL_REST_PAIR_Z_WARD_PASS="
    +
    str(
        ward[
            "direction_results"
        ][
            "z"
        ][
            "standard_fronsdal_source_ward_pass"
        ]
    )
)

print(
    "FRONSDAL_MAX_NORMALIZED_WARD_RESIDUAL="
    f"{ward['maximum_normalized_ward_residual']:.12e}"
)

print(
    "DIRECT_REST_PAIR_FRONSDAL_WITHOUT_COMPENSATOR_CLOSED=True"
)

print(
    "FRONSDAL_COMPENSATING_CURRENT_CLOSED=False"
)

print(
    "FULL_DIRAC_SOURCE_FAMILY_CLOSED=False"
)

print(
    "GENERIC_DIRAC_ALGEBRAIC_SPIN1_CARRIER_NONZERO="
    +
    str(
        generic[
            "algebraic_spin1_carrier_nonzero"
        ]
    )
)

print(
    "GENERIC_DIRAC_ALGEBRAIC_SPIN3_CARRIER_NONZERO="
    +
    str(
        generic[
            "algebraic_spin3_carrier_nonzero"
        ]
    )
)

print(
    "GENERIC_DIRAC_WITNESS_ONSHELL=False"
)

print(
    "BMS_FIRST_METRIC_DISTORTION_MIXING_DIMENSION=5"
)

print(
    "BMS_FIRST_METRIC_DISTORTION_MIXING_DERIVATIVE_ORDER=3"
)

print(
    "BMS_NATURAL_DIM5_MIXING_AT_10CM="
    f"{mixing['natural_dimension5_mixing_ratio']:.12e}"
)

for row in mixing[
    "target_rows"
]:
    if math.isclose(
        row[
            "target_mixing"
        ],
        1.0e-3,
    ):
        print(
            "BMS_WILSON_REQUIRED_FOR_1E3_MIXING="
            f"{row['required_dimensionless_wilson']:.12e}"
        )

    if math.isclose(
        row[
            "target_mixing"
        ],
        1.0e-1,
    ):
        print(
            "BMS_WILSON_REQUIRED_FOR_1E1_MIXING="
            f"{row['required_dimensionless_wilson']:.12e}"
        )

print(
    "BMS_MIXING_NATURALNESS_NO_GO_ESTABLISHED=False"
)

print(
    "EP_DIRAC_MOTIVATED_PROTECTION=True"
)

print(
    "EP_REDUCED_METRIC_FORM=EINSTEIN_PLUS_CANONICAL_PSEUDOSCALAR"
)

print(
    "EP_NEW_DIRECT_UNIVERSAL_PHYSICAL_METRIC_PORTAL_IDENTIFIED=False"
)

print(
    "STRESS_ONLY_10MJ_10CM_ACCEL_UPPER_BOUND_M_S2="
    f"{einstein_bound['acceleration_upper_bound_m_s2']:.12e}"
)

print(
    "STRESS_ONLY_TARGET_GAP="
    f"{einstein_bound['target_to_upper_bound_ratio']:.12e}"
)

print(
    "STRESS_ONLY_REQUIRED_ENERGY_J="
    f"{einstein_bound['energy_required_at_same_bound_j']:.12e}"
)

print(
    "EP_PSEUDOSCALAR_DECLARED_DIRECT_SUB10MJ_BRIDGE_CLOSED=True"
)

print(
    "ALL_EXTENDED_PROJECTIVE_MODELS_CLOSED=False"
)

print(
    "PROTECTED_SPIN1_ONSHELL_DIRAC_CLOSED=False"
)

print(
    "BROADER_HOOK_MIXED_MAG_CLOSED=False"
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
