"""032H17A10F1 — source normalization + finite-payload BVP gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_marzo_finite_transverse_payload_bvp import (
    h17a10f1_summary,
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

    a10f0_path = (
        data_dir
        /
        "032h17a10f0_hook17_marzo_physical_scale_payload_loading_summary.json"
    )

    if not a10f0_path.exists():
        raise FileNotFoundError(
            str(
                a10f0_path
            )
        )

    a10f0 = json.loads(
        a10f0_path.read_text(
            encoding="utf-8"
        )
    )

    assert a10f0[
        "branch"
    ] == "032H17A10F0"

    assert a10f0[
        "partial_green"
    ] is True

    summary = h17a10f1_summary()

    assert summary[
        "source_normalization"
    ][
        "corrected_absolute_source_normalization_preflight"
    ] is True

    assert summary[
        "finite_neutral_payload_reduced_eft_bvp_established"
    ] is True

    assert summary[
        "on_axis_spherical_payload_current_geometry_rejected_by_energy"
    ] is True

    assert summary[
        "complete_energy_established"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a10f1_hook17_marzo_finite_transverse_payload_bvp_summary.json"
    )

    convergence_path = (
        data_dir
        /
        "032h17a10f1_hook17_finite_payload_convergence.csv"
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

    convergence = summary[
        "primary_convergence"
    ]

    rows = [
        {
            "diagnostic":
                "GRID_ENERGY_RELATIVE_CHANGE",

            "value":
                convergence[
                    "grid_energy_relative_change"
                ],

            "pass":
                (
                    convergence[
                        "grid_energy_relative_change"
                    ]
                    <
                    0.03
                ),
        },
        {
            "diagnostic":
                "GRID_SOURCE_COUNT_RELATIVE_CHANGE",

            "value":
                convergence[
                    "grid_source_count_relative_change"
                ],

            "pass":
                (
                    convergence[
                        "grid_source_count_relative_change"
                    ]
                    <
                    0.03
                ),
        },
        {
            "diagnostic":
                "DOMAIN_ENERGY_RELATIVE_CHANGE",

            "value":
                convergence[
                    "domain_energy_relative_change"
                ],

            "pass":
                (
                    convergence[
                        "domain_energy_relative_change"
                    ]
                    <
                    0.002
                ),
        },
        {
            "diagnostic":
                "SOURCE_WORK_RELATIVE_ERROR",

            "value":
                convergence[
                    "fine_source_work_relative_error"
                ],

            "pass":
                (
                    convergence[
                        "fine_source_work_relative_error"
                    ]
                    <
                    0.001
                ),
        },
    ]

    with convergence_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "diagnostic",
                "value",
                "pass",
            ],
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    normalization = summary[
        "source_normalization"
    ]

    primary = summary[
        "primary_torus_payload_bvp"
    ]

    sphere = summary[
        "on_axis_sphere_comparator"
    ]

    source_energy = summary[
        "source_rest_energy"
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
        "WHEELER_EQ28_RESPONSE_IS_BARE_CURRENT="
        +
        str(
            normalization[
                "eq28_response_is_bare_connection_current"
            ]
        )
    )

    print(
        "CANONICAL_CONNECTION_CURRENT_RESPONSE_FACTOR="
        +
        str(
            normalization[
                "canonical_symmetric_connection_current_relative_to_unit_eq28_response_magnitude"
            ]
        )
    )

    print(
        "A10D_NONZERO_POLE_OVERLAP_SURVIVES_REPAIR="
        +
        str(
            normalization[
                "a10d_nonzero_pole_overlap_survives_normalization_repair"
            ]
        )
    )

    print(
        "CORRECTED_SOURCE_SATURATED_RESIDUE="
        +
        str(
            normalization[
                "corrected_connection_current_residue"
            ]
        )
    )

    print(
        "CORRECTED_CANONICAL_PAIR_POLE_COUPLING="
        +
        str(
            normalization[
                "corrected_canonical_pair_pole_coupling_magnitude"
            ]
        )
    )

    print(
        "PRIMARY_PAYLOAD_KIND="
        +
        primary[
            "payload_kind"
        ]
    )

    print(
        "PRIMARY_PAYLOAD_MASS_KG="
        +
        str(
            primary[
                "payload_mass_kg"
            ]
        )
    )

    print(
        "PRIMARY_GEOMETRIC_STANDOFF_M="
        +
        str(
            primary[
                "geometric_external_standoff_m"
            ]
        )
    )

    print(
        "PRIMARY_COM_OUTWARD_ACCELERATION_M_S2="
        +
        str(
            primary[
                "payload_com_outward_acceleration_m_s2"
            ]
        )
    )

    print(
        "PRIMARY_LOCAL_ACCELERATION_MIN_M_S2="
        +
        str(
            primary[
                "payload_local_outward_acceleration_min_m_s2"
            ]
        )
    )

    print(
        "PRIMARY_LOCAL_ACCELERATION_MAX_M_S2="
        +
        str(
            primary[
                "payload_local_outward_acceleration_max_m_s2"
            ]
        )
    )

    print(
        "PRIMARY_LAMBDA_EV_M2="
        +
        str(
            primary[
                "lambda_ev_m2"
            ]
        )
    )

    print(
        "PRIMARY_EMPIRICAL_LAMBDA_MARGIN="
        +
        str(
            summary[
                "primary_lambda_empirical_margin"
            ]
        )
    )

    print(
        "PRIMARY_FIELD_LOADING_ENERGY_J="
        +
        str(
            primary[
                "field_loading_energy_j"
            ]
        )
    )

    print(
        "PRIMARY_SOURCE_WORK_ENERGY_J="
        +
        str(
            primary[
                "source_work_energy_j"
            ]
        )
    )

    print(
        "PRIMARY_SOURCE_WORK_RELATIVE_ERROR="
        +
        str(
            primary[
                "source_work_relative_error"
            ]
        )
    )

    print(
        "SOURCE_PAIR_COUNT="
        +
        str(
            source_energy[
                "source_pair_count"
            ]
        )
    )

    print(
        "ELECTRON_POSITRON_REST_FLOOR_J="
        +
        str(
            source_energy[
                "electron_positron_rest_energy_floor_j"
            ]
        )
    )

    print(
        "PROTON_ANTIPROTON_REST_COMPARATOR_J="
        +
        str(
            source_energy[
                "proton_antiproton_rest_energy_comparator_j"
            ]
        )
    )

    print(
        "FIELD_PLUS_ELECTRON_REST_FLOOR_J="
        +
        str(
            source_energy[
                "field_plus_electron_rest_floor_j"
            ]
        )
    )

    print(
        "FIELD_PLUS_PROTON_REST_COMPARATOR_J="
        +
        str(
            source_energy[
                "field_plus_proton_rest_comparator_j"
            ]
        )
    )

    print(
        "MAX_SOURCE_PARTICLE_MASS_GEV_BEFORE_PARTIAL_10MJ="
        +
        str(
            source_energy[
                "maximum_particle_mass_gev_before_field_plus_rest_hits_10mj"
            ]
        )
    )

    print(
        "SOURCE_Q_OVER_ABS_F="
        +
        str(
            summary[
                "source_characteristic_q_over_abs_f"
            ]
        )
    )

    print(
        "BVP_CONVERGENCE_PASS="
        +
        str(
            summary[
                "primary_convergence"
            ][
                "convergence_pass"
            ]
        )
    )

    print(
        "ON_AXIS_SPHERE_FIELD_ENERGY_J="
        +
        str(
            sphere[
                "field_loading_energy_j"
            ]
        )
    )

    print(
        "ON_AXIS_SPHERE_GEOMETRY_REJECTED="
        +
        str(
            summary[
                "on_axis_spherical_payload_current_geometry_rejected_by_energy"
            ]
        )
    )

    print(
        "FINITE_NEUTRAL_PAYLOAD_REDUCED_EFT_BVP="
        +
        str(
            summary[
                "finite_neutral_payload_reduced_eft_bvp_established"
            ]
        )
    )

    print(
        "PROJECT_TRUE_STANDOFF_CERTIFIED="
        +
        str(
            summary[
                "project_true_standoff_certified"
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
        "CONVERGENCE_PATH="
        +
        str(
            convergence_path
        )
    )


if __name__ == "__main__":
    main()
