"""032V26E1B1 — quadratic active-state escape simulation."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.v26e1b1_quadratic_active_state_escape import (
    nda_family_gate,
    power_family_rows,
    quadratic_activation_gate,
    quadratic_candidate_classification,
    technical_naturalness_gate,
    v26e1b1_summary,
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

    e1b0_path = (
        data_dir
        /
        "032v26e1b0_pure_j0_provenance_collision_summary.json"
    )

    if not e1b0_path.exists():
        raise FileNotFoundError(
            str(
                e1b0_path
            )
        )

    e1b0 = json.loads(
        e1b0_path.read_text(
            encoding="utf-8"
        )
    )[
        "summary"
    ]

    assert e1b0[
        "exact_v17_equivalent_completion_closed"
    ] is True

    assert e1b0[
        "all_v26d_completions_globally_closed"
    ] is False

    quadratic = quadratic_activation_gate()
    candidate = quadratic_candidate_classification()
    nda = nda_family_gate()
    naturalness = technical_naturalness_gate()
    summary = v26e1b1_summary()

    payload = {
        "quadratic_activation":
            quadratic,

        "quadratic_candidate":
            candidate,

        "nda_family":
            nda,

        "technical_naturalness":
            naturalness,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032v26e1b1_quadratic_active_state_escape_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    family_path = (
        data_dir
        /
        "032v26e1b1_power_activation_family.csv"
    )

    rows = power_family_rows()

    with family_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    nda_path = (
        data_dir
        /
        "032v26e1b1_wilsonian_nda_descendants.csv"
    )

    nda_rows = nda[
        "rows"
    ]

    with nda_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                nda_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(
            nda_rows
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
        "V26E1B0_PROVENANCE_PASS="
        +
        str(
            summary[
                "v26e1b0_provenance_pass"
            ]
        )
    )

    print(
        "QUADRATIC_ACTIVE_STATE_CLASSICAL_ESCAPE="
        +
        str(
            summary[
                "quadratic_active_state_classical_escape"
            ]
        )
    )

    print(
        "QUADRATIC_CANDIDATE_STATUS="
        +
        summary[
            "quadratic_candidate_status"
        ]
    )

    print(
        "QUADRATIC_ETA="
        +
        str(
            summary[
                "quadratic_eta"
            ]
        )
    )

    print(
        "QUADRATIC_ACTIVE_BETA_1="
        +
        str(
            summary[
                "quadratic_active_beta_1"
            ]
        )
    )

    print(
        "QUADRATIC_OFFSTATE_BETA_1="
        +
        str(
            summary[
                "quadratic_offstate_beta_1"
            ]
        )
    )

    print(
        "QUADRATIC_ACTIVE_MAP_MARGIN="
        +
        str(
            summary[
                "quadratic_active_map_margin"
            ]
        )
    )

    print(
        "QUADRATIC_TENSOR_MARGIN="
        +
        str(
            summary[
                "quadratic_tensor_margin"
            ]
        )
    )

    print(
        "QUADRATIC_TREE_R5_TWO_SCALAR_VERTEX_ABSENT="
        +
        str(
            summary[
                "quadratic_tree_r5_two_scalar_vertex_absent"
            ]
        )
    )

    print(
        "POWER_FAMILY_CLASSICAL_ESCAPE_PASS="
        +
        str(
            summary[
                "power_family_classical_escape_pass"
            ]
        )
    )

    print(
        "OLD_OVERLAP_REQUIRED_RELATIVE_OFFSTATE_C1="
        +
        str(
            summary[
                "old_overlap_required_relative_offstate_c1"
            ]
        )
    )

    print(
        "QUADRATIC_NDA_RELATIVE_OFFSTATE_TO_ACTIVE="
        +
        str(
            summary[
                "quadratic_nda_relative_offstate_to_active"
            ]
        )
    )

    print(
        "QUADRATIC_NDA_ADJUSTED_OLD_EMPIRICAL_MIN_EV="
        +
        str(
            summary[
                "quadratic_nda_adjusted_old_empirical_min_ev"
            ]
        )
    )

    print(
        "OLD_ENERGY_METRIC_MAX_EV="
        +
        str(
            summary[
                "old_energy_metric_max_ev"
            ]
        )
    )

    print(
        "QUADRATIC_NDA_RADIATIVE_HEADROOM_PRESENT="
        +
        str(
            summary[
                "quadratic_nda_radiative_headroom_present"
            ]
        )
    )

    print(
        "QUADRATIC_NDA_UNCERTAINTY_HEADROOM_FACTOR="
        +
        str(
            summary[
                "quadratic_nda_uncertainty_headroom_factor"
            ]
        )
    )

    print(
        "NDA_IS_QUANTUM_CERTIFICATION="
        +
        str(
            summary[
                "nda_is_quantum_certification"
            ]
        )
    )

    print(
        "TECHNICAL_NATURALNESS_CERTIFIED="
        +
        str(
            summary[
                "technical_naturalness_certified"
            ]
        )
    )

    print(
        "UV_MATCHING_COMPUTED="
        +
        str(
            summary[
                "uv_matching_computed"
            ]
        )
    )

    print(
        "CURRENT_NATURALNESS_STATUS="
        +
        summary[
            "current_naturalness_status"
        ]
    )

    print(
        "FULL_STATIC_SPACELIKE_SCALAR_HEALTH_ESTABLISHED="
        +
        str(
            summary[
                "full_static_spacelike_scalar_health_established"
            ]
        )
    )

    print(
        "PHYSICAL_G00_CROSS_RESPONSE_ESTABLISHED="
        +
        str(
            summary[
                "physical_g00_cross_response_established"
            ]
        )
    )

    print(
        "MIN_OUTWARD_ACCELERATION_M_S2="
        +
        str(
            summary[
                "minimum_required_outward_acceleration_m_s2"
            ]
        )
    )

    print(
        "MIN_TRUE_STANDOFF_M="
        +
        str(
            summary[
                "minimum_required_true_standoff_m"
            ]
        )
    )

    print(
        "PERFORMANCE_ABOVE_FLOOR_IS_FAVORABLE="
        +
        str(
            summary[
                "performance_above_floor_is_favorable"
            ]
        )
    )

    print(
        "V26D_COMPLETE_ENERGY_J="
        +
        str(
            summary[
                "v26d_complete_energy_j"
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
        "PHYSICAL_ANTIGRAVITY_MODEL_FOUND="
        +
        str(
            summary[
                "physical_antigravity_model_found"
            ]
        )
    )

    print(
        "QUADRATIC_CANDIDATE_PROMOTED_TO_NEXT_PHYSICAL_GATE="
        +
        str(
            summary[
                "quadratic_candidate_promoted_to_next_physical_gate"
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
        "POWER_FAMILY_PATH="
        +
        str(
            family_path
        )
    )

    print(
        "NDA_DESCENDANT_PATH="
        +
        str(
            nda_path
        )
    )


if __name__ == "__main__":
    main()
