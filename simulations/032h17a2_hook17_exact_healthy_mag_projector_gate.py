"""032H17A2 exact V24 -> healthy hook-MAG source projector gate.

Run after 032H17A.

This simulation writes durable H17A2 source-projector and static-Fourier
diagnostics without modifying the AGMINER candidate database.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_healthy_mag_projector import (
    clean_v24_source_components,
    h17a2_summary,
    healthy_branch_identity_scan,
    same_action_provenance_gate,
    static_fourier_source_gate,
    timelike_rest_pole_projector_gate,
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

SUMMARY_OUT = (
    DATA
    /
    "032h17a2_hook17_exact_healthy_mag_projector_summary.json"
)

PROJECTOR_OUT = (
    DATA
    /
    "032h17a2_hook17_exact_projector_atlas.csv"
)

STATIC_OUT = (
    DATA
    /
    "032h17a2_hook17_static_fourier_source_atlas.csv"
)


source = (
    clean_v24_source_components()
)

pole = (
    timelike_rest_pole_projector_gate()
)

scan = (
    healthy_branch_identity_scan()
)

static = (
    static_fourier_source_gate()
)

provenance = (
    same_action_provenance_gate()
)

summary = (
    h17a2_summary()
)


payload = {
    "source":
        source,

    "timelike_rest_pole":
        pole,

    "healthy_branch_identity_scan":
        scan,

    "static_fourier":
        static,

    "same_action_provenance":
        provenance,

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


with PROJECTOR_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "mode",
            "exact_pole_source_nonzero",
            "raw_rest_source_norm2",
            "tensor_character",
            "healthy_reference_branch",
            "canonical_identity",
            "same_action_complete",
        ],
    )

    writer.writeheader()

    writer.writerow(
        {
            "mode":
                "HOOK_2_PLUS",

            "exact_pole_source_nonzero":
                pole[
                    "hook_2plus_exact_pole_source_nonzero"
                ],

            "raw_rest_source_norm2":
                pole[
                    "hook_2plus_raw_spatial_norm2"
                ],

            "tensor_character":
                "SPATIAL_SYMMETRIC_TRACELESS",

            "healthy_reference_branch":
                "m1<0,b6<0",

            "canonical_identity":
                "J2_NORM2=-32/b6",

            "same_action_complete":
                False,
        }
    )

    writer.writerow(
        {
            "mode":
                "HOOK_1_PLUS",

            "exact_pole_source_nonzero":
                pole[
                    "hook_1plus_exact_pole_source_nonzero"
                ],

            "raw_rest_source_norm2":
                pole[
                    "hook_1plus_raw_spatial_norm2"
                ],

            "tensor_character":
                "SPATIAL_ANTISYMMETRIC",

            "healthy_reference_branch":
                "m1<0,b7<0",

            "canonical_identity":
                "J1_NORM2=-128/b7",

            "same_action_complete":
                False,
        }
    )


with STATIC_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=[
            "axis",
            "hook_2plus_raw_norm2",
            "hook_1plus_raw_norm2",
        ],
    )

    writer.writeheader()

    for (
        axis,
        row,
    ) in static[
        "axis_rows"
    ].items():
        writer.writerow(
            {
                "axis":
                    axis,

                "hook_2plus_raw_norm2":
                    row[
                        "hook_2plus_raw_norm2"
                    ],

                "hook_1plus_raw_norm2":
                    row[
                        "hook_1plus_raw_norm2"
                    ],
            }
        )


print(
    "032H17A2_DECISION="
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
    "HOOK_2PLUS_EXACT_POLE_SOURCE_NONZERO="
    +
    str(
        summary[
            "hook_2plus_exact_pole_source_nonzero"
        ]
    )
)

print(
    "HOOK_1PLUS_EXACT_POLE_SOURCE_NONZERO="
    +
    str(
        summary[
            "hook_1plus_exact_pole_source_nonzero"
        ]
    )
)

print(
    "HOOK_2PLUS_RAW_REST_SOURCE_NORM2="
    +
    f"{summary['hook_2plus_raw_rest_norm2']:.12f}"
)

print(
    "HOOK_1PLUS_RAW_REST_SOURCE_NORM2="
    +
    f"{summary['hook_1plus_raw_rest_norm2']:.12f}"
)

print(
    "HOOK_2PLUS_CANONICAL_IDENTITY_PASS="
    +
    str(
        summary[
            "hook_2plus_canonical_identity_all_pass"
        ]
    )
)

print(
    "HOOK_1PLUS_CANONICAL_IDENTITY_PASS="
    +
    str(
        summary[
            "hook_1plus_canonical_identity_all_pass"
        ]
    )
)

print(
    "HOOK_2PLUS_STATIC_GENERIC_SUPPORT_NONZERO="
    +
    str(
        summary[
            "hook_2plus_static_generic_support_nonzero"
        ]
    )
)

print(
    "HOOK_1PLUS_STATIC_GENERIC_SUPPORT_NONZERO="
    +
    str(
        summary[
            "hook_1plus_static_generic_support_nonzero"
        ]
    )
)

print(
    "HOOK_2PLUS_STATIC_ANGULAR_AVG_NORM2="
    +
    f"{summary['hook_2plus_static_unit_sphere_average_norm2']:.12f}"
)

print(
    "HOOK_1PLUS_STATIC_ANGULAR_AVG_NORM2="
    +
    f"{summary['hook_1plus_static_unit_sphere_average_norm2']:.12f}"
)

print(
    "SAME_ACTION_COMPLETE="
    +
    str(
        summary[
            "same_action_complete"
        ]
    )
)

print(
    "EXPLICIT_SAME_ACTION_CONSTRUCTION_ATTEMPT_AUTHORIZED="
    +
    str(
        summary[
            "explicit_same_action_construction_attempt_authorized"
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
    "HOOK17_REFERENCE_CAPACITY_RP1E12_J="
    +
    f"{summary['hook17_reference_capacity_rp1e12_j']:.12f}"
)

print(
    "HOOK17_COMPLETE_ENERGY_J=UNKNOWN"
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND="
    +
    (
        "YES"

        if summary[
            "physical_antigravity_model_found"
        ]

        else "NO"
    )
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND="
    +
    (
        "YES"

        if summary[
            "certified_sub10mj_model_found"
        ]

        else "NO"
    )
)

print(
    "PRACTICAL_DEVICE_FOUND="
    +
    (
        "YES"

        if summary[
            "practical_device_found"
        ]

        else "NO"
    )
)

print(
    "SUMMARY_JSON="
    +
    str(
        SUMMARY_OUT
    )
)

print(
    "PROJECTOR_CSV="
    +
    str(
        PROJECTOR_OUT
    )
)

print(
    "STATIC_CSV="
    +
    str(
        STATIC_OUT
    )
)
