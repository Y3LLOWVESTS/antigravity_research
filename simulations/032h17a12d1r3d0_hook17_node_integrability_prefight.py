"""Execute 032H17A12D1R3D0 polarization-node Maxwell-integrability preflight."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3d0_node_integrability import (
    BRANCH,
    GROSS_NODE_REORIENTATION_DEG,
    GRID_SPACINGS_M,
    LMAX_VALUES,
    NODE_TAPER_ROTATION_DEG,
    closed_surface_integrability_gate,
    decision_from_atlas,
    provenance_gate,
    run_grid_lmax,
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

    summary_path = (
        data_dir
        /
        "032h17a12d1r3d0_hook17_node_integrability_summary.json"
    )

    atlas_path = (
        data_dir
        /
        "032h17a12d1r3d0_hook17_node_integrability_atlas.csv"
    )

    provenance = (
        provenance_gate()
    )

    assert provenance[
        "pass"
    ] is True

    theorem = (
        closed_surface_integrability_gate()
    )

    print(
        "BRANCH="
        +
        BRANCH
    )

    print(
        "OBJECTIVE="
        "STATIC_SINGLE_FIELD_NODE_MAXWELL_INTEGRABILITY_"
        "AND_APPROXIMATE_NODE_CAPACITY"
    )

    print(
        "EXACT_NONTRIVIAL_CLOSED_NODE="
        +
        str(
            theorem[
                "exact_nontrivial_single_field_closed_node"
            ]
        )
    )

    print(
        "APPROXIMATE_NODE_STILL_OPEN="
        +
        str(
            theorem[
                "approximate_node_still_open"
            ]
        )
    )

    print(
        "GROSS_NODE_REORIENTATION_DEG="
        +
        str(
            GROSS_NODE_REORIENTATION_DEG
        )
    )

    print(
        "NODE_TAPER_ROTATION_DEG="
        +
        str(
            NODE_TAPER_ROTATION_DEG
        )
    )

    atlas = []

    for h in GRID_SPACINGS_M:
        for lmax in LMAX_VALUES:
            result = (
                run_grid_lmax(
                    h,
                    lmax,
                )
            )

            atlas.append(
                result
            )

            best = (
                result[
                    "best"
                ]
                or
                {}
            )

            print(
                "R3D0_POINT "
                +
                f"H={h} "
                +
                f"LMAX={lmax} "
                +
                "E_T_FLOOR="
                +
                str(
                    result[
                        "electric_exact_trace_floor_amplitude"
                    ]
                )
                +
                " B_N_FLOOR="
                +
                str(
                    result[
                        "magnetic_exact_trace_floor_amplitude"
                    ]
                )
                +
                " POSITIVE_PAIRS="
                +
                str(
                    result[
                        "whole_payload_positive_pair_count"
                    ]
                )
                +
                " BEST_DRIVER_RATIO="
                +
                str(
                    best.get(
                        "driver_ratio_vs_r3b"
                    )
                )
                +
                " SUPPRESSION="
                +
                str(
                    best.get(
                        "interface_suppression_factor_vs_r3b"
                    )
                )
                +
                " EXT_ENERGY_J="
                +
                str(
                    best.get(
                        "exterior_canonical_energy_j"
                    )
                )
                +
                " E_ID="
                +
                str(
                    best.get(
                        "e_id"
                    )
                )
                +
                " B_ID="
                +
                str(
                    best.get(
                        "b_id"
                    )
                )
            )

    decision = (
        decision_from_atlas(
            atlas
        )
    )

    summary = {
        "branch":
            BRANCH,

        "provenance":
            provenance,

        "closed_surface_integrability_gate":
            theorem,

        "atlas":
            atlas,

        **decision,
    }

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

    for result in atlas:
        best = (
            result[
                "best"
            ]
            or
            {}
        )

        rows.append(
            {
                "grid_spacing_m":
                    result[
                        "grid_spacing_m"
                    ],

                "lmax":
                    result[
                        "lmax"
                    ],

                "interface_cells_across_taper":
                    result[
                        "interface_cells_across_taper"
                    ],

                "electric_trace_floor_amplitude":
                    result[
                        "electric_exact_trace_floor_amplitude"
                    ],

                "magnetic_trace_floor_amplitude":
                    result[
                        "magnetic_exact_trace_floor_amplitude"
                    ],

                "whole_payload_positive_pair_count":
                    result[
                        "whole_payload_positive_pair_count"
                    ],

                "best_driver_ratio_vs_r3b":
                    best.get(
                        "driver_ratio_vs_r3b"
                    ),

                "best_suppression_factor_vs_r3b":
                    best.get(
                        "interface_suppression_factor_vs_r3b"
                    ),

                "best_exterior_canonical_energy_j":
                    best.get(
                        "exterior_canonical_energy_j"
                    ),

                "best_e_id":
                    best.get(
                        "e_id"
                    ),

                "best_b_id":
                    best.get(
                        "b_id"
                    ),

                "best_e_t_fraction":
                    best.get(
                        "electric_tangent_amplitude_fraction"
                    ),

                "best_b_n_fraction":
                    best.get(
                        "magnetic_normal_amplitude_fraction"
                    ),
            }
        )

    with atlas_path.open(
        "w",
        encoding="utf-8",
        newline="",
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

    print()
    print(
        "================ R3D0 FINAL DECISION ================"
    )

    print(
        "DECISION="
        +
        decision[
            "decision"
        ]
    )

    print(
        "NEXT="
        +
        decision[
            "next"
        ]
    )

    print(
        "AUTHORIZE_R3D1="
        +
        str(
            decision[
                "authorize_single_field_loaded_r3d1"
            ]
        )
    )

    print(
        "AUTHORIZE_R3X0="
        +
        str(
            decision[
                "authorize_cross_topological_r3x0"
            ]
        )
    )

    print(
        "EXACT_CLOSED_NODE_NONTRIVIAL=False"
    )

    print(
        "THRESHOLD_CONTINUUM_CERTIFIED=False"
    )

    print(
        "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=False"
    )

    print(
        "CERTIFIED_SUB10MJ_MODEL_FOUND=False"
    )

    print(
        "006D_REPLACED=False"
    )

    print(
        "SUMMARY="
        +
        str(
            summary_path
        )
    )

    print(
        "ATLAS="
        +
        str(
            atlas_path
        )
    )


if __name__ == "__main__":
    main()
