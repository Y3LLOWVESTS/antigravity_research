"""B17-M4B2: Earth translation in the reduced static carrier action.

Scientific question
-------------------
Does the old Earth tracer-force integral agree with an independently
derived, on-shell variation of the carrier action when the finite
Earth target translates relative to the onboard source?

The source is the M4B1 approximate R3B-aligned control. It is NOT
the exact original R3B or B7 finite-width source.

For fixed material density, the corrected Lorentzian block operator
has a symmetric weighted action Hessian:

    [ Wp Kp,  Wp C  ]
    [ Wa D, -Wa Ka ]

with Wa D = C.T Wp.

At a stationary solution with fixed onboard currents:

    S_on = N * (-phi.T Wp jphi + a.T Wa ja) / 2

where N = 2*pi*h*h*EV_J/HBAR_C_EV_M.

For an infinitesimal displacement of the ground material:

    dS_on/dz = N * phi.T Wp (dC/dz) a.

Both derivatives are evaluated independently.

The ground movement also displaces air when atmosphere is enabled.
The carrier action is not a complete Earth/craft/gravity action.
Its derivative has force units but is NOT certified spacecraft thrust.

No historical sources, tests or results are modified.
"""

from __future__ import annotations

from dataclasses import replace
import math

import numpy as np
from scipy.sparse import diags

from .hook17_concurrent_u1_fieldstrength_metric import (
    EV_J,
    HBAR_C_EV_M,
)
from .hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)
from .hook17_fdual_f_loaded_payload_homotopy import (
    _build_same_action_coupling,
)
from .hook17_r3b_m4b_sparse_earth_loading import (
    MaterialGeometry,
    material_density,
    _solve_fixed_sources,
)
from .hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
    _metric_sigma,
    _ground_tracer_force,
)

BRANCH = "032H17A12D1R3X3B17-M4B2"


def _weights(source):
    field = source["field"]
    h = field["h"]
    ops = source["operators"]
    nz = ops["nz_inner"]

    wp = np.tile(
        np.r_[h / 8.0, field["rhos"][1:-1]],
        nz,
    )
    wa = np.tile(field["rhos"][1:-1], nz)

    normalization = (
        2 * math.pi * h * h * EV_J / HBAR_C_EV_M
    )

    assert len(wp) == len(source["j_phi"])
    assert len(wa) == len(source["j_a"])

    return wp, wa, normalization


def _beta(source, geometry, scale, include_air):
    density, fraction = material_density(
        source["field"],
        geometry,
        include_air,
        True,
    )

    beta = 1.0 - loading_coefficient_z(
        density, scale
    )

    return beta, density, fraction


def _source_at_scale(source, scale):
    amplitude = (scale / 1000.0)**2
    return {
        **source,
        "j_phi": source["j_phi"] * amplitude,
        "j_a": source["j_a"] * amplitude,
    }


def _on_shell_action(state, source, weights):
    wp, wa, normalization = weights

    phi = state["phi"][1:-1, :-1].ravel()
    a = state["a"][1:-1, 1:-1].ravel()

    return float(
        normalization * (
            -0.5 * np.dot(wp * phi, source["j_phi"])
            +0.5 * np.dot(wa * a, source["j_a"])
        )
    )


def _full_reduced_action(state, source, beta, weights):
    """Independent full quadratic source-fixed static action."""
    wp, wa, normalization = weights
    field = source["field"]
    ops = source["operators"]

    coupling = _build_same_action_coupling(
        field["rhos"],
        field["zs"],
        field["h"],
        beta,
        ops,
    )["c"]

    phi = state["phi"][1:-1, :-1].ravel()
    a = state["a"][1:-1, 1:-1].ravel()

    return float(
        normalization * (
            0.5 * np.dot(wp * phi, ops["k_phi"] @ phi)
            -0.5 * np.dot(wa * a, ops["k_a"] @ a)
            +np.dot(wp * phi, coupling @ a)
            -np.dot(wp * phi, source["j_phi"])
            +np.dot(wa * a, source["j_a"])
        )
    )


def _fixed_field_derivative(
    state, source, geometry_plus, geometry_minus,
    scale, include_air, step, weights,
):
    """Envelope-theorem derivative holding the central fields fixed."""
    wp, _, normalization = weights
    field = source["field"]
    ops = source["operators"]

    beta_plus, _, _ = _beta(
        source, geometry_plus, scale, include_air
    )
    beta_minus, _, _ = _beta(
        source, geometry_minus, scale, include_air
    )

    c_plus = _build_same_action_coupling(
        field["rhos"], field["zs"],
        field["h"], beta_plus, ops,
    )["c"]

    c_minus = _build_same_action_coupling(
        field["rhos"], field["zs"],
        field["h"], beta_minus, ops,
    )["c"]

    phi = state["phi"][1:-1, :-1].ravel()
    a = state["a"][1:-1, 1:-1].ravel()

    return float(
        normalization
        * np.dot(wp * phi, (c_plus - c_minus) @ a)
        / (2.0 * step)
    )


