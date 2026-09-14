"""Simulation 032H17A8 — protected 2+ atlas / projective rerank.

No continuous parameter scan is performed.

No energy optimization is performed.

This run persists:
- the scoped BMS protected-spin2 theorem;
- the healthy-but-unprotected Mikura-Percacci 2+ branch;
- the Percacci-Sezgin projective family;
- exact clean-V24 projective source trace contractions;
- the next-family rerank.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_native_protected_2plus_atlas import (
    bms_pair_antisymmetric_spin2_protection_gate,
    clean_v24_projective_spin_rerank_gate,
    clean_v24_projective_trace_gate,
    h17a8_summary,
    mikura_percacci_hook_2plus_gate,
    percacci_sezgin_projective_family_gate,
    protected_2plus_atlas_rows,
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

    a7_path = (
        data_dir
        /
        "032h17a7_hook17_barker_zell_iso_weyl_source_match_summary.json"
    )

    if not a7_path.exists():
        raise FileNotFoundError(
            str(
                a7_path
            )
        )

    a7_payload = json.loads(
        a7_path.read_text(
            encoding="utf-8"
        )
    )

    a7 = a7_payload[
        "summary"
    ]

    assert (
        a7[
            "direct_clean_v24_barker_zell_iw_vector_route_closed"
        ]
        is True
    )

    assert (
        a7[
            "productive_clean_v24_1plus_survives"
        ]
        is True
    )

    assert (
        a7[
            "productive_clean_v24_2plus_survives"
        ]
        is True
    )

    bms = (
        bms_pair_antisymmetric_spin2_protection_gate()
    )

    mp = (
        mikura_percacci_hook_2plus_gate()
    )

    ps = (
        percacci_sezgin_projective_family_gate()
    )

    trace = (
        clean_v24_projective_trace_gate()
    )

    rerank = (
        clean_v24_projective_spin_rerank_gate()
    )

    summary = h17a8_summary()

    payload = {
        "bms_pair_antisymmetric_spin2_protection":
            bms,

        "mikura_percacci_hook_2plus":
            mp,

        "percacci_sezgin_projective_family":
            ps,

        "clean_v24_projective_trace":
            trace,

        "clean_v24_projective_spin_rerank":
            rerank,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032h17a8_hook17_native_protected_2plus_atlas_summary.json"
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

    atlas_path = (
        data_dir
        /
        "032h17a8_hook17_protected_2plus_atlas.csv"
    )

    with atlas_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "family",
                "healthy_2plus",
                "symmetry_protected",
                "clean_v24_2plus_available",
                "protected_2plus_survivor",
                "status",
            ],
        )

        writer.writeheader()
        writer.writerows(
            protected_2plus_atlas_rows()
        )

    trace_path = (
        data_dir
        /
        "032h17a8_hook17_projective_source_trace_summary.json"
    )

    trace_path.write_text(
        json.dumps(
            trace,
            indent=
                2,
            sort_keys=
                True,
        )
        +
        "\n",
        encoding="utf-8",
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
        "A7_PROVENANCE_PASS="
        +
        str(
            summary[
                "a7_provenance_pass"
            ]
        )
    )

    print(
        "BMS_CONFIRMED_UNITARY_MODELS="
        +
        str(
            bms[
                "confirmed_unitary_models"
            ]
        )
    )

    print(
        "BMS_SYMMETRY_SUPPORTED_SPIN2_FOUND="
        +
        str(
            bms[
                "symmetry_supporting_spin_two_found"
            ]
        )
    )

    print(
        "MIKURA_PERCACCI_HEALTHY_2PLUS_EXISTS="
        +
        str(
            summary[
                "mikura_percacci_healthy_2plus_exists"
            ]
        )
    )

    print(
        "MIKURA_PERCACCI_2PLUS_PROTECTION_ESTABLISHED="
        +
        str(
            summary[
                "mikura_percacci_2plus_protection_established"
            ]
        )
    )

    print(
        "PERCACCI_SEZGIN_PROJECTIVE_FAMILY_EXISTS="
        +
        str(
            summary[
                "percacci_sezgin_projective_family_exists"
            ]
        )
    )

    print(
        "PERCACCI_SEZGIN_EXTRA_MASSIVE_2PLUS_EXISTS="
        +
        str(
            summary[
                "percacci_sezgin_extra_massive_2plus_exists"
            ]
        )
    )

    print(
        "PERCACCI_SEZGIN_PROTECTED_1PLUS_EXISTS="
        +
        str(
            summary[
                "percacci_sezgin_protected_1plus_exists"
            ]
        )
    )

    print(
        "CLEAN_V24_PROJECTIVE_TRACE12="
        +
        str(
            trace[
                "trace_first_second"
            ]
        )
    )

    print(
        "CLEAN_V24_PROJECTIVE_TRACE23="
        +
        str(
            trace[
                "trace_second_third"
            ]
        )
    )

    print(
        "CLEAN_V24_PROJECTIVE_SOURCE_TRACE_CONSTRAINTS_PASS="
        +
        str(
            summary[
                "clean_v24_projective_source_trace_constraints_pass"
            ]
        )
    )

    print(
        "CLEAN_V24_PROJECTIVE_2MINUS_SUPPORT_ZERO="
        +
        str(
            summary[
                "clean_v24_projective_2minus_support_zero"
            ]
        )
    )

    print(
        "CLEAN_V24_PROJECTIVE_1PLUS_SUPPORT_NONZERO="
        +
        str(
            summary[
                "clean_v24_projective_1plus_support_nonzero"
            ]
        )
    )

    print(
        "PROJECTIVE_1PLUS_EXACT_SOURCE_MATCH_AUTHORIZED="
        +
        str(
            summary[
                "projective_1plus_exact_source_match_authorized"
            ]
        )
    )

    print(
        "CURRENT_PROTECTED_2PLUS_ATLAS_SURVIVORS="
        +
        str(
            summary[
                "current_declared_protected_2plus_atlas_survivor_count"
            ]
        )
    )

    print(
        "ALL_PROTECTED_2PLUS_GLOBALLY_CLOSED="
        +
        str(
            summary[
                "all_possible_protected_2plus_globally_closed"
            ]
        )
    )

    print(
        "PRODUCTIVE_CLEAN_V24_1PLUS_NORM2="
        +
        str(
            summary[
                "clean_v24_1plus_norm2"
            ]
        )
    )

    print(
        "PRODUCTIVE_CLEAN_V24_2PLUS_NORM2="
        +
        str(
            summary[
                "clean_v24_2plus_norm2"
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
        "ATLAS_PATH="
        +
        str(
            atlas_path
        )
    )

    print(
        "PROJECTIVE_TRACE_PATH="
        +
        str(
            trace_path
        )
    )


if __name__ == "__main__":
    main()
