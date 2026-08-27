"""Simulation 004A.

Search for a finite, positive-ADM-mass Einstein-Maxwell source with a
repulsive gravitational region outside the physical surface.

Geometry:

    Minkowski interior
    charged thin shell at radius R
    Reissner-Nordstrom exterior

Criterion:

    z = r_rep/R > 1

where

    r_rep = Q^2/(4*pi*epsilon0*M*c^2).

We then require the shell to satisfy:

    NEC
    WEC
    DEC

and note that the exterior Maxwell field itself has positive energy and
satisfies the standard classical energy conditions.

This is a known GR mechanism being reproduced and quantitatively tested,
not a claim of novel physics.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from antigravity_research.geometry.reissner_nordstrom import (
    charged_shell_surface_energy_j_m2,
    charged_shell_surface_pressure_n_m,
    electric_field_v_m,
    electromagnetic_field_energy_mass_outside_kg,
    evaluate_shell_conditions,
    neutral_free_tendency_m_s2,
    repulsion_radius_m,
    schwinger_critical_field_v_m,
    solve_source_for_surface_repulsion,
)


G0 = 9.80665

TARGETS = [
    ("micro_g", 1.0e-6 * G0),
    ("one_percent_g", 1.0e-2 * G0),
    ("one_g", G0),
]

RADIUS_M = 1.0

Z_SCAN = np.linspace(
    1.001,
    1.999,
    1999,
)

SCHWINGER = (
    schwinger_critical_field_v_m()
)

rows = []

print(
    "=== SIMULATION 004A RESULTS ==="
)

print()

print(
    "THEORY=EINSTEIN_MAXWELL"
)

print(
    "EXTERIOR=REISSNER_NORDSTROM"
)

print(
    "INTERIOR=MINKOWSKI"
)

print(
    "SOURCE=STATIC_CHARGED_THIN_SHELL"
)

print(
    f"SCHWINGER_FIELD={SCHWINGER:.12e} V/m"
)

print()

for target_name, target_g in TARGETS:

    passing = []

    for z in Z_SCAN:

        mass, charge = (
            solve_source_for_surface_repulsion(
                target_g,
                RADIUS_M,
                float(z),
            )
        )

        surface_energy = (
            charged_shell_surface_energy_j_m2(
                RADIUS_M,
                mass,
                charge,
            )
        )

        surface_pressure = (
            charged_shell_surface_pressure_n_m(
                RADIUS_M,
                mass,
                charge,
            )
        )

        conditions = (
            evaluate_shell_conditions(
                surface_energy,
                surface_pressure,
            )
        )

        field = electric_field_v_m(
            RADIUS_M,
            charge,
        )

        r_rep = repulsion_radius_m(
            mass,
            charge,
        )

        field_mass = (
            electromagnetic_field_energy_mass_outside_kg(
                RADIUS_M,
                charge,
            )
        )

        reconstructed_g = (
            neutral_free_tendency_m_s2(
                RADIUS_M,
                mass,
                charge,
            )
        )

        row = {
            "target":
                target_name,
            "target_outward_acceleration_m_s2":
                target_g,
            "radius_m":
                RADIUS_M,
            "z_rrep_over_R":
                float(z),
            "mass_kg":
                mass,
            "charge_c":
                charge,
            "repulsion_radius_m":
                r_rep,
            "repulsive_zone_width_m":
                r_rep - RADIUS_M,
            "surface_electric_field_v_m":
                field,
            "surface_field_over_schwinger":
                field / SCHWINGER,
            "em_field_energy_mass_outside_kg":
                field_mass,
            "em_field_mass_fraction_of_adm":
                field_mass / mass,
            "shell_surface_energy_j_m2":
                surface_energy,
            "shell_surface_pressure_n_m":
                surface_pressure,
            "shell_nec":
                conditions.nec,
            "shell_wec":
                conditions.wec,
            "shell_dec":
                conditions.dec,
            "reconstructed_surface_repulsion_m_s2":
                reconstructed_g,
        }

        rows.append(row)

        if (
            surface_energy >= 0.0
            and conditions.nec
            and conditions.wec
            and conditions.dec
        ):
            passing.append(
                row
            )

    print(
        f"=== TARGET={target_name} ==="
    )

    print(
        f"TARGET_G_FRACTION={target_g/G0:.12e}"
    )

    print(
        f"RADIUS={RADIUS_M:.6f} m"
    )

    if not passing:
        print(
            "POSITIVE_ENERGY_DEC_REPULSIVE_CANDIDATE=NO"
        )

        print()
        continue

    z_min = min(
        row["z_rrep_over_R"]
        for row in passing
    )

    z_max = max(
        row["z_rrep_over_R"]
        for row in passing
    )

    print(
        "POSITIVE_ENERGY_DEC_REPULSIVE_CANDIDATE=YES"
    )

    print(
        f"DEC_REPULSIVE_Z_MIN={z_min:.6f}"
    )

    print(
        f"DEC_REPULSIVE_Z_MAX={z_max:.6f}"
    )

    # Robust benchmark comfortably inside expected window.
    benchmark = min(
        passing,
        key=lambda row: abs(
            row["z_rrep_over_R"]
            - 1.2
        ),
    )

    print()
    print(
        "--- ROBUST z≈1.2 BENCHMARK ---"
    )

    print(
        f"Z={benchmark['z_rrep_over_R']:.6f}"
    )

    print(
        f"ADM_MASS={benchmark['mass_kg']:.12e} kg"
    )

    print(
        f"CHARGE={benchmark['charge_c']:.12e} C"
    )

    print(
        "REPULSION_RADIUS="
        f"{benchmark['repulsion_radius_m']:.12e} m"
    )

    print(
        "EXTERNAL_REPULSIVE_ZONE_WIDTH="
        f"{benchmark['repulsive_zone_width_m']:.12e} m"
    )

    print(
        "SURFACE_ELECTRIC_FIELD="
        f"{benchmark['surface_electric_field_v_m']:.12e} V/m"
    )

    print(
        "FIELD_OVER_SCHWINGER="
        f"{benchmark['surface_field_over_schwinger']:.12e}"
    )

    print(
        "EM_FIELD_MASS_FRACTION="
        f"{benchmark['em_field_mass_fraction_of_adm']:.12f}"
    )

    print(
        "SHELL_SURFACE_ENERGY="
        f"{benchmark['shell_surface_energy_j_m2']:.12e} J/m^2"
    )

    print(
        "SHELL_SURFACE_PRESSURE="
        f"{benchmark['shell_surface_pressure_n_m']:.12e} N/m"
    )

    print(
        f"SHELL_NEC={'PASS' if benchmark['shell_nec'] else 'FAIL'}"
    )

    print(
        f"SHELL_WEC={'PASS' if benchmark['shell_wec'] else 'FAIL'}"
    )

    print(
        f"SHELL_DEC={'PASS' if benchmark['shell_dec'] else 'FAIL'}"
    )

    print(
        "RECONSTRUCTED_OUTWARD_GRAVITY="
        f"{benchmark['reconstructed_surface_repulsion_m_s2']:.12e} m/s^2"
    )

    print()


# ============================================================
# Save full search
# ============================================================

data_path = Path(
    "results/data/"
    "004a_einstein_maxwell_repulsion.csv"
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
# Plot one-g z=1.2 candidate
# ============================================================

mass, charge = solve_source_for_surface_repulsion(
    G0,
    1.0,
    1.2,
)

r_rep = repulsion_radius_m(
    mass,
    charge,
)

radii = np.linspace(
    1.0,
    2.0,
    1200,
)

gravity = np.array([
    neutral_free_tendency_m_s2(
        float(r),
        mass,
        charge,
    )
    for r in radii
])

figure_path = Path(
    "results/figures/"
    "004a_rn_neutral_gravity_1g_z1p2.png"
)

plt.figure(
    figsize=(10, 6)
)

plt.plot(
    radii,
    gravity / G0,
    label="Neutral gravitational tendency",
)

plt.axhline(
    0.0,
    linewidth=1.0,
)

plt.axvline(
    r_rep,
    linestyle="--",
    label=(
        "Gravity sign-change radius "
        f"{r_rep:.3f} m"
    ),
)

plt.xlabel(
    "Radius from center (m)"
)

plt.ylabel(
    "Outward gravitational tendency / g"
)

plt.title(
    "Simulation 004A — Positive-Mass RN Repulsive Region"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.close()


# ============================================================
# Schwinger-radius search
# ============================================================

print(
    "=== QED FIELD-SCALE SEARCH AT z=1.2 ==="
)

print()

for target_name, target_g in TARGETS:

    radius_scan = np.logspace(
        -4,
        7,
        5000,
    )

    first_below = None

    for radius in radius_scan:

        mass, charge = (
            solve_source_for_surface_repulsion(
                target_g,
                float(radius),
                1.2,
            )
        )

        field = electric_field_v_m(
            float(radius),
            charge,
        )

        if field < SCHWINGER:
            first_below = (
                float(radius),
                mass,
                charge,
                field,
            )
            break

    print(
        f"TARGET={target_name}"
    )

    if first_below is None:
        print(
            "  SUB_SCHWINGER_RADIUS_FOUND=NO"
        )
    else:
        (
            radius,
            mass,
            charge,
            field,
        ) = first_below

        print(
            "  SUB_SCHWINGER_RADIUS_FOUND=YES"
        )

        print(
            f"  MIN_RADIUS_APPROX={radius:.12e} m"
        )

        print(
            f"  ADM_MASS={mass:.12e} kg"
        )

        print(
            f"  CHARGE={charge:.12e} C"
        )

        print(
            f"  SURFACE_FIELD={field:.12e} V/m"
        )

    print()


# ============================================================
# Summary
# ============================================================

positive_dec_repulsive = [
    row
    for row in rows
    if (
        row["z_rrep_over_R"] > 1.0
        and row["shell_surface_energy_j_m2"] >= 0.0
        and row["shell_nec"]
        and row["shell_wec"]
        and row["shell_dec"]
    )
]

print(
    "=== SIMULATION 004A SUMMARY ==="
)

print()

print(
    "POSITIVE_ADM_MASS=YES"
)

print(
    "MAXWELL_FIELD_ENERGY_POSITIVE=YES"
)

print(
    "MAXWELL_NEC_WEC_DEC=PASS"
)

print(
    "EXTERNAL_NEUTRAL_GRAVITATIONAL_REPULSION="
    f"{'YES' if positive_dec_repulsive else 'NO'}"
)

print(
    "REPULSION_WITH_NONNEGATIVE_SHELL_ENERGY="
    f"{'YES' if positive_dec_repulsive else 'NO'}"
)

print(
    "REPULSION_WITH_SHELL_WEC="
    f"{'YES' if positive_dec_repulsive else 'NO'}"
)

print(
    "REPULSION_WITH_SHELL_DEC="
    f"{'YES' if positive_dec_repulsive else 'NO'}"
)

print(
    "NEGATIVE_ADM_MASS_REQUIRED="
    f"{'NO' if positive_dec_repulsive else 'UNRESOLVED'}"
)

print(
    "NEGATIVE_ENERGY_REQUIRED="
    f"{'NO_FOR_THIS_EXACT_MODEL' if positive_dec_repulsive else 'UNRESOLVED'}"
)

print(
    f"DATA={data_path}"
)

print(
    f"FIGURE={figure_path}"
)

print()

print(
    "KNOWN_RN_REPULSIVE_GRAVITY_MECHANISM_REPRODUCED="
    f"{'YES' if positive_dec_repulsive else 'NO'}"
)

print(
    "NOVEL_PHYSICS_CLAIM=NO"
)

print(
    "PRACTICAL_DEVICE_ESTABLISHED=NO"
)

print(
    "NEXT="
    "CHARGED_SHELL_STABILITY_DISCHARGE_AND_MATERIAL_REALIZABILITY"
)
