"""B17-M5D: separation-preserving translation phase/pinning audit.

This is a reduced-action diagnostic on the corrected R3X1 two-carrier
system, reusing the compact net-neutral M5B surrogate. It holds source,
enclosure, material, portal scale and finite-box operators fixed except
for the specified rigid translations. A common displacement must not
change physical Earth/craft separation.

M5B uses tiny subcell shifts; M5C uses a whole-cell displacement. Their
slopes differ by orders of magnitude, but are NOT directly comparable
until both are evaluated on the same displacement path. This run samples
S(z_E, z_C) along Earth-only, craft-only and common-shift paths, and
measures drift and nonlinear grid-phase sensitivity.

The M5B source is an artificial compact surrogate, not B7 hardware.
Input profile shifts are not continuity-certified source motion.
On-shell action gradients are not physical spacecraft forces.
Fixed Dirichlet outer boundaries and finite ground geometry remain.
No complete action, Ward identity, exterior metric or energy certified.
"""

from __future__ import annotations

import math
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

BRANCH = "032H17A12D1R3X3B17-M5D"


def _offsets(h, small):
    fractions = (0.02, 0.1, 0.25, 0.5, 0.75, 1.0)
    positive = [small] + [h * value for value in fractions]

    if not small < h * 0.02:
        raise ValueError(
            "Small step must be below the 0.02-cell probe"
        )

    return sorted({
        0.0,
        *positive,
        *(-value for value in positive),
    })


def _slope(rows, key, step):
    return (
        rows[step][key] - rows[-step][key]
    ) / (2 * step)


def _path_samples(source, portal_ev, positions):
    """Solve and cache Earth-present and Earth-free action values.

    Cache retains scalar results only, rather than the full
    field-solution arrays.
    """
    memo = {}

    def action(earth, craft):
        key = (float(earth), float(craft))

        if key not in memo:
            value = pair_action(
                source,
                portal_ev,
                *key,
            )

            on = float(
                value["loaded"]["action_j"]
            )
            off = float(
                value["air_only"]["action_j"]
            )

            if not all(
                math.isfinite(v)
                for v in (on, off)
            ):
                raise ArithmeticError(
                    "Nonfinite stationary action"
                )

            memo[key] = {
                "earth_present_action_j": on,
                "earth_absent_action_j": off,
                "interaction_action_j": on-off,
            }

        return memo[key]

    common = {
        offset: action(offset, offset)
        for offset in positions
    }

    return common, action


def evaluate(
    h=0.25,
    bias=0.0,
    portal_ev=21147.0,
    small_step_m=0.0002,
    reverse_magnetic=False,
):
    """Evaluate three direct action paths at matched displacements."""

    if (
        h not in (0.25, 0.2)
        or bias not in (-0.5, 0.0, 0.5)
        or portal_ev != 21147.0
        or not math.isfinite(small_step_m)
        or not 1e-6 <= small_step_m < h * 0.02
    ):
        raise ValueError(
            "Unregistered B17-M5D preflight parameter"
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

    support = {
        label: source_support_check(
            source, shift
        )
        for label, shift in (
            ("minus_one_cell", -h),
            ("plus_one_cell", h),
        )
    }

    if not all(
        item["inside_enclosure_radius"]
        for item in support.values()
    ):
        raise ArithmeticError(
            "A source translation escaped the craft enclosure"
        )

    offsets = _offsets(
        h, small_step_m
    )

    common, action = _path_samples(
        source,
        portal_ev,
        offsets,
    )

    # All three paths use IDENTICAL displacements.
    axis_offsets = (
        -h,
        -small_step_m,
        0.0,
        small_step_m,
        h,
    )

    earth = {
        s: action(s, 0.0)
        for s in axis_offsets
    }

    craft = {
        s: action(0.0, s)
        for s in axis_offsets
    }

    keys = (
        "earth_present_action_j",
        "earth_absent_action_j",
        "interaction_action_j",
    )

    paired = {}

    for step, name in (
        (small_step_m, "subcell"),
        (h, "one_cell"),
    ):
        paired[name] = {}

        for key in keys:
            de = _slope(
                earth, key, step
            )

            dc = _slope(
                craft, key, step
            )

            dcommon = _slope(
                common, key, step
            )

            paired[name][key] = {
                "earth_only_slope_j_per_m": de,
                "craft_only_slope_j_per_m": dc,
                "paired_sum_slope_j_per_m":
                    de + dc,
                "common_shift_slope_j_per_m":
                    dcommon,
                "path_nonlinearity_difference_j_per_m":
                    dcommon - (de + dc),
            }

    path_values = [
        common[s]["interaction_action_j"]
        for s in offsets
    ]

    lower = common[-h][
        "interaction_action_j"
    ]

    upper = common[h][
        "interaction_action_j"
    ]

    center = common[0.0][
        "interaction_action_j"
    ]

    # Subtract the line between full-cell endpoints.
    # Remaining structure is NOT a physical force.
    nonlinear = [
        val - (
            lower
            + (s+h)*(upper-lower)/(2*h)
        )
        for s, val in zip(
            offsets, path_values
        )
    ]

    jumps = [
        (
            path_values[i+1]
            - path_values[i]
        ) / (
            offsets[i+1]
            - offsets[i]
        )
        for i in range(
            len(offsets)-1
        )
    ]

    small_slope = paired[
        "subcell"
    ]["interaction_action_j"][
        "common_shift_slope_j_per_m"
    ]

    large_slope = (
        upper - lower
    ) / (2*h)

    return {
        "branch": BRANCH,
        "scope":
            "DIRECT_ON_SHELL_ACTION_GRID_PHASE_DIAGNOSTIC_NOT_FORCE",
        "h_m": h,
        "source_bias": bias,
        "portal_ev": portal_ev,
        "small_displacement_m":
            small_step_m,
        "magnetic_reversed":
            bool(reverse_magnetic),

        "source": {
            "max_compact_radius_m":
                audit[
                    "max_nonzero_source_radius_m"
                ],
            "net_electric_charge_relative_residual":
                audit[
                    "net_electric_charge_relative_residual"
                ],
            "support_one_cell": support,
        },

        "common_shift_phase_samples": [
            {
                "shift_m": float(s),
                **common[s],
            }
            for s in offsets
        ],

        "matched_earth_and_craft_slopes":
            paired,

        "grid_phase_diagnostics": {
            "common_interaction_center_j":
                center,
            "one_cell_end_to_end_action_change_j":
                upper-lower,
            "one_cell_mean_slope_j_per_m":
                large_slope,
            "maximum_abs_deviation_from_endpoint_line_j":
                float(max(
                    abs(v)
                    for v in nonlinear
                )),
            "phase_span_interaction_action_j":
                float(
                    max(path_values)
                    - min(path_values)
                ),
            "min_adjacent_secant_j_per_m":
                float(min(jumps)),
            "max_adjacent_secant_j_per_m":
                float(max(jumps)),
            "subcell_to_one_cell_slope_ratio":
                float(
                    abs(small_slope)
                    / max(
                        abs(large_slope),
                        1e-20,
                    )
                ),
        },

        "source_translation_continuity_certified":
            False,
        "finite_box_artifact_excluded": False,
        "full_Earth_craft_Noether_identity_certified":
            False,
        "exterior_metric_transmission_derived":
            False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }
