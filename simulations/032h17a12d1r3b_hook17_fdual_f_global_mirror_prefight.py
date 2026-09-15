"""032H17A12D1R3B — global mirror and interface-transfer preflight."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_global_mirror_prefight import (
    A12C_REFERENCE_FIELD_ENERGY_J,
    BRANCH,
    FIT_LMAX_VALUES,
    FIT_RADII_M,
    GRID_SPACINGS_M,
    PRIMARY_FIT_RADIUS_M,
    PRIMARY_LMAX,
    claim_policy_gate,
    decision_from_results,
    fit_exterior_multipoles,
    interface_orientation_diagnostics,
    mirror_global_energy_gate,
    mirror_payload_reconstruction,
    polarization_node_corridor,
    provenance_gate,
    reconstruct_a12c_field,
    surface_charge_diagnostics,
)


def scalar_fit_record(
    h: float,
    fit: dict,
) -> dict:
    return {
        "grid_spacing_m":
            h,

        "fit_radius_m":
            fit[
                "fit_radius_m"
            ],

        "lmax":
            fit[
                "lmax"
            ],

        "relative_rms_field_residual":
            fit[
                "relative_rms_field_residual"
            ],

        "multipole_magnetic_exterior_energy_j":
            fit[
                "multipole_magnetic_exterior_energy_j"
            ],

        "direct_numerical_magnetic_exterior_energy_j":
            fit[
                "direct_numerical_magnetic_exterior_energy_j"
            ],

        "exterior_energy_relative_error":
            fit[
                "exterior_energy_relative_error"
            ],

        "electric_total_minimum_energy_j":
            fit[
                "electric_total_minimum_energy_j"
            ],
    }


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
        "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json"
    )

    fit_scan_path = (
        data_dir
        /
        "032h17a12d1r3b_hook17_fdual_f_multipole_fit_scan.csv"
    )

    interface_path = (
        data_dir
        /
        "032h17a12d1r3b_hook17_fdual_f_interface_pareto.csv"
    )

    provenance = (
        provenance_gate()
    )

    assert provenance[
        "pass"
    ] is True

    print(
        "BRANCH="
        +
        BRANCH
    )

    print(
        "PRIMARY_GOAL=PRESERVE_2P656859J_BY_GLOBAL_ELECTROSTATIC_MIRROR_AND_INTERFACE_DESIGN"
    )

    grid_results = {}
    fit_rows = []
    interface_rows = []

    for h in GRID_SPACINGS_M:
        print()
        print(
            "================================================================"
        )

        print(
            "A12C_RECONSTRUCTION_GRID_M="
            +
            str(
                h
            )
        )

        print(
            "================================================================"
        )

        field = (
            reconstruct_a12c_field(
                h
            )
        )

        energy_relerr = (
            abs(
                field[
                    "field_energy_j"
                ]
                -
                A12C_REFERENCE_FIELD_ENERGY_J
            )
            /
            A12C_REFERENCE_FIELD_ENERGY_J
        )

        print(
            "A12C_RECONSTRUCTED_FIELD_ENERGY_J="
            +
            str(
                field[
                    "field_energy_j"
                ]
            )
        )

        print(
            "A12C_REFERENCE_FIELD_ENERGY_J="
            +
            str(
                A12C_REFERENCE_FIELD_ENERGY_J
            )
        )

        print(
            "A12C_RECONSTRUCTION_ENERGY_RELERR="
            +
            str(
                energy_relerr
            )
        )

        print(
            "A12C_RECONSTRUCTED_PAYLOAD_MIN_ACCEL_M_S2="
            +
            str(
                field[
                    "payload_acceleration_min_m_s2"
                ]
            )
        )

        print(
            "A12C_RECONSTRUCTED_PAYLOAD_SIGMA_MAX="
            +
            str(
                field[
                    "payload_sigma_max"
                ]
            )
        )

        fits = {}

        for fit_radius in FIT_RADII_M:
            for lmax in FIT_LMAX_VALUES:
                fit = (
                    fit_exterior_multipoles(
                        field,
                        fit_radius,
                        lmax,
                    )
                )

                key = (
                    f"R{fit_radius:.2f}_L{lmax}"
                )

                fits[
                    key
                ] = fit

                fit_rows.append(
                    scalar_fit_record(
                        h,
                        fit,
                    )
                )

                print(
                    "FIT_GRID_M="
                    +
                    str(
                        h
                    )
                    +
                    " R_M="
                    +
                    str(
                        fit_radius
                    )
                    +
                    " LMAX="
                    +
                    str(
                        lmax
                    )
                    +
                    " RMS_REL="
                    +
                    str(
                        fit[
                            "relative_rms_field_residual"
                        ]
                    )
                    +
                    " EXT_ENERGY_RELERR="
                    +
                    str(
                        fit[
                            "exterior_energy_relative_error"
                        ]
                    )
                )

        primary_key = (
            f"R{PRIMARY_FIT_RADIUS_M:.2f}_L{PRIMARY_LMAX}"
        )

        primary_fit = (
            fits[
                primary_key
            ]
        )

        global_energy = (
            mirror_global_energy_gate(
                field,
                primary_fit,
            )
        )

        surface_charge = (
            surface_charge_diagnostics(
                primary_fit
            )
        )

        payload_reconstruction = (
            mirror_payload_reconstruction(
                field,
                primary_fit,
                global_energy,
            )
        )

        interface = (
            interface_orientation_diagnostics(
                field
            )
        )

        for row in interface[
            "pareto"
        ]:
            interface_rows.append(
                {
                    "grid_spacing_m":
                        h,

                    **row,
                }
            )

        print()
        print(
            "PRIMARY_MULTIPOLE_FIT_RMS_REL="
            +
            str(
                primary_fit[
                    "relative_rms_field_residual"
                ]
            )
        )

        print(
            "PRIMARY_MULTIPOLE_EXT_ENERGY_RELERR="
            +
            str(
                primary_fit[
                    "exterior_energy_relative_error"
                ]
            )
        )

        print(
            "ORIGINAL_NUMERICAL_EXTERIOR_B_ENERGY_J="
            +
            str(
                primary_fit[
                    "direct_numerical_magnetic_exterior_energy_j"
                ]
            )
        )

        print(
            "MULTIPOLE_EXTERIOR_B_ENERGY_J="
            +
            str(
                primary_fit[
                    "multipole_magnetic_exterior_energy_j"
                ]
            )
        )

        print()
        print(
            "NEW_MAGNETIC_HALF_ENERGY_J="
            +
            str(
                global_energy[
                    "new_magnetic_half_energy_j"
                ]
            )
        )

        print(
            "MINIMUM_GLOBAL_ELECTRIC_MIRROR_ENERGY_J="
            +
            str(
                global_energy[
                    "new_electric_minimum_global_energy_j"
                ]
            )
        )

        print(
            "MIXED_GLOBAL_FIELD_ENERGY_PRE_1G_RENORM_J="
            +
            str(
                global_energy[
                    "mixed_global_field_energy_before_1g_renormalization_j"
                ]
            )
        )

        print(
            "MIXED_GLOBAL_ENERGY_OVER_A12C="
            +
            str(
                global_energy[
                    "mixed_global_energy_over_a12c"
                ]
            )
        )

        print(
            "MIRROR_SURFACE_CHARGE_NET_ZERO_ANALYTIC="
            +
            str(
                surface_charge[
                    "net_charge_zero_analytic"
                ]
            )
        )

        print(
            "MIRROR_SURFACE_CHARGE_NET_OVER_ABSOLUTE="
            +
            str(
                surface_charge[
                    "net_over_absolute"
                ]
            )
        )

        print(
            "TRUE_EXTERNAL_STANDOFF_PRESERVED="
            +
            str(
                global_energy[
                    "true_external_standoff_preserved"
                ]
            )
        )

        print()
        print(
            "MIXED_PAYLOAD_SIGMA_RMS_RELERR="
            +
            str(
                payload_reconstruction[
                    "payload_sigma_relative_rms_error"
                ]
            )
        )

        print(
            "MIXED_PAYLOAD_ACCEL_MIN_PRE_RENORM_M_S2="
            +
            str(
                payload_reconstruction[
                    "payload_acceleration_min_before_renormalization_m_s2"
                ]
            )
        )

        print(
            "MIXED_PAYLOAD_ACCEL_MAX_PRE_RENORM_M_S2="
            +
            str(
                payload_reconstruction[
                    "payload_acceleration_max_before_renormalization_m_s2"
                ]
            )
        )

        print(
            "MIXED_WHOLE_PAYLOAD_OUTWARD_PRE_RENORM="
            +
            str(
                payload_reconstruction[
                    "whole_payload_outward_before_renormalization"
                ]
            )
        )

        print(
            "MIXED_GLOBAL_FIELD_ENERGY_NORMALIZED_TO_1G_J="
            +
            str(
                payload_reconstruction[
                    "normalized_mixed_global_field_energy_j"
                ]
            )
        )

        print(
            "MIXED_SUB100J="
            +
            str(
                payload_reconstruction[
                    "sub100j_after_1g_normalization"
                ]
            )
        )

        print(
            "MIXED_SUB10KJ="
            +
            str(
                payload_reconstruction[
                    "sub10kj_after_1g_normalization"
                ]
            )
        )

        print()
        print(
            "INTERFACE_WEIGHTED_BNORMAL2_FRACTION="
            +
            str(
                interface[
                    "gradient_weighted_Bnormal2_fraction"
                ]
            )
        )

        print(
            "INTERFACE_WEIGHTED_BTANGENT2_FRACTION="
            +
            str(
                interface[
                    "gradient_weighted_Btangent2_fraction"
                ]
            )
        )

        print(
            "INTERFACE_OPTIMAL_GLOBAL_E_OVER_B="
            +
            str(
                interface[
                    "optimal_global_E_over_B_ratio_for_driver"
                ]
            )
        )

        print(
            "INTERFACE_OPTIMAL_DRIVER_RATIO_VS_EQUAL_SPLIT="
            +
            str(
                interface[
                    "optimal_driver_ratio_vs_equal_split"
                ]
            )
        )

        print(
            "FIELD_ENERGY_RATIO_AT_INTERFACE_DRIVER_OPTIMUM="
            +
            str(
                interface[
                    "field_energy_ratio_at_driver_optimum"
                ]
            )
        )

        grid_results[
            str(
                h
            )
        ] = {
            "reconstruction":
                {
                    "grid_spacing_m":
                        h,

                    "field_energy_j":
                        field[
                            "field_energy_j"
                        ],

                    "field_energy_relative_error_vs_a12c":
                        energy_relerr,

                    "exterior_energy_j":
                        field[
                            "exterior_energy_j"
                        ],

                    "payload_acceleration_min_m_s2":
                        field[
                            "payload_acceleration_min_m_s2"
                        ],

                    "payload_acceleration_max_m_s2":
                        field[
                            "payload_acceleration_max_m_s2"
                        ],

                    "payload_sigma_max":
                        field[
                            "payload_sigma_max"
                        ],
                },

            "primary_fit":
                {
                    key:
                        value
                    for key, value in primary_fit.items()
                    if key
                    not in (
                        "boundary_amplitudes",
                        "mode_rows",
                    )
                },

            "multipole_modes":
                primary_fit[
                    "mode_rows"
                ],

            "global_energy":
                global_energy,

            "surface_charge":
                surface_charge,

            "payload_reconstruction":
                payload_reconstruction,

            "interface_orientation":
                interface,
        }

    coarse = (
        grid_results[
            str(
                GRID_SPACINGS_M[
                    0
                ]
            )
        ]
    )

    fine = (
        grid_results[
            str(
                GRID_SPACINGS_M[
                    1
                ]
            )
        ]
    )

    fine_fit = (
        fine[
            "primary_fit"
        ]
    )

    fine_global = (
        fine[
            "global_energy"
        ]
    )

    fine_payload = (
        fine[
            "payload_reconstruction"
        ]
    )

    coarse_payload = (
        coarse[
            "payload_reconstruction"
        ]
    )

    energy_coarse = (
        coarse_payload[
            "normalized_mixed_global_field_energy_j"
        ]
    )

    energy_fine = (
        fine_payload[
            "normalized_mixed_global_field_energy_j"
        ]
    )

    if (
        energy_coarse
        is not None
        and
        energy_fine
        is not None
    ):
        grid_energy_relerr = (
            abs(
                energy_fine
                -
                energy_coarse
            )
            /
            energy_fine
        )
    else:
        grid_energy_relerr = None

    node = (
        polarization_node_corridor()
    )

    decision = (
        decision_from_results(
            fine_fit,
            fine_global,
            fine_payload,
            coarse_payload,
        )
    )

    print()
    print(
        "================================================================"
    )

    print(
        "POLARIZATION-NODE DESIGN CLUE"
    )

    print(
        "================================================================"
    )

    print(
        "REQUIRED_SIGMA_GRADIENT_PER_M="
        +
        str(
            node[
                "required_sigma_gradient_per_m"
            ]
        )
    )

    print(
        "SIGMA_CHANGE_REQUIRED_ACROSS_0P1M_TAPER="
        +
        str(
            node[
                "sigma_change_required_across_taper"
            ]
        )
    )

    print(
        "SIGMA_CHANGE_OVER_A12C_SIGMA_MAX="
        +
        str(
            node[
                "sigma_change_over_a12c_sigma_max"
            ]
        )
    )

    print(
        "P_NODE_ROTATION_RATE_RAD_PER_M="
        +
        str(
            node[
                "rotation_rate_at_equal_field_P_node_rad_per_m"
            ]
        )
    )

    print(
        "P_NODE_ROTATION_ANGLE_ACROSS_TAPER_RAD="
        +
        str(
            node[
                "rotation_angle_across_taper_rad"
            ]
        )
    )

    print(
        "P_NODE_ROTATION_ANGLE_ACROSS_TAPER_DEG="
        +
        str(
            node[
                "rotation_angle_across_taper_deg"
            ]
        )
    )

    print(
        "BETA_PEAK_TIMES_ROTATION_ANGLE="
        +
        str(
            node[
                "beta_peak_times_rotation_angle"
            ]
        )
    )

    print(
        "EXACT_INTERFACE_MIX_NULL_AT_P_NODE=True"
    )

    print(
        "FINITE_WIDTH_TAPER_STILL_REQUIRES_LOADED_BVP=True"
    )

    print()
    print(
        "================================================================"
    )

    print(
        "R3B FINAL SCIENTIFIC RESULT"
    )

    print(
        "================================================================"
    )

    print(
        "DECISION="
        +
        decision[
            "decision"
        ]
    )

    print(
        "FINE_GLOBAL_MIRROR_FIELD_ENERGY_PRE_1G_J="
        +
        str(
            decision[
                "fine_global_energy_before_renormalization_j"
            ]
        )
    )

    print(
        "FINE_GLOBAL_MIRROR_FIELD_ENERGY_1G_J="
        +
        str(
            decision[
                "fine_global_energy_after_1g_renormalization_j"
            ]
        )
    )

    print(
        "LOW_JOULE_CLASS_PRESERVED="
        +
        str(
            decision[
                "low_joule_class_preserved"
            ]
        )
    )

    print(
        "SUB10KJ_PRESERVED="
        +
        str(
            decision[
                "sub10kj_preserved"
            ]
        )
    )

    print(
        "WHOLE_PAYLOAD_OUTWARD_BOTH_GRIDS="
        +
        str(
            decision[
                "whole_payload_outward_on_both_grids"
            ]
        )
    )

    print(
        "MIXED_FIELD_GRID_ENERGY_RELERR="
        +
        str(
            grid_energy_relerr
        )
    )

    print(
        "R3C_AUTHORIZED="
        +
        str(
            decision[
                "r3c_authorized"
            ]
        )
    )

    print(
        "SURFACE_CHARGE_PHYSICALIZED=False"
    )

    print(
        "PARITY_CP_COMPLETED=False"
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
        "HOOK17_CLOSED=False"
    )

    print(
        "NEXT="
        +
        decision[
            "next"
        ]
    )

    summary = {
        "branch":
            BRANCH,

        "decision":
            decision[
                "decision"
            ],

        "provenance":
            provenance,

        "claim_policy":
            claim_policy_gate(),

        "grid_results":
            grid_results,

        "polarization_node_corridor":
            node,

        "mixed_field_grid_energy_relative_difference":
            grid_energy_relerr,

        "low_joule_class_preserved":
            decision[
                "low_joule_class_preserved"
            ],

        "sub10kj_preserved":
            decision[
                "sub10kj_preserved"
            ],

        "whole_payload_outward_on_both_grids":
            decision[
                "whole_payload_outward_on_both_grids"
            ],

        "r3c_authorized":
            decision[
                "r3c_authorized"
            ],

        "surface_charge_physicalized":
            False,

        "parity_cp_completed":
            False,

        "full_loaded_topological_bvp_completed":
            False,

        "a12b_exact_massless_carrier_closed":
            False,

        "a12c_low_capacity_clue_discarded":
            False,

        "mixed_eb_topological_portal_closed":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "006d_replaced":
            False,

        "practical_device_found":
            False,

        "hook17_closed":
            False,

        "next":
            decision[
                "next"
            ],
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

    with fit_scan_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                fit_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            fit_rows
        )

    with interface_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                interface_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            interface_rows
        )

    print(
        "SUMMARY_PATH="
        +
        str(
            summary_path
        )
    )

    print(
        "MULTIPOLE_SCAN_PATH="
        +
        str(
            fit_scan_path
        )
    )

    print(
        "INTERFACE_PARETO_PATH="
        +
        str(
            interface_path
        )
    )


if __name__ == "__main__":
    main()
