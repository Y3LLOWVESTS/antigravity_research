"""Simulation 003A.

Question
--------

Can the positive-energy w=-1 source identified in Simulation 002 be
localized into a finite spherical region and directly matched to vacuum?

We test:

1. stress-energy conservation / TOV;
2. pressure at the proposed boundary;
3. metric-value matching;
4. metric-derivative matching;
5. compactness and horizon scale;
6. sign of the corresponding positive-mass exterior field.

This is a boundary-consistency diagnostic.

A full thin-shell Israel junction analysis is intentionally deferred until
the need for a shell has first been independently established.
"""

from __future__ import annotations

import csv
from pathlib import Path

from antigravity_research.geometry.kottler import C

from antigravity_research.geometry.vacuum_energy_core import (
    compactness,
    de_sitter_horizon_radius_m,
    de_sitter_metric_derivative_per_m,
    de_sitter_metric_f,
    enclosed_energy_mass_kg,
    schwarzschild_metric_derivative_per_m,
    schwarzschild_metric_f,
    tov_pressure_gradient_pa_per_m,
    vacuum_energy_density_for_rate,
    weak_field_exterior_acceleration_m_s2,
)


G0 = 9.80665

TARGETS = [
    ("micro_g_over_1m", 1.0e-6 * G0, 1.0),
    ("one_percent_g_over_1m", 1.0e-2 * G0, 1.0),
    ("one_g_over_1m", G0, 1.0),
]

CORE_RADII_M = [
    0.1,
    1.0,
    10.0,
    100.0,
]

rows = []

print(
    "=== SIMULATION 003A RESULTS ==="
)

print()

for (
    target_name,
    target_acceleration,
    target_separation,
) in TARGETS:

    rate = (
        target_acceleration
        / target_separation
    )

    epsilon = (
        vacuum_energy_density_for_rate(
            rate
        )
    )

    pressure = -epsilon

    horizon_radius = (
        de_sitter_horizon_radius_m(
            rate
        )
    )

    print(
        f"=== TARGET={target_name} ==="
    )

    print(
        f"RATE={rate:.12e} s^-2"
    )

    print(
        f"ENERGY_DENSITY={epsilon:.12e} J/m^3"
    )

    print(
        f"PRESSURE={pressure:.12e} Pa"
    )

    print(
        "INTERIOR_EOS=w=-1"
    )

    print(
        "INTERIOR_PRESSURE_NONZERO=YES"
    )

    print(
        f"DE_SITTER_HORIZON_RADIUS="
        f"{horizon_radius:.12e} m"
    )

    print()

    for radius in CORE_RADII_M:

        mass = enclosed_energy_mass_kg(
            radius,
            epsilon,
        )

        comp = compactness(
            radius,
            mass,
        )

        f_in = de_sitter_metric_f(
            radius,
            epsilon,
        )

        f_out = schwarzschild_metric_f(
            radius,
            mass,
        )

        df_in = (
            de_sitter_metric_derivative_per_m(
                radius,
                epsilon,
            )
        )

        df_out = (
            schwarzschild_metric_derivative_per_m(
                radius,
                mass,
            )
        )

        tov_gradient = (
            tov_pressure_gradient_pa_per_m(
                radius,
                mass,
                epsilon,
                pressure,
            )
        )

        surface_exterior_accel = (
            weak_field_exterior_acceleration_m_s2(
                radius,
                mass,
            )
        )

        exterior_2r_accel = (
            weak_field_exterior_acceleration_m_s2(
                2.0 * radius,
                mass,
            )
        )

        metric_value_error = abs(
            f_in - f_out
        )

        derivative_jump = (
            df_out - df_in
        )

        derivative_ratio = (
            df_in / df_out
            if df_out != 0.0
            else float("nan")
        )

        shell_required_diagnostic = (
            abs(derivative_jump) > 0.0
            and pressure != 0.0
        )

        rows.append({
            "target": target_name,
            "target_acceleration_m_s2":
                target_acceleration,
            "rate_s-2":
                rate,
            "core_radius_m":
                radius,
            "energy_density_j_m3":
                epsilon,
            "pressure_pa":
                pressure,
            "core_energy_mass_kg":
                mass,
            "compactness":
                comp,
            "de_sitter_horizon_radius_m":
                horizon_radius,
            "f_inside_boundary":
                f_in,
            "f_outside_boundary":
                f_out,
            "metric_value_abs_error":
                metric_value_error,
            "df_inside_per_m":
                df_in,
            "df_outside_per_m":
                df_out,
            "derivative_ratio_inside_outside":
                derivative_ratio,
            "derivative_jump_per_m":
                derivative_jump,
            "tov_pressure_gradient_pa_per_m":
                tov_gradient,
            "weak_exterior_accel_surface_m_s2":
                surface_exterior_accel,
            "weak_exterior_accel_2R_m_s2":
                exterior_2r_accel,
            "shell_required_diagnostic":
                shell_required_diagnostic,
        })

        print(
            f"CORE_RADIUS={radius:.6e} m"
        )

        print(
            f"  CORE_ENERGY_MASS={mass:.12e} kg"
        )

        print(
            f"  COMPACTNESS={comp:.12e}"
        )

        print(
            f"  F_INTERIOR_BOUNDARY={f_in:.15e}"
        )

        print(
            f"  F_EXTERIOR_BOUNDARY={f_out:.15e}"
        )

        print(
            "  METRIC_VALUE_MATCH="
            f"{'YES' if metric_value_error < 1e-12 else 'NO'}"
        )

        print(
            f"  DF_INTERIOR={df_in:.12e} m^-1"
        )

        print(
            f"  DF_EXTERIOR={df_out:.12e} m^-1"
        )

        print(
            f"  DERIVATIVE_RATIO={derivative_ratio:.12e}"
        )

        print(
            f"  TOV_DP_DR={tov_gradient:.12e} Pa/m"
        )

        print(
            "  W_MINUS_ONE_CAN_TAPER_SMOOTHLY="
            f"{'YES' if tov_gradient != 0.0 else 'NO'}"
        )

        print(
            "  EXTERIOR_ACCEL_AT_SURFACE="
            f"{surface_exterior_accel:.12e} m/s^2"
        )

        print(
            "  EXTERIOR_ACCEL_AT_2R="
            f"{exterior_2r_accel:.12e} m/s^2"
        )

        print(
            "  EXTERIOR_FIELD_DIRECTION="
            f"{'INWARD' if exterior_2r_accel < 0.0 else 'OUTWARD'}"
        )

        print(
            "  BOUNDARY_LAYER_REQUIRED_DIAGNOSTIC="
            f"{'YES' if shell_required_diagnostic else 'NO'}"
        )

        print()


