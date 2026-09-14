"""032V26E1A — exact Einstein-frame map / invertibility simulation."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.v26e1a_exact_einstein_frame_map import (
    explicit_inverse_map_gate,
    forward_reconstruction_gate,
    frame_observable_discipline_gate,
    invertibility_identity_scan,
    invertibility_scan_gate,
    representative_frame_gate,
    v26e1a_summary,
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

    v26e0_path = (
        data_dir
        /
        "032v26e0_static_spacelike_tensor_symbol_summary.json"
    )

    if not v26e0_path.exists():
        raise FileNotFoundError(
            str(
                v26e0_path
            )
        )

    v26e0 = json.loads(
        v26e0_path.read_text(
            encoding="utf-8"
        )
    )[
        "summary"
    ]

    assert v26e0[
        "tensor_sector_partial_green"
    ] is True

    inverse = explicit_inverse_map_gate()
    forward = forward_reconstruction_gate()
    representative = representative_frame_gate()
    scan = invertibility_scan_gate()
    discipline = frame_observable_discipline_gate()
    summary = v26e1a_summary()

    payload = {
        "inverse_class_ia_map":
            inverse,

        "forward_eh_reconstruction":
            forward,

        "representative_frame_map":
            representative,

        "invertibility_scan":
            scan,

        "frame_observable_discipline":
            discipline,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032v26e1a_exact_einstein_frame_map_summary.json"
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

    scan_path = (
        data_dir
        /
        "032v26e1a_invertibility_identity_scan.csv"
    )

    rows = invertibility_identity_scan()

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
        "V26E0_PROVENANCE_PASS="
        +
        str(
            summary[
                "v26e0_provenance_pass"
            ]
        )
    )

    print(
        "INVERSE_CLASS_IA_EQUATIONS_PASS="
        +
        str(
            summary[
                "inverse_class_ia_equations_pass"
            ]
        )
    )

    print(
        "FORWARD_EH_RECONSTRUCTS_V26D_COEFFICIENTS="
        +
        str(
            summary[
                "forward_eh_reconstructs_v26d_coefficients"
            ]
        )
    )

    print(
        "QUADRATIC_DHOST_GRAVITY_SECTOR_EH_EQUIVALENT="
        +
        str(
            summary[
                "quadratic_dhost_gravity_sector_eh_equivalent"
            ]
        )
    )

    print(
        "REPRESENTATIVE_A="
        +
        str(
            summary[
                "representative_A"
            ]
        )
    )

    print(
        "REPRESENTATIVE_D_MAP="
        +
        str(
            summary[
                "representative_D_map"
            ]
        )
    )

    print(
        "REPRESENTATIVE_MAP_INVERTIBLE="
        +
        str(
            summary[
                "representative_map_invertible"
            ]
        )
    )

    print(
        "LINEAR_F_MAP_D_IDENTICALLY_ONE="
        +
        str(
            summary[
                "linear_F_map_D_identically_one"
            ]
        )
    )

    print(
        "MIN_SCANNED_MAP_JACOBIAN_MARGIN="
        +
        str(
            summary[
                "minimum_scanned_map_jacobian_margin"
            ]
        )
    )

    print(
        "FIELD_REDEFINITION_NEAR_SINGULAR="
        +
        str(
            summary[
                "field_redefinition_near_singular"
            ]
        )
    )

    print(
        "FIELD_REDEFINITION_MARGIN_COLLAPSE_USED_FOR_GAIN="
        +
        str(
            summary[
                "field_redefinition_margin_collapse_used_for_gain"
            ]
        )
    )

    print(
        "EINSTEIN_FRAME_CURVATURE_COEFFICIENT_CONSTANT="
        +
        str(
            summary[
                "einstein_frame_curvature_coefficient_constant"
            ]
        )
    )

    print(
        "HIGHER_DERIVATIVE_GRAVITY_SECTOR_SUPPLIES_INDEPENDENT_SCALAR_MODE="
        +
        str(
            summary[
                "higher_derivative_gravity_sector_supplies_independent_scalar_mode"
            ]
        )
    )

    print(
        "LOWER_DERIVATIVE_SCALAR_COMPLETION_REQUIRED="
        +
        str(
            summary[
                "lower_derivative_scalar_completion_required"
            ]
        )
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
        "FRAME_INVARIANT_CROSS_RESPONSE_AUDIT_REQUIRED="
        +
        str(
            summary[
                "frame_invariant_cross_response_audit_required"
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
        "HOOK17_CAPACITY_REFERENCE_TRANSFERS_TO_V26D="
        +
        str(
            summary[
                "hook17_capacity_reference_transfers_to_v26d"
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
        "V26E1A_PARTIAL_GREEN="
        +
        str(
            summary[
                "v26e1a_partial_green"
            ]
        )
    )

    print(
        "V26E1B_AUTHORIZED="
        +
        str(
            summary[
                "v26e1b_authorized"
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
        "INVERTIBILITY_SCAN_PATH="
        +
        str(
            scan_path
        )
    )


if __name__ == "__main__":
    main()
