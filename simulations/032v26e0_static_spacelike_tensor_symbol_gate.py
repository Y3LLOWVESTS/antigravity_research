"""032V26E0 — static-spacelike TT tensor symbol/background gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.v26e0_static_spacelike_tensor_symbol import (
    background_route_atlas,
    p_only_scalar_stationary_point_gate,
    representative_tensor_angle_scan,
    representative_tensor_gate,
    unsupported_flat_background_gate,
    v26e0_summary,
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

    a9r3_path = (
        data_dir
        /
        "032h17a9r3_hook17_covariant_projective_stress_protection_summary.json"
    )

    v26d_path = (
        data_dir
        /
        "032v26d_protected_ct1_dhost_kmm_action_summary.json"
    )

    if not a9r3_path.exists():
        raise FileNotFoundError(
            str(
                a9r3_path
            )
        )

    if not v26d_path.exists():
        raise FileNotFoundError(
            str(
                v26d_path
            )
        )

    a9r3 = json.loads(
        a9r3_path.read_text(
            encoding="utf-8"
        )
    )[
        "summary"
    ]

    assert a9r3[
        "v26d_resume_authorized"
    ] is True

    tensor = representative_tensor_gate()
    background = unsupported_flat_background_gate()
    scalar = p_only_scalar_stationary_point_gate()
    summary = v26e0_summary()

    payload = {
        "representative_tensor":
            tensor,

        "unsupported_flat_background":
            background,

        "p_only_scalar_stationary_point":
            scalar,

        "background_routes":
            background_route_atlas(),

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032v26e0_static_spacelike_tensor_symbol_summary.json"
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

    tensor_path = (
        data_dir
        /
        "032v26e0_tensor_angle_scan.csv"
    )

    rows = representative_tensor_angle_scan()

    with tensor_path.open(
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

    background_path = (
        data_dir
        /
        "032v26e0_background_route_atlas.csv"
    )

    background_rows = background_route_atlas()

    with background_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                background_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(
            background_rows
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
        "A9R3_FALLBACK_TRIGGER_PASS="
        +
        str(
            summary[
                "a9r3_fallback_trigger_pass"
            ]
        )
    )

    print(
        "A9_A9R3_PARTIAL_RESULTS_PRESERVED="
        +
        str(
            summary[
                "a9_a9r3_partial_results_preserved"
            ]
        )
    )

    print(
        "CURRENT_PS_CASE_I_REMAINS_BLOCKED="
        +
        str(
            summary[
                "current_ps_case_i_remains_blocked"
            ]
        )
    )

    print(
        "V26D_PROVENANCE_PASS="
        +
        str(
            summary[
                "v26d_provenance_pass"
            ]
        )
    )

    print(
        "A4_BETA_TENSOR_IDENTITY_PASS="
        +
        str(
            summary[
                "a4_beta_tensor_identity_pass"
            ]
        )
    )

    print(
        "ANISOTROPIC_TENSOR_CONE_CT1_ESTABLISHED_ON_CONSTANT_GRADIENT_PATCH="
        +
        str(
            summary[
                "anisotropic_tensor_cone_ct1_established_on_constant_gradient_patch"
            ]
        )
    )

    print(
        "REPRESENTATIVE_BETA_1="
        +
        str(
            summary[
                "representative_beta_1"
            ]
        )
    )

    print(
        "REPRESENTATIVE_WORST_TENSOR_RELATIVE_MARGIN="
        +
        str(
            summary[
                "representative_worst_tensor_relative_margin"
            ]
        )
    )

    print(
        "TENSOR_HEALTH_CRITICAL_ABS_BETA_1="
        +
        str(
            summary[
                "tensor_health_critical_abs_beta_1"
            ]
        )
    )

    print(
        "REPRESENTATIVE_TENSOR_PRINCIPAL_HEALTH_PASS="
        +
        str(
            summary[
                "representative_tensor_principal_health_pass"
            ]
        )
    )

    print(
        "LARGE_RESPONSE_FROM_TENSOR_MARGIN_COLLAPSE_ASSUMED="
        +
        str(
            summary[
                "large_response_from_tensor_margin_collapse_assumed"
            ]
        )
    )

    print(
        "UNSUPPORTED_FLAT_BACKGROUND_THEOREM_PASS="
        +
        str(
            summary[
                "unsupported_flat_background_theorem_pass"
            ]
        )
    )

    print(
        "UNSUPPORTED_FLAT_REQUIRES_P_ZERO="
        +
        str(
            summary[
                "unsupported_flat_requires_P_zero"
            ]
        )
    )

    print(
        "UNSUPPORTED_FLAT_REQUIRES_P_X_ZERO="
        +
        str(
            summary[
                "unsupported_flat_requires_P_X_zero"
            ]
        )
    )

    print(
        "P_ONLY_STATIONARY_BACKGROUND_HAS_TIME_KINETIC="
        +
        str(
            summary[
                "p_only_stationary_background_has_time_kinetic"
            ]
        )
    )

    print(
        "FULL_CONSTRAINED_SCALAR_METRIC_SYMBOL_REQUIRED="
        +
        str(
            summary[
                "full_constrained_scalar_metric_symbol_required"
            ]
        )
    )

    print(
        "TENSOR_SECTOR_PARTIAL_GREEN="
        +
        str(
            summary[
                "tensor_sector_partial_green"
            ]
        )
    )

    print(
        "FULL_STATIC_SPACELIKE_CANONICAL_HEALTH_ESTABLISHED="
        +
        str(
            summary[
                "canonical_health_on_full_static_spacelike_background_established"
            ]
        )
    )

    print(
        "STATIC_SPACELIKE_SOURCE_TO_METRIC_CROSS_RESPONSE_ESTABLISHED="
        +
        str(
            summary[
                "static_spacelike_source_to_metric_cross_response_established"
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
        "V26E1_FULL_CONSTRAINED_SYMBOL_CROSSPROP_AUTHORIZED="
        +
        str(
            summary[
                "v26e1_full_constrained_symbol_crossprop_authorized"
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
        "TENSOR_SCAN_PATH="
        +
        str(
            tensor_path
        )
    )

    print(
        "BACKGROUND_ATLAS_PATH="
        +
        str(
            background_path
        )
    )


if __name__ == "__main__":
    main()
