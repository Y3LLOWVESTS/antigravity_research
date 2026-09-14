"""Simulation 032H17A9 — exact Percacci-Sezgin 1+ source gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_percacci_sezgin_1plus_projector import (
    diffeomorphism_ward_gate,
    exact_ps_1plus_pole_source_gate,
    h17a9_summary,
    percacci_sezgin_case_i_gate,
    projected_projective_trace_gate,
    source_component_rows,
    torsion_free_projection_identity_gate,
    torsion_free_source_gate,
    wheeler_ps_source_map_gate,
)


def main() -> None:
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

    a8_path = (
        data_dir
        /
        "032h17a8_hook17_native_protected_2plus_atlas_summary.json"
    )

    if not a8_path.exists():
        raise FileNotFoundError(
            str(a8_path)
        )

    a8_payload = json.loads(
        a8_path.read_text(
            encoding="utf-8"
        )
    )

    a8 = a8_payload["summary"]

    assert (
        a8[
            "projective_1plus_exact_source_match_authorized"
        ]
        is True
    )

    assert (
        a8[
            "clean_v24_projective_source_trace_constraints_pass"
        ]
        is True
    )

    case = percacci_sezgin_case_i_gate()
    source_map = wheeler_ps_source_map_gate()
    projection = torsion_free_source_gate()
    identity = torsion_free_projection_identity_gate()
    trace = projected_projective_trace_gate()
    pole = exact_ps_1plus_pole_source_gate()
    diffeo = diffeomorphism_ward_gate()
    summary = h17a9_summary()

    payload = {
        "case_i":
            case,

        "source_map":
            source_map,

        "torsion_free_projection":
            projection,

        "projection_identity":
            identity,

        "projective_trace":
            trace,

        "exact_1plus_pole":
            pole,

        "diffeomorphism_ward":
            diffeo,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032h17a9_hook17_percacci_sezgin_1plus_projector_summary.json"
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

    source_path = (
        data_dir
        /
        "032h17a9_hook17_ps1plus_source_components.csv"
    )

    with source_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "stage",
                "c",
                "a",
                "b",
                "value",
            ],
        )

        writer.writeheader()

        writer.writerows(
            source_component_rows()
        )

    ward_path = (
        data_dir
        /
        "032h17a9_hook17_diffeomorphism_ward_witnesses.csv"
    )

    with ward_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "witness",
                "q",
                "connection_residual",
                "connection_residual_norm",
                "full_ward_established",
            ],
        )

        writer.writeheader()

        writer.writerow(
            {
                "witness":
                    "MASSIVE_1PLUS_REST",

                "q":
                    str(
                        pole[
                            "q_up"
                        ]
                    ),

                "connection_residual":
                    str(
                        diffeo[
                            "massive_rest_connection_term"
                        ]
                    ),

                "connection_residual_norm":
                    diffeo[
                        "massive_rest_connection_term_norm"
                    ],

                "full_ward_established":
                    False,
            }
        )

        writer.writerow(
            {
                "witness":
                    "GENERIC_MIXED_FOURIER",

                "q":
                    str(
                        diffeo[
                            "generic_mixed_q"
                        ]
                    ),

                "connection_residual":
                    str(
                        diffeo[
                            "generic_mixed_connection_term"
                        ]
                    ),

                "connection_residual_norm":
                    diffeo[
                        "generic_mixed_connection_term_norm"
                    ],

                "full_ward_established":
                    False,
            }
        )

    print(
        "BRANCH="
        +
        summary["branch"]
    )

    print(
        "SUBGATE="
        +
        summary["subgate"]
    )

    print(
        "DECISION="
        +
        summary["decision"]
    )

    print(
        "A8_PROVENANCE_PASS="
        +
        str(
            summary[
                "a8_provenance_pass"
            ]
        )
    )

    print(
        "PERCACCI_SEZGIN_CASE_I_HEALTHY="
        +
        str(
            summary[
                "percacci_sezgin_case_i_healthy"
            ]
        )
    )

    print(
        "CASE_I_M_PLUS_SQUARED="
        +
        str(
            case[
                "m_plus_squared"
            ]
        )
    )

    print(
        "CASE_I_R_PLUS="
        +
        str(
            case[
                "r_plus"
            ]
        )
    )

    print(
        "WHEELER_TO_PS_SOURCE_MAP_RECONSTRUCTED="
        +
        str(
            summary[
                "wheeler_to_ps_source_map_reconstructed"
            ]
        )
    )

    print(
        "TORSION_FREE_SOURCE_PROJECTION_RECONSTRUCTED="
        +
        str(
            summary[
                "torsion_free_source_projection_reconstructed"
            ]
        )
    )

    print(
        "TORSION_FREE_SOURCE_PROJECTION_IDENTITY_PASS="
        +
        str(
            summary[
                "torsion_free_source_projection_identity_pass"
            ]
        )
    )

    print(
        "PROJECTIVE_SOURCE_TRACE_CONSTRAINTS_PASS="
        +
        str(
            summary[
                "projective_source_trace_constraints_pass"
            ]
        )
    )

    print(
        "NAIVE_RAW_REST_1PLUS_CURRENT_ZERO="
        +
        str(
            summary[
                "naive_raw_rest_1plus_current_zero"
            ]
        )
    )

    print(
        "TORSION_FREE_PROJECTED_REST_1PLUS_CURRENT_NONZERO="
        +
        str(
            summary[
                "torsion_free_projected_rest_1plus_current_nonzero"
            ]
        )
    )

    print(
        "EXACT_PS_1PLUS_POLE_NUMERATOR="
        +
        str(
            summary[
                "exact_ps_1plus_pole_numerator"
            ]
        )
    )

    print(
        "EXACT_PS_1PLUS_POLE_NUMERATOR_NONZERO="
        +
        str(
            summary[
                "exact_ps_1plus_pole_numerator_nonzero"
            ]
        )
    )

    print(
        "PS_1PLUS_POLE_COEFFICIENT_PROXY="
        +
        str(
            pole[
                "full_propagator_pole_coefficient_proxy"
            ]
        )
    )

    print(
        "POLE_COEFFICIENT_PROXY_IS_PHYSICAL_ENERGY="
        +
        str(
            pole[
                "pole_coefficient_proxy_is_physical_energy"
            ]
        )
    )

    print(
        "GENERIC_DIFFEO_CONNECTION_TERM_NONZERO="
        +
        str(
            diffeo[
                "generic_connection_term_nonzero"
            ]
        )
    )

    print(
        "METRIC_SOURCE_SIGMA_REQUIRED="
        +
        str(
            summary[
                "metric_source_sigma_required"
            ]
        )
    )

    print(
        "FULL_DIFFEO_MATTER_WARD_ESTABLISHED="
        +
        str(
            summary[
                "full_diffeomorphism_matter_ward_established"
            ]
        )
    )

    print(
        "PROJECTIVE_SYMMETRY_OF_COMBINED_WHEELER_MATTER_ACTION_ESTABLISHED="
        +
        str(
            summary[
                "projective_symmetry_of_combined_wheeler_matter_action_established"
            ]
        )
    )

    print(
        "SAME_ACTION_HOOK17_COMPLETE="
        +
        str(
            summary[
                "same_action_hook17_complete"
            ]
        )
    )

    print(
        "PARTIAL_GREEN_A9="
        +
        str(
            summary[
                "partial_green"
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
        "SOURCE_COMPONENT_PATH="
        +
        str(
            source_path
        )
    )

    print(
        "DIFFEO_WARD_PATH="
        +
        str(
            ward_path
        )
    )


if __name__ == "__main__":
    main()
