"""B17-M4B3C: B7/R3B multipole transfer and parity diagnostic.

For each pure analytic B7 electric multipole ell, deposit charge
onto the axisymmetric R3X1 scalar grid and measure all output
multipoles k. The transfer matrix T[k,ell] equals the identity
for exact multipole-preserving deposition.

The original fitted R3B multipoles are recovered from the analytic
moment values in the completed M4B3B JSON.

Source-axis alignment is varied independently to expose artificial
odd/even parity mixing.

This is a SOURCE-ONLY numerical audit. It does not solve loaded
Earth response, source hardware, whole-craft force or complete energy.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from .hook17_r3b_m4b3b_cylindrical_source import (
    deposit_b7_to_axisymmetric_nodes,
)
from .hook17_fdual_f_loaded_payload_homotopy import (
    PRODUCTION_RHO_MAX_M,
    PRODUCTION_Z_MIN_M,
    PRODUCTION_Z_MAX_M,
)

BRANCH = "032H17A12D1R3X3B17-M4B3C"
RADIUS_M = 2.0


def _moment_scale(ell):
    return (
        4.0 * math.pi
        * RADIUS_M ** (ell + 1)
        / math.sqrt(2.0)
    )


def _axes(h):
    return (
        np.arange(
            PRODUCTION_Z_MIN_M,
            PRODUCTION_Z_MAX_M + 0.5*h,
            h,
        ),
        np.arange(
            0.0,
            PRODUCTION_RHO_MAX_M + 0.5*h,
            h,
        ),
    )


def _deposited_amplitudes(deposition, scales):
    return np.array([
        -row["deposited_volume_multipole"] / s
        for row, s in zip(
            deposition["moment_rows"], scales
        )
    ], dtype=float)


def evaluate(
    original_json,
    align_source_axis=False,
    radial_order=48,
    angular_order=96,
):
    """Audit all twelve R3B/B7 source multipoles independently.

    The result is not an Earth-loaded field solution or a
    spacecraft-force computation.
    """
    original_json = Path(original_json)

    saved = json.loads(
        original_json.read_text(encoding="utf-8")
    )

    if saved.get("branch") != (
        "032H17A12D1R3X3B17-M4B3B"
    ):
        raise ValueError(
            "Expected an M4B3B source-audit JSON"
        )

    h = float(saved["h_m"])

    if h not in (0.3, 0.25, 0.2):
        raise ValueError("Unexpected preflight grid")

    previous = saved["source"]["moment_rows"]
    n = len(previous)

    if (
        n != 12
        or [r["ell"] for r in previous]
        != list(range(1, 13))
    ):
        raise ValueError(
            "Expected twelve consecutive multipoles"
        )

    scales = np.array([
        _moment_scale(ell)
        for ell in range(1, n+1)
    ])

    amplitudes = np.array([
        -row["analytic_volume_multipole"] / scale
        for row, scale in zip(
            previous, scales
        )
    ])

    amplitude_scale = float(
        np.max(np.abs(amplitudes))
    )

    if (
        amplitude_scale <= 0
        or not np.isfinite(amplitudes).all()
    ):
        raise ValueError("Invalid source amplitudes")

    zs, rhos = _axes(h)

    nearest_z = float(
        zs[np.argmin(np.abs(zs))]
    )

    shift = (
        -nearest_z
        if align_source_axis
        else 0.0
    )

    zs = zs + shift

    columns = []
    max_outside = 0
    max_neutrality = 0.0

    for ell in range(n):
        basis = np.zeros(n)
        basis[ell] = 1.0

        result = deposit_b7_to_axisymmetric_nodes(
            zs,
            rhos,
            h,
            basis,
            source_radius_m=RADIUS_M,
            shell_width_m=0.10,
            radial_order=radial_order,
            angular_order=angular_order,
        )

        columns.append(
            _deposited_amplitudes(
                result, scales
            )
        )

        max_outside = max(
            max_outside,
            result["source_outside_support_count"],
        )

        max_neutrality = max(
            max_neutrality,
            result["net_charge_relative_residual"],
        )

    transfer = np.column_stack(columns)

    combined = deposit_b7_to_axisymmetric_nodes(
        zs,
        rhos,
        h,
        amplitudes,
        source_radius_m=RADIUS_M,
        shell_width_m=0.10,
        radial_order=radial_order,
        angular_order=angular_order,
    )

    measured = _deposited_amplitudes(
        combined, scales
    )

    predicted = transfer @ amplitudes

    linearity_error = float(
        np.max(np.abs(measured - predicted))
        / amplitude_scale
    )

    previous_measured = np.array([
        -row["deposited_volume_multipole"] / s
        for row, s in zip(
            previous, scales
        )
    ])

    reproduction_error = (
        float(
            np.max(
                np.abs(measured - previous_measured)
            ) / amplitude_scale
        )
        if not align_source_axis
        else None
    )

    # Keep only odd-ell source amplitudes.
    # Any even-ell output then measures parity leakage.
    odd_source = np.zeros(n)
    odd_source[::2] = amplitudes[::2]

    parity_output = transfer @ odd_source

    odd_to_even = float(
        np.max(np.abs(parity_output[1::2]))
        / amplitude_scale
    )

    errors = (
        np.abs(measured - amplitudes)
        / amplitude_scale
    )

    return {
        "branch": BRANCH,
        "classification":
            "B7_R3B_2D_MULTIPOLE_TRANSFER_PARITY_DIAGNOSTIC",
        "input_m4b3b_json": original_json.name,
        "grid_m": h,
        "axis_aligned": bool(align_source_axis),
        "original_nearest_source_z_m": nearest_z,
        "applied_grid_shift_m": float(shift),
        "max_input_amplitude": amplitude_scale,
        "normalized_mixed_max_mode_error":
            float(np.max(errors)),
        "normalized_mixed_max_odd_mode_error":
            float(np.max(errors[::2])),
        "normalized_mixed_max_even_mode_error":
            float(np.max(errors[1::2])),
        "normalized_odd_input_to_even_output_leakage":
            odd_to_even,
        "transfer_matrix": transfer.tolist(),
        "transfer_diagonal":
            np.diag(transfer).tolist(),
        "original_analytic_amplitudes":
            amplitudes.tolist(),
        "deposited_equivalent_amplitudes":
            measured.tolist(),
        "per_mode_error_normalized_to_max_amplitude":
            errors.tolist(),
        "linear_superposition_relative_error":
            linearity_error,
        "unshifted_original_json_reproduction_error":
            reproduction_error,
        "max_pure_source_charge_neutrality":
            max_neutrality,
        "mixed_source_charge_neutrality":
            combined["net_charge_relative_residual"],
        "max_source_outside_support_count":
            max(
                max_outside,
                combined[
                    "source_outside_support_count"
                ],
            ),
        "original_unloaded_r3b_field_capacity_j":
            1.5429162116460216,
        "original_unloaded_b7_field_capacity_j":
            1.5473042949759672,
        "original_r3b_source_exactly_realized": False,
        "loaded_earth_solver_executed": False,
        "exterior_field_convergence_certified": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
        "warning":
            "Source-deposition transfer only; "
            "not propulsion or lift",
    }
