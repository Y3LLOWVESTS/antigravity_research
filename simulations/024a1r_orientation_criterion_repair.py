"""024A1R — orientation-criterion repair for the fixed-field sextic gate.

PURPOSE
-------
Repair the interpretation of Simulation 024A1 before its worst-direction
result is used to close the direct sextic-placement route.

SCIENTIFIC QUESTION
-------------------
024A1 required an additive positive sextic sector to improve acceleration per
energy in the worst of 320 payload orientations.

Is that a fair promotion criterion for a positive active-source addition, or
is failure structurally forced by spherical kernel geometry?

THEORY
------
For a point payload centered at c = h n and source point x,

    K(x;n) = (x.n - h) / |x - h n|^3.

The orientation average satisfies the shell-theorem identity

    <1/|x-h n|>_n = 1/max(r,h).

Differentiating with respect to h gives

    <K>_n = -1/h^2    for r < h
             0         for r > h.

Thus a nonnegative added active source cannot provide a positive increment in
every payload orientation.

The repository finite-payload kernel is

    K_P = (x.n-h) / max(|x-h n|^3, R_P^3).

This file independently verifies numerically that its spherical orientation
average is also non-positive for the 024A1 payload geometry.

FIXED-ORIENTATION OBSERVABLE
----------------------------
For each saved orientation,

    eta0 = A0/E0

    G6 = 4 L6 / eta0.

For frozen-field added sextic energy fraction lambda = E6/E0,

    eta(lambda)/eta0
    =
    (1 + lambda G6)/(1 + lambda).

Therefore G6 > 1 is the exact infinitesimal efficiency-improvement condition
for one fixed orientation.

AXES TESTED
-----------
1. TRUSTED_INT15_AXIS
   Fixed before 024A1.

2. BASELINE_MAX_AXIS
   Selected using A0 only, without examining L6.

3. BASELINE_MIN_AXIS
   Retained as the robust worst-direction diagnostic.

4. SEXTIC_MAX_GAIN_AXIS_EXPLORATORY
   Reported only as exploratory information.

PROMOTION LOGIC
---------------
The all-320 additive-improvement criterion is retired as a universal promotion
condition for a nonnegative added active sector.

If the trusted axis or baseline-selected maximum-response axis has G6 > 1,
the direct sextic route remains open for an orientation-locked reduced
re-equilibration prefilter.

No result here authorizes a large generalized 3D PDE solve.

INPUTS
------
results/data/024a1_sextic_fixed_field_orientation_arrays.npz
results/data/024a1_sextic_fixed_field_kernel_placement_summary.json

OUTPUTS
-------
results/data/024a1r_orientation_criterion_repair_summary.json
results/data/024a1r_orientation_axis_metrics.csv

ASSUMPTIONS / LIMITATIONS
-------------------------
- fixed existing fields;
- linearized-GR payload observable;
- no generalized-field re-equilibration;
- no orientation-control energy;
- no stability conclusion;
- no nonlinear Einstein-matter conclusion;
- no practical-device claim.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_024A1R_ORIENTATION_CRITERION_REPAIR
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results/data"

IN_NPZ = DATA / "024a1_sextic_fixed_field_orientation_arrays.npz"
IN_JSON = DATA / "024a1_sextic_fixed_field_kernel_placement_summary.json"

OUT_JSON = DATA / "024a1r_orientation_criterion_repair_summary.json"
OUT_CSV = DATA / "024a1r_orientation_axis_metrics.csv"

TRUSTED_INT15_DIRECTION = np.array(
    [
        -0.45435018446379805,
        +0.01878880658050992,
        +0.8906249999999961,
    ],
    dtype=float,
)
TRUSTED_INT15_DIRECTION /= np.linalg.norm(TRUSTED_INT15_DIRECTION)

DIAGNOSTIC_LAMBDAS = np.array(
    [
        1.0e-4,
        1.0e-3,
        3.0e-3,
        1.0e-2,
        3.0e-2,
        1.0e-1,
    ]
)


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def finite_payload_orientation_average(
    radius: float,
    h: float,
    payload_radius: float,
    mu: np.ndarray,
    weights: np.ndarray,
) -> float:
    """Return the spherical orientation average of the payload kernel."""
    d2 = (
        radius * radius
        + h * h
        - 2.0 * radius * h * mu
    )

    distance = np.sqrt(np.maximum(d2, 0.0))

    denominator = np.maximum(
        distance**3,
        payload_radius**3,
    )

    kernel = (
        radius * mu - h
    ) / denominator

    return float(
        0.5
        * np.sum(
            weights * kernel
        )
    )


def point_payload_average_analytic(
    radius: float,
    h: float,
) -> float:
    """Return the shell-theorem result away from radius=h."""
    if radius < h:
        return -1.0 / h**2

    if radius > h:
        return 0.0

    return float("nan")


def gain_array(
    acceleration: np.ndarray,
    sextic_leverage: np.ndarray,
    energy: float,
) -> np.ndarray:
    """Return orientation-dependent infinitesimal sextic efficiency gain."""
    acceleration = np.asarray(
        acceleration,
        dtype=float,
    )

    sextic_leverage = np.asarray(
        sextic_leverage,
        dtype=float,
    )

    if np.any(acceleration <= 0.0):
        raise RuntimeError(
            "Saved 024A1 baseline is not outward in all directions"
        )

    baseline_efficiency = (
        acceleration
        / float(energy)
    )

    return (
        4.0
        * sextic_leverage
        / baseline_efficiency
    )


def axis_row(
    source: str,
    axis_name: str,
    index: int,
    directions: np.ndarray,
    acceleration: np.ndarray,
    sextic_leverage: np.ndarray,
    gain: np.ndarray,
) -> dict:
    """Build one auditable fixed-axis result row."""
    direction = directions[index]

    row = {
        "source": source,
        "axis": axis_name,
        "index": int(index),
        "nx": float(direction[0]),
        "ny": float(direction[1]),
        "nz": float(direction[2]),
        "A0": float(acceleration[index]),
        "L6": float(sextic_leverage[index]),
        "G6": float(gain[index]),
        "infinitesimal_efficiency_improves": (
            "YES"
            if gain[index] > 1.0
            else "NO"
        ),
    }

    for lam in DIAGNOSTIC_LAMBDAS:
        ratio = (
            1.0
            + lam * gain[index]
        ) / (
            1.0 + lam
        )

        row[
            f"eta_ratio_lambda_{lam:.0e}"
        ] = float(ratio)

    return row


def analyze_source(
    source: str,
    directions: np.ndarray,
    acceleration: np.ndarray,
    sextic_leverage: np.ndarray,
    energy: float,
) -> tuple[dict, list[dict]]:
    """Evaluate the repaired fixed-orientation criteria."""
    gain = gain_array(
        acceleration,
        sextic_leverage,
        energy,
    )

    trusted_index = int(
        np.argmax(
            directions
            @ TRUSTED_INT15_DIRECTION
        )
    )

    baseline_max_index = int(
        np.argmax(acceleration)
    )

    baseline_min_index = int(
        np.argmin(acceleration)
    )

    sextic_max_index = int(
        np.argmax(gain)
    )

    rows = [
        axis_row(
            source,
            "TRUSTED_INT15_AXIS",
            trusted_index,
            directions,
            acceleration,
            sextic_leverage,
            gain,
        ),
        axis_row(
            source,
            "BASELINE_MAX_AXIS",
            baseline_max_index,
            directions,
            acceleration,
            sextic_leverage,
            gain,
        ),
        axis_row(
            source,
            "BASELINE_MIN_AXIS",
            baseline_min_index,
            directions,
            acceleration,
            sextic_leverage,
            gain,
        ),
        axis_row(
            source,
            "SEXTIC_MAX_GAIN_AXIS_EXPLORATORY",
            sextic_max_index,
            directions,
            acceleration,
            sextic_leverage,
            gain,
        ),
    ]

    top10_threshold = float(
        np.quantile(
            acceleration,
            0.90,
        )
    )

    top25_threshold = float(
        np.quantile(
            acceleration,
            0.75,
        )
    )

    top10 = (
        acceleration
        >= top10_threshold
    )

    top25 = (
        acceleration
        >= top25_threshold
    )

    summary = {
        "E": float(energy),
        "orientation_count": int(
            len(acceleration)
        ),
        "mean_L6": float(
            np.mean(sextic_leverage)
        ),
        "min_G6": float(
            np.min(gain)
        ),
        "median_G6": float(
            np.median(gain)
        ),
        "max_G6": float(
            np.max(gain)
        ),
        "fraction_G6_gt_1": float(
            np.mean(gain > 1.0)
        ),
        "fraction_L6_positive": float(
            np.mean(
                sextic_leverage > 0.0
            )
        ),
        "corr_A0_L6": float(
            np.corrcoef(
                acceleration,
                sextic_leverage,
            )[0, 1]
        ),
        "corr_A0_G6": float(
            np.corrcoef(
                acceleration,
                gain,
            )[0, 1]
        ),
        "trusted_direction_nearest_dot": float(
            directions[trusted_index]
            @ TRUSTED_INT15_DIRECTION
        ),
        "trusted_axis_G6": float(
            gain[trusted_index]
        ),
        "baseline_max_axis_G6": float(
            gain[
                baseline_max_index
            ]
        ),
        "baseline_min_axis_G6": float(
            gain[
                baseline_min_index
            ]
        ),
        "sextic_selected_max_G6": float(
            gain[
                sextic_max_index
            ]
        ),
        "sextic_selected_max_G6_baseline_fraction_of_max": float(
            acceleration[
                sextic_max_index
            ]
            / np.max(acceleration)
        ),
        "top10_baseline_fraction_G6_gt_1": float(
            np.mean(
                gain[top10] > 1.0
            )
        ),
        "top25_baseline_fraction_G6_gt_1": float(
            np.mean(
                gain[top25] > 1.0
            )
        ),
        "trusted_axis_improves": bool(
            gain[
                trusted_index
            ] > 1.0
        ),
        "baseline_max_axis_improves": bool(
            gain[
                baseline_max_index
            ] > 1.0
        ),
        "some_orientation_improves": bool(
            np.any(
                gain > 1.0
            )
        ),
    }

    if (
        summary[
            "trusted_axis_improves"
        ]
        and summary[
            "baseline_max_axis_improves"
        ]
    ):
        classification = (
            "GREEN_TWO_NON_SEXTIC_SELECTED_AXES"
        )

    elif (
        summary[
            "trusted_axis_improves"
        ]
        or summary[
            "baseline_max_axis_improves"
        ]
    ):
        classification = (
            "YELLOW_ONE_NON_SEXTIC_SELECTED_AXIS"
        )

    elif summary[
        "some_orientation_improves"
    ]:
        classification = (
            "YELLOW_ONLY_SEXTIC_SELECTED_NARROW_SECTORS"
        )

    else:
        classification = (
            "RED_NO_FIXED_ORIENTATION_GAIN_FOUND"
        )

    summary[
        "fixed_orientation_classification"
    ] = classification

    return summary, rows


def main() -> None:
    require(IN_NPZ)
    require(IN_JSON)

    with IN_JSON.open() as handle:
        old_summary = json.load(
            handle
        )

    with np.load(
        IN_NPZ,
        allow_pickle=False,
    ) as data:
        directions = np.asarray(
            data["directions"],
            dtype=float,
        )

        exact_A = np.asarray(
            data["exact_high_A0"],
            dtype=float,
        )

        exact_L6 = np.asarray(
            data["exact_high_L6"],
            dtype=float,
        )

        n65_A = np.asarray(
            data["n65_A0"],
            dtype=float,
        )

        n65_L6 = np.asarray(
            data["n65_L6"],
            dtype=float,
        )

    direction_norm_error = float(
        np.max(
            np.abs(
                np.linalg.norm(
                    directions,
                    axis=1,
                )
                - 1.0
            )
        )
    )

    if (
        direction_norm_error
        > 1.0e-12
    ):
        raise RuntimeError(
            "Direction normalization changed"
        )

    h = float(
        old_summary[
            "payload"
        ][
            "center_radius"
        ]
    )

    payload_radius = float(
        old_summary[
            "payload"
        ][
            "payload_radius"
        ]
    )

    exact_energy = float(
        old_summary[
            "exact_levels"
        ][
            "HIGH"
        ][
            "E"
        ]
    )

    n65_energy = float(
        old_summary[
            "n65"
        ][
            "E"
        ]
    )

    print(
        "=== 024A1R — "
        "ORIENTATION-CRITERION REPAIR ==="
    )

    print(
        f"PAYLOAD_CENTER_RADIUS="
        f"{h:.15e}"
    )

    print(
        f"PAYLOAD_RADIUS="
        f"{payload_radius:.15e}"
    )

    print(
        f"DIRECTION_NORM_MAX_ERROR="
        f"{direction_norm_error:.15e}"
    )

    print(
        "\n=== A — ANALYTIC "
        "POINT-PAYLOAD ORIENTATION "
        "AVERAGE ==="
    )

    print(
        "POINT_PAYLOAD_AVG_KERNEL_R_LT_H="
        "-1_OVER_H_SQUARED"
    )

    print(
        "POINT_PAYLOAD_AVG_KERNEL_R_GT_H="
        "ZERO"
    )

    print(
        "NONNEGATIVE_ADDED_ACTIVE_SOURCE_"
        "ALL_ORIENTATION_POSITIVE_INCREMENT="
        "IMPOSSIBLE_POINT_PAYLOAD"
    )

    mu, weights = leggauss(
        2048
    )

    radius_grid = np.unique(
        np.concatenate(
            [
                np.linspace(
                    0.0,
                    2.0 * h,
                    321,
                ),
                h
                + np.linspace(
                    -2.0
                    * payload_radius,
                    +2.0
                    * payload_radius,
                    161,
                ),
            ]
        )
    )

    radius_grid = radius_grid[
        radius_grid >= 0.0
    ]

    finite_average = np.array(
        [
            finite_payload_orientation_average(
                float(radius),
                h,
                payload_radius,
                mu,
                weights,
            )
            for radius
            in radius_grid
        ],
        dtype=float,
    )

    finite_scaled_min = float(
        np.min(
            finite_average
        )
        * h**2
    )

    finite_scaled_max = float(
        np.max(
            finite_average
        )
        * h**2
    )

    finite_nonpositive = bool(
        finite_scaled_max
        <= 5.0e-8
    )

    print(
        "FINITE_PAYLOAD_AVG_KERNEL_"
        f"SCALED_MIN="
        f"{finite_scaled_min:.15e}"
    )

    print(
        "FINITE_PAYLOAD_AVG_KERNEL_"
        f"SCALED_MAX="
        f"{finite_scaled_max:.15e}"
    )

    print(
        "FINITE_PAYLOAD_ORIENTATION_"
        "AVERAGE_NONPOSITIVE_NUMERIC="
        + (
            "PASS"
            if finite_nonpositive
            else "FAIL"
        )
    )

    point_samples = [
        0.25 * h,
        0.50 * h,
        0.90 * h,
        1.10 * h,
        1.50 * h,
    ]

    point_error = 0.0

    for radius in point_samples:
        d2 = (
            radius**2
            + h**2
            - 2.0
            * radius
            * h
            * mu
        )

        distance = np.sqrt(
            np.maximum(
                d2,
                1.0e-300,
            )
        )

        kernel = (
            radius * mu - h
        ) / distance**3

        numerical = float(
            0.5
            * np.sum(
                weights * kernel
            )
        )

        analytical = (
            point_payload_average_analytic(
                radius,
                h,
            )
        )

        error = (
            abs(
                numerical
                - analytical
            )
            * h**2
        )

        point_error = max(
            point_error,
            error,
        )

    point_pass = bool(
        point_error
        <= 2.0e-8
    )

    print(
        "POINT_PAYLOAD_THEOREM_"
        f"MAX_SCALED_ABSERR="
        f"{point_error:.15e}"
    )

    print(
        "POINT_PAYLOAD_THEOREM_"
        "NUMERIC_CHECK="
        + (
            "PASS"
            if point_pass
            else "FAIL"
        )
    )

    print(
        "\n=== B — SAVED 024A1 "
        "AXIS REINTERPRETATION ==="
    )

    exact_summary, exact_rows = (
        analyze_source(
            "EXACT_HIGH",
            directions,
            exact_A,
            exact_L6,
            exact_energy,
        )
    )

    n65_summary, n65_rows = (
        analyze_source(
            "N65",
            directions,
            n65_A,
            n65_L6,
            n65_energy,
        )
    )

    for name, result in (
        (
            "EXACT_HIGH",
            exact_summary,
        ),
        (
            "N65",
            n65_summary,
        ),
    ):
        print(
            f"\n--- {name} ---"
        )

        for key in (
            "mean_L6",
            "min_G6",
            "median_G6",
            "max_G6",
            "fraction_G6_gt_1",
            "corr_A0_L6",
            "corr_A0_G6",
            "trusted_axis_G6",
            "baseline_max_axis_G6",
            "baseline_min_axis_G6",
            "sextic_selected_max_G6",
            "sextic_selected_max_G6_baseline_fraction_of_max",
            "top10_baseline_fraction_G6_gt_1",
            "top25_baseline_fraction_G6_gt_1",
        ):
            print(
                f"{name}_{key.upper()}="
                f"{result[key]:.15e}"
            )

        print(
            f"{name}_FIXED_ORIENTATION_"
            "CLASSIFICATION="
            f"{result['fixed_orientation_classification']}"
        )

    rows = (
        exact_rows
        + n65_rows
    )

    with OUT_CSV.open(
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

    print(
        "\n=== C — AXIS DETAILS ==="
    )

    for row in rows:
        print(
            f"{row['source']} "
            f"{row['axis']} "
            f"INDEX={row['index']} "
            f"A0={row['A0']:.12e} "
            f"L6={row['L6']:.12e} "
            f"G6={row['G6']:.12e} "
            "IMPROVES="
            f"{row['infinitesimal_efficiency_improves']}"
        )

    n65_preselected = bool(
        n65_summary[
            "trusted_axis_improves"
        ]
        or n65_summary[
            "baseline_max_axis_improves"
        ]
    )

    exact_preselected = bool(
        exact_summary[
            "trusted_axis_improves"
        ]
        or exact_summary[
            "baseline_max_axis_improves"
        ]
    )

    if (
        n65_preselected
        and exact_preselected
    ):
        decision = (
            "GREEN_ORIENTATION_LOCKED_SIGNAL_"
            "IN_BOTH_REFERENCES"
        )

        next_action = (
            "024A2_ORIENTATION_LOCKED_"
            "DIELECTRIC_SEXTIC_REDUCED_PREFILTER"
        )

    elif n65_preselected:
        decision = (
            "GREEN_N65_ORIENTATION_LOCKED_SIGNAL_"
            "EXACT_MAP_MIXED"
        )

        next_action = (
            "024A2_N65_SEEDED_ORIENTATION_LOCKED_"
            "DIELECTRIC_PREFILTER"
        )

    elif exact_preselected:
        decision = (
            "YELLOW_EXACT_ORIENTATION_LOCKED_SIGNAL_"
            "N65_NOT_PRESELECTED"
        )

        next_action = (
            "024A2_DIELECTRIC_SEXTIC_PLACEMENT_"
            "ORACLE_BEFORE_REEQUILIBRATION"
        )

    elif (
        exact_summary[
            "some_orientation_improves"
        ]
        or n65_summary[
            "some_orientation_improves"
        ]
    ):
        decision = (
            "YELLOW_NARROW_SEXTIC_SELECTED_"
            "ORIENTATION_SIGNAL_ONLY"
        )

        next_action = (
            "024A2_DIELECTRIC_SEXTIC_"
            "PLACEMENT_ORACLE"
        )

    else:
        decision = (
            "RED_NO_ORIENTATION_LOCKED_"
            "FIXED_FIELD_GAIN"
        )

        next_action = (
            "024A2_GEOMETRY_REORGANIZING_"
            "ADDITIONAL_FIELD_PREFILTER"
        )

    repaired_summary = {
        "claim_classification":
            "PROJECT_DERIVED_024A1R_"
            "ORIENTATION_CRITERION_REPAIR",

        "point_payload_orientation_average_theorem": {
            "r_lt_h":
                "-1/h^2",
            "r_gt_h":
                "0",
            "all_orientation_positive_increment_for_nonnegative_active_addition":
                False,
            "numeric_max_scaled_abs_error":
                point_error,
            "numeric_check_pass":
                point_pass,
        },

        "finite_payload_orientation_average_numeric": {
            "scaled_min":
                finite_scaled_min,
            "scaled_max":
                finite_scaled_max,
            "nonpositive_pass":
                finite_nonpositive,
            "quadrature_n":
                2048,
        },

        "old_024a1_decision":
            old_summary.get(
                "decision"
            ),

        "old_024a1_worst_direction_result_retained_as_robustness_diagnostic":
            True,

        "old_all_orientation_improvement_promotion_condition_retired":
            bool(
                point_pass
                and finite_nonpositive
            ),

        "exact_high":
            exact_summary,

        "n65":
            n65_summary,

        "corrected_decision":
            decision,

        "next":
            next_action,

        "large_generalized_3d_pde_scan_authorized":
            False,

        "current_knowledge_heuristic":
            "APPROXIMATELY_70_TO_71_PERCENT_NOT_A_PROBABILITY",

        "practical_antigravity_device":
            False,

        "new_physics_discovery":
            False,
    }

    with OUT_JSON.open(
        "w"
    ) as handle:
        json.dump(
            repaired_summary,
            handle,
            indent=2,
            sort_keys=True,
        )

        handle.write(
            "\n"
        )

    print(
        "\n=== D — 024A1R "
        "CORRECTED DECISION ==="
    )

    print(
        "024A1_WORST_DIRECTION_"
        "FIXED_FIELD_DETERIORATION="
        "RETAINED"
    )

    print(
        "ALL_320_ADDITIVE_IMPROVEMENT_"
        "AS_POSITIVE_SECTOR_PROMOTION_GATE="
        "RETIRED_STRUCTURALLY_OVER_STRONG"
    )

    print(
        "POINT_PAYLOAD_ORIENTATION_"
        "AVERAGE_THEOREM="
        + (
            "PASS"
            if point_pass
            else "FAIL"
        )
    )

    print(
        "FINITE_PAYLOAD_ORIENTATION_"
        "AVERAGE_NONPOSITIVE="
        + (
            "PASS"
            if finite_nonpositive
            else "FAIL"
        )
    )

    print(
        "024A1R_ORIENTATION_"
        "CRITERION_REPAIR="
        f"{decision}"
    )

    print(
        f"NEXT={next_action}"
    )

    print(
        "LARGE_GENERALIZED_3D_"
        "PDE_SCAN_AUTHORIZED=NO"
    )

    print(
        "GENERALIZED_L2_L4_L6_V_"
        "CONSTITUTIVE_PREFLIGHT=RETAINED"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_"
        "NOT_A_PROBABILITY"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_024A1R_"
        "ORIENTATION_CRITERION_REPAIR"
    )

    print(
        "SUMMARY_JSON="
        f"{OUT_JSON.relative_to(ROOT)}"
    )

    print(
        "AXIS_CSV="
        f"{OUT_CSV.relative_to(ROOT)}"
    )

    print(
        "024A1R_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
