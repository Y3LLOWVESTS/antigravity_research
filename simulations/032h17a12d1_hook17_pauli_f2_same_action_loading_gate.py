"""032H17A12D1 — same-action F2 payload-loading / Pauli overlap gate.

This simulation persists the analytic loading and energy-overlap result.

It deliberately does not rerun the frozen A12C field BVP.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_pauli_f2_same_action_loading import (
    a12c_reference_gate,
    controlled_portal_window_gate,
    h17a12d1_summary,
    maximum_local_loading_lower_bound,
    pauli_loading_overlap_gate,
    unloaded_reference_scaling_at_portal_scale,
)
from antigravity_research.agminer.hook17_pauli_f2_source_reopen import (
    source_energy_at_portal_scale,
)


def main() -> None:
    """Persist A12D1 theorem/scale-overlap results."""

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
        h17a12d1_summary()
    )

    assert summary[
        "minimal_electron_pauli_perturbative_kernel_reuse_closed"
    ] is True

    assert summary[
        "a12b_exact_massless_carrier_closed"
    ] is False

    assert summary[
        "a12c_gauge_invariant_f2_metric_mechanism_closed"
    ] is False

    assert summary[
        "hook17_closed"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a12d1_hook17_pauli_f2_same_action_loading_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a12d1_hook17_pauli_f2_same_action_loading_scan.csv"
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

    overlap = (
        pauli_loading_overlap_gate()
    )

    window = (
        controlled_portal_window_gate()
    )

    reference = (
        a12c_reference_gate()
    )

    scales = [
        (
            "PAULI_CHARACTERISTIC_Q",
            float(
                overlap[
                    "characteristic_q_ev"
                ]
            ),
        ),
        (
            "PAULI_PARTIAL_10MJ_BOUNDARY",
            float(
                overlap[
                    "optimistic_pauli_partial_10mj_upper_portal_scale_ev"
                ]
            ),
        ),
        (
            "A12C_REFERENCE_1KEV",
            float(
                reference[
                    "reference_portal_scale_ev"
                ]
            ),
        ),
        (
            "NECESSARY_ORDER_ONE_LOADING_SCALE",
            float(
                overlap[
                    "necessary_order_one_loading_scale_ev"
                ]
            ),
        ),
        (
            "NECESSARY_TEN_PERCENT_LOADING_SCALE",
            float(
                overlap[
                    "necessary_ten_percent_loading_scale_ev"
                ]
            ),
        ),
        (
            "NECESSARY_ONE_PERCENT_LOADING_SCALE",
            float(
                overlap[
                    "necessary_one_percent_loading_scale_ev"
                ]
            ),
        ),
        (
            "UNLOADED_FIELD_ONLY_10MJ_BOUNDARY",
            float(
                window[
                    "field_only_strict_10mj_upper_portal_scale_ev"
                ]
            ),
        ),
    ]

    rows = []

    for label, scale_ev in scales:
        loading = (
            maximum_local_loading_lower_bound(
                scale_ev
            )
        )

        unloaded = (
            unloaded_reference_scaling_at_portal_scale(
                scale_ev
            )
        )

        pauli = (
            source_energy_at_portal_scale(
                scale_ev
            )
        )

        rows.append(
            {
                "label":
                    label,

                "portal_scale_ev":
                    scale_ev,

                "maximum_local_epsilon_load_lower_bound":
                    loading[
                        "maximum_local_epsilon_load_lower_bound"
                    ],

                "global_loading_le_1_not_ruled_out":
                    loading[
                        "global_loading_le_1_not_ruled_out"
                    ],

                "global_loading_le_0p1_not_ruled_out":
                    loading[
                        "global_loading_le_0p1_not_ruled_out"
                    ],

                "global_loading_le_0p01_not_ruled_out":
                    loading[
                        "global_loading_le_0p01_not_ruled_out"
                    ],

                "unloaded_reference_field_energy_j":
                    unloaded[
                        "unloaded_reference_field_energy_j"
                    ],

                "unloaded_reference_integrated_source_ev_m":
                    unloaded[
                        "unloaded_reference_integrated_source_ev_m"
                    ],

                "optimistic_pauli_electron_rest_floor_j":
                    pauli[
                        "optimistic_electron_rest_floor_j"
                    ],

                "pauli_partial_total_j":
                    pauli[
                        "partial_total_j"
                    ],

                "pauli_partial_strict_sub10mj":
                    (
                        pauli[
                            "partial_total_j"
                        ]
                        <
                        1.0e7
                    ),

                "loaded_solution_computed":
                    False,

                "complete_energy_certified":
                    False,
            }
        )

    with scan_path.open(
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

    density = (
        summary[
            "payload_average_density"
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
        "AVERAGE_PAYLOAD_REST_ENERGY_DENSITY_EV4="
        +
        str(
            density[
                "average_payload_rest_energy_density_ev4"
            ]
        )
    )

    print(
        "A12C_1KEV_MAX_LOCAL_LOADING_LOWER_BOUND="
        +
        str(
            maximum_local_loading_lower_bound(
                1.0e3
            )[
                "maximum_local_epsilon_load_lower_bound"
            ]
        )
    )

    print(
        "PAULI_10MJ_BOUNDARY_EV="
        +
        str(
            overlap[
                "optimistic_pauli_partial_10mj_upper_portal_scale_ev"
            ]
        )
    )

    print(
        "PAULI_BOUNDARY_MAX_LOCAL_LOADING_LOWER_BOUND="
        +
        str(
            overlap[
                "maximum_local_loading_lower_bound_at_pauli_10mj_boundary"
            ]
        )
    )

    print(
        "NECESSARY_ORDER_ONE_LOADING_SCALE_EV="
        +
        str(
            overlap[
                "necessary_order_one_loading_scale_ev"
            ]
        )
    )

    print(
        "NECESSARY_TEN_PERCENT_LOADING_SCALE_EV="
        +
        str(
            overlap[
                "necessary_ten_percent_loading_scale_ev"
            ]
        )
    )

    print(
        "NECESSARY_ONE_PERCENT_LOADING_SCALE_EV="
        +
        str(
            overlap[
                "necessary_one_percent_loading_scale_ev"
            ]
        )
    )

    print(
        "UNLOADED_FIELD_ONLY_10MJ_UPPER_SCALE_EV="
        +
        str(
            window[
                "field_only_strict_10mj_upper_portal_scale_ev"
            ]
        )
    )

    print(
        "ORDER_ONE_LOADING_SCALE_OVER_PAULI_10MJ_BOUNDARY="
        +
        str(
            overlap[
                "order_one_loading_scale_over_pauli_10mj_boundary"
            ]
        )
    )

    print(
        "PAULI_SUB10MJ_AND_ORDER_ONE_LOADING_OVERLAP="
        +
        str(
            overlap[
                "pauli_sub10mj_and_global_order_one_loading_overlap_exists"
            ]
        )
    )

    print(
        "A12C_ONE_PERCENT_LOADING_CANDIDATE_INTERVAL_EXISTS="
        +
        str(
            summary[
                "source_independent_loading_controlled_candidate_window_exists"
            ]
        )
    )

    print(
        "A12B_CARRIER_CLOSED="
        +
        str(
            summary[
                "a12b_exact_massless_carrier_closed"
            ]
        )
    )

    print(
        "A12C_F2_MECHANISM_CLOSED="
        +
        str(
            summary[
                "a12c_gauge_invariant_f2_metric_mechanism_closed"
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
