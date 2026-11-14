"""B17-M4B3A: exact B7 radial moment and source-resolution preflight.

For each electric multipole ell >= 1, the B7 radial potential
f(r) is regular inside R-width, cubic Hermite within the shell,
and the original exterior harmonic outside R.

The radial source coefficient is

    q_ell = -(f'' + 2f'/r - ell(ell+1)f/r^2).

The exterior multipole moment is

    M_ell = integral_0^R q_ell(r) r^(ell+2) dr.

Exact B7 matching requires

    M_ell = (2ell+1)*c*R^(ell+1),

where c = -amplitude/sqrt(2).

Compare the analytic boundary identity, direct quadrature,
naive midpoint sampling and cell-integrated conservative
radial source representation.

This test DOES NOT solve the coupled Earth-loading BVP.
Moment matching does not establish local source resolution,
microscopic source hardware, spacecraft lift or complete energy.
"""

from __future__ import annotations

import math
import numpy as np
from numpy.polynomial.legendre import leggauss

from .hook17_fdual_f_r3x3b7_finite_charge_shell import (
    radial_profile,
    source_density_proxy,
)

BRANCH = "032H17A12D1R3X3B17-M4B3A"

DEFAULT_GRIDS = (
    0.30, 0.25, 0.20, 0.10,
    0.05, 0.025, 0.02, 0.01,
)

DEFAULT_PHASES = tuple(np.arange(8, dtype=float) / 8)


def _validate(ell, amplitude, radius, width):
    if (
        type(ell) is not int
        or ell < 1
        or not math.isfinite(float(amplitude))
        or amplitude == 0
    ):
        raise ValueError("Invalid multipole or amplitude")

    if not (
        0 < width < radius
        and math.isfinite(width)
        and math.isfinite(radius)
    ):
        raise ValueError("Require 0 < width < radius")


def expected_moment(ell, amplitude=1.0, radius=2.0):
    """Independent exterior matching formula."""
    c = -float(amplitude) / math.sqrt(2.0)
    return (2 * ell + 1) * c * radius ** (ell + 1)


def boundary_moment(
    ell, amplitude=1.0, radius=2.0, width=0.1,
):
    """Integrate the source using endpoint potential data."""
    _validate(ell, amplitude, radius, width)

    r = np.array([radius - width, radius], dtype=float)

    f, fp, _ = radial_profile(
        ell, amplitude, radius, width, r
    )

    boundary = (
        -(r ** (ell + 2)) * fp
        + ell * r ** (ell + 1) * f
    )

    return float(boundary[1] - boundary[0])


def _integral_on_interval(
    ell, amplitude, radius, width,
    a, b, nodes, weights,
):
    if b <= a:
        return 0.0

    r = (a + b) / 2 + (b - a) / 2 * nodes

    q = source_density_proxy(
        ell, amplitude, radius, width, r
    )

    return float(
        (b - a) / 2
        * np.dot(weights, q * r ** (ell + 2))
    )


def exact_shell_quadrature(
    ell, amplitude=1.0, radius=2.0,
    width=0.1, order=32,
):
    _validate(ell, amplitude, radius, width)

    nodes, weights = leggauss(order)

    return _integral_on_interval(
        ell, amplitude, radius, width,
        radius - width, radius,
        nodes, weights,
    )


def split_cell_moment(
    ell, h, phase=0.0, amplitude=1.0,
    radius=2.0, width=0.1, order=24,
):
    """Conservative radial-cell integration split at shell edges."""
    _validate(ell, amplitude, radius, width)

    if (
        not math.isfinite(h)
        or h <= 0
        or not math.isfinite(phase)
        or not 0 <= phase < 1
    ):
        raise ValueError("Invalid grid or phase")

    nodes, weights = leggauss(order)

    origin = phase * h
    start = radius - width

    first = math.floor((start - origin) / h) - 1
    last = math.ceil((radius - origin) / h) + 1

    moment = 0.0
    cell_count = 0

    for k in range(first, last + 1):
        a = max(start, origin + k * h)
        b = min(radius, origin + (k + 1) * h)

        if b > a + 1e-14:
            moment += _integral_on_interval(
                ell, amplitude, radius, width,
                a, b, nodes, weights,
            )
            cell_count += 1

    return moment, cell_count


def midpoint_moment(
    ell, h, phase=0.0, amplitude=1.0,
    radius=2.0, width=0.1,
):
    """Deliberately naive, nonconservative source sampling."""
    _validate(ell, amplitude, radius, width)

    if (
        not math.isfinite(h)
        or h <= 0
        or not math.isfinite(phase)
        or not 0 <= phase < 1
    ):
        raise ValueError("Invalid grid or phase")

    n = math.ceil((radius + 2*h) / h)

    r = (
        np.arange(n, dtype=float)
        + 0.5
        + phase
    ) * h

    q = source_density_proxy(
        ell, amplitude, radius, width, r
    )

    return float(
        h * np.dot(q, r ** (ell + 2))
    )


def evaluate(
    grids=DEFAULT_GRIDS,
    multipoles=(1, 3, 12),
    phases=DEFAULT_PHASES,
    radius=2.0,
    width=0.10,
):
    if not grids or not multipoles or not phases:
        raise ValueError("Empty resolution scan")

    rows = []

    for ell in multipoles:
        expected = expected_moment(
            ell, 1.0, radius
        )

        boundary = boundary_moment(
            ell, 1.0, radius, width
        )

        quadrature = exact_shell_quadrature(
            ell, 1.0, radius, width
        )

        for h in grids:
            phase_rows = []

            for phase in phases:
                midpoint = midpoint_moment(
                    ell, float(h), float(phase),
                    1.0, radius, width,
                )

                split, count = split_cell_moment(
                    ell, float(h), float(phase),
                    1.0, radius, width,
                )

                phase_rows.append({
                    "phase": float(phase),
                    "midpoint_exterior_moment_ratio":
                        midpoint / expected,
                    "split_cell_exterior_moment_ratio":
                        split / expected,
                    "intersected_radial_cells": count,
                })

            midpoint_errors = [
                abs(p["midpoint_exterior_moment_ratio"] - 1)
                for p in phase_rows
            ]

            split_errors = [
                abs(p["split_cell_exterior_moment_ratio"] - 1)
                for p in phase_rows
            ]

            rows.append({
                "ell": ell,
                "grid_m": float(h),
                "shell_width_in_grid_cells": width / h,
                "expected_analytic_exterior_moment":
                    expected,
                "boundary_to_exact_moment_ratio":
                    boundary / expected,
                "quadrature_to_exact_moment_ratio":
                    quadrature / expected,
                "midpoint_max_phase_relative_error":
                    max(midpoint_errors),
                "split_cell_max_phase_relative_error":
                    max(split_errors),
                "phases": phase_rows,
                "source_local_profile_converged": False,
            })

    return {
        "branch": BRANCH,
        "classification":
            "B7_ANALYTIC_RADIAL_SOURCE_MOMENT_AND_SAMPLING_PREFLIGHT",
        "source_radius_m": radius,
        "finite_charge_shell_width_m": width,
        "rows": rows,
        "full_3d_loaded_earth_solver": False,
        "b7_microscopic_source_realized": False,
        "exact_R3B_global_fields_loaded": False,
        "source_local_profile_convergence_certified": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
        "warning":
            "Moment preservation is necessary, "
            "not local resolution or spacecraft lift",
    }
