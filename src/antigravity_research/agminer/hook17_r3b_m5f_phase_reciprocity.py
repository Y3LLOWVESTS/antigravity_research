"""B17 ALPHA-1 M5F: phase-ensemble reciprocity preflight.

Averaging over absolute grid phase is an artifact diagnostic, not a
continuum, source, Ward, force, or spacecraft-lift certificate.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from .hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from .hook17_r3b_m5b_compact_transfer import (
    compact_shaped_source,
)
from .hook17_r3b_m4b4_paired_translation import (
    pair_action,
    source_support_check,
)

BRANCH = "032H17A12D1R3X3B17-ALPHA1-M5F"

KEYS = (
    "earth_present_action_j",
    "earth_absent_action_j",
    "interaction_action_j",
)


def phase_positions(h, bins, offset=0.5):
    if (
        not isinstance(bins, int)
        or bins < 2
        or bins > 64
        or not 0 <= offset < 1
    ):
        raise ValueError("Invalid phase quadrature")

    return [
        round(
            h * ((k + offset) / bins - 0.5),
            12,
        )
        for k in range(bins)
    ]


def _relative_difference(a, b):
    return (
        abs(a - b)
        / max(abs(a), abs(b), 1.0)
    )


def evaluate(
    h=0.25,
    bias=0.0,
    reverse_magnetic=False,
    displacement_m=0.0002,
    reference=None,
):
    if (
        h not in (0.25, 0.2)
        or bias not in (0.0, 0.5)
        or not isinstance(reverse_magnetic, bool)
        or not math.isfinite(displacement_m)
        or not 1e-6 <= displacement_m < 0.001
    ):
        raise ValueError(
            "Unsupported ALPHA-1-M5F control"
        )

    source, audit = compact_shaped_source(
        assemble_original_aligned_source(h),
        bias,
    )

    if reverse_magnetic:
        source = {
            **source,
            "j_a": -np.asarray(source["j_a"]),
        }

    support = [
        source_support_check(
            source,
            sign * (h / 2 + displacement_m),
        )
        for sign in (-1.0, 1.0)
    ]

    if not all(
        row["inside_enclosure_radius"]
        for row in support
    ):
        raise ArithmeticError(
            "ALPHA-1 source escaped enclosure"
        )

    cache = {}

    def action(earth_m, craft_m):
        key = (
            round(float(earth_m), 12),
            round(float(craft_m), 12),
        )

        if key not in cache:
            result = pair_action(
                source, 21147.0, *key
            )

            on = float(
                result["loaded"]["action_j"]
            )
            off = float(
                result["air_only"]["action_j"]
            )

            if (
                not math.isfinite(on)
                or not math.isfinite(off)
            ):
                raise ArithmeticError(
                    "Nonfinite reduced action"
                )

            cache[key] = {
                "earth_present_action_j": on,
                "earth_absent_action_j": off,
                "interaction_action_j": on - off,
            }

        return cache[key]

    def at_phase(s):
        d = displacement_m

        samples = {
            "center": action(s, s),
            "earth_plus": action(s + d, s),
            "earth_minus": action(s - d, s),
            "craft_plus": action(s, s + d),
            "craft_minus": action(s, s - d),
            "common_plus": action(s + d, s + d),
            "common_minus": action(s - d, s - d),
        }

        slopes = {}

        for key in KEYS:
            earth = (
                samples["earth_plus"][key]
                - samples["earth_minus"][key]
            ) / (2*d)

            craft = (
                samples["craft_plus"][key]
                - samples["craft_minus"][key]
            ) / (2*d)

            common = (
                samples["common_plus"][key]
                - samples["common_minus"][key]
            ) / (2*d)

            slopes[key] = {
                "earth_only_j_per_m": earth,
                "craft_only_j_per_m": craft,
                "paired_sum_j_per_m":
                    earth + craft,
                "common_shift_j_per_m":
                    common,
                "nonlinear_path_difference_j_per_m":
                    common - earth - craft,
            }

        return {
            "phase_m": s,
            "center_interaction_action_j":
                samples["center"][
                    "interaction_action_j"
                ],
            "slopes": slopes,
        }

    def quadrature(bins, offset):
        phase_rows = [
            at_phase(s)
            for s in phase_positions(
                h, bins, offset
            )
        ]

        averaged = {}

        for key in KEYS:
            names = tuple(
                phase_rows[0]["slopes"][key]
            )

            averaged[key] = {
                name: float(np.mean([
                    p["slopes"][key][name]
                    for p in phase_rows
                ]))
                for name in names
            }

            r = averaged[key]

            r["relative_reciprocity_defect"] = (
                abs(r["paired_sum_j_per_m"])
                / max(
                    abs(r["earth_only_j_per_m"]),
                    abs(r["craft_only_j_per_m"]),
                    1.0,
                )
            )

            r["relative_common_drift"] = (
                abs(r["common_shift_j_per_m"])
                / max(
                    abs(r["earth_only_j_per_m"]),
                    abs(r["craft_only_j_per_m"]),
                    1.0,
                )
            )

        baseline = [
            p["center_interaction_action_j"]
            for p in phase_rows
        ]

        return {
            "bins": bins,
            "phase_offset_bins": offset,
            "mean_interaction_action_j":
                float(np.mean(baseline)),
            "interaction_phase_span_j":
                float(
                    max(baseline)
                    - min(baseline)
                ),
            "average_slopes": averaged,
            "phase_rows": phase_rows,
        }

    midpoint4 = quadrature(4, 0.5)
    midpoint8 = quadrature(8, 0.5)
    node4 = quadrature(4, 0.0)

    convergence = {}

    for key in KEYS:
        convergence[key] = {
            name: _relative_difference(
                midpoint4[
                    "average_slopes"
                ][key][name],
                midpoint8[
                    "average_slopes"
                ][key][name],
            )
            for name in (
                "earth_only_j_per_m",
                "craft_only_j_per_m",
                "common_shift_j_per_m",
                "paired_sum_j_per_m",
            )
        }

    center = at_phase(0.0)

    reference_errors = None

    if reference is not None:
        old = json.loads(
            Path(reference).read_text(
                encoding="utf-8"
            )
        )

        if (
            old.get("branch")
            != "032H17A12D1R3X3B17-M5D"
            or abs(old["h_m"] - h) > 1e-12
            or abs(
                old["source_bias"] - bias
            ) > 1e-12
            or bool(
                old["magnetic_reversed"]
            ) != reverse_magnetic
            or abs(
                old["small_displacement_m"]
                - displacement_m
            ) > 1e-12
        ):
            raise ValueError(
                "M5D historical control mismatch"
            )

        old_slopes = old[
            "matched_earth_and_craft_slopes"
        ]["subcell"]

        mappings = {
            "earth_only_j_per_m":
                "earth_only_slope_j_per_m",
            "craft_only_j_per_m":
                "craft_only_slope_j_per_m",
            "paired_sum_j_per_m":
                "paired_sum_slope_j_per_m",
            "common_shift_j_per_m":
                "common_shift_slope_j_per_m",
        }

        reference_errors = {
            key: {
                new: abs(
                    center["slopes"][key][new]
                    - old_slopes[key][oldname]
                )
                for new, oldname
                in mappings.items()
            }
            for key in KEYS
        }

    estimate = midpoint8[
        "average_slopes"
    ]["interaction_action_j"]

    quadrature_variation = max(
        convergence[
            "interaction_action_j"
        ]["earth_only_j_per_m"],
        convergence[
            "interaction_action_j"
        ]["craft_only_j_per_m"],
    )

    return {
        "branch": BRANCH,
        "h_m": h,
        "bias": bias,
        "reverse_magnetic":
            reverse_magnetic,
        "displacement_m":
            displacement_m,

        "source_audit": {
            "net_electric_charge_relative_residual":
                float(
                    audit[
                        "net_electric_charge_relative_residual"
                    ]
                ),
            "max_source_radius_m":
                float(
                    audit[
                        "max_nonzero_source_radius_m"
                    ]
                ),
            "compensation_charge_before":
                float(
                    audit[
                        "compensation_charge_before"
                    ]
                ),
            "support_extremes": support,
            "same_physical_source_across_grids_certified":
                False,
        },

        "quadratures": {
            "midpoint4": midpoint4,
            "midpoint8": midpoint8,
            "node4": node4,
        },

        "quadrature_relative_differences_4_to_8":
            convergence,

        "node4_vs_midpoint4_mean_interaction_difference_j":
            float(
                node4[
                    "mean_interaction_action_j"
                ]
                - midpoint4[
                    "mean_interaction_action_j"
                ]
            ),

        "central_historical_reference_abs_errors_j_per_m":
            reference_errors,

        "diagnostic_gates": {
            "quadrature_4_to_8_earth_craft_within_5pct":
                quadrature_variation <= 0.05,

            "phase_averaged_reciprocity_defect_within_5pct":
                estimate[
                    "relative_reciprocity_defect"
                ] <= 0.05,

            "phase_averaged_common_drift_within_5pct":
                estimate[
                    "relative_common_drift"
                ] <= 0.05,

            "reference_reproduced_within_0p1_j_per_m":
                (
                    reference_errors is not None
                    and max(
                        error
                        for group
                        in reference_errors.values()
                        for error
                        in group.values()
                    ) <= 0.1
                ),
        },

        "phase_averaged_gradient_is_physical_force":
            False,
        "interface_action_discretization_certified":
            False,
        "finite_box_artifact_excluded":
            False,
        "full_Earth_craft_Noether_identity_certified":
            False,
        "exterior_metric_transmission_derived":
            False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }
