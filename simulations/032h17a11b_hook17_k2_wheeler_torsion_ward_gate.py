"""032H17A11B — exact K2 / Wheeler torsion source-Ward run."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_k2_wheeler_torsion_ward import (
    h17a11b_summary,
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

    a11a_path = (
        data_dir
        /
        "032h17a11a_hook17_exact_current_protection_atlas_summary.json"
    )

    if not a11a_path.exists():
        raise FileNotFoundError(
            str(
                a11a_path
            )
        )

    a11a = json.loads(
        a11a_path.read_text(
            encoding="utf-8"
        )
    )

    assert a11a[
        "branch"
    ] == "032H17A11A"

    assert a11a[
        "three_minimal_source_protection_repairs_closed"
    ] is True

    summary = h17a11b_summary()

    assert summary[
        "a11a_provenance"
    ] is True

    assert summary[
        "new_scientific_fact_engineered_states_source_full_wheeler_torsion"
    ] is True

    assert summary[
        "single_lightlike_screen_would_have_false_green"
    ] is True

    assert summary[
        "direct_k2_rest_density_wheeler_route_closed"
    ] is True

    assert summary[
        "hook17_closed"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a11b_hook17_k2_wheeler_torsion_ward_summary.json"
    )

    nullspace_path = (
        data_dir
        /
        "032h17a11b_hook17_k2_rest_density_ward_nullspace.csv"
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

    theorem = summary[
        "exact_rest_density_theorem"
    ]

    rows = []

    for index, vector in enumerate(
        theorem[
            "ward_nullspace_vectors"
        ]
    ):
        if not vector:
            rows.append(
                {
                    "null_vector":
                        index,

                    "direction":
                        "",

                    "coefficient":
                        "",
                }
            )

        for item in vector:
            rows.append(
                {
                    "null_vector":
                        index,

                    "direction":
                        item[
                            "direction"
                        ],

                    "coefficient":
                        item[
                            "coefficient"
                        ],
                }
            )

    with nullspace_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "null_vector",
                "direction",
                "coefficient",
            ],
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    engineered = summary[
        "engineered_torsion_sources"
    ]

    ward = summary[
        "engineered_sample_ward"
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
        "WHEELER_FULL_EQ27_RECONSTRUCTED="
        +
        str(
            summary[
                "wheeler_eq27_validation"
            ][
                "full_general_spinor_torsion_reconstruction"
            ]
        )
    )

    print(
        "WHEELER_EQ27_SPECIAL_CASE_VALIDATION="
        +
        str(
            summary[
                "wheeler_eq27_validation"
            ][
                "electron_special_case_exact"
            ]
            and
            summary[
                "wheeler_eq27_validation"
            ][
                "positron_special_case_exact"
            ]
        )
    )

    print(
        "HISTORICAL_CLEAN_PAIR_TORSION_ZERO="
        +
        str(
            engineered[
                "historical_clean_U1_V2_torsion_zero"
            ]
        )
    )

    print(
        "ENGINEERED_U1V1_TORSION_NORM="
        +
        str(
            engineered[
                "U1_V1_torsion_norm"
            ]
        )
    )

    print(
        "ENGINEERED_U2V2_TORSION_NORM="
        +
        str(
            engineered[
                "U2_V2_torsion_norm"
            ]
        )
    )

    print(
        "ENGINEERED_STATES_REOPEN_FULL_WHEELER_TORSION="
        +
        str(
            engineered[
                "engineered_source_state_reopens_full_wheeler_torsion"
            ]
        )
    )

    print(
        "ACCIDENTAL_LIGHTLIKE_FALSE_GREEN="
        +
        str(
            ward[
                "both_engineered_sources_accidentally_pass_lightlike_z"
            ]
        )
    )

    print(
        "ENGINEERED_GENERIC_K2_WARD_FAIL="
        +
        str(
            ward[
                "both_engineered_sources_fail_generic_k2_ward"
            ]
        )
    )

    print(
        "REST_DENSITY_DIMENSION="
        +
        str(
            theorem[
                "rest_density_real_dimension"
            ]
        )
    )

    print(
        "WHEELER_TORSION_SOURCE_MAP_RANK="
        +
        str(
            theorem[
                "wheeler_torsion_source_map_rank"
            ]
        )
    )

    print(
        "K2_WARD_POLYNOMIAL_RANK="
        +
        str(
            theorem[
                "k2_exact_polynomial_ward_rank"
            ]
        )
    )

    print(
        "K2_WARD_NULLITY="
        +
        str(
            theorem[
                "k2_exact_polynomial_ward_nullity"
            ]
        )
    )

    print(
        "WARD_NULLSPACE_SOURCE_IMAGE_RANK="
        +
        str(
            theorem[
                "ward_nullspace_source_image_rank"
            ]
        )
    )

    print(
        "NONZERO_K2_WARD_COMPATIBLE_REST_SOURCE_EXISTS="
        +
        str(
            theorem[
                "nonzero_ward_compatible_wheeler_torsion_source_exists"
            ]
        )
    )

    print(
        "DIRECT_K2_REST_DENSITY_ROUTE_CLOSED="
        +
        str(
            summary[
                "direct_k2_rest_density_wheeler_route_closed"
            ]
        )
    )

    print(
        "K2_MASSLESS_FAMILY_GLOBALLY_CLOSED="
        +
        str(
            summary[
                "k2_massless_family_globally_closed"
            ]
        )
    )

    print(
        "K2_NONREST_TEXTURED_SOURCE_CLOSED="
        +
        str(
            summary[
                "k2_nonrest_momentum_textured_dirac_source_closed"
            ]
        )
    )

    print(
        "METRIC_GATE_AUTHORIZED="
        +
        str(
            summary[
                "metric_gate_authorized"
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
        "NULLSPACE_PATH="
        +
        str(
            nullspace_path
        )
    )


if __name__ == "__main__":
    main()
