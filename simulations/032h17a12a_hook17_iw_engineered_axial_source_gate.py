"""032H17A12A — engineered Dirac reopening of Barker-Zell IW vector."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_iw_engineered_axial_source import (
    h17a12a_summary,
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

    a11c_path = (
        data_dir
        /
        "032h17a11c_hook17_k2_onshell_dirac_bilinear_summary.json"
    )

    if not a11c_path.exists():
        raise FileNotFoundError(
            str(
                a11c_path
            )
        )

    a11c = json.loads(
        a11c_path.read_text(
            encoding="utf-8"
        )
    )

    assert a11c[
        "branch"
    ] == "032H17A11C"

    assert a11c[
        "direct_k2_ordinary_dirac_onshell_wheeler_route_closed"
    ] is True

    assert a11c[
        "hook17_closed"
    ] is False

    summary = (
        h17a12a_summary()
    )

    source = summary[
        "source_reopening"
    ]

    maxwell = summary[
        "maxwell_source_ward"
    ]

    proca = summary[
        "proca_protection"
    ]

    assert summary[
        "engineered_iw_source_channel_reopened"
    ] is True

    assert source[
        "engineered_nonzero_axial_pair_ids"
    ] == [
        "U1_V1",
        "U2_V2",
    ]

    assert source[
        "u1_v1_u2_v2_axial_sources_equal_and_opposite"
    ] is True

    assert maxwell[
        "direct_engineered_dirac_iw_maxwell_branch_closed"
    ] is True

    assert proca[
        "meter_scale_proca_mass_technically_protected_by_iw_alone"
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
        "032h17a12a_hook17_iw_engineered_axial_source_summary.json"
    )

    atlas_path = (
        data_dir
        /
        "032h17a12a_hook17_iw_engineered_source_atlas.csv"
    )

    rerank_path = (
        data_dir
        /
        "032h17a12a_hook17_protected_source_rerank.csv"
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

    with atlas_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fields = [
            "pair_id",
            "historical_clean_pair",
            "full_torsion_norm",
            "j_t_hat_axial",
            "j_t_hat_norm",
            "j_t_hat_nonzero",
            "j_q_weyl_trace",
            "j_q_norm",
            "j_q_zero",
            "finite_nonzero_b3_over_2b2_induces_q_source",
            "source_norm_is_physical_energy",
        ]

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            source[
                "rows"
            ]
        )

    with rerank_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fields = [
            "priority",
            "family",
            "status",
            "reason",
        ]

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            summary[
                "rerank"
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
        "A11C_DIRECT_K2_ORDINARY_DIRAC_CLOSED=True"
    )

    print(
        "A7_GENERIC_DIRAC_IW_ESCAPE_WAS_OPEN="
        +
        str(
            source[
                "a7_generic_dirac_source_state_engineering_was_open"
            ]
        )
    )

    print(
        "ENGINEERED_NONZERO_AXIAL_PAIR_IDS="
        +
        ",".join(
            source[
                "engineered_nonzero_axial_pair_ids"
            ]
        )
    )

    print(
        "ENGINEERED_IW_T_HAT_SOURCE_REOPENED="
        +
        str(
            source[
                "engineered_dirac_reopens_a7_t_hat_channel"
            ]
        )
    )

    print(
        "ALL_TESTED_DIRECT_Q_WEYL_TRACES_ZERO="
        +
        str(
            source[
                "all_tested_weyl_q_direct_traces_zero"
            ]
        )
    )

    print(
        "FINITE_IW_MIXING_REOPENS_EFFECTIVE_Q_SOURCE="
        +
        str(
            source[
                "finite_nonzero_mixing_reopens_effective_q_source"
            ]
        )
    )

    print(
        "SAME_ACTION_IW_MATTER_COMPLETION_ESTABLISHED="
        +
        str(
            source[
                "same_action_iw_matter_completion_established"
            ]
        )
    )

    print(
        "DIRECT_IW_MAXWELL_SOURCE_WARD_PASS="
        +
        str(
            maxwell[
                "direct_maxwell_source_ward_pass"
            ]
        )
    )

    print(
        "DIRECT_ENGINEERED_DIRAC_IW_MAXWELL_CLOSED="
        +
        str(
            maxwell[
                "direct_engineered_dirac_iw_maxwell_branch_closed"
            ]
        )
    )

    print(
        "METER_SCALE_PROCA_MASS_PROTECTED_BY_IW_ALONE="
        +
        str(
            proca[
                "meter_scale_proca_mass_technically_protected_by_iw_alone"
            ]
        )
    )

    print(
        "ELECTRON_MASS_OVER_METER_VECTOR_MASS="
        +
        str(
            proca[
                "electron_mass_over_meter_vector_mass"
            ]
        )
    )

    print(
        "A10F2_LOOP_COEFFICIENT_TRANSFERRED_TO_IW="
        +
        str(
            proca[
                "a10f2_loop_coefficient_transferred_to_iw"
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
        "ATLAS_PATH="
        +
        str(
            atlas_path
        )
    )

    print(
        "RERANK_PATH="
        +
        str(
            rerank_path
        )
    )


if __name__ == "__main__":
    main()
