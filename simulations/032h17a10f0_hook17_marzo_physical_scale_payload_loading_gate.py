"""032H17A10F0 — physical normalization / payload-loading run."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_marzo_physical_scale_payload_loading import (
    h17a10f0_summary,
)


def main() -> None:
    root = (
        Path(
            __file__
        )
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

    a10e_path = (
        data_dir
        /
        "032h17a10e_hook17_marzo2022_quadratic_universal_metric_summary.json"
    )

    if not a10e_path.exists():
        raise FileNotFoundError(
            str(
                a10e_path
            )
        )

    a10e = json.loads(
        a10e_path.read_text(
            encoding="utf-8"
        )
    )

    assert a10e[
        "branch"
    ] == "032H17A10E"

    assert a10e[
        "partial_green"
    ] is True

    assert a10e[
        "physical_g00_outward_sign"
    ] is True

    assert a10e[
        "one_universal_payload_metric"
    ] is True

    summary = h17a10f0_summary()

    assert summary[
        "partial_green"
    ] is True

    assert summary[
        "physical_planck_normalized_family"
    ][
        "published_health_branch_II_pass"
    ] is True

    assert summary[
        "planck_normalization_kills_one_metre_carrier"
    ] is False

    assert summary[
        "canonical_source_overlap_planck_suppressed"
    ] is False

    assert summary[
        "payload_loading_is_stronger_than_inverse_cube_empirical_limit"
    ] is True

    assert summary[
        "load_controlled_partial_capacity_corridor_open"
    ] is True

    assert summary[
        "complete_energy_established"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a10f0_hook17_marzo_physical_scale_payload_loading_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a10f0_hook17_payload_loading_capacity_scan.csv"
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

    rows = summary[
        "loading_capacity_scan"
    ]

    fields = [
        "target_inside_mR",
        "lambda_ev_m2",
        "empirical_lambda_over_selected_lambda",
        "payload_canonical_amplitude_ev",
        "source_surface_canonical_amplitude_ev",
        "scalar_yukawa_capacity_energy_j",
        "capacity_below_strict_10mj",
    ]

    with scan_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    physical = summary[
        "physical_planck_normalized_family"
    ]

    empirical_load = summary[
        "payload_loading_at_empirical_portal_limit"
    ]

    selected = summary[
        "selected_payload_loading"
    ]

    capacity = summary[
        "selected_capacity_comparator"
    ]

    gradient = summary[
        "source_stueckelberg_gradient_control"
    ]

    threshold = summary[
        "capacity_10mj_loading_threshold"
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
        "PLANCK_NORMALIZED_HEALTH_BRANCH_II="
        +
        str(
            physical[
                "published_health_branch_II_pass"
            ]
        )
    )

    print(
        "MASS_IDENTITY="
        +
        summary[
            "physical_scale_identity"
        ][
            "mass_squared_exact"
        ]
    )

    print(
        "ONE_METRE_MASS_EV="
        +
        str(
            physical[
                "d1_ev"
            ]
        )
    )

    print(
        "D1_OVER_REDUCED_PLANCK="
        +
        str(
            physical[
                "d1_over_reduced_planck"
            ]
        )
    )

    print(
        "HUGE_C7_REQUIRED="
        +
        str(
            summary[
                "huge_c7_required_for_one_metre_range"
            ]
        )
    )

    print(
        "CANONICAL_SOURCE_COUPLING="
        +
        str(
            physical[
                "canonical_source_coupling_magnitude"
            ]
        )
    )

    print(
        "CANONICAL_SOURCE_PLANCK_SUPPRESSED="
        +
        str(
            summary[
                "canonical_source_overlap_planck_suppressed"
            ]
        )
    )

    print(
        "EMPIRICAL_PORTAL_LAMBDA_MAX_EV_M2="
        +
        str(
            summary[
                "empirical_quadratic_metric_gate"
            ][
                "lambda_empirical_max_ev_m2"
            ]
        )
    )

    print(
        "EMPIRICAL_LIMIT_PAYLOAD_M_IN_R="
        +
        str(
            empirical_load[
                "inside_mR"
            ]
        )
    )

    print(
        "EMPIRICAL_LIMIT_FINITE_PAYLOAD_SAFE="
        +
        str(
            summary[
                "empirical_portal_limit_is_finite_payload_safe"
            ]
        )
    )

    print(
        "SELECTED_LOAD_TARGET_M_IN_R="
        +
        str(
            summary[
                "selected_loading_target_mR"
            ]
        )
    )

    print(
        "SELECTED_LOAD_CONTROL_LAMBDA_EV_M2="
        +
        str(
            summary[
                "selected_loading_lambda_ev_m2"
            ]
        )
    )

    print(
        "SELECTED_RECONSTRUCTED_M_IN_R="
        +
        str(
            selected[
                "inside_mR"
            ]
        )
    )

    print(
        "SELECTED_PAYLOAD_FIELD_MEV="
        +
        str(
            capacity[
                "payload_canonical_amplitude_ev"
            ]
            /
            1.0e6
        )
    )

    print(
        "SELECTED_PARTIAL_CAPACITY_J="
        +
        str(
            capacity[
                "scalar_yukawa_capacity_energy_j"
            ]
        )
    )

    print(
        "SELECTED_PARTIAL_CAPACITY_FRACTION_10MJ="
        +
        str(
            summary[
                "selected_partial_capacity_fraction_of_10mj"
            ]
        )
    )

    print(
        "SOURCE_Q_OVER_F="
        +
        str(
            gradient[
                "q_over_f"
            ]
        )
    )

    print(
        "CAPACITY_10MJ_CROSSING_M_IN_R="
        +
        str(
            threshold[
                "capacity_10mj_crossing_mR"
            ]
        )
    )

    print(
        "LOAD_CONTROLLED_PARTIAL_CAPACITY_CORRIDOR="
        +
        str(
            summary[
                "load_controlled_partial_capacity_corridor_open"
            ]
        )
    )

    print(
        "EXACT_FINITE_PAYLOAD_ESTABLISHED="
        +
        str(
            summary[
                "finite_payload_established"
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
        "SCAN_PATH="
        +
        str(
            scan_path
        )
    )


if __name__ == "__main__":
    main()
