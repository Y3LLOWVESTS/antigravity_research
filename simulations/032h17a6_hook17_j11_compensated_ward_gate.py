"""Simulation 032H17A6 — J11 common-Ward and compensator prefilter.

PURPOSE
-------
Run the theorem-first HOOK17 A6 source-Ward gate.

This simulation:

1. records the exact J11/K3 catalogue nesting used by the gate;
2. verifies that the A5 necessary Ward generator survives the additional
   J11 kappa1 kinetic operator;
3. applies that surviving Ward identity to the actual V24 source;
4. independently reconstructs the full quadratic Ward polynomial;
5. solves the complete zero-derivative vector/axial improvement problem;
6. tests a pure Stückelberg gauge-image correction on the lightlike pole;
7. writes durable result artifacts.

This simulation performs no energy optimization, no geometry scan, and no
AGMINER database mutation.

CLAIM LIMIT
-----------
A RED result does not close all protected 1+ actions or all compensated
HOOK17 realizations.  A genuinely dynamical same-action hook compensator and
Noether-complete source remain separate questions.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_j11_compensated_ward import (
    compensator_prefilter_rows,
    h17a6_summary,
    ward_coefficient_tensor,
)

from antigravity_research.agminer.hook17_protected_k3_ward import (
    v24_bms_current,
)


def main() -> int:
    """Run H17A6 and persist its theorem-first artifacts."""

    root = (
        Path(
            __file__
        )
        .resolve()
        .parents[
            1
        ]
    )

    output_dir = (
        root
        /
        "results"
        /
        "data"
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary = (
        h17a6_summary()
    )

    summary_path = (
        output_dir
        /
        "032h17a6_hook17_j11_common_ward_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            indent=
                2,
            sort_keys=
                True,
        )
        +
        "\n"
    )

    rows = (
        compensator_prefilter_rows()
    )

    csv_path = (
        output_dir
        /
        "032h17a6_hook17_compensator_prefilter.csv"
    )

    with csv_path.open(
        "w",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "candidate",
                "status",
                "ward_residual_norm",
                "locality",
                "same_action_status",
                "productive_1plus",
                "closure_scope",
            ],
        )

        writer.writeheader()
        writer.writerows(
            rows
        )

    coeff = (
        ward_coefficient_tensor(
            v24_bms_current()
        )
    )

    coefficient_path = (
        output_dir
        /
        "032h17a6_hook17_v24_ward_polynomial.csv"
    )

    with coefficient_path.open(
        "w",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "ward_alpha",
                "q_beta",
                "q_chi",
                "coefficient",
            ],
        )

        writer.writeheader()

        for alpha in range(
            4
        ):
            for beta in range(
                4
            ):
                for chi in range(
                    beta,
                    4,
                ):
                    value = float(
                        coeff[
                            alpha,
                            beta,
                            chi,
                        ]
                    )

                    if abs(
                        value
                    ) <= 1.0e-14:
                        continue

                    writer.writerow(
                        {
                            "ward_alpha":
                                alpha,

                            "q_beta":
                                beta,

                            "q_chi":
                                chi,

                            "coefficient":
                                value,
                        }
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
        "J11_CATALOGUE_RELATION_RECONSTRUCTED="
        +
        str(
            summary[
                "j11_catalogue_relation_reconstructed"
            ]
        )
    )

    print(
        "K3_IS_J11_KAPPA1_ZERO_SPECIALIZATION="
        +
        str(
            summary[
                "k3_is_j11_kappa1_zero_specialization"
            ]
        )
    )

    print(
        "A5_COMMON_WARD_GENERATOR_SURVIVES_J11="
        +
        str(
            summary[
                "a5_common_ward_generator_survives_j11"
            ]
        )
    )

    print(
        "WARD_POLYNOMIAL_INDEPENDENT_RECONSTRUCTION="
        +
        str(
            summary[
                "ward_polynomial_independent_reconstruction"
            ]
        )
    )

    print(
        "DIRECT_CLEAN_V24_TO_J11_CLOSED="
        +
        str(
            summary[
                "direct_clean_v24_to_j11_closed"
            ]
        )
    )

    print(
        "PRODUCTIVE_1PLUS_REPRESENTATION_SURVIVES="
        +
        str(
            summary[
                "productive_1plus_representation_survives"
            ]
        )
    )

    print(
        "MINIMAL_VECTOR_AXIAL_IMPROVEMENT_CLOSED="
        +
        str(
            summary[
                "minimal_zero_derivative_vector_axial_improvement_closed"
            ]
        )
    )

    print(
        "PURE_STUECKELBERG_GAUGE_IMAGE_RESCUE_CLOSED="
        +
        str(
            summary[
                "pure_stueckelberg_gauge_image_rescue_closed"
            ]
        )
    )

    print(
        "GENERAL_SAME_ACTION_COMPENSATED_CURRENT_CLOSED="
        +
        str(
            summary[
                "general_local_same_action_compensated_current_closed"
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
        "COMPENSATOR_PREFILTER_PATH="
        +
        str(
            csv_path
        )
    )

    print(
        "WARD_POLYNOMIAL_PATH="
        +
        str(
            coefficient_path
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
