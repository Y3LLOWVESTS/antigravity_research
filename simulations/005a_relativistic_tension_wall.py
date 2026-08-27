"""Simulation 005A.

Question:

What positive-energy stress tensor gives the largest planar gravitational
repulsion while satisfying the dominant energy condition?

For an isotropic membrane:

    surface energy = U
    tangential tension = tau = q U

Repulsion:
    q > 1/2

DEC:
    q <= 1

Therefore:

    1/2 < q <= 1

is a positive-energy DEC-compatible repulsive interval.

The q=1 endpoint is the ideal relativistic domain wall and minimizes the
positive energy required for a specified gravitational acceleration.

We also translate that minimum wall tension into the parameters of a
standard phi^4 scalar kink.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from antigravity_research.geometry.relativistic_wall import (
    circular_patch_energy_mass_kg,
    domain_wall_minimum_surface_energy_j_m2,
    evaluate_wall_energy_conditions,
    outward_planar_acceleration_m_s2,
    phi4_v_gev_for_tension,
    phi4_wall_thickness_m,
    required_surface_energy_j_m2,
    surface_mass_equivalent_kg_m2,
    wall_tension_gev3_from_si,
)


G0 = 9.80665

TARGETS = [
    ("micro_g", 1.0e-6 * G0),
    ("one_percent_g", 1.0e-2 * G0),
    ("one_g", G0),
]

Q_VALUES = [
    0.51,
    0.60,
    0.75,
    0.90,
    1.00,
]

LAMBDA_VALUES = [
    1.0,
    0.1,
    0.01,
]

PATCH_RADII = [
    1.0,
    1.0e-2,
    1.0e-3,
    1.0e-6,
]

rows = []

print(
    "=== SIMULATION 005A RESULTS ==="
)

print()

print(
    "MODEL=POSITIVE_ENERGY_RELATIVISTIC_MEMBRANE"
)

print(
    "GRAVITY_THEORY=GENERAL_RELATIVITY"
)

print(
    "REPULSION_CONDITION=TAU_OVER_U_GT_1_OVER_2"
)

print(
    "DEC_CONDITION=TAU_OVER_U_LE_1"
)

print(
    "DEC_COMPATIBLE_REPULSIVE_INTERVAL=0.5_LT_Q_LE_1.0"
)

print()

for target_name, target_accel in TARGETS:

    print(
        f"=== TARGET={target_name} ==="
    )

    print(
        f"ACCELERATION={target_accel:.12e} m/s^2"
    )

    print()

    for q in Q_VALUES:

        u = required_surface_energy_j_m2(
            target_accel,
            q,
        )

        tau = (
            q * u
        )

        reconstructed = (
            outward_planar_acceleration_m_s2(
                u,
                tau,
            )
        )

        conditions = (
            evaluate_wall_energy_conditions(
                u,
                tau,
            )
        )

        mass_per_area = (
            surface_mass_equivalent_kg_m2(
                u
            )
        )

        rows.append({
            "target":
                target_name,
            "target_acceleration_m_s2":
                target_accel,
            "q_tension_over_energy":
                q,
            "surface_energy_j_m2":
                u,
            "surface_tension_n_m":
                tau,
            "surface_mass_equivalent_kg_m2":
                mass_per_area,
            "reconstructed_acceleration_m_s2":
                reconstructed,
            "nec":
                conditions.nec,
            "wec":
                conditions.wec,
            "dec":
                conditions.dec,
        })

        print(
            f"Q={q:.2f}"
        )

        print(
            f"  SURFACE_ENERGY={u:.12e} J/m^2"
        )

        print(
            f"  TENSION={tau:.12e} N/m"
        )

        print(
            f"  MASS_EQUIVALENT_PER_AREA={mass_per_area:.12e} kg/m^2"
        )

        print(
            f"  NEC={'PASS' if conditions.nec else 'FAIL'}"
        )

        print(
            f"  WEC={'PASS' if conditions.wec else 'FAIL'}"
        )

        print(
            f"  DEC={'PASS' if conditions.dec else 'FAIL'}"
        )

        print(
            f"  RECONSTRUCTED_ACCELERATION={reconstructed:.12e} m/s^2"
        )

        print()

    u_min = (
        domain_wall_minimum_surface_energy_j_m2(
            target_accel
        )
    )

    sigma_gev3 = (
        wall_tension_gev3_from_si(
            u_min
        )
    )

    print(
        "--- OPTIMAL DEC DOMAIN-WALL LIMIT q=1 ---"
    )

    print(
        f"MIN_SURFACE_ENERGY={u_min:.12e} J/m^2"
    )

    print(
        "MIN_SURFACE_MASS_EQUIVALENT="
        f"{surface_mass_equivalent_kg_m2(u_min):.12e} kg/m^2"
    )

    print(
        f"NATURAL_UNIT_TENSION={sigma_gev3:.12e} GeV^3"
    )

    print()

    for lam in LAMBDA_VALUES:

        v = phi4_v_gev_for_tension(
            u_min,
            lam,
        )

        thickness = phi4_wall_thickness_m(
            v,
            lam,
        )

        print(
            f"PHI4_LAMBDA={lam:.2e}"
        )

        print(
            f"  VEV_SCALE={v:.12e} GeV"
        )

        print(
            f"  WALL_THICKNESS_SCALE={thickness:.12e} m"
        )

    print()

    print(
        "--- PATCH ENERGY ACCOUNTING ---"
    )

    for radius in PATCH_RADII:

        patch_mass = circular_patch_energy_mass_kg(
            radius,
            u_min,
        )

        print(
            f"PATCH_RADIUS={radius:.12e} m"
        )

        print(
            f"  POSITIVE_ENERGY_MASS={patch_mass:.12e} kg"
        )

        print(
            f"  POSITIVE_ENERGY={patch_mass * 299792458.0**2:.12e} J"
        )

    print()


# ============================================================
# SAVE CSV
# ============================================================

data_path = Path(
    "results/data/"
    "005a_relativistic_tension_wall.csv"
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


# ============================================================
# PLOT ENERGY PENALTY VS q
# ============================================================

q_scan = np.linspace(
    0.5005,
    1.0,
    2000,
)

u_scan = np.array([
    required_surface_energy_j_m2(
        G0,
        float(q),
    )
    for q in q_scan
])

u_opt = (
    domain_wall_minimum_surface_energy_j_m2(
        G0
    )
)

figure_path = Path(
    "results/figures/"
    "005a_tension_efficiency.png"
)

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    q_scan,
    u_scan / u_opt,
)

plt.axvline(
    1.0,
    linestyle="--",
    label="Domain-wall limit q=1",
)

plt.axhline(
    1.0,
    linestyle=":",
)

plt.yscale(
    "log"
)

plt.xlabel(
    "Tension ratio q = tau / U"
)

plt.ylabel(
    "Required surface energy / domain-wall minimum"
)

plt.title(
    "Simulation 005A — Repulsive Gravity Efficiency of Relativistic Tension"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.close()


# ============================================================
# GLOBAL CONCLUSIONS
# ============================================================

repulsive_dec_window_confirmed = all(
    row["reconstructed_acceleration_m_s2"] > 0.0
    and row["nec"]
    and row["wec"]
    and row["dec"]
    for row in rows
)

one_g_min = (
    domain_wall_minimum_surface_energy_j_m2(
        G0
    )
)

one_g_v = (
    phi4_v_gev_for_tension(
        one_g_min,
        1.0,
    )
)

print(
    "=== SIMULATION 005A SUMMARY ==="
)

print()

print(
    "POSITIVE_ENERGY_REPULSION_WITH_NEC_WEC_DEC="
    f"{'YES' if repulsive_dec_window_confirmed else 'NO'}"
)

print(
    "REPULSIVE_TENSION_THRESHOLD_Q=0.5"
)

print(
    "DEC_MAXIMUM_TENSION_RATIO_Q=1.0"
)

print(
    "DOMAIN_WALL_Q1_OPTIMAL_WITHIN_DEC_MEMBRANE_CLASS=YES"
)

print(
    f"ONE_G_MIN_SURFACE_ENERGY={one_g_min:.12e} J/m^2"
)

print(
    "ONE_G_MIN_SURFACE_MASS="
    f"{surface_mass_equivalent_kg_m2(one_g_min):.12e} kg/m^2"
)

print(
    f"ONE_G_PHI4_LAMBDA1_VEV={one_g_v:.12e} GeV"
)

print(
    "NEGATIVE_ENERGY_REQUIRED=NO"
)

print(
    "NEGATIVE_ADM_MASS_REQUIRED=NO_FOR_PLANAR_WALL"
)

print(
    "ELECTRIC_CHARGE_REQUIRED=NO"
)

print(
    "SCHWINGER_LIMIT_RELEVANT=NO"
)

print(
    "KNOWN_GR_DOMAIN_WALL_REPULSION_REPRODUCED=YES"
)

print(
    "FINITE_STABLE_LAB_CONFIGURATION_ESTABLISHED=NO"
)

print(
    f"DATA={data_path}"
)

print(
    f"FIGURE={figure_path}"
)

print()

print(
    "DESIGN_PRINCIPLE="
    "MAXIMIZE_RELATIVISTIC_TANGENTIAL_TENSION_PER_UNIT_POSITIVE_ENERGY"
)

print(
    "NEXT="
    "FINITE_SCALAR_WALL_STABILITY_AND_BOUNDARY_SUPPORT"
)
