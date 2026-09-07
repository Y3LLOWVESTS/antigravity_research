"""032V25A — explicit active-state KGB action-existence gate.

V25 promoted the A1 design requirement:

    intrinsic high-charge source
        ->
    protected active-state portal
        ->
    one universal physical metric
        ->
    non-removable physical cross response.

V25A constructs the simplest concrete covariant action found that satisfies
this architecture structurally:

    cubic shift-symmetric Horndeski / kinetic gravity braiding
        +
    the historical hidden axial derivative source.

The run also derives the minimal cubic gain-vs-kinetic-margin relation.

It does NOT optimize parameters or create an action oracle.

CLAIM_CLASSIFICATION=
EXPLICIT_ACTION_EXISTENCE_AND_ACTIVE_OFFSTATE_BRAIDING_PREFLIGHT
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.active_state_kgb_action import (
    action_specification,
    active_offstate_cross_response_demo,
    off_state_tree_gate,
    persist_v25a_metadata,
    protection_gate,
    quadratic_cross_response_invariance,
    required_state_for_canonical_gain,
    source_and_conservation_gate,
    static_spacelike_state,
    v25a_action_existence_gate,
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

V25 = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v25_nonremovable_crosspropagator_rerank_summary.json"
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
    "032v25a_active_state_kgb_action_summary.json"
)

STATE_SCAN_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25a_minimal_cubic_kgb_state_scan.csv"
)

GAIN_SCAN_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25a_canonical_gain_margin_scan.csv"
)

CROSS_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v25a_cross_response_field_redefinition_scan.csv"
)

TARGET_J = 1.0e7


# ============================================================
# 0. POLICY / V25 PROVENANCE
# ============================================================

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


if not V25.exists():
    raise FileNotFoundError(
        str(
            V25
        )
    )


v25 = json.loads(
    V25.read_text(
        encoding="utf-8"
    )
)


assert v25[
    "a1_design_target"
][
    "name"
] == (
    "INTRINSIC_SOURCE_ACTIVE_STATE_UNIVERSAL_METRIC_SYNTHESIS"
)

assert v25[
    "a1_design_target"
][
    "is_physical_model"
] is False

assert v25[
    "promotion_status"
][
    "action_oracle_authorized"
] is False

assert v25[
    "promotion_status"
][
    "blind_parameter_scan_authorized"
] is False

assert v25[
    "promotion_status"
][
    "nonremovable_crosspropagator_model_identified"
] is False


# ============================================================
# 1. EXPLICIT ACTION
# ============================================================

action = action_specification()
offstate = off_state_tree_gate()
source = source_and_conservation_gate()
protection = protection_gate()
gate = v25a_action_existence_gate()


assert action[
    "one_universal_physical_metric"
] is True

assert action[
    "ordinary_matter_minimally_coupled"
] is True

assert action[
    "exact_constant_shift_symmetry"
] is True

assert action[
    "direct_v17_c1_matter_operator_present"
] is False

assert action[
    "tree_level_r5_same_operator_present"
] is False


assert offstate[
    "tree_level_active_offstate_separation"
] is True

assert offstate[
    "r5_same_tree_operator_absent"
] is True

assert offstate[
    "offstate_empirical_closure"
] is False


assert source[
    "hidden_axial_derivative_source_operator_exists"
] is True

assert source[
    "new_kgb_static_selfconsistent_source_solved"
] is False

assert source[
    "full_metric_scalar_hidden_source_conservation_solved"
] is False


# ============================================================
# 2. MINIMAL CUBIC STATIC-GRADIENT SCAN
# ============================================================

state_y_values = (
    0.0,
    0.01,
    0.10,
    0.25,
    0.50,
    2.0 / 3.0,
    0.90,
    0.99,
    0.999,
    1.0,
    1.01,
)

state_rows = []

for y in state_y_values:
    row = static_spacelike_state(
        y
    )

    state_rows.append(
        row
    )


assert state_rows[
    0
][
    "active_debraided_matter_coupling_nonzero"
] is False

assert static_spacelike_state(
    0.10
)[
    "hyperbolic_principal_part"
] is True

assert static_spacelike_state(
    1.0
)[
    "hyperbolic_principal_part"
] is False


# ============================================================
# 3. CANONICAL GAIN / KINETIC-MARGIN THEOREM
# ============================================================

gain_values = (
    0.0,
    0.1,
    1.0,
    3.0,
    10.0,
    100.0,
    1000.0,
    10000.0,
)

gain_rows = []

for gain in gain_values:
    row = required_state_for_canonical_gain(
        gain
    )

    gain_rows.append(
        row
    )


gain_10 = required_state_for_canonical_gain(
    10.0
)

gain_1000 = required_state_for_canonical_gain(
    1000.0
)


assert abs(
    gain_10[
        "required_z_time_margin"
    ]
    -
    1.0
    /
    201.0
) < 1.0e-14


assert gain_1000[
    "required_z_time_margin"
] < 5.1e-7

assert gain_1000[
    "near_kinetic_degeneracy"
] is True


# ============================================================
# 4. FIELD-REDEFINITION RESPONSE INVARIANCE
# ============================================================

mixing_values = (
    0.0,
    0.05,
    0.10,
    0.25,
    0.50,
    0.80,
)

cross_rows = []

for mixing in mixing_values:
    result = quadratic_cross_response_invariance(
        metric_kinetic=
            1.0,

        scalar_kinetic=
            1.0,

        mixing=
            mixing,
    )

    cross_rows.append(
        {
            "mixing":
                mixing,

            **result,
        }
    )


for row in cross_rows:
    assert row[
        "healthy_quadratic_channel"
    ] is True

    assert row[
        "relative_error"
    ] < 1.0e-12


active_offstate = active_offstate_cross_response_demo()

assert active_offstate[
    "offstate_zero"
] is True

assert active_offstate[
    "active_nonzero"
] is True

assert active_offstate[
    "active_response_field_redefinition_invariant"
] is True


# ============================================================
# 5. CLAIM BOUNDARIES
# ============================================================

assert protection[
    "full_source_coupled_naturalness_certified"
] is False

assert gate[
    "explicit_covariant_action_exists"
] is True

assert gate[
    "full_tensor_nonremovable_crosspropagator_certified"
] is False

assert gate[
    "new_action_source_solution_exists"
] is False

assert gate[
    "full_source_ward_compatibility_certified"
] is False

assert gate[
    "outward_sign_established"
] is False

assert gate[
    "finite_payload_response_established"
] is False

assert gate[
    "source_charge_per_joule_established"
] is False

assert gate[
    "complete_operating_energy_established"
] is False

assert gate[
    "action_oracle_authorized"
] is False

assert gate[
    "blind_parameter_scan_authorized"
] is False


# ============================================================
# 6. DATABASE — METADATA ONLY
# ============================================================

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
                    f"SELECT COUNT(*) AS count FROM {table}"
                ).fetchone()[
                    "count"
                ]
            )
        for table
        in TABLES
    }

    persist_v25a_metadata(
        storage
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
        in TABLES
    }

finally:
    storage.close()


assert before == after


# ============================================================
# 7. OUTPUT ARTIFACTS
# ============================================================

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)


with STATE_SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                state_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()

    writer.writerows(
        state_rows
    )


with GAIN_SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                gain_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()

    writer.writerows(
        gain_rows
    )


cross_fields = sorted(
    {
        key
        for row
        in cross_rows
        for key
        in row
    }
)


with CROSS_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            cross_fields,
    )

    writer.writeheader()

    writer.writerows(
        cross_rows
    )


decision = gate[
    "decision"
]

next_step = gate[
    "next"
]


summary = {
    "branch":
        "032V25A_ACTIVE_STATE_KGB_ACTION_EXISTENCE_GATE",

    "claim_class":
        "EXPLICIT_ACTION_EXISTENCE_AND_ACTIVE_OFFSTATE_BRAIDING_PREFLIGHT",

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

    "explicit_action":
        action,

    "offstate_tree_gate":
        offstate,

    "source_gate":
        source,

    "protection_gate":
        protection,

    "action_existence_gate":
        gate,

    "minimal_cubic_gain_tradeoff": {
        "definition":
            (
                "y=beta^2*|grad_phi|^4/"
                "(2*Mpl^2*Lambda^6)"
            ),

        "z_time":
            "1-y",

        "z_transverse":
            "1-y",

        "z_parallel":
            "1+3y",

        "uncanonical_coupling_times_mpl":
            "sqrt(y/2)",

        "canonical_coupling_times_mpl":
            "sqrt(y/(2*(1-y)))",

        "gain_10x_required_z_time":
            gain_10[
                "required_z_time_margin"
            ],

        "gain_1000x_required_z_time":
            gain_1000[
                "required_z_time_margin"
            ],

        "interpretation":
            (
                "MINIMAL_CUBIC_LARGE_CANONICAL_GAIN_"
                "APPROACHES_KINETIC_DEGENERACY"
            ),

        "practical_no_go_established":
            False,
    },

    "cross_response_gate": {
        "offstate_cross_zero":
            active_offstate[
                "offstate_zero"
            ],

        "active_cross_nonzero":
            active_offstate[
                "active_nonzero"
            ],

        "response_survives_declared_field_redefinition":
            active_offstate[
                "active_response_field_redefinition_invariant"
            ],

        "full_tensor_horndeski_crosspropagator_certified":
            False,
    },

    "database": {
        "counts_before":
            before,

        "counts_after":
            after,

        "science_tables_mutated":
            before
            !=
            after,

        "region_rules_inserted":
            0,

        "action_oracles_inserted":
            0,

        "metadata_updated":
            True,
    },

    "promotion_status": {
        "explicit_action_exists":
            True,

        "action_is_physical_antigravity_model":
            False,

        "action_oracle_authorized":
            False,

        "blind_parameter_scan_authorized":
            False,

        "full_tensor_nonremovable_crosspropagator_certified":
            False,

        "new_action_source_solution_exists":
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

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,
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


# ============================================================
# 8. TERMINAL REPORT
# ============================================================

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
    "EXPLICIT_COVARIANT_ACTION_EXISTS=True"
)

print(
    "ACTION_FAMILY="
    +
    action[
        "family"
    ]
)

print(
    "EXACT_CONSTANT_SHIFT_SYMMETRY=True"
)

print(
    "ONE_UNIVERSAL_PHYSICAL_METRIC=True"
)

print(
    "ORDINARY_MATTER_MINIMALLY_COUPLED=True"
)

print(
    "HIDDEN_AXIAL_DERIVATIVE_SOURCE_OPERATOR_EXISTS=True"
)

print(
    "NEW_KGB_STATIC_SOURCE_SOLUTION_EXISTS=False"
)

print(
    "TREE_ACTIVE_OFFSTATE_SEPARATION=True"
)

print(
    "R5_SAME_TREE_OPERATOR_PRESENT=False"
)

print(
    "ACTIVE_DEBRAIDED_MATTER_COUPLING_EXISTS=True"
)

print(
    "CROSS_RESPONSE_SURVIVES_DECLARED_FIELD_REDEFINITION=True"
)

print(
    "FULL_TENSOR_NONREMOVABLE_CROSSPROPAGATOR_CERTIFIED=False"
)

print(
    "MINIMAL_CUBIC_10X_GAIN_ZTIME="
    f"{gain_10['required_z_time_margin']:.12e}"
)

print(
    "MINIMAL_CUBIC_1000X_GAIN_ZTIME="
    f"{gain_1000['required_z_time_margin']:.12e}"
)

print(
    "MINIMAL_CUBIC_LARGE_GAIN_APPROACHES_KINETIC_DEGENERACY=True"
)

print(
    "MINIMAL_CUBIC_PRACTICAL_NO_GO_ESTABLISHED=False"
)

print(
    "BULK_GALILEON_PROTECTION_CONTEXT=True"
)

print(
    "FULL_SOURCE_COUPLED_NATURALNESS_CERTIFIED=False"
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
    "DB_SCIENCE_TABLES_MUTATED=False"
)

print(
    "DB_REGION_RULES_INSERTED=0"
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
