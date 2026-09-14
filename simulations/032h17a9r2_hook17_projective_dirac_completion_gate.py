"""032H17A9R2 — projectively completed Dirac matter-action gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_projective_dirac_completion import (
    all_probe_projective_completion_gate,
    clean_projected_source_gate,
    conventional_projective_dirac_literature_gate,
    conventional_vector_1plus_no_go_gate,
    h17a9r2_summary,
    projected_wheeler_action_scaffold_gate,
    projected_wheeler_probe_rows,
    projector_algebra_gate,
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

    a9r1_path = (
        data_dir
        /
        "032h17a9r1_hook17_ps_wheeler_same_action_noether_summary.json"
    )

    if not a9r1_path.exists():
        raise FileNotFoundError(
            str(
                a9r1_path
            )
        )

    a9r1_payload = json.loads(
        a9r1_path.read_text(
            encoding="utf-8"
        )
    )

    a9r1 = a9r1_payload[
        "summary"
    ]

    assert a9r1[
        "direct_unmodified_wheeler_ps_same_action_closed"
    ] is True

    assert a9r1[
        "a9_exact_1plus_pole_overlap_preserved"
    ] is True

    algebra = projector_algebra_gate()
    probes = all_probe_projective_completion_gate()
    clean = clean_projected_source_gate()
    literature = conventional_projective_dirac_literature_gate()
    conventional = conventional_vector_1plus_no_go_gate()
    scaffold = projected_wheeler_action_scaffold_gate()
    summary = h17a9r2_summary()

    payload = {
        "projector_algebra":
            algebra,

        "probe_completion":
            {
                key:
                    value
                for key, value in probes.items()
                if key
                !=
                "rows"
            },

        "clean_source":
            clean,

        "conventional_projective_dirac":
            literature,

        "conventional_vector_1plus_no_go":
            conventional,

        "projected_wheeler_action_scaffold":
            scaffold,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032h17a9r2_hook17_projective_dirac_completion_summary.json"
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

    probe_path = (
        data_dir
        /
        "032h17a9r2_hook17_projected_wheeler_probe_atlas.csv"
    )

    with probe_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "name",
                "kind",
                "raw_source_norm",
                "projected_source_norm",
                "projected_trace_12",
                "projected_trace_23",
                "projected_trace_12_norm",
                "projected_trace_23_norm",
                "projective_compatible_after_action_projection",
            ],
        )

        writer.writeheader()

        for row in projected_wheeler_probe_rows():
            writer.writerow(
                {
                    **row,
                    "projected_trace_12":
                        str(
                            row[
                                "projected_trace_12"
                            ]
                        ),

                    "projected_trace_23":
                        str(
                            row[
                                "projected_trace_23"
                            ]
                        ),
                }
            )

    vector_path = (
        data_dir
        /
        "032h17a9r2_hook17_standard_dirac_vector_1plus_no_go.csv"
    )

    with vector_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "basis_vector",
                "trace_12_norm",
                "trace_23_norm",
                "antisymmetric_div1_norm",
                "double_transverse_current_norm",
                "pole_numerator",
                "physical_1plus_current_zero",
            ],
        )

        writer.writeheader()
        writer.writerows(
            conventional[
                "rows"
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
        "A9R1_PROVENANCE_PASS="
        +
        str(
            summary[
                "a9r1_provenance_pass"
            ]
        )
    )

    print(
        "UNMODIFIED_WHEELER_PS_SAME_ACTION_CLOSED="
        +
        str(
            summary[
                "unmodified_wheeler_ps_same_action_closed"
            ]
        )
    )

    print(
        "STANDARD_PROJECTIVE_LORENTZ_DIRAC_ACTION_EXISTS="
        +
        str(
            summary[
                "standard_projective_lorentz_dirac_action_exists"
            ]
        )
    )

    print(
        "STANDARD_PROJECTIVE_LORENTZ_DIRAC_PURE_TENSOR_SOURCE="
        +
        str(
            summary[
                "standard_projective_lorentz_dirac_pure_tensor_source"
            ]
        )
    )

    print(
        "STANDARD_PROJECTIVE_LORENTZ_DIRAC_VECTOR_CLASS_1PLUS_CLOSED="
        +
        str(
            summary[
                "standard_projective_lorentz_dirac_vector_class_1plus_closed"
            ]
        )
    )

    print(
        "PROJECTIVE_PROJECTOR_LOCAL="
        +
        str(
            summary[
                "projective_projector_local"
            ]
        )
    )

    print(
        "PROJECTIVE_PROJECTOR_IDEMPOTENT="
        +
        str(
            summary[
                "projective_projector_idempotent"
            ]
        )
    )

    print(
        "PROJECTIVE_PROJECTOR_SELF_ADJOINT="
        +
        str(
            summary[
                "projective_projector_self_adjoint"
            ]
        )
    )

    print(
        "PROJECTIVE_PROJECTOR_ANNIHILATES_GAUGE_IMAGE="
        +
        str(
            summary[
                "projective_projector_annihilates_gauge_image"
            ]
        )
    )

    print(
        "ALL_16_PROJECTED_WHEELER_PROBES_PROJECTIVE_COMPATIBLE="
        +
        str(
            summary[
                "all_16_projected_wheeler_probes_projective_compatible"
            ]
        )
    )

    print(
        "MAX_PROJECTED_WHEELER_TRACE_NORM="
        +
        str(
            summary[
                "maximum_projected_wheeler_trace_norm"
            ]
        )
    )

    print(
        "CLEAN_A9_SOURCE_UNCHANGED_BY_PROJECTIVE_COMPLETION="
        +
        str(
            summary[
                "clean_a9_source_unchanged_by_projective_completion"
            ]
        )
    )

    print(
        "CLEAN_A9_PROJECTED_1PLUS_POLE_NUMERATOR="
        +
        str(
            summary[
                "clean_a9_projected_1plus_pole_numerator"
            ]
        )
    )

    print(
        "CLEAN_A9_1PLUS_POLE_NUMERATOR_PRESERVED="
        +
        str(
            summary[
                "clean_a9_1plus_pole_numerator_preserved"
            ]
        )
    )

    print(
        "LINEARIZED_LOCAL_PROJECTIVE_MATTER_ACTION_SCAFFOLD_EXISTS="
        +
        str(
            summary[
                "linearized_local_projective_matter_action_scaffold_exists"
            ]
        )
    )

    print(
        "NONLINEAR_COVARIANT_WORLD_SPINOR_LIFT_ESTABLISHED="
        +
        str(
            summary[
                "nonlinear_covariant_world_spinor_lift_established"
            ]
        )
    )

    print(
        "ACTUAL_SAME_ACTION_METRIC_STRESS_DERIVED="
        +
        str(
            summary[
                "actual_same_action_metric_stress_derived"
            ]
        )
    )

    print(
        "FULL_NONLINEAR_MATTER_NOETHER_IDENTITY_ESTABLISHED="
        +
        str(
            summary[
                "full_nonlinear_matter_noether_identity_established"
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
        "PARTIAL_GREEN_A9R2="
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
        "PROJECTED_PROBE_PATH="
        +
        str(
            probe_path
        )
    )

    print(
        "STANDARD_VECTOR_NOGO_PATH="
        +
        str(
            vector_path
        )
    )


if __name__ == "__main__":
    main()
