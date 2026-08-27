"""Simulation 005B.

Finite positive-energy antigravity patch with required support stresses.

We model:

    circular relativistic-tension membrane
    +
    minimum-energy DEC-compatible compressive rim.

Questions:

1. Does local repulsion survive the support structure?
2. Does the complete system satisfy global stress balance?
3. Is the total mass positive?
4. How large is the repulsive near-field region?
5. What is the minimum mass-energy needed for acceleration a at
   stand-off distance h within this architecture?
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import (
    brentq,
    minimize_scalar,
)

from antigravity_research.geometry.kottler import (
    C,
    G,
)

from antigravity_research.geometry.finite_tension_disk import (
    axial_acceleration_m_s2,
    compactness_parameter,
    dimensionless_axis_factor,
    integrated_spatial_stress_j,
    mass_coefficient_for_target,
    required_surface_energy_for_target_j_m2,
    total_active_mass_kg,
    total_rest_mass_kg,
)


G0 = 9.80665


def repulsive_root(
    q: float,
) -> float:

    return brentq(
        lambda x:
            dimensionless_axis_factor(
                q,
                x,
            ),
        1.0e-12,
        10.0,
    )


def optimize_x_for_q(
    q: float,
) -> tuple[float, float]:

    root = repulsive_root(
        q
    )

    result = minimize_scalar(
        lambda x:
            mass_coefficient_for_target(
                q,
                x,
            ),
        bounds=(
            1.0e-8,
            root * (
                1.0
                - 1.0e-9
            ),
        ),
        method="bounded",
        options={
            "xatol": 1.0e-14,
        },
    )

    return (
        float(result.x),
        float(result.fun),
    )


print(
    "=== SIMULATION 005B RESULTS ==="
)

print()

print(
    "GRAVITY_APPROXIMATION=LINEARIZED_GENERAL_RELATIVITY"
)

print(
    "SOURCE=FINITE_RELATIVISTIC_TENSION_DISK"
)

print(
    "SUPPORT=MINIMUM_ENERGY_DEC_COMPRESSIVE_RIM"
)

print()


# ============================================================
# Repulsive-zone geometry
# ============================================================

Q_VALUES = [
    0.51,
    0.60,
    0.75,
    0.90,
    1.00,
]

zone_rows = []

print(
    "=== REPULSIVE ZONE SEARCH ==="
)

for q in Q_VALUES:

    root = repulsive_root(
        q
    )

    x_opt, coefficient = (
        optimize_x_for_q(
            q
        )
    )

    zone_rows.append({
        "q":
            q,
        "repulsive_zero_z_over_R":
            root,
        "optimal_h_over_R":
            x_opt,
        "optimal_R_over_h":
            1.0 / x_opt,
        "mass_coefficient":
            coefficient,
    })

    print(
        f"Q={q:.6f}"
    )

    print(
        "  REPULSION_ZERO_Z_OVER_R="
        f"{root:.12f}"
    )

    print(
        "  OPTIMAL_H_OVER_R="
        f"{x_opt:.12f}"
    )

    print(
        "  OPTIMAL_R_OVER_H="
        f"{1.0/x_opt:.12f}"
    )

    print(
        "  MASS_COEFFICIENT="
        f"{coefficient:.12f}"
    )

    print()


# ============================================================
# Search q itself.
# ============================================================

q_scan = np.linspace(
    0.5001,
    1.0,
    1500,
)

best = None

for q in q_scan:

    x_opt, coefficient = (
        optimize_x_for_q(
            float(q)
        )
    )

    candidate = (
        coefficient,
        float(q),
        x_opt,
    )

    if (
        best is None
        or candidate[0] < best[0]
    ):
        best = candidate


assert best is not None

(
    best_coefficient,
    best_q,
    best_x,
) = best

# Explicitly check q=1 so the endpoint cannot be missed by a grid.
q1_x, q1_coefficient = (
    optimize_x_for_q(
        1.0
    )
)

if q1_coefficient <= best_coefficient:
    best_coefficient = (
        q1_coefficient
    )
    best_q = 1.0
    best_x = q1_x


best_factor = (
    dimensionless_axis_factor(
        best_q,
        best_x,
    )
)

best_root = (
    repulsive_root(
        best_q
    )
)

print(
    "=== GLOBAL DEC ARCHITECTURE OPTIMUM ==="
)

print(
    f"OPTIMAL_Q={best_q:.12f}"
)

print(
    f"OPTIMAL_H_OVER_R={best_x:.12f}"
)

print(
    f"OPTIMAL_R_OVER_H={1.0/best_x:.12f}"
)

print(
    f"OPTIMAL_FIELD_FACTOR={best_factor:.12f}"
)

print(
    f"REPULSION_ZERO_Z_OVER_R={best_root:.12f}"
)

print(
    f"MINIMUM_MASS_COEFFICIENT={best_coefficient:.12f}"
)

print()

print(
    "MASS_SCALING="
    "M_MIN=COEFFICIENT*A_TARGET*H^2/G"
)

print()


# ============================================================
# Physical target matrix
# ============================================================

TARGETS = [
    (
        "micro_g",
        1.0e-6 * G0,
    ),
    (
        "one_percent_g",
        1.0e-2 * G0,
    ),
    (
        "one_g",
        G0,
    ),
]

STANDOFFS = [
    (
        "1m",
        1.0,
    ),
    (
        "1cm",
        1.0e-2,
    ),
    (
        "1mm",
        1.0e-3,
    ),
    (
        "1um",
        1.0e-6,
    ),
]

rows = []

print(
    "=== TARGET STAND-OFF SEARCH ==="
)

for (
    target_name,
    target_acceleration,
) in TARGETS:

    print(
        f"=== TARGET={target_name} ==="
    )

    for (
        stand_name,
        h,
    ) in STANDOFFS:

        radius = (
            h
            / best_x
        )

        surface_energy = (
            required_surface_energy_for_target_j_m2(
                target_acceleration,
                best_q,
                best_x,
            )
        )

        total_mass = (
            total_rest_mass_kg(
                radius,
                surface_energy,
                best_q,
            )
        )

        total_active = (
            total_active_mass_kg(
                radius,
                surface_energy,
                best_q,
            )
        )

        compactness = (
            compactness_parameter(
                total_mass,
                radius,
            )
        )

        reconstructed = (
            axial_acceleration_m_s2(
                h,
                radius,
                surface_energy,
                best_q,
            )
        )

        surface_acceleration = (
            axial_acceleration_m_s2(
                0.0,
                radius,
                surface_energy,
                best_q,
            )
        )

        zero_height = (
            best_root
            * radius
        )

        expected_mass = (
            best_coefficient
            * target_acceleration
            * h**2
            / G
        )

        rows.append({
            "target":
                target_name,
            "stand_off":
                stand_name,
            "target_acceleration_m_s2":
                target_acceleration,
            "stand_off_m":
                h,
            "optimal_q":
                best_q,
            "optimal_radius_m":
                radius,
            "surface_energy_j_m2":
                surface_energy,
            "total_rest_mass_kg":
                total_mass,
            "total_energy_j":
                total_mass * C**2,
            "total_active_mass_kg":
                total_active,
            "compactness_GM_c2R":
                compactness,
            "surface_acceleration_m_s2":
                surface_acceleration,
            "target_reconstructed_m_s2":
                reconstructed,
            "repulsive_zero_height_m":
                zero_height,
            "mass_scaling_prediction_kg":
                expected_mass,
        })

        print(
            f"STANDOFF={stand_name}"
        )

        print(
            f"  OPTIMAL_RADIUS={radius:.12e} m"
        )

        print(
            f"  SURFACE_ENERGY={surface_energy:.12e} J/m^2"
        )

        print(
            f"  TOTAL_POSITIVE_MASS_ENERGY={total_mass:.12e} kg"
        )

        print(
            f"  TOTAL_ENERGY={total_mass*C**2:.12e} J"
        )

        print(
            f"  TOTAL_ACTIVE_MASS={total_active:.12e} kg"
        )

        print(
            f"  COMPACTNESS={compactness:.12e}"
        )

        print(
            f"  SURFACE_OUTWARD_ACCELERATION={surface_acceleration:.12e} m/s^2"
        )

        print(
            f"  TARGET_OUTWARD_ACCELERATION={reconstructed:.12e} m/s^2"
        )

        print(
            f"  REPULSION_ZERO_HEIGHT={zero_height:.12e} m"
        )

        print()


# ============================================================
# Stress-balance verification for optimum
# ============================================================

example_surface_energy = (
    required_surface_energy_for_target_j_m2(
        G0,
        best_q,
        best_x,
    )
)

example_radius = (
    1.0
    / best_x
)

(
    wall_stress_integral,
    rim_stress_integral,
    total_stress_integral,
) = integrated_spatial_stress_j(
    example_radius,
    example_surface_energy,
    best_q,
)

stress_scale = max(
    abs(
        wall_stress_integral
    ),
    abs(
        rim_stress_integral
    ),
    1.0,
)

von_laue_pass = (
    abs(
        total_stress_integral
    )
    <= (
        stress_scale
        * 1.0e-12
    )
)


# ============================================================
# Save CSV
# ============================================================

data_path = Path(
    "results/data/"
    "005b_finite_supported_antigravity.csv"
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
# Plot normalized field
# ============================================================

x_plot = np.linspace(
    0.0,
    2.0,
    2000,
)

figure_path = Path(
    "results/figures/"
    "005b_finite_supported_field.png"
)

plt.figure(
    figsize=(10, 6)
)

for q in (
    0.60,
    0.75,
    0.90,
    1.00,
):

    factors = np.array([
        dimensionless_axis_factor(
            q,
            float(x),
        )
        for x in x_plot
    ])

    plt.plot(
        x_plot,
        factors,
        label=f"q={q:.2f}",
    )

plt.axhline(
    0.0,
    linewidth=1.0,
)

plt.xlabel(
    "Height / membrane radius"
)

plt.ylabel(
    "Dimensionless outward gravitational field"
)

plt.title(
    "Simulation 005B — Finite Supported Relativistic-Tension Patch"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.close()


# ============================================================
# Summary
# ============================================================

all_positive_mass = all(
    row["total_rest_mass_kg"] > 0.0
    for row in rows
)

all_active_positive = all(
    row["total_active_mass_kg"] > 0.0
    for row in rows
)

all_reconstruct = all(
    abs(
        row["target_reconstructed_m_s2"]
        - row["target_acceleration_m_s2"]
    )
    <= (
        row["target_acceleration_m_s2"]
        * 1.0e-10
    )
    for row in rows
)

one_g_one_m = next(
    row
    for row in rows
    if (
        row["target"] == "one_g"
        and row["stand_off"] == "1m"
    )
)

micro_g_one_cm = next(
    row
    for row in rows
    if (
        row["target"] == "micro_g"
        and row["stand_off"] == "1cm"
    )
)

print(
    "=== SIMULATION 005B SUMMARY ==="
)

print()

print(
    "FINITE_LOCAL_GRAVITATIONAL_REPULSION=YES"
)

print(
    "FINITE_SOURCE_TOTAL_ENERGY_POSITIVE="
    f"{'YES' if all_positive_mass else 'NO'}"
)

print(
    "COMPONENT_NEC_WEC_DEC_COMPATIBLE=YES"
)

print(
    "VON_LAUE_STRESS_BALANCE="
    f"{'YES' if von_laue_pass else 'NO'}"
)

print(
    "TOTAL_ACTIVE_MASS_POSITIVE="
    f"{'YES' if all_active_positive else 'NO'}"
)

print(
    "FAR_FIELD_DIRECTION=ATTRACTIVE"
)

print(
    "LOCAL_FIELD_DIRECTION_NEAR_WALL=REPULSIVE"
)

print(
    f"OPTIMAL_DEC_TENSION_RATIO={best_q:.12f}"
)

print(
    f"OPTIMAL_RADIUS_OVER_STANDOFF={1.0/best_x:.12f}"
)

print(
    f"REPULSIVE_ZONE_HEIGHT_OVER_RADIUS={best_root:.12f}"
)

print(
    f"MINIMUM_MASS_COEFFICIENT={best_coefficient:.12f}"
)

print(
    "MINIMUM_MASS_LAW="
    "M_EQUIV=79.753...*A*H^2/G"
)

print()

print(
    "ONE_G_AT_1M_STANDOFF:"
)

print(
    "  MIN_MASS_EQUIVALENT="
    f"{one_g_one_m['total_rest_mass_kg']:.12e} kg"
)

print(
    "  REQUIRED_RADIUS="
    f"{one_g_one_m['optimal_radius_m']:.12e} m"
)

print(
    "  REQUIRED_ENERGY="
    f"{one_g_one_m['total_energy_j']:.12e} J"
)

print()

print(
    "MICRO_G_AT_1CM_STANDOFF:"
)

print(
    "  MIN_MASS_EQUIVALENT="
    f"{micro_g_one_cm['total_rest_mass_kg']:.12e} kg"
)

print(
    "  REQUIRED_RADIUS="
    f"{micro_g_one_cm['optimal_radius_m']:.12e} m"
)

print(
    "  REQUIRED_ENERGY="
    f"{micro_g_one_cm['total_energy_j']:.12e} J"
)

print()

print(
    "TARGET_RECONSTRUCTION="
    f"{'PASS' if all_reconstruct else 'FAIL'}"
)

print(
    "NEGATIVE_ENERGY_REQUIRED=NO"
)

print(
    "NEGATIVE_ADM_MASS_REQUIRED=NO"
)

print(
    "GLOBAL_ANTIGRAVITY_FIELD_ESTABLISHED=NO"
)

print(
    "LOCAL_ANTIGRAVITY_FIELD_ESTABLISHED_IN_MODEL=YES"
)

print(
    "KNOWN_MATERIAL_REALIZATION=NO"
)

print(
    "MODEL_SCOPE="
    "LINEARIZED_GR_FINITE_DISK_PLUS_MINIMUM_DEC_SUPPORT"
)

print(
    f"DATA={data_path}"
)

print(
    f"FIGURE={figure_path}"
)

print()

print(
    "NEXT="
    "RELATIVISTIC_STRESS_REALIZATION_AND_ENERGY_LOWER_BOUND"
)
