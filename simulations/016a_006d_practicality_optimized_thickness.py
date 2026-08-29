r"""016A — 006D practicality-optimized finite-thickness gate.

PURPOSE
-------
Revisit the 006D finite positive-energy linearized-GR repulsion architecture
using a practical multi-objective criterion rather than minimizing only total
energy coefficient C.

The original finite-thickness sequence approached the thin conserved limit
monotonically.  That improves total energy only modestly while making the
outer support transition and finite vertical profile increasingly sharp.

This gate reconstructs the exact radial stress profiles and asks:

1. How much peak stress is paid to reduce C?
2. Is a thicker 006D realization a much better physical target?
3. Does microscopic standoff really rescue a macroscopic device?
4. Which thickness should be taken into a charged/gauged field-theory
   realization attempt?

SCIENTIFIC SCOPE
----------------
This is an analytical/numerical design gate inside the existing static
linearized-GR 006D construction.

It does not establish:
- exact nonlinear GR;
- a stable soliton;
- a known material;
- a practical device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_006D_MULTI_OBJECTIVE_REALIZABILITY_PREFLIGHT
"""

from __future__ import annotations

import math

import numpy as np


G = 6.67430e-11
C_LIGHT = 299_792_458.0
G_STANDARD = 9.80665

ALPHA = 1.437500564637
BETA = 4.701437405300

EV4_TO_J_M3 = 20.852156864043042
EV3_TO_J_M2 = 4.114693148808747e-6

FINITE_CASES = (
    (0.40000, 11.369718516276, 0.149453529535, 38.037638025730),
    (0.20000, 11.233723934208, 0.190019680852, 29.559369544823),
    (0.10000, 11.165255241660, 0.212604998246, 26.258214373557),
    (0.05000, 11.130897375158, 0.224509078286, 24.789414887263),
    (0.02500, 11.113686825672, 0.230618147495, 24.095429926871),
    (0.01250, 11.105073553053, 0.233712433325, 23.757986246352),
    (0.00625, 11.100764905398, 0.235269573750, 23.591586299249),
)

C_THIN = 23.426710175391

FIXED_CHARGE_TMAX_OVER_E = 0.186185265139
FIXED_CHARGE_CRITICAL_OVER_E = 0.125
GAUGE_TAKEOVER_CRITICAL_FRACTION = 0.383694

H_SCAN_M = (
    1.0,
    1.0e-1,
    1.0e-2,
    1.0e-3,
    1.0e-6,
    1.0e-9,
    1.0e-10,
    1.0e-12,
    1.0e-15,
)


def smoothstep(u: np.ndarray) -> np.ndarray:
    return u * u * (3.0 - 2.0 * u)


def smoothstep_prime(u: np.ndarray) -> np.ndarray:
    return 6.0 * u * (1.0 - u)


