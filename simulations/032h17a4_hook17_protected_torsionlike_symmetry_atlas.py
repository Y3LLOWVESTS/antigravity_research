"""032H17A4 protected torsion-like symmetry/action-family atlas.

This simulation requires the completed 032H17A3 result and performs no
candidate-database mutation or energy optimization.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_protected_torsionlike_atlas import (
    h17a2_oneplus_spatial_dual_vector_gate,
    h17a4_summary,
    mapped_v24_torsionlike_source_gate,
    protected_family_atlas,
    stueckelberg_vector_metric_gate,
    torsionlike_catalogue_theorem_gate,
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

DATA = (
    ROOT
    /
    "results"
    /
    "data"
)

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

A3_OUT = (
    DATA
    /
    "032h17a3_hook17_same_action_naturalness_summary.json"
)

if not A3_OUT.exists():
    raise FileNotFoundError(
        str(
            A3_OUT
        )
    )

a3_payload = json.loads(
    A3_OUT.read_text(
        encoding="utf-8"
    )
)

a3_summary = (
    a3_payload[
        "summary"
    ]
)

assert str(
    a3_summary[
        "decision"
    ]
).startswith(
    "YELLOW_H17A3_"
)

assert a3_summary[
    "hook_2plus_tree_level_action_scaffold"
] is True

assert a3_summary[
    "hook_1plus_tree_level_action_scaffold"
] is True

assert a3_summary[
    "hook_2plus_protection_gate_pass"
] is False

assert a3_summary[
    "hook_1plus_protection_gate_pass"
] is False

assert a3_summary[
    "linear_response_field_redefinition_invariant"
] is True

assert a3_summary[
    "h17b_authorized"
] is False

assert a3_summary[
    "energy_optimization_authorized"
] is False


SUMMARY_OUT = (
    DATA
    /
    "032h17a4_hook17_protected_torsionlike_summary.json"
)

ATLAS_OUT = (
    DATA
    /
    "032h17a4_hook17_protected_family_atlas.csv"
)


mapped = (
    mapped_v24_torsionlike_source_gate()
)

oneplus = (
    h17a2_oneplus_spatial_dual_vector_gate()
)

catalogue = (
    torsionlike_catalogue_theorem_gate()
)

metric = (
    stueckelberg_vector_metric_gate()
)

atlas = (
    protected_family_atlas()
)

summary = (
    h17a4_summary()
)


payload = {
    "a3_provenance":
        a3_summary,

    "mapped_v24_source":
        mapped,

    "h17a2_oneplus_dual_vector":
        oneplus,

    "torsionlike_catalogue":
        catalogue,

    "stueckelberg_metric":
        metric,

    "protected_family_atlas":
        atlas,

    "summary":
        summary,
}

SUMMARY_OUT.write_text(
    json.dumps(
        payload,
        indent=2,
    )
    +
    "\n",
    encoding="utf-8",
)


with ATLAS_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "priority",
            "family",
            "protection",
            "healthy_open_region_or_models",
            "v24_representation_match",
            "v24_exact_action_projector",
            "gauge_invariant_metric_witness",
            "status",
        ],
    )

    writer.writeheader()
    writer.writerows(
        atlas
    )


print(
    "A3_PROVENANCE_PASS=True"
)

print(
    "032H17A4_DECISION="
    +
    summary[
        "decision"
    ]
)

print(
    "NEXT="
    +
    summary[
        "next"
    ]
)

print(
    "V24_HOOK_TO_TORSIONLIKE_MAP_GREEN="
    +
    str(
        summary[
            "v24_hook_to_torsionlike_map_green"
        ]
    )
)

print(
    "MAPPED_SOURCE_SIMPLE_VECTOR_TRACE_ZERO="
    +
    str(
        summary[
            "mapped_source_simple_vector_trace_zero"
        ]
    )
)

print(
    "MAPPED_SOURCE_AXIAL_PSEUDOTRACE_ZERO="
    +
    str(
        summary[
            "mapped_source_axial_pseudotrace_zero"
        ]
    )
)

print(
    "MAPPED_SOURCE_CYCLIC_IDENTITY_ZERO="
    +
    str(
        summary[
            "mapped_source_cyclic_identity_zero"
        ]
    )
)

print(
    "TRACE_ZERO_CLOSES_ALL_VECTOR_MODES="
    +
    str(
        summary[
            "trace_zero_closes_all_vector_modes"
        ]
    )
)

print(
    "H17A2_1PLUS_SPATIAL_DUAL_VECTOR_NONZERO="
    +
    str(
        summary[
            "h17a2_1plus_spatial_dual_vector_nonzero"
        ]
    )
)

print(
    "H17A2_1PLUS_SPATIAL_DUAL_VECTOR_NORM2="
    +
    f"{summary['h17a2_1plus_spatial_dual_vector_norm2']:.12f}"
)

print(
    "TORSIONLIKE_CATALOGUE_GAUGE_SYMMETRIC_SPECIALIZATIONS="
    +
    str(
        summary[
            "torsionlike_catalogue_gauge_symmetric_specializations"
        ]
    )
)

print(
    "TORSIONLIKE_CATALOGUE_UNITARY_SPECIALIZATIONS="
    +
    str(
        summary[
            "torsionlike_catalogue_unitary_specializations"
        ]
    )
)

print(
    "TORSIONLIKE_CATALOGUE_VECTOR_ONLY_UNITARY_MODES="
    +
    str(
        summary[
            "torsionlike_catalogue_vector_only_unitary_modes"
        ]
    )
)

print(
    "CATALOGUE_DIRECTLY_RESCUES_2PLUS="
    +
    str(
        summary[
            "catalogue_directly_rescues_2plus"
        ]
    )
)

print(
    "CATALOGUE_KEEPS_1PLUS_TARGET_OPEN="
    +
    str(
        summary[
            "catalogue_keeps_1plus_target_open"
        ]
    )
)

print(
    "CATALOGUE_CLOSES_ALL_PROTECTED_2PLUS="
    +
    str(
        summary[
            "catalogue_closes_all_protected_2plus"
        ]
    )
)

print(
    "STUECKELBERG_METRIC_GAUGE_INVARIANT="
    +
    str(
        summary[
            "stueckelberg_metric_gauge_invariant"
        ]
    )
)

print(
    "STUECKELBERG_METRIC_OFFSTATE_SILENT="
    +
    str(
        summary[
            "stueckelberg_metric_offstate_silent"
        ]
    )
)

print(
    "STUECKELBERG_METRIC_ACTIVE_RESPONSE_NONZERO="
    +
    str(
        summary[
            "stueckelberg_metric_active_response_nonzero"
        ]
    )
)

print(
    "PROTECTED_EXACT_SAME_ACTION_SURVIVORS="
    +
    str(
        summary[
            "protected_exact_same_action_survivors"
        ]
    )
)

print(
    "SAME_ACTION_PROVENANCE_COMPLETE="
    +
    str(
        summary[
            "same_action_provenance_complete"
        ]
    )
)

print(
    "FULL_NOETHER_COMPLETION="
    +
    str(
        summary[
            "full_noether_completion"
        ]
    )
)

print(
    "H17B_AUTHORIZED="
    +
    str(
        summary[
            "h17b_authorized"
        ]
    )
)

print(
    "ENERGY_OPTIMIZATION_AUTHORIZED="
    +
    str(
        summary[
            "energy_optimization_authorized"
        ]
    )
)

print(
    "SUB100J_EFFICIENCY_TUNING_AUTHORIZED="
    +
    str(
        summary[
            "sub100j_efficiency_tuning_authorized"
        ]
    )
)

print(
    "HOOK17_REFERENCE_CAPACITY_RP1E12_J="
    +
    f"{summary['hook17_reference_capacity_rp1e12_j']:.12f}"
)

print(
    "HOOK17_COMPLETE_ENERGY_J=UNKNOWN"
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO"
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND=NO"
)

print(
    "PRACTICAL_DEVICE_FOUND=NO"
)

print(
    "SUMMARY_JSON="
    +
    str(
        SUMMARY_OUT
    )
)

print(
    "ATLAS_CSV="
    +
    str(
        ATLAS_OUT
    )
)
