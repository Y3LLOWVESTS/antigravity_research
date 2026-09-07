"""032V26A — global invariant-bridge theorem / preflight rerank.

SCIENTIFIC QUESTION
-------------------
After V25F closed denominator-driven source-aligned G2+G3 KGB gain, which
candidate bridge classes still possess a plausible genuinely new physical
numerator and deserve the next action-specific construction?

This simulation does not optimize energy. It applies four cheap analytical
or algebraic gates, persists the audit, and reranks the immediate frontier.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.invariant_bridge_theorem_gate import (
    STRICT_ENERGY_TARGET_J,
    field_strength_medium_health,
    field_strength_two_mediator_kernel,
    normalized_field_strength_portal_bound,
    required_cross_mixing_margin_for_transfer,
    static_first_derivative_metric_response,
    v17_einstein_metric_response_norms,
    v26a_gate,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26a_global_invariant_bridge_theorem_summary.json"
)

FIELD_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26a_field_strength_portal_scan.csv"
)

MIX_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v26a_cross_mixing_margin_scan.csv"
)

RERANK_OUT = (
    ROOT
    /
    "results"
    /
    "agminer"
    /
    "032v26a_global_invariant_bridge_rerank.csv"
)


# ===========================================================================
# 0. HARD POLICY IS PROVENANCE, NOT AN OPTIMIZATION VARIABLE
# ===========================================================================

policy = (
    current_energy_policy()
)

assert float(
    policy[
        "limit_j"
    ]
) == STRICT_ENERGY_TARGET_J

assert str(
    policy[
        "comparison"
    ]
) == "LT"


# ===========================================================================
# 1. STATIC FIRST-DERIVATIVE CONFORMAL / DISFORMAL NUMERATOR THEOREM
# ===========================================================================

pure_disformal = (
    static_first_derivative_metric_response(
        conformal_coefficient=
            0.0,

        disformal_coefficient=
            1.0,

        gradient_magnitude=
            1.0,
    )
)

mixed_static = (
    static_first_derivative_metric_response(
        conformal_coefficient=
            1.0,

        disformal_coefficient=
            1.0,

        gradient_magnitude=
            1.0,
    )
)

assert (
    pure_disformal[
        "delta_g00"
    ]
    ==
    0.0
)

assert (
    pure_disformal[
        "pure_static_disformal_has_leading_rest_mass_numerator"
    ]
    is False
)

assert (
    mixed_static[
        "leading_static_rest_mass_response_depends_on_conformal_piece"
    ]
    is True
)


# ===========================================================================
# 2. U(1) FIELD-STRENGTH ACTIVE / OFF-STATE QUANTUM-FORCE THEOREM
# ===========================================================================

field_bound = (
    normalized_field_strength_portal_bound()
)

assert (
    field_bound[
        "unconstrained_ratio_to_scalar_reference"
    ]
    <
    1.0
)

assert (
    field_bound[
        "healthy_minimum_ratio_to_scalar_reference"
    ]
    ==
    2.0
)

assert (
    field_bound[
        "healthy_leading_portal_beats_scalar_reference"
    ]
    is False
)

field_rows = []

for e_value in (
    -2.0,
    -1.5,
    -1.0,
    -0.5,
    0.0,
    7.0 / 23.0,
    0.5,
    1.0,
):
    kernel = (
        field_strength_two_mediator_kernel(
            electric_coefficient=
                e_value,

            magnetic_coefficient=
                1.0,
        )
    )

    health = (
        field_strength_medium_health(
            electric_coefficient=
                e_value,

            magnetic_coefficient=
                1.0,

            density_normalization=
                0.1,
        )
    )

    field_rows.append(
        {
            "electric_coefficient":
                e_value,

            "magnetic_coefficient":
                1.0,

            "kernel_coefficient":
                kernel[
                    "kernel_coefficient"
                ],

            "ratio_to_scalar_reference":
                kernel[
                    "ratio_to_scalar_reference"
                ],

            "z_electric":
                health[
                    "z_electric"
                ],

            "z_magnetic":
                health[
                    "z_magnetic"
                ],

            "speed_squared":
                health[
                    "speed_squared"
                ],

            "positive_kinetic":
                health[
                    "positive_kinetic"
                ],

            "causal_relative_to_reference_metric":
                health[
                    "causal_relative_to_reference_metric"
                ],

            "healthy_declared_medium":
                health[
                    "healthy_declared_medium"
                ],
        }
    )

healthy_rows = [
    row
    for row
    in field_rows
    if row[
        "healthy_declared_medium"
    ]
]

assert healthy_rows

assert min(
    row[
        "ratio_to_scalar_reference"
    ]
    for row
    in healthy_rows
) >= (
    2.0
    -
    1.0e-14
)


# ===========================================================================
# 3. CANONICAL CROSS-MIXING DENOMINATOR-TRAP SCAN
# ===========================================================================

mix_rows = [
    required_cross_mixing_margin_for_transfer(
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

mix1000 = next(
    row
    for row
    in mix_rows
    if row[
        "transfer"
    ]
    ==
    1000.0
)

assert (
    mix1000[
        "maximum_minimum_eigenvalue"
    ]
    <
    5.1e-4
)

assert (
    mix1000[
        "condition_number_at_threshold"
    ]
    >
    3900.0
)


# ===========================================================================
# 4. DIRECT EINSTEIN-METRIC PAYLOAD RESPONSE NORM
# ===========================================================================

metric_norms = (
    v17_einstein_metric_response_norms()
)

assert (
    metric_norms[
        "benchmark_1g"
    ][
        "dirichlet_response_norm_j"
    ]
    >
    2.4e8
)

assert (
    metric_norms[
        "benchmark_1g"
    ][
        "norm_below_strict_10mj_target"
    ]
    is False
)

assert (
    metric_norms[
        "v17_reported_volume_average"
    ][
        "dirichlet_response_norm_j"
    ]
    >
    4.5e9
)


# ===========================================================================
# 5. GLOBAL SCOPED GATE AND NEXT-ACTION RERANK
# ===========================================================================

gate = (
    v26a_gate()
)

assert (
    gate[
        "all_dhost_closed"
    ]
    is False
)

assert (
    gate[
        "all_vector_portals_closed"
    ]
    is False
)

assert (
    gate[
        "all_metric_affine_closed"
    ]
    is False
)

assert (
    gate[
        "intrinsic_dirac_hypermomentum_preserved"
    ]
    is True
)

assert (
    gate[
        "near_singular_cross_mixing_as_free_gain_engine_closed"
    ]
    is True
)

assert (
    gate[
        "blind_parameter_scan_authorized"
    ]
    is False
)

assert (
    gate[
        "generic_energy_optimization_authorized"
    ]
    is False
)

assert (
    gate[
        "next_action_specific_construction_authorized"
    ]
    is True
)

rerank_rows = [
    {
        "rank":
            1,

        "family":
            (
                "riemannian_offstate_exact_nonlinear_mag_"
                "dirac_hypermomentum_bridge"
            ),

        "status":
            "PRIORITY_OPEN",

        "new_numerator_required":
            True,

        "reason":
            (
                "V24 intrinsic Dirac source preserved; tested linear bridge "
                "closed; construct active-background nonremovable metric "
                "response without principal-margin collapse"
            ),
    },
    {
        "rank":
            2,

        "family":
            "protected_active_only_ct1_dhost_kmm_portal",

        "status":
            "OPEN_CONSTRAINED",

        "new_numerator_required":
            True,

        "reason":
            (
                "pure static disformal rest-mass numerator is zero; only a "
                "genuinely protected active-state higher/nonlinear operator "
                "merits follow-up"
            ),
    },
    {
        "rank":
            3,

        "family":
            "leading_u1_field_strength_metric_portal",

        "status":
            "RED_SCOPED",

        "new_numerator_required":
            False,

        "reason":
            (
                "formal two-mediator cancellation loses its advantage under "
                "the declared positive-kinetic causal-medium condition"
            ),
    },
    {
        "rank":
            4,

        "family":
            "near_singular_generic_cross_mixing_gain",

        "status":
            "RED_AS_GAIN_ENGINE",

        "new_numerator_required":
            False,

        "reason":
            (
                "large cross response from canonical two-mode mixing requires "
                "a collapsing principal eigenvalue"
            ),
    },
    {
        "rank":
            5,

        "family":
            "direct_planck_normalized_einstein_metric_response",

        "status":
            "RED_PREFLIGHT_FOR_SUB10MJ",

        "new_numerator_required":
            False,

        "reason":
            (
                "payload-region Dirichlet response norm is already >10 MJ; "
                "this is a preflight norm, not a gauge-invariant GR energy "
                "theorem"
            ),
    },
]

summary = {
    "phase":
        "032V26A",

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

    "static_first_derivative_metric":
        {
            "pure_disformal":
                pure_disformal,

            "mixed_example":
                mixed_static,
        },

    "u1_field_strength_portal":
        field_bound,

    "canonical_cross_mixing":
        {
            "transfer_margin_rows":
                mix_rows,

            "gain_1000":
                mix1000,
        },

    "einstein_payload_response_norm":
        metric_norms,

    "promotion_status":
        gate,

    "frontier_rerank":
        rerank_rows,

    "claim_limits":
        {
            "all_dhost_closed":
                False,

            "all_vector_portals_closed":
                False,

            "all_metric_affine_closed":
                False,

            "new_antigravity_model_established":
                False,

            "complete_sub10mj_model_established":
                False,

            "practical_device_established":
                False,
        },
}

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

RERANK_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

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

with FIELD_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            field_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(
        field_rows
    )

with MIX_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            mix_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(
        mix_rows
    )

with RERANK_OUT.open(
    "w",
    encoding="utf-8",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            rerank_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(
        rerank_rows
    )

print(
    "032V26A_GLOBAL_INVARIANT_BRIDGE_THEOREM_GATE=COMPLETED"
)

print(
    "STATIC_PURE_DISFORMAL_LEADING_REST_PAYLOAD_NUMERATOR="
    f"{gate['static_pure_disformal_leading_rest_payload_numerator']}"
)

print(
    "U1_FIELD_STRENGTH_HEALTHY_MIN_OVER_SCALAR="
    f"{field_bound['healthy_minimum_ratio_to_scalar_reference']:.12g}"
)

print(
    "CROSS_MIX_1000X_MAX_PRINCIPAL_MARGIN="
    f"{mix1000['maximum_minimum_eigenvalue']:.12g}"
)

print(
    "EINSTEIN_1G_PAYLOAD_DIRICHLET_NORM_MJ="
    f"{metric_norms['benchmark_1g']['dirichlet_response_norm_mj']:.12g}"
)

print(
    "V17_AVERAGE_EINSTEIN_DIRICHLET_NORM_MJ="
    f"{metric_norms['v17_reported_volume_average']['dirichlet_response_norm_mj']:.12g}"
)

print(
    "ALL_DHOST_CLOSED=NO"
)

print(
    "ALL_VECTOR_PORTALS_CLOSED=NO"
)

print(
    "ALL_METRIC_AFFINE_CLOSED=NO"
)

print(
    "INTRINSIC_DIRAC_HYPERMOMENTUM=PRESERVED"
)

print(
    "BLIND_PARAMETER_SCAN_AUTHORIZED=NO"
)

print(
    "GENERIC_ENERGY_OPTIMIZATION_AUTHORIZED=NO"
)

print(
    "NEXT="
    +
    str(
        gate[
            "next_phase"
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
    "FIELD_SCAN="
    +
    str(
        FIELD_OUT
    )
)

print(
    "MIX_SCAN="
    +
    str(
        MIX_OUT
    )
)

print(
    "RERANK="
    +
    str(
        RERANK_OUT
    )
)
