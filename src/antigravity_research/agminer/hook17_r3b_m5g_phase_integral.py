"""ALPHA-1R2/M5G: endpoint identity and phase quadrature audit.

The current and material are translated within the same finite-grid
reduced operator. These are stationary action diagnostics, not
mechanical forces, Ward identities, spacecraft lift, or device energy.

Averaging over absolute grid phase cannot create physical reciprocity.
The fundamental theorem of calculus provides an independent exact
one-cell mean-derivative target for the sampled common-shift path.
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

BRANCH = "032H17A12D1R3X3B17-ALPHA1R2-M5G"


def phase_nodes(h: float, count: int) -> list[float]:
    if (
        h not in (0.2, 0.25)
        or type(count) is not int
        or count < 2
    ):
        raise ValueError(
            "Unregistered grid or phase count"
        )

    return [
        round(
            h * (
                (i + 0.5) / count - 0.5
            ),
            12,
        )
        for i in range(count)
    ]


def endpoint_integral(
    left: float,
    right: float,
    h: float,
) -> float:
    if (
        not all(
            map(
                math.isfinite,
                (left, right, h),
            )
        )
        or h <= 0
    ):
        raise ValueError(
            "Invalid endpoint integral"
        )

    return (right - left) / h


def phase_mean_slopes(
    action,
    h: float,
    count: int,
    step: float,
) -> dict:
    rows = []

    for s in phase_nodes(h, count):
        earth = (
            action(s + step, s)
            - action(s - step, s)
        ) / (2 * step)

        craft = (
            action(s, s + step)
            - action(s, s - step)
        ) / (2 * step)

        common = (
            action(s + step, s + step)
            - action(s - step, s - step)
        ) / (2 * step)

        rows.append((
            earth,
            craft,
            common,
            action(s, s),
        ))

    array = np.asarray(
        rows,
        dtype=float,
    )

    if not np.all(np.isfinite(array)):
        raise ArithmeticError(
            "Nonfinite phase response"
        )

    earth, craft, common, center = (
        array.mean(axis=0)
    )

    return {
        "phase_count": count,

        "earth_only_j_per_m":
            float(earth),

        "craft_only_j_per_m":
            float(craft),

        "paired_sum_j_per_m":
            float(earth + craft),

        "common_shift_j_per_m":
            float(common),

        "common_minus_paired_j_per_m":
            float(common - earth - craft),

        "phase_action_mean_j":
            float(center),

        "phase_action_span_j":
            float(
                np.ptp(array[:, 3])
            ),
    }


def _archive_sanity(
    old,
    previous,
    h,
    bias,
    reversed_field,
    step,
):
    if (
        old.get("branch")
        != "032H17A12D1R3X3B17-M5D"

        or previous.get("branch")
        != "032H17A12D1R3X3B17-ALPHA1-M5F"

        or any(
            abs(record["h_m"] - h) > 1e-12
            for record in (old, previous)
        )

        or abs(
            old["source_bias"] - bias
        ) > 1e-12

        or abs(
            previous["bias"] - bias
        ) > 1e-12

        or bool(
            old["magnetic_reversed"]
        ) != reversed_field

        or bool(
            previous["reverse_magnetic"]
        ) != reversed_field

        or abs(
            previous["displacement_m"]
            - step
        ) > 1e-12
    ):
        raise ValueError(
            "Historical control mismatch"
        )


def evaluate(
    h,
    bias,
    reverse_magnetic,
    m5d_path,
    m5f_path,
    step=0.0002,
):
    if (
        h not in (0.2, 0.25)
        or bias != 0.0
        or type(reverse_magnetic) is not bool
        or not math.isfinite(step)
        or not 1e-6 <= step <= 0.0005
    ):
        raise ValueError(
            "Unregistered M5G control"
        )

    old = json.loads(
        Path(m5d_path).read_text(
            encoding="utf-8"
        )
    )

    previous = json.loads(
        Path(m5f_path).read_text(
            encoding="utf-8"
        )
    )

    _archive_sanity(
        old,
        previous,
        h,
        bias,
        reverse_magnetic,
        step,
    )

    source, audit = compact_shaped_source(
        assemble_original_aligned_source(h),
        bias,
    )

    if reverse_magnetic:
        source = {
            **source,
            "j_a": -np.asarray(
                source["j_a"]
            ),
        }

    support = [
        source_support_check(
            source,
            sign * (h / 2 + step),
        )
        for sign in (-1, 1)
    ]

    if not all(
        row["inside_enclosure_radius"]
        for row in support
    ):
        raise ArithmeticError(
            "Source escaped enclosure"
        )

    cache = {}

    def action(e, c):
        key = (
            round(float(e), 12),
            round(float(c), 12),
        )

        if key not in cache:
            state = pair_action(
                source,
                21147.0,
                *key,
            )

            loaded = float(
                state["loaded"]["action_j"]
            )

            free = float(
                state["air_only"]["action_j"]
            )

            if (
                not math.isfinite(loaded)
                or not math.isfinite(free)
            ):
                raise ArithmeticError(
                    "Nonfinite coupled action"
                )

            cache[key] = loaded - free

        return cache[key]

    left = action(
        -h / 2,
        -h / 2,
    )

    right = action(
        h / 2,
        h / 2,
    )

    exact = endpoint_integral(
        left,
        right,
        h,
    )

    known = {
        round(
            float(row["shift_m"]),
            12,
        ): float(
            row["interaction_action_j"]
        )
        for row in old[
            "common_shift_phase_samples"
        ]
    }

    left_key = round(-h / 2, 12)
    right_key = round(h / 2, 12)

    archival_expected = endpoint_integral(
        known[left_key],
        known[right_key],
        h,
    )

    endpoint_error = max(
        abs(left - known[left_key]),
        abs(right - known[right_key]),
    )

    if endpoint_error > 1e-5:
        raise ArithmeticError(
            "M5D endpoint failed reproduction"
        )

    quadratures = {
        str(n): phase_mean_slopes(
            action,
            h,
            n,
            step,
        )
        for n in (8, 16, 32)
    }

    historic = previous[
        "quadratures"
    ]["midpoint8"][
        "average_slopes"
    ]["interaction_action_j"]

    current8 = quadratures["8"]

    historical_error = max(
        abs(
            current8["earth_only_j_per_m"]
            - historic["earth_only_j_per_m"]
        ),
        abs(
            current8["craft_only_j_per_m"]
            - historic["craft_only_j_per_m"]
        ),
        abs(
            current8["common_shift_j_per_m"]
            - historic["common_shift_j_per_m"]
        ),
    )

    if historical_error > 1e-4:
        raise ArithmeticError(
            "M5F eight-phase reproduction failed"
        )

    errors = {}

    for count in (8, 16, 32):
        key = str(count)

        difference = abs(
            quadratures[key][
                "common_shift_j_per_m"
            ] - exact
        )

        errors[key] = {
            "absolute_common_drift_error_j_per_m":
                difference,

            "normalized_common_drift_error":
                difference / max(
                    abs(exact),
                    1.0,
                ),
        }

    latest = quadratures["32"]

    relative_reciprocity_defect = (
        abs(
            latest["paired_sum_j_per_m"]
        )
        / max(
            abs(latest["earth_only_j_per_m"]),
            abs(latest["craft_only_j_per_m"]),
            1.0,
        )
    )

    return {
        "branch": BRANCH,
        "grid_m": h,
        "reverse_magnetic":
            reverse_magnetic,

        "source_compensation_charge_before":
            float(
                audit["compensation_charge_before"]
            ),

        "source_relative_net_charge_residual":
            float(
                audit[
                    "net_electric_charge_relative_residual"
                ]
            ),

        "source_physical_equivalence_between_grids_proven":
            False,

        "endpoint_common_shift_action_j": {
            "minus_half_cell_j": left,
            "plus_half_cell_j": right,
        },

        "exact_one_cell_mean_common_derivative_j_per_m":
            exact,

        "m5d_archived_endpoint_identity_j_per_m":
            archival_expected,

        "m5d_archived_endpoint_reproduction_error_j":
            endpoint_error,

        "m5f_eight_phase_reproduction_error_j_per_m":
            historical_error,

        "quadratures": quadratures,

        "quadrature_errors_against_exact_identity":
            errors,

        "relative_32phase_reciprocity_defect":
            relative_reciprocity_defect,

        "diagnostic_gates": {
            "exact_endpoint_action_reproduced":
                endpoint_error <= 1e-5,

            "m5f_eight_phase_reproduced":
                historical_error <= 1e-4,

            "32phase_common_integral_absolute_error_below_0p5_j_per_m":
                errors["32"][
                    "absolute_common_drift_error_j_per_m"
                ] < 0.5,

            "32phase_apparent_reciprocity_below_5pct":
                relative_reciprocity_defect < 0.05,
        },

        "phase_averaging_is_noether_identity":
            False,

        "source_ward_identity_certified":
            False,

        "exterior_metric_transmission_derived":
            False,

        "whole_craft_force_n": None,

        "complete_operating_energy_j": None,

        "006d_replaced": False,
    }
