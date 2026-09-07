"""032V26D — protected cT=1 DHOST/KMM explicit-action gate.

This run does NOT optimize energy.

It establishes only whether a sharply defined action-level DHOST/KMM scaffold
exists that:

    - has one matter-minimal physical metric;
    - satisfies the quadratic-DHOST degeneracy relation;
    - lies on the A3=0 no-graviton-decay branch;
    - permits nonzero active beta_1;
    - has beta_1 -> 0 at X -> 0;
    - is distinct from the already-closed V21/V22 constructions.

A successful run authorizes V26E:

    static-spacelike principal symbol
    +
    constrained source->metric Green function
    +
    nonremovable active numerator bound.

No AGMINER database mutation occurs.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.protected_ct1_dhost_kmm_action import (
    action_specification,
    active_background_gate,
    identity_scan,
    inherited_failure_separation,
    offstate_gate,
    v26d_gate,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

V26C = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26c_protected_hook_same_action_symmetry_summary.json"
)

SUMMARY_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26d_protected_ct1_dhost_kmm_action_summary.json"
)

IDENTITY_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26d_dhost_kmm_identity_scan.csv"
)

PROVENANCE_OUT = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v26d_dhost_kmm_action_provenance.csv"
)


# ===========================================================================
# 0. POLICY AND V26C PROVENANCE
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

if not V26C.exists():
    raise FileNotFoundError(
        str(
            V26C
        )
    )

v26c = json.loads(
    V26C.read_text(
        encoding="utf-8"
    )
)

v26c_gate = (
    v26c[
        "promotion_status"
    ]
)

assert (
    v26c_gate[
        "mag_frontier_status"
    ]
    ==
    "PARKED_PENDING_GENUINELY_NEW_SYMMETRY_COMPATIBLE_ACTION"
)

assert (
    v26c_gate[
        "protected_ct1_dhost_kmm_explicit_action_gate_authorized"
    ]
    is True
)


# ===========================================================================
# 1. EXPLICIT ACTION / MATTER FRAME
# ===========================================================================

action = (
    action_specification()
)

assert (
    action[
        "ordinary_matter_minimal_to_physical_metric"
    ]
    is True
)

assert (
    action[
        "second_physical_metric_required"
    ]
    is False
)

assert (
    action[
        "ordinary_matter_special_charge_required"
    ]
    is False
)

assert (
    action[
        "A3"
    ]
    ==
    0.0
)

assert (
    action[
        "A5"
    ]
    ==
    0.0
)


# ===========================================================================
# 2. ACTIVE / OFF-STATE IDENTITIES
# ===========================================================================

offstate = (
    offstate_gate()
)

active = (
    active_background_gate()
)

assert (
    offstate[
        "classical_kmm_zero"
    ]
    is True
)

assert (
    active[
        "active_kmm_parameter_nonzero"
    ]
    is True
)

assert (
    active[
        "cosmological_no_decay_identity_pass"
    ]
    is True
)


# ===========================================================================
# 3. FAILURE-MEMORY SEPARATION
# ===========================================================================

separation = (
    inherited_failure_separation()
)

assert (
    separation[
        "v21_stationary_time_gradient_q_reopened"
    ]
    is False
)

assert (
    separation[
        "v22_explicit_disformal_physical_metric_reopened"
    ]
    is False
)

assert (
    separation[
        "v22_offstate_lesson_still_applies"
    ]
    is True
)


# ===========================================================================
# 4. SMALL THEOREM / IDENTITY SCAN
# ===========================================================================

identity_rows = (
    identity_scan()
)

assert identity_rows

assert all(
    row[
        "no_decay_identity_pass"
    ]
    is True
    for row
    in identity_rows
)

assert all(
    row[
        "active_kmm"
    ]
    is True
    for row
    in identity_rows
    if not row[
        "offstate"
    ]
)

assert all(
    row[
        "energy_point"
    ]
    is False
    for row
    in identity_rows
)


# ===========================================================================
# 5. CONSERVATIVE PROMOTION GATE
# ===========================================================================

gate = (
    v26d_gate()
)

assert (
    gate[
        "explicit_same_action_scaffold"
    ]
    is True
)

assert (
    gate[
        "one_universal_physical_metric"
    ]
    is True
)

assert (
    gate[
        "a3_zero_no_decay_identity"
    ]
    is True
)

assert (
    gate[
        "active_offstate_separation_at_eft_identity_level"
    ]
    is True
)

assert (
    gate[
        "microscopic_source_solution_in_full_dhost_action_established"
    ]
    is False
)

assert (
    gate[
        "static_spacelike_source_to_metric_cross_response_established"
    ]
    is False
)

assert (
    gate[
        "canonical_health_on_static_spacelike_background_established"
    ]
    is False
)

assert (
    gate[
        "anisotropic_tensor_cone_ct1_established"
    ]
    is False
)

assert (
    gate[
        "offstate_quantum_descendants_audited"
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

assert (
    gate[
        "v26e_principal_symbol_crossprop_gate_authorized"
    ]
    is True
)


# ===========================================================================
# 6. READ-ONLY ARTIFACTS
# ===========================================================================

SUMMARY_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

PROVENANCE_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with IDENTITY_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            identity_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        identity_rows
    )

provenance_rows = [
    {
        "item":
            "KINETIC_MATTER_MIXING",

        "status":
            "PUBLISHED_MECHANISM",

        "scope":
            (
                "FRAME_INDEPENDENT_KMM; "
                "MATTER_MINIMAL_FRAME_AVAILABLE"
            ),

        "promotion":
            "MECHANISM_PROVENANCE_ONLY",
    },
    {
        "item":
            "CT1_QUADRATIC_DHOST",

        "status":
            "PUBLISHED_SUBCLASS",

        "scope":
            "COSMOLOGICAL_GW_SPEED_COMPATIBLE_STRUCTURE",

        "promotion":
            "ACTION_PROVENANCE_ONLY",
    },
    {
        "item":
            "A3_ZERO",

        "status":
            "PUBLISHED_NO_DECAY_SUBCLASS",

        "scope":
            "ALPHA_H_PLUS_2_BETA1_ZERO",

        "promotion":
            "IDENTITY_VERIFIED",
    },
    {
        "item":
            "STATIC_SPACELIKE_ACTIVE_BACKGROUND",

        "status":
            "PROJECT_TARGET",

        "scope":
            "PARTIAL_T_PHI_ZERO; SPATIAL_GRADIENT_NONZERO",

        "promotion":
            "PRINCIPAL_SYMBOL_NOT_YET_DERIVED",
    },
    {
        "item":
            "HIDDEN_AXIAL_SOURCE",

        "status":
            "PROJECT_SOURCE_VERTEX",

        "scope":
            "SAME_ACTION_VERTEX_EXPLICIT",

        "promotion":
            "FULL_DHOST_SOURCE_SOLUTION_NOT_ESTABLISHED",
    },
]

with PROVENANCE_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            provenance_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        provenance_rows
    )

summary = {
    "phase":
        "032V26D",

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

            "energy_optimization_performed":
                False,
        },

    "v26c_provenance":
        {
            "mag_parked":
                True,

            "dhost_gate_authorized":
                v26c_gate[
                    "protected_ct1_dhost_kmm_explicit_action_gate_authorized"
                ],
        },

    "action":
        action,

    "offstate":
        offstate,

    "active_state":
        active,

    "inherited_failure_separation":
        separation,

    "identity_scan":
        identity_rows,

    "promotion_status":
        gate,

    "claim_limits":
        {
            "static_spacelike_principal_symbol":
                False,

            "nonremovable_source_metric_crosspropagator":
                False,

            "outward_gravity":
                False,

            "microscopic_source_solution_in_full_action":
                False,

            "anisotropic_ct1":
                False,

            "offstate_quantum_silence":
                False,

            "naturalness":
                False,

            "finite_payload":
                False,

            "complete_sub10mj_model":
                False,

            "practical_device":
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
# 7. TERMINAL MARKERS
# ===========================================================================

print(
    "032V26D_PROTECTED_CT1_DHOST_KMM_ACTION_GATE=COMPLETED"
)

print(
    "ONE_UNIVERSAL_PHYSICAL_METRIC="
    +
    str(
        gate[
            "one_universal_physical_metric"
        ]
    )
)

print(
    "SECOND_PHYSICAL_METRIC_REQUIRED="
    +
    str(
        gate[
            "second_physical_metric_required"
        ]
    )
)

print(
    "ORDINARY_MATTER_SPECIAL_CHARGE_REQUIRED="
    +
    str(
        gate[
            "ordinary_matter_special_charge_required"
        ]
    )
)

print(
    "DHOST_DEGENERACY_RELATION_EXPLICIT="
    +
    str(
        gate[
            "dhost_degeneracy_relation_explicit"
        ]
    )
)

print(
    "A3_ZERO_NO_DECAY_IDENTITY="
    +
    str(
        gate[
            "a3_zero_no_decay_identity"
        ]
    )
)

print(
    "PUBLISHED_FRAME_INDEPENDENT_KMM_STRUCTURE="
    +
    str(
        gate[
            "published_frame_independent_kmm_structure"
        ]
    )
)

print(
    "OFFSTATE_CLASSICAL_KMM_ZERO="
    +
    str(
        gate[
            "offstate_classical_kmm_zero"
        ]
    )
)

print(
    "ACTIVE_KMM_WITNESS_NONZERO="
    +
    str(
        gate[
            "active_kmm_witness_nonzero"
        ]
    )
)

print(
    "ACTIVE_OFFSTATE_SEPARATION_EFT_LEVEL="
    +
    str(
        gate[
            "active_offstate_separation_at_eft_identity_level"
        ]
    )
)

print(
    "ACTIVE_SAMPLE_ALPHA_H="
    f"{active['alpha_H']:.12e}"
)

print(
    "ACTIVE_SAMPLE_BETA1="
    f"{active['beta_1']:.12e}"
)

print(
    "ACTIVE_SAMPLE_ALPHA_H_PLUS_2_BETA1="
    f"{active['alpha_H_plus_2_beta_1']:.12e}"
)

print(
    "V21_CLOSED_ROUTE_REOPENED="
    +
    str(
        gate[
            "v21_closed_route_reopened"
        ]
    )
)

print(
    "V22_CLOSED_ROUTE_REOPENED="
    +
    str(
        gate[
            "v22_closed_route_reopened"
        ]
    )
)

print(
    "MICROSCOPIC_SOURCE_VERTEX_EXPLICIT="
    +
    str(
        gate[
            "microscopic_source_vertex_explicit"
        ]
    )
)

print(
    "MICROSCOPIC_SOURCE_SOLUTION_FULL_DHOST="
    +
    str(
        gate[
            "microscopic_source_solution_in_full_dhost_action_established"
        ]
    )
)

print(
    "STATIC_SPACELIKE_SOURCE_METRIC_CROSS_RESPONSE="
    +
    str(
        gate[
            "static_spacelike_source_to_metric_cross_response_established"
        ]
    )
)

print(
    "CANONICAL_STATIC_SPACELIKE_HEALTH="
    +
    str(
        gate[
            "canonical_health_on_static_spacelike_background_established"
        ]
    )
)

print(
    "ANISOTROPIC_TENSOR_CONE_CT1="
    +
    str(
        gate[
            "anisotropic_tensor_cone_ct1_established"
        ]
    )
)

print(
    "OFFSTATE_QUANTUM_DESCENDANTS_AUDITED="
    +
    str(
        gate[
            "offstate_quantum_descendants_audited"
        ]
    )
)

print(
    "OUTWARD_SIGN_ESTABLISHED="
    +
    str(
        gate[
            "outward_sign_established"
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
    "V26E_PRINCIPAL_SYMBOL_CROSSPROP_GATE_AUTHORIZED="
    +
    str(
        gate[
            "v26e_principal_symbol_crossprop_gate_authorized"
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
    "IDENTITY_SCAN="
    +
    str(
        IDENTITY_OUT
    )
)

print(
    "PROVENANCE="
    +
    str(
        PROVENANCE_OUT
    )
)
