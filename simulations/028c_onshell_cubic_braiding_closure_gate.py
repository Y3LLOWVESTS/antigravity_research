#!/usr/bin/env python3
"""028C — on-shell cubic-braiding closure gate.

PURPOSE
-------
Perform the final decisive test of the subscale gain window left by 028B.

028B found a YELLOW surrogate window for the conservative 006D true-stand-off
source at

    acceleration = 0.1 g
    stand-off scale = 1 cm
    total energy budget = 1 PJ.

However, 028B prescribed a near-critical anisotropic kinetic background
without requiring that background to solve the cubic-Galileon field equation.

028C replaces that off-shell surrogate by an explicit shift-symmetric cubic
Galileon / kinetic-gravity-braiding bulk field.

SCIENTIFIC QUESTION
-------------------
Can an explicit healthy on-shell cubic Galileon background provide enough
local response enhancement to preserve the 028B 0.1 g / 1 cm / 1 PJ window?

If not, the tested local scalar gain program through 028C is closed.

PHYSICAL MODEL
--------------
Use the cubic Galileon convention

    L =
        -1/2 (partial pi)^2
        - c3/Lambda^3 (partial pi)^2 box(pi)

with c3 > 0.

The dimensionless constant-Hessian bulk background is

    partial_i partial_j pi
        =
    Lambda^3 diag(x1,x2,x3).

The cubic Galileon field equation in vacuum is

    s + 4 c3 p2 = 0

where

    s  = x1 + x2 + x3

    p2 = x1*x2 + x1*x3 + x2*x3.

The high-frequency fluctuation kinetic coefficients are

    Qt = 1 + 4 c3 s

    Zi = 1 + 4 c3 (s - xi).

For the most favorable possible directional response, define

    Gamma_upper = 1/Z3.

This is deliberately an UPPER BOUND rather than a claimed realized metric
gain.

The literature relation after canonical normalization implies that a small
positive kinetic coefficient can at most enhance a scalar response like
1/Z before strong-coupling and localization costs are included.

ONSHELL MINIMUM-NORM BRANCH
---------------------------
Fix

    Z3 = epsilon = 1/Gamma.

Then

    x1 + x2
        =
    (epsilon - 1)/(4 c3).

The minimum-Hessian-norm solution is exactly symmetric,

    x1 = x2 = a,

with

    a =
    (epsilon - 1)/(8 c3).

The bulk field equation then determines

    x3 =
    (1-epsilon)(epsilon+3)
    /
    (16 c3 epsilon).

This is crucial.

For Gamma >> 1,

    x3 ~ 3 Gamma/(16 c3).

Thus enforcing the field equation makes the supposedly inexpensive critical
background itself increasingly anisotropic and large.

This is the central correction to 028B.

MINIMUM-NORM PROOF
------------------
Write

    u = x1 + x2

and

    x1 = u/2 + t
    x2 = u/2 - t.

The field equation fixes x3.

The Hessian norm becomes an even function of t whose coefficients are
positive on the healthy epsilon > 0 branch.

Therefore

    t = 0

is the global minimum.

No numerical optimizer is being trusted for this central result.

CUTOFF / STRONG-COUPLING GATE
-----------------------------
The soft fluctuation is canonically normalized by sqrt(Zmin).

Use the favorable strong-coupling requirement

    Lambda_eff
        =
    Lambda sqrt(Zmin)
        >=
    safety * hbar c / L_probe.

Therefore

    Lambda
        >=
    safety * hbar c
    /
    (L_probe sqrt(Zmin)).

Primary safety factor:

    10.

Also test:

    1
    100.

Blind non-evidentiary safety checks:

    0.625
    1.6
    1.875
    3.125
    5.

BACKGROUND POSITIVE INVENTORY
-----------------------------
The explicit canonical gradient contribution inside a sphere of radius R is

    E_grad
        =
    (2 pi / 15)
    Lambda^6 R^5
    (x1^2 + x2^2 + x3^2).

This is a mandatory positive field inventory.

It is used in the no-cancellation practicality ledger.

BULK COVARIANT STRESS-ENERGY
----------------------------
For the equivalent KGB form

    F = X/2
    K = -c3 X/Lambda^3

with mostly-negative metric signature, the literature KGB stress tensor is

    T_mn =
        2 F_X partial_m pi partial_n pi
        + 2 K_X box(pi) partial_m pi partial_n pi
        - partial_m K partial_n pi
        - partial_n K partial_m pi
        - g_mn F
        + g_mn partial K dot partial pi.

028C evaluates this tensor explicitly throughout the constant-Hessian bulk.

For the static diagonal background,

    rho =
        1/2 |grad pi|^2
        - 2 c3/Lambda^3
          grad(pi) . Hessian(pi) . grad(pi).

The exact signed integrated bulk energy is also reconstructed analytically
and independently by Sobol volume integration.

The signed interaction contribution is NOT allowed to erase the positive
gradient inventory without being reported as cancellation.

BOUNDARY CONDITION
------------------
The constant-Hessian solution is treated as the interior of the device.

Transition-wall energy is deliberately OMITTED.

That assumption strongly favors survival.

Therefore:

    RED despite omitted walls
        =
    strong falsification.

    GREEN
        =
    only permission to build the actual localized boundary-value problem.

SPHERICAL PHYSICAL-BRANCH CONTROL
---------------------------------
Independently reproduce the exact static spherical cubic-Galileon relation

    y + y^2 = A

in dimensionless literature normalization.

The physical branch is

    y =
    2A / (1 + sqrt(1+4A)).

Therefore

    y/A <= 1.

The cubic nonlinearity suppresses rather than amplifies the ordinary
spherically sourced response.

This is an independent limiting-case check and is not assumed to prove the
anisotropic result by itself.

028B OFF-SHELL AUDIT
--------------------
Take the actual stored 028B 006D-small primary background.

First choose c3 so that the exact cubic kinetic coefficient Z3 reproduces the
028B reported Q3.

Measure its exact bulk field-equation residual.

Then separately choose c3 so that the same Hessian is forced on-shell.

Measure the resulting Z3.

This distinguishes:

    critical but off-shell

from

    on-shell but unstable.

PRACTICALITY CASES
------------------
Test:

    IDEAL_SMALL
        C = 1
        0.1 g
        1 cm
        1 PJ

    006D_SMALL
        C = 23.591586299249
        0.1 g
        1 cm
        1 PJ

    IDEAL_MACRO
        C = 1
        1 g
        1 m
        1 TJ

    006D_MACRO
        C = 23.591586299249
        1 g
        1 m
        1 TJ.

For each theory point, Gamma is optimized rather than prescribed.

The no-cancellation energy is

    E_total
        =
    E_source/Gamma
        +
    E_grad.

The scan also records the exact signed bulk KGB energy separately.

PRIMARY OBSERVABLE
------------------
Minimum complete no-cancellation energy relative to the declared target
budget.

FALSIFICATION
-------------
DECISIVE RED:

    even the IDEAL C=1 source fails the 0.1 g / 1 cm / 1 PJ target
    under safety = 1

while

    the actual spherical branch has no nonlinear amplification.

RED:

    conservative 006D small case fails at safety = 10.

YELLOW:

    only an optimistic safety = 1 branch survives.

GREEN:

    006D small survives at safety = 10.

Even GREEN does not establish a device because transition walls and a real
localized coupled Einstein-Galileon solution remain absent.

80-PERCENT RULE
---------------
No approximate bulk calculation is allowed to set the overall practical
antigravity heuristic to 80%.

The final marker remains false unless a later complete localized solution
closes:

    gain,
    T_mn,
    control energy,
    boundaries,
    backreaction,
    stability,
    empirical consistency.

ASSUMPTIONS
-----------
- Weak gravitational backreaction for this bulk analytical gate.
- Constant-Hessian interior.
- Positive c3; c3 is set to one without loss of generality because its
  normalization can be absorbed into Lambda.
- Gain = 1/Zmin is an optimistic upper bound, not an established complete
  metric response.
- Transition walls omitted.
- No unexplained cancellation is credited toward practical energy budget.

APPROXIMATION LEVEL
-------------------
Flat-background cubic Galileon/KGB bulk plus exact quadratic fluctuation
operator.

This is stronger than 028B but still short of a fully localized nonlinear
Einstein-KGB solution.

CONSERVATION
------------
For the explicit KGB stress tensor,

    partial_mu T^{mu nu}

is proportional to the scalar field equation.

The constant-Hessian branch is required to satisfy the field equation
analytically.

STABILITY
---------
Require

    Qt > 0
    Zi > 0.

The strong-coupling scale of the soft direction must satisfy the declared
cutoff-safety margin.

ENERGY CONDITIONS
-----------------
WEC and DEC fractions of the KGB bulk are reported diagnostically.

They are not assumed automatically because healthy KGB theories can violate
ordinary matter energy conditions.

However, large negative-energy cancellation is never silently counted as a
practical benefit.

VALIDATION
----------
- 94 known-solution regression tests before the run.
- Exact algebraic field-equation identity.
- Exact minimum-norm derivation.
- Analytic signed bulk energy.
- Independent Sobol integration of T00.
- Spherical Vainshtein limiting-case reconstruction.
- Stored 028B background independently re-tested against exact cubic
  equations.
- Smoke test before full run.

RELATED FILES
-------------
results/data/028b_critical_braiding_gain_summary.json
results/data/028a_metric_gain_localization_gate_summary.json
results/data/027d_exact_self_closing_stress_summary.json

OUTPUTS
-------
results/data/028c_onshell_cubic_braiding_closure_summary.json
results/data/028c_onshell_cubic_braiding_cases.csv
results/data/028c_target_gain_audit.csv
results/data/028c_wildcard_audit.csv

CLAIM CLASSIFICATION
--------------------
TRUE_ANTIGRAVITY_GAIN_ENGINE_EXPLICIT_ONSHELL_CUBIC_KGB_GATE

WHAT THIS FILE DOES NOT ESTABLISH
--------------------------------
It does not establish:

- a practical antigravity device;
- a full localized KGB device;
- a nonlinear Einstein-KGB solution;
- boundary-wall closure;
- empirical compatibility;
- complete actual metric gain;
- escape from all possible modified-gravity gain mechanisms.
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import qmc


C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
G0 = 9.80665

HBARC_EV_M = 1.973269804e-7
EV_J = 1.602176634e-19

C_006D = 23.591586299249

C3 = 1.0
PRIMARY_SAFETY = 10.0

BUDGET_SMALL = 1.0e15
BUDGET_MACRO = 1.0e12

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

P028B = DATA / "028b_critical_braiding_gain_summary.json"
P028A = DATA / "028a_metric_gain_localization_gate_summary.json"
P027D = DATA / "027d_exact_self_closing_stress_summary.json"

OUT = DATA / "028c_onshell_cubic_braiding_closure_summary.json"
CASES_CSV = DATA / "028c_onshell_cubic_braiding_cases.csv"
TARGET_CSV = DATA / "028c_target_gain_audit.csv"
WILD_CSV = DATA / "028c_wildcard_audit.csv"

SMOKE = os.environ.get("AG028C_SMOKE", "0") == "1"


if SMOKE:
    REGION_RATIOS = (
        1.0,
    )

    PHYSICAL_SAFETIES = (
        1.0,
        10.0,
    )

    STRESS_SAMPLES = 2 ** 10

else:
    REGION_RATIOS = (
        0.5,
        1.0,
        2.0,
    )

    PHYSICAL_SAFETIES = (
        1.0,
        10.0,
        100.0,
    )

    STRESS_SAMPLES = 2 ** 15


WILDCARDS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


SCENARIOS = (
    (
        "IDEAL_SMALL",
        1.0,
        0.1 * G0,
        0.01,
        BUDGET_SMALL,
    ),
    (
        "006D_SMALL",
        C_006D,
        0.1 * G0,
        0.01,
        BUDGET_SMALL,
    ),
    (
        "IDEAL_MACRO",
        1.0,
        G0,
        1.0,
        BUDGET_MACRO,
    ),
    (
        "006D_MACRO",
        C_006D,
        G0,
        1.0,
        BUDGET_MACRO,
    ),
)


def load_json(path: Path) -> dict:
    """Load one required lineage result."""

    if not path.is_file():
        raise FileNotFoundError(
            f"Required lineage missing: {path}"
        )

    return json.loads(
        path.read_text(
            encoding="utf-8",
        )
    )


J028B = load_json(P028B)
J028A = load_json(P028A)
J027D = load_json(P027D)


if not str(
    J028B.get(
        "decision",
        "",
    )
).startswith(
    "YELLOW_"
):
    raise RuntimeError(
        "028C expects the completed YELLOW 028B lineage"
    )


def source_energy(
    coefficient: float,
    acceleration: float,
    h: float,
    gamma: float,
) -> float:
    """Return amplified true-stand-off source energy in joules."""

    return (
        coefficient
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


def source_only_target_gamma(
    coefficient: float,
    acceleration: float,
    h: float,
    budget: float,
) -> float:
    """Return gain that would make source energy alone equal the budget."""

    return (
        coefficient
        * acceleration
        * C_LIGHT
        ** 2
        * h
        ** 2
        / (
            G_NEWTON
            * budget
        )
    )


def onshell_branch(
    gamma: float,
) -> dict:
    """Construct the exact minimum-Hessian-norm on-shell branch."""

    if gamma <= 1.0:
        raise ValueError(
            "Gamma must exceed one"
        )

    epsilon = (
        1.0
        / gamma
    )

    a = (
        epsilon
        - 1.0
    ) / (
        8.0
        * C3
    )

    b = (
        (
            1.0
            - epsilon
        )
        * (
            epsilon
            + 3.0
        )
    ) / (
        16.0
        * C3
        * epsilon
    )

    x = np.array(
        [
            a,
            a,
            b,
        ],
        dtype=float,
    )

    trace = float(
        np.sum(
            x
        )
    )

    pair = float(
        x[0]
        * x[1]
        + x[0]
        * x[2]
        + x[1]
        * x[2]
    )

    eom = (
        trace
        + 4.0
        * C3
        * pair
    )

    qt = (
        1.0
        + 4.0
        * C3
        * trace
    )

    z1 = (
        1.0
        + 4.0
        * C3
        * (
            a
            + b
        )
    )

    z = np.array(
        [
            z1,
            z1,
            epsilon,
        ],
        dtype=float,
    )

    zmin = float(
        min(
            qt,
            *z,
        )
    )

    if zmin <= 0.0:
        raise RuntimeError(
            "On-shell branch became unstable"
        )

    return {
        "gamma":
            gamma,

        "epsilon":
            epsilon,

        "x":
            x,

        "trace":
            trace,

        "pair":
            pair,

        "EOM_residual":
            eom,

        "Qt":
            qt,

        "Z":
            z,

        "Zmin":
            zmin,

        "xnorm2":
            float(
                np.dot(
                    x,
                    x,
                )
            ),

        "c1_sq":
            float(
                z[
                    0
                ]
                / qt
            ),

        "c2_sq":
            float(
                z[
                    1
                ]
                / qt
            ),

        "c3_sq":
            float(
                z[
                    2
                ]
                / qt
            ),
    }


def state_energy(
    gamma: float,
    h: float,
    region_ratio: float,
    safety: float,
) -> dict:
    """Return exact on-shell bulk state and mandatory positive energy."""

    state = onshell_branch(
        gamma
    )

    radius = (
        h
        * region_ratio
    )

    probe = min(
        h,
        radius,
    )

    bare_cutoff_eV = (
        safety
        * HBARC_EV_M
        / (
            probe
            * math.sqrt(
                state[
                    "Zmin"
                ]
            )
        )
    )

    radius_evinv = (
        radius
        / HBARC_EV_M
    )

    prefactor_eV = (
        2.0
        * math.pi
        / 15.0
        * bare_cutoff_eV
        ** 6
        * radius_evinv
        ** 5
    )

    x = state[
        "x"
    ]

    e_gradient_j = (
        prefactor_eV
        * state[
            "xnorm2"
        ]
        * EV_J
    )

    signed_factor = float(
        np.sum(
            x
            ** 2
        )
        - 4.0
        * C3
        * np.sum(
            x
            ** 3
        )
    )

    e_bulk_signed_j = (
        prefactor_eV
        * signed_factor
        * EV_J
    )

    state.update(
        {
            "R_m":
                radius,

            "bare_cutoff_eV":
                bare_cutoff_eV,

            "effective_soft_cutoff_eV":
                (
                    bare_cutoff_eV
                    * math.sqrt(
                        state[
                            "Zmin"
                        ]
                    )
                ),

            "E_gradient_J":
                e_gradient_j,

            "E_bulk_signed_J":
                e_bulk_signed_j,

            "signed_over_gradient":
                (
                    e_bulk_signed_j
                    / e_gradient_j
                ),
        }
    )

    return state


def stress_audit(
    state: dict,
    nsamp: int,
) -> dict:
    """Evaluate the explicit KGB bulk T_mn on a Sobol sphere."""

    x = state[
        "x"
    ]

    power = int(
        round(
            math.log2(
                nsamp
            )
        )
    )

    u = qmc.Sobol(
        d=3,
        scramble=True,
        seed=2803,
    ).random_base2(
        power
    )

    radius = (
        u[
            :,
            0,
        ]
        ** (
            1.0
            / 3.0
        )
    )

    mu = (
        2.0
        * u[
            :,
            1,
        ]
        - 1.0
    )

    phi = (
        2.0
        * math.pi
        * u[
            :,
            2,
        ]
    )

    sint = np.sqrt(
        np.maximum(
            0.0,
            1.0
            - mu
            * mu,
        )
    )

    y = np.column_stack(
        (
            radius
            * sint
            * np.cos(
                phi
            ),

            radius
            * sint
            * np.sin(
                phi
            ),

            radius
            * mu,
        )
    )

    grad = (
        x[
            None,
            :,
        ]
        * y
    )

    grad2 = np.sum(
        grad
        * grad,
        axis=1,
    )

    cubic_coordinate = np.sum(
        (
            x
            ** 3
        )[
            None,
            :,
        ]
        * (
            y
            * y
        ),
        axis=1,
    )

    rho = (
        0.5
        * grad2
        - 2.0
        * C3
        * cubic_coordinate
    )

    scalar = (
        -0.5
        * grad2
        + 2.0
        * C3
        * cubic_coordinate
    )

    coeff = np.empty(
        (
            3,
            3,
        ),
        dtype=float,
    )

    trace = state[
        "trace"
    ]

    for i in range(
        3
    ):
        for j in range(
            3
        ):
            coeff[
                i,
                j,
            ] = (
                1.0
                + 2.0
                * C3
                * trace
                - 2.0
                * C3
                * (
                    x[
                        i
                    ]
                    + x[
                        j
                    ]
                )
            )

    stress = np.empty(
        (
            len(
                y
            ),
            3,
            3,
        ),
        dtype=float,
    )

    for row in range(
        len(
            y
        )
    ):
        stress[
            row
        ] = (
            np.outer(
                grad[
                    row
                ],
                grad[
                    row
                ],
            )
            * coeff
            + np.eye(
                3
            )
            * scalar[
                row
            ]
        )

    eigenvalues = np.linalg.eigvalsh(
        stress
    )

    wec = np.logical_and(
        rho >= 0.0,
        np.min(
            rho[
                :,
                None,
            ]
            + eigenvalues,
            axis=1,
        )
        >= 0.0,
    )

    dec = np.logical_and(
        rho >= 0.0,
        np.max(
            np.abs(
                eigenvalues
            ),
            axis=1,
        )
        <= (
            rho
            + 1.0e-12
        ),
    )

    volume = (
        4.0
        * math.pi
        / 3.0
    )

    radius_evinv = (
        state[
            "R_m"
        ]
        / HBARC_EV_M
    )

    scale_eV = (
        state[
            "bare_cutoff_eV"
        ]
        ** 6
        * radius_evinv
        ** 5
    )

    e_abs_mc_j = (
        scale_eV
        * volume
        * float(
            np.mean(
                np.abs(
                    rho
                )
            )
        )
        * EV_J
    )

    e_signed_mc_j = (
        scale_eV
        * volume
        * float(
            np.mean(
                rho
            )
        )
        * EV_J
    )

    signed_relerr = (
        abs(
            e_signed_mc_j
            - state[
                "E_bulk_signed_J"
            ]
        )
        / max(
            abs(
                state[
                    "E_bulk_signed_J"
                ]
            ),
            1.0e-300,
        )
    )

    return {
        "sample_count":
            len(
                y
            ),

        "rho_min_dimensionless":
            float(
                np.min(
                    rho
                )
            ),

        "rho_max_dimensionless":
            float(
                np.max(
                    rho
                )
            ),

        "WEC_fraction":
            float(
                np.mean(
                    wec
                )
            ),

        "DEC_fraction":
            float(
                np.mean(
                    dec
                )
            ),

        "E_abs_MC_J":
            e_abs_mc_j,

        "E_signed_MC_J":
            e_signed_mc_j,

        "signed_MC_relative_error":
            signed_relerr,
    }


def optimize_case(
    coefficient: float,
    acceleration: float,
    h: float,
    budget: float,
    region_ratio: float,
    safety: float,
) -> dict:
    """Minimize source plus mandatory positive background inventory."""

    def total_from_log_gamma(
        log_gamma: float,
    ) -> float:

        gamma = (
            10.0
            ** log_gamma
        )

        state = state_energy(
            gamma,
            h,
            region_ratio,
            safety,
        )

        return (
            source_energy(
                coefficient,
                acceleration,
                h,
                gamma,
            )
            + state[
                "E_gradient_J"
            ]
        )

    solution = minimize_scalar(
        lambda x: math.log(
            total_from_log_gamma(
                x
            )
        ),
        bounds=(
            1.0e-8,
            20.0,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-10,
        },
    )

    gamma = (
        10.0
        ** solution.x
    )

    state = state_energy(
        gamma,
        h,
        region_ratio,
        safety,
    )

    e_source = source_energy(
        coefficient,
        acceleration,
        h,
        gamma,
    )

    e_no_cancel = (
        e_source
        + state[
            "E_gradient_J"
        ]
    )

    compactness = (
        2.0
        * G_NEWTON
        * max(
            abs(
                state[
                    "E_bulk_signed_J"
                ]
            ),
            state[
                "E_gradient_J"
            ],
        )
        / (
            C_LIGHT
            ** 4
            * state[
                "R_m"
            ]
        )
    )

    return {
        "gamma_opt":
            gamma,

        "E_source_J":
            e_source,

        "E_gradient_J":
            state[
                "E_gradient_J"
            ],

        "E_no_cancel_J":
            e_no_cancel,

        "budget_ratio":
            e_no_cancel
            / budget,

        "meets_budget":
            bool(
                e_no_cancel
                <= budget
            ),

        "compactness_proxy":
            compactness,

        "Qt":
            state[
                "Qt"
            ],

        "Z1":
            state[
                "Z"
            ][
                0
            ],

        "Z2":
            state[
                "Z"
            ][
                1
            ],

        "Z3":
            state[
                "Z"
            ][
                2
            ],

        "c1_sq":
            state[
                "c1_sq"
            ],

        "c2_sq":
            state[
                "c2_sq"
            ],

        "c3_sq":
            state[
                "c3_sq"
            ],

        "x1":
            state[
                "x"
            ][
                0
            ],

        "x2":
            state[
                "x"
            ][
                1
            ],

        "x3":
            state[
                "x"
            ][
                2
            ],

        "EOM_residual":
            state[
                "EOM_residual"
            ],

        "bare_cutoff_eV":
            state[
                "bare_cutoff_eV"
            ],

        "effective_soft_cutoff_eV":
            state[
                "effective_soft_cutoff_eV"
            ],

        "E_bulk_signed_J":
            state[
                "E_bulk_signed_J"
            ],

        "signed_over_gradient":
            state[
                "signed_over_gradient"
            ],
    }


def audit_028b_background() -> dict:
    """Test the stored 028B primary background against exact cubic equations."""

    row = J028B[
        "selected_cases"
    ][
        "006D_SMALL"
    ][
        "primary"
    ]

    x = np.array(
        [
            row[
                "x1"
            ],
            row[
                "x2"
            ],
            row[
                "x3"
            ],
        ],
        dtype=float,
    )

    q3_reported = float(
        row[
            "Q3"
        ]
    )

    u = (
        x[
            0
        ]
        + x[
            1
        ]
    )

    trace = float(
        np.sum(
            x
        )
    )

    pair = float(
        x[
            0
        ]
        * x[
            1
        ]
        + x[
            0
        ]
        * x[
            2
        ]
        + x[
            1
        ]
        * x[
            2
        ]
    )

    c3_matching_q3 = (
        q3_reported
        - 1.0
    ) / (
        4.0
        * u
    )

    eom_residual_at_match = (
        trace
        + 4.0
        * c3_matching_q3
        * pair
    )

    c3_required_onshell = (
        -trace
        / (
            4.0
            * pair
        )
    )

    z3_if_same_hessian_onshell = (
        1.0
        + 4.0
        * c3_required_onshell
        * u
    )

    return {
        "x":
            x.tolist(),

        "reported_Q3":
            q3_reported,

        "c3_matching_reported_Q3":
            c3_matching_q3,

        "EOM_residual_at_matching_c3":
            eom_residual_at_match,

        "c3_required_for_bulk_EOM":
            c3_required_onshell,

        "Z3_if_same_Hessian_forced_onshell":
            z3_if_same_hessian_onshell,
    }


def spherical_vainshtein_control() -> dict:
    """Independently verify that the physical spherical branch is screened."""

    source_strength = np.logspace(
        -12.0,
        12.0,
        2000,
    )

    field = (
        2.0
        * source_strength
        / (
            1.0
            + np.sqrt(
                1.0
                + 4.0
                * source_strength
            )
        )
    )

    ratio = (
        field
        / source_strength
    )

    return {
        "samples":
            len(
                source_strength
            ),

        "max_force_ratio_to_unscreened":
            float(
                np.max(
                    ratio
                )
            ),

        "min_force_ratio_to_unscreened":
            float(
                np.min(
                    ratio
                )
            ),

        "all_force_ratios_le_one":
            bool(
                np.all(
                    ratio
                    <= 1.0
                    + 1.0e-13
                )
            ),
    }


print(
    "=== 028C LINEAGE ===",
    flush=True,
)

print(
    (
        "028B_DECISION="
        + str(
            J028B.get(
                "decision"
            )
        )
    ),
    flush=True,
)

print(
    (
        "028A_DECISION="
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
        "027D_DECISION="
        + str(
            J027D.get(
                "decision"
            )
        )
    ),
    flush=True,
)


off_shell_audit = audit_028b_background()
spherical_control = spherical_vainshtein_control()


print(
    "\n=== 028B EXACT ONSHELL AUDIT ===",
    flush=True,
)

print(
    (
        "028B_MATCHING_C3="
        f"{off_shell_audit['c3_matching_reported_Q3']:.15e}"
    ),
    flush=True,
)

print(
    (
        "028B_EOM_RESIDUAL_AT_MATCH="
        f"{off_shell_audit['EOM_residual_at_matching_c3']:.15e}"
    ),
    flush=True,
)

print(
    (
        "028B_C3_REQUIRED_ONSHELL="
        f"{off_shell_audit['c3_required_for_bulk_EOM']:.15e}"
    ),
    flush=True,
)

print(
    (
        "028B_Z3_IF_SAME_HESSIAN_FORCED_ONSHELL="
        f"{off_shell_audit['Z3_if_same_Hessian_forced_onshell']:.15e}"
    ),
    flush=True,
)


print(
    "\n=== SPHERICAL PHYSICAL-BRANCH CONTROL ===",
    flush=True,
)

print(
    (
        "SPHERICAL_FORCE_RATIO_MAX="
        f"{spherical_control['max_force_ratio_to_unscreened']:.15e}"
    ),
    flush=True,
)

print(
    (
        "SPHERICAL_FORCE_RATIO_MIN="
        f"{spherical_control['min_force_ratio_to_unscreened']:.15e}"
    ),
    flush=True,
)

print(
    (
        "SPHERICAL_NONLINEAR_AMPLIFICATION_FOUND="
        + (
            "NO"
            if spherical_control[
                "all_force_ratios_le_one"
            ]
            else "YES"
        )
    ),
    flush=True,
)


cases = []


for (
    case_name,
    coefficient,
    acceleration,
    h,
    budget,
) in SCENARIOS:

    print(
        (
            "\n028C_CASE_BEGIN "
            f"CASE={case_name}"
        ),
        flush=True,
    )

    for region_ratio in REGION_RATIOS:
        for safety in PHYSICAL_SAFETIES:

            result = optimize_case(
                coefficient,
                acceleration,
                h,
                budget,
                region_ratio,
                safety,
            )

            result.update(
                {
                    "case":
                        case_name,

                    "C_source":
                        coefficient,

                    "acceleration_m_s2":
                        acceleration,

                    "h_m":
                        h,

                    "budget_J":
                        budget,

                    "region_ratio":
                        region_ratio,

                    "safety":
                        safety,

                    "selection_role":
                        "PHYSICAL",
                }
            )

            cases.append(
                result
            )

            print(
                (
                    "028C_CASE_RESULT "
                    f"CASE={case_name} "
                    f"RREG={region_ratio:.6g} "
                    f"SAFETY={safety:.6g} "
                    f"GAMMA={result['gamma_opt']:.12e} "
                    f"E={result['E_no_cancel_J']:.12e} "
                    f"RATIO={result['budget_ratio']:.12e} "
                    f"X3={result['x3']:.12e} "
                    f"Z3={result['Z3']:.12e} "
                    f"EOM={result['EOM_residual']:.3e}"
                ),
                flush=True,
            )


primary = {}
optimistic = {}


for (
    case_name,
    _coefficient,
    _acceleration,
    _h,
    _budget,
) in SCENARIOS:

    rows = [
        row
        for row in cases
        if row[
            "case"
        ]
        == case_name
    ]

    primary_rows = [
        row
        for row in rows
        if abs(
            row[
                "safety"
            ]
            - PRIMARY_SAFETY
        )
        < 1.0e-12
    ]

    primary[
        case_name
    ] = min(
        primary_rows,
        key=lambda row: row[
            "E_no_cancel_J"
        ],
    )

    optimistic[
        case_name
    ] = min(
        rows,
        key=lambda row: row[
            "E_no_cancel_J"
        ],
    )


wildcards = []


for safety in WILDCARDS:

    result = optimize_case(
        C_006D,
        0.1
        * G0,
        0.01,
        BUDGET_SMALL,
        1.0,
        safety,
    )

    wildcards.append(
        {
            "safety":
                safety,

            "gamma_opt":
                result[
                    "gamma_opt"
                ],

            "E_no_cancel_J":
                result[
                    "E_no_cancel_J"
                ],

            "budget_ratio":
                result[
                    "budget_ratio"
                ],

            "selection_role":
                "BLIND_NON_EVIDENTIARY_EXCLUDED",
        }
    )


targets = []


for (
    case_name,
    coefficient,
    acceleration,
    h,
    budget,
) in SCENARIOS:

    gamma = source_only_target_gamma(
        coefficient,
        acceleration,
        h,
        budget,
    )

    state = state_energy(
        gamma,
        h,
        1.0,
        PRIMARY_SAFETY,
    )

    targets.append(
        {
            "case":
                case_name,

            "gamma_source_only_budget":
                gamma,

            "x3_onshell":
                state[
                    "x"
                ][
                    2
                ],

            "Qt":
                state[
                    "Qt"
                ],

            "Z1":
                state[
                    "Z"
                ][
                    0
                ],

            "Z3":
                state[
                    "Z"
                ][
                    2
                ],

            "E_gradient_J_safety10":
                state[
                    "E_gradient_J"
                ],

            "E_bulk_signed_J_safety10":
                state[
                    "E_bulk_signed_J"
                ],

            "bare_cutoff_eV_safety10":
                state[
                    "bare_cutoff_eV"
                ],

            "signed_over_gradient":
                state[
                    "signed_over_gradient"
                ],
        }
    )


primary_006d_small_state = state_energy(
    primary[
        "006D_SMALL"
    ][
        "gamma_opt"
    ],
    0.01,
    primary[
        "006D_SMALL"
    ][
        "region_ratio"
    ],
    PRIMARY_SAFETY,
)


stress = stress_audit(
    primary_006d_small_state,
    STRESS_SAMPLES,
)


max_eom_residual = max(
    abs(
        row[
            "EOM_residual"
        ]
    )
    for row in cases
)


if max_eom_residual > 1.0e-5:
    raise RuntimeError(
        (
            "On-shell algebra failed: "
            f"max EOM residual={max_eom_residual}"
        )
    )


if (
    not spherical_control[
        "all_force_ratios_le_one"
    ]
):
    raise RuntimeError(
        "Spherical Vainshtein limiting-case validation failed"
    )


if (
    stress[
        "signed_MC_relative_error"
    ]
    > 2.0e-4
):
    raise RuntimeError(
        (
            "Independent T00 integration failed: "
            f"relative error={stress['signed_MC_relative_error']}"
        )
    )


ideal_small_safety1 = min(
    (
        row
        for row in cases
        if (
            row[
                "case"
            ]
            == "IDEAL_SMALL"
            and abs(
                row[
                    "safety"
                ]
                - 1.0
            )
            < 1.0e-12
        )
    ),
    key=lambda row: row[
        "E_no_cancel_J"
    ],
)


sixd_small_safety1 = min(
    (
        row
        for row in cases
        if (
            row[
                "case"
            ]
            == "006D_SMALL"
            and abs(
                row[
                    "safety"
                ]
                - 1.0
            )
            < 1.0e-12
        )
    ),
    key=lambda row: row[
        "E_no_cancel_J"
    ],
)


if (
    not ideal_small_safety1[
        "meets_budget"
    ]
    and not sixd_small_safety1[
        "meets_budget"
    ]
):
    decision = (
        "DECISIVE_RED_ONSHELL_CUBIC_BRAIDING_"
        "CLOSES_028B_SUBSCALE_WINDOW"
    )

    next_step = (
        "CLOSE_028A_THROUGH_028C_LOCAL_SCALAR_GAIN_CLASSES_"
        "AND_PRESERVE_006D_AS_TRUE_STANDOFF_BASELINE"
    )

elif primary[
    "006D_SMALL"
][
    "meets_budget"
]:
    decision = (
        "GREEN_006D_SMALL_ONSHELL_BULK_UPPER_BOUND_SURVIVES"
    )

    next_step = (
        "ONLY_THEN_BUILD_FULL_LOCALIZED_EINSTEIN_KGB_"
        "BOUNDARY_VALUE_PROBLEM"
    )

elif primary[
    "IDEAL_SMALL"
][
    "meets_budget"
]:
    decision = (
        "YELLOW_IDEAL_SMALL_ONSHELL_BULK_SURVIVES_"
        "BUT_006D_DOES_NOT"
    )

    next_step = (
        "DO_NOT_PROMOTE_GAIN_ENGINE; "
        "SOURCE_COEFFICIENT_AND_LOCALIZATION_GAPS_REMAIN"
    )

elif sixd_small_safety1[
    "meets_budget"
]:
    decision = (
        "YELLOW_ONLY_SAFETY1_006D_SMALL_SURVIVES"
    )

    next_step = (
        "CUTOFF_MARGIN_MUST_BE_CLOSED_BEFORE_ANY_FIELD_REALIZATION"
    )

else:
    decision = (
        "RED_PRIMARY_ONSHELL_CUBIC_BRAIDING_"
        "SUBSCALE_WINDOW"
    )

    next_step = (
        "CLOSE_CUBIC_CRITICAL_BRAIDING_AS_PRACTICAL_GAIN_ENGINE"
    )


summary = {
    "branch":
        "TRUE_ANTIGRAVITY_GAIN_ENGINE",

    "simulation":
        "028C",

    "question":
        (
            "Can the 028B subscale critical-braiding window survive "
            "the exact cubic Galileon bulk equation of motion, explicit "
            "KGB stress-energy, and strong-coupling energy ledger?"
        ),

    "lineage": {
        "028B":
            J028B.get(
                "decision"
            ),

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

    "model": {
        "c3":
            C3,

        "gain_upper_bound":
            "Gamma = 1/Z3",

        "bulk_EOM":
            "s + 4 c3 (x1*x2+x1*x3+x2*x3) = 0",

        "fluctuation_kinetic":
            (
                "Qt=1+4c3*s; "
                "Zi=1+4c3*(s-xi)"
            ),

        "onshell_minimum_norm":
            (
                "x1=x2=(epsilon-1)/(8c3); "
                "x3=(1-epsilon)(epsilon+3)/(16c3*epsilon)"
            ),

        "transition_wall_energy":
            "OMITTED_FAVORABLE_ASSUMPTION",
    },

    "028B_offshell_audit":
        off_shell_audit,

    "spherical_control":
        spherical_control,

    "primary_cases":
        primary,

    "optimistic_cases":
        optimistic,

    "ideal_small_safety1":
        ideal_small_safety1,

    "006D_small_safety1":
        sixd_small_safety1,

    "target_gain_audit":
        targets,

    "stress_audit_006D_small_primary":
        stress,

    "validation": {
        "max_onshell_EOM_residual":
            max_eom_residual,

        "stress_signed_MC_relative_error":
            stress[
                "signed_MC_relative_error"
            ],

        "spherical_force_ratio_le_one":
            spherical_control[
                "all_force_ratios_le_one"
            ],
    },

    "decision":
        decision,

    "next":
        next_step,

    "gain_engine_80_heuristic_authorized":
        False,

    "overall_practical_antigravity_80_heuristic_authorized":
        False,

    "mandatory_parallel_credibility_branch":
        "026C_N89_FORCE_CONVERGENCE",

    "claims": {
        "explicit_bulk_KGB_Tmunu_evaluated":
            True,

        "bulk_field_equation_imposed":
            True,

        "full_localized_covariant_solution":
            False,

        "transition_wall_energy_included":
            False,

        "actual_complete_metric_gain_proven":
            False,

        "empirical_consistency_closed":
            False,

        "nonlinear_Einstein_KGB":
            False,

        "practical_antigravity_device":
            False,
    },
}


DATA.mkdir(
    parents=True,
    exist_ok=True,
)


OUT.write_text(
    json.dumps(
        summary,
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
    ),
    encoding="utf-8",
)


with CASES_CSV.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=list(
            cases[
                0
            ].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(
        cases
    )


with TARGET_CSV.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=list(
            targets[
                0
            ].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(
        targets
    )


with WILD_CSV.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=list(
            wildcards[
                0
            ].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(
        wildcards
    )


print(
    "\n=== 028C FINAL ONSHELL CUBIC-BRAIDING CLOSURE GATE ===",
    flush=True,
)


print(
    (
        "028B_REPORTED_DECISION="
        + str(
            J028B.get(
                "decision"
            )
        )
    ),
    flush=True,
)


print(
    (
        "028B_MATCH_C3="
        f"{off_shell_audit['c3_matching_reported_Q3']:.15e}"
    ),
    flush=True,
)


print(
    (
        "028B_EOM_RESIDUAL_AT_MATCH="
        f"{off_shell_audit['EOM_residual_at_matching_c3']:.15e}"
    ),
    flush=True,
)


print(
    (
        "028B_C3_REQUIRED_ONSHELL="
        f"{off_shell_audit['c3_required_for_bulk_EOM']:.15e}"
    ),
    flush=True,
)


print(
    (
        "028B_Z3_IF_SAME_HESSIAN_FORCED_ONSHELL="
        f"{off_shell_audit['Z3_if_same_Hessian_forced_onshell']:.15e}"
    ),
    flush=True,
)


print(
    (
        "SPHERICAL_FORCE_RATIO_MAX="
        f"{spherical_control['max_force_ratio_to_unscreened']:.15e}"
    ),
    flush=True,
)


for name in (
    "IDEAL_SMALL",
    "006D_SMALL",
    "IDEAL_MACRO",
    "006D_MACRO",
):

    row = primary[
        name
    ]

    opt = optimistic[
        name
    ]

    print(
        (
            f"{name}_PRIMARY "
            f"GAMMA={row['gamma_opt']:.12e} "
            f"E={row['E_no_cancel_J']:.12e} "
            f"RATIO={row['budget_ratio']:.12e} "
            f"X3={row['x3']:.12e} "
            f"Z3={row['Z3']:.12e} "
            f"SAFETY={row['safety']:.6g} "
            f"RREG={row['region_ratio']:.6g}"
        ),
        flush=True,
    )

    print(
        (
            f"{name}_OPTIMISTIC "
            f"GAMMA={opt['gamma_opt']:.12e} "
            f"E={opt['E_no_cancel_J']:.12e} "
            f"RATIO={opt['budget_ratio']:.12e} "
            f"SAFETY={opt['safety']:.6g} "
            f"RREG={opt['region_ratio']:.6g}"
        ),
        flush=True,
    )


print(
    (
        "006D_SMALL_SAFETY1_BUDGET_RATIO="
        f"{sixd_small_safety1['budget_ratio']:.15e}"
    ),
    flush=True,
)


print(
    (
        "IDEAL_SMALL_SAFETY1_BUDGET_RATIO="
        f"{ideal_small_safety1['budget_ratio']:.15e}"
    ),
    flush=True,
)


print(
    (
        "006D_SMALL_PRIMARY_WEC_FRACTION="
        f"{stress['WEC_fraction']:.15e}"
    ),
    flush=True,
)


print(
    (
        "006D_SMALL_PRIMARY_DEC_FRACTION="
        f"{stress['DEC_fraction']:.15e}"
    ),
    flush=True,
)


print(
    (
        "006D_SMALL_PRIMARY_E_ABS_BULK_J="
        f"{stress['E_abs_MC_J']:.15e}"
    ),
    flush=True,
)


print(
    (
        "006D_SMALL_PRIMARY_SIGNED_BULK_OVER_GRAD="
        f"{primary['006D_SMALL']['signed_over_gradient']:.15e}"
    ),
    flush=True,
)


print(
    (
        "INDEPENDENT_T00_MC_RELERR="
        f"{stress['signed_MC_relative_error']:.15e}"
    ),
    flush=True,
)


print(
    (
        "MAX_ONSHELL_EOM_RESIDUAL="
        f"{max_eom_residual:.15e}"
    ),
    flush=True,
)


print(
    f"028C_DECISION={decision}",
    flush=True,
)


print(
    f"NEXT={next_step}",
    flush=True,
)


print(
    "GAIN_ENGINE_80_HEURISTIC_AUTHORIZED=NO",
    flush=True,
)


print(
    "OVERALL_PRACTICAL_ANTIGRAVITY_80_HEURISTIC_AUTHORIZED=NO",
    flush=True,
)


print(
    "BOUNDARY_WALL_ENERGY_INCLUDED=NO",
    flush=True,
)


print(
    "ACTUAL_COMPLETE_METRIC_GAIN_PROVEN=NO",
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
    "028C_RUN_COMPLETE=YES",
    flush=True,
)
