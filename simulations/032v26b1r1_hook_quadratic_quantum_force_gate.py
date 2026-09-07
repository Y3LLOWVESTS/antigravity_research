"""032V26B1R1 — quadratic-hook off-state quantum-force / capacity gate.

PURPOSE
-------
V26B1 established an algebraic quadratic active-background hook numerator but
only checked that the LINEAR off-state response vanishes.

This run checks the unavoidable two-mediator off-state descendant before the
project invests in an explicit symmetry-compatible nonlinear MAG action.

It asks:

    Does the published inverse-cube force constraint force the canonically
    normalized active hook background to carry >10 MJ even under an optimistic
    spherical capacity bound?

If YES:
    close the quadratic universal-hook metric scaffold.

If NO:
    retain it and proceed to explicit same-action construction.

No parameter optimization and no AGMINER database mutation are performed.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook_quadratic_quantum_force import (
    HOYLE_2004_BETA3_68_ABS,
    empirical_capacity_corridor,
    projector_penalty_at_energy_target,
    range_massless_preflight,
    two_mediator_inverse_cube_coefficient,
    v26b1r1_gate,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

V26B1 = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26b1_same_action_hook_metric_summary.json"
)

OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26b1r1_hook_quadratic_quantum_force_summary.json"
)

SCAN_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26b1r1_projector_penalty_capacity_scan.csv"
)


# ===========================================================================
# 0. POLICY / V26B1 PROVENANCE
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

assert V26B1.exists()

v26b1 = json.loads(
    V26B1.read_text(
        encoding="utf-8"
    )
)

promotion = (
    v26b1[
        "promotion_status"
    ]
)

assert (
    promotion[
        "algebraic_design_witness"
    ]
    is True
)

assert (
    promotion[
        "hook_quadratic_rank2_metric_descendant_exists"
    ]
    is True
)

assert (
    promotion[
        "offstate_linear_hook_metric_response_zero"
    ]
    is True
)

assert (
    promotion[
        "action_oracle_authorized"
    ]
    is False
)


# ===========================================================================
# 1. TWO-MEDIATOR ANALYTIC DESCENDANT
# ===========================================================================

pair_coefficient = (
    two_mediator_inverse_cube_coefficient()
)

assert (
    pair_coefficient
    >
    0.0
)


# ===========================================================================
# 2. RANGE PREFLIGHT
# ===========================================================================

range_gate = (
    range_massless_preflight()
)

assert (
    range_gate[
        "massless_preflight_valid"
    ]
    is True
)


# ===========================================================================
# 3. PROJECTOR-PENALTY / EMPIRICAL-CAPACITY SCAN
# ===========================================================================

projector_penalties = [
    1.0,
    1.0e2,
    1.0e4,
    1.0e6,
    1.0e8,
    1.0e10,
    1.0e12,
    1.0e16,
    1.0e20,
    1.0e22,
    1.0e23,
    1.0e24,
]

rows = []

for penalty in projector_penalties:
    result = (
        empirical_capacity_corridor(
            projector_penalty=
                penalty
        )
    )

    rows.append(
        {
            "projector_penalty":
                result[
                    "projector_penalty"
                ],

            "active_coupling_max_ev_m2":
                result[
                    "active_coupling_max_ev_m2"
                ],

            "active_metric_scale_tev":
                result[
                    "equivalent_active_metric_scale_tev"
                ],

            "minimum_background_amplitude_kev":
                result[
                    "minimum_background_amplitude_kev"
                ],

            "massless_capacity_energy_j":
                result[
                    "massless_capacity_energy_j"
                ],

            "device_range_capacity_energy_j":
                result[
                    "device_range_capacity_energy_j"
                ],

            "capacity_fraction_of_10mj":
                result[
                    "capacity_energy_fraction_of_10mj"
                ],

            "below_strict_10mj":
                result[
                    "capacity_energy_below_strict_10mj"
                ],

            "reconstructed_beta3":
                result[
                    "reconstructed_beta3"
                ],
        }
    )

assert (
    rows[
        0
    ][
        "below_strict_10mj"
    ]
    is True
)

assert (
    next(
        row
        for row
        in rows
        if row[
            "projector_penalty"
        ]
        ==
        1.0e12
    )[
        "below_strict_10mj"
    ]
    is True
)


# ===========================================================================
# 4. EXACT PROJECTOR PENALTY NEEDED TO HIT ENERGY POLICY
# ===========================================================================

threshold = (
    projector_penalty_at_energy_target()
)

assert (
    threshold[
        "projector_penalty_for_target"
    ]
    >
    1.0e23
)


# ===========================================================================
# 5. CONSERVATIVE GATE
# ===========================================================================

gate = (
    v26b1r1_gate()
)

assert (
    gate[
        "quadratic_metric_has_offstate_two_mediator_force"
    ]
    is True
)

assert (
    gate[
        "empirical_inverse_cube_gate_closes_quadratic_hook_portal"
    ]
    is False
)

assert (
    gate[
        "explicit_action_construction_authorized"
    ]
    is True
)

assert (
    gate[
        "energy_optimization_authorized"
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


# ===========================================================================
# 6. PERSIST READ-ONLY SCIENTIFIC ARTIFACTS
# ===========================================================================

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with SCAN_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        rows
    )

nominal = (
    empirical_capacity_corridor(
        projector_penalty=
            1.0
    )
)

summary = {
    "phase":
        "032V26B1R1",

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

    "v26b1_provenance":
        {
            "algebraic_design_witness":
                promotion[
                    "algebraic_design_witness"
                ],

            "quadratic_rank2_metric_descendant":
                promotion[
                    "hook_quadratic_rank2_metric_descendant_exists"
                ],

            "offstate_linear_response_zero":
                promotion[
                    "offstate_linear_hook_metric_response_zero"
                ],
        },

    "two_mediator_force":
        {
            "potential_power":
                -3,

            "coefficient":
                pair_coefficient,

            "canonical_form":
                (
                    "|V| = m1*m2*(lambda*q)^2*R_P/"
                    "(64*pi^3*r^3)"
                ),

            "historical_beta3_68_abs_limit":
                HOYLE_2004_BETA3_68_ABS,

            "reference_length_m":
                1.0e-3,
        },

    "range_preflight":
        range_gate,

    "nominal_projector_corridor":
        nominal,

    "projector_penalty_energy_threshold":
        threshold,

    "projector_scan":
        rows,

    "promotion_status":
        gate,

    "claim_limits":
        {
            "same_action_established":
                False,

            "healthy_hook_propagator_established":
                False,

            "actual_projector_penalty_established":
                False,

            "finite_payload_antigravity_established":
                False,

            "complete_source_energy_established":
                False,

            "complete_sub10mj_model_established":
                False,

            "practical_device_established":
                False,
        },
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
# 7. TERMINAL MARKERS
# ===========================================================================

print(
    "032V26B1R1_HOOK_QUADRATIC_QUANTUM_FORCE_GATE=COMPLETED"
)

print(
    "V26B1_ALGEBRAIC_DESIGN_WITNESS=PRESERVED"
)

print(
    "OFFSTATE_LINEAR_RESPONSE_ZERO=True"
)

print(
    "OFFSTATE_TWO_MEDIATOR_FORCE=PRESENT"
)

print(
    "TWO_MEDIATOR_POTENTIAL_POWER=R^-3"
)

print(
    "TWO_MEDIATOR_COEFFICIENT="
    f"{pair_coefficient:.12e}"
)

print(
    "HOYLE_2004_BETA3_68_ABS_LIMIT="
    f"{HOYLE_2004_BETA3_68_ABS:.12e}"
)

print(
    "DEVICE_RANGE_MASSLESS_AT_1MM_PREFLIGHT="
    +
    str(
        range_gate[
            "massless_preflight_valid"
        ]
    )
)

print(
    "NOMINAL_ACTIVE_METRIC_SCALE_TEV="
    f"{nominal['equivalent_active_metric_scale_tev']:.12e}"
)

print(
    "NOMINAL_MIN_BACKGROUND_KEV="
    f"{nominal['minimum_background_amplitude_kev']:.12e}"
)

print(
    "NOMINAL_DEVICE_RANGE_CAPACITY_ENERGY_J="
    f"{nominal['device_range_capacity_energy_j']:.12e}"
)

print(
    "PROJECTOR_1E12_CAPACITY_ENERGY_J="
    f"{gate['projector_1e12_capacity_floor_j']:.12e}"
)

print(
    "PROJECTOR_PENALTY_TO_HIT_10MJ="
    f"{gate['projector_penalty_required_to_hit_10mj']:.12e}"
)

print(
    "EMPIRICAL_INVERSE_CUBE_GATE_CLOSES_QUADRATIC_HOOK_PORTAL="
    +
    str(
        gate[
            "empirical_inverse_cube_gate_closes_quadratic_hook_portal"
        ]
    )
)

print(
    "EXPLICIT_ACTION_CONSTRUCTION_AUTHORIZED="
    +
    str(
        gate[
            "explicit_action_construction_authorized"
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
        OUT
    )
)

print(
    "SCAN="
    +
    str(
        SCAN_OUT
    )
)
