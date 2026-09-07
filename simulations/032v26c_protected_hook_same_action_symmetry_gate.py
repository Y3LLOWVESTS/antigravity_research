"""032V26C — protected-hook same-action symmetry compatibility gate.

PURPOSE
-------
V26B1 found a nonzero quadratic active-state metric numerator from the actual
V24 Dirac hook source.

V26B1R1 showed that its leading two-mediator off-state force does not by itself
close the architecture.

Before constructing or optimizing a nonlinear metric-affine model, V26C tests
a more fundamental condition:

    DOES THE SOURCE + UNIVERSAL METRIC RESPECT THE PROTECTING
    GAUGE SYMMETRY OF THE HEALTHY PUBLISHED HOOK-CARRYING ACTION?

The primary comparison is the massless extended-Fronsdal sector of
Percacci-Sezgin arXiv:2508.14211.

No AGMINER database mutation is performed.
No energy optimization is performed.
No action oracle is created.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.protected_hook_symmetry_compatibility import (
    bms_torsionlike_same_action_gate,
    massless_hook_shift_source_ward_gate,
    marzo_nonlinear_same_action_gate,
    percacci_sezgin_massive_gate,
    percacci_sezgin_massless_same_action_gate,
    quadratic_metric_hook_shift_gate,
    v26c_action_compatibility_atlas,
    v26c_gate,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

V26B1R1 = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26b1r1_hook_quadratic_quantum_force_summary.json"
)

SUMMARY_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26c_protected_hook_same_action_symmetry_summary.json"
)

ATLAS_OUT = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v26c_protected_hook_action_compatibility.csv"
)


# ===========================================================================
# 0. POLICY / UPSTREAM PROVENANCE
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

if not V26B1R1.exists():
    raise FileNotFoundError(
        str(
            V26B1R1
        )
    )

v26b1r1 = json.loads(
    V26B1R1.read_text(
        encoding="utf-8"
    )
)

upstream = (
    v26b1r1[
        "promotion_status"
    ]
)

assert (
    upstream[
        "quadratic_metric_has_offstate_two_mediator_force"
    ]
    is True
)

assert (
    upstream[
        "empirical_inverse_cube_gate_closes_quadratic_hook_portal"
    ]
    is False
)

assert (
    upstream[
        "explicit_action_construction_authorized"
    ]
    is True
)

assert (
    upstream[
        "action_oracle_authorized"
    ]
    is False
)


# ===========================================================================
# 1. EXACT MASSLESS HOOK-SHIFT SOURCE WARD TEST
# ===========================================================================

source_ward = (
    massless_hook_shift_source_ward_gate()
)

assert (
    source_ward[
        "actual_v24_source_hook_nonzero"
    ]
    is True
)

assert (
    source_ward[
        "actual_v24_source_pure_hook_within_tolerance"
    ]
    is True
)

assert (
    source_ward[
        "source_shift_variation_nonzero"
    ]
    is True
)

assert (
    source_ward[
        "direct_hook_source_respects_published_massless_hook_shift"
    ]
    is False
)


# ===========================================================================
# 2. QUADRATIC UNIVERSAL-METRIC HOOK-SHIFT TEST
# ===========================================================================

metric_shift = (
    quadratic_metric_hook_shift_gate()
)

assert (
    metric_shift[
        "quadratic_metric_g00_nonzero"
    ]
    is True
)

assert (
    metric_shift[
        "offstate_first_variation_zero"
    ]
    is True
)

assert (
    metric_shift[
        "active_first_variation_nonzero"
    ]
    is True
)

assert (
    metric_shift[
        "quadratic_metric_respects_hook_shift_on_all_backgrounds"
    ]
    is False
)


# ===========================================================================
# 3. PUBLISHED MASSLESS SAME-ACTION DECISION
# ===========================================================================

massless = (
    percacci_sezgin_massless_same_action_gate()
)

assert (
    massless[
        "hook_degrees_pure_gauge_in_published_sector"
    ]
    is True
)

assert (
    massless[
        "current_same_action_hook_source_plus_h2_metric"
    ]
    is False
)

assert (
    massless[
        "current_h2_scaffold_closed_for_this_published_massless_sector"
    ]
    is True
)

assert (
    massless[
        "all_metric_affine_gravity_closed"
    ]
    is False
)


# ===========================================================================
# 4. OTHER MAG BRANCHES — PRESERVE WITHOUT FALSE PROMOTION
# ===========================================================================

massive = (
    percacci_sezgin_massive_gate()
)

bms = (
    bms_torsionlike_same_action_gate()
)

marzo = (
    marzo_nonlinear_same_action_gate()
)

assert (
    massive[
        "healthy_massive_spin3_region_reported"
    ]
    is True
)

assert (
    massive[
        "current_same_action_survivor"
    ]
    is False
)

assert (
    bms[
        "actual_hook_to_torsionlike_representation_map"
    ]
    is True
)

assert (
    bms[
        "current_same_action_survivor"
    ]
    is False
)

assert (
    marzo[
        "v24d_linear_route_closed"
    ]
    is True
)

assert (
    marzo[
        "nonlinear_completion_globally_closed"
    ]
    is False
)

assert (
    marzo[
        "current_same_action_survivor"
    ]
    is False
)


# ===========================================================================
# 5. CURRENT ACTION-COMPATIBILITY ATLAS
# ===========================================================================

atlas = (
    v26c_action_compatibility_atlas()
)

assert atlas

assert not any(
    row[
        "same_action_survivor"
    ]
    for row
    in atlas
)


# ===========================================================================
# 6. FRONTIER DECISION
# ===========================================================================

gate = (
    v26c_gate()
)

assert (
    gate[
        "v24_intrinsic_dirac_hook_source_preserved"
    ]
    is True
)

assert (
    gate[
        "v26b1_quadratic_algebraic_numerator_preserved"
    ]
    is True
)

assert (
    gate[
        "protected_massless_hook_h2_same_action_survives"
    ]
    is False
)

assert (
    gate[
        "current_mag_explicit_same_action_survivor"
    ]
    is False
)

assert (
    gate[
        "all_metric_affine_gravity_closed"
    ]
    is False
)

assert (
    gate[
        "intrinsic_dirac_hypermomentum_closed"
    ]
    is False
)

assert (
    gate[
        "expensive_mag_noether_completion_authorized"
    ]
    is False
)

assert (
    gate[
        "mag_energy_optimization_authorized"
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
        "agminer_database_mutation_authorized"
    ]
    is False
)

assert (
    gate[
        "protected_ct1_dhost_kmm_explicit_action_gate_authorized"
    ]
    is True
)


# ===========================================================================
# 7. PERSIST READ-ONLY SCIENTIFIC ARTIFACTS
# ===========================================================================

SUMMARY_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

ATLAS_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with ATLAS_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            atlas[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        atlas
    )

summary = {
    "phase":
        "032V26C",

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

    "upstream_v26b1r1":
        {
            "quadratic_portal_survived_inverse_cube_preflight":
                (
                    not upstream[
                        "empirical_inverse_cube_gate_closes_quadratic_hook_portal"
                    ]
                ),

            "explicit_action_construction_had_been_authorized":
                upstream[
                    "explicit_action_construction_authorized"
                ],
        },

    "massless_hook_shift_source_ward_gate":
        source_ward,

    "quadratic_metric_hook_shift_gate":
        metric_shift,

    "percacci_sezgin_massless_gate":
        massless,

    "percacci_sezgin_massive_gate":
        massive,

    "bms_torsionlike_gate":
        bms,

    "marzo_nonlinear_gate":
        marzo,

    "action_compatibility_atlas":
        atlas,

    "promotion_status":
        gate,

    "claim_limits":
        {
            "all_metric_affine_gravity_closed":
                False,

            "intrinsic_dirac_hypermomentum_closed":
                False,

            "physical_antigravity_model":
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
# 8. TERMINAL MARKERS
# ===========================================================================

print(
    "032V26C_PROTECTED_HOOK_SAME_ACTION_SYMMETRY_GATE=COMPLETED"
)

print(
    "V24_INTRINSIC_DIRAC_HOOK_SOURCE=PRESERVED"
)

print(
    "V26B1_QUADRATIC_ALGEBRAIC_NUMERATOR=PRESERVED"
)

print(
    "V26B1R1_QUANTUM_FORCE_PREFLIGHT=PRESERVED"
)

print(
    "ACTUAL_V24_SOURCE_PURE_HOOK="
    +
    str(
        source_ward[
            "actual_v24_source_pure_hook_within_tolerance"
        ]
    )
)

print(
    "HOOK_SOURCE_SHIFT_VARIATION="
    f"{source_ward['source_shift_variation']:.12e}"
)

print(
    "HOOK_SOURCE_SHIFT_VARIATION_NONZERO="
    +
    str(
        source_ward[
            "source_shift_variation_nonzero"
        ]
    )
)

print(
    "MASSLESS_HOOK_SHIFT_DIRECT_SOURCE_WARD_COMPATIBLE="
    +
    str(
        source_ward[
            "direct_hook_source_respects_published_massless_hook_shift"
        ]
    )
)

print(
    "H2_METRIC_OFFSTATE_FIRST_VARIATION_ZERO="
    +
    str(
        metric_shift[
            "offstate_first_variation_zero"
        ]
    )
)

print(
    "H2_METRIC_ACTIVE_G00="
    f"{metric_shift['quadratic_metric_g00']:.12e}"
)

print(
    "H2_METRIC_ACTIVE_SHIFT_G00="
    f"{metric_shift['active_first_variation_g00']:.12e}"
)

print(
    "H2_METRIC_FULL_HOOK_SHIFT_COMPATIBLE="
    +
    str(
        metric_shift[
            "quadratic_metric_respects_hook_shift_on_all_backgrounds"
        ]
    )
)

print(
    "PROTECTED_MASSLESS_HOOK_H2_SAME_ACTION_SURVIVES="
    +
    str(
        gate[
            "protected_massless_hook_h2_same_action_survives"
        ]
    )
)

print(
    "CURRENT_MAG_SAME_ACTION_SURVIVOR_COUNT="
    +
    str(
        gate[
            "current_mag_same_action_survivor_count"
        ]
    )
)

print(
    "ALL_METRIC_AFFINE_GRAVITY_CLOSED="
    +
    str(
        gate[
            "all_metric_affine_gravity_closed"
        ]
    )
)

print(
    "INTRINSIC_DIRAC_HYPERMOMENTUM_CLOSED="
    +
    str(
        gate[
            "intrinsic_dirac_hypermomentum_closed"
        ]
    )
)

print(
    "MAG_FRONTIER_STATUS="
    +
    str(
        gate[
            "mag_frontier_status"
        ]
    )
)

print(
    "EXPENSIVE_MAG_NOETHER_COMPLETION_AUTHORIZED="
    +
    str(
        gate[
            "expensive_mag_noether_completion_authorized"
        ]
    )
)

print(
    "MAG_ENERGY_OPTIMIZATION_AUTHORIZED="
    +
    str(
        gate[
            "mag_energy_optimization_authorized"
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
    "AGMINER_DATABASE_MUTATION_AUTHORIZED="
    +
    str(
        gate[
            "agminer_database_mutation_authorized"
        ]
    )
)

print(
    "PROTECTED_CT1_DHOST_KMM_EXPLICIT_ACTION_GATE_AUTHORIZED="
    +
    str(
        gate[
            "protected_ct1_dhost_kmm_explicit_action_gate_authorized"
        ]
    )
)

print(
    "MAG_REOPEN_CONDITION="
    +
    str(
        gate[
            "mag_reopen_condition"
        ]
    )
)

print(
    "NEXT="
    +
    str(
        gate[
            "next"
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
    "ATLAS="
    +
    str(
        ATLAS_OUT
    )
)
