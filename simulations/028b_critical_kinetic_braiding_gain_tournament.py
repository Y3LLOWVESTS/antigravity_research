#!/usr/bin/env python3
"""028B — critical kinetic-braiding gain tournament.

Question
--------
Can a healthy derivative-mixing / cubic kinetic-braiding sector amplify the
metric response of the conservative true-stand-off source by the required
10^16–10^17 factor without reintroducing prohibitive control energy, a soft
kinetic mode below the device EFT scale, or extreme cancellation?

Theory
------
Generic two-mode mixing:

    K = [[1,b],[b,k]]

    Gamma = 1/(1-b^2/k)

For fixed Gamma, the minimum condition number occurs at k=1 and approaches

    kappa_min ~ 4 Gamma

at large Gamma.

This is independently verified by numerical minimization.

Cubic/KGB-inspired anisotropic background:

    Qt = 1 + 2(x1+x2+x3)

    Q1 = 1 + 2(x2+x3)

    Q2 = 1 + 2(x1+x3)

    Q3 = 1 + 2(x1+x2)

with the optimistic response surrogate

    Gamma = 1 + alpha^2/Q3

For fixed Q3, x1=x2 minimizes the Hessian norm.

x3 is chosen minimally to enforce

    Qt >= Qtime_floor

Canonical normalization of a cubic operator gives

    Lambda_eff = Lambda sqrt(Z_min)

The explicit positive canonical gradient-energy inventory of a quadratic
background occupying a sphere of radius R is

    E_can
      =
    (2 pi / 15)
    Lambda^6 R^5
    sum_i x_i^2

in natural units.

Project practicality targets
-----------------------------
Primary macroscopic target:

    a = 1 g
    h = 1 m
    total budget = 1 TJ

Two sign-source coefficients are tested:

    C = 1
        idealized source-side control

    C = 23.591586299249
        conservative 006D true-stand-off source

Secondary generous target:

    a = 0.1 g
    h = 1 cm
    total budget = 1 PJ

The script does NOT choose Gamma in advance.

For every theory point it minimizes

    E_total(Gamma)
      =
    E_source(Gamma)
      +
    E_background(Gamma)

over Gamma.

It then independently asks:

    If the no-cancellation ledger misses the target,
    how much negative interaction-energy cancellation would be required
    to force the complete gain sector under budget?

That cancellation is diagnostic only.

Promotion
---------
MAJOR GREEN:

    006D
    + primary health margin
    + cutoff safety >= 10
    + no interaction-energy cancellation
    + 1 g / 1 m
    + total <= 1 TJ

GREEN:

    ideal C=1 source
    + same health/cutoff requirements
    + total <= 1 TJ

YELLOW:

    only an optimistic macroscopic branch survives

or

    the macroscopic 1-TJ gate fails,
    but the conservative 006D source survives the generous
    0.1 g / 1 cm / 1 PJ branch.

RED:

    tested critical cubic-braiding class cannot reach even those gates.

80% rule
--------
The gain-engine 80% marker is earned only by MAJOR GREEN.

Overall practical-antigravity 80% remains false in this analytical run because
a full covariant localized realization, full T_mn, empirical consistency,
backreaction, transition walls, and combined source+gain solution remain
separate accomplishments.

Blind wildcard audit
--------------------
The values

    0.625
    1.6
    1.875
    3.125
    5

are tested as cutoff-safety wildcards.

They are explicitly excluded from scientific selection.

Assumptions / limitations
-------------------------
This is a falsification-first analytical/EFT surrogate, not a complete
covariant localized KGB solution.

The canonical gradient energy is an explicit positive component of the chosen
field architecture, but the complete Galileon interaction stress-energy is not
computed here.

Therefore:

- a large required cancellation is a severe warning;
- it is not a theorem excluding every derivative-mixing completion.

The run does not close:

- full covariant gain-sector T_mn;
- transition-wall energy;
- recovery of GR outside the device;
- nonlinear metric backreaction;
- empirical fifth-force constraints;
- equivalence-principle constraints;
- radiation;
- device formation/reset;
- a practical antigravity device.

References
----------
Deffayet, Pujolas, Sawicki, Vikman, arXiv:1008.0048.

Kase and Tsujikawa, arXiv:1809.08735.

Claim classification
--------------------
TRUE_ANTIGRAVITY_GAIN_ENGINE_ANALYTICAL_FALSIFICATION_GATE

Novel-physics claim
-------------------
NO
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar


C_LIGHT = 299_792_458.0

G_NEWTON = 6.67430e-11

G0 = 9.80665

HBARC_EV_M = 1.973269804e-7

EV_J = 1.602176634e-19

C_006D = 23.591586299249

LOOP_FLOOR = (
    1.0
    / (
        16.0
        * math.pi
        ** 2
    )
)


ROOT = Path(
    __file__
).resolve().parents[
    1
]

DATA = (
    ROOT
    / "results"
    / "data"
)

SMOKE = (
    os.environ.get(
        "AG028B_SMOKE",
        "0",
    )
    == "1"
)


P028A = (
    DATA
    / "028a_metric_gain_localization_gate_summary.json"
)

P027D = (
    DATA
    / "027d_exact_self_closing_stress_summary.json"
)


OUT = (
    DATA
    / "028b_critical_braiding_gain_summary.json"
)

MATRIX_CSV = (
    DATA
    / "028b_kinetic_matrix_theorem_scan.csv"
)

CASES_CSV = (
    DATA
    / "028b_cubic_braiding_practicality_scan.csv"
)

TARGET_CSV = (
    DATA
    / "028b_target_gain_audit.csv"
)

WILD_CSV = (
    DATA
    / "028b_wildcard_audit.csv"
)


SOURCES = (
    (
        "IDEAL_C1",
        1.0,
    ),
    (
        "006D_REFERENCE",
        C_006D,
    ),
)


SCENARIOS = (
    (
        "ONE_G_ONE_M_ONE_TJ",
        G0,
        1.0,
        1.0e12,
    ),
    (
        "POINT_ONE_G_ONE_CM_ONE_PJ",
        0.1
        * G0,
        0.01,
        1.0e15,
    ),
)


if SMOKE:
    ALPHAS = (
        1.0,
    )

    QT_FLOORS = (
        0.1,
    )

    SAFETIES = (
        1.0,
        10.0,
    )

    REGION_RATIOS = (
        1.0,
    )

else:
    ALPHAS = (
        1.0,
        1.0
        / math.sqrt(
            6.0
        ),
        0.1,
    )

    QT_FLOORS = (
        1.0e-3,
        1.0e-2,
        0.1,
        1.0,
    )

    SAFETIES = (
        1.0,
        10.0,
        100.0,
    )

    REGION_RATIOS = (
        0.5,
        1.0,
        2.0,
    )


WILDCARDS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


def load_json(
    path: Path,
) -> dict:
    """Load a required lineage artifact."""

    if not path.is_file():
        raise FileNotFoundError(
            f"Required lineage missing: {path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


J028A = load_json(
    P028A
)

J027D = load_json(
    P027D
)


if not str(
    J028A.get(
        "decision",
        "",
    )
).startswith(
    "RED_"
):
    raise RuntimeError(
        "Expected closed RED 028A lineage"
    )


if not str(
    J027D.get(
        "decision",
        "",
    )
).startswith(
    "RED_"
):
    raise RuntimeError(
        "Expected closed RED 027D lineage"
    )


def kmatrix(
    gamma: float,
    k: float = 1.0,
) -> tuple[
    float,
    float,
    float,
]:
    """Return eigenvalues and condition number of the mixing matrix."""

    if (
        gamma
        <= 1.0
        or
        k
        <= 0.0
    ):
        raise ValueError(
            "gamma>1 and k>0 required"
        )

    det = (
        k
        / gamma
    )

    trace = (
        1.0
        + k
    )

    disc = math.sqrt(
        max(
            0.0,
            trace
            * trace
            - 4.0
            * det,
        )
    )

    lambda_max = (
        0.5
        * (
            trace
            + disc
        )
    )

    lambda_min = (
        det
        / lambda_max
    )

    condition = (
        lambda_max
        / lambda_min
    )

    return (
        lambda_min,
        lambda_max,
        condition,
    )


def exact_mix(
    gamma: float,
) -> dict:
    """Return the exact balanced minimum-condition-number solution."""

    inv = (
        1.0
        / gamma
    )

    root = math.sqrt(
        max(
            0.0,
            1.0
            - inv,
        )
    )

    lambda_max = (
        1.0
        + root
    )

    lambda_min = (
        inv
        / lambda_max
    )

    condition = (
        lambda_max
        / lambda_min
    )

    return {
        "Gamma":
            gamma,

        "k_opt_exact":
            1.0,

        "b_opt_exact":
            math.sqrt(
                max(
                    0.0,
                    1.0
                    - inv,
                )
            ),

        "lambda_min":
            lambda_min,

        "lambda_max":
            lambda_max,

        "condition_number":
            condition,

        "condition_over_4Gamma":
            condition
            / (
                4.0
                * gamma
            ),

        "tuning_digits":
            math.log10(
                gamma
            ),
    }


def numeric_mix(
    gamma: float,
) -> tuple[
    float,
    float,
]:
    """Numerically verify the exact k=1 theorem."""

    def objective(
        log_k: float,
    ) -> float:
        k = math.exp(
            log_k
        )

        return math.log(
            kmatrix(
                gamma,
                k,
            )[
                2
            ]
        )

    result = minimize_scalar(
        objective,
        bounds=(
            -20.0,
            20.0,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-12,
        },
    )

    return (
        math.exp(
            result.x
        ),
        math.exp(
            result.fun
        ),
    )


def cubic_state(
    gamma: float,
    alpha: float,
    h: float,
    region_ratio: float,
    qt_floor: float,
    safety: float,
) -> dict:
    """Construct the minimum-norm critical cubic-background surrogate."""

    if gamma <= 1.0:
        raise ValueError(
            "Gamma must exceed one"
        )

    q3 = (
        alpha
        * alpha
        / (
            gamma
            - 1.0
        )
    )

    x1 = (
        q3
        - 1.0
    ) / 4.0

    x2 = x1

    x3 = max(
        0.0,
        (
            qt_floor
            - q3
        )
        / 2.0,
    )

    qt = (
        q3
        + 2.0
        * x3
    )

    q1 = (
        1.0
        + 2.0
        * (
            x2
            + x3
        )
    )

    q2 = (
        1.0
        + 2.0
        * (
            x1
            + x3
        )
    )

    zmin = min(
        qt,
        q1,
        q2,
        q3,
    )

    if zmin <= 0.0:
        raise RuntimeError(
            "Non-positive fluctuation kinetic coefficient"
        )

    radius = (
        h
        * region_ratio
    )

    probe = min(
        h,
        radius,
    )

    device_eV = (
        HBARC_EV_M
        / probe
    )

    bare_eV = (
        safety
        * device_eV
        / math.sqrt(
            zmin
        )
    )

    effective_eV = (
        bare_eV
        * math.sqrt(
            zmin
        )
    )

    radius_evinv = (
        radius
        / HBARC_EV_M
    )

    xnorm2 = (
        x1
        * x1
        + x2
        * x2
        + x3
        * x3
    )

    energy_eV = (
        (
            2.0
            * math.pi
            / 15.0
        )
        * bare_eV
        ** 6
        * radius_evinv
        ** 5
        * xnorm2
    )

    energy_j = (
        energy_eV
        * EV_J
    )

    return {
        "Q3":
            q3,

        "Qt":
            qt,

        "Q1":
            q1,

        "Q2":
            q2,

        "Z_min":
            zmin,

        "x1":
            x1,

        "x2":
            x2,

        "x3":
            x3,

        "xnorm2":
            xnorm2,

        "bare_cutoff_eV":
            bare_eV,

        "effective_cutoff_eV":
            effective_eV,

        "canonical_background_J":
            energy_j,

        "critical_control_digits":
            -math.log10(
                max(
                    q3,
                    1.0e-300,
                )
            ),
    }


def source_energy(
    csrc: float,
    acceleration: float,
    h: float,
    gamma: float,
) -> float:
    """Return the source energy after response amplification Gamma."""

    return (
        csrc
        * acceleration
        * C_LIGHT
        ** 2
        * h
        ** 2
        / (
            G_NEWTON
            * gamma
        )
    )


def optimize_case(
    csrc: float,
    acceleration: float,
    h: float,
    budget: float,
    alpha: float,
    region_ratio: float,
    qt_floor: float,
    safety: float,
) -> dict:
    """Optimize Gamma and separately optimize required energy cancellation."""

    gamma_floor = max(
        1.0
        + alpha
        * alpha
        + 1.0e-9,
        1.000001,
    )

    lower = math.log10(
        gamma_floor
    )

    upper = 20.0

    def total(
        log_gamma: float,
    ) -> float:
        gamma = (
            10.0
            ** log_gamma
        )

        background = cubic_state(
            gamma,
            alpha,
            h,
            region_ratio,
            qt_floor,
            safety,
        )[
            "canonical_background_J"
        ]

        return (
            source_energy(
                csrc,
                acceleration,
                h,
                gamma,
            )
            + background
        )

    optimum = minimize_scalar(
        lambda x: math.log(
            total(
                x
            )
        ),
        bounds=(
            lower,
            upper,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-9,
        },
    )

    gamma = (
        10.0
        ** optimum.x
    )

    state = cubic_state(
        gamma,
        alpha,
        h,
        region_ratio,
        qt_floor,
        safety,
    )

    e_source = source_energy(
        csrc,
        acceleration,
        h,
        gamma,
    )

    e_background = state[
        "canonical_background_J"
    ]

    e_total = (
        e_source
        + e_background
    )

    gamma_budget = max(
        (
            csrc
            * acceleration
            * C_LIGHT
            ** 2
            * h
            ** 2
            / (
                G_NEWTON
                * budget
            )
        ),
        1.0
        + 1.0e-12,
    )

    cancellation_floor = max(
        gamma_budget
        * (
            1.0
            + 1.0e-12
        ),
        gamma_floor,
    )

    cancellation_lower = math.log10(
        cancellation_floor
    )

    def negative_log_allowed(
        log_gamma: float,
    ) -> float:
        g = (
            10.0
            ** log_gamma
        )

        remaining_budget = (
            budget
            - source_energy(
                csrc,
                acceleration,
                h,
                g,
            )
        )

        if remaining_budget <= 0.0:
            return 1.0e300

        background = cubic_state(
            g,
            alpha,
            h,
            region_ratio,
            qt_floor,
            safety,
        )[
            "canonical_background_J"
        ]

        return -(
            math.log(
                remaining_budget
            )
            - math.log(
                background
            )
        )

    cancellation_optimum = minimize_scalar(
        negative_log_allowed,
        bounds=(
            cancellation_lower,
            upper,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-10,
        },
    )

    log_allowed = (
        -cancellation_optimum.fun
    )

    if log_allowed > -745.0:
        allowed = math.exp(
            log_allowed
        )

    else:
        allowed = 0.0

    allowed = min(
        1.0,
        max(
            0.0,
            allowed,
        ),
    )

    if allowed < 1.0:
        cancellation_digits = (
            -math.log10(
                max(
                    allowed,
                    1.0e-300,
                )
            )
        )

    else:
        cancellation_digits = 0.0

    return {
        "gamma_opt":
            gamma,

        "E_source_J":
            e_source,

        "E_background_canonical_J":
            e_background,

        "E_total_no_cancel_J":
            e_total,

        "budget_ratio":
            e_total
            / budget,

        "meets_budget_no_cancel":
            bool(
                e_total
                <= budget
            ),

        "gamma_source_only_budget":
            gamma_budget,

        "gamma_best_cancellation":
            10.0
            ** cancellation_optimum.x,

        "allowed_background_residual_fraction":
            allowed,

        "required_interaction_cancellation_fraction":
            max(
                0.0,
                1.0
                - allowed,
            ),

        "cancellation_digits":
            cancellation_digits,

        **state,
    }


print(
    "=== 028B CRITICAL KINETIC-BRAIDING GAIN TOURNAMENT ===",
    flush=True,
)

print(
    (
        "028A_LINEAGE="
        + str(
            J028A.get(
                "decision"
            )
        )
    ),
    flush=True,
)

print(
    (
        "027D_LINEAGE="
        + str(
            J027D.get(
                "decision"
            )
        )
    ),
    flush=True,
)

print(
    f"SMOKE={SMOKE}",
    flush=True,
)


matrix_rows = []

gamma_count = (
    17
    if SMOKE
    else 81
)

for gamma in np.logspace(
    0.05,
    20.0,
    gamma_count,
):
    exact = exact_mix(
        float(
            gamma
        )
    )

    k_numeric, condition_numeric = numeric_mix(
        float(
            gamma
        )
    )

    matrix_rows.append(
        {
            **exact,

            "k_opt_numeric":
                k_numeric,

            "condition_numeric":
                condition_numeric,

            "k_error":
                abs(
                    k_numeric
                    - 1.0
                ),

            "condition_relerr":
                abs(
                    condition_numeric
                    - exact[
                        "condition_number"
                    ]
                )
                / exact[
                    "condition_number"
                ],
        }
    )


max_k_error = max(
    row[
        "k_error"
    ]
    for row in matrix_rows
)

max_condition_error = max(
    row[
        "condition_relerr"
    ]
    for row in matrix_rows
)


print(
    "=== GENERIC MIXING THEOREM ===",
    flush=True,
)

print(
    f"MATRIX_MAX_K_ERROR={max_k_error:.6e}",
    flush=True,
)

print(
    (
        "MATRIX_MAX_CONDITION_RELERR="
        f"{max_condition_error:.6e}"
    ),
    flush=True,
)

print(
    "KINETIC_THEOREM=K_OPT_1_AND_KAPPA_ASYMPTOTIC_4GAMMA",
    flush=True,
)

print(
    (
        "UNPROTECTED_LOOP_FLOOR="
        f"{LOOP_FLOOR:.15e}"
    ),
    flush=True,
)

print(
    (
        "UNPROTECTED_GAIN_SCALE="
        f"{1.0 / LOOP_FLOOR:.15e}"
    ),
    flush=True,
)


case_rows = []


for source_name, csrc in SOURCES:
    for (
        scenario,
        acceleration,
        h,
        budget,
    ) in SCENARIOS:

        print(
            (
                "028B_GROUP "
                f"SOURCE={source_name} "
                f"SCENARIO={scenario}"
            ),
            flush=True,
        )

        for alpha in ALPHAS:
            for region_ratio in REGION_RATIOS:
                for qt_floor in QT_FLOORS:
                    for safety in SAFETIES:

                        result = optimize_case(
                            csrc,
                            acceleration,
                            h,
                            budget,
                            alpha,
                            region_ratio,
                            qt_floor,
                            safety,
                        )

                        case_rows.append(
                            {
                                "source":
                                    source_name,

                                "C_source":
                                    csrc,

                                "scenario":
                                    scenario,

                                "accel_m_s2":
                                    acceleration,

                                "h_m":
                                    h,

                                "budget_J":
                                    budget,

                                "alpha":
                                    alpha,

                                "region_ratio":
                                    region_ratio,

                                "qtime_floor":
                                    qt_floor,

                                "cutoff_safety":
                                    safety,

                                **result,
                            }
                        )


def rows_for(
    source: str,
    scenario: str,
) -> list[dict]:
    """Return one source/scenario slice."""

    return [
        row
        for row in case_rows
        if (
            row[
                "source"
            ]
            == source
            and
            row[
                "scenario"
            ]
            == scenario
        )
    ]


def optimistic(
    rows: list[dict],
) -> dict:
    """Return the most favorable point in the full scan."""

    return min(
        rows,
        key=lambda row: row[
            "E_total_no_cancel_J"
        ],
    )


def primary(
    rows: list[dict],
) -> dict:
    """Return the best predeclared primary-health point."""

    eligible = [
        row
        for row in rows
        if (
            abs(
                row[
                    "alpha"
                ]
                - 1.0
            )
            < 1.0e-12
            and
            row[
                "qtime_floor"
            ]
            >= 0.1
            and
            row[
                "cutoff_safety"
            ]
            >= 10.0
        )
    ]

    if not eligible:
        raise RuntimeError(
            "No primary-health cases"
        )

    return min(
        eligible,
        key=lambda row: row[
            "E_total_no_cancel_J"
        ],
    )


groups = {
    "IDEAL_MACRO":
        rows_for(
            "IDEAL_C1",
            "ONE_G_ONE_M_ONE_TJ",
        ),

    "006D_MACRO":
        rows_for(
            "006D_REFERENCE",
            "ONE_G_ONE_M_ONE_TJ",
        ),

    "006D_SMALL":
        rows_for(
            "006D_REFERENCE",
            "POINT_ONE_G_ONE_CM_ONE_PJ",
        ),
}


selected = {
    name: {
        "optimistic":
            optimistic(
                rows
            ),

        "primary":
            primary(
                rows
            ),
    }
    for name, rows in groups.items()
}


ideal_optimistic = selected[
    "IDEAL_MACRO"
][
    "optimistic"
]

ideal_primary = selected[
    "IDEAL_MACRO"
][
    "primary"
]

sixd_primary = selected[
    "006D_MACRO"
][
    "primary"
]

small_primary = selected[
    "006D_SMALL"
][
    "primary"
]


if sixd_primary[
    "meets_budget_no_cancel"
]:
    decision = (
        "MAJOR_GREEN_006D_CRITICAL_BRAIDING_"
        "MEETS_1TJ_MACRO_GATE"
    )

    next_step = (
        "BUILD_FULL_COVARIANT_LOCALIZED_KGB_GAIN_FIELD_"
        "AND_EMPIRICAL_AUDIT"
    )

    gain_80 = True

elif ideal_primary[
    "meets_budget_no_cancel"
]:
    decision = (
        "GREEN_IDEAL_SOURCE_CRITICAL_BRAIDING_"
        "MEETS_1TJ_MACRO_GATE"
    )

    next_step = (
        "BUILD_COVARIANT_GAIN_FIELD_"
        "BEFORE_COMBINING_WITH_006D"
    )

    gain_80 = False

elif ideal_optimistic[
    "meets_budget_no_cancel"
]:
    decision = (
        "YELLOW_ONLY_OPTIMISTIC_CRITICAL_BRAIDING_"
        "MEETS_MACRO_GATE"
    )

    next_step = (
        "CLOSE_HEALTH_MARGIN_AND_CUTOFF_GAPS_"
        "BEFORE_FIELD_REALIZATION"
    )

    gain_80 = False

elif small_primary[
    "meets_budget_no_cancel"
]:
    decision = (
        "YELLOW_SUBSCALE_WINDOW_"
        "MACROSCOPIC_1TJ_GATE_RED"
    )

    next_step = (
        "TEST_FULL_COVARIANT_KGB_STRESS_ENERGY_"
        "ON_0P1G_1CM_WINDOW_BEFORE_ABANDONING_GAIN_CLASS"
    )

    gain_80 = False

else:
    decision = (
        "RED_TESTED_CRITICAL_CUBIC_BRAIDING_"
        "PRACTICALITY_CLASS"
    )

    next_step = (
        "CLOSE_CUBIC_CRITICAL_BRAIDING_"
        "AND_RERANK_NONCONFORMAL_GAIN_CLASSES"
    )

    gain_80 = False


def target_row(
    source_name: str,
    csrc: float,
    scenario: str,
    acceleration: float,
    h: float,
    budget: float,
) -> dict:
    """Audit the gain needed if the source alone were to hit budget."""

    gamma = max(
        (
            csrc
            * acceleration
            * C_LIGHT
            ** 2
            * h
            ** 2
            / (
                G_NEWTON
                * budget
            )
        ),
        1.0
        + 1.0e-12,
    )

    mix = exact_mix(
        gamma
    )

    state_s1 = cubic_state(
        gamma,
        1.0,
        h,
        1.0,
        0.1,
        1.0,
    )

    state_s10 = cubic_state(
        gamma,
        1.0,
        h,
        1.0,
        0.1,
        10.0,
    )

    return {
        "source":
            source_name,

        "scenario":
            scenario,

        "Gamma_source_only_budget":
            gamma,

        "minimum_kinetic_condition_number":
            mix[
                "condition_number"
            ],

        "minimum_soft_eigenvalue":
            mix[
                "lambda_min"
            ],

        "critical_tuning_digits":
            math.log10(
                gamma
            ),

        "unprotected_loop_margin":
            (
                1.0
                / gamma
            )
            / LOOP_FLOOR,

        "bare_cutoff_eV_safety1":
            state_s1[
                "bare_cutoff_eV"
            ],

        "canonical_background_J_safety1":
            state_s1[
                "canonical_background_J"
            ],

        "bare_cutoff_eV_safety10":
            state_s10[
                "bare_cutoff_eV"
            ],

        "canonical_background_J_safety10":
            state_s10[
                "canonical_background_J"
            ],
    }


target_rows = [
    target_row(
        source_name,
        csrc,
        scenario,
        acceleration,
        h,
        budget,
    )
    for source_name, csrc in SOURCES
    for (
        scenario,
        acceleration,
        h,
        budget,
    ) in SCENARIOS
]


wildcard_rows = []


for value in WILDCARDS:
    result = optimize_case(
        C_006D,
        G0,
        1.0,
        1.0e12,
        1.0,
        1.0,
        0.1,
        value,
    )

    wildcard_rows.append(
        {
            "wildcard_cutoff_safety":
                value,

            "gamma_opt":
                result[
                    "gamma_opt"
                ],

            "E_total_no_cancel_J":
                result[
                    "E_total_no_cancel_J"
                ],

            "budget_ratio":
                result[
                    "budget_ratio"
                ],

            "selection_role":
                "BLIND_NON_EVIDENTIARY_EXCLUDED",
        }
    )


summary = {
    "branch":
        "TRUE_ANTIGRAVITY_GAIN_ENGINE",

    "simulation":
        "028B",

    "question":
        (
            "Can healthy near-critical derivative mixing or cubic kinetic "
            "braiding supply the 10^16-10^17 universal response gain "
            "required by a true-stand-off source without recreating a "
            "prohibitive control-energy or strong-coupling burden?"
        ),

    "lineage": {
        "028A":
            J028A.get(
                "decision"
            ),

        "027D":
            J027D.get(
                "decision"
            ),

        "C_006D":
            C_006D,
    },

    "generic_mixing": {
        "Gamma":
            "1/(1-b^2/k)",

        "k_opt":
            1.0,

        "large_Gamma_condition":
            "kappa_min ~ 4 Gamma",

        "max_k_numeric_error":
            max_k_error,

        "max_condition_relative_error":
            max_condition_error,

        "unprotected_loop_floor":
            LOOP_FLOOR,

        "unprotected_gain_scale":
            1.0
            / LOOP_FLOOR,
    },

    "cubic_background_status":
        "SURROGATE_NOT_FULL_COVARIANT_LOCALIZED_SOLUTION",

    "selected_cases":
        selected,

    "target_gain_audit":
        target_rows,

    "decision":
        decision,

    "next":
        next_step,

    "gain_engine_80_heuristic_authorized":
        gain_80,

    "overall_practical_antigravity_80_heuristic_authorized":
        False,

    "mandatory_parallel_credibility_branch":
        "026C_N89_FORCE_CONVERGENCE",

    "claims": {
        "full_covariant_gain_Tmunu":
            False,

        "transition_wall_energy_closed":
            False,

        "empirical_consistency_closed":
            False,

        "universal_metric_gain_realized":
            False,

        "practical_antigravity_device":
            False,
    },
}


DATA.mkdir(
    parents=True,
    exist_ok=True,
)


with OUT.open(
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        summary,
        f,
        indent=2,
        sort_keys=True,
        default=lambda obj: (
            obj.item()
            if isinstance(
                obj,
                np.generic,
            )
            else str(
                obj
            )
        ),
    )


for path, rows in (
    (
        MATRIX_CSV,
        matrix_rows,
    ),
    (
        CASES_CSV,
        case_rows,
    ),
    (
        TARGET_CSV,
        target_rows,
    ),
    (
        WILD_CSV,
        wildcard_rows,
    ),
):
    with path.open(
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


print(
    "=== 028B DECISIVE RESULTS ===",
    flush=True,
)


for label, row in (
    (
        "IDEAL_MACRO_OPTIMISTIC",
        ideal_optimistic,
    ),
    (
        "IDEAL_MACRO_PRIMARY",
        ideal_primary,
    ),
    (
        "006D_MACRO_PRIMARY",
        sixd_primary,
    ),
    (
        "006D_SMALL_PRIMARY",
        small_primary,
    ),
):
    print(
        (
            f"{label} "
            f"GAMMA_OPT={row['gamma_opt']:.12e} "
            f"E_TOTAL={row['E_total_no_cancel_J']:.12e} "
            f"BUDGET_RATIO={row['budget_ratio']:.12e} "
            f"ALLOWED_BG_RESIDUAL="
            f"{row['allowed_background_residual_fraction']:.12e} "
            f"CANCEL_DIGITS={row['cancellation_digits']:.6f} "
            f"SAFETY={row['cutoff_safety']:.6g} "
            f"QT_FLOOR={row['qtime_floor']:.6g} "
            f"REGION_RATIO={row['region_ratio']:.6g}"
        ),
        flush=True,
    )


for row in target_rows:
    if (
        row[
            "scenario"
        ]
        == "ONE_G_ONE_M_ONE_TJ"
    ):
        print(
            (
                f"TARGET_GAIN_{row['source']}="
                f"{row['Gamma_source_only_budget']:.15e}"
            ),
            flush=True,
        )

        print(
            (
                f"TARGET_CONDITION_{row['source']}="
                f"{row['minimum_kinetic_condition_number']:.15e}"
            ),
            flush=True,
        )

        print(
            (
                f"TARGET_CANONICAL_BG_S10_{row['source']}="
                f"{row['canonical_background_J_safety10']:.15e}"
            ),
            flush=True,
        )


print(
    f"028B_DECISION={decision}",
    flush=True,
)

print(
    f"NEXT={next_step}",
    flush=True,
)

print(
    (
        "GAIN_ENGINE_80_HEURISTIC_AUTHORIZED="
        + (
            "YES"
            if gain_80
            else "NO"
        )
    ),
    flush=True,
)

print(
    "OVERALL_PRACTICAL_ANTIGRAVITY_80_HEURISTIC_AUTHORIZED=NO",
    flush=True,
)

print(
    "FULL_COVARIANT_GAIN_TMUNU=NO",
    flush=True,
)

print(
    "EMPIRICAL_CONSISTENCY_CLOSED=NO",
    flush=True,
)

print(
    "PRACTICAL_ANTIGRAVITY_DEVICE=NO",
    flush=True,
)

print(
    "026C_N89_STILL_REQUIRED=YES",
    flush=True,
)

print(
    f"SUMMARY_JSON={OUT}",
    flush=True,
)

print(
    f"MATRIX_CSV={MATRIX_CSV}",
    flush=True,
)

print(
    f"CASES_CSV={CASES_CSV}",
    flush=True,
)

print(
    f"TARGET_CSV={TARGET_CSV}",
    flush=True,
)

print(
    f"WILDCARD_CSV={WILD_CSV}",
    flush=True,
)

print(
    "028B_RUN_COMPLETE=YES",
    flush=True,
)
