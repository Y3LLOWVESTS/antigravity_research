"""ALPHA-1R3 / B17-M5H: source provenance and quadrature audit.

PURPOSE:
Determine how the independently generated 0.20 m and 0.25 m
artificial source arrays differ. Confirm observed integration
convergence against the exact saved one-cell action identity.

LIMITATIONS:
Discrete array sums are not physical continuum integrals.
Extrapolated action gradients are not measured forces.
This diagnostic cannot certify Ward identities, Earth reaction,
exterior metric transmission, or spacecraft lift.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from antigravity_research.agminer.hook17_r3b_m5b_compact_transfer import (
    compact_shaped_source,
)


BRANCH = "032H17A12D1R3X3B17-ALPHA1R3-M5H"


def richardson_second_order(g16, g32):
    return (
        4.0 * float(g32) - float(g16)
    ) / 3.0


def source_fingerprint(h):
    source, audit = compact_shaped_source(
        assemble_original_aligned_source(h),
        0.0,
    )

    arrays = {}

    for key, value in sorted(source.items()):
        a = np.asarray(value)

        if (
            a.ndim == 0
            or a.dtype.kind not in "iufc"
        ):
            continue

        if not np.all(np.isfinite(a)):
            raise ArithmeticError(
                f"Nonfinite source array: {key}"
            )

        magnitude = np.abs(a)

        arrays[key] = {
            "shape": list(a.shape),

            "max_abs":
                float(magnitude.max(initial=0.0)),

            "l1_discrete":
                float(magnitude.sum()),

            "l2_discrete":
                float(np.linalg.norm(a.ravel())),

            "nonzero_nodes":
                int(np.count_nonzero(a)),

            "h2_weighted_l1_diagnostic":
                float(magnitude.sum() * h**2),

            "h3_weighted_l1_diagnostic":
                float(magnitude.sum() * h**3),
        }

    if not arrays:
        raise ArithmeticError(
            "No numerical source arrays found"
        )

    return {
        "grid_m": h,

        "array_fingerprints": arrays,

        "compensation_charge_before_raw":
            float(
                audit["compensation_charge_before"]
            ),

        "electric_net_charge_relative_residual":
            float(
                audit[
                    "net_electric_charge_relative_residual"
                ]
            ),

        "max_nonzero_source_radius_m":
            float(
                audit[
                    "max_nonzero_source_radius_m"
                ]
            ),

        "common_continuum_source_definition_available":
            False,

        "current_continuity_Ward_certified":
            False,

        "array_norms_are_physical_integrals":
            False,
    }


def analyze(records):
    expected = (
        ("original_h025", 0.25, False),
        ("original_h020", 0.2, False),
        ("reversed_h025", 0.25, True),
    )

    reports = {}

    for key, h, reverse in expected:
        r = records[key]

        if (
            r.get("branch")
            != "032H17A12D1R3X3B17-ALPHA1R2-M5G"
            or r.get("grid_m") != h
            or r.get("reverse_magnetic")
            is not reverse
        ):
            raise ValueError(
                f"M5G historical control mismatch: {key}"
            )

        exact = float(
            r[
                "exact_one_cell_mean_common_derivative_j_per_m"
            ]
        )

        estimates = {
            n: float(
                r["quadratures"][str(n)][
                    "common_shift_j_per_m"
                ]
            )
            for n in (8, 16, 32)
        }

        errors = {
            n: abs(estimates[n] - exact)
            for n in (8, 16, 32)
        }

        extrap = richardson_second_order(
            estimates[16],
            estimates[32],
        )

        ratio8to16 = (
            errors[8]
            / max(errors[16], 1e-15)
        )

        ratio16to32 = (
            errors[16]
            / max(errors[32], 1e-15)
        )

        reports[key] = {
            "exact_one_cell_mean_common_shift_j_per_m":
                exact,

            "phase_errors_j_per_m": {
                str(k): v
                for k, v in errors.items()
            },

            "error_reduction_8_to_16":
                ratio8to16,

            "error_reduction_16_to_32":
                ratio16to32,

            "second_order_extrapolated_common_shift_j_per_m":
                extrap,

            "extrapolation_absolute_error_j_per_m":
                abs(extrap - exact),

            "observed_second_order_error_scaling":
                (
                    3.0 < ratio8to16 < 5.0
                    and
                    3.0 < ratio16to32 < 5.0
                ),

            "extrapolation_within_0p025_j_per_m":
                abs(extrap - exact) < 0.025,

            "phase32_earth_gradient_j_per_m":
                float(
                    r["quadratures"]["32"][
                        "earth_only_j_per_m"
                    ]
                ),

            "phase32_craft_gradient_j_per_m":
                float(
                    r["quadratures"]["32"][
                        "craft_only_j_per_m"
                    ]
                ),
        }

    a = reports["original_h025"][
        "phase32_earth_gradient_j_per_m"
    ]

    b = reports["original_h020"][
        "phase32_earth_gradient_j_per_m"
    ]

    return {
        "branch": BRANCH,

        "quadrature_closeout": reports,

        "cross_grid_earth_gradient_relative_difference_unmatched_sources":
            abs(a - b)
            / max(abs(a), abs(b), 1.0),

        "source_fingerprints": {
            "original_h025":
                source_fingerprint(0.25),

            "original_h020":
                source_fingerprint(0.2),
        },

        "scientific_certification": {
            "quadrature_rule_diagnostic_explained":
                all(
                    row[
                        "observed_second_order_error_scaling"
                    ]
                    and row[
                        "extrapolation_within_0p025_j_per_m"
                    ]
                    for row in reports.values()
                ),

            "identical_continuum_source_crossgrid":
                False,

            "discrete_current_Ward_or_Noether_identity":
                False,

            "continuum_material_interface":
                False,

            "finite_box_artifact_excluded":
                False,

            "physical_earth_craft_reciprocity":
                False,

            "exterior_metric_transmission":
                False,

            "whole_craft_lift":
                False,

            "complete_energy_below_10MJ":
                False,

            "006d_replaced":
                False,
        },
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--original-h025",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--original-h020",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--reversed-h025",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    records = {
        "original_h025":
            json.loads(
                args.original_h025.read_text()
            ),

        "original_h020":
            json.loads(
                args.original_h020.read_text()
            ),

        "reversed_h025":
            json.loads(
                args.reversed_h025.read_text()
            ),
    }

    result = analyze(records)

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            result,
            indent=2,
            allow_nan=False,
        ) + "\n"
    )

    print(
        json.dumps(
            result,
            indent=2,
            allow_nan=False,
        )
    )


if __name__ == "__main__":
    main()