# ============================================================
# Save data
# ============================================================

data_path = Path(
    "results/data/"
    "003a_finite_vacuum_energy_core.csv"
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
# Global logical checks
# ============================================================

all_tov_zero = all(
    row["tov_pressure_gradient_pa_per_m"] == 0.0
    for row in rows
)

all_metric_values_match = all(
    row["metric_value_abs_error"] < 1e-12
    for row in rows
)

all_derivatives_mismatch = all(
    row["derivative_jump_per_m"] != 0.0
    for row in rows
)

all_exteriors_inward = all(
    row["weak_exterior_accel_2R_m_s2"] < 0.0
    for row in rows
)

all_shell_diagnostics = all(
    row["shell_required_diagnostic"]
    for row in rows
)

print(
    "=== SIMULATION 003A SUMMARY ==="
)

print()

print(
    f"TOV_W_MINUS_ONE_DP_DR_ZERO="
    f"{'YES' if all_tov_zero else 'NO'}"
)

print(
    "PURE_W_MINUS_ONE_SMOOTH_LOCALIZATION="
    f"{'NO' if all_tov_zero else 'UNRESOLVED'}"
)

print(
    "INTERIOR_EXTERIOR_METRIC_VALUE_MATCH="
    f"{'YES' if all_metric_values_match else 'NO'}"
)

print(
    "INTERIOR_EXTERIOR_DERIVATIVE_MATCH="
    f"{'NO' if all_derivatives_mismatch else 'UNRESOLVED'}"
)

print(
    "BOUNDARY_LAYER_REQUIRED_DIAGNOSTIC="
    f"{'YES' if all_shell_diagnostics else 'UNRESOLVED'}"
)

print(
    "POSITIVE_ENERGY_CORE_EXTERIOR_FIELD="
    f"{'INWARD' if all_exteriors_inward else 'MIXED'}"
)

print(
    "INTERIOR_DEFOCUSING_IMPLIES_EXTERNAL_REPULSION="
    "NO"
)

print(
    "FINITE_REPULSIVE_DEVICE_ESTABLISHED="
    "NO"
)

print(
    f"DATA={data_path}"
)

print()

print(
    "NEXT="
    "ISRAEL_JUNCTION_SHELL_STRESS_AND_EXTERNAL_MASS_SEARCH"
)
