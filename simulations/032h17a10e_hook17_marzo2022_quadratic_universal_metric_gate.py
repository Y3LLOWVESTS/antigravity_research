"""032H17A10E — protected quadratic universal-metric gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_marzo2022_quadratic_universal_metric import (
    h17a10e_summary,
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

    a10d_path = (
        data_dir
        /
        "032h17a10d_hook17_marzo2022_exact_1minus_pole_summary.json"
    )

    if not a10d_path.exists():
        raise FileNotFoundError(
            str(
                a10d_path
            )
        )

    a10d = json.loads(
        a10d_path.read_text(
            encoding="utf-8"
        )
    )

    assert a10d[
        "branch"
    ] == "032H17A10D"

    assert a10d[
        "exact_linearized_healthy_1minus_pole_overlap_established"
    ] is True

    assert a10d[
        "partial_green"
    ] is True

    summary = h17a10e_summary()

    assert summary[
        "a10d_exact_healthy_pole_provenance"
    ] is True

    assert summary[
        "healthy_pole_exact_vector_factorization"
    ] is True

    assert summary[
        "technical_naturalness_external_operator_preflight"
    ] is True

    assert summary[
        "one_universal_payload_metric"
    ] is True

    assert summary[
        "physical_g00_response_nonzero"
    ] is True

    assert summary[
        "physical_g00_outward_sign"
    ] is True

    assert summary[
        "field_redefinition_invariant_tidal_response_nonzero"
    ] is True

    assert summary[
        "partial_green"
    ] is True

    assert summary[
        "finite_payload_established"
    ] is False

    assert summary[
        "energy_optimization_authorized"
    ] is False

    summary_path = (
        data_dir
        /
        "032h17a10e_hook17_marzo2022_quadratic_universal_metric_summary.json"
    )

    profile_path = (
        data_dir
        /
        "032h17a10e_hook17_static_metric_profile.csv"
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

    static = summary[
        "static_external_response"
    ]

    m = static[
        "inverse_range_m"
    ]

    sigma_h = static[
        "sigma_at_payload"
    ]

    h = static[
        "stand_off_probe_m"
    ]

    rows = []

    for z in (
        0.0,
        0.25,
        0.5,
        0.75,
        1.0,
        1.25,
        1.5,
        2.0,
    ):
        sigma = (
            sigma_h
            *
            math.exp(
                -2.0
                *
                m
                *
                (
                    z
                    -
                    h
                )
            )
        )

        acceleration = (
            2.0
            *
            299792458.0**2
            *
            m
            *
            sigma
        )

        rows.append(
            {
                "z_m":
                    z,

                "sigma":
                    sigma,

                "acceleration_m_s2":
                    acceleration,
            }
        )

    with profile_path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "z_m",
                "sigma",
                "acceleration_m_s2",
            ],
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
        "A10D_EXACT_HEALTHY_POLE_PROVENANCE="
        +
        str(
            summary[
                "a10d_exact_healthy_pole_provenance"
            ]
        )
    )

    print(
        "HEALTHY_POLE_VECTOR_FACTORIZATION="
        +
        str(
            summary[
                "healthy_pole_exact_vector_factorization"
            ]
        )
    )

    print(
        "QUADRATIC_G00_NUMERATOR="
        +
        str(
            summary[
                "quadratic_metric"
            ][
                "quadratic_g00_numerator_nonzero"
            ]
        )
    )

    print(
        "NONREDUNDANT_SOURCEFREE_LINEAR_METRIC_RESPONSE="
        +
        str(
            summary[
                "sourcefree_nonredundant_linear_metric_response"
            ]
        )
    )

    print(
        "LINEAR_EXTERNAL_OPERATOR_PROTECTION="
        +
        str(
            summary[
                "linear_operator_protection"
            ][
                "linear_external_operator_protection_pass"
            ]
        )
    )

    print(
        "ACTION_LEVEL_SCAFFOLD="
        +
        str(
            summary[
                "same_action_scaffold"
            ][
                "action_level_scaffold_established"
            ]
        )
    )

    print(
        "ONE_UNIVERSAL_PAYLOAD_METRIC="
        +
        str(
            summary[
                "one_universal_payload_metric"
            ]
        )
    )

    print(
        "STATIC_RANGE_M="
        +
        str(
            summary[
                "static_external_response"
            ][
                "range_m"
            ]
        )
    )

    print(
        "STATIC_MASS_EV="
        +
        str(
            summary[
                "static_external_response"
            ][
                "mass_eV"
            ]
        )
    )

    print(
        "SIGMA_AT_1M_FOR_1G="
        +
        str(
            summary[
                "static_external_response"
            ][
                "sigma_at_payload"
            ]
        )
    )

    print(
        "PHYSICAL_G00_OUTWARD_SIGN="
        +
        str(
            summary[
                "physical_g00_outward_sign"
            ]
        )
    )

    print(
        "INVARIANT_TIDAL_RESPONSE="
        +
        str(
            summary[
                "field_redefinition_invariant_tidal_response_nonzero"
            ]
        )
    )

    print(
        "TECHNICAL_NATURALNESS_EXTERNAL_OPERATOR_PREFLIGHT="
        +
        str(
            summary[
                "technical_naturalness_external_operator_preflight"
            ]
        )
    )

    print(
        "FULL_QUANTUM_RG_UV_CERTIFIED="
        +
        str(
            summary[
                "full_quantum_rg_uv_certified"
            ]
        )
    )

    print(
        "FINITE_PAYLOAD_ESTABLISHED="
        +
        str(
            summary[
                "finite_payload_established"
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
        "PROFILE_PATH="
        +
        str(
            profile_path
        )
    )


if __name__ == "__main__":
    import math
    main()
