"""032H17A10A — spin-engineered Dirac rest-source theorem gate.

PURPOSE
-------
Persist and independently assert the exact four-state Wheeler rest-basis
source atlas before spending work on a protected-action Ward calculation.

SUCCESS
-------
The historical U1+V2 trace-vector source remains zero, while at least one
different zero-momentum particle/antiparticle basis pair has exact nonzero
totally-symmetric trace-vector overlap.

FAILURE
-------
If the complete rest basis remains trace silent, this source-state rescue is
closed immediately.

CLAIM LIMIT
-----------
A green A10A result is source-level representation progress only.

It is not a protected same-action HOOK17 model and does not authorize energy
or geometry optimization.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_spin_engineered_dirac_source import (
    h17a10a_summary,
    rest_pair_state_atlas,
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

    rows = rest_pair_state_atlas()
    summary = h17a10a_summary()

    assert summary[
        "historical_clean_pair_trace_zero_reproduced"
    ] is True

    assert summary[
        "spin_engineered_rest_pair_trace_escape_exists"
    ] is True

    assert summary[
        "expected_engineered_pair_set_reproduced"
    ] is True

    assert summary[
        "engineered_trace_exact_values_reproduced"
    ] is True

    assert summary[
        "engineered_trace_equal_and_opposite"
    ] is True

    assert summary[
        "all_full_weyl_dilation_traces_zero"
    ] is True

    assert summary[
        "trace_carrier_identity_all_pairs_pass"
    ] is True

    assert summary[
        "partial_green"
    ] is True

    assert summary[
        "energy_optimization_authorized"
    ] is False

    json_path = (
        data_dir
        /
        "032h17a10a_hook17_spin_engineered_dirac_source_summary.json"
    )

    csv_path = (
        data_dir
        /
        "032h17a10a_hook17_rest_dirac_source_state_atlas.csv"
    )

    payload = {
        "state_atlas":
            rows,

        "summary":
            summary,
    }

    json_path.write_text(
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    csv_fields = [
        "pair_id",
        "historical_clean_pair",
        "full_wheeler_source_component_norm",
        "full_wheeler_source_zero",
        "full_weyl_dilation_trace_norm",
        "full_weyl_dilation_trace_zero",
        "totally_symmetric_source_component_norm",
        "hook_source_component_norm",
        "totally_symmetric_lorentz_trace_covector",
        "totally_symmetric_lorentz_trace_norm",
        "totally_symmetric_trace_nonzero",
        "maximum_direct_trace_carrier_overlap",
        "direct_trace_carrier_overlap_nonzero",
        "so3_combined_spin1_screen_norm",
        "so3_spin2_zero_ij_stf_norm",
        "so3_spin3_spatial_stf_norm",
    ]

    with csv_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=csv_fields,
        )

        writer.writeheader()

        for row in rows:
            output = {
                key:
                    row[
                        key
                    ]

                for key
                in csv_fields
            }

            output[
                "totally_symmetric_lorentz_trace_covector"
            ] = json.dumps(
                output[
                    "totally_symmetric_lorentz_trace_covector"
                ]
            )

            writer.writerow(
                output
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
        "HISTORICAL_CLEAN_PAIR_TRACE_ZERO="
        +
        str(
            summary[
                "historical_clean_pair_trace_zero_reproduced"
            ]
        )
    )

    print(
        "SPIN_ENGINEERED_REST_PAIR_TRACE_ESCAPE="
        +
        str(
            summary[
                "spin_engineered_rest_pair_trace_escape_exists"
            ]
        )
    )

    print(
        "ENGINEERED_NONZERO_PAIR_IDS="
        +
        ",".join(
            summary[
                "spin_engineered_nonzero_pair_ids"
            ]
        )
    )

    print(
        "ENGINEERED_TRACE_MAGNITUDE="
        +
        str(
            summary[
                "engineered_trace_component_magnitude"
            ]
        )
    )

    print(
        "ENGINEERED_MAX_DIRECT_TRACE_CARRIER_OVERLAP="
        +
        str(
            summary[
                "engineered_maximum_direct_trace_carrier_overlap"
            ]
        )
    )

    print(
        "ALL_FULL_WEYL_DILATION_TRACES_ZERO="
        +
        str(
            summary[
                "all_full_weyl_dilation_traces_zero"
            ]
        )
    )

    print(
        "EXACT_BMS_TENSOR_GAUGE_WARD_EVALUATED="
        +
        str(
            summary[
                "exact_bms_tensor_gauge_source_ward_evaluated"
            ]
        )
    )

    print(
        "ENGINEERED_TORSION_CANCELLATION_ESTABLISHED="
        +
        str(
            summary[
                "engineered_pair_torsion_cancellation_established"
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
            json_path
        )
    )

    print(
        "ATLAS_PATH="
        +
        str(
            csv_path
        )
    )


if __name__ == "__main__":
    main()
