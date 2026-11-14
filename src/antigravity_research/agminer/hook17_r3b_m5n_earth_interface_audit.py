"""ALPHA-1R9 / B17-M5N: Earth material-interface derivative audit.

QUESTION
--------
Why do M5M's Earth-only reduced-action derivatives disagree between
0.25 m and 0.20 m grids, despite identical continuum source input?

For fixed source j and prescribed material parameter x, define
    Q(u,x) = 1/2 u^T H(x) u - u^T W j
    H(x) u_*(x) = W j.

The stationary (envelope/Hellmann-Feynman) identity is
    dQ_*/dx = 1/2 u_*^T (dH/dx) u_*.

Evaluate its centered derivative through two independently
constructed material operators, without re-solving at x +/- d.
Compare against M5M's independently re-solved Earth-only derivative.

Spatial row attribution is a diagnostic, not a unique local stress
tensor or a whole-spacecraft force. Prescribed Earth material and
carrier sources remain nondynamical. All source and physical-energy
limitations of M5M remain open.
"""

from __future__ import annotations

import math
import numpy as np

from .hook17_r3b_m5i_continuum_source import SourceSpec
from .hook17_r3b_m5m_translation_consistency import (
    BRANCH as M5M_BRANCH,
    PORTAL_SCALE_EV,
    carrier_action_conversion_j_per_native,
    redeposit_shifted_source,
)
from .hook17_r3b_m5l_variational_audit import (
    assemble_variational_matrix,
)

BRANCH = "032H17A12D1R3X3B17-ALPHA1R9-M5N"


def envelope_rows(u, h_plus, h_minus, step, conversion):
    """Per-degree-of-freedom variation of stationary quadratic Q."""
    u = np.asarray(u, dtype=float)

    if (
        not math.isfinite(step)
        or step <= 0
        or not math.isfinite(conversion)
        or conversion <= 0
    ):
        raise ValueError("Invalid difference step or normalization")

    if (
        h_plus.shape != h_minus.shape
        or h_plus.shape != (len(u), len(u))
        or not np.isfinite(u).all()
    ):
        raise ValueError("Invalid weighted operator dimensions")

    delta = (h_plus - h_minus) @ u

    rows = 0.5 * conversion * u * delta / (2.0 * step)

    if not np.isfinite(rows).all():
        raise ArithmeticError("Nonfinite envelope derivative")

    return rows


def zone_attribution(rows, field, geometry):
    """Disjoint diagnostic partition of the two operator meshes."""
    rhos = np.asarray(field["rhos"], dtype=float)
    zs = np.asarray(field["zs"], dtype=float)
    h = float(field["h"])

    z = zs[1:-1]
    rp = rhos[:-1]
    ra = rhos[1:-1]

    row_r = np.r_[
        np.tile(rp, len(z)),
        np.tile(ra, len(z)),
    ]

    row_z = np.r_[
        np.repeat(z, len(rp)),
        np.repeat(z, len(ra)),
    ]

    rows = np.asarray(rows, dtype=float)

    if len(rows) != len(row_z):
        raise ValueError("Spatial attribution layout mismatch")

    top = float(geometry.ground_top_relative_z_m)
    bottom = top - float(geometry.ground_depth_m)
    radius = float(geometry.ground_radius_m)

    width = max(
        2.0 * h,
        2.0 * float(geometry.interface_width_m),
    )

    remaining = np.ones(len(rows), dtype=bool)

    definitions = (
        ("ground_top_band", np.abs(row_z - top) <= width),
        ("ground_bottom_band", np.abs(row_z - bottom) <= width),
        ("ground_radial_edge_band",
         np.abs(row_r - radius) <= width),
    )

    result = {}
    total_absolute = float(np.sum(np.abs(rows)))

    for name, region in definitions:
        mask = remaining & region
        remaining &= ~mask

        selected = rows[mask]

        result[name] = {
            "signed_derivative_j_per_m": float(selected.sum()),
            "absolute_derivative_sum_j_per_m":
                float(np.abs(selected).sum()),
            "row_count": int(np.count_nonzero(mask)),
        }

    selected = rows[remaining]

    result["other_rows"] = {
        "signed_derivative_j_per_m": float(selected.sum()),
        "absolute_derivative_sum_j_per_m":
            float(np.abs(selected).sum()),
        "row_count": int(np.count_nonzero(remaining)),
    }

    for value in result.values():
        value["fraction_of_absolute_contributions"] = (
            value["absolute_derivative_sum_j_per_m"]
            / max(total_absolute, 1e-300)
        )

    return {
        "bands_m": width,
        "ground_top_relative_z_m": top,
        "ground_bottom_relative_z_m": bottom,
        "ground_radius_m": radius,
        "total_signed_j_per_m": float(rows.sum()),
        "total_absolute_j_per_m": total_absolute,
        "signed_to_absolute_cancellation_ratio":
            abs(float(rows.sum()))
            / max(total_absolute, 1e-300),
        "regions": result,
        "attribution_is_unique_physical_stress": False,
    }


