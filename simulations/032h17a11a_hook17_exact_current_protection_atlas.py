"""032H17A11A — three-lane source-protection closeout."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_exact_current_protection_atlas import (
    h17a11a_summary,
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

    summary = h17a11a_summary()

    assert summary[
        "a10f2_provenance"
    ][
        "pass"
    ] is True

    assert summary[
        "three_minimal_source_protection_repairs_closed"
    ] is True

    assert summary[
        "hook17_closed"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a11a_hook17_exact_current_protection_atlas_summary.json"
    )

    atlas_path = (
        data_dir
        /
        "032h17a11a_hook17_source_protection_lane_atlas.csv"
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

    energy = summary[
        "optimistic_energy_coupling_floor"
    ]

    higgs = summary[
        "perturbative_heavy_radial_higgs"
    ]

    pauli = summary[
        "pauli_derivative_exact_current"
    ]

    em_like = summary[
        "em_like_exact_ordinary_current"
    ]

    rows = [
        {
            "lane":
                "PERTURBATIVE_HEAVY_RADIAL_HIGGS",

            "energy_required_coupling":
                energy[
                    "minimum_effective_constituent_coupling_for_partial_sub10mj"
                ],

            "allowed_or_max_coupling":
                higgs[
                    "maximum_g_with_perturbative_radial_at_or_above_electron_threshold"
                ],

            "gap":
                higgs[
                    "energy_to_higgs_coupling_gap"
                ],

            "overlap":
                higgs[
                    "heavy_radial_energy_overlap_exists"
                ],

            "scoped_closed":
                higgs[
                    "simple_perturbative_heavy_radial_higgs_closed"
                ],
        },

        {
            "lane":
                "DIMENSION5_PAULI_DERIVATIVE_CURRENT",

            "energy_required_coupling":
                energy[
                    "minimum_effective_constituent_coupling_for_partial_sub10mj"
                ],

            "allowed_or_max_coupling":
                pauli[
                    "optimistic_effective_g_max"
                ],

            "gap":
                pauli[
                    "energy_to_pauli_coupling_gap"
                ],

            "overlap":
                pauli[
                    "energy_eft_overlap_exists"
                ],

            "scoped_closed":
                pauli[
                    "simple_dimension5_pauli_current_valid_through_electron_threshold_closed"
                ],
        },

        {
            "lane":
                "EM_LIKE_EXACT_CURRENT_RB",

            "energy_required_coupling":
                em_like[
                    "epsilon_energy_min"
                ],

            "allowed_or_max_coupling":
                em_like[
                    "epsilon_rb_95"
                ],

            "gap":
                em_like[
                    "energy_to_rb_bound_gap"
                ],

            "overlap":
                em_like[
                    "rb_energy_overlap_exists"
                ],

            "scoped_closed":
                (
                    not em_like[
                        "rb_energy_overlap_exists"
                    ]
                ),
        },

        {
            "lane":
                "EM_LIKE_EXACT_CURRENT_CS",

            "energy_required_coupling":
                em_like[
                    "epsilon_energy_min"
                ],

            "allowed_or_max_coupling":
                em_like[
                    "epsilon_cs_95"
                ],

            "gap":
                em_like[
                    "energy_to_cs_bound_gap"
                ],

            "overlap":
                em_like[
                    "cs_energy_overlap_exists"
                ],

            "scoped_closed":
                (
                    not em_like[
                        "cs_energy_overlap_exists"
                    ]
                ),
        },
    ]

    with atlas_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "lane",
                "energy_required_coupling",
                "allowed_or_max_coupling",
                "gap",
                "overlap",
                "scoped_closed",
            ],
        )

        writer.writeheader()
        writer.writerows(
            rows
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
        "A10F2_PROVENANCE="
        +
        str(
            summary[
                "a10f2_provenance"
            ][
                "pass"
            ]
        )
    )

    print(
        "OPTIMISTIC_ENERGY_MIN_SOURCE_COUPLING="
        +
        str(
            energy[
                "minimum_effective_constituent_coupling_for_partial_sub10mj"
            ]
        )
    )

    print(
        "HIGGS_HEAVY_RADIAL_G_MAX="
        +
        str(
            higgs[
                "maximum_g_with_perturbative_radial_at_or_above_electron_threshold"
            ]
        )
    )

    print(
        "HIGGS_ENERGY_GAP="
        +
        str(
            higgs[
                "energy_to_higgs_coupling_gap"
            ]
        )
    )

    print(
        "SIMPLE_HEAVY_RADIAL_HIGGS_CLOSED="
        +
        str(
            higgs[
                "simple_perturbative_heavy_radial_higgs_closed"
            ]
        )
    )

    print(
        "PAULI_SOURCE_SHAPE_IDENTITY="
        +
        str(
            pauli[
                "source_shape"
            ][
                "source_shape_identity_pass"
            ]
        )
    )

    print(
        "PAULI_EFFECTIVE_G_MAX="
        +
        str(
            pauli[
                "optimistic_effective_g_max"
            ]
        )
    )

    print(
        "PAULI_ENERGY_GAP="
        +
        str(
            pauli[
                "energy_to_pauli_coupling_gap"
            ]
        )
    )

    print(
        "SIMPLE_PAULI_CURRENT_CLOSED="
        +
        str(
            pauli[
                "simple_dimension5_pauli_current_valid_through_electron_threshold_closed"
            ]
        )
    )

    print(
        "NEUTRAL_ORDINARY_CURRENT_EM_LIKE="
        +
        str(
            em_like[
                "ordinary_current_theorem"
            ][
                "solution_em_like_up_to_overall_normalization"
            ]
        )
    )

    print(
        "EM_LIKE_EPSILON_ENERGY_MIN="
        +
        str(
            em_like[
                "epsilon_energy_min"
            ]
        )
    )

    print(
        "ELECTRON_GMINUS2_EPSILON_RB95="
        +
        str(
            em_like[
                "epsilon_rb_95"
            ]
        )
    )

    print(
        "ELECTRON_GMINUS2_EPSILON_CS95="
        +
        str(
            em_like[
                "epsilon_cs_95"
            ]
        )
    )

    print(
        "EM_LIKE_RB_GAP="
        +
        str(
            em_like[
                "energy_to_rb_bound_gap"
            ]
        )
    )

    print(
        "EM_LIKE_CS_GAP="
        +
        str(
            em_like[
                "energy_to_cs_bound_gap"
            ]
        )
    )

    print(
        "MINIMAL_EM_LIKE_EXACT_CURRENT_CLOSED="
        +
        str(
            em_like[
                "minimal_em_like_exact_current_rescue_closed_by_electron_gminus2"
            ]
        )
    )

    print(
        "THREE_MINIMAL_SOURCE_PROTECTION_REPAIRS_CLOSED="
        +
        str(
            summary[
                "three_minimal_source_protection_repairs_closed"
            ]
        )
    )

    print(
        "ALL_HIGGSED_NOETHER_COMPLETIONS_CLOSED="
        +
        str(
            summary[
                "all_higgsed_noether_completions_closed"
            ]
        )
    )

    print(
        "ALL_EXACT_CONSERVED_CURRENT_COMPLETIONS_CLOSED="
        +
        str(
            summary[
                "all_exact_conserved_current_completions_closed"
            ]
        )
    )

    print(
        "K3_CLEAN_ROUTE_REOPENED="
        +
        str(
            summary[
                "k3_historical_direct_clean_source_route_reopened"
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
