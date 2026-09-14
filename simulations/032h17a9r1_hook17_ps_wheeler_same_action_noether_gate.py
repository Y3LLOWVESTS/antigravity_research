"""032H17A9R1 — Wheeler / P&S projective matter Noether preflight."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_ps_wheeler_same_action_noether import (
    clean_a9_special_source_gate,
    clean_local_sigma_completion_gate,
    h17a9r1_summary,
    local_sigma_ward_witness_gate,
    projective_hermitian_probe_rows,
    wheeler_projective_source_identity_gate,
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

    a9_path = (
        data_dir
        /
        "032h17a9_hook17_percacci_sezgin_1plus_projector_summary.json"
    )

    if not a9_path.exists():
        raise FileNotFoundError(
            str(
                a9_path
            )
        )

    a9_payload = json.loads(
        a9_path.read_text(
            encoding="utf-8"
        )
    )

    a9 = a9_payload[
        "summary"
    ]

    assert a9[
        "partial_green"
    ] is True

    assert a9[
        "exact_projective_1plus_pole_overlap_established"
    ] is True

    projective = wheeler_projective_source_identity_gate()
    clean = clean_a9_special_source_gate()
    sigma = clean_local_sigma_completion_gate()
    witnesses = local_sigma_ward_witness_gate()
    summary = h17a9r1_summary()

    payload = {
        "projective_source_identity":
            {
                key:
                    value
                for key, value in projective.items()
                if key
                !=
                "rows"
            },

        "clean_a9_special_source":
            clean,

        "local_sigma_completion":
            {
                key:
                    (
                        value.tolist()
                        if hasattr(
                            value,
                            "tolist"
                        )
                        else value
                    )
                for key, value in sigma.items()
                if key
                !=
                "solution_tensor"
            },

        "local_sigma_ward_witnesses":
            witnesses,

        "summary":
            summary,
    }

    summary_path = (
        data_dir
        /
        "032h17a9r1_hook17_ps_wheeler_same_action_noether_summary.json"
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
        "032h17a9r1_hook17_wheeler_projective_probe_atlas.csv"
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
                "source_norm",
                "trace_12",
                "trace_23",
                "analytic_trace",
                "trace_12_norm",
                "trace_23_norm",
                "analytic_reconstruction_error",
                "projective_compatible",
            ],
        )

        writer.writeheader()

        for row in projective_hermitian_probe_rows():
            writer.writerow(
                {
                    **row,
                    "trace_12":
                        str(
                            row[
                                "trace_12"
                            ]
                        ),
                    "trace_23":
                        str(
                            row[
                                "trace_23"
                            ]
                        ),
                    "analytic_trace":
                        str(
                            row[
                                "analytic_trace"
                            ]
                        ),
                }
            )

    sigma_path = (
        data_dir
        /
        "032h17a9r1_hook17_local_sigma_completion.json"
    )

    sigma_payload = {
        key:
            (
                value.tolist()
                if hasattr(
                    value,
                    "tolist"
                )
                else value
            )
        for key, value in sigma.items()
    }

    sigma_path.write_text(
        json.dumps(
            sigma_payload,
            indent=2,
            sort_keys=True,
        )
        +
        "\n",
        encoding="utf-8",
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
        "A9_PROVENANCE_PASS="
        +
        str(
            summary[
                "a9_provenance_pass"
            ]
        )
    )

    print(
        "A9_EXACT_1PLUS_POLE_OVERLAP_PRESERVED="
        +
        str(
            summary[
                "a9_exact_1plus_pole_overlap_preserved"
            ]
        )
    )

    print(
        "A9_EXACT_1PLUS_POLE_NUMERATOR="
        +
        str(
            summary[
                "a9_exact_1plus_pole_numerator"
            ]
        )
    )

    print(
        "CLEAN_A9_PROJECTIVE_SPECIAL_STATE_PASS="
        +
        str(
            summary[
                "clean_a9_projective_special_state_pass"
            ]
        )
    )

    print(
        "WHEELER_HERMITIAN_PROBE_COUNT="
        +
        str(
            summary[
                "wheeler_hermitian_probe_count"
            ]
        )
    )

    print(
        "WHEELER_PROJECTIVE_COMPATIBLE_PROBES="
        +
        str(
            summary[
                "wheeler_projective_compatible_probe_count"
            ]
        )
    )

    print(
        "WHEELER_PROJECTIVE_INCOMPATIBLE_PROBES="
        +
        str(
            summary[
                "wheeler_projective_incompatible_probe_count"
            ]
        )
    )

    print(
        "MAX_PROJECTIVE_TRACE_NORM="
        +
        str(
            summary[
                "maximum_projective_trace_norm"
            ]
        )
    )

    print(
        "ANALYTIC_PROJECTIVE_TRACE_RECONSTRUCTION_PASS="
        +
        str(
            summary[
                "analytic_projective_trace_reconstruction_pass"
            ]
        )
    )

    print(
        "D1_PROJECTIVE_TRACE="
        +
        str(
            projective[
                "d1_trace"
            ]
        )
    )

    print(
        "I01_PROJECTIVE_TRACE="
        +
        str(
            projective[
                "i01_trace"
            ]
        )
    )

    print(
        "UNMODIFIED_WHEELER_PROJECTIVE_SOURCE_IDENTITY="
        +
        str(
            summary[
                "unmodified_wheeler_projective_source_identity"
            ]
        )
    )

    print(
        "DIRECT_UNMODIFIED_WHEELER_PS_SAME_ACTION_CLOSED="
        +
        str(
            summary[
                "direct_unmodified_wheeler_ps_same_action_closed"
            ]
        )
    )

    print(
        "SOURCE_STATE_RESTRICTION_ALONE_ACCEPTED_AS_GAUGE_INVARIANCE="
        +
        str(
            summary[
                "source_state_restriction_alone_accepted_as_gauge_invariance"
            ]
        )
    )

    print(
        "LOCAL_SYMMETRIC_SIGMA_COMPLETION_EXISTS="
        +
        str(
            summary[
                "local_symmetric_sigma_completion_exists"
            ]
        )
    )

    print(
        "LOCAL_SIGMA_LINEAR_SYSTEM_RANK="
        +
        str(
            summary[
                "local_sigma_linear_system_rank"
            ]
        )
    )

    print(
        "LOCAL_SIGMA_S032="
        +
        str(
            summary[
                "local_sigma_s032"
            ]
        )
    )

    print(
        "LOCAL_SIGMA_MAX_POLYNOMIAL_RESIDUAL="
        +
        str(
            summary[
                "local_sigma_max_polynomial_residual"
            ]
        )
    )

    print(
        "LOCAL_SIGMA_WARD_WITNESSES_PASS="
        +
        str(
            summary[
                "local_sigma_ward_witnesses_pass"
            ]
        )
    )

    print(
        "LOCAL_SIGMA_IS_SAME_ACTION_WHEELER_METRIC_STRESS="
        +
        str(
            summary[
                "local_sigma_is_same_action_wheeler_metric_stress"
            ]
        )
    )

    print(
        "DIFFEO_LOCAL_COMPLETION_OBSTRUCTION="
        +
        str(
            summary[
                "diffeomorphism_local_completion_obstruction"
            ]
        )
    )

    print(
        "PROJECTIVELY_COMPLETED_WHEELER_MATTER_ACTION_CLOSED="
        +
        str(
            summary[
                "projectively_completed_wheeler_matter_action_closed"
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
        "PROJECTIVE_PROBE_PATH="
        +
        str(
            probe_path
        )
    )

    print(
        "LOCAL_SIGMA_PATH="
        +
        str(
            sigma_path
        )
    )


if __name__ == "__main__":
    main()
