"""032H17A10F2 — strict payload + source-naturalness closeout."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_marzo_source_naturalness_closeout import (
    h17a10f2_summary,
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

    f1_path = (
        data_dir
        /
        "032h17a10f1_hook17_marzo_finite_transverse_payload_bvp_summary.json"
    )

    if not f1_path.exists():
        raise FileNotFoundError(
            str(
                f1_path
            )
        )

    f1 = json.loads(
        f1_path.read_text(
            encoding="utf-8"
        )
    )

    assert f1[
        "branch"
    ] == "032H17A10F1"

    assert f1[
        "partial_green"
    ] is True

    summary = h17a10f2_summary()

    strict = summary[
        "strict_payload_floor"
    ]

    naturalness = summary[
        "electron_threshold_naturalness"
    ]

    longitudinal = summary[
        "longitudinal_diagnostic"
    ]

    hypothetical = summary[
        "hypothetical_weak_current_escape"
    ]

    assert summary[
        "strict_reduced_eft_1g_1m_payload_performance_survives"
    ] is True

    assert summary[
        "current_ordinary_dirac_wheeler_marzo_realization_blocked"
    ] is True

    assert summary[
        "expensive_full_nonlinear_bvp_authorized"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a10f2_hook17_marzo_source_naturalness_closeout_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a10f2_hook17_source_naturalness_scan.csv"
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

    rows = []

    for row in naturalness[
        "rows"
    ]:
        rows.append(
            {
                "kind":
                    "CURRENT_COUPLING_NDA",

                "loop_coefficient":
                    row[
                        "loop_coefficient"
                    ],

                "epsilon":
                    1.0,

                "delta_m2_over_target":
                    row[
                        "nda_delta_mass_squared_over_target"
                    ],

                "partial_energy_j":
                    "",

                "naturalness_energy_overlap":
                    False,
            }
        )

    for row in hypothetical[
        "rows"
    ]:
        rows.append(
            {
                "kind":
                    "HYPOTHETICAL_EPSILON_ESCAPE",

                "loop_coefficient":
                    row[
                        "loop_coefficient"
                    ],

                "epsilon":
                    row[
                        "epsilon_naturalness_max"
                    ],

                "delta_m2_over_target":
                    1.0,

                "partial_energy_j":
                    row[
                        "field_plus_source_rest_at_naturalness_epsilon_j"
                    ],

                "naturalness_energy_overlap":
                    row[
                        "naturalness_energy_overlap"
                    ],
            }
        )

    with scan_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "kind",
                "loop_coefficient",
                "epsilon",
                "delta_m2_over_target",
                "partial_energy_j",
                "naturalness_energy_overlap",
            ],
        )

        writer.writeheader()
        writer.writerows(
            rows
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
        "STRICT_PAYLOAD_ORIGINAL_LOCAL_MIN_M_S2="
        +
        str(
            strict[
                "original_local_min_acceleration_m_s2"
            ]
        )
    )

    print(
        "STRICT_PAYLOAD_AMPLITUDE_SCALE="
        +
        str(
            strict[
                "required_field_source_amplitude_scale"
            ]
        )
    )

    print(
        "STRICT_PAYLOAD_ENERGY_SCALE="
        +
        str(
            strict[
                "required_acceleration_energy_scale"
            ]
        )
    )

    print(
        "STRICT_PAYLOAD_LOCAL_MIN_M_S2="
        +
        str(
            strict[
                "strict_local_min_acceleration_m_s2"
            ]
        )
    )

    print(
        "STRICT_PAYLOAD_COM_M_S2="
        +
        str(
            strict[
                "strict_payload_com_acceleration_m_s2"
            ]
        )
    )

    print(
        "STRICT_FIELD_ENERGY_J="
        +
        str(
            strict[
                "strict_field_loading_energy_j"
            ]
        )
    )

    print(
        "STRICT_SOURCE_PAIR_COUNT="
        +
        str(
            strict[
                "strict_source_pair_count"
            ]
        )
    )

    print(
        "STRICT_FIELD_PLUS_ELECTRON_REST_J="
        +
        str(
            strict[
                "strict_field_plus_electron_rest_partial_j"
            ]
        )
    )

    print(
        "STRICT_FIELD_PLUS_PROTON_REST_J="
        +
        str(
            strict[
                "strict_field_plus_proton_rest_partial_j"
            ]
        )
    )

    print(
        "STRICT_REDUCED_EFT_1G_1M_PAYLOAD_PASS="
        +
        str(
            summary[
                "strict_reduced_eft_1g_1m_payload_performance_survives"
            ]
        )
    )

    print(
        "CONSTITUENT_COUPLING_LOWER_BOUND="
        +
        str(
            summary[
                "microscopic_coupling"
            ][
                "constituent_coupling_lower_bound"
            ]
        )
    )

    print(
        "CURRENT_ACTION_SMALL_SOURCE_COUPLING_KNOB="
        +
        str(
            summary[
                "microscopic_coupling"
            ][
                "current_action_has_free_small_source_coupling"
            ]
        )
    )

    print(
        "STUECKELBERG_F_EV="
        +
        str(
            summary[
                "stueckelberg_protection"
            ][
                "stueckelberg_f_abs_ev"
            ]
        )
    )

    print(
        "BARE_CURRENT_EXACT_CONSERVATION_ESTABLISHED="
        +
        str(
            summary[
                "stueckelberg_protection"
            ][
                "operator_level_exact_engineered_current_conservation_established"
            ]
        )
    )

    print(
        "ELECTRON_OVER_F="
        +
        str(
            longitudinal[
                "electron_energy_over_f"
            ]
        )
    )

    print(
        "LONGITUDINAL_G_E_OVER_F="
        +
        str(
            longitudinal[
                "longitudinal_enhancement_gE_over_f_at_electron_threshold"
            ]
        )
    )

    print(
        "NOMINAL_4PI_F_OVER_G_SCALE_EV="
        +
        str(
            longitudinal[
                "nominal_4pi_f_over_g_scale_ev"
            ]
        )
    )

    print(
        "NOMINAL_ELECTRON_NDA_DELTA_M2_OVER_TARGET="
        +
        str(
            naturalness[
                "rows"
            ][
                0
            ][
                "nda_delta_mass_squared_over_target"
            ]
        )
    )

    print(
        "LOOP_COEFFICIENT_REQUIRED_FOR_NATURAL_MASS="
        +
        str(
            naturalness[
                "loop_coefficient_required_for_delta_m2_at_most_target"
            ]
        )
    )

    print(
        "HYPOTHETICAL_EPSILON_ENERGY_MIN="
        +
        str(
            hypothetical[
                "epsilon_energy_min_for_electron_partial_below_10mj"
            ]
        )
    )

    print(
        "HYPOTHETICAL_EPSILON_NATURALNESS_MAX_C1="
        +
        str(
            hypothetical[
                "epsilon_naturalness_max_for_c_loop_1"
            ]
        )
    )

    print(
        "HYPOTHETICAL_SIMPLE_EPSILON_OVERLAP="
        +
        str(
            not hypothetical[
                "all_tested_coefficients_have_no_energy_naturalness_overlap"
            ]
        )
    )

    print(
        "LOOP_COEFFICIENT_NEEDED_FOR_EPSILON_OVERLAP="
        +
        str(
            hypothetical[
                "loop_coefficient_needed_before_simple_epsilon_overlap"
            ]
        )
    )

    print(
        "CURRENT_ORDINARY_DIRAC_NATURALNESS_CERTIFIED="
        +
        str(
            summary[
                "current_ordinary_dirac_source_technical_naturalness_certified"
            ]
        )
    )

    print(
        "CURRENT_WHEELER_MARZO_REALIZATION_BLOCKED="
        +
        str(
            summary[
                "current_ordinary_dirac_wheeler_marzo_realization_blocked"
            ]
        )
    )

    print(
        "EXPENSIVE_NONLINEAR_RUN_AUTHORIZED="
        +
        str(
            summary[
                "expensive_full_nonlinear_bvp_authorized"
            ]
        )
    )

    print(
        "MARZO_1MINUS_FAMILY_GLOBALLY_CLOSED="
        +
        str(
            summary[
                "marzo_protected_1minus_family_globally_closed"
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
