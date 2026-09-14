"""Simulation 032H17A6R1 — dynamical compensator / Noether Ward theorem.

PURPOSE
-------
Persist the theorem-first A6R1 result after the successful A6 gate.

The simulation tests:

1. exact A6 provenance;
2. the first-divergence V24 two-form source;
3. equivalence of its massless two-form conservation law to the A5/A6 Ward
   identity;
4. the pure exact Stückelberg Noether theorem;
5. the ordinary healthy massless two-form compensator;
6. the remaining physically distinct escape families.

No energy optimization, geometry scan, field solve, or AGMINER database
mutation is performed.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_dynamic_compensator_noether import (
    h17a6r1_summary,
    witness_atlas,
)


def main() -> int:
    """Run and persist 032H17A6R1."""

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

    a6_path = (
        data_dir
        /
        "032h17a6_hook17_j11_common_ward_summary.json"
    )

    if not a6_path.exists():
        raise FileNotFoundError(
            str(
                a6_path
            )
        )

    a6 = json.loads(
        a6_path.read_text(
            encoding="utf-8"
        )
    )

    assert (
        a6[
            "direct_clean_v24_to_j11_closed"
        ]
        is True
    )

    assert (
        a6[
            "productive_1plus_representation_survives"
        ]
        is True
    )

    assert (
        a6[
            "general_local_same_action_compensated_current_closed"
        ]
        is False
    )

    summary = h17a6r1_summary()

    summary_path = (
        data_dir
        /
        "032h17a6r1_hook17_dynamic_compensator_noether_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            indent=
                2,
            sort_keys=
                True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    witnesses = witness_atlas()

    witness_path = (
        data_dir
        /
        "032h17a6r1_hook17_twoform_noether_witnesses.csv"
    )

    with witness_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "witness",
                "q_cov",
                "ward_norm",
                "twoform_conservation_norm",
                "ward_reconstruction_pass",
                "twoform_noether_identity_pass",
                "massless_twoform_source_compatible",
            ],
        )

        writer.writeheader()
        writer.writerows(
            witnesses
        )

    escape_path = (
        data_dir
        /
        "032h17a6r1_hook17_noether_escape_atlas.csv"
    )

    with escape_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "family",
                "status",
                "changes_ward_surface",
                "adds_physical_longitudinal_mode",
                "same_action_requirement",
                "next_action",
            ],
        )

        writer.writeheader()
        writer.writerows(
            summary[
                "escape_atlas"
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
        "A6_PROVENANCE_PASS="
        +
        str(
            summary[
                "a6_provenance_pass"
            ]
        )
    )

    print(
        "PRODUCTIVE_1PLUS_REPRESENTATION_SURVIVES="
        +
        str(
            summary[
                "productive_1plus_representation_survives"
            ]
        )
    )

    print(
        "PURE_EXACT_MASSLESS_STUECKELBERG_CLOSED="
        +
        str(
            summary[
                "pure_exact_massless_stueckelberg_closed"
            ]
        )
    )

    print(
        "HEALTHY_MASSLESS_TWOFORM_COMPENSATOR_CLOSED="
        +
        str(
            summary[
                "healthy_massless_twoform_compensator_closed"
            ]
        )
    )

    print(
        "DECLARED_EXACT_MASSLESS_SINGLE_COMPENSATOR_CLASS_CLOSED="
        +
        str(
            summary[
                "declared_exact_massless_single_compensator_class_closed"
            ]
        )
    )

    print(
        "FULL_NOETHER_COMPLETE_MATTER_COMPENSATOR_CLOSED="
        +
        str(
            summary[
                "full_noether_complete_matter_compensator_closed"
            ]
        )
    )

    print(
        "HIGGSED_OR_MASSIVE_HOOK_CLOSED="
        +
        str(
            summary[
                "higgsed_or_massive_hook_closed"
            ]
        )
    )

    print(
        "MARZO_PROTECTED_STUECKELBERG_FAMILY_CLOSED="
        +
        str(
            summary[
                "marzo_protected_stueckelberg_family_closed"
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
        "STOP_RULE_AFTER_NEXT="
        +
        summary[
            "stop_rule_after_next"
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
        "TWOFORM_WITNESS_PATH="
        +
        str(
            witness_path
        )
    )

    print(
        "NOETHER_ESCAPE_ATLAS_PATH="
        +
        str(
            escape_path
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
