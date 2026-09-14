"""032H17A10C — engineered Marzo-2022 Stueckelberg Noether gate.

PURPOSE
-------
Persist the A10C theorem-level source-completion result.

This run verifies that:

1. A10B really reopened the engineered Marzo 1- representation;
2. the direct pure-connection engineered current is not Abelian-Ward
   compatible as a generic fixed-state scalar-envelope source;
3. the published Stueckelberg symmetry supplies one fixed local completion;
4. the completion preserves the nonzero engineered 1- representation;
5. exact pole residue, torsion reconstruction, metric response and energy
   remain unclaimed.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_marzo2022_engineered_stueckelberg_noether import (
    h17a10c_summary,
)


def main() -> None:
    """Run A10C and persist JSON/CSV artifacts."""

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

    a10b_path = (
        data_dir
        /
        "032h17a10b_hook17_protected_spin1_ward_rerank_summary.json"
    )

    if not a10b_path.exists():
        raise FileNotFoundError(
            str(
                a10b_path
            )
        )

    a10b = json.loads(
        a10b_path.read_text(
            encoding="utf-8"
        )
    )

    assert (
        a10b[
            "branch"
        ]
        ==
        "032H17A10B"
    )

    assert (
        a10b[
            "bms_compact_localized_rest_density_trace_route_closed"
        ]
        is True
    )

    assert (
        a10b[
            "marzo2022_engineered_1minus_representation_reopened"
        ]
        is True
    )

    assert (
        a10b[
            "marzo2022_exact_physical_1minus_pole_overlap_established"
        ]
        is False
    )

    assert (
        a10b[
            "hook17_closed"
        ]
        is False
    )

    summary = h17a10c_summary()

    assert (
        summary[
            "marzo2022_published_protected_stueckelberg_family"
        ]
        is True
    )

    assert (
        summary[
            "stueckelberg_invariant_combination_exact_linearized"
        ]
        is True
    )

    assert (
        summary[
            "both_engineered_direct_pure_connection_ward_fail_generic"
        ]
        is True
    )

    assert (
        summary[
            "both_engineered_stueckelberg_completed_ward_pass"
        ]
        is True
    )

    assert (
        summary[
            "both_engineered_1minus_representation_preserved"
        ]
        is True
    )

    assert (
        summary[
            "linearized_local_abelian_invariant_matter_interaction_scaffold_exists"
        ]
        is True
    )

    assert (
        summary[
            "exact_physical_1minus_pole_overlap_established"
        ]
        is False
    )

    assert (
        summary[
            "full_engineered_wheeler_torsion_source_reconstructed"
        ]
        is False
    )

    assert (
        summary[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        summary[
            "partial_green"
        ]
        is True
    )

    summary_path = (
        data_dir
        /
        "032h17a10c_hook17_marzo2022_engineered_stueckelberg_noether_summary.json"
    )

    atlas_path = (
        data_dir
        /
        "032h17a10c_hook17_marzo2022_source_ward_atlas.csv"
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

    for pair in summary[
        "engineered_pair_rows"
    ]:
        trace = pair[
            "marzo_abelian_trace_covector"
        ]

        for ward_row in pair[
            "ward_rows"
        ]:
            for completion in ward_row[
                "completions"
            ]:
                csv_rows.append(
                    {
                        "pair_id":
                            pair[
                                "pair_id"
                            ],

                        "marzo_trace_0":
                            trace[
                                0
                            ],

                        "marzo_trace_1":
                            trace[
                                1
                            ],

                        "marzo_trace_2":
                            trace[
                                2
                            ],

                        "marzo_trace_3":
                            trace[
                                3
                            ],

                        "marzo_trace_norm":
                            pair[
                                "marzo_abelian_trace_norm"
                            ],

                        "momentum_id":
                            ward_row[
                                "momentum_id"
                            ],

                        "direct_residual":
                            ward_row[
                                "direct_pure_connection_residual"
                            ],

                        "direct_pass":
                            ward_row[
                                "direct_pass"
                            ],

                        "f":
                            completion[
                                "f"
                            ],

                        "scalar_source":
                            completion[
                                "scalar_source"
                            ],

                        "completed_residual":
                            completion[
                                "completed_residual"
                            ],

                        "completed_pass":
                            completion[
                                "pass"
                            ],

                        "one_minus_trace_norm":
                            pair[
                                "engineered_1minus_spatial_trace_norm"
                            ],

                        "exact_pole_projector":
                            pair[
                                "exact_1minus_pole_projector_evaluated"
                            ],
                    }
                )

    fields = [
        "pair_id",
        "marzo_trace_0",
        "marzo_trace_1",
        "marzo_trace_2",
        "marzo_trace_3",
        "marzo_trace_norm",
        "momentum_id",
        "direct_residual",
        "direct_pass",
        "f",
        "scalar_source",
        "completed_residual",
        "completed_pass",
        "one_minus_trace_norm",
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
        "A10B_PROVENANCE=PASS"
    )

    print(
        "MARZO_PROTECTED_STUECKELBERG_FAMILY="
        +
        str(
            summary[
                "marzo2022_published_protected_stueckelberg_family"
            ]
        )
    )

    print(
        "STUECKELBERG_INVARIANT_COMBINATION_EXACT="
        +
        str(
            summary[
                "stueckelberg_invariant_combination_exact_linearized"
            ]
        )
    )

    print(
        "ENGINEERED_DIRECT_PURE_CONNECTION_WARD_FAILS="
        +
        str(
            summary[
                "both_engineered_direct_pure_connection_ward_fail_generic"
            ]
        )
    )

    print(
        "ENGINEERED_STUECKELBERG_COMPLETED_WARD_PASS="
        +
        str(
            summary[
                "both_engineered_stueckelberg_completed_ward_pass"
            ]
        )
    )

    print(
        "ENGINEERED_1MINUS_REPRESENTATION_PRESERVED="
        +
        str(
            summary[
                "both_engineered_1minus_representation_preserved"
            ]
        )
    )

    for pair in summary[
        "engineered_pair_rows"
    ]:
        print(
            pair[
                "pair_id"
            ]
            +
            "_MARZO_TRACE="
            +
            str(
                pair[
                    "marzo_abelian_trace_covector"
                ]
            )
        )

        print(
            pair[
                "pair_id"
            ]
            +
            "_1MINUS_TRACE="
            +
            str(
                pair[
                    "engineered_1minus_spatial_trace_vector"
                ]
            )
        )

    print(
        "LINEARIZED_LOCAL_ABELIAN_INVARIANT_SOURCE_SCAFFOLD="
        +
        str(
            summary[
                "linearized_local_abelian_invariant_matter_interaction_scaffold_exists"
            ]
        )
    )

    print(
        "FULL_COVARIANT_DIRAC_MATTER_ACTION="
        +
        str(
            summary[
                "full_covariant_dirac_matter_action_established"
            ]
        )
    )

    print(
        "FULL_ENGINEERED_TORSION_RECONSTRUCTED="
        +
        str(
            summary[
                "full_engineered_wheeler_torsion_source_reconstructed"
            ]
        )
    )

    print(
        "EXACT_MARZO_1MINUS_POLE_OVERLAP="
        +
        str(
            summary[
                "exact_physical_1minus_pole_overlap_established"
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