def evaluate_case(h, reverse, historical):
    from .hook17_r3b_m4b1_source_recovery import (
        assemble_original_aligned_source,
    )
    from . import hook17_r3b_m4b_sparse_earth_loading as loading
    from .hook17_r3b_m4b4_paired_translation import (
        MaterialGeometry,
        shifted_material,
    )

    if (
        historical.get("branch") != M5M_BRANCH
        or historical.get("grid_m") != h
        or historical.get("reverse_magnetic") is not reverse
        or not all(historical["diagnostic_gates"].values())
        or h not in (0.25, 0.2)
    ):
        raise ValueError("Incorrect M5M historical control")

    base = assemble_original_aligned_source(h)
    spec = SourceSpec(
        azimuthal_current_amplitude=(-1.0 if reverse else 1.0)
    )

    source, source_audit = redeposit_shifted_source(
        base, spec, 0.0, order=6
    )

    amplifier = (PORTAL_SCALE_EV / 1000.0)**2

    active = {
        **source,
        "j_phi": amplifier * source["j_phi"],
        "j_a": amplifier * source["j_a"],
    }

    field = source["field"]
    operators = source["operators"]
    j = np.r_[active["j_phi"], active["j_a"]]

    conversion = carrier_action_conversion_j_per_native(h)

    def beta(earth_position, earth_present):
        return shifted_material(
            source,
            earth_position,
            0.0,
            PORTAL_SCALE_EV,
            earth_present=earth_present,
        )[0]

    earth_beta = beta(0.0, True)
    air_beta = beta(0.0, False)

    earth_state = loading._solve_fixed_sources(
        active, earth_beta, fraction=1.0
    )

    air_state = loading._solve_fixed_sources(
        active, air_beta, fraction=1.0
    )

    def solution(state):
        return np.r_[
            state["phi"][1:-1, :-1].ravel(),
            state["a"][1:-1, 1:-1].ravel(),
        ]

    earth_u = solution(earth_state)
    air_u = solution(air_state)

    def weighted_matrix(coupling):
        _, matrix, weights, asymmetry = (
            assemble_variational_matrix(
                operators, coupling, field["rhos"], h
            )
        )

        return matrix, weights, float(asymmetry)

    earth_h, weights, asym_e = weighted_matrix(
        earth_state["coupling"]
    )

    air_h, air_weights, asym_a = weighted_matrix(
        air_state["coupling"]
    )

    if not np.array_equal(weights, air_weights):
        raise ArithmeticError("Material-dependent source weights")

    def on_shell_action(u):
        return -0.5 * float(
            np.dot(u, weights * j)
        ) * conversion

    center_action = (
        on_shell_action(earth_u)
        - on_shell_action(air_u)
    )

    historical_center = float(
        historical["center_reduced_carrier_interaction_action_j"]
    )

    center_error = abs(center_action - historical_center)

    if center_error > 1e-5:
        raise ArithmeticError(
            "Failed M5M center-action reproduction"
        )

    def h_for_earth(position):
        b = beta(position, True)

        coupling = loading._build_same_action_coupling(
            field["rhos"], field["zs"], h, b, operators
        )

        matrix, new_weights, asymmetry = weighted_matrix(
            coupling
        )

        if not np.array_equal(weights, new_weights):
            raise ArithmeticError("Weights changed under translation")

        return matrix, b, asymmetry

    geometry = MaterialGeometry()
    steps = {}

    for step in (0.002, 0.001):
        plus_h, plus_beta, plus_asym = h_for_earth(step)
        minus_h, minus_beta, minus_asym = h_for_earth(-step)

        per_row = envelope_rows(
            earth_u, plus_h, minus_h, step, conversion
        )

        predicted = float(per_row.sum())

        archived = float(
            historical["translation_derivatives"][str(step)][
                "earth_only_reduced_action_derivative_j_per_m"
            ]
        )

        delta_beta = (
            plus_beta - minus_beta
        ) / (2.0 * step)

        shifted_air_error = max(
            float(np.max(np.abs(beta(step, False) - air_beta))),
            float(np.max(np.abs(beta(-step, False) - air_beta))),
        )

        steps[str(step)] = {
            "envelope_derivative_j_per_m": predicted,
            "M5M_resolved_Earth_derivative_j_per_m": archived,
            "envelope_minus_resolved_j_per_m":
                predicted - archived,
            "envelope_absolute_disagreement_j_per_m":
                abs(predicted - archived),
            "material_beta_derivative_max_abs":
                float(np.max(np.abs(delta_beta))),
            "material_beta_derivative_rms":
                float(np.sqrt(np.mean(delta_beta**2))),
            "Earth_free_beta_change_max_abs":
                shifted_air_error,
            "max_shifted_weighted_asymmetry":
                max(plus_asym, minus_asym),
            "spatial_attribution":
                zone_attribution(per_row, field, geometry),
        }

    envelope_step_difference = abs(
        steps["0.002"]["envelope_derivative_j_per_m"]
        - steps["0.001"]["envelope_derivative_j_per_m"]
    )

    resolved_error = max(
        row["envelope_absolute_disagreement_j_per_m"]
        for row in steps.values()
    )

    air_change = max(
        row["Earth_free_beta_change_max_abs"]
        for row in steps.values()
    )

    total_asym = max(
        asym_e,
        asym_a,
        *(
            row["max_shifted_weighted_asymmetry"]
            for row in steps.values()
        ),
    )

    return {
        "branch": BRANCH,
        "grid_m": h,
        "reverse_magnetic": reverse,
        "scope": "PRESCRIBED_MATERIAL_ENVELOPE_DERIVATIVE",
        "center_action_j": center_action,
        "M5M_center_action_reproduction_error_j": center_error,
        "source_audit_at_zero_translation": source_audit,
        "source_is_redeposited_during_Earth_only_shift": False,
        "envelope_variation": steps,
        "envelope_step_difference_j_per_m":
            envelope_step_difference,
        "maximum_envelope_vs_M5M_disagreement_j_per_m":
            resolved_error,
        "diagnostic_gates": {
            "center_action_reproduced_below_1e_minus_5_j":
                bool(center_error < 1e-5),
            "Earth_free_material_independent_of_Earth_shift":
                bool(air_change < 1e-12),
            "all_weighted_matrices_symmetric_below_1e_minus_9":
                bool(total_asym < 1e-9),
            "envelope_matches_M5M_within_0p1_j_per_m":
                bool(resolved_error < 0.1),
        },
        "crossgrid_continuum_force_converged": False,
        "prescribed_Earth_matter_action_is_dynamical": False,
        "local_attribution_is_physical_stress": False,
        "source_dynamical_Ward_certified": False,
        "exterior_metric_transmission_derived": False,
        "Earth_environment_reaction_derived": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }
