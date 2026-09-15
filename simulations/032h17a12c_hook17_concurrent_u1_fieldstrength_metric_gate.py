"""032H17A12C — exact-massless U(1) F^2 metric and empirical gate."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    REFERENCE_PORTAL_SCALE_EV,
    STRICT_COMPLETE_OPERATING_TARGET_J,
    canonical_ordinary_source_cost_gate,
    fda_mri_empirical_sanity_gate,
    h17a12c_summary,
)


def main() -> None:
    """Run A12C and persist the scoped field-strength-metric result."""

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

    a12b_path = (
        data_dir
        /
        "032h17a12b_hook17_concurrent_iw_exact_source_summary.json"
    )

    if not a12b_path.exists():
        raise FileNotFoundError(
            str(
                a12b_path
            )
        )

    a12b = json.loads(
        a12b_path.read_text(
            encoding="utf-8"
        )
    )

    assert a12b[
        "branch"
    ] == "032H17A12B"

    assert a12b[
        "classical_protected_same_action_massless_source_corridor_exists"
    ] is True

    assert a12b[
        "hook17_closed"
    ] is False

    summary = (
        h17a12c_summary()
    )

    bvp = summary[
        "massless_f2_finite_payload_bvp"
    ]

    production = bvp[
        "production"
    ]

    source = (
        canonical_ordinary_source_cost_gate()
    )

    empirical = (
        fda_mri_empirical_sanity_gate()
    )

    assert summary[
        "gauge_invariant_massless_f2_reduced_eft_1g_1m_witness"
    ] is True

    assert summary[
        "ordinary_em_like_minimal_f2_a12b_realization_closed"
    ] is True

    assert summary[
        "a12b_exact_massless_carrier_closed"
    ] is False

    assert summary[
        "hook17_closed"
    ] is False

    assert bvp[
        "preflight_convergence_pass"
    ] is True

    assert empirical[
        "fda_grad_b2_over_candidate_1g_gradient"
    ] > 1000.0

    summary_path = (
        data_dir
        /
        "032h17a12c_hook17_concurrent_u1_fieldstrength_metric_summary.json"
    )

    scan_path = (
        data_dir
        /
        "032h17a12c_hook17_f2_portal_scale_scan.csv"
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

    reference_energy = float(
        production[
            "field_energy_j"
        ]
    )

    reference_b_min = float(
        production[
            "payload_b_tesla_min"
        ]
    )

    reference_b_max = float(
        production[
            "payload_b_tesla_max"
        ]
    )

    reference_grad = float(
        production[
            "payload_outward_grad_b2_t2_per_m_min"
        ]
    )

    fda_grad = float(
        empirical[
            "fda_grad_b2_t2_per_m"
        ]
    )

    scales = [
        1.0e3,
        1.0e4,
        2.0e4,
        3.0e4,
        4.0e4,
        float(
            source[
                "field_plus_kinematic_source_strict_10mj_portal_scale_ev"
            ]
        ),
        float(
            source[
                "field_only_strict_10mj_portal_scale_ev"
            ]
        ),
    ]

    rows = []

    for scale_ev in scales:
        ratio = (
            scale_ev
            /
            REFERENCE_PORTAL_SCALE_EV
        )

        field_energy_j = (
            reference_energy
            *
            ratio**4
        )

        b_min_t = (
            reference_b_min
            *
            ratio**2
        )

        b_max_t = (
            reference_b_max
            *
            ratio**2
        )

        grad_b2 = (
            reference_grad
            *
            ratio**4
        )

        fda_over_one_g = (
            fda_grad
            /
            grad_b2
        )

        rows.append(
            {
                "portal_scale_ev":
                    scale_ev,

                "field_energy_j":
                    field_energy_j,

                "payload_b_tesla_min":
                    b_min_t,

                "payload_b_tesla_max":
                    b_max_t,

                "candidate_grad_b2_t2_per_m_for_1g":
                    grad_b2,

                "fda_grad_b2_over_candidate_1g_gradient":
                    fda_over_one_g,

                "field_energy_strict_lt10mj":
                    field_energy_j
                    <
                    STRICT_COMPLETE_OPERATING_TARGET_J,

                "complete_energy_certified":
                    False,
            }
        )

    with scan_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        fields = [
            "portal_scale_ev",
            "field_energy_j",
            "payload_b_tesla_min",
            "payload_b_tesla_max",
            "candidate_grad_b2_t2_per_m_for_1g",
            "fda_grad_b2_over_candidate_1g_gradient",
            "field_energy_strict_lt10mj",
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
        "A12B_PROVENANCE="
        +
        str(
            summary[
                "a12b_provenance"
            ][
                "pass"
            ]
        )
    )

    print(
        "OLD_Q_SQUARED_METRIC_TRANSFERABLE="
        +
        str(
            summary[
                "gauge_invariant_metric"
            ][
                "a10e_q_mu_q_nu_portal_transferable_to_exact_massless_a12b"
            ]
        )
    )

    print(
        "MINIMAL_GAUGE_INVARIANT_METRIC="
        +
        summary[
            "gauge_invariant_metric"
        ][
            "minimal_magnetostatic_quadratic_gauge_invariant"
        ]
    )

    print(
        "A11A_MASSIVE_GMINUS2_BOUND_REUSED="
        +
        str(
            summary[
                "exact_massless_u1_rotation"
            ][
                "a11a_massive_vector_gminus2_bound_reused"
            ]
        )
    )

    print(
        "ORDINARY_PAYLOAD_SILENT_CURRENT="
        +
        summary[
            "a12b_provenance"
        ][
            "ordinary_stable_payload_silent_current"
        ]
    )

    print(
        "F2_BVP_PREFLIGHT_CONVERGENCE="
        +
        str(
            bvp[
                "preflight_convergence_pass"
            ]
        )
    )

    print(
        "F2_REDUCED_EFT_1G_1M_WITNESS="
        +
        str(
            summary[
                "gauge_invariant_massless_f2_reduced_eft_1g_1m_witness"
            ]
        )
    )

    print(
        "REFERENCE_PORTAL_SCALE_EV="
        +
        str(
            production[
                "reference_portal_scale_ev"
            ]
        )
    )

    print(
        "REFERENCE_FIELD_ENERGY_J="
        +
        str(
            production[
                "field_energy_j"
            ]
        )
    )

    print(
        "REFERENCE_PAYLOAD_LOCAL_MIN_M_S2="
        +
        str(
            production[
                "payload_local_acceleration_min_m_s2"
            ]
        )
    )

    print(
        "REFERENCE_PAYLOAD_LOCAL_MAX_M_S2="
        +
        str(
            production[
                "payload_local_acceleration_max_m_s2"
            ]
        )
    )

    print(
        "REFERENCE_PAYLOAD_COM_M_S2="
        +
        str(
            production[
                "payload_com_acceleration_m_s2"
            ]
        )
    )

    print(
        "GEOMETRIC_STANDOFF_M="
        +
        str(
            production[
                "geometric_external_standoff_m"
            ]
        )
    )

    print(
        "FIELD_ONLY_10MJ_MAX_M_EM_EV="
        +
        str(
            source[
                "field_only_strict_10mj_portal_scale_ev"
            ]
        )
    )

    print(
        "FIELD_PLUS_OPTIMISTIC_SOURCE_10MJ_MAX_M_EM_EV="
        +
        str(
            source[
                "field_plus_kinematic_source_strict_10mj_portal_scale_ev"
            ]
        )
    )

    print(
        "OPTIMISTIC_SOURCE_ENERGY_FLOOR_AT_PARTIAL_CEILING_J="
        +
        str(
            source[
                "optimistic_source_energy_floor_at_partial_ceiling_j"
            ]
        )
    )

    print(
        "FDA_MRI_B_T="
        +
        str(
            empirical[
                "fda_b_tesla"
            ]
        )
    )

    print(
        "FDA_MRI_GRAD_T_PER_M="
        +
        str(
            empirical[
                "fda_spatial_gradient_t_per_m"
            ]
        )
    )

    print(
        "FDA_REPORTED_DEFLECTION_DEG_LESS_THAN="
        +
        str(
            empirical[
                "fda_reported_deflection_deg_less_than"
            ]
        )
    )

    print(
        "MAXIMALLY_FAVORABLE_CANDIDATE_PAYLOAD_B_T_MIN="
        +
        str(
            empirical[
                "candidate_payload_b_tesla_min"
            ]
        )
    )

    print(
        "MAXIMALLY_FAVORABLE_CANDIDATE_PAYLOAD_B_T_MAX="
        +
        str(
            empirical[
                "candidate_payload_b_tesla_max"
            ]
        )
    )

    print(
        "FDA_GRAD_B2_OVER_CANDIDATE_1G_GRADIENT="
        +
        str(
            empirical[
                "fda_grad_b2_over_candidate_1g_gradient"
            ]
        )
    )

    print(
        "PORTAL_PREDICTED_UNIVERSAL_ACCELERATION_IN_G_AT_FDA_GRADIENT="
        +
        str(
            empirical[
                "portal_predicted_universal_acceleration_in_g"
            ]
        )
    )

    print(
        "ORDINARY_EM_LIKE_MINIMAL_F2_ROUTE_CLOSED="
        +
        str(
            summary[
                "ordinary_em_like_minimal_f2_a12b_realization_closed"
            ]
        )
    )

    print(
        "A12B_EXACT_MASSLESS_CARRIER_CLOSED="
        +
        str(
            summary[
                "a12b_exact_massless_carrier_closed"
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
        "SCALE_SCAN_PATH="
        +
        str(
            scan_path
        )
    )


if __name__ == "__main__":
    main()
