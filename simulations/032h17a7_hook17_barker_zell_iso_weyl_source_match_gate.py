"""Simulation 032H17A7 — Barker-Zell iso-Weyl source-match gate.

This is a theorem-first source prefilter.

It does not:
- scan continuous parameters;
- solve a PDE;
- recompute HOOK17 capacity;
- calculate complete energy;
- mutate AGMINER;
- promote a physical model.

It persists the direct clean-pair IW source result and the post-IW rerank.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_barker_zell_iso_weyl_source_match import (
    barker_zell_iso_weyl_family_gate,
    barker_zell_iw_clean_source_match_gate,
    clean_v24_pair_axial_torsion_gate,
    clean_v24_pair_weyl_trace_gate,
    h17a7_summary,
    iw_nondynamical_mixing_source_theorem,
    prior_barker_zell_ep_gate,
    source_channel_rows,
)


def main() -> None:
    """Run A7 and persist durable source/provenance artifacts."""

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

    a6r2_path = (
        data_dir
        /
        "032h17a6r2_hook17_marzo2022_massive_source_match_summary.json"
    )

    if not a6r2_path.exists():
        raise FileNotFoundError(
            str(
                a6r2_path
            )
        )

    a6r2_payload = json.loads(
        a6r2_path.read_text(
            encoding="utf-8"
        )
    )

    a6r2 = a6r2_payload[
        "summary"
    ]

    assert (
        a6r2[
            "direct_clean_v24_marzo2022_massive_1minus_closed"
        ]
        is True
    )

    assert (
        a6r2[
            "productive_clean_v24_1plus_survives"
        ]
        is True
    )

    assert (
        a6r2[
            "productive_clean_v24_2plus_survives"
        ]
        is True
    )

    assert (
        a6r2[
            "hook17_closed"
        ]
        is False
    )

    prior_ep = prior_barker_zell_ep_gate()
    family = barker_zell_iso_weyl_family_gate()
    q_gate = clean_v24_pair_weyl_trace_gate()
    axial_gate = clean_v24_pair_axial_torsion_gate()
    mixing = iw_nondynamical_mixing_source_theorem()
    source_match = barker_zell_iw_clean_source_match_gate()
    summary = h17a7_summary()

    payload = {
        "prior_barker_zell_ep":
            prior_ep,

        "barker_zell_iso_weyl_family":
            family,

        "clean_v24_pair_weyl_trace":
            q_gate,

        "clean_v24_pair_axial_torsion":
            axial_gate,

        "iw_nondynamical_mixing_theorem":
            mixing,

        "iw_clean_source_match":
            source_match,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032h17a7_hook17_barker_zell_iso_weyl_source_match_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            payload,
            indent=
                2,
            sort_keys=
                True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    source_path = (
        data_dir
        /
        "032h17a7_hook17_iso_weyl_source_channels.csv"
    )

    with source_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "channel",
                "support_nonzero",
                "support_measure",
                "status",
            ],
        )

        writer.writeheader()

        writer.writerows(
            source_channel_rows()
        )

    rerank_path = (
        data_dir
        /
        "032h17a7_hook17_post_iso_weyl_rerank.csv"
    )

    with rerank_path.open(
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
                "reason",
            ],
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
        "SUBGATE="
        +
        summary[
            "subgate"
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
        "A6R2_PROVENANCE_PASS="
        +
        str(
            summary[
                "a6r2_provenance_pass"
            ]
        )
    )

    print(
        "PRIOR_BARKER_ZELL_EP_PSEUDOSCALAR_ALREADY_CLOSED="
        +
        str(
            summary[
                "prior_ep_pseudoscalar_already_closed"
            ]
        )
    )

    print(
        "PRIOR_EP_REPEATED="
        +
        str(
            not summary[
                "prior_ep_not_repeated"
            ]
        )
    )

    print(
        "IW_DISTINCT_BRANCH_PRESERVED_BY_V24B="
        +
        str(
            summary[
                "iw_distinct_branch_preserved_by_v24b"
            ]
        )
    )

    print(
        "BARKER_ZELL_IW_PUBLISHED_VECTOR_FAMILY_EXISTS="
        +
        str(
            summary[
                "barker_zell_iw_published_vector_family_exists"
            ]
        )
    )

    print(
        "IW_PROPAGATING_VECTOR="
        +
        summary[
            "iw_propagating_vector"
        ]
    )

    print(
        "IW_REDUCED_VECTOR_THEORY="
        +
        summary[
            "iw_reduced_vector_theory"
        ]
    )

    print(
        "CLEAN_V24_PAIR_NONMETRICITY_NONZERO="
        +
        str(
            q_gate[
                "pair_nonmetricity_tensor_nonzero"
            ]
        )
    )

    print(
        "CLEAN_V24_PAIR_WEYL_TRACE_ZERO="
        +
        str(
            q_gate[
                "pair_weyl_trace_zero"
            ]
        )
    )

    print(
        "CLEAN_V24_PAIR_TORSION_RESPONSE_ZERO="
        +
        str(
            axial_gate[
                "full_pair_torsion_response_zero"
            ]
        )
    )

    print(
        "CLEAN_V24_PAIR_AXIAL_TORSION_CHANNEL_ZERO="
        +
        str(
            axial_gate[
                "identified_iw_t_hat_channel_zero"
            ]
        )
    )

    print(
        "IW_NATIVE_VECTOR_BLOCK_SOURCE_ZERO="
        +
        str(
            mixing[
                "direct_clean_v24_iw_native_vector_block_source_zero"
            ]
        )
    )

    print(
        "IW_NONDYNAMICAL_MIXING_CAN_CREATE_SOURCE_FROM_ZERO_ZERO="
        +
        str(
            mixing[
                "mixing_can_create_nonzero_source_from_zero_zero"
            ]
        )
    )

    print(
        "DIRECT_CLEAN_V24_BARKER_ZELL_IW_VECTOR_ROUTE_CLOSED="
        +
        str(
            summary[
                "direct_clean_v24_barker_zell_iw_vector_route_closed"
            ]
        )
    )

    print(
        "FULL_BARKER_ZELL_IW_FAMILY_CLOSED="
        +
        str(
            summary[
                "full_barker_zell_iw_family_closed"
            ]
        )
    )

    print(
        "GENERIC_DIRAC_IW_ROUTE_CLOSED="
        +
        str(
            summary[
                "generic_dirac_iw_route_closed"
            ]
        )
    )

    print(
        "GENERIC_DIRAC_SOURCE_STATE_ENGINEERING_OPEN="
        +
        str(
            summary[
                "generic_dirac_source_state_engineering_open"
            ]
        )
    )

    print(
        "PRODUCTIVE_CLEAN_V24_1PLUS_SURVIVES="
        +
        str(
            summary[
                "productive_clean_v24_1plus_survives"
            ]
        )
    )

    print(
        "PRODUCTIVE_CLEAN_V24_1PLUS_NORM2="
        +
        str(
            summary[
                "productive_clean_v24_1plus_norm2"
            ]
        )
    )

    print(
        "PRODUCTIVE_CLEAN_V24_2PLUS_SURVIVES="
        +
        str(
            summary[
                "productive_clean_v24_2plus_survives"
            ]
        )
    )

    print(
        "PRODUCTIVE_CLEAN_V24_2PLUS_NORM2="
        +
        str(
            summary[
                "productive_clean_v24_2plus_norm2"
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
        "HOOK17_REFERENCE_CAPACITY_RP1E12_J="
        +
        str(
            summary[
                "hook17_reference_capacity_rp1e12_j"
            ]
        )
    )

    print(
        "HOOK17_COMPLETE_ENERGY_J="
        +
        str(
            summary[
                "hook17_complete_energy_j"
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
        "H17B_AUTHORIZED="
        +
        str(
            summary[
                "h17b_authorized"
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
        "SOURCE_CHANNEL_PATH="
        +
        str(
            source_path
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
