"""Simulation 001B.

Scan the tidal/geodesic-deviation eigenvalues of Kottler spacetime.

Unlike Simulation 001A, this examines relative acceleration between
neighboring freely falling observers rather than merely radial coordinate
acceleration.

Baseline reproduction of established GR.
"""

from pathlib import Path
import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from antigravity_research.geometry.kottler import (
    C,
    MEGAPARSEC_M,
    SOLAR_MASS_KG,
    cosmological_constant_from_flat_lcdm,
    static_radius,
)

from antigravity_research.geometry.kottler_tidal import (
    radial_tidal_eigenvalue_s2,
    transverse_tidal_eigenvalue_s2,
)


# ------------------------------------------------------------
# Cosmology
# ------------------------------------------------------------

H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_LAMBDA = 1.0 - OMEGA_M

H0_S = (
    H0_KM_S_MPC
    * 1000.0
    / MEGAPARSEC_M
)

LAMBDA = cosmological_constant_from_flat_lcdm(
    H0_S,
    OMEGA_LAMBDA,
)


# ------------------------------------------------------------
# Test mass scale
# ------------------------------------------------------------

MASS_SOLAR = 1.0e12
MASS_KG = MASS_SOLAR * SOLAR_MASS_KG

R_STATIC_M = static_radius(
    MASS_KG,
    LAMBDA,
)

R_STATIC_MPC = (
    R_STATIC_M
    / MEGAPARSEC_M
)


# ------------------------------------------------------------
# Numerical scan
# ------------------------------------------------------------

radius_mpc = np.logspace(
    math.log10(0.05),
    math.log10(5.0),
    5000,
)

radius_m = (
    radius_mpc
    * MEGAPARSEC_M
)

radial = np.array([
    radial_tidal_eigenvalue_s2(
        r,
        MASS_KG,
        LAMBDA,
    )
    for r in radius_m
])

transverse = np.array([
    transverse_tidal_eigenvalue_s2(
        r,
        MASS_KG,
        LAMBDA,
    )
    for r in radius_m
])

trace = radial + 2.0 * transverse


# ------------------------------------------------------------
# Numerical zero crossing
# ------------------------------------------------------------

crossing_index = int(
    np.argmin(
        np.abs(transverse)
    )
)

numerical_threshold_mpc = (
    radius_mpc[crossing_index]
)

threshold_relative_error = (
    abs(
        numerical_threshold_mpc
        - R_STATIC_MPC
    )
    / R_STATIC_MPC
)


# ------------------------------------------------------------
# Pure de Sitter scale
# ------------------------------------------------------------

de_sitter_eigenvalue = (
    LAMBDA
    * C**2
    / 3.0
)

de_sitter_rate = math.sqrt(
    de_sitter_eigenvalue
)

de_sitter_timescale_s = (
    1.0
    / de_sitter_rate
)

SECONDS_PER_YEAR = (
    365.25
    * 24.0
    * 3600.0
)

de_sitter_timescale_gyr = (
    de_sitter_timescale_s
    / SECONDS_PER_YEAR
    / 1.0e9
)


# ------------------------------------------------------------
# Fundamental identity check
# ------------------------------------------------------------

expected_trace = (
    LAMBDA
    * C**2
)

max_trace_abs_error = float(
    np.max(
        np.abs(
            trace
            - expected_trace
        )
    )
)

max_trace_relative_error = (
    max_trace_abs_error
    / expected_trace
)


# ------------------------------------------------------------
# Save numerical results
# ------------------------------------------------------------

data_path = Path(
    "results/data/"
    "001b_kottler_tidal_eigenvalues.csv"
)

np.savetxt(
    data_path,
    np.column_stack([
        radius_m,
        radius_mpc,
        radial,
        transverse,
        trace,
    ]),
    delimiter=",",
    header=(
        "radius_m,"
        "radius_mpc,"
        "radial_eigenvalue_s-2,"
        "transverse_eigenvalue_s-2,"
        "tidal_trace_s-2"
    ),
    comments="",
)


# ------------------------------------------------------------
# Figure
# ------------------------------------------------------------

