"""032H17A12D — Pauli/magnetization source reopening gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_pauli_f2_source_reopen import (
    h17a12d_summary,
    pauli_geometry_gate,
    source_energy_at_portal_scale,
)


def main() -> None:
    """Run A12D and persist the exact source-energy/scale result."""

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

    a12c_path = (
        data_dir
        /
        "032h17a12c_hook17_concurrent_u1_fieldstrength_metric_summary.json"
    )

    if not a12c_path.exists():
        raise FileNotFoundError(
            str(a12c_path)
        )

    a12c = json.loads(
        a12c_path.read_text(
            encoding="utf-8"
        )
    )

    assert a12c[
        "branch"
    ] == "032H17A12C"

    assert a12c[
        "gauge_invariant_massless_f2_reduced_eft_1g_1m_witness"
    ] is True

    assert a12c[
        "a12b_exact_massless_carrier_closed"
    ] is False

    summary = (
        h17a12d_summary()
    )

    assert summary[
        "minimal_electron_pauli_source_partial_corridor_reopened"
    ] is True

    assert summary[
        "controlled_local_f2_eft_completion_promoted"
    ] is False

    assert summary[
        "hook17_closed"
    ] is False

    geometry = summary[
        "pauli_geometry"
    ]

    stellar = summary[
        "stellar_electron_dipole_bound"
    ]

    energy = summary[
        "strict_partial_energy_boundary"
    ]

    summary_path = (
        data_dir
        /
        "032h17a12d_hook17_pauli_f2_source_reopen_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a12d_hook17_pauli_portal_scale_scan.csv"
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

    q_ev = float(
        geometry[
            "q_from_source_radius_ev"
        ]
    )

    boundary_ev = float(
        energy[
            "strict_sub10mj_requires_portal_scale_ev_less_than"
        ]
    )

    scales = [
        0.5 * q_ev,
        q_ev,
        1.1 * q_ev,
        1.2 * q_ev,
        boundary_ev,
        2.0 * q_ev,
        10.0 * q_ev,
        1.0e-6,
        1.0e-3,
        1.0,
        1.0e3,
    ]

    rows = []

    for scale_ev in scales:
        row = (
            source_energy_at_portal_scale(
                scale_ev
            )
        )

        row[
            "portal_scale_over_q"
        ] = (
            scale_ev
            /
            q_ev
        )

        row[
            "q_over_portal_scale"
        ] = (
            q_ev
            /
            scale_ev
        )

        row[
            "strict_partial_sub10mj"
        ] = (
            row[
                "partial_total_j"
            ]
            <
            1.0e7
        )

        row[
            "complete_energy_certified"
        ] = False

        rows.append(
            row
        )

    with scan_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fields = [
            "portal_scale_ev",
            "portal_scale_over_q",
            "q_over_portal_scale",
            "field_energy_j",
            "optimistic_electron_rest_floor_j",
            "partial_total_j",
            "optimistic_fully_polarized_electron_count",
            "strict_partial_sub10mj",
            "complete_energy_certified",
        ]

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
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
        "A12C_PROVENANCE="
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
        "PAULI_SOURCE_SHAPE_IDENTITY="
        +
        str(
            geometry[
                "source_shape_identity_pass"
            ]
        )
    )

    print(
        "PAULI_CURRENT_IDENTICALLY_CONSERVED="
        +
        str(
            geometry[
                "derivative_current_identically_conserved"
            ]
        )
    )

    print(
        "CHARACTERISTIC_Q_EV="
        +
        str(
            geometry[
                "q_from_source_radius_ev"
            ]
        )
    )

    print(
        "STELLAR_MIN_EFFECTIVE_PAULI_SCALE_EV="
        +
        str(
            stellar[
                "minimum_effective_pauli_scale_ev"
            ]
        )
    )

    print(
        "STELLAR_MAX_EFFECTIVE_PAULI_COUPLING="
        +
        str(
            stellar[
                "maximum_effective_constituent_coupling"
            ]
        )
    )

    reference = summary[
        "reference_source_floor"
    ]

    print(
        "ONE_KEV_OPTIMISTIC_ELECTRON_REST_FLOOR_J="
        +
        str(
            reference[
                "optimistic_electron_rest_floor_j"
            ]
        )
    )

    at_q = energy[
        "partial_at_q"
    ]

    print(
        "AT_PORTAL_SCALE_EQUAL_Q_FIELD_ENERGY_J="
        +
        str(
            at_q[
                "field_energy_j"
            ]
        )
    )

    print(
        "AT_PORTAL_SCALE_EQUAL_Q_ELECTRON_REST_FLOOR_J="
        +
        str(
            at_q[
                "optimistic_electron_rest_floor_j"
            ]
        )
    )

    print(
        "AT_PORTAL_SCALE_EQUAL_Q_PARTIAL_TOTAL_J="
        +
        str(
            at_q[
                "partial_total_j"
            ]
        )
    )

    print(
        "AT_PORTAL_SCALE_EQUAL_Q_ELECTRON_COUNT="
        +
        str(
            at_q[
                "optimistic_fully_polarized_electron_count"
            ]
        )
    )

    print(
        "STRICT_SUB10MJ_PORTAL_SCALE_UPPER_BOUND_EV="
        +
        str(
            energy[
                "strict_sub10mj_requires_portal_scale_ev_less_than"
            ]
        )
    )

    print(
        "STRICT_BOUNDARY_PORTAL_SCALE_OVER_Q="
        +
        str(
            energy[
                "portal_boundary_over_characteristic_q"
            ]
        )
    )

    print(
        "BEST_Q_OVER_PORTAL_SCALE_WITHIN_SUB10MJ="
        +
        str(
            energy[
                "minimum_q_over_portal_scale_inside_sub10mj_corridor"
            ]
        )
    )

    print(
        "TWO_Q_MARGIN_SUB10MJ="
        +
        str(
            energy[
                "two_q_scale_margin_sub10mj"
            ]
        )
    )

    print(
        "TEN_Q_MARGIN_SUB10MJ="
        +
        str(
            energy[
                "ten_q_scale_margin_sub10mj"
            ]
        )
    )

    print(
        "PARAMETRIC_Q_OVER_M_SMALL="
        +
        str(
            energy[
                "parametric_q_over_M_small"
            ]
        )
    )

    print(
        "MINIMAL_PAULI_PARTIAL_CORRIDOR_REOPENED="
        +
        str(
            summary[
                "minimal_electron_pauli_source_partial_corridor_reopened"
            ]
        )
    )

    print(
        "CONTROLLED_LOCAL_F2_EFT_COMPLETION_PROMOTED="
        +
        str(
            summary[
                "controlled_local_f2_eft_completion_promoted"
            ]
        )
    )

    scope = summary[
        "source_selectivity_and_empirical_scope"
    ]

    print(
        "A12C_MRI_PHOTON_KILL_DIRECTLY_REUSED="
        +
        str(
            scope[
                "a12c_mri_photon_field_kill_directly_reused"
            ]
        )
    )

    print(
        "RADIATIVE_KINETIC_MIXING_CERTIFIED_ZERO="
        +
        str(
            scope[
                "radiative_kinetic_mixing_certified_zero"
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