def _matrix_symmetry(source, beta):
    """Audit diagonal weighted symmetry and cross-carrier reciprocity."""
    field = source["field"]
    ops = source["operators"]
    wp, wa, _ = _weights(source)

    coupling = _build_same_action_coupling(
        field["rhos"],
        field["zs"],
        field["h"],
        beta,
        ops,
    )

    phi_matrix = diags(wp) @ ops["k_phi"]
    a_matrix = diags(wa) @ ops["k_a"]
    cross = diags(wp) @ coupling["c"]

    difference = (
        cross - (diags(wa) @ coupling["d"]).T
    ).tocsr()

    scale = max(
        float(np.max(np.abs(cross.data)))
        if cross.nnz else 0.0,
        1.0,
    )

    def antisymmetry(matrix):
        residual = (matrix - matrix.T).tocsr()
        return (
            float(np.max(np.abs(residual.data)))
            if residual.nnz else 0.0
        )

    return {
        "phi_weighted_antisymmetry_max":
            antisymmetry(phi_matrix),
        "a_weighted_antisymmetry_max":
            antisymmetry(a_matrix),
        "relative_weighted_cross_antisymmetry":
            (
                float(np.max(np.abs(difference.data))) / scale
                if difference.nnz else 0.0
            ),
    }


def evaluate(
    h=0.25,
    scale_ev=1000.0,
    include_air=True,
    steps=(1e-5, 1e-6, 1e-7),
    interface_width_m=0.25,
):
    """Re-solve fields under Earth translations; audit the action.

    The onboard currents remain identical across all translations.
    No spacecraft or metric momentum equation is solved here.
    """
    if not np.isfinite(scale_ev) or scale_ev <= 0:
        raise ValueError("Invalid portal scale")

    if (
        not np.isfinite(interface_width_m)
        or interface_width_m <= 0
    ):
        raise ValueError("Invalid interface width")

    source = assemble_original_aligned_source(float(h))
    base = _source_at_scale(source, scale_ev)
    weights = _weights(source)

    geometry = MaterialGeometry(
        interface_width_m=float(interface_width_m)
    )

    beta, _, ground_fraction = _beta(
        source, geometry, scale_ev, include_air
    )

    middle = _solve_fixed_sources(base, beta, 1.0)

    reduced_action = _on_shell_action(
        middle, base, weights
    )
    full_action = _full_reduced_action(
        middle, base, beta, weights
    )

    ground_density = (
        geometry.ground_density_kg_m3 * ground_fraction
    )

    tracer = _ground_tracer_force(
        _metric_sigma(middle["em"], scale_ev),
        source["field"],
        ground_density,
    )

    scan = []

    for step in steps:
        if (
            not np.isfinite(step)
            or not 0 < step < interface_width_m / 2
        ):
            raise ValueError("Invalid translation step")

        plus_geometry = replace(
            geometry,
            ground_top_relative_z_m=(
                geometry.ground_top_relative_z_m + step
            ),
        )
        minus_geometry = replace(
            geometry,
            ground_top_relative_z_m=(
                geometry.ground_top_relative_z_m - step
            ),
        )

        plus_beta, _, _ = _beta(
            source, plus_geometry, scale_ev, include_air
        )
        minus_beta, _, _ = _beta(
            source, minus_geometry, scale_ev, include_air
        )

        plus_state = _solve_fixed_sources(
            base, plus_beta, 1.0
        )
        minus_state = _solve_fixed_sources(
            base, minus_beta, 1.0
        )

        on_shell_slope = (
            _on_shell_action(plus_state, base, weights)
            - _on_shell_action(minus_state, base, weights)
        ) / (2.0 * step)

        envelope_slope = _fixed_field_derivative(
            middle,
            source,
            plus_geometry,
            minus_geometry,
            scale_ev,
            include_air,
            step,
            weights,
        )

        relative_error = (
            abs(on_shell_slope - envelope_slope)
            / max(
                abs(on_shell_slope),
                abs(envelope_slope),
                1e-12,
            )
        )

        scan.append({
            "step_m": float(step),
            "on_shell_action_slope_j_per_m":
                float(on_shell_slope),
            "frozen_field_envelope_slope_j_per_m":
                float(envelope_slope),
            "relative_derivative_identity_error":
                float(relative_error),
            "max_shifted_solver_residual": max(
                plus_state["residual"],
                minus_state["residual"],
            ),
        })

    return {
        "branch": BRANCH,
        "classification":
            "SOURCE_FIXED_REDUCED_ACTION_EARTH_TRANSLATION_AUDIT",
        "h_m": float(h),
        "scale_ev": float(scale_ev),
        "include_air": bool(include_air),
        "interface_width_m": float(interface_width_m),
        "ground_translation_displaces_air": bool(include_air),
        "source_unloaded_energy_j":
            source["recovered_unloaded_energy_j"],
        "original_r3b_unloaded_j": 1.5429162116460216,
        "approximate_source_is_exact_r3b": False,
        "original_b7_10cm_layer_cells": 0.10 / h,
        "b7_layer_resolved": h <= 0.10 / 3.0,
        "central_on_shell_action_j": reduced_action,
        "central_full_quadratic_action_j": full_action,
        "stationary_action_identity_error_j":
            abs(reduced_action - full_action),
        "central_canonical_carrier_j":
            middle["carrier_energy_j"],
        "central_legacy_ground_tracer_n": tracer,
        "central_solver_residual": middle["residual"],
        "weighted_symmetry": _matrix_symmetry(source, beta),
        "translation_scan": scan,
        "sign_as_physical_force_certified": False,
        "whole_craft_force_n": None,
        "source_hardware_reaction_n": None,
        "earth_gravity_metric_momentum_ledger_closed": False,
        "interface_and_box_convergence_certified": False,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
        "warning":
            "Carrier-action derivative only, not actual Earth/craft thrust",
    }
