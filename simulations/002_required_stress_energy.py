"""Simulation 002.

Reverse the local isotropic GR acceleration equation.

Question:

    What idealized perfect-fluid stress-energy would be required to
    produce a prescribed outward relative acceleration between
    neighboring free-falling observers?

This is a CURVATURE REQUIREMENT BENCHMARK.

It is not yet a finite-source solution or antigravity-device design.
"""

from __future__ import annotations

import csv
from pathlib import Path
import math

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from antigravity_research.geometry.kottler import (
    C,
    MEGAPARSEC_M,
    cosmological_constant_from_flat_lcdm,
)

from antigravity_research.geometry.perfect_fluid_defocusing import (
    evaluate_energy_conditions,
    isotropic_defocusing_rate_s2,
    required_active_mass_density_kg_m3,
    required_energy_density_for_w,
)


G0 = 9.80665

# ------------------------------------------------------------
# Observed cosmological baseline
# ------------------------------------------------------------

H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_LAMBDA = 1.0 - OMEGA_M

H0_S = (
    H0_KM_S_MPC
    * 1000.0
    / MEGAPARSEC_M
)

OBSERVED_LAMBDA = (
    cosmological_constant_from_flat_lcdm(
        H0_S,
        OMEGA_LAMBDA,
    )
)

OBSERVED_LAMBDA_RATE = (
    OBSERVED_LAMBDA
    * C**2
    / 3.0
)


# ------------------------------------------------------------
# Target effects
# ------------------------------------------------------------

TARGETS = [
    ("micro_g", 1.0e-6 * G0),
    ("one_percent_g", 1.0e-2 * G0),
    ("one_g", 1.0 * G0),
]

SEPARATIONS_M = [
    0.1,
    1.0,
    10.0,
    100.0,
]


# ------------------------------------------------------------
# Equation-of-state models
#
# p = w * epsilon
# ------------------------------------------------------------

MODELS = [
    ("phantom_w_-1.2", -1.2),
    ("vacuum_w_-1", -1.0),
    ("negative_pressure_w_-2_3", -2.0 / 3.0),
    ("negative_pressure_w_-1_2", -0.5),
    ("near_SEC_boundary_w_-0.34", -0.34),
    ("dust_negative_energy_route", 0.0),
]


# ------------------------------------------------------------
# Scan
# ------------------------------------------------------------

rows = []

for target_name, target_acceleration in TARGETS:

    for separation_m in SEPARATIONS_M:

        target_rate = (
            target_acceleration
            / separation_m
        )

        rho_active = (
            required_active_mass_density_kg_m3(
                target_acceleration,
                separation_m,
                cosmological_constant_m2=OBSERVED_LAMBDA,
            )
        )

        for model_name, w in MODELS:

            epsilon = (
                required_energy_density_for_w(
                    target_acceleration,
                    separation_m,
                    w,
                    cosmological_constant_m2=OBSERVED_LAMBDA,
                )
            )

            pressure = (
                w
                * epsilon
            )

            rho_equivalent = (
                epsilon
                / C**2
            )

            conditions = (
                evaluate_energy_conditions(
                    epsilon,
                    pressure,
                )
            )

            reconstructed_rate = (
                isotropic_defocusing_rate_s2(
                    epsilon,
                    pressure,
                    OBSERVED_LAMBDA,
                )
            )

            reconstructed_acceleration = (
                reconstructed_rate
                * separation_m
            )

            reconstruction_relative_error = (
                abs(
                    reconstructed_acceleration
                    - target_acceleration
                )
                / target_acceleration
            )

            sphere_volume_m3 = (
                4.0
                / 3.0
                * math.pi
                * separation_m**3
            )

            energy_equivalent_mass_in_sphere_kg = (
                rho_equivalent
                * sphere_volume_m3
            )

            rows.append({
                "target": target_name,
                "target_acceleration_m_s2": target_acceleration,
                "target_g_fraction": target_acceleration / G0,
                "separation_m": separation_m,
                "target_rate_s-2": target_rate,
                "model": model_name,
                "w": w,
                "energy_density_j_m3": epsilon,
                "equivalent_mass_density_kg_m3": rho_equivalent,
                "pressure_pa": pressure,
                "active_mass_density_kg_m3": rho_active,
                "energy_equivalent_mass_sphere_kg":
                    energy_equivalent_mass_in_sphere_kg,
                "nec": conditions.nec,
                "wec": conditions.wec,
                "sec": conditions.sec,
                "dec": conditions.dec,
                "reconstruction_relative_error":
                    reconstruction_relative_error,
            })


# ------------------------------------------------------------
# CSV
# ------------------------------------------------------------

data_path = Path(
    "results/data/"
    "002_required_stress_energy.csv"
)

with data_path.open(
    "w",
    newline="",
) as handle:

    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            rows[0].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(rows)


# ------------------------------------------------------------
# Numerical consistency
# ------------------------------------------------------------

max_reconstruction_error = max(
    row["reconstruction_relative_error"]
    for row in rows
)


# ------------------------------------------------------------
# Plot:
# required |rho| versus target acceleration at 1 m
# ------------------------------------------------------------

figure_path = Path(
    "results/figures/"
    "002_required_energy_density_1m.png"
)

target_acceleration_scan = (
    np.logspace(
        -9,
        0,
        400,
    )
    * G0
)

plt.figure(
    figsize=(10, 6)
)

for model_name, w in MODELS:

    densities = []

    for acceleration in target_acceleration_scan:

        epsilon = (
            required_energy_density_for_w(
                acceleration,
                1.0,
                w,
                cosmological_constant_m2=OBSERVED_LAMBDA,
            )
        )

        densities.append(
            abs(
                epsilon
                / C**2
            )
        )

    plt.loglog(
        target_acceleration_scan / G0,
        densities,
        label=model_name,
    )

