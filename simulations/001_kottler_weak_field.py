"""Simulation 001A

Numerically explore the weak-field radial acceleration in
Schwarzschild-de Sitter (Kottler) spacetime.

This simulation is a BASELINE REPRODUCTION of known physics.

It does not represent a novel antigravity claim.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from antigravity_research.geometry.kottler import (
    C,
    MEGAPARSEC_M,
    SOLAR_MASS_KG,
    cosmological_acceleration,
    cosmological_constant_from_flat_lcdm,
    static_radius,
    weak_field_attractive_acceleration,
)


# ---------------------------------------------------------------------------
# Planck 2018 baseline cosmology
# ---------------------------------------------------------------------------

H0_KM_S_MPC = 67.4
OMEGA_M = 0.315

# Flat Lambda-CDM baseline.
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


# ---------------------------------------------------------------------------
# Test system
# ---------------------------------------------------------------------------

# Use a Milky-Way-scale gravitational mass.
#
# This is not intended to model all details of the actual Milky Way.
# It is simply a convenient spherical mass scale for the baseline experiment.

MASS_SOLAR = 1.0e12
MASS_KG = MASS_SOLAR * SOLAR_MASS_KG


# ---------------------------------------------------------------------------
# Analytical balance radius
# ---------------------------------------------------------------------------

R_STATIC_M = static_radius(
    MASS_KG,
    LAMBDA,
)

R_STATIC_MPC = R_STATIC_M / MEGAPARSEC_M


# ---------------------------------------------------------------------------
# Numerical radius grid
# ---------------------------------------------------------------------------

radius_mpc = np.logspace(
    np.log10(0.05),
    np.log10(5.0),
    2000,
)

radius_m = radius_mpc * MEGAPARSEC_M


# ---------------------------------------------------------------------------
# Calculate acceleration components
# ---------------------------------------------------------------------------

attractive = np.array(
    [
        weak_field_attractive_acceleration(r, MASS_KG)
        for r in radius_m
    ]
)

lambda_outward = np.array(
    [
        cosmological_acceleration(r, LAMBDA)
        for r in radius_m
    ]
)

net = attractive + lambda_outward


# ---------------------------------------------------------------------------
# Numerical sign-change estimate
# ---------------------------------------------------------------------------

crossing_index = np.argmin(np.abs(net))

R_NUMERICAL_MPC = radius_mpc[crossing_index]
A_NUMERICAL = net[crossing_index]


# ---------------------------------------------------------------------------
# Save numerical data
# ---------------------------------------------------------------------------

output_data = Path(
    "results/data/001_kottler_weak_field.csv"
)

table = np.column_stack(
    (
        radius_m,
        radius_mpc,
        attractive,
        lambda_outward,
        net,
    )
)

np.savetxt(
    output_data,
    table,
    delimiter=",",
    header=(
        "radius_m,"
        "radius_mpc,"
        "attractive_acceleration_m_s2,"
        "lambda_acceleration_m_s2,"
        "net_acceleration_m_s2"
    ),
    comments="",
)


# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------

output_figure = Path(
    "results/figures/001_kottler_weak_field.png"
)

plt.figure(figsize=(10, 6))

plt.plot(
    radius_mpc,
    attractive,
    label="Central attraction",
)

plt.plot(
    radius_mpc,
    lambda_outward,
    label="Positive cosmological-constant term",
)

plt.plot(
    radius_mpc,
    net,
    label="Net radial acceleration",
)

plt.axhline(
    0.0,
    linewidth=1.0,
)

plt.axvline(
    R_STATIC_MPC,
    linestyle="--",
    label=f"Analytical balance radius = {R_STATIC_MPC:.3f} Mpc",
)

plt.xscale("log")

plt.yscale(
    "symlog",
    linthresh=1.0e-15,
)

plt.xlabel("Radius (Mpc)")
plt.ylabel("Radial acceleration (m/s²)")

plt.title(
    "Simulation 001A — Schwarzschild-de Sitter Weak-Field Acceleration"
)

plt.legend()

plt.tight_layout()
plt.savefig(
    output_figure,
    dpi=180,
)

plt.close()


# ---------------------------------------------------------------------------
# Diagnostic sample points
# ---------------------------------------------------------------------------

sample_radii_mpc = [
    0.1,
    0.5,
    1.0,
    R_STATIC_MPC,
    2.0,
    5.0,
]


print("=== SIMULATION 001A RESULTS ===")
print()

print(
    f"H0={H0_KM_S_MPC:.3f} km/s/Mpc"
)

print(
    f"OMEGA_M={OMEGA_M:.6f}"
)

print(
    f"OMEGA_LAMBDA={OMEGA_LAMBDA:.6f}"
)

print(
    f"LAMBDA={LAMBDA:.12e} m^-2"
)

print()

print(
    f"MASS={MASS_SOLAR:.6e} solar masses"
)

print(
    f"ANALYTICAL_STATIC_RADIUS={R_STATIC_MPC:.12f} Mpc"
)

print(
    f"NUMERICAL_STATIC_RADIUS={R_NUMERICAL_MPC:.12f} Mpc"
)

relative_error = abs(
    R_NUMERICAL_MPC - R_STATIC_MPC
) / R_STATIC_MPC

print(
    f"STATIC_RADIUS_RELATIVE_GRID_ERROR={relative_error:.6e}"
)

print(
    f"NET_ACCELERATION_NEAR_NUMERICAL_CROSSING="
    f"{A_NUMERICAL:.12e} m/s^2"
)

print()

print("=== SAMPLE RADIAL ACCELERATIONS ===")

for radius_mpc_value in sample_radii_mpc:

    r = radius_mpc_value * MEGAPARSEC_M

    a_mass = weak_field_attractive_acceleration(
        r,
        MASS_KG,
    )

    a_lambda = cosmological_acceleration(
        r,
        LAMBDA,
    )

    a_total = a_mass + a_lambda

    direction = (
        "OUTWARD"
        if a_total > 0.0
        else "INWARD"
        if a_total < 0.0
        else "BALANCED"
    )

    print()
    print(
        f"RADIUS={radius_mpc_value:.12f} Mpc"
    )
    print(
        f"  MASS_TERM={a_mass:.12e} m/s^2"
    )
    print(
        f"  LAMBDA_TERM={a_lambda:.12e} m/s^2"
    )
    print(
        f"  NET={a_total:.12e} m/s^2"
    )
    print(
        f"  DIRECTION={direction}"
    )

print()
print(
    f"DATA={output_data}"
)

print(
    f"FIGURE={output_figure}"
)

print()
print(
    "INTERPRETATION=BASELINE_KNOWN_PHYSICS_ONLY"
)
print(
    "NOVEL_ANTIGRAVITY_CLAIM=NO"
)
