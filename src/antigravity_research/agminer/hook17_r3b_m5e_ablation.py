"""B17-M5E: exact source-interpolation versus material-sampling ablation.

Same static reduced two-carrier R3X1 operator and net-neutral compact M5B
surrogate as M5D. Do not change source physics or the matter portal.

For simultaneous common displacement s, evaluate three deliberately
counterfactual paths:

    FULL:          I(j_s, beta_s)
    SOURCE-ONLY:   I(j_s, beta_0)
    MATERIAL-ONLY: I(j_0, beta_s)

I denotes the Earth-present on-shell action minus Earth-free action.

The mixed difference is then computed exactly. Only FULL translates
the entire modeled arrangement; the other paths are NOT valid
independent mechanical motions.

For linear current interpolation within one grid cell, the weighted
on-shell quadratic action obeys an exact midpoint identity.
An independently re-solved difference-current control measures the
corresponding interpolation curvature at frozen material coefficients.

No action slope certifies physical force or a Ward/Noether identity.
Finite box, microscopic source, material stress and physical
gravity remain incomplete. No whole-craft lift or device energy.
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
from .hook17_r3b_m4b2_earth_variational_audit import (
    _on_shell_action,
    _weights,
)
from .hook17_r3b_m4b4_paired_translation import (
    shifted_material,
    shifted_source,
    source_support_check,
)
from .hook17_r3b_m4b_sparse_earth_loading import (
    _solve_fixed_sources,
)

BRANCH = "032H17A12D1R3X3B17-M5E"


def _state_action(source, weights, currents, beta):
    state = _solve_fixed_sources(
        currents, beta, 1.0
    )
    if state["residual"] > 1e-8:
        raise ArithmeticError(
            "Carrier solve residual unacceptable"
        )
    return (
        _on_shell_action(state, currents, weights),
        float(state["residual"]),
    )


def _pair_action(
    source, weights, currents, on_beta, off_beta
):
    on, ron = _state_action(
        source, weights, currents, on_beta
    )
    off, roff = _state_action(
        source, weights, currents, off_beta
    )
    return {
        "earth_present_action_j": on,
        "earth_absent_action_j": off,
        "interaction_action_j": on - off,
    }, max(ron, roff)


def _secant(rows, step):
    return (
        rows[step]["interaction_action_j"]
        - rows[-step]["interaction_action_j"]
    ) / (2 * step)


def evaluate(
    h=0.25,
    bias=0.0,
    reverse_magnetic=False,
    small_step_m=0.0002,
    portal_ev=21147.0,
    reference=None,
):
    """Separate source and material phases at matched positions."""

    if (
        h not in (0.25, 0.2)
        or bias not in (0.0, 0.5)
        or portal_ev != 21147.0
        or not math.isfinite(small_step_m)
        or not 1e-6 <= small_step_m < 0.02*h
    ):
        raise ValueError("Unregistered M5E control")

    base, audit = compact_shaped_source(
        assemble_original_aligned_source(h),
        bias,
    )

    if reverse_magnetic:
        base = {
            **base,
            "j_a": -base["j_a"],
        }

    support = [
        source_support_check(base, value)
        for value in (-h, h)
    ]

    if not all(
        item["inside_enclosure_radius"]
        for item in support
    ):
        raise ArithmeticError(
            "Source escaped enclosure"
        )

    weights = _weights(base)

    positions = (
        -h,
        -h/2,
        -small_step_m,
        0.0,
        small_step_m,
        h/2,
        h,
    )

    currents = {
        s: shifted_source(
            base, portal_ev, s
        )
        for s in positions
    }

    beta = {
        s: {
            flag: shifted_material(
                base, s, s, portal_ev,
                earth_present=flag,
            )[0]
            for flag in (True, False)
        }
        for s in positions
    }

    outputs = {
        name: {}
        for name in (
            "full",
            "source_only",
            "material_only",
        )
    }

    max_residual = 0.0

    for s in positions:
        variants = {
            "full": (
                currents[s], beta[s]
            ),
            "source_only": (
                currents[s], beta[0.0]
            ),
            "material_only": (
                currents[0.0], beta[s]
            ),
        }

        for name, (current, material) in variants.items():
            result, residual = _pair_action(
                base,
                weights,
                current,
                material[True],
                material[False],
            )
            outputs[name][s] = result
            max_residual = max(
                max_residual, residual
            )

    center = outputs["full"][0.0][
        "interaction_action_j"
    ]

    samples = []

    for s in positions:
        full = outputs["full"][s][
            "interaction_action_j"
        ]
        source_only = outputs["source_only"][s][
            "interaction_action_j"
        ]
        material_only = outputs["material_only"][s][
            "interaction_action_j"
        ]

        samples.append({
            "translation_m": float(s),
            "full_interaction_action_j": full,
            "source_only_counterfactual_interaction_j":
                source_only,
            "material_only_counterfactual_interaction_j":
                material_only,
            "mixed_counterfactual_interaction_j":
                full-source_only-material_only+center,
        })

    # Independent quadratic source-increment control.
    # At fixed material beta, on-shell action is quadratic
    # in the source-current vector.

    j0 = currents[0.0]
    jh = currents[h]
    jhalf = currents[h/2]

    delta_source = {
        **j0,
        "j_phi": jh["j_phi"] - j0["j_phi"],
        "j_a": jh["j_a"] - j0["j_a"],
    }

    increment, residual = _pair_action(
        base,
        weights,
        delta_source,
        beta[0.0][True],
        beta[0.0][False],
    )

    max_residual = max(
        max_residual, residual
    )

    source_curvature = (
        outputs["source_only"][h/2][
            "interaction_action_j"
        ]
        - 0.5 * (
            outputs["source_only"][0.0][
                "interaction_action_j"
            ]
            + outputs["source_only"][h][
                "interaction_action_j"
            ]
        )
    )

    predicted_curvature = (
        -0.25 * increment["interaction_action_j"]
    )

    linear_phi_error = (
        np.linalg.norm(
            jhalf["j_phi"]
            - 0.5 * (j0["j_phi"] + jh["j_phi"])
        )
        / max(np.linalg.norm(j0["j_phi"]), 1.0)
    )

    linear_a_error = (
        np.linalg.norm(
            jhalf["j_a"]
            - 0.5 * (j0["j_a"] + jh["j_a"])
        )
        / max(np.linalg.norm(j0["j_a"]), 1.0)
    )

    def curvature(name):
        values = outputs[name]
        return (
            values[h/2]["interaction_action_j"]
            - 0.5 * (
                values[0.0]["interaction_action_j"]
                + values[h]["interaction_action_j"]
            )
        )

    decomposition = {}

    for name in outputs:
        decomposition[name] = {
            "small_symmetric_slope_j_per_m":
                _secant(outputs[name], small_step_m),
            "one_cell_symmetric_slope_j_per_m":
                _secant(outputs[name], h),
            "positive_halfcell_deviation_from_endpoint_chord_j":
                curvature(name),
            "positive_halfcell_interaction_change_from_center_j":
                outputs[name][h/2][
                    "interaction_action_j"
                ] - center,
        }

    keys = (
        "small_symmetric_slope_j_per_m",
        "one_cell_symmetric_slope_j_per_m",
        "positive_halfcell_deviation_from_endpoint_chord_j",
    )

    mixed = {
        key: (
            decomposition["full"][key]
            - decomposition["source_only"][key]
            - decomposition["material_only"][key]
        )
        for key in keys
    }

    mixed[
        "positive_halfcell_interaction_change_from_center_j"
    ] = samples[5][
        "mixed_counterfactual_interaction_j"
    ]

    decomposition["mixed_difference"] = mixed

    reproduction = None

    if reference is not None:
        import json
        from pathlib import Path

        previous = json.loads(
            Path(reference).read_text(
                encoding="utf-8"
            )
        )

        if (
            previous.get("branch")
            != "032H17A12D1R3X3B17-M5D"
            or abs(previous["h_m"] - h) > 1e-12
            or bool(previous["magnetic_reversed"])
               != bool(reverse_magnetic)
            or abs(previous["source_bias"] - bias) > 1e-12
        ):
            raise ValueError(
                "Historical M5D controls mismatch"
            )

        lookup = {
            float(row["shift_m"]):
                row["interaction_action_j"]
            for row in previous[
                "common_shift_phase_samples"
            ]
        }

        differences = []

        for s in positions:
            old_position = min(
                lookup,
                key=lambda value: abs(value-s),
            )

            if abs(old_position-s) > 1e-9:
                raise ValueError(
                    "Historical M5D sample missing"
                )

            differences.append(
                abs(
                    outputs["full"][s][
                        "interaction_action_j"
                    ]
                    - lookup[old_position]
                )
            )

        reproduction = max(differences)

    return {
        "branch": BRANCH,
        "h_m": h,
        "bias": bias,
        "portal_ev": portal_ev,
        "magnetic_reversed":
            bool(reverse_magnetic),
        "small_displacement_m":
            small_step_m,
        "source_net_charge_relative_residual":
            audit[
                "net_electric_charge_relative_residual"
            ],
        "source_max_radius_m":
            audit[
                "max_nonzero_source_radius_m"
            ],
        "source_support_extreme_shifts":
            support,
        "samples": samples,
        "decomposition": decomposition,
        "frozen_material_quadratic_midpoint_identity": {
            "source_halfcell_is_linear_interpolant_relative_error_phi":
                float(linear_phi_error),
            "source_halfcell_is_linear_interpolant_relative_error_a":
                float(linear_a_error),
            "source_only_chord_curvature_j":
                float(source_curvature),
            "independently_solved_increment_current_interaction_action_j":
                float(increment["interaction_action_j"]),
            "predicted_chord_curvature_j":
                float(predicted_curvature),
            "absolute_identity_error_j":
                float(
                    abs(
                        source_curvature
                        - predicted_curvature
                    )
                ),
        },
        "saved_m5d_full_path_reproduction_max_abs_error_j":
            reproduction,
        "max_coupled_solver_residual":
            max_residual,
        "counterfactual_paths_are_physical_motions":
            False,
        "phase_action_is_physical_force":
            False,
        "discrete_current_transport_Ward_certified":
            False,
        "finite_box_artifact_excluded":
            False,
        "exterior_metric_transmission_derived":
            False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }
