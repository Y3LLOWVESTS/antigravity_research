"""032H17A11C — exact finite-transfer Wheeler / K2 source closeout."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_k2_onshell_dirac_bilinear import (
    h17a11c_summary,
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

    a11b_path = (
        data_dir
        /
        "032h17a11b_hook17_k2_wheeler_torsion_ward_summary.json"
    )

    if not a11b_path.exists():
        raise FileNotFoundError(
            str(
                a11b_path
            )
        )

    a11b = json.loads(
        a11b_path.read_text(
            encoding="utf-8"
        )
    )

    assert a11b[
        "branch"
    ] == "032H17A11B"

    assert a11b[
        "direct_k2_rest_density_wheeler_route_closed"
    ] is True

    assert a11b[
        "hook17_closed"
    ] is False

    summary = (
        h17a11c_summary()
    )

    theorem = summary[
        "exact_breit_k2_theorem"
    ]

    count = theorem[
        "k2_constraint_count_validation"
    ]

    assert summary[
        "a11b_provenance"
    ] is True

    assert count[
        "published_constraint_count_match"
    ] is True

    assert theorem[
        "necessary_ward_nonzero_survivors_exist"
    ] is True

    assert theorem[
        "full_k2_rank_is_eight_for_every_finite_nonzero_transfer"
    ] is True

    assert theorem[
        "nonzero_full_k2_admissible_onshell_dirac_source_exists"
    ] is False

    assert summary[
        "direct_k2_ordinary_dirac_onshell_wheeler_route_closed"
    ] is True

    assert summary[
        "healthy_pole_evaluation_authorized"
    ] is False

    assert summary[
        "metric_gate_authorized"
    ] is False

    assert summary[
        "payload_gate_authorized"
    ] is False

    assert summary[
        "energy_optimization_authorized"
    ] is False

    assert summary[
        "hook17_closed"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a11c_hook17_k2_onshell_dirac_bilinear_summary.json"
    )

    rank_path = (
        data_dir
        /
        "032h17a11c_hook17_k2_breit_rank_checks.csv"
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

    with rank_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fields = (
            "z",
            "q_over_m",
            "full_k2_constraint_rank",
            "full_k2_nullity",
            "witness_minor",
        )

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            theorem[
                "sample_rank_checks"
            ]
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
        "A11B_PROVENANCE="
        +
        str(
            summary[
                "a11b_provenance"
            ]
        )
    )

    print(
        "PUBLISHED_K2_CONSTRAINT_COUNT_MATCH="
        +
        str(
            count[
                "published_constraint_count_match"
            ]
        )
    )

    print(
        "FULL_K2_INDEPENDENT_CONSTRAINT_RANK="
        +
        str(
            count[
                "full_k2_independent_constraint_rank"
            ]
        )
    )

    print(
        "K2_ADMISSIBLE_SOURCE_DIMENSION="
        +
        str(
            count[
                "k2_admissible_source_dimension_at_nonzero_breit_q"
            ]
        )
    )

    print(
        "A11B_NECESSARY_WARD_NONZERO_SURVIVORS_EXIST="
        +
        str(
            theorem[
                "necessary_ward_nonzero_survivors_exist"
            ]
        )
    )

    print(
        "A11B_NECESSARY_WARD_SOURCE_IMAGE_RANK="
        +
        str(
            theorem[
                "combined_necessary_ward_source_image_rank"
            ]
        )
    )

    print(
        "FULL_K2_WITNESS_DETERMINANT="
        +
        theorem[
            "full_k2_witness_determinant"
        ]
    )

    print(
        "FULL_K2_WITNESS_ROOTS_INSIDE_0_1="
        +
        str(
            theorem[
                "full_k2_witness_real_roots_inside_0_1"
            ]
        )
    )

    print(
        "FULL_K2_RANK8_ALL_FINITE_NONZERO_TRANSFER="
        +
        str(
            theorem[
                "full_k2_rank_is_eight_for_every_finite_nonzero_transfer"
            ]
        )
    )

    print(
        "NONZERO_FULL_K2_ADMISSIBLE_ONSHELL_DIRAC_SOURCE_EXISTS="
        +
        str(
            theorem[
                "nonzero_full_k2_admissible_onshell_dirac_source_exists"
            ]
        )
    )

    print(
        "Z0_RANK="
        +
        str(
            theorem[
                "z0_full_constraint_rank"
            ]
        )
    )

    print(
        "Z1_RANK="
        +
        str(
            theorem[
                "z1_full_constraint_rank"
            ]
        )
    )

    print(
        "DIRECT_K2_ORDINARY_DIRAC_ONSHELL_WHEELER_ROUTE_CLOSED="
        +
        str(
            summary[
                "direct_k2_ordinary_dirac_onshell_wheeler_route_closed"
            ]
        )
    )

    print(
        "HEALTHY_POLE_EVALUATION_AUTHORIZED="
        +
        str(
            summary[
                "healthy_pole_evaluation_authorized"
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
        "PAYLOAD_GATE_AUTHORIZED="
        +
        str(
            summary[
                "payload_gate_authorized"
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
        "RANK_CHECK_PATH="
        +
        str(
            rank_path
        )
    )


if __name__ == "__main__":
    main()
