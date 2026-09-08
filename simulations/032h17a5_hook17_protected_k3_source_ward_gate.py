"""032H17A5 — exact protected K3 1+ V24 source-Ward falsification gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_protected_k3_ward import (
    bms_helicity_prefilter,
    h17a5_summary,
    k3_published_model_gate,
    k3_ward_counterexample_gate,
    localized_scalar_envelope_theorem,
    protected_rescue_rerank,
    source_component_gate,
    vector_graviton_identification_gate,
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

A4_OUT = (
    DATA
    /
    "032h17a4_hook17_protected_torsionlike_summary.json"
)

if not A4_OUT.exists():
    raise FileNotFoundError(
        str(
            A4_OUT
        )
    )

a4_payload = json.loads(
    A4_OUT.read_text(
        encoding="utf-8"
    )
)

a4_summary = (
    a4_payload[
        "summary"
    ]
)

assert str(
    a4_summary[
        "decision"
    ]
).startswith(
    "YELLOW_H17A4_"
)

assert (
    a4_summary[
        "v24_hook_to_torsionlike_map_green"
    ]
    is True
)

assert (
    a4_summary[
        "catalogue_keeps_1plus_target_open"
    ]
    is True
)

assert (
    a4_summary[
        "protected_exact_same_action_survivors"
    ]
    ==
    0
)

assert (
    a4_summary[
        "h17b_authorized"
    ]
    is False
)

assert (
    a4_summary[
        "energy_optimization_authorized"
    ]
    is False
)


SUMMARY_OUT = (
    DATA
    /
    "032h17a5_hook17_protected_k3_source_ward_summary.json"
)

WARD_OUT = (
    DATA
    /
    "032h17a5_hook17_k3_ward_witnesses.csv"
)

RERANK_OUT = (
    DATA
    /
    "032h17a5_hook17_protected_rescue_rerank.csv"
)


source = (
    source_component_gate()
)

helicity = (
    bms_helicity_prefilter()
)

model = (
    k3_published_model_gate()
)

ward = (
    k3_ward_counterexample_gate()
)

envelope = (
    localized_scalar_envelope_theorem()
)

bridge = (
    vector_graviton_identification_gate()
)

rerank = (
    protected_rescue_rerank()
)

summary = (
    h17a5_summary()
)


payload = {
    "a4_provenance":
        a4_summary,

    "mapped_v24_bms_source":
        source,

    "helicity_prefilter":
        helicity,

    "k3_published_model":
        model,

    "k3_ward":
        ward,

    "localized_scalar_envelope":
        envelope,

    "vector_graviton_identification":
        bridge,

    "protected_rescue_rerank":
        rerank,

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


with WARD_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "witness",
            "q_cov",
            "q2",
            "residual",
            "residual_norm",
            "passes_necessary_ward",
        ],
    )

    writer.writeheader()

    for (
        name,
        row,
    ) in ward[
        "rows"
    ].items():
        writer.writerow(
            {
                "witness":
                    name,

                "q_cov":
                    json.dumps(
                        row[
                            "q_cov"
                        ]
                    ),

                "q2":
                    row[
                        "q2"
                    ],

                "residual":
                    json.dumps(
                        row[
                            "residual"
                        ]
                    ),

                "residual_norm":
                    row[
                        "residual_norm"
                    ],

                "passes_necessary_ward":
                    row[
                        "passes_necessary_ward"
                    ],
            }
        )


with RERANK_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "priority",
            "family",
            "status",
        ],
    )

    writer.writeheader()
    writer.writerows(
        rerank
    )


print(
    "A4_PROVENANCE_PASS=True"
)

print(
    "032H17A5_DECISION="
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
    "V24_BMS_LAST_PAIR_ANTISYMMETRIC="
    +
    str(
        source[
            "last_pair_antisymmetric"
        ]
    )
)

print(
    "V24_BMS_CURRENT_NORM="
    +
    f"{source['component_norm']:.12f}"
)

print(
    "V24_BMS_SPIN2_HELICITY_SEED_ZERO="
    +
    str(
        helicity[
            "spin2_helicity_seed_zero"
        ]
    )
)

print(
    "V24_BMS_ZERO_HELICITY_SEED_ZERO="
    +
    str(
        helicity[
            "zero_helicity_seed_zero"
        ]
    )
)

print(
    "V24_BMS_SPIN1_HELICITY_SEED_NONZERO="
    +
    str(
        helicity[
            "spin1_helicity_seed_nonzero"
        ]
    )
)

print(
    "V24_BMS_SPIN1_HELICITY_SEED_NORM2="
    +
    f"{helicity['spin1_helicity_seed_norm2']:.12f}"
)

print(
    "K3_GAUGE_SYMMETRIC="
    +
    str(
        model[
            "gauge_symmetric"
        ]
    )
)

print(
    "K3_GHOST_TACHYON_FREE="
    +
    str(
        model[
            "ghost_tachyon_free"
        ]
    )
)

print(
    "K3_PROPAGATING_SECTOR="
    +
    model[
        "propagating_sector"
    ]
)

print(
    "K3_PHYSICAL_POLARIZATIONS="
    +
    str(
        model[
            "physical_polarizations"
        ]
    )
)

print(
    "K3_PUBLISHED_SOURCE_CONSTRAINT_COUNT="
    +
    str(
        model[
            "published_source_constraint_count"
        ]
    )
)

print(
    "K3_LIGHTLIKE_Z_Q2="
    +
    f"{ward['rows']['LIGHTLIKE_Z']['q2']:.12f}"
)

print(
    "K3_LIGHTLIKE_Z_WARD_RESIDUAL="
    +
    str(
        ward[
            "rows"
        ][
            "LIGHTLIKE_Z"
        ][
            "residual"
        ]
    )
)

print(
    "K3_LIGHTLIKE_Z_WARD_RESIDUAL_NORM="
    +
    f"{ward['rows']['LIGHTLIKE_Z']['residual_norm']:.12f}"
)

print(
    "K3_DIRECT_V24_SOURCE_WARD_COMPATIBLE="
    +
    str(
        ward[
            "direct_v24_k3_source_ward_compatible"
        ]
    )
)

print(
    "K3_DIRECT_V24_SOURCE_CLOSED="
    +
    str(
        summary[
            "k3_direct_v24_source_closed"
        ]
    )
)

print(
    "K3_REPRESENTATION_SPIN1_OVERLAP_PRESERVED="
    +
    str(
        summary[
            "k3_representation_spin1_overlap_preserved"
        ]
    )
)

print(
    "CLEAN_SCALAR_ENVELOPE_K3_CLOSED="
    +
    str(
        summary[
            "clean_scalar_envelope_k3_closed"
        ]
    )
)

print(
    "Q_DEPENDENT_SOURCE_ENGINEERING_OPEN="
    +
    str(
        summary[
            "q_dependent_source_engineering_open"
        ]
    )
)

print(
    "COMPENSATED_CURRENT_OPEN="
    +
    str(
        summary[
            "compensated_current_open"
        ]
    )
)

print(
    "J11_OPEN="
    +
    str(
        summary[
            "j11_open"
        ]
    )
)

print(
    "K3_VECTOR_GRAVITON_SAME_ACTION_IDENTIFICATION="
    +
    str(
        summary[
            "k3_vector_graviton_same_action_identification"
        ]
    )
)

print(
    "HOOK17_ALL_PROTECTED_1PLUS_CLOSED="
    +
    str(
        summary[
            "hook17_all_protected_1plus_closed"
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
    "JOURNAL_NOW="
    +
    str(
        summary[
            "journal_now"
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
    "WARD_CSV="
    +
    str(
        WARD_OUT
    )
)

print(
    "RERANK_CSV="
    +
    str(
        RERANK_OUT
    )
)