def radial_profiles(
    x: np.ndarray,
    delta: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return epsilon, p_r, p_phi for exact normalized 006D profile."""

    inner_width = delta / 4.0
    outer_width = delta

    x_minus = ALPHA - inner_width
    x_plus = ALPHA + inner_width
    x_max = BETA + outer_width

    q = np.zeros_like(x)
    qp = np.zeros_like(x)

    core = x < x_minus

    q[core] = -x[core]
    qp[core] = -1.0

    transition = (
        (x >= x_minus)
        & (x <= x_plus)
    )

    if np.any(transition):
        xt = x[transition]

        u = (
            (xt - x_minus)
            / (x_plus - x_minus)
        )

        s = smoothstep(u)
        sp = (
            smoothstep_prime(u)
            / (x_plus - x_minus)
        )

        q_core = -xt
        qp_core = -np.ones_like(xt)

        q_ann = -(ALPHA * ALPHA) / xt
        qp_ann = (ALPHA * ALPHA) / (xt * xt)

        q[transition] = (
            (1.0 - s) * q_core
            + s * q_ann
        )

        qp[transition] = (
            (1.0 - s) * qp_core
            + s * qp_ann
            + sp * (q_ann - q_core)
        )

    annulus = (
        (x > x_plus)
        & (x < BETA)
    )

    if np.any(annulus):
        xa = x[annulus]

        q[annulus] = (
            -(ALPHA * ALPHA)
            / xa
        )

        qp[annulus] = (
            (ALPHA * ALPHA)
            / (xa * xa)
        )

    collar = (
        (x >= BETA)
        & (x <= x_max)
    )

    if np.any(collar):
        xc = x[collar]

        v = (
            (xc - BETA)
            / outer_width
        )

        s = smoothstep(v)
        sp = (
            smoothstep_prime(v)
            / outer_width
        )

        q_ann = (
            -(ALPHA * ALPHA)
            / xc
        )

        qp_ann = (
            (ALPHA * ALPHA)
            / (xc * xc)
        )

        q[collar] = (
            (1.0 - s)
            * q_ann
        )

        qp[collar] = (
            (1.0 - s)
            * qp_ann
            - sp * q_ann
        )

    p_r = np.zeros_like(x)

    positive_x = x > 0.0

    p_r[positive_x] = (
        q[positive_x]
        / x[positive_x]
    )

    p_r[~positive_x] = -1.0

    p_phi = qp

    epsilon = np.maximum(
        np.abs(p_r),
        np.abs(p_phi),
    )

    return (
        epsilon,
        p_r,
        p_phi,
    )


def max_surface_epsilon(delta: float) -> float:
    """Resolve maximum dimensionless surface-profile energy density."""

    x_max = BETA + delta

    x = np.linspace(
        0.0,
        x_max,
        1_000_001,
        dtype=float,
    )

    epsilon, _, _ = radial_profiles(
        x,
        delta,
    )

    return float(
        np.max(
            epsilon
        )
    )


def required_surface_energy(
    field_factor: float,
) -> float:
    """Return U0 in J/m^2 for 1g at target."""

    return (
        G_STANDARD
        * C_LIGHT**2
        / (
            2.0
            * math.pi
            * G
            * field_factor
        )
    )


def qft_volume_scale_gev(
    energy_density_j_m3: float,
) -> float:
    """Fourth-root energy scale associated with energy density."""

    ev = (
        energy_density_j_m3
        / EV4_TO_J_M3
    ) ** 0.25

    return ev / 1.0e9


def surface_tension_scale_gev(
    surface_energy_j_m2: float,
) -> float:
    """Cube-root natural-unit scale associated with wall tension."""

    ev = (
        surface_energy_j_m2
        / EV3_TO_J_M2
    ) ** (1.0 / 3.0)

    return ev / 1.0e9


def main() -> None:
    print(
        "=== 016A — 006D PRACTICALITY-OPTIMIZED "
        "THICKNESS GATE ==="
    )

    rows: list[dict[str, float]] = []

    for (
        delta,
        mass_factor,
        field_factor,
        coefficient,
    ) in FINITE_CASES:
        eps_max = max_surface_epsilon(
            delta
        )

        vertical_peak = (
            1.875
            / delta
        )

        U0 = required_surface_energy(
            field_factor
        )

        peak_prefactor = (
            U0
            * eps_max
            * vertical_peak
        )

        x_max = (
            BETA
            + delta
        )

        min_feature_fraction = (
            delta
            / 4.0
        )

        mass_per_covered_area = (
            coefficient
            * G_STANDARD
            / (
                math.pi
                * x_max**2
                * G
            )
        )

        energy_per_covered_area = (
            mass_per_covered_area
            * C_LIGHT**2
        )

        sigma_scale = (
            surface_tension_scale_gev(
                U0
            )
        )

        rows.append(
            {
                "delta":
                    delta,
                "mass_factor":
                    mass_factor,
                "field_factor":
                    field_factor,
                "C":
                    coefficient,
                "eps_max":
                    eps_max,
                "vertical_peak":
                    vertical_peak,
                "U0":
                    U0,
                "peak_prefactor":
                    peak_prefactor,
                "x_max":
                    x_max,
                "min_feature_fraction":
                    min_feature_fraction,
                "mass_per_area":
                    mass_per_covered_area,
                "energy_per_area":
                    energy_per_covered_area,
                "sigma_scale_gev":
                    sigma_scale,
            }
        )

    thin = rows[-1]

    print()
    print(
        "=== EXACT MULTIOBJECTIVE THICKNESS TABLE ==="
    )

    for row in rows:
        c_penalty = (
            row["C"]
            / thin["C"]
        )

        peak_relief = (
            thin["peak_prefactor"]
            / row["peak_prefactor"]
        )

        feature_relief = (
            row["min_feature_fraction"]
            / thin["min_feature_fraction"]
        )

        print(
            "CASE "
            f"DELTA={row['delta']:.8f} "
            f"C={row['C']:.12f} "
            f"C_OVER_FINE={c_penalty:.12f} "
            f"PEAK_STRESS_RELIEF={peak_relief:.12f} "
            f"FEATURE_WIDTH_GAIN={feature_relief:.12f} "
            f"U0_J_M2={row['U0']:.12e} "
            f"WALL_TENSION_SCALE_GEV="
            f"{row['sigma_scale_gev']:.9f} "
            f"PEAK_DENSITY_PREFACTOR_J_M2="
            f"{row['peak_prefactor']:.12e} "
            f"ENERGY_PER_COVERED_M2_J="
            f"{row['energy_per_area']:.12e}"
        )

    print()
    print(
        "=== KEY TRADEOFFS ==="
    )

    by_delta = {
        row["delta"]:
            row
        for row in rows
    }

    for candidate_delta in (
        0.10,
        0.20,
        0.40,
    ):
        row = by_delta[
            candidate_delta
        ]

        print(
            "AUGMENTATION "
            f"DELTA={candidate_delta:.2f} "
            f"C_PENALTY_PERCENT="
            f"{100.0 * (row['C']/thin['C'] - 1.0):.6f} "
            f"PEAK_STRESS_REDUCTION_FACTOR="
            f"{thin['peak_prefactor']/row['peak_prefactor']:.6f} "
            f"MIN_FEATURE_WIDTH_GAIN="
            f"{row['min_feature_fraction']/thin['min_feature_fraction']:.6f}"
        )

    print()
    print(
        "=== PROJECT STABILITY / GAUGE INPUTS ==="
    )

    print(
        "FIXED_CHARGE_TMAX_OVER_E="
        f"{FIXED_CHARGE_TMAX_OVER_E:.12f}"
    )

    print(
        "FIXED_CHARGE_CRITICAL_OVER_E="
        f"{FIXED_CHARGE_CRITICAL_OVER_E:.12f}"
    )

    print(
        "FIXED_CHARGE_STABILITY_CAPACITY_RATIO="
        f"{FIXED_CHARGE_TMAX_OVER_E/FIXED_CHARGE_CRITICAL_OVER_E:.12f}"
    )

    print(
        "GAUGE_TAKEOVER_CRITICAL_FRACTION="
        f"{GAUGE_TAKEOVER_CRITICAL_FRACTION:.12f}"
    )

    print()
    print(
        "=== MICROSTANDOFF SCALE MAP ==="
    )

    for candidate_delta in (
        0.10,
        0.20,
    ):
        row = by_delta[
            candidate_delta
        ]

        print()
        print(
            "CANDIDATE_DELTA="
            f"{candidate_delta:.2f}"
        )

        for h in H_SCAN_M:
            point_mass = (
                row["C"]
                * G_STANDARD
                * h**2
                / G
            )

            point_energy = (
                point_mass
                * C_LIGHT**2
            )

            peak_density = (
                row["peak_prefactor"]
                / h
            )

            min_feature = (
                row["min_feature_fraction"]
                * h
            )

            source_radius = (
                row["x_max"]
                * h
            )

            qft_scale = (
                qft_volume_scale_gev(
                    peak_density
                )
            )

            print(
                "SCALE "
                f"H_M={h:.12e} "
                f"POINT_TARGET_SOURCE_MASS_KG="
                f"{point_mass:.12e} "
                f"POINT_TARGET_SOURCE_ENERGY_J="
                f"{point_energy:.12e} "
                f"SOURCE_RADIUS_M="
                f"{source_radius:.12e} "
                f"MIN_FEATURE_M="
                f"{min_feature:.12e} "
                f"PEAK_ENERGY_DENSITY_J_M3="
                f"{peak_density:.12e} "
                f"PEAK_QFT_SCALE_GEV="
                f"{qft_scale:.9f}"
            )

    print()
    print(
        "=== MACROSCOPIC COVERAGE NO-FREE-LUNCH CHECK ==="
    )

    for candidate_delta in (
        0.00625,
        0.10,
        0.20,
    ):
        row = by_delta[
            candidate_delta
        ]

        print(
            "COVERAGE "
            f"DELTA={candidate_delta:.5f} "
            f"MASS_EQUIVALENT_PER_COVERED_M2_KG="
            f"{row['mass_per_area']:.12e} "
            f"ENERGY_PER_COVERED_M2_J="
            f"{row['energy_per_area']:.12e} "
            "H_DEPENDENCE=NONE_FOR_GEOMETRIC_TILING"
        )

    print()
    print(
        "=== DECISION ==="
    )

    d01 = by_delta[
        0.10
    ]

    d02 = by_delta[
        0.20
    ]

    print(
        "THIN_LIMIT_IS_BEST_PRACTICAL_REALIZATION_TARGET="
        "NO"
    )

    print(
        "DELTA_0P10_C_PENALTY_PERCENT="
        f"{100.0*(d01['C']/thin['C']-1.0):.6f}"
    )

    print(
        "DELTA_0P10_PEAK_STRESS_RELIEF="
        f"{thin['peak_prefactor']/d01['peak_prefactor']:.6f}"
    )

    print(
        "DELTA_0P20_C_PENALTY_PERCENT="
        f"{100.0*(d02['C']/thin['C']-1.0):.6f}"
    )

    print(
        "DELTA_0P20_PEAK_STRESS_RELIEF="
        f"{thin['peak_prefactor']/d02['peak_prefactor']:.6f}"
    )

    print(
        "PREFERRED_006D_AUGMENTATION="
        "THICK_DELTA_0P10_TO_0P20_"
        "DOMAIN_WALL_CORE_PLUS_FIXED_CHARGE_"
        "GAUGE_COMPENSATED_COLLAR"
    )

    print(
        "DYNAMIC_STABILITY_TARGET="
        "CHARGED_GAUGED_SOLITON_NOT_ARBITRARY_STRESS"
    )

    print(
        "PURE_GR_MICROSTANDOFF_SOLVES_MACROSCOPIC_AREA_ENERGY="
        "NO"
    )

    print(
        "NEXT_IF_FIELD_REALIZATION_IS_PURSUED="
        "016B_GLOBAL_SMOOTH_CHARGED_GAUGE_"
        "SOLITON_BOUNDARY_VALUE_PROBLEM_AT_DELTA_0P10_AND_0P20"
    )

    print(
        "NEXT_REQUIRED_OPERATIONAL_GATE="
        "FINITE_PAYLOAD_CENTER_OF_MASS_ACCELERATION"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_006D_MULTI_OBJECTIVE_"
        "REALIZABILITY_PREFLIGHT"
    )


if __name__ == "__main__":
    main()
