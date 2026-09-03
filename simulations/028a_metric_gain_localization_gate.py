#!/usr/bin/env python3
"""028A — conventional local Planck-mass gain localization gate.

PURPOSE
-------
Test whether a healthy positive-kinetic scalar-tensor sector

    S =
    integral sqrt(-g) [
        F(chi) R / 2
        - Z(chi) (d chi)^2 / 2
        - U(chi)
    ]

can provide a large device-local enhancement of gravitational response
without reintroducing an O(1/G) control/localization energy.

THEORY
------
For F > 0, transforming the metric scalar degree of freedom to Einstein frame
generates the positive conformal kinetic contribution

    rho_conf
    >=
    3 c^4/(32 pi G)
    |grad ln F|^2

when the Jordan-frame scalar kinetic sector is non-negative.

If a localized wall of area A and thickness ell changes the effective Planck
factor by

    Gamma
    =
    F_out/F_in
    =
    G_in/G_out

Cauchy-Schwarz gives the favorable localization bound

    E_wall
    >=
    3 c^4 A/(32 pi G ell)
    (ln Gamma)^2

This contribution cannot be eliminated merely by making F(chi) steeper in
field space because the Einstein-frame term depends directly on grad ln F.

SOURCE + GAIN LEDGER
--------------------
Use

    E_source(Gamma)
    =
    C_source a c^2 h^2
    /
    (G Gamma)

and define

    E0
    =
    a c^2 h^2/G

Then

    E_total/E0
    =
    C_source exp(-x)
    +
    B x^2

where

    x = ln Gamma

and

    B
    =
    3 c^2 A
    /
    (32 pi a h^2 ell)

The exact optimum satisfies

    x exp(x)
    =
    C_source/(2B)

so

    x_opt
    =
    W(C_source/(2B))

This is therefore an analytical falsification gate, not a speculative
large-Gamma parameter fit.

GEOMETRY
--------
Primary:

    A = 4 pi R^2

for a spherical localized gravitational phase.

Also include an intentionally favorable control:

    A = pi R^2

Wall thicknesses up to

    ell = 10 R

are included even though the thickest cases are only weakly device-local.

CLAIM LIMITS
------------
A RED result closes only the conventional positive-kinetic metric
scalar-tensor F(chi)R localization class under the assumptions above.

It does not exclude every modified-gravity, derivative-mixing, multimetric,
critical-response, screened, nonlocal, or other possible gain sector.

CLAIM CLASSIFICATION
--------------------
ANALYTICAL_EFT_SCALING_FALSIFICATION_GATE

NOVEL PHYSICS CLAIM
-------------------
NO
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from scipy.special import lambertw


C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
G0 = 9.80665


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

OUT_JSON = (
    DATA
    / "028a_metric_gain_localization_gate_summary.json"
)

OUT_CSV = (
    DATA
    / "028a_metric_gain_localization_scan.csv"
)

OUT_TARGETS = (
    DATA
    / "028a_metric_gain_target_gamma.csv"
)


SOURCE_COEFFICIENTS = (
    (
        "IDEAL_C1_CONTROL",
        1.0,
    ),
    (
        "027B_CORRECTED_GENUINE_SOURCE",
        3.08075881130598,
    ),
    (
        "006D_REFERENCE",
        23.591586299249,
    ),
)


SCENARIOS = (
    (
        "ONE_G_ONE_M",
        G0,
        1.0,
    ),
    (
        "POINT_ONE_G_ONE_CM",
        0.1
        * G0,
        0.01,
    ),
    (
        "ONE_G_ONE_CM",
        G0,
        0.01,
    ),
)


AREA_MODELS = (
    (
        "OPTIMISTIC_DISK",
        math.pi,
    ),
    (
        "SPHERICAL_PRIMARY",
        4.0
        * math.pi,
    ),
)


R_OVER_H = (
    0.25,
    0.5,
    1.0,
    2.0,
)


ELL_OVER_R = (
    0.25,
    0.5,
    1.0,
    2.0,
    5.0,
    10.0,
)


TARGET_GAMMA = (
    10.0,
    1.0e3,
    1.0e6,
    1.0e9,
    1.0e12,
    1.0e17,
)


rows = []

best_improvement = 1.0
best_row = None


for source_name, c_source in SOURCE_COEFFICIENTS:
    for scenario, accel, h in SCENARIOS:
        e0 = (
            accel
            * C_LIGHT
            ** 2
            * h
            ** 2
            / G_NEWTON
        )

        for area_name, area_factor in AREA_MODELS:
            for r_ratio in R_OVER_H:
                radius = (
                    r_ratio
                    * h
                )

                area = (
                    area_factor
                    * radius
                    ** 2
                )

                for ell_ratio in ELL_OVER_R:
                    ell = (
                        ell_ratio
                        * radius
                    )

                    b = (
                        3.0
                        * C_LIGHT
                        ** 2
                        * area
                        / (
                            32.0
                            * math.pi
                            * accel
                            * h
                            ** 2
                            * ell
                        )
                    )

                    x_opt = float(
                        lambertw(
                            c_source
                            / (
                                2.0
                                * b
                            )
                        ).real
                    )

                    gamma_opt = math.exp(
                        x_opt
                    )

                    normalized_min = (
                        c_source
                        * math.exp(
                            -x_opt
                        )
                        + b
                        * x_opt
                        ** 2
                    )

                    improvement = (
                        c_source
                        / normalized_min
                    )

                    e_min = (
                        normalized_min
                        * e0
                    )

                    e_baseline = (
                        c_source
                        * e0
                    )

                    row = {
                        "source":
                            source_name,

                        "C_source":
                            c_source,

                        "scenario":
                            scenario,

                        "accel_m_s2":
                            accel,

                        "h_m":
                            h,

                        "area_model":
                            area_name,

                        "R_over_h":
                            r_ratio,

                        "ell_over_R":
                            ell_ratio,

                        "B_dimensionless":
                            b,

                        "x_opt_ln_Gamma":
                            x_opt,

                        "Gamma_opt":
                            gamma_opt,

                        "energy_reduction_factor":
                            improvement,

                        "E_baseline_J":
                            e_baseline,

                        "E_min_J":
                            e_min,
                    }

                    rows.append(
                        row
                    )

                    if (
                        improvement
                        > best_improvement
                    ):
                        best_improvement = improvement
                        best_row = row


target_rows = []


for source_name, c_source in SOURCE_COEFFICIENTS:
    for scenario, accel, h in SCENARIOS:
        subset = [
            r
            for r in rows
            if (
                r[
                    "source"
                ]
                == source_name
                and
                r[
                    "scenario"
                ]
                == scenario
            )
        ]

        favorable = min(
            subset,
            key=lambda r: r[
                "B_dimensionless"
            ],
        )

        b = favorable[
            "B_dimensionless"
        ]

        e0 = (
            accel
            * C_LIGHT
            ** 2
            * h
            ** 2
            / G_NEWTON
        )

        for gamma in TARGET_GAMMA:
            x = math.log(
                gamma
            )

            c_wall = (
                b
                * x
                * x
            )

            c_total = (
                c_source
                / gamma
                + c_wall
            )

            e_wall = (
                c_wall
                * e0
            )

            e_total = (
                c_total
                * e0
            )

            b_max_beneficial = (
                c_source
                * (
                    1.0
                    - 1.0
                    / gamma
                )
                / (
                    x
                    * x
                )
            )

            burden_ratio = (
                b
                / b_max_beneficial
            )

            target_rows.append(
                {
                    "source":
                        source_name,

                    "C_source":
                        c_source,

                    "scenario":
                        scenario,

                    "accel_m_s2":
                        accel,

                    "h_m":
                        h,

                    "area_model":
                        favorable[
                            "area_model"
                        ],

                    "R_over_h":
                        favorable[
                            "R_over_h"
                        ],

                    "ell_over_R":
                        favorable[
                            "ell_over_R"
                        ],

                    "Gamma":
                        gamma,

                    "ln_Gamma":
                        x,

                    "B_actual":
                        b,

                    "B_max_beneficial":
                        b_max_beneficial,

                    "localization_burden_ratio":
                        burden_ratio,

                    "localization_burden_orders":
                        math.log10(
                            burden_ratio
                        ),

                    "E_wall_J":
                        e_wall,

                    "E_total_J":
                        e_total,
                }
            )


if (
    best_improvement
    < 1.01
):
    decision = (
        "RED_CONVENTIONAL_POSITIVE_KINETIC_"
        "F_R_LOCAL_GAIN"
    )

    next_step = (
        "DO_NOT_BUILD_F_R_GAIN_PDE; "
        "RERANK_HEALTHY_DERIVATIVE_MIXING_"
        "CRITICAL_OR_NONCONFORMAL_GAIN_CLASSES"
    )

else:
    decision = (
        "YELLOW_CONVENTIONAL_F_R_GAIN_"
        "HAS_NONTRIVIAL_ENERGY_WINDOW"
    )

    next_step = (
        "AUDIT_STABILITY_EFT_EMPIRICAL_AND_"
        "BACKREACTION_BEFORE_ANY_REALIZATION"
    )


summary = {
    "branch":
        "TRUE_ANTIGRAVITY_GAIN_ENGINE",

    "simulation":
        "028A",

    "theory_class":
        (
            "metric scalar-tensor F(chi)R with F>0 "
            "and nonnegative Jordan-frame scalar "
            "kinetic energy"
        ),

    "analytic_bound":
        (
            "E_wall >= "
            "3 c^4 A/(32 pi G ell) "
            "(ln Gamma)^2"
        ),

    "source_scaling":
        (
            "E_source = "
            "C a c^2 h^2/(G Gamma)"
        ),

    "optimization":
        (
            "x_opt = LambertW(C/(2B)), "
            "x=ln Gamma"
        ),

    "best_energy_reduction_factor":
        best_improvement,

    "best_case":
        best_row,

    "decision":
        decision,

    "next":
        next_step,

    "claims": {
        "closes_all_modified_gravity":
            False,

        "closes_positive_kinetic_conformal_F_R_local_gain_under_assumptions":
            decision.startswith(
                "RED_"
            ),

        "practical_gain_engine":
            False,

        "practical_antigravity_device":
            False,
    },
}


with OUT_JSON.open(
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        summary,
        f,
        indent=2,
        sort_keys=True,
    )


with OUT_CSV.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=list(
            rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        rows
    )


with OUT_TARGETS.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=list(
            target_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        target_rows
    )


key_target = None

for row in target_rows:
    if (
        row[
            "source"
        ]
        == "027B_CORRECTED_GENUINE_SOURCE"
        and
        row[
            "scenario"
        ]
        == "ONE_G_ONE_M"
        and
        abs(
            row[
                "Gamma"
            ]
            - 1.0e17
        )
        / 1.0e17
        < 1.0e-12
    ):
        key_target = row
        break


print(
    "=== 028A METRIC-GAIN LOCALIZATION GATE ==="
)

print(
    "THEORY_CLASS=POSITIVE_KINETIC_METRIC_SCALAR_TENSOR_F_R"
)

print(
    (
        "BOUND="
        "E_WALL_GE_3_C4_A_OVER_32PI_G_ELL_"
        "TIMES_LN_GAMMA_SQUARED"
    )
)

print(
    (
        "BEST_ENERGY_REDUCTION_FACTOR="
        f"{best_improvement:.15e}"
    )
)

if best_row is not None:
    print(
        (
            "BEST_CASE_SOURCE="
            f"{best_row['source']}"
        )
    )

    print(
        (
            "BEST_CASE_SCENARIO="
            f"{best_row['scenario']}"
        )
    )

    print(
        (
            "BEST_CASE_AREA="
            f"{best_row['area_model']}"
        )
    )

    print(
        (
            "BEST_CASE_R_OVER_H="
            f"{best_row['R_over_h']}"
        )
    )

    print(
        (
            "BEST_CASE_ELL_OVER_R="
            f"{best_row['ell_over_R']}"
        )
    )

    print(
        (
            "BEST_CASE_B="
            f"{best_row['B_dimensionless']:.15e}"
        )
    )

    print(
        (
            "BEST_CASE_GAMMA_OPT="
            f"{best_row['Gamma_opt']:.15e}"
        )
    )


if key_target is not None:
    print(
        (
            "027B_SOURCE_1G_1M_GAMMA_1E17_"
            "LOCALIZATION_BURDEN_ORDERS="
            f"{key_target['localization_burden_orders']:.12f}"
        )
    )

    print(
        (
            "027B_SOURCE_1G_1M_GAMMA_1E17_"
            "E_WALL_J="
            f"{key_target['E_wall_J']:.15e}"
        )
    )


print(
    f"028A_DECISION={decision}"
)

print(
    f"NEXT={next_step}"
)

print(
    "REMOVES_1_OVER_G_BOTTLENECK=NO"
)

print(
    "PRACTICAL_GAIN_ENGINE=NO"
)

print(
    "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
)

print(
    f"SUMMARY_JSON={OUT_JSON}"
)

print(
    f"SCAN_CSV={OUT_CSV}"
)

print(
    f"TARGET_GAMMA_CSV={OUT_TARGETS}"
)

print(
    "028A_RUN_COMPLETE=YES"
)
