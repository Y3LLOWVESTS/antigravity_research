"""032H17A12D0 — final-session low-capacity F^2 consolidation."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_low_capacity_f2_completion_atlas import (
    completion_combination_atlas,
    field_sector_portal_atlas,
    h17a12d0_summary,
    source_completion_atlas,
)


def _csv_safe_row(
    row: dict,
) -> dict:
    """Convert list-valued fields into stable pipe-separated CSV cells."""

    result = dict(
        row
    )

    for key, value in list(
        result.items()
    ):
        if isinstance(
            value,
            list,
        ):
            result[
                key
            ] = "|".join(
                str(item)
                for item in value
            )

    return result


def _write_rows(
    path: Path,
    rows: list[dict],
) -> None:
    """Write heterogeneous atlas rows using a union of field names."""

    fields: list[str] = []

    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(
                    key
                )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(
                _csv_safe_row(
                    row
                )
            )


def main() -> None:
    """Run A12D0 and persist session-closeout state."""

    root = (
        Path(__file__)
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

    summary = (
        h17a12d0_summary()
    )

    assert summary[
        "provenance"
    ][
        "pass"
    ] is True

    assert summary[
        "low_capacity_mechanism_reference_preserved"
    ] is True

    assert summary[
        "quadratic_metric_basis"
    ][
        "basis_exhaustive_within_declared_scope"
    ] is True

    assert summary[
        "quadratic_metric_basis"
    ][
        "pure_magnetostatic_unique_g00_result_pass"
    ] is True

    assert summary[
        "documentation_update_authorized"
    ] is True

    assert summary[
        "physical_antigravity_model_found"
    ] is False

    assert summary[
        "certified_sub10mj_model_found"
    ] is False

    reference = summary[
        "frozen_low_capacity_reference"
    ]

    summary_path = (
        data_dir
        /
        "032h17a12d0_hook17_low_capacity_f2_completion_atlas_summary.json"
    )

    reference_path = (
        data_dir
        /
        "032h17a12d0_hook17_low_capacity_reference.csv"
    )

    metric_path = (
        data_dir
        /
        "032h17a12d0_hook17_quadratic_metric_sector_atlas.csv"
    )

    source_path = (
        data_dir
        /
        "032h17a12d0_hook17_source_completion_atlas.csv"
    )

    combination_path = (
        data_dir
        /
        "032h17a12d0_hook17_completion_combination_atlas.csv"
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

    _write_rows(
        reference_path,
        [
            reference
        ],
    )

    _write_rows(
        metric_path,
        field_sector_portal_atlas(),
    )

    _write_rows(
        source_path,
        source_completion_atlas(),
    )

    _write_rows(
        combination_path,
        completion_combination_atlas(),
    )

    metric = summary[
        "quadratic_metric_basis"
    ]

    top = summary[
        "top_completion"
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
        "PROVENANCE_PASS="
        +
        str(
            summary[
                "provenance"
            ][
                "pass"
            ]
        )
    )

    print(
        "LOW_CAPACITY_REFERENCE_FROZEN="
        +
        str(
            reference[
                "reference_kernel_frozen"
            ]
        )
    )

    print(
        "REFERENCE_PORTAL_SCALE_EV="
        +
        str(
            reference[
                "reference_portal_scale_ev"
            ]
        )
    )

    print(
        "REFERENCE_FIELD_ENERGY_J="
        +
        str(
            reference[
                "field_energy_j"
            ]
        )
    )

    print(
        "REFERENCE_SOURCE_WORK_J="
        +
        str(
            reference[
                "source_work_j"
            ]
        )
    )

    print(
        "REFERENCE_SOURCE_WORK_RELATIVE_ERROR="
        +
        str(
            reference[
                "source_work_relative_error"
            ]
        )
    )

    print(
        "REFERENCE_PAYLOAD_MASS_KG="
        +
        str(
            reference[
                "payload_mass_kg"
            ]
        )
    )

    print(
        "REFERENCE_STANDOFF_M="
        +
        str(
            reference[
                "geometric_external_standoff_m"
            ]
        )
    )

    print(
        "REFERENCE_PAYLOAD_MIN_ACCEL_M_S2="
        +
        str(
            reference[
                "payload_local_acceleration_min_m_s2"
            ]
        )
    )

    print(
        "REFERENCE_PAYLOAD_MAX_ACCEL_M_S2="
        +
        str(
            reference[
                "payload_local_acceleration_max_m_s2"
            ]
        )
    )

    print(
        "REFERENCE_PAYLOAD_COM_ACCEL_M_S2="
        +
        str(
            reference[
                "payload_com_acceleration_m_s2"
            ]
        )
    )

    print(
        "FIELD_ENERGY_IMPROVEMENT_VS_A10F2="
        +
        str(
            reference[
                "field_energy_improvement_factor_vs_a10f2"
            ]
        )
    )

    print(
        "FIELD_TERM_BELOW_100J="
        +
        str(
            reference[
                "field_term_below_100j"
            ]
        )
    )

    print(
        "FIELD_EFFICIENCY_OPTIMIZATION_AUTHORIZED="
        +
        str(
            reference[
                "field_efficiency_optimization_authorized"
            ]
        )
    )

    print(
        "QUADRATIC_METRIC_BASIS_EXHAUSTIVE_WITHIN_SCOPE="
        +
        str(
            metric[
                "basis_exhaustive_within_declared_scope"
            ]
        )
    )

    print(
        "ODD_RANK2_IDENTITY_PASS="
        +
        str(
            metric[
                "odd_rank2_identity_pass"
            ]
        )
    )

    print(
        "DUALDUAL_IDENTITY_PASS="
        +
        str(
            metric[
                "dualdual_identity_pass"
            ]
        )
    )

    print(
        "PURE_MAGNETOSTATIC_USEFUL_QUADRATIC_G00_DIMENSION="
        +
        str(
            metric[
                "pure_magnetostatic_useful_static_g00_basis_dimension"
            ]
        )
    )

    print(
        "PURE_MAGNETOSTATIC_UNIQUE_QUADRATIC_G00_PORTAL="
        +
        metric[
            "pure_magnetostatic_unique_quadratic_algebraic_g00_portal"
        ]
    )

    print(
        "FIELD_SECTOR_PORTAL_COUNT="
        +
        str(
            summary[
                "field_sector_portal_count"
            ]
        )
    )

    print(
        "STRUCTURALLY_OPEN_PORTAL_COUNT="
        +
        str(
            summary[
                "structurally_open_portal_count"
            ]
        )
    )

    print(
        "SOURCE_FAMILY_COUNT="
        +
        str(
            summary[
                "source_family_count"
            ]
        )
    )

    print(
        "OPEN_OR_RESEARCHABLE_SOURCE_FAMILY_COUNT="
        +
        str(
            summary[
                "open_or_researchable_source_family_count"
            ]
        )
    )

    print(
        "COMPLETION_COMBINATION_COUNT="
        +
        str(
            summary[
                "completion_combination_count"
            ]
        )
    )

    print(
        "OPEN_COMPLETION_COMBINATION_COUNT="
        +
        str(
            summary[
                "open_completion_combination_count"
            ]
        )
    )

    print(
        "TOP_SOURCE_COMPLETION="
        +
        top[
            "source_id"
        ]
    )

    print(
        "TOP_METRIC_PORTAL="
        +
        top[
            "portal_id"
        ]
    )

    print(
        "TOP_EXACT_A12C_KERNEL_REUSE="
        +
        str(
            top[
                "exact_a12c_kernel_reuse"
            ]
        )
    )

    print(
        "TOP_PRIORITY_SCORE_NOT_PROBABILITY="
        +
        str(
            top[
                "priority_score_not_probability"
            ]
        )
    )

    print(
        "A12B_EXACT_MASSLESS_CARRIER_PRESERVED="
        +
        str(
            summary[
                "a12b_exact_massless_carrier_preserved"
            ]
        )
    )

    print(
        "A12C_F2_METRIC_MECHANISM_PRESERVED="
        +
        str(
            summary[
                "a12c_f2_metric_mechanism_preserved"
            ]
        )
    )

    print(
        "A12C_ORDINARY_EM_LIKE_ROUTE_REMAINS_CLOSED="
        +
        str(
            summary[
                "a12c_ordinary_em_like_route_remains_closed"
            ]
        )
    )

    print(
        "NEW_PHYSICS_DISCOVERY_CLAIM="
        +
        str(
            summary[
                "new_physics_discovery_claim"
            ]
        )
    )

    print(
        "PROJECT_LEVEL_MECHANISM_RESULT="
        +
        str(
            summary[
                "project_level_mechanism_result"
            ]
        )
    )

    print(
        "COMPLETE_ENERGY_ESTABLISHED="
        +
        str(
            summary[
                "complete_energy_established"
            ]
        )
    )

    print(
        "PHYSICAL_ANTIGRAVITY_MODEL_FOUND="
        +
        str(
            summary[
                "physical_antigravity_model_found"
            ]
        )
    )

    print(
        "CERTIFIED_SUB10MJ_MODEL_FOUND="
        +
        str(
            summary[
                "certified_sub10mj_model_found"
            ]
        )
    )

    print(
        "DOCUMENTATION_UPDATE_AUTHORIZED="
        +
        str(
            summary[
                "documentation_update_authorized"
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
        "REFERENCE_PATH="
        +
        str(
            reference_path
        )
    )

    print(
        "METRIC_ATLAS_PATH="
        +
        str(
            metric_path
        )
    )

    print(
        "SOURCE_ATLAS_PATH="
        +
        str(
            source_path
        )
    )

    print(
        "COMBINATION_ATLAS_PATH="
        +
        str(
            combination_path
        )
    )


if __name__ == "__main__":
    main()