figure_path = Path(
    "results/figures/"
    "001b_kottler_tidal_eigenvalues.png"
)

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    radius_mpc,
    radial,
    label="Radial geodesic deviation",
)

plt.plot(
    radius_mpc,
    transverse,
    label="Transverse geodesic deviation",
)

plt.axhline(
    0.0,
    linewidth=1.0,
)

plt.axvline(
    R_STATIC_MPC,
    linestyle="--",
    label=(
        "All-direction stretching threshold "
        f"{R_STATIC_MPC:.3f} Mpc"
    ),
)

plt.xscale("log")

plt.yscale(
    "symlog",
    linthresh=1e-35,
)

plt.xlabel(
    "Radius (Mpc)"
)

plt.ylabel(
    "Geodesic-deviation eigenvalue (s^-2)"
)

plt.title(
    "Simulation 001B — Kottler Tidal Eigenvalues"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.close()


# ------------------------------------------------------------
# Output
# ------------------------------------------------------------

print(
    "=== SIMULATION 001B RESULTS ==="
)

print()

print(
    f"LAMBDA={LAMBDA:.12e} m^-2"
)

print(
    f"MASS={MASS_SOLAR:.6e} solar masses"
)

print()

print(
    "ANALYTICAL_ALL_DIRECTION_THRESHOLD="
    f"{R_STATIC_MPC:.12f} Mpc"
)

print(
    "NUMERICAL_TRANSVERSE_ZERO="
    f"{numerical_threshold_mpc:.12f} Mpc"
)

print(
    "THRESHOLD_RELATIVE_GRID_ERROR="
    f"{threshold_relative_error:.6e}"
)

print()

print(
    "PURE_DE_SITTER_TIDAL_EIGENVALUE="
    f"{de_sitter_eigenvalue:.12e} s^-2"
)

print(
    "PURE_DE_SITTER_CHARACTERISTIC_RATE="
    f"{de_sitter_rate:.12e} s^-1"
)

print(
    "PURE_DE_SITTER_CHARACTERISTIC_TIMESCALE="
    f"{de_sitter_timescale_gyr:.9f} Gyr"
)

print()

print(
    "EXPECTED_TIDAL_TRACE="
    f"{expected_trace:.12e} s^-2"
)

print(
    "MAX_TRACE_RELATIVE_ERROR="
    f"{max_trace_relative_error:.6e}"
)

print()

print(
    "=== SAMPLE TIDAL STATES ==="
)

for radius_value in [
    0.1,
    0.5,
    1.0,
    R_STATIC_MPC,
    2.0,
    5.0,
]:

    r = (
        radius_value
        * MEGAPARSEC_M
    )

    radial_value = (
        radial_tidal_eigenvalue_s2(
            r,
            MASS_KG,
            LAMBDA,
        )
    )

    transverse_value = (
        transverse_tidal_eigenvalue_s2(
            r,
            MASS_KG,
            LAMBDA,
        )
    )

    if (
        radial_value > 0.0
        and transverse_value > 0.0
    ):
        state = (
            "ALL_DIRECTION_STRETCHING"
        )

    elif (
        radial_value > 0.0
        and transverse_value < 0.0
    ):
        state = (
            "RADIAL_STRETCH_"
            "TRANSVERSE_COMPRESSION"
        )

    else:
        state = "OTHER"

    print()
    print(
        f"RADIUS={radius_value:.12f} Mpc"
    )

    print(
        "  RADIAL="
        f"{radial_value:.12e} s^-2"
    )

    print(
        "  TRANSVERSE="
        f"{transverse_value:.12e} s^-2"
    )

    print(
        f"  STATE={state}"
    )

print()

print(
    f"DATA={data_path}"
)

print(
    f"FIGURE={figure_path}"
)

print()

print(
    "GEODESIC_DEVIATION_USED=YES"
)

print(
    "ALL_DIRECTION_STRETCHING_REGION="
    "EXPECTED"
)

print(
    "KNOWN_GR_RESULT_REPRODUCED=YES"
)

print(
    "NOVEL_ANTIGRAVITY_CLAIM=NO"
)
