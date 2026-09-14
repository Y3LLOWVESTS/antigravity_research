"""032H17A10B — protected spin-one Ward / 1- rerank simulation.

This simulation persists the exact theorem-level A10B result.

It deliberately does not compute energy, geometry, payload acceleration,
or a metric response.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_spin_engineered_protected_vector_ward import (
    engineered_fixed_pair_bms_ward_gate,
    engineered_totally_symmetric_1minus_gate,
    h17a10b_summary,
)


def main() -> None:
    root = (
        Path(
            __file__
        )
        .resolve()
        .parents[
            1
        ]
    )

    data_dir = (
        root
        /
        "results"
        /
        "data"
    )

    data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary = (
        h17a10b_summary()
    )

    assert (
        summary[
            "a10a_source_state_escape_preserved"
        ]
        is True
    )

    assert (
        summary[
            "exact_bms_tensor_gauge_ward_operator_evaluated"
        ]
        is True
    )

    assert (
        summary[
            "bms_fixed_engineered_pair_direct_ward_fails"
        ]
        is True
    )

    assert (
        summary[
            "bms_generic_ward_compatible_trace_escape_exists"
        ]
        is False
    )

    assert (
        summary[
            "bms_compact_localized_rest_density_trace_route_closed"
        ]
        is True
    )

    assert (
        summary[
            "bms_global_family_closed"
        ]
        is False
    )

    assert (
        summary[
            "marzo2022_engineered_1minus_representation_reopened"
        ]
        is True
    )

    assert (
        summary[
            "marzo2022_exact_physical_1minus_pole_overlap_established"
        ]
        is False
    )

    assert (
        summary[
            "energy_optimization_authorized"
        ]
        is False
    )

    summary_path = (
        data_dir
        /
        "032h17a10b_hook17_protected_spin1_ward_rerank_summary.json"
    )

    atlas_path = (
        data_dir
        /
        "032h17a10b_hook17_protected_spin1_gate_atlas.csv"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    csv_rows = []

    for row in (
        engineered_fixed_pair_bms_ward_gate()[
            "rows"
        ]
    ):
        csv_rows.append(
            {
                "gate":
                    "BMS_DIRECT_WARD",

                "pair_id":
                    row[
                        "pair_id"
                    ],

                "momentum_id":
                    row[
                        "momentum_id"
                    ],

                "ward_residual_norm":
                    row[
                        "ward_residual_norm"
                    ],

                "ward_pass":
                    row[
                        "ward_pass"
                    ],

                "spin1_trace_norm":
                    "",

                "one_minus_representation_support":
                    "",

                "exact_pole_projector":
                    False,
            }
        )

    for row in (
        engineered_totally_symmetric_1minus_gate()[
            "rows"
        ]
    ):
        csv_rows.append(
            {
                "gate":
                    "MARZO2022_1MINUS_REPRESENTATION",

                "pair_id":
                    row[
                        "pair_id"
                    ],

                "momentum_id":
                    "",

                "ward_residual_norm":
                    "",

                "ward_pass":
                    "",

                "spin1_trace_norm":
                    row[
                        "spatial_spin1_trace_norm"
                    ],

                "one_minus_representation_support":
                    row[
                        "totally_symmetric_1minus_representation_support_nonzero"
                    ],

                "exact_pole_projector":
                    row[
                        "exact_physical_1minus_pole_projector_evaluated"
                    ],
            }
        )

    fields = [
        "gate",
        "pair_id",
        "momentum_id",
        "ward_residual_norm",
        "ward_pass",
        "spin1_trace_norm",
        "one_minus_representation_support",
        "exact_pole_projector",
    ]

    with atlas_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            csv_rows
        )

    print(
        "BRANCH="
        +
        summary[
            "branch"
        ]
    )

    print(
        "DECISION="
        +
        summary[
            "decision"
        ]
    )

    print(
        "BMS_FIXED_ENGINEERED_DIRECT_WARD_FAILS="
        +
        str(
            summary[
                "bms_fixed_engineered_pair_direct_ward_fails"
            ]
        )
    )

    print(
        "BMS_GENERIC_WARD_RANK="
        +
        str(
            summary[
                "bms_generic_rest_density_ward_rank"
            ]
        )
    )

    print(
        "BMS_GENERIC_WARD_NULLITY="
        +
        str(
            summary[
                "bms_generic_rest_density_ward_nullity"
            ]
        )
    )

    print(
        "BMS_GENERIC_TRACE_ESCAPE_EXISTS="
        +
        str(
            summary[
                "bms_generic_ward_compatible_trace_escape_exists"
            ]
        )
    )

    print(
        "BMS_COMPACT_LOCALIZED_REST_DENSITY_ROUTE_CLOSED="
        +
        str(
            summary[
                "bms_compact_localized_rest_density_trace_route_closed"
            ]
        )
    )

    print(
        "BMS_GLOBAL_FAMILY_CLOSED="
        +
        str(
            summary[
                "bms_global_family_closed"
            ]
        )
    )

    print(
        "MARZO2022_PROTECTED_FAMILY_PUBLISHED="
        +
        str(
            summary[
                "marzo2022_protected_family_published"
            ]
        )
    )

    print(
        "MARZO2022_UNIQUE_MASSIVE_POLE="
        +
        str(
            summary[
                "marzo2022_unique_massive_physical_pole_sector"
            ]
        )
    )

    print(
        "MARZO2022_ENGINEERED_1MINUS_REPRESENTATION_REOPENED="
        +
        str(
            summary[
                "marzo2022_engineered_1minus_representation_reopened"
            ]
        )
    )

    print(
        "MARZO2022_EXACT_POLE_OVERLAP_ESTABLISHED="
        +
        str(
            summary[
                "marzo2022_exact_physical_1minus_pole_overlap_established"
            ]
        )
    )

    print(
        "ENGINEERED_FULL_TORSION_SOURCE_RECONSTRUCTED="
        +
        str(
            summary[
                "engineered_full_torsion_source_reconstructed"
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
        "HOOK17_CLOSED="
        +
        str(
            summary[
                "hook17_closed"
            ]
        )
    )

    print(
        "NEXT="
        +
        summary[
            "next"
        ]
    )

    print(
        "SUMMARY_PATH="
        +
        str(
            summary_path
        )
    )

    print(
        "ATLAS_PATH="
        +
        str(
            atlas_path
        )
    )


if __name__ == "__main__":
    main()
