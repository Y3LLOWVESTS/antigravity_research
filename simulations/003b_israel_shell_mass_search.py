"""Simulation 003B.

Exact static Israel-junction shell search.

We use a positive-vacuum-energy de Sitter core and vary the Schwarzschild
ADM mass outside the shell.

Primary question:

    Can a finite spherical source have an outward Schwarzschild exterior
    while retaining ordinary shell energy conditions?

For Schwarzschild vacuum:

    outward weak-field acceleration requires M_ADM < 0.

We therefore scan positive, zero, and negative exterior ADM mass while
calculating the exact shell surface energy and tangential pressure.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from antigravity_research.geometry.israel_shell import (
    evaluate_shell_energy_conditions,
    exterior_weak_field_acceleration_m_s2,
    gravastar_mass_relation_residual_kg,
    interior_volume_mass_kg,
    shell_energy_mass_kg,
    surface_energy_j_m2,
    surface_mass_density_kg_m2,
    surface_pressure_n_m,
)


G0 = 9.80665

TARGETS = [
    (
        "micro_g_over_1m",
        1.0e-6 * G0,
        1.0,
    ),
    (
        "one_percent_g_over_1m",
        1.0e-2 * G0,
        1.0,
    ),
    (
        "one_g_over_1m",
        G0,
        1.0,
    ),
]

# M_ext / M_volume
MASS_RATIOS = np.array([
    -2.0,
    -1.0,
    -0.75,
    -0.50,
    -0.49,
    -0.25,
    -0.10,
    0.0,
    0.25,
    0.50,
    0.75,
    1.0,
    1.25,
    2.0,
])

rows = []

print(
    "=== SIMULATION 003B RESULTS ==="
)

print()

for (
    target_name,
    target_acceleration,
    radius,
) in TARGETS:

    rate = (
        target_acceleration
        / radius
    )

    volume_mass = interior_volume_mass_kg(
        rate,
        radius,
    )

    print(
        f"=== TARGET={target_name} ==="
    )

    print(
        f"CORE_RADIUS={radius:.12e} m"
    )

    print(
        f"TARGET_DEFOCUSING_RATE={rate:.12e} s^-2"
    )

    print(
        f"INTERIOR_VOLUME_ENERGY_MASS={volume_mass:.12e} kg"
    )

    print()

    for ratio in MASS_RATIOS:

        exterior_mass = (
            float(ratio)
            * volume_mass
        )

        energy = surface_energy_j_m2(
            rate,
            radius,
            exterior_mass,
        )

        mass_density = (
            surface_mass_density_kg_m2(
                rate,
                radius,
                exterior_mass,
            )
        )

        pressure = surface_pressure_n_m(
            rate,
            radius,
            exterior_mass,
        )

        shell_mass = shell_energy_mass_kg(
            rate,
            radius,
            exterior_mass,
        )

        conditions = evaluate_shell_energy_conditions(
            energy,
            pressure,
        )

        acceleration_2r = (
            exterior_weak_field_acceleration_m_s2(
                2.0 * radius,
                exterior_mass,
            )
        )

        residual = (
            gravastar_mass_relation_residual_kg(
                rate,
                radius,
                exterior_mass,
            )
        )

        outward = (
            acceleration_2r > 0.0
        )

        rows.append({
            "target":
                target_name,
            "radius_m":
                radius,
            "rate_s-2":
                rate,
            "interior_volume_mass_kg":
                volume_mass,
            "exterior_mass_ratio":
                float(ratio),
            "exterior_adm_mass_kg":
                exterior_mass,
            "surface_energy_j_m2":
                energy,
            "surface_mass_density_kg_m2":
                mass_density,
            "shell_energy_mass_kg":
                shell_mass,
            "surface_pressure_n_m":
                pressure,
            "nec":
                conditions.nec,
            "wec":
                conditions.wec,
            "dec":
                conditions.dec,
            "exterior_acceleration_at_2r_m_s2":
                acceleration_2r,
            "exterior_outward":
                outward,
            "mass_relation_residual_kg":
                residual,
        })

        print(
            f"M_EXT_OVER_MV={ratio:+.2f}"
        )

        print(
            f"  M_EXT={exterior_mass:.12e} kg"
        )

        print(
            f"  SHELL_SURFACE_ENERGY={energy:.12e} J/m^2"
        )

        print(
            f"  SHELL_SURFACE_MASS_DENSITY={mass_density:.12e} kg/m^2"
        )

        print(
            f"  SHELL_ENERGY_MASS={shell_mass:.12e} kg"
        )

        print(
            f"  SHELL_TANGENTIAL_PRESSURE={pressure:.12e} N/m"
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
            "  EXTERIOR_ACCELERATION_AT_2R="
            f"{acceleration_2r:.12e} m/s^2"
        )

        print(
            "  EXTERIOR_DIRECTION="
            f"{'OUTWARD' if outward else 'INWARD' if acceleration_2r < 0 else 'ZERO'}"
        )

        print(
            "  MASS_RELATION_RESIDUAL="
            f"{residual:.12e} kg"
        )

        print()


# ============================================================
# Save CSV
# ============================================================

data_path = Path(
    "results/data/"
    "003b_israel_shell_mass_search.csv"
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
# Continuous one-g scan for plot and threshold diagnostics
# ============================================================

target_acceleration = G0
radius = 1.0
rate = target_acceleration / radius

volume_mass = interior_volume_mass_kg(
    rate,
    radius,
)

scan_ratios = np.linspace(
    -2.0,
    2.0,
    4001,
)

scan_energy = []
scan_pressure = []
scan_nec_margin = []

for ratio in scan_ratios:

    exterior_mass = (
        float(ratio)
        * volume_mass
    )

    energy = surface_energy_j_m2(
        rate,
        radius,
        exterior_mass,
    )

    pressure = surface_pressure_n_m(
        rate,
        radius,
        exterior_mass,
    )

    scan_energy.append(
        energy
    )

    scan_pressure.append(
        pressure
    )

    scan_nec_margin.append(
        energy + pressure
    )

scan_energy = np.array(
    scan_energy
)

scan_pressure = np.array(
    scan_pressure
)

scan_nec_margin = np.array(
    scan_nec_margin
)

# Locate sign changes.
def nearest_zero_ratio(values):
    index = int(
        np.argmin(
            np.abs(values)
        )
    )

    return float(
        scan_ratios[index]
    )


energy_zero_ratio = (
    nearest_zero_ratio(
        scan_energy
    )
)

nec_zero_ratio = (
    nearest_zero_ratio(
        scan_nec_margin
    )
)


# ============================================================
# Plot
# ============================================================

figure_path = Path(
    "results/figures/"
    "003b_israel_shell_conditions_1g.png"
)

scale = max(
    np.max(
        np.abs(
            scan_energy
        )
    ),
    np.max(
        np.abs(
            scan_pressure
        )
    ),
)

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    scan_ratios,
    scan_energy / scale,
    label="Surface energy / scale",
)

plt.plot(
    scan_ratios,
    scan_pressure / scale,
    label="Tangential pressure / scale",
)

plt.plot(
    scan_ratios,
    scan_nec_margin / scale,
    label="NEC margin (U + P) / scale",
)

plt.axhline(
    0.0,
    linewidth=1.0,
)

plt.axvline(
    0.0,
    linestyle="--",
    label="Exterior mass = 0",
)

plt.axvline(
    1.0,
    linestyle=":",
    label="Exterior mass = core volume mass",
)

plt.xlabel(
    "Exterior ADM mass / interior volume-energy mass"
)

plt.ylabel(
    "Normalized shell stress"
)

plt.title(
    "Simulation 003B — Israel Shell Stress vs Exterior ADM Mass"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.close()


# ============================================================
# Global questions
# ============================================================

outward_rows = [
    row
    for row in rows
    if row["exterior_outward"]
]

outward_wec_pass = [
    row
    for row in outward_rows
    if row["wec"]
]

outward_dec_pass = [
    row
    for row in outward_rows
    if row["dec"]
]

outward_nec_pass = [
    row
    for row in outward_rows
    if row["nec"]
]

positive_surface_energy_outward = [
    row
    for row in outward_rows
    if row["surface_energy_j_m2"] >= 0.0
]

max_mass_relation_fractional_error = max(
    abs(
        row["mass_relation_residual_kg"]
    )
    / max(
        abs(
            row["exterior_adm_mass_kg"]
        ),
        abs(
            row["interior_volume_mass_kg"]
        ),
        1.0,
    )
    for row in rows
)

print(
    "=== SIMULATION 003B SUMMARY ==="
)

print()

print(
    f"ONE_G_SURFACE_ENERGY_ZERO_MASS_RATIO="
    f"{energy_zero_ratio:.6f}"
)

print(
    f"ONE_G_NEC_ZERO_MASS_RATIO_APPROX="
    f"{nec_zero_ratio:.6f}"
)

print()

print(
    "OUTWARD_SCHWARZSCHILD_EXTERIOR_REQUIRES_NEGATIVE_ADM_MASS=YES"
)

print(
    "OUTWARD_CASE_WITH_NONNEGATIVE_SHELL_SURFACE_ENERGY="
    f"{'YES' if positive_surface_energy_outward else 'NO'}"
)

print(
    "OUTWARD_CASE_WITH_WEC="
    f"{'YES' if outward_wec_pass else 'NO'}"
)

print(
    "OUTWARD_CASE_WITH_DEC="
    f"{'YES' if outward_dec_pass else 'NO'}"
)

print(
    "OUTWARD_CASE_WITH_NEC="
    f"{'YES' if outward_nec_pass else 'NO'}"
)

print(
    "NEGATIVE_SHELL_ENERGY_REQUIRED_FOR_OUTWARD_EXTERIOR="
    f"{'NO' if positive_surface_energy_outward else 'YES'}"
)

print(
    "MAX_MASS_RELATION_FRACTIONAL_ERROR="
    f"{max_mass_relation_fractional_error:.12e}"
)

print(
    f"DATA={data_path}"
)

print(
    f"FIGURE={figure_path}"
)

print()

print(
    "STATIC_SPHERICAL_POSITIVE_ENERGY_ANTIGRAVITY_FOUND=NO"
)

print(
    "EXOTIC_NEGATIVE_SURFACE_ENERGY_ROUTE_EXISTS="
    f"{'YES' if outward_rows else 'NO'}"
)

print(
    "NEXT=DYNAMIC_STABILITY_AND_NEC_SURVIVING_NEGATIVE_MASS_WINDOW"
)
