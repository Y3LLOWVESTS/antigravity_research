"""Simulation 032H17A6R2 — Marzo-2022 protected massive MAG source match.

PURPOSE
-------
Persist the first direct clean-V24 source-representation test against a
concrete published healthy massive/Stueckelberg metric-affine family after
H17A6R1.

The calculation is theorem-first.

It does not scan continuous parameters.

It does not calculate energy.

It does not solve a field equation.

It asks whether the actual clean microscopic V24 source has any rest-frame
support in the only physical massive spin/parity pole of the published
Marzo-2022 protected family.

OUTPUTS
-------
results/data/
    032h17a6r2_hook17_marzo2022_massive_source_match_summary.json

    032h17a6r2_hook17_clean_v24_parity_support.csv

    032h17a6r2_hook17_post_massive_rescue_rerank.csv

CLAIM LIMIT
-----------
A zero direct healthy-pole projector closes only the clean equal-rest V24
source into this published 1- carrier.

It does not close generic Dirac states, static off-shell constrained
response, other protected 1+/2+ families, or HOOK17 globally.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_marzo2022_massive_source_match import (
    clean_v24_full_1minus_source_gate,
    clean_v24_hook_parity_gate,
    clean_v24_totally_symmetric_parity_gate,
    generic_dirac_escape_gate,
    h17a6r2_summary,
    marzo2022_clean_v24_source_match_gate,
    marzo2022_published_family_gate,
    source_support_rows,
)


def main() -> int:
    """Run the A6R2 source-match gate and persist durable artifacts."""

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

    r1_path = (
        data_dir
        /
        "032h17a6r1_hook17_dynamic_compensator_noether_summary.json"
    )

    if not r1_path.exists():
        raise FileNotFoundError(
            str(
                r1_path
            )
        )

    r1 = json.loads(
        r1_path.read_text(
            encoding="utf-8"
        )
    )

    assert (
        r1[
            "declared_exact_massless_single_compensator_class_closed"
        ]
        is True
    )

    assert (
        r1[
            "higgsed_or_massive_hook_closed"
        ]
        is False
    )

    assert (
        r1[
            "marzo_protected_stueckelberg_family_closed"
        ]
        is False
    )

    assert (
        r1[
            "hook17_closed"
        ]
        is False
    )

    family = (
        marzo2022_published_family_gate()
    )

    symmetric = (
        clean_v24_totally_symmetric_parity_gate()
    )

    hook = (
        clean_v24_hook_parity_gate()
    )

    full = (
        clean_v24_full_1minus_source_gate()
    )

    source_match = (
        marzo2022_clean_v24_source_match_gate()
    )

    generic = (
        generic_dirac_escape_gate()
    )

    summary = (
        h17a6r2_summary()
    )

    payload = {
        "r1_provenance":
            r1,

        "published_marzo2022_family":
            family,

        "clean_v24_totally_symmetric_parity":
            symmetric,

        "clean_v24_hook_parity":
            hook,

        "clean_v24_full_1minus_source":
            full,

        "marzo2022_clean_source_match":
            source_match,

        "generic_dirac_escape":
            generic,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032h17a6r2_hook17_marzo2022_massive_source_match_summary.json"
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

    support_path = (
        data_dir
        /
        "032h17a6r2_hook17_clean_v24_parity_support.csv"
    )

    with support_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "source_sector",
                "support_nonzero",
                "support_norm2",
                "status",
            ],
        )

        writer.writeheader()
        writer.writerows(
            source_support_rows()
        )

    rerank_path = (
        data_dir
        /
        "032h17a6r2_hook17_post_massive_rescue_rerank.csv"
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
        "MARZO2022_PUBLISHED_PROTECTED_MASSIVE_FAMILY_EXISTS="
        +
        str(
            summary[
                "marzo2022_published_protected_massive_family_exists"
            ]
        )
    )

    print(
        "MARZO2022_MASSIVE_PHYSICAL_POLE_SECTOR="
        +
        summary[
            "marzo2022_massive_physical_pole_sector"
        ]
    )

    print(
        "CLEAN_TOTAL_SYMMETRIC_NONZERO_COMPONENT_COUNT="
        +
        str(
            symmetric[
                "nonzero_component_count"
            ]
        )
    )

    print(
        "CLEAN_TOTAL_SYMMETRIC_ALL_NONZERO_HAVE_ONE_TIME_INDEX="
        +
        str(
            symmetric[
                "all_nonzero_components_have_exactly_one_time_index"
            ]
        )
    )

    print(
        "CLEAN_TOTAL_SYMMETRIC_S00I_ZERO="
        +
        str(
            symmetric[
                "s_00i_zero"
            ]
        )
    )

    print(
        "CLEAN_TOTAL_SYMMETRIC_SIJK_ZERO="
        +
        str(
            symmetric[
                "s_ijk_zero"
            ]
        )
    )

    print(
        "CLEAN_TOTAL_SYMMETRIC_1MINUS_SUPPORT_ZERO="
        +
        str(
            symmetric[
                "totally_symmetric_1minus_support_zero"
            ]
        )
    )

    print(
        "CLEAN_HOOK_1MINUS_SUPPORT_ZERO="
        +
        str(
            hook[
                "hook_1minus_support_zero"
            ]
        )
    )

    print(
        "CLEAN_FULL_V24_1MINUS_SUPPORT_ZERO="
        +
        str(
            summary[
                "clean_v24_full_1minus_support_zero"
            ]
        )
    )

    print(
        "DIRECT_CLEAN_V24_MARZO2022_HEALTHY_POLE_SOURCE_ZERO="
        +
        str(
            source_match[
                "direct_clean_v24_healthy_massive_pole_source_zero"
            ]
        )
    )

    print(
        "DIRECT_CLEAN_V24_MARZO2022_MASSIVE_1MINUS_CLOSED="
        +
        str(
            summary[
                "direct_clean_v24_marzo2022_massive_1minus_closed"
            ]
        )
    )

    print(
        "STATIC_OFFSHELL_MARZO2022_RESPONSE_CLOSED="
        +
        str(
            summary[
                "static_offshell_marzo2022_response_closed"
            ]
        )
    )

    print(
        "GENERIC_DIRAC_MARZO2022_SOURCE_CLOSED="
        +
        str(
            summary[
                "generic_dirac_marzo2022_source_closed"
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
        "PRODUCTIVE_CLEAN_V24_2PLUS_SURVIVES="
        +
        str(
            summary[
                "productive_clean_v24_2plus_survives"
            ]
        )
    )

    print(
        "ALL_HIGGSED_OR_MASSIVE_HOOK_CLOSED="
        +
        str(
            summary[
                "all_higgsed_or_massive_hook_closed"
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
        "SOURCE_SUPPORT_PATH="
        +
        str(
            support_path
        )
    )

    print(
        "RERANK_PATH="
        +
        str(
            rerank_path
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
