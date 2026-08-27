"""Simulation 006A.

Independent numerical test of the most optimistic positive-energy static
antigravity bound in linearized GR.

We formulate the stress-balance problem as a linear program.

Variables:

    E_r      repulsive-region energy
    E_s      support-region energy

    P_ri     integrated principal stresses in repulsive region
    P_si     integrated principal stresses in support region

Units are normalized so the required negative integrated active source is

    -(E_r + sum P_ri) = 1.

Constraints:

    E >= 0

DEC:

    -E <= P_i <= E

Static Laue balance:

    P_ri + P_si = 0
    for i = x,y,z.

We minimize:

    E_total = E_r + E_s.

If the analytic reasoning is correct, the optimum should be

    E_r = 1/2
    E_s = 1/2

with

    P_ri = -1/2
    P_si = +1/2

in all three directions.

Therefore:

    E_total / negative_active_source = 1.

For a membrane constrained to

    P_rx = 0
    P_ry = P_rz = -E_r,

the corresponding optimum should be 2.
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog

from antigravity_research.geometry.energy_bounds import (
    energy_j_from_mass_kg,
    pointwise_dec_mass_lower_bound_kg,
    static_laue_dec_mass_lower_bound_kg,
)


G0 = 9.80665
DISK_005B_COEFFICIENT = 79.753148116012


def solve_general_static_dec_lp():
    # variables:
    # Er, Es, Prx, Pry, Prz, Psx, Psy, Psz

    c = np.array([
        1.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ])

    aub = []
    bub = []

    # DEC: |P_ri| <= Er
    for index in (2, 3, 4):
        row = np.zeros(8)
        row[index] = 1.0
        row[0] = -1.0
        aub.append(row)
        bub.append(0.0)

        row = np.zeros(8)
        row[index] = -1.0
        row[0] = -1.0
        aub.append(row)
        bub.append(0.0)

    # DEC: |P_si| <= Es
    for index in (5, 6, 7):
        row = np.zeros(8)
        row[index] = 1.0
        row[1] = -1.0
        aub.append(row)
        bub.append(0.0)

        row = np.zeros(8)
        row[index] = -1.0
        row[1] = -1.0
        aub.append(row)
        bub.append(0.0)

    aeq = []
    beq = []

    # Laue balance in each direction.
    for ri, si in zip(
        (2, 3, 4),
        (5, 6, 7),
    ):
        row = np.zeros(8)
        row[ri] = 1.0
        row[si] = 1.0
        aeq.append(row)
        beq.append(0.0)

    # Normalize negative active source:
    #
    # Er + Prx + Pry + Prz = -1.
    row = np.zeros(8)
    row[0] = 1.0
    row[2] = 1.0
    row[3] = 1.0
    row[4] = 1.0
    aeq.append(row)
    beq.append(-1.0)

    result = linprog(
        c,
        A_ub=np.array(aub),
        b_ub=np.array(bub),
        A_eq=np.array(aeq),
        b_eq=np.array(beq),
        bounds=[
            (0.0, None),
            (0.0, None),
            (None, None),
            (None, None),
            (None, None),
            (None, None),
            (None, None),
            (None, None),
        ],
        method="highs",
    )

    if not result.success:
        raise RuntimeError(
            result.message
        )

    return result


def solve_domain_wall_subclass_lp():
    # Same variables and DEC/Laue constraints, plus:
    #
    # Prx = 0
    # Pry = -Er
    # Prz = -Er
    #
    # This represents the q=1 membrane stress pattern.

    c = np.array([
        1.0,
        1.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ])

    aub = []
    bub = []

    for energy_index, pressure_indices in (
        (0, (2, 3, 4)),
        (1, (5, 6, 7)),
    ):
        for index in pressure_indices:
            row = np.zeros(8)
            row[index] = 1.0
            row[energy_index] = -1.0
            aub.append(row)
            bub.append(0.0)

            row = np.zeros(8)
            row[index] = -1.0
            row[energy_index] = -1.0
            aub.append(row)
            bub.append(0.0)

    aeq = []
    beq = []

    for ri, si in zip(
        (2, 3, 4),
        (5, 6, 7),
    ):
        row = np.zeros(8)
        row[ri] = 1.0
        row[si] = 1.0
        aeq.append(row)
        beq.append(0.0)

    # Wall stress constraints.
    row = np.zeros(8)
    row[2] = 1.0
    aeq.append(row)
    beq.append(0.0)

    row = np.zeros(8)
    row[3] = 1.0
    row[0] = 1.0
    aeq.append(row)
    beq.append(0.0)

    row = np.zeros(8)
    row[4] = 1.0
    row[0] = 1.0
    aeq.append(row)
    beq.append(0.0)

    # Negative active source normalization.
    row = np.zeros(8)
    row[0] = 1.0
    row[2] = 1.0
    row[3] = 1.0
    row[4] = 1.0
    aeq.append(row)
    beq.append(-1.0)

    result = linprog(
        c,
        A_ub=np.array(aub),
        b_ub=np.array(bub),
        A_eq=np.array(aeq),
        b_eq=np.array(beq),
        bounds=[
            (0.0, None),
            (0.0, None),
            (None, None),
            (None, None),
            (None, None),
            (None, None),
            (None, None),
            (None, None),
        ],
        method="highs",
    )

    if not result.success:
        raise RuntimeError(
            result.message
        )

    return result


general = solve_general_static_dec_lp()
wall = solve_domain_wall_subclass_lp()

print(
    "=== SIMULATION 006A RESULTS ==="
)

print()

print(
    "GENERAL_STATIC_DEC_LP_STATUS=GREEN"
)

print(
    f"GENERAL_MIN_ENERGY_COEFFICIENT={general.fun:.12f}"
)

labels = (
    "E_REP",
    "E_SUPPORT",
    "P_REP_X",
    "P_REP_Y",
    "P_REP_Z",
    "P_SUPPORT_X",
    "P_SUPPORT_Y",
    "P_SUPPORT_Z",
)

for label, value in zip(
    labels,
    general.x,
):
    print(
        f"{label}={value:.12f}"
    )

print()

print(
    "DOMAIN_WALL_STATIC_DEC_LP_STATUS=GREEN"
)

print(
    f"DOMAIN_WALL_MIN_ENERGY_COEFFICIENT={wall.fun:.12f}"
)

print()

print(
    "005B_DISK_MASS_COEFFICIENT="
    f"{DISK_005B_COEFFICIENT:.12f}"
)

print(
    "005B_OVER_GENERAL_STATIC_BOUND="
    f"{DISK_005B_COEFFICIENT/general.fun:.12f}"
)

print(
    "005B_OVER_DOMAIN_WALL_ABSTRACT_BOUND="
    f"{DISK_005B_COEFFICIENT/wall.fun:.12f}"
)

print()


TARGETS = [
    ("micro_g", 1.0e-6 * G0),
    ("one_percent_g", 1.0e-2 * G0),
    ("one_g", G0),
]

DISTANCES = [
    ("1m", 1.0),
    ("1cm", 1.0e-2),
    ("1mm", 1.0e-3),
    ("1um", 1.0e-6),
    ("1nm", 1.0e-9),
]

rows = []

print(
    "=== FUNDAMENTAL SCALE MATRIX ==="
)

for target_name, acceleration in TARGETS:

    print(
        f"=== TARGET={target_name} ==="
    )

    for distance_name, h in DISTANCES:

        pointwise_mass = (
            pointwise_dec_mass_lower_bound_kg(
                acceleration,
                h,
            )
        )

        static_mass = (
            static_laue_dec_mass_lower_bound_kg(
                acceleration,
                h,
            )
        )

        disk_mass = (
            DISK_005B_COEFFICIENT
            * acceleration
            * h**2
            / 6.67430e-11
        )

        static_energy = (
            energy_j_from_mass_kg(
                static_mass
            )
        )

        rows.append({
            "target":
                target_name,
            "distance":
                distance_name,
            "acceleration_m_s2":
                acceleration,
            "minimum_distance_m":
                h,
            "pointwise_dec_mass_bound_kg":
                pointwise_mass,
            "static_laue_dec_mass_bound_kg":
                static_mass,
            "static_laue_dec_energy_bound_j":
                static_energy,
            "005b_disk_mass_kg":
                disk_mass,
            "005b_over_static_bound":
                disk_mass / static_mass,
        })

        print(
            f"DISTANCE={distance_name}"
        )

        print(
            "  POINTWISE_DEC_MIN_MASS="
            f"{pointwise_mass:.12e} kg"
        )

        print(
            "  STATIC_LAUE_DEC_MIN_MASS="
            f"{static_mass:.12e} kg"
        )

        print(
            "  STATIC_LAUE_DEC_MIN_ENERGY="
            f"{static_energy:.12e} J"
        )

        print(
            "  005B_DISK_EQUIVALENT_MASS="
            f"{disk_mass:.12e} kg"
        )

    print()


data_path = Path(
    "results/data/"
    "006a_static_dec_energy_bound.csv"
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
# Plot one-g distance scaling.
# ============================================================

h_scan = np.logspace(
    -9,
    1,
    1000,
)

static_mass_scan = (
    G0
    * h_scan**2
    / 6.67430e-11
)

disk_mass_scan = (
    DISK_005B_COEFFICIENT
    * G0
    * h_scan**2
    / 6.67430e-11
)

figure_path = Path(
    "results/figures/"
    "006a_static_dec_mass_bound.png"
)

plt.figure(
    figsize=(10, 6)
)

plt.loglog(
    h_scan,
    static_mass_scan,
    label="Optimistic static DEC + Laue lower bound",
)

plt.loglog(
    h_scan,
    disk_mass_scan,
    label="Simulation 005B disk + rim",
)

plt.xlabel(
    "Minimum source-target distance h (m)"
)

plt.ylabel(
    "Energy-equivalent mass for 1g (kg)"
)

plt.title(
    "Simulation 006A — Positive-Energy Static Antigravity Cost"
)

plt.legend()
plt.tight_layout()

plt.savefig(
    figure_path,
    dpi=180,
)

plt.close()


# ============================================================
# Specific decisive benchmarks.
# ============================================================

one_g_1m = static_laue_dec_mass_lower_bound_kg(
    G0,
    1.0,
)

one_g_1um = static_laue_dec_mass_lower_bound_kg(
    G0,
    1.0e-6,
)

micro_g_1cm = static_laue_dec_mass_lower_bound_kg(
    1.0e-6 * G0,
    1.0e-2,
)

print(
    "=== SIMULATION 006A SUMMARY ==="
)

print()

print(
    "POINTWISE_DEC_MAX_NEGATIVE_ACTIVE_RATIO=-2"
)

print(
    "MAXIMALLY_REPULSIVE_DEC_STRESS="
    "PX_EQ_PY_EQ_PZ_EQ_MINUS_EPSILON"
)

print(
    "STATIC_LAUE_STRESS_BALANCE_REQUIRED=YES"
)

print(
    "GENERAL_STATIC_DEC_MIN_MASS_COEFFICIENT="
    f"{general.fun:.12f}"
)

print(
    "DOMAIN_WALL_SUBCLASS_MIN_MASS_COEFFICIENT="
    f"{wall.fun:.12f}"
)

print(
    "005B_ARCHITECTURE_COEFFICIENT="
    f"{DISK_005B_COEFFICIENT:.12f}"
)

print()

print(
    "ONE_G_1M_STATIC_LOWER_BOUND_MASS="
    f"{one_g_1m:.12e} kg"
)

print(
    "ONE_G_1M_STATIC_LOWER_BOUND_ENERGY="
    f"{energy_j_from_mass_kg(one_g_1m):.12e} J"
)

print(
    "ONE_G_1UM_STATIC_LOWER_BOUND_MASS="
    f"{one_g_1um:.12e} kg"
)

print(
    "ONE_G_1UM_STATIC_LOWER_BOUND_ENERGY="
    f"{energy_j_from_mass_kg(one_g_1um):.12e} J"
)

print(
    "MICRO_G_1CM_STATIC_LOWER_BOUND_MASS="
    f"{micro_g_1cm:.12e} kg"
)

print(
    "MICRO_G_1CM_STATIC_LOWER_BOUND_ENERGY="
    f"{energy_j_from_mass_kg(micro_g_1cm):.12e} J"
)

print()

print(
    "METER_SCALE_PRACTICAL_STATIC_DEC_ANTIGRAVITY="
    "NO_WITH_KNOWN_ENERGY_SCALES"
)

print(
    "MICROSCOPIC_DISTANCE_REDUCES_COST_AS_H_SQUARED=YES"
)

print(
    "NEGATIVE_ENERGY_NEEDED_FOR_THE_SIGN=NO"
)

print(
    "NEGATIVE_ENERGY_OR_MODIFIED_GRAVITY_NEEDED_TO_BEAT_THIS_BOUND="
    "LIKELY_UNDER_STATED_ASSUMPTIONS"
)

print(
    "BOUND_SCOPE="
    "STATIC_LINEARIZED_GR_TYPE_I_DEC_LOCALIZED_SOURCE"
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
    "DEC_BOUND_ESCAPE_ROUTES_QUANTUM_NEGATIVE_ENERGY_VS_MODIFIED_GRAVITY"
)
