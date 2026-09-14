"""032H17A10D — exact protected 1- pole/source saturation run."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_marzo2022_exact_1minus_pole import (
    h17a10d_summary,
)


def main() -> None:
    root = (
        Path(
            __file__
        )
        .resolve()
        .parents[1]
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

    a10c_path = (
        data_dir
        /
        "032h17a10c_hook17_marzo2022_engineered_stueckelberg_noether_summary.json"
    )

    if not a10c_path.exists():
        raise FileNotFoundError(
            str(
                a10c_path
            )
        )

    a10c = json.loads(
        a10c_path.read_text(
            encoding="utf-8"
        )
    )

    assert a10c[
        "branch"
    ] == "032H17A10C"

    assert a10c[
        "partial_green"
    ] is True

    assert a10c[
        "both_engineered_stueckelberg_completed_ward_pass"
    ] is True

    assert a10c[
        "both_engineered_1minus_representation_preserved"
    ] is True

    summary = h17a10d_summary()

    assert summary[
        "a10c_source_noether_completion_preserved"
    ] is True

    assert summary[
        "independent_action_level_1minus_operator_reconstructed"
    ] is True

    assert summary[
        "anchor_exact_residue_16_reproduced"
    ] is True

    assert summary[
        "robustness_nonzero_overlap_reproduced"
    ] is True

    assert summary[
        "exact_linearized_healthy_1minus_pole_overlap_established"
    ] is True

    assert summary[
        "energy_optimization_authorized"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a10d_hook17_marzo2022_exact_1minus_pole_summary.json"
    )

    atlas_path = (
        data_dir
        /
        "032h17a10d_hook17_marzo2022_exact_pole_source_atlas.csv"
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

    rows = []

    for benchmark_key in (
        "anchor",
        "robustness",
    ):
        benchmark = summary[
            benchmark_key
        ]

        for source in benchmark[
            "source_rows"
        ]:
            rows.append(
                {
                    "benchmark":
                        benchmark_key,

                    "benchmark_id":
                        benchmark[
                            "benchmark_id"
                        ],

                    "published_mass_squared":
                        benchmark[
                            "published_mass_squared"
                        ],

                    "published_residue":
                        benchmark[
                            "published_residue"
                        ],

                    "pair_id":
                        source[
                            "pair_id"
                        ],

                    "pole_amplitude":
                        source[
                            "pole_amplitude"
                        ],

                    "source_saturated_pole_residue":
                        source[
                            "source_saturated_pole_residue"
                        ],

                    "canonical_pole_coupling_magnitude":
                        source[
                            "canonical_pole_coupling_magnitude"
                        ],

                    "equivalent_published_constrained_source_norm":
                        source[
                            "equivalent_published_constrained_source_norm"
                        ],

                    "pole_overlap_nonzero":
                        source[
                            "pole_overlap_nonzero"
                        ],

                    "pole_rest_stueckelberg_scalar_source_zero":
                        source[
                            "pole_rest_stueckelberg_scalar_source_zero"
                        ],
                }
            )

    fields = [
        "benchmark",
        "benchmark_id",
        "published_mass_squared",
        "published_residue",
        "pair_id",
        "pole_amplitude",
        "source_saturated_pole_residue",
        "canonical_pole_coupling_magnitude",
        "equivalent_published_constrained_source_norm",
        "pole_overlap_nonzero",
        "pole_rest_stueckelberg_scalar_source_zero",
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
            rows
        )

    anchor = summary[
        "anchor"
    ]

    robust = summary[
        "robustness"
    ]

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
        "A10C_PROVENANCE=PASS"
    )

    print(
        "ACTION_1MINUS_OPERATOR_RECONSTRUCTED="
        +
        str(
            summary[
                "independent_action_level_1minus_operator_reconstructed"
            ]
        )
    )

    print(
        "ANCHOR_HEALTH_BRANCH_I="
        +
        str(
            anchor[
                "published_health_branch_I_pass"
            ]
        )
    )

    print(
        "ANCHOR_MASS_SQUARED="
        +
        str(
            anchor[
                "published_mass_squared"
            ]
        )
    )

    print(
        "ANCHOR_PUBLISHED_RESIDUE="
        +
        str(
            anchor[
                "published_residue"
            ]
        )
    )

    print(
        "ANCHOR_ACTION_DETERMINANT="
        +
        anchor[
            "action_determinant_factorized"
        ]
    )

    for row in anchor[
        "source_rows"
    ]:
        print(
            row[
                "pair_id"
            ]
            +
            "_POLE_AMPLITUDE_ABS="
            +
            str(
                row[
                    "pole_amplitude_abs"
                ]
            )
        )

        print(
            row[
                "pair_id"
            ]
            +
            "_SOURCE_SATURATED_RESIDUE="
            +
            str(
                row[
                    "source_saturated_pole_residue"
                ]
            )
        )

        print(
            row[
                "pair_id"
            ]
            +
            "_CANONICAL_POLE_COUPLING="
            +
            str(
                row[
                    "canonical_pole_coupling_magnitude"
                ]
            )
        )

    print(
        "ROBUST_D2_0P1_HEALTH="
        +
        str(
            robust[
                "published_health_branch_I_pass"
            ]
        )
    )

    print(
        "ROBUST_D2_0P1_MASS_SQUARED="
        +
        str(
            robust[
                "published_mass_squared"
            ]
        )
    )

    print(
        "ROBUST_D2_0P1_NONZERO_POLE_OVERLAP="
        +
        str(
            robust[
                "both_engineered_sources_have_nonzero_positive_pole_residue"
            ]
        )
    )

    print(
        "EXACT_HEALTHY_1MINUS_POLE_OVERLAP="
        +
        str(
            summary[
                "exact_linearized_healthy_1minus_pole_overlap_established"
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
        "UNIVERSAL_PHYSICAL_METRIC="
        +
        str(
            summary[
                "universal_physical_metric_established"
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