plt.xlabel(
    "Desired relative acceleration / g at 1 m"
)

plt.ylabel(
    "|required energy-equivalent density| (kg/m³)"
)

plt.title(
    "Simulation 002 — Stress-Energy Scale for Local Defocusing"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.close()


# ------------------------------------------------------------
# Diagnostic summary
# ------------------------------------------------------------

print(
    "=== SIMULATION 002 RESULTS ==="
)

print()

print(
    "MODEL="
    "LOCALLY_HOMOGENEOUS_ISOTROPIC_PERFECT_FLUID"
)

print(
    "FINITE_STATIC_SOURCE_SOLUTION=NO"
)

print()

print(
    f"OBSERVED_LAMBDA="
    f"{OBSERVED_LAMBDA:.12e} m^-2"
)

print(
    f"OBSERVED_LAMBDA_DEFOCUSING_RATE="
    f"{OBSERVED_LAMBDA_RATE:.12e} s^-2"
)

print(
    "OBSERVED_LAMBDA_ACCELERATION_AT_1M="
    f"{OBSERVED_LAMBDA_RATE:.12e} m/s^2"
)

print(
    "OBSERVED_LAMBDA_G_FRACTION_AT_1M="
    f"{OBSERVED_LAMBDA_RATE / G0:.12e}"
)

print()

print(
    "=== ONE-METER VACUUM-LIKE BENCHMARK ==="
)

for target_name, target_acceleration in TARGETS:

    epsilon = (
        required_energy_density_for_w(
            target_acceleration,
            1.0,
            -1.0,
            cosmological_constant_m2=OBSERVED_LAMBDA,
        )
    )

    rho = (
        epsilon
        / C**2
    )

    pressure = (
        -epsilon
    )

    active_rho = (
        required_active_mass_density_kg_m3(
            target_acceleration,
            1.0,
            cosmological_constant_m2=OBSERVED_LAMBDA,
        )
    )

    sphere_equivalent_mass = (
        rho
        * (
            4.0
            / 3.0
            * math.pi
        )
    )

    print()
    print(
        f"TARGET={target_name}"
    )

    print(
        "  ACCELERATION="
        f"{target_acceleration:.12e} m/s^2"
    )

    print(
        "  G_FRACTION="
        f"{target_acceleration / G0:.12e}"
    )

    print(
        "  REQUIRED_ENERGY_DENSITY="
        f"{epsilon:.12e} J/m^3"
    )

    print(
        "  ENERGY_EQUIVALENT_DENSITY="
        f"{rho:.12e} kg/m^3"
    )

    print(
        "  REQUIRED_PRESSURE="
        f"{pressure:.12e} Pa"
    )

    print(
        "  ACTIVE_GRAVITATIONAL_DENSITY="
        f"{active_rho:.12e} kg/m^3"
    )

    print(
        "  ENERGY_EQUIVALENT_MASS_IN_1M_RADIUS_SPHERE="
        f"{sphere_equivalent_mass:.12e} kg"
    )

    print(
        "  NEC=SATURATED"
    )

    print(
        "  WEC=SATISFIED"
    )

    print(
        "  SEC=VIOLATED"
    )

    print(
        "  DEC=SATURATED"
    )


# ------------------------------------------------------------
# Compare equations of state for 1g over 1m
# ------------------------------------------------------------

print()

print(
    "=== ONE_G_OVER_ONE_METER EOS SEARCH ==="
)

target_acceleration = G0
separation_m = 1.0

for model_name, w in MODELS:

    epsilon = (
        required_energy_density_for_w(
            target_acceleration,
            separation_m,
            w,
            cosmological_constant_m2=OBSERVED_LAMBDA,
        )
    )

    pressure = (
        w
        * epsilon
    )

    rho = (
        epsilon
        / C**2
    )

    conditions = (
        evaluate_energy_conditions(
            epsilon,
            pressure,
        )
    )

    print()
    print(
        f"MODEL={model_name}"
    )

    print(
        f"  W={w:.12f}"
    )

    print(
        "  EPSILON="
        f"{epsilon:.12e} J/m^3"
    )

    print(
        "  RHO_EQUIVALENT="
        f"{rho:.12e} kg/m^3"
    )

    print(
        "  PRESSURE="
        f"{pressure:.12e} Pa"
    )

    print(
        f"  NEC={'PASS' if conditions.nec else 'FAIL'}"
    )

    print(
        f"  WEC={'PASS' if conditions.wec else 'FAIL'}"
    )

    print(
        f"  SEC={'PASS' if conditions.sec else 'FAIL'}"
    )

    print(
        f"  DEC={'PASS' if conditions.dec else 'FAIL'}"
    )


print()

print(
    "MAX_RECONSTRUCTION_RELATIVE_ERROR="
    f"{max_reconstruction_error:.12e}"
)

print(
    f"DATA={data_path}"
)

print(
    f"FIGURE={figure_path}"
)

print()

print(
    "POSITIVE_ENERGY_DEFOCUSING_WITHOUT_NEC_VIOLATION="
    "POSSIBLE_IN_IDEAL_PERFECT_FLUID_MODEL"
)

print(
    "STRONG_ENERGY_CONDITION_VIOLATION_REQUIRED_FOR_THIS_CLASS="
    "YES"
)

print(
    "PRACTICAL_LOCAL_SOURCE_ESTABLISHED="
    "NO"
)

print(
    "NOVEL_ANTIGRAVITY_CLAIM="
    "NO"
)

print(
    "NEXT="
    "FINITE_SPHERICAL_SOURCE_AND_BOUNDARY_CONSISTENCY"
)
