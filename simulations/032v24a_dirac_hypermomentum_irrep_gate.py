"""032V24A — explicit Dirac hypermomentum/nonmetricity irrep preflight.

V23 closed the practical ordinary-stress one-derivative reciprocal Yukawa
route but left intrinsic/Dirac hypermomentum and full metric-affine gravity
open. This run reconstructs Wheeler's explicit Dirac nonmetricity response,
closes only exact dead sectors, records a torsion-cancelled e-/e+ source
witness, and derives a generic reciprocal weak-mixing identity before any
healthy-projector or parameter scan.

GREEN_PARTIAL here means only that trace-free Dirac source carriers deserve
V24B. It does not establish a propagating mode, physical metric bridge,
outward finite-payload response, source charge per joule, energy, empirical
viability, or a device.

Outputs:
- results/data/032v24a_dirac_hypermomentum_irrep_summary.json
- results/data/032v24a_dirac_hypermomentum_mode_intersection_atlas.csv
- results/data/032v24a_quadratic_mixing_scaling_scout.csv

Database mutation is limited to narrow region rules and metadata.

CLAIM_CLASSIFICATION=
LITERATURE_RECONSTRUCTION_PLUS_PROJECT_DERIVED_ALGEBRAIC_PREFLIGHT
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.dirac_hypermomentum_irrep import (
    direct_structureless_payload_gate,
    literature_intersection_atlas,
    persist_v24a_region_rules,
    rest_spinup_special_case,
    source_irrep_diagnostics,
    weak_mixing_scaling_scout,
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

V23 = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v23_derivative_hypermomentum_multipole_summary.json"
)

OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24a_dirac_hypermomentum_irrep_summary.json"
)

ATLAS_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24a_dirac_hypermomentum_mode_intersection_atlas.csv"
)

MIXING_OUT = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "032v24a_quadratic_mixing_scaling_scout.csv"
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

STRICT_TARGET_J = 1.0e7


# ============================================================
# 0. PROVENANCE / POLICY GUARDS
# ============================================================

policy = (
    current_energy_policy()
)

assert float(
    policy[
        "limit_j"
    ]
) == STRICT_TARGET_J

assert str(
    policy[
        "comparison"
    ]
) == "LT"

if not V23.exists():
    raise FileNotFoundError(
        str(
            V23
        )
    )

v23 = json.loads(
    V23.read_text(
        encoding=
            "utf-8"
    )
)

assert v23[
    "ordinary_stress_derivative_practical_route_closed"
] is True

assert v23[
    "all_derivative_tensor_structures_closed"
] is False

assert v23[
    "intrinsic_hypermomentum_closed"
] is False

assert v23[
    "dirac_hypermomentum_closed"
] is False

assert v23[
    "full_metric_affine_gravity_closed"
] is False

assert v23[
    "physical_metric_bridge_established"
] is False

assert v23[
    "blind_parameter_scan_authorized"
] is False


# ============================================================
# 1. EXPLICIT SOURCE-RESPONSE RECONSTRUCTION
# ============================================================

witness_spinors = {
    "rest_first_basis_state":
        np.array(
            [
                1 + 0j,
                0j,
                0j,
                0j,
            ]
        ),

    "rest_second_basis_state":
        np.array(
            [
                0j,
                1 + 0j,
                0j,
                0j,
            ]
        ),

    "rest_third_basis_state":
        np.array(
            [
                0j,
                0j,
                1 + 0j,
                0j,
            ]
        ),

    "rest_fourth_basis_state":
        np.array(
            [
                0j,
                0j,
                0j,
                1 + 0j,
            ]
        ),

    "generic_complex_spinor":
        np.array(
            [
                1 + 0.2j,
                0.3 - 0.4j,
                -0.2 + 0.9j,
                0.5 + 0.1j,
            ]
        ),
}

witness_results = {
    name:
        source_irrep_diagnostics(
            spinor
        )

    for name, spinor
    in witness_spinors.items()
}

for result in witness_results.values():
    assert result[
        "nonmetricity_response_nonzero"
    ] is True

    assert result[
        "last_pair_symmetric"
    ] is True

    assert result[
        "weyl_dilation_trace_overlap_zero"
    ] is True

    assert result[
        "lorentz_trace_norm"
    ] < 1e-12

    assert result[
        "exact_propagating_spin_projector_overlap_established"
    ] is False

    assert result[
        "physical_metric_bridge_established"
    ] is False

    assert result[
        "source_charge_per_joule_established"
    ] is False


special = (
    rest_spinup_special_case()
)

assert special[
    "electron_nonmetricity_matches_published_special_case"
] is True

assert special[
    "positron_nonmetricity_matches_published_special_case"
] is True

assert special[
    "equal_amplitude_particle_antiparticle_same_nonmetricity_sign"
] is True

assert special[
    "equal_amplitude_particle_antiparticle_opposite_torsion_sign"
] is True

assert special[
    "pair_torsion_response_cancels"
] is True

assert special[
    "pair_nonmetricity_response_adds"
] is True

assert math.isclose(
    special[
        "pair_nonmetricity_component_norm_over_single"
    ],
    2.0,
    abs_tol=
        1e-12,
)

rest_irrep = special[
    "electron_irrep"
]

assert rest_irrep[
    "totally_symmetric_carrier_nonzero"
] is True

assert rest_irrep[
    "hook_symmetric_carrier_nonzero"
] is True

assert math.isclose(
    rest_irrep[
        "component_totally_symmetric_norm_fraction"
    ],
    1
    /
    3,
    abs_tol=
        1e-12,
)

assert math.isclose(
    rest_irrep[
        "component_hook_symmetric_norm_fraction"
    ],
    2
    /
    3,
    abs_tol=
        1e-12,
)


# ============================================================
# 2. UNIVERSAL PAYLOAD + MIXING THEOREM
# ============================================================

payload_gate = (
    direct_structureless_payload_gate()
)

assert payload_gate[
    "direct_post_riemannian_microstructure_force_available"
] is False

assert payload_gate[
    "usual_riemannian_geodesic_recovered"
] is True

assert payload_gate[
    "universal_metric_backreaction_closed"
] is False


mixing_rows = (
    weak_mixing_scaling_scout()
)

assert all(
    float(
        row[
            "reciprocity_identity_relative_error"
        ]
    ) < 1e-12

    for row
    in mixing_rows
)

r1 = mixing_rows[
    -2
]

r2 = mixing_rows[
    -1
]

ratio = (
    float(
        r1[
            "mixing"
        ]
    )
    /
    float(
        r2[
            "mixing"
        ]
    )
)

cross_power = (
    math.log(
        float(
            r1[
                "abs_cross_response"
            ]
        )
        /
        float(
            r2[
                "abs_cross_response"
            ]
        )
    )
    /
    math.log(
        ratio
    )
)

visible_power = (
    math.log(
        float(
            r1[
                "visible_offstate_correction"
            ]
        )
        /
        float(
            r2[
                "visible_offstate_correction"
            ]
        )
    )
    /
    math.log(
        ratio
    )
)

assert abs(
    cross_power
    -
    1.0
) < 1e-3

assert abs(
    visible_power
    -
    2.0
) < 1e-3


# ============================================================
# 3. THEORY-SPACE INTERSECTION
# ============================================================

atlas = (
    literature_intersection_atlas()
)

atlas_by_sector = {
    row[
        "sector"
    ]:
        row

    for row
    in atlas
}

assert atlas_by_sector[
    "WEYL_DILATION_TRACE"
][
    "status"
] == (
    "CLOSED_FOR_EXPLICIT_WHEELER_DIRAC_SOURCE"
)

assert atlas_by_sector[
    "TOTALLY_SYMMETRIC_TRACEFREE"
][
    "status"
] == (
    "OPEN_FOR_EXACT_PROJECTOR_AND_METRIC_BRIDGE_TEST"
)

assert atlas_by_sector[
    "HOOK_SYMMETRIC_TRACEFREE"
][
    "status"
] == (
    "OPEN_FOR_EXACT_PROJECTOR_AND_METRIC_BRIDGE_TEST"
)

assert atlas_by_sector[
    "DIRECT_STRUCTURELESS_CONNECTION_FORCE"
][
    "status"
] == (
    "NOT_A_UNIVERSAL_PAYLOAD_BRIDGE"
)

assert atlas_by_sector[
    "TORSION_CANCELLED_PARTICLE_ANTIPARTICLE_PAIR_SOURCE"
][
    "status"
] == (
    "OPEN_MICROSCOPIC_SOURCE_WITNESS"
)

assert atlas_by_sector[
    "WEAK_UNIVERSAL_METRIC_MIXING_PLUS_LARGE_HIDDEN_CHARGE"
][
    "status"
] == (
    "OPEN_STRUCTURAL_PORTAL_STRATEGY"
)


# ============================================================
# 4. AGMINER FAILURE MEMORY ONLY
# ============================================================

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

    inserted_rules = (
        persist_v24a_region_rules(
            storage
        )
    )

    metadata = {
        "032v24a_wheeler_dirac_nonmetricity_source_response_exists":
            "1",

        "032v24a_wheeler_dirac_weyl_dilation_overlap":
            "0",

        "032v24a_tracefree_totally_symmetric_carrier_open":
            "1",

        "032v24a_tracefree_hook_carrier_open":
            "1",

        "032v24a_torsion_cancelled_pair_source_witness":
            "1",

        "032v24a_universal_metric_bridge_established":
            "0",

        "032v24a_source_charge_per_joule_established":
            "0",

        "agminer_next_family":
            (
                "DIRAC_HYPERMOMENTUM_EXACT_HEALTHY_PROJECTOR_"
                "CANONICAL_METRIC_BRIDGE"
            ),
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


# ============================================================
# 5. PERSISTENT ARTIFACTS
# ============================================================

OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with ATLAS_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    fields = sorted(
        {
            key
            for row in atlas
            for key in row
        }
    )

    writer = csv.DictWriter(
        handle,
        fieldnames=
            fields,
    )

    writer.writeheader()
    writer.writerows(
        atlas
    )


with MIXING_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                mixing_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        mixing_rows
    )


decision = (
    "GREEN_PARTIAL_032V24A_EXPLICIT_DIRAC_TRACEFREE_NONMETRICITY_"
    "CARRIERS_EXIST__WEYL_DILATION_ZERO__TORSION_CANCELLED_PAIR_"
    "SOURCE_WITNESS_EXISTS__DIRECT_STRUCTURELESS_CONNECTION_FORCE_"
    "NOT_UNIVERSAL__WEAK_MIXING_CROSS_LINEAR_OFFSTATE_QUADRATIC__"
    "EXACT_HEALTHY_PROJECTOR_AND_METRIC_BRIDGE_REQUIRED"
)

next_step = (
    "032V24B_EXACT_CANONICAL_HEALTHY_PROJECTOR_AND_"
    "UNIVERSAL_METRIC_BRIDGE_GATE"
)


summary = {
    "branch":
        "032V24A_DIRAC_HYPERMOMENTUM_IRREP_PREFLIGHT",

    "energy_policy": {
        "limit_j":
            STRICT_TARGET_J,

        "comparison":
            "LT",

        "exactly_10mj_passes":
            False,

        "energy_evaluated_in_v24a":
            False,
    },

    "v23_provenance": {
        "ordinary_stress_derivative_practical_route_closed":
            True,

        "intrinsic_hypermomentum_closed":
            False,

        "dirac_hypermomentum_closed":
            False,

        "full_metric_affine_gravity_closed":
            False,
    },

    "wheeler_dirac_source": {
        "explicit_nonmetricity_source_response_exists":
            True,

        "weyl_dilation_trace_overlap_zero":
            True,

        "totally_symmetric_tracefree_algebraic_carrier":
            True,

        "hook_symmetric_tracefree_algebraic_carrier":
            True,

        "exact_propagating_spin_projector_overlap_established":
            False,

        "wheeler_eh_response_itself_is_propagating_mode_realization":
            False,
    },

    "rest_spinup_pair_witness": {
        "torsion_response_cancels":
            special[
                "pair_torsion_response_cancels"
            ],

        "nonmetricity_response_adds":
            special[
                "pair_nonmetricity_response_adds"
            ],

        "nonmetricity_component_norm_over_single":
            special[
                "pair_nonmetricity_component_norm_over_single"
            ],

        "hidden_vector_charge_cancellation_established":
            False,

        "total_spin_cancellation_established":
            False,

        "support_cost_established":
            False,

        "source_energy_established":
            False,
    },

    "rest_spinup_algebraic_split": {
        "totally_symmetric_component_norm_fraction":
            rest_irrep[
                "component_totally_symmetric_norm_fraction"
            ],

        "hook_symmetric_component_norm_fraction":
            rest_irrep[
                "component_hook_symmetric_norm_fraction"
            ],

        "component_norm_is_lorentz_invariant":
            False,

        "component_norm_is_field_energy":
            False,
    },

    "structureless_payload_gate":
        payload_gate,

    "quadratic_mixing_reciprocity": {
        "identity":
            (
                "G_vh^2="
                "(G_vv-G_vv_at_zero_mixing)*G_hh"
            ),

        "small_mixing_cross_power":
            cross_power,

        "small_mixing_visible_offstate_power":
            visible_power,

        "interpretation":
            (
                "FAVORABLE_STRUCTURE_ONLY__"
                "LARGE_HIDDEN_CHARGE_PER_JOULE_STILL_REQUIRED"
            ),

        "physical_metric_affine_action_match_established":
            False,

        "empirical_bound_mapped":
            False,
    },

    "theory_intersection_atlas":
        atlas,

    "database": {
        "models_mutated":
            after[
                "models"
            ]
            !=
            before[
                "models"
            ],

        "rejections_mutated":
            after[
                "rejections"
            ]
            !=
            before[
                "rejections"
            ],

        "action_oracles_mutated":
            after[
                "action_oracles"
            ]
            !=
            before[
                "action_oracles"
            ],

        "mechanism_metrics_mutated":
            after[
                "mechanism_metrics"
            ]
            !=
            before[
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

        "canonical_normalization_established":
            False,

        "universal_physical_metric_bridge_established":
            False,

        "source_charge_per_joule_established":
            False,

        "finite_payload_response_established":
            False,

        "outward_sign_established":
            False,

        "true_standoff_established":
            False,

        "naturalness_established":
            False,

        "empirical_consistency_established":
            False,

        "complete_operating_energy_established":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,
    },

    "v24b_priority": [
        (
            "1__TORSION_CANCELLED_DIRAC_PAIR_TO_SYMMETRY_PROTECTED_"
            "TOTALLY_SYMMETRIC_TRACEFREE_HEALTHY_PROJECTOR"
        ),
        (
            "2__DERIVE_CANONICAL_H_Q_MIXING_AND_UNIVERSAL_METRIC_"
            "CROSS_PROPAGATOR__APPLY_RECIPROCITY_OFFSTATE_GATE"
        ),
        (
            "3__ONLY_IF_1_AND_2_SURVIVE__SOURCE_CHARGE_PER_JOULE_"
            "AND_POSITIVE_EXTERIOR_FIELD_INVENTORY"
        ),
        (
            "4__HOOK_SPIN3_OR_SPIN3_PLUS0_ONLY_WITH_EXPLICIT_"
            "RADIATIVE_PROTECTION"
        ),
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


# ============================================================
# 6. TERMINAL SUMMARY
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
    "ENERGY_EVALUATED_IN_V24A=False"
)

print(
    "WHEELER_DIRAC_NONMETRICITY_SOURCE_RESPONSE_EXISTS=True"
)

print(
    "WHEELER_DIRAC_WEYL_DILATION_TRACE_OVERLAP=0"
)

print(
    "TOTALLY_SYMMETRIC_TRACEFREE_ALGEBRAIC_CARRIER=NONZERO"
)

print(
    "HOOK_SYMMETRIC_TRACEFREE_ALGEBRAIC_CARRIER=NONZERO"
)

print(
    "EXACT_PROPAGATING_SPIN_PROJECTOR_OVERLAP_ESTABLISHED=False"
)

print(
    "PAIR_TORSION_RESPONSE_CANCELS=True"
)

print(
    "PAIR_NONMETRICITY_RESPONSE_ADDS=True"
)

print(
    "REST_PAIR_NONMETRICITY_COMPONENT_NORM_OVER_SINGLE="
    f"{special['pair_nonmetricity_component_norm_over_single']:.12e}"
)

print(
    "REST_TOTAL_SYMMETRIC_COMPONENT_NORM_FRACTION="
    f"{rest_irrep['component_totally_symmetric_norm_fraction']:.12e}"
)

print(
    "REST_HOOK_COMPONENT_NORM_FRACTION="
    f"{rest_irrep['component_hook_symmetric_norm_fraction']:.12e}"
)

print(
    "COMPONENT_NORM_IS_LORENTZ_INVARIANT=False"
)

print(
    "DIRECT_STRUCTURELESS_CONNECTION_FORCE_IS_UNIVERSAL_BRIDGE=False"
)

print(
    "UNIVERSAL_METRIC_BACKREACTION_CLOSED=False"
)

print(
    "WEAK_MIXING_CROSS_POWER="
    f"{cross_power:.12e}"
)

print(
    "WEAK_MIXING_VISIBLE_OFFSTATE_POWER="
    f"{visible_power:.12e}"
)

print(
    "QUADRATIC_RECIPROCITY_IDENTITY=PASS"
)

print(
    "SOURCE_CHARGE_PER_JOULE_ESTABLISHED=False"
)

print(
    "PHYSICAL_METRIC_BRIDGE_ESTABLISHED=False"
)

print(
    "BLIND_PARAMETER_SCAN_AUTHORIZED=False"
)

print(
    "DB_MODELS_MUTATED="
    +
    str(
        after[
            "models"
        ]
        !=
        before[
            "models"
        ]
    )
)

print(
    "DB_REJECTIONS_MUTATED="
    +
    str(
        after[
            "rejections"
        ]
        !=
        before[
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
        after[
            "action_oracles"
        ]
        !=
        before[
            "action_oracles"
        ]
    )
)

print(
    "DB_MECHANISM_METRICS_MUTATED="
    +
    str(
        after[
            "mechanism_metrics"
        ]
        !=
        before[
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
