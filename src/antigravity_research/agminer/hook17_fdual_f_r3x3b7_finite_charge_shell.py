"""R3X3B7: finite-thickness electric source inside the 2 m source radius.

Preserve every R3B exterior electric multipole exactly while replacing
the ideal surface-charge sheet with a finite-width charge distribution.

For each ell >= 1, the radial potential is regular and harmonic inside
R-width, cubic Hermite within the shell, and the original decaying
harmonic for r >= R.

The potential and first radial derivative are continuous at both shell
interfaces. Thus no delta-function charge sheet is required.

For fixed boundary potential, the original harmonic interior minimizes
the canonical electric energy. A finite shell has a positive energy cost.

This is a field-level result. It is NOT:
- a microscopic charged-matter source realization;
- a self-consistent loaded finite-payload solution;
- complete operating energy;
- or a working antigravity model.
"""
from __future__ import annotations

import math

import numpy as np

from .hook17_concurrent_u1_fieldstrength_metric import (
    EV_J,
    HBAR_C_EV_M,
    SOURCE_RADIUS_M,
)


def _validate(ell, radius, width):
    if type(ell) is not int or ell < 1:
        raise ValueError("Multipoles must begin at ell=1")

    if not math.isfinite(radius) or radius <= 0:
        raise ValueError("Invalid source radius")

    if not math.isfinite(width) or not 0 < width < radius:
        raise ValueError("Invalid source layer width")


def radial_profile(ell, amplitude, radius, width, radii):
    """Return f(r), f'(r), f''(r) multiplying P_ell(cos theta)."""
    _validate(ell, radius, width)

    r = np.asarray(radii, dtype=float)

    if not np.isfinite(r).all() or np.any(r < 0):
        raise ValueError("Invalid radial coordinates")

    c = -float(amplitude) / math.sqrt(2.0)
    start = radius - width

    f = np.empty_like(r)
    fp = np.empty_like(r)
    fpp = np.empty_like(r)

    core = r < start
    shell = (r >= start) & (r <= radius)
    exterior = r > radius

    ri = r[core]
    q = ri / radius

    f[core] = c * q**ell
    fp[core] = c * ell / radius * q**(ell - 1)

    if ell == 1:
        fpp[core] = 0.0
    else:
        fpp[core] = (
            c * ell * (ell - 1)
            / radius**2
            * q**(ell - 2)
        )

    rs = r[shell]
    t = (rs - start) / width

    v0 = c * (start / radius)**ell
    d0 = c * ell / radius * (start / radius)**(ell - 1)

    v1 = c
    d1 = -c * (ell + 1) / radius

    f[shell] = (
        (2*t**3 - 3*t**2 + 1) * v0
        + (t**3 - 2*t**2 + t) * width * d0
        + (-2*t**3 + 3*t**2) * v1
        + (t**3 - t**2) * width * d1
    )

    fp[shell] = (
        (6*t**2 - 6*t) / width * v0
        + (3*t**2 - 4*t + 1) * d0
        + (-6*t**2 + 6*t) / width * v1
        + (3*t**2 - 2*t) * d1
    )

    fpp[shell] = (
        (12*t - 6) / width**2 * v0
        + (6*t - 4) / width * d0
        + (-12*t + 6) / width**2 * v1
        + (6*t - 2) / width * d1
    )

    ro = r[exterior]

    f[exterior] = (
        c * (radius / ro)**(ell + 1)
    )

    fp[exterior] = (
        -(ell + 1) * f[exterior] / ro
    )

    fpp[exterior] = (
        (ell + 1) * (ell + 2)
        * f[exterior] / ro**2
    )

    return f, fp, fpp


def source_density_proxy(ell, amplitude, radius, width, radii):
    """Radial coefficient of -Laplacian(phi), not SI charge density."""
    r = np.asarray(radii, dtype=float)

    if np.any(r <= 0):
        raise ValueError("Positive radii required")

    f, fp, fpp = radial_profile(
        ell, amplitude, radius, width, r
    )

    return -(
        fpp
        + 2.0 * fp / r
        - ell * (ell + 1) * f / r**2
    )


