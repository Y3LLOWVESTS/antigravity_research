"""032H17A12B — concurrent-IW exact massless vector/current protection gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_concurrent_iw_exact_source import (
    h17a12b_summary,
)


def main() -> None:
    """Run A12B and persist the exact symmetry/protection result."""

    root = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    data_dir = (
        root
        / "results"
        / "data"
    )
    data_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    a12a_path = (
        data_dir
        / "032h17a12a_hook17_iw_engineered_axial_source_summary.json"
    )

    if not a12a_path.exists():
        raise FileNotFoundError(
            str(a12a_path)
        )

    a12a = json.loads(
        a12a_path.read_text(
            encoding="utf-8"
        )
    )

    assert a12a["branch"] == "032H17A12A"
    assert a12a["engineered_iw_source_channel_reopened"] is True
    assert a12a["full_same_action_iw_noether_completion_closed"] is False
    assert a12a["hook17_closed"] is False

    summary = h17a12b_summary()

    assert summary[
        "classical_protected_same_action_massless_source_corridor_exists"
    ] is True

    assert summary["ultralight_proca_mass_required"] is False
    assert summary["near_singular_gain_used"] is False
    assert summary["canonical_source_empirical_gate_authorized"] is True
    assert summary["metric_gate_authorized"] is False
    assert summary["payload_gate_authorized"] is False
    assert summary["complete_energy_optimization_authorized"] is False
    assert summary["hook17_closed"] is False

    summary_path = (
        data_dir
        / "032h17a12b_hook17_concurrent_iw_exact_source_summary.json"
    )

    witness_path = (
        data_dir
        / "032h17a12b_hook17_concurrent_iw_corridor_witness.csv"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    witness = summary[
        "rational_nonsingular_witness"
    ]

    with witness_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fields = [
            "b1",
            "b2",
            "b3",
            "b4",
            "b5",
            "b6",
            "c",
            "nondynamical_hessian_determinant",
            "nondynamical_hessian_eigenvalues",
            "full_vector_mass_hessian_eigenvalues",
            "gauge_null_vector",
            "gauge_null_residual",
            "effective_j_n_fraction",
            "distance_from_projective_source_cancellation_c1",
            "nondynamical_sector_nonsingular",
            "positive_nondynamical_margins",
            "one_exact_gauge_null_and_other_mass_eigenvalues_positive",
            "gain_from_near_singular_mixing",
            "masslessness_is_exact_symmetry_null_not_small_eigenvalue",
        ]

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )
        writer.writeheader()

        row = dict(witness)

        for key in (
            "nondynamical_hessian_eigenvalues",
            "full_vector_mass_hessian_eigenvalues",
            "gauge_null_vector",
            "gauge_null_residual",
        ):
            row[key] = "|".join(
                row[key]
            )

        writer.writerow(row)

    reduction = summary[
        "exact_concurrent_reduction"
    ]
    symmetry = summary[
        "enhanced_u1_symmetry"
    ]

    print(
        "BRANCH="
        + summary["branch"]
    )

    print(
        "DECISION="
        + summary["decision"]
    )

    print(
        "A12A_PROVENANCE="
        + str(
            summary[
                "a12a_provenance"
            ][
                "pass"
            ]
        )
    )

    print(
        "AXIAL_DECOUPLING_CONDITION="
        + reduction[
            "axial_decoupling_condition"
        ]
    )

    print(
        "MASSLESS_CONDITION="
        + reduction[
            "massless_condition_after_axial_decoupling"
        ]
    )

    print(
        "CORRIDOR_EFFECTIVE_SOURCE="
        + reduction[
            "corridor_effective_source"
        ]
    )

    print(
        "PROJECTIVE_ALIGNED_C1_SOURCE_CANCELS="
        + str(
            reduction[
                "projective_aligned_c1_source_cancels"
            ]
        )
    )

    print(
        "ENHANCED_U1_DELTA_Q="
        + symmetry[
            "delta_q_coefficient"
        ]
    )

    print(
        "ENHANCED_U1_DELTA_ZC="
        + symmetry[
            "delta_zc_coefficient"
        ]
    )

    print(
        "ENHANCED_U1_DELTA_ZEP="
        + symmetry[
            "delta_zep_coefficient"
        ]
    )

    print(
        "MASSIVE_DIRAC_VECTOR_CURRENT_CLASSICALLY_CONSERVED="
        + str(
            symmetry[
                "massive_dirac_vector_current_classically_conserved"
            ]
        )
    )

    print(
        "MATTER_VARIATION_CANCELS_EXACTLY="
        + str(
            symmetry[
                "matter_variation_cancels_exactly"
            ]
        )
    )

    print(
        "HOLST_SQUARE_ALLOWED_GENERIC_C_NE_1="
        + str(
            symmetry[
                "holst_square_allowed_by_generic_c_not_1_enhanced_u1"
            ]
        )
    )

    print(
        "WITNESS_NONDYNAMICAL_DETERMINANT="
        + witness[
            "nondynamical_hessian_determinant"
        ]
    )

    print(
        "WITNESS_NONDYNAMICAL_EIGENVALUES="
        + ",".join(
            witness[
                "nondynamical_hessian_eigenvalues"
            ]
        )
    )

    print(
        "WITNESS_MASS_HESSIAN_EIGENVALUES="
        + ",".join(
            witness[
                "full_vector_mass_hessian_eigenvalues"
            ]
        )
    )

    print(
        "WITNESS_EFFECTIVE_JN_FRACTION="
        + witness[
            "effective_j_n_fraction"
        ]
    )

    print(
        "GAIN_FROM_NEAR_SINGULAR_MIXING="
        + str(
            witness[
                "gain_from_near_singular_mixing"
            ]
        )
    )

    print(
        "PROTECTED_SAME_ACTION_MASSLESS_SOURCE_CORRIDOR="
        + str(
            summary[
                "classical_protected_same_action_massless_source_corridor_exists"
            ]
        )
    )

    print(
        "ULTRALIGHT_PROCA_MASS_REQUIRED="
        + str(
            summary[
                "ultralight_proca_mass_required"
            ]
        )
    )

    print(
        "FULL_SM_ANOMALY_FREE_EMBEDDING_ESTABLISHED="
        + str(
            summary[
                "full_standard_model_anomaly_free_embedding_established"
            ]
        )
    )

    print(
        "NEUTRAL_PAYLOAD_DIRECT_FORCE_SILENCE_ESTABLISHED="
        + str(
            summary[
                "neutral_payload_direct_force_silence_established"
            ]
        )
    )

    print(
        "EMPIRICAL_CONSISTENCY_ESTABLISHED="
        + str(
            summary[
                "empirical_consistency_established"
            ]
        )
    )

    print(
        "CANONICAL_SOURCE_EMPIRICAL_GATE_AUTHORIZED="
        + str(
            summary[
                "canonical_source_empirical_gate_authorized"
            ]
        )
    )

    print(
        "METRIC_GATE_AUTHORIZED="
        + str(
            summary[
                "metric_gate_authorized"
            ]
        )
    )

    print(
        "PAYLOAD_GATE_AUTHORIZED="
        + str(
            summary[
                "payload_gate_authorized"
            ]
        )
    )

    print(
        "HOOK17_CLOSED="
        + str(
            summary[
                "hook17_closed"
            ]
        )
    )

    print(
        "NEXT="
        + summary["next"]
    )

    print(
        "SUMMARY_PATH="
        + str(summary_path)
    )

    print(
        "WITNESS_PATH="
        + str(witness_path)
    )


if __name__ == "__main__":
    main()