def shell_energy_penalty(amplitudes, radius, width, order=128):
    """Compute exact spherical-harmonic energy penalty by quadrature."""
    _validate(1, radius, width)

    amplitudes = np.asarray(amplitudes, dtype=float)

    if not amplitudes.size or not np.isfinite(amplitudes).all():
        raise ValueError("Invalid multipole amplitudes")

    x, weights = np.polynomial.legendre.leggauss(order)

    r = radius - width / 2.0 + width * x / 2.0

    conversion = EV_J / HBAR_C_EV_M

    direct_total = 0.0
    positive_total = 0.0

    for ell, amplitude in enumerate(amplitudes, start=1):
        f, fp, _ = radial_profile(
            ell, amplitude, radius, width, r
        )

        c = -float(amplitude) / math.sqrt(2.0)

        f0 = c * (r / radius)**ell
        fp0 = (
            c * ell / radius
            * (r / radius)**(ell - 1)
        )

        coefficient = (
            2.0 * math.pi
            / (2 * ell + 1)
            * conversion
            * width / 2.0
        )

        direct = coefficient * float(np.dot(
            weights,
            r**2 * (fp**2 - fp0**2)
            + ell * (ell + 1) * (f**2 - f0**2),
        ))

        positive = coefficient * float(np.dot(
            weights,
            r**2 * (fp - fp0)**2
            + ell * (ell + 1) * (f - f0)**2,
        ))

        if abs(direct - positive) > max(
            1e-12, 1e-8 * abs(positive)
        ):
            raise AssertionError("Dirichlet identity failed")

        direct_total += direct
        positive_total += positive

    return {
        "layer_width_m": float(width),
        "extra_electric_field_energy_j_before_1g_normalization":
            float(positive_total),
        "dirichlet_identity_relative_error":
            abs(direct_total - positive_total)
            / max(positive_total, 1e-300),
        "exterior_field_unchanged_analytically": True,
        "charge_supported_inside_source": True,
        "net_electric_monopole": 0,
        "microscopic_source_realized": False,
    }


def evaluate_r3b_grid(h, widths=(0.05, 0.10, 0.20)):
    """Use the original R3B field, fit, and payload normalization."""
    from .hook17_fdual_f_global_mirror_prefight import (
        reconstruct_a12c_field,
        fit_exterior_multipoles,
        mirror_global_energy_gate,
        mirror_payload_reconstruction,
        PRIMARY_FIT_RADIUS_M,
        PRIMARY_LMAX,
    )

    field = reconstruct_a12c_field(float(h))

    fit = fit_exterior_multipoles(
        field,
        PRIMARY_FIT_RADIUS_M,
        PRIMARY_LMAX,
    )

    energy = mirror_global_energy_gate(field, fit)

    payload = mirror_payload_reconstruction(
        field, fit, energy
    )

    original = payload[
        "normalized_mixed_global_field_energy_j"
    ]

    normalization = payload[
        "amplitude_squared_normalization_to_1g"
    ]

    if original is None or normalization is None:
        raise RuntimeError("Original R3B preloaded response failed")

    shells = []

    for width in widths:
        row = shell_energy_penalty(
            fit["boundary_amplitudes"],
            SOURCE_RADIUS_M,
            float(width),
        )

        penalty = (
            row[
                "extra_electric_field_energy_j_before_1g_normalization"
            ] * normalization
        )

        row["extra_electric_field_energy_j_normalized"] = penalty
        row["mixed_field_energy_j_normalized"] = original + penalty

        shells.append(row)

    return {
        "h_m": float(h),
        "original_preloaded_field_energy_j": float(original),
        "source_radius_m": float(SOURCE_RADIUS_M),
        "shells": shells,
        "original_exterior_1g_response_preserved": True,
        "fully_loaded_payload_certified": False,
        "complete_energy_certified": False,
    }
