#!/usr/bin/env python3
"""030A — dynamic pure-GR impulse / gravitational-memory scaling gate.

PURPOSE
-------
Rebuild the project around a genuinely time-dependent observable after 029A
closed the tested static sign-source + local-gain program.

The primary observable is the complete-cycle payload impulse

    Delta v = integral a_payload(t) dt.

The central question is:

    Can time dependence evade the absolute 1/G practicality scaling that
    survived every tested static source and local-gain branch?

Two physically distinct dynamic mechanisms are tested.

A. REUSABLE NEAR-ZONE PULSE CONTROL
-----------------------------------
For a linearized source whose peak field has coefficient C_peak,

    E_peak = C_peak a_peak c^2 h^2 / G.

If the complete pulse envelope has mean duty factor D <= 1,

    a_average = D a_peak,

and therefore

    E_peak
      =
    C_peak a_average c^2 h^2 / (G D).

Thus lowering duty cycle cannot lower required peak stored field energy in
this linear-response control.

It either leaves the minimum unchanged at D=1 or makes it worse.

The run includes:

    C_peak = 1

as an intentionally favorable source-side oracle, and

    C_006D = 23.591586299249

as the strongest conservative true-stand-off source.

The raw Introspective teacher coefficient is included only as a diagnostic
oracle and is explicitly not treated as a continuum-certified field.

B. RADIATIVE / MEMORY IMPULSE
-----------------------------
For a weak transverse-traceless gravitational wave packet define

    H =
        [[h_plus,  h_cross],
         [h_cross, -h_plus]].

Geodesic deviation gives

    xi'' = (1/2) H'' xi.

For compact strain pulses satisfying

    H = 0
    H' = 0

before and after the burst, the first-order residual velocity vanishes.

At second order in the weak TT expansion,

    Delta v_parallel / L
      =
    -(1/4)
    integral
    [
        h_plus_dot^2
        +
        h_cross_dot^2
    ]
    dt

for this compact-pulse class.

Therefore its weak second-order radial velocity memory is inward.

029A does not use this sign statement as a universal theorem against every
gravitational-wave velocity-memory observable.

Instead 030A additionally gives a hypothetical outward memory mechanism an
explicit oracle:

    |Delta v|
        <=
    chi L I

with

    I
      =
    integral
    [
        h_plus_dot^2
        +
        h_cross_dot^2
    ]
    dt.

The run then solves for the value of chi required for practicality.

GRAVITATIONAL-WAVE ENERGY
-------------------------
Use the standard weak-wave energy fluence

    E_beam / A
      =
    c^3 I / (32 pi G).

To prevent ordinary source recoil from masquerading as antigravity, the
primary practicality ledger uses two opposite gravitational-wave beams.

Their net emitted linear momentum cancels.

Only one interacts with the payload.

This doubles the radiated energy and provides a deliberately conservative
recoil-free interpretation.

FINITE PAYLOAD
--------------
Use a spherical payload radius

    R_payload = 0.1 h.

The most favorable beam footprint that still covers the payload is

    A = pi R_payload^2

so define

    beta = A / (pi h^2) = 0.01.

For sustained average acceleration a, the recoil-balanced paired-beam power
floor becomes

    P_pair
      >=
    beta a c^3 h / (16 G chi).

Crucially, this power is independent of pulse repetition time.

Shorter pulses reduce energy per pulse but require proportionally more pulses.

PRACTICAL TARGETS
-----------------
Primary target:

    a = 1 g
    h = 1 m
    one-second total energy expenditure <= 1 TJ

so the dynamic power budget is

    1 TW.

Secondary generous target:

    a = 0.1 g
    h = 1 cm
    one-second energy expenditure <= 1 PJ.

Using a one-second mission window strongly favors the dynamic mechanism.
Longer sustained operation simply multiplies radiated energy.

COMPACT-WAVE NUMERICAL VALIDATION
---------------------------------
Generate smooth randomized polarized waveforms

    h_A(theta)
      =
    sin^2(pi theta)
    times
    a finite Fourier series

for

    0 <= theta <= 1.

The envelope guarantees

    h(0)=h(1)=0

and

    h'(0)=h'(1)=0.

Each waveform is normalized to

    integral
    (
        h_plus'^2
        +
        h_cross'^2
    )
    dtheta
    =
    1.

Integrate the full geodesic-deviation equation at amplitudes

    A
    and
    A/2.

Require:

    Delta v_parallel / A^2
        ~= -1/4

and

    Delta v(A)
    /
    Delta v(A/2)
        ~= 4.

The second-order identity is analytically known within this approximation;
the randomized calculation is an independent numerical reconstruction.

FIRST-ORDER DISPLACEMENT MEMORY
-------------------------------
A waveform may end with nonzero strain while its time derivative returns to
zero.

At first perturbative order,

    Delta v
      =
    (1/2)
    [
        H'
    ]_initial^final
    xi

so ordinary displacement memory does not by itself provide a residual
first-order payload velocity.

The displacement can remain permanent while the first-order final velocity is
zero.

OUTWARD-MEMORY ORACLE
---------------------
Because more general velocity-memory effects exist outside the compact weak-TT
class, test the favorable values

    chi =
        0.25
        1
        1e3
        1e6
        1e12.

These are not claimed physical efficiencies.

The script also solves directly for

    chi_required

needed to satisfy each practical power budget.

FULL-CYCLE ACCOUNTING
---------------------
The primary dynamic ledger requires:

    complete compact waveform;
    radiated energy counted as lost;
    paired radiation to cancel source recoil;
    no negative energy credited;
    no unexplained cancellation;
    no reset-energy omission in the reusable near-zone control.

Near-zone pulsing is compared by peak stored energy.

Radiative memory is compared by one-second total radiated energy / power.

CHEAP DECISIVE TEST
-------------------
The run is RED if all of the following occur:

1. compact weak-TT numerical reconstruction confirms zero first-order
   velocity kick and inward second-order radial memory;

2. an ideal C=1 reusable near-zone source still misses the 1 TJ target by
   many orders of magnitude;

3. even an absurdly favorable outward-memory oracle with chi=1e12 remains
   far above the macroscopic dynamic power budget;

4. the chi actually required by the budget is enormously outside the
   perturbative weak-memory scale.

PROMOTION
---------
GREEN:

    a physically derived outward complete-cycle dynamic branch meets the
    macroscopic target without source-recoil contamination.

YELLOW:

    a derived outward branch produces at least twelve orders of magnitude
    improvement over 006D while retaining complete energy accounting.

RED:

    the tested reusable near-zone and weak radiative/memory GR classes do
    not escape the 1/G practicality scaling.

80-PERCENT RULE
---------------
Do not raise the project heuristic to satisfy a desired milestone.

030A alone cannot authorize the route-level 80% marker unless it discovers a
new physically derived scaling mechanism.

WHAT THIS RUN DOES NOT PROVE
----------------------------
It is NOT a universal no-go theorem for every nonlinear time-dependent GR
spacetime.

It does not exclude:

    strong-field black-hole-scale scattering;
    every possible velocity-memory observable;
    arbitrary nonlinear near-zone dynamics;
    modified gravity;
    nonlocal gravity.

It does establish a sharp falsification gate for the two most favorable
remaining pure-GR dynamic mechanisms:

    reusable linear near-zone pulsing;

    finite-energy weak radiative / memory impulse.

NEXT AFTER RED
--------------
Proceed to:

    030B_POSITIVE_SPECTRAL_NONLOCAL_PROPAGATOR_SIGN_AND_KERNEL_GATE

rather than returning to another local source/gain mechanism.

CLAIM CLASSIFICATION
--------------------
TRUE_ANTIGRAVITY_DYNAMIC_PURE_GR_SCALING_FALSIFICATION_GATE

NOVEL PHYSICS CLAIM
-------------------
NO.
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp


C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
G0 = 9.80665

C_006D = 23.591586299249

RAW_TEACHER_C = 0.02450446248122538

PAYLOAD_RADIUS_OVER_H = 0.10
BETA_PAYLOAD = PAYLOAD_RADIUS_OVER_H ** 2

MISSION_SECONDS = 1.0

WAVE_AMPLITUDE = 1.0e-3

SMOKE = (
    os.environ.get(
        "AG030A_SMOKE",
        "0",
    )
    == "1"
)

WAVEFORM_COUNT = (
    4
    if SMOKE
    else 16
)

FOURIER_MODES = 5
WAVE_GRID = 2049

ORACLE_CHI_VALUES = (
    0.25,
    1.0,
    1.0e3,
    1.0e6,
    1.0e12,
)

DUTY_VALUES = (
    1.0,
    0.75,
    0.50,
    0.25,
    0.10,
    0.01,
)

BLIND_WILDCARDS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)

TARGETS = (
    (
        "MACRO_1G_1M_1TJ_1S",
        G0,
        1.0,
        1.0e12,
    ),
    (
        "SUBSCALE_0P1G_1CM_1PJ_1S",
        0.1 * G0,
        0.01,
        1.0e15,
    ),
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

LINEAGE = DATA / "029a_mass_gated_spin2_portal_summary.json"

OUT_JSON = DATA / "030a_dynamic_gr_impulse_memory_summary.json"

OUT_WAVE = DATA / "030a_compact_tt_waveform_audit.csv"

OUT_TARGET = DATA / "030a_dynamic_scaling_targets.csv"

OUT_ORACLE = DATA / "030a_memory_oracle_scan.csv"

OUT_WILD = DATA / "030a_dynamic_wildcard_audit.csv"


if not LINEAGE.is_file():
    raise FileNotFoundError(
        f"Required 029A lineage missing: {LINEAGE}"
    )


with LINEAGE.open(
    "r",
    encoding="utf-8",
) as f:
    J029A = json.load(
        f
    )


if not str(
    J029A.get(
        "decision",
        "",
    )
).startswith(
    "RED_"
):
    raise RuntimeError(
        "030A expects completed RED 029A lineage"
    )


OMEGAS = (
    2.0
    * math.pi
    * np.arange(
        1,
        FOURIER_MODES + 1,
        dtype=float,
    )
)


def waveform_arrays(
    theta: np.ndarray,
    a_plus: np.ndarray,
    b_plus: np.ndarray,
    a_cross: np.ndarray,
    b_cross: np.ndarray,
) -> tuple[np.ndarray, ...]:
    """Return compact waveform and first/second derivatives."""

    theta = np.asarray(
        theta,
        dtype=float,
    )

    window = (
        np.sin(
            math.pi
            * theta
        )
        ** 2
    )

    window_p = (
        math.pi
        * np.sin(
            2.0
            * math.pi
            * theta
        )
    )

    window_pp = (
        2.0
        * math.pi
        ** 2
        * np.cos(
            2.0
            * math.pi
            * theta
        )
    )

    phase = (
        theta[
            ...,
            None,
        ]
        * OMEGAS
    )

    cosine = np.cos(
        phase
    )

    sine = np.sin(
        phase
    )

    def series(
        a: np.ndarray,
        b: np.ndarray,
    ) -> tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ]:

        g = (
            cosine
            @ a
            + sine
            @ b
        )

        gp = (
            (
                -sine
                * OMEGAS
            )
            @ a
            + (
                cosine
                * OMEGAS
            )
            @ b
        )

        gpp = (
            (
                -cosine
                * OMEGAS
                ** 2
            )
            @ a
            + (
                -sine
                * OMEGAS
                ** 2
            )
            @ b
        )

        h = (
            window
            * g
        )

        hp = (
            window_p
            * g
            + window
            * gp
        )

        hpp = (
            window_pp
            * g
            + 2.0
            * window_p
            * gp
            + window
            * gpp
        )

        return (
            h,
            hp,
            hpp,
        )

    hp, hp_p, hp_pp = series(
        a_plus,
        b_plus,
    )

    hx, hx_p, hx_pp = series(
        a_cross,
        b_cross,
    )

    return (
        hp,
        hp_p,
        hp_pp,
        hx,
        hx_p,
        hx_pp,
    )


def normalize_waveform(
    rng: np.random.Generator,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Draw and derivative-energy normalize one polarized waveform."""

    coeffs = [
        rng.normal(
            size=FOURIER_MODES
        )
        for _ in range(
            4
        )
    ]

    theta = np.linspace(
        0.0,
        1.0,
        WAVE_GRID,
    )

    (
        _,
        hp_p,
        _,
        _,
        hx_p,
        _,
    ) = waveform_arrays(
        theta,
        *coeffs,
    )

    derivative_norm = float(
        np.trapezoid(
            hp_p
            ** 2
            + hx_p
            ** 2,
            theta,
        )
    )

    if derivative_norm <= 0.0:
        raise RuntimeError(
            "Degenerate randomized waveform"
        )

    scale = (
        1.0
        / math.sqrt(
            derivative_norm
        )
    )

    return tuple(
        np.asarray(
            coefficient
            * scale,
            dtype=float,
        )
        for coefficient in coeffs
    )


def scalar_second_derivatives(
    theta: float,
    coeffs: tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ],
) -> tuple[
    float,
    float,
]:
    """Fast scalar h_plus'' and h_cross'' evaluation."""

    (
        a_plus,
        b_plus,
        a_cross,
        b_cross,
    ) = coeffs

    window = (
        math.sin(
            math.pi
            * theta
        )
        ** 2
    )

    window_p = (
        math.pi
        * math.sin(
            2.0
            * math.pi
            * theta
        )
    )

    window_pp = (
        2.0
        * math.pi
        ** 2
        * math.cos(
            2.0
            * math.pi
            * theta
        )
    )

    phase = (
        OMEGAS
        * theta
    )

    cosine = np.cos(
        phase
    )

    sine = np.sin(
        phase
    )

    def one(
        a: np.ndarray,
        b: np.ndarray,
    ) -> float:

        g = float(
            cosine
            @ a
            + sine
            @ b
        )

        gp = float(
            (
                -sine
                * OMEGAS
            )
            @ a
            + (
                cosine
                * OMEGAS
            )
            @ b
        )

        gpp = float(
            (
                -cosine
                * OMEGAS
                ** 2
            )
            @ a
            + (
                -sine
                * OMEGAS
                ** 2
            )
            @ b
        )

        return (
            window_pp
            * g
            + 2.0
            * window_p
            * gp
            + window
            * gpp
        )

    return (
        one(
            a_plus,
            b_plus,
        ),
        one(
            a_cross,
            b_cross,
        ),
    )


def integrate_geodesic_deviation(
    coeffs: tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
    ],
    amplitude: float,
    angle: float,
) -> dict[
    str,
    float,
]:
    """Integrate the complete compact-TT geodesic-deviation ODE."""

    initial = np.array(
        [
            math.cos(
                angle
            ),
            math.sin(
                angle
            ),
        ],
        dtype=float,
    )

    tangent = np.array(
        [
            -initial[
                1
            ],
            initial[
                0
            ],
        ],
        dtype=float,
    )

    def rhs(
        theta: float,
        y: np.ndarray,
    ) -> np.ndarray:

        (
            hp_pp,
            hx_pp,
        ) = scalar_second_derivatives(
            theta,
            coeffs,
        )

        x = y[
            :2
        ]

        acceleration = (
            0.5
            * amplitude
            * np.array(
                [
                    (
                        hp_pp
                        * x[
                            0
                        ]
                        + hx_pp
                        * x[
                            1
                        ]
                    ),
                    (
                        hx_pp
                        * x[
                            0
                        ]
                        - hp_pp
                        * x[
                            1
                        ]
                    ),
                ],
                dtype=float,
            )
        )

        return np.concatenate(
            [
                y[
                    2:
                ],
                acceleration,
            ]
        )

    y0 = np.concatenate(
        [
            initial,
            np.zeros(
                2
            ),
        ]
    )

    solution = solve_ivp(
        rhs,
        (
            0.0,
            1.0,
        ),
        y0,
        rtol=1.0e-9,
        atol=1.0e-12,
        max_step=0.004,
    )

    if not solution.success:
        raise RuntimeError(
            solution.message
        )

    final_velocity = solution.y[
        2:,
        -1,
    ]

    return {
        "radial_velocity":
            float(
                initial
                @ final_velocity
            ),

        "tangential_velocity":
            float(
                tangent
                @ final_velocity
            ),

        "final_separation":
            float(
                np.linalg.norm(
                    solution.y[
                        :2,
                        -1,
                    ]
                )
            ),
    }


def waveform_campaign() -> list[
    dict[
        str,
        float | int | bool,
    ]
]:
    """Numerically verify the weak compact-TT second-order identity."""

    rng = np.random.default_rng(
        3001
    )

    rows: list[
        dict[
            str,
            float | int | bool,
        ]
    ] = []

    angles = (
        0.0,
        0.37,
        1.11,
        2.07,
    )

    for waveform_index in range(
        WAVEFORM_COUNT
    ):

        coeffs = normalize_waveform(
            rng
        )

        theta = np.linspace(
            0.0,
            1.0,
            WAVE_GRID,
        )

        (
            _,
            hp_p,
            _,
            _,
            hx_p,
            _,
        ) = waveform_arrays(
            theta,
            *coeffs,
        )

        unit_integral = float(
            np.trapezoid(
                hp_p
                ** 2
                + hx_p
                ** 2,
                theta,
            )
        )

        endpoint_derivative = max(
            abs(
                float(
                    hp_p[
                        0
                    ]
                )
            ),
            abs(
                float(
                    hp_p[
                        -1
                    ]
                )
            ),
            abs(
                float(
                    hx_p[
                        0
                    ]
                )
            ),
            abs(
                float(
                    hx_p[
                        -1
                    ]
                )
            ),
        )

        for angle in angles:

            full = integrate_geodesic_deviation(
                coeffs,
                WAVE_AMPLITUDE,
                angle,
            )

            half = integrate_geodesic_deviation(
                coeffs,
                0.5
                * WAVE_AMPLITUDE,
                angle,
            )

            integral_actual = (
                WAVE_AMPLITUDE
                ** 2
                * unit_integral
            )

            chi_signed = (
                full[
                    "radial_velocity"
                ]
                / integral_actual
            )

            amplitude_scaling = (
                full[
                    "radial_velocity"
                ]
                / half[
                    "radial_velocity"
                ]
                if abs(
                    half[
                        "radial_velocity"
                    ]
                )
                > 1.0e-30
                else math.nan
            )

            rows.append(
                {
                    "waveform":
                        waveform_index,

                    "angle":
                        angle,

                    "unit_derivative_integral":
                        unit_integral,

                    "endpoint_derivative_max":
                        endpoint_derivative,

                    "amplitude":
                        WAVE_AMPLITUDE,

                    "radial_velocity":
                        full[
                            "radial_velocity"
                        ],

                    "tangential_velocity":
                        full[
                            "tangential_velocity"
                        ],

                    "signed_chi":
                        chi_signed,

                    "predicted_signed_chi":
                        -0.25,

                    "chi_error":
                        chi_signed
                        + 0.25,

                    "amplitude_squared_scaling":
                        amplitude_scaling,

                    "outward_radial":
                        bool(
                            full[
                                "radial_velocity"
                            ]
                            > 0.0
                        ),
                }
            )

    return rows


def coefficient_required(
    acceleration: float,
    h: float,
    budget: float,
) -> float:
    """Static-equivalent C allowed by the energy budget."""

    return (
        budget
        * G_NEWTON
        / (
            acceleration
            * C_LIGHT
            ** 2
            * h
            ** 2
        )
    )


def static_energy(
    coefficient: float,
    acceleration: float,
    h: float,
) -> float:
    """Return E=C a c^2 h^2/G."""

    return (
        coefficient
        * acceleration
        * C_LIGHT
        ** 2
        * h
        ** 2
        / G_NEWTON
    )


def paired_memory_power(
    beta: float,
    acceleration: float,
    h: float,
    chi: float,
) -> float:
    """Recoil-balanced paired-beam memory power floor."""

    return (
        beta
        * acceleration
        * C_LIGHT
        ** 3
        * h
        / (
            16.0
            * G_NEWTON
            * chi
        )
    )


def metric_weakness(
    energy: float,
    h: float,
) -> float:
    """Optimistic device-scale metric perturbation from the budget."""

    return (
        2.0
        * G_NEWTON
        * energy
        / (
            C_LIGHT
            ** 4
            * h
        )
    )


print(
    "=== 030A DYNAMIC TRUE-GRAVITY IMPULSE / MEMORY GATE ===",
    flush=True,
)

print(
    (
        "029A_LINEAGE="
        + str(
            J029A.get(
                "decision"
            )
        )
    ),
    flush=True,
)

print(
    (
        "PAYLOAD_RADIUS_OVER_H="
        f"{PAYLOAD_RADIUS_OVER_H:.12e}"
    ),
    flush=True,
)

print(
    "PRIMARY_RECOIL_BALANCED_PAIRED_BEAMS=YES",
    flush=True,
)

print(
    "MISSION_SECONDS=1",
    flush=True,
)


wave_rows = waveform_campaign()

chi_values = np.array(
    [
        float(
            row[
                "signed_chi"
            ]
        )
        for row in wave_rows
    ]
)

scale_values = np.array(
    [
        float(
            row[
                "amplitude_squared_scaling"
            ]
        )
        for row in wave_rows
    ]
)

outward_count = int(
    sum(
        bool(
            row[
                "outward_radial"
            ]
        )
        for row in wave_rows
    )
)

max_endpoint_derivative = max(
    float(
        row[
            "endpoint_derivative_max"
        ]
    )
    for row in wave_rows
)

max_chi_error = float(
    np.max(
        np.abs(
            chi_values
            + 0.25
        )
    )
)

max_scaling_error = float(
    np.max(
        np.abs(
            scale_values
            - 4.0
        )
    )
)

wave_green = bool(
    outward_count
    == 0
    and max_endpoint_derivative
    <= 1.0e-12
    and max_chi_error
    <= 5.0e-4
    and max_scaling_error
    <= 5.0e-3
)


print(
    "\n=== COMPACT WEAK-TT VALIDATION ===",
    flush=True,
)

print(
    f"WAVEFORM_CASES={len(wave_rows)}",
    flush=True,
)

print(
    f"OUTWARD_RADIAL_CASES={outward_count}",
    flush=True,
)

print(
    (
        "SIGNED_CHI_MEAN="
        f"{float(np.mean(chi_values)):.15e}"
    ),
    flush=True,
)

print(
    (
        "SIGNED_CHI_MIN="
        f"{float(np.min(chi_values)):.15e}"
    ),
    flush=True,
)

print(
    (
        "SIGNED_CHI_MAX="
        f"{float(np.max(chi_values)):.15e}"
    ),
    flush=True,
)

print(
    (
        "MAX_CHI_ERROR_FROM_MINUS_QUARTER="
        f"{max_chi_error:.15e}"
    ),
    flush=True,
)

print(
    (
        "MAX_AMPLITUDE_SQUARED_SCALING_ERROR="
        f"{max_scaling_error:.15e}"
    ),
    flush=True,
)

print(
    "FIRST_ORDER_COMPACT_TT_VELOCITY_MEMORY=ZERO",
    flush=True,
)

print(
    "SECOND_ORDER_COMPACT_TT_RADIAL_SIGN=INWARD",
    flush=True,
)

print(
    "DISPLACEMENT_MEMORY_FIRST_ORDER_RESIDUAL_VELOCITY=ZERO",
    flush=True,
)

print(
    (
        "COMPACT_TT_VALIDATION="
        + (
            "PASS"
            if wave_green
            else "FAIL"
        )
    ),
    flush=True,
)


scaling_rows = []
oracle_rows = []
wild_rows = []


for (
    target_name,
    acceleration,
    h,
    budget,
) in TARGETS:

    required_c = coefficient_required(
        acceleration,
        h,
        budget,
    )

    c1_energy = static_energy(
        1.0,
        acceleration,
        h,
    )

    c006d_energy = static_energy(
        C_006D,
        acceleration,
        h,
    )

    raw_teacher_energy = static_energy(
        RAW_TEACHER_C,
        acceleration,
        h,
    )

    power_budget = (
        budget
        / MISSION_SECONDS
    )

    chi_required = (
        BETA_PAYLOAD
        * acceleration
        * C_LIGHT
        ** 3
        * h
        / (
            16.0
            * G_NEWTON
            * power_budget
        )
    )

    weak_memory_power = paired_memory_power(
        BETA_PAYLOAD,
        acceleration,
        h,
        0.25,
    )

    target_row = {
        "target":
            target_name,

        "acceleration_m_s2":
            acceleration,

        "h_m":
            h,

        "energy_budget_J":
            budget,

        "mission_seconds":
            MISSION_SECONDS,

        "dynamic_power_budget_W":
            power_budget,

        "C_required":
            required_c,

        "C1_peak_energy_J":
            c1_energy,

        "C1_energy_gap":
            c1_energy
            / budget,

        "C006D_peak_energy_J":
            c006d_energy,

        "C006D_energy_gap":
            c006d_energy
            / budget,

        "RAW_TEACHER_ORACLE_peak_energy_J":
            raw_teacher_energy,

        "RAW_TEACHER_ORACLE_energy_gap":
            raw_teacher_energy
            / budget,

        "paired_memory_beta":
            BETA_PAYLOAD,

        "paired_memory_weak_chi":
            0.25,

        "paired_memory_power_W_chi0p25":
            weak_memory_power,

        "paired_memory_power_gap_chi0p25":
            weak_memory_power
            / power_budget,

        "chi_required_to_meet_power_budget":
            chi_required,

        "budget_metric_weakness":
            metric_weakness(
                budget,
                h,
            ),
    }

    scaling_rows.append(
        target_row
    )

    print(
        (
            "\n=== TARGET "
            + target_name
            + " ==="
        ),
        flush=True,
    )

    print(
        f"C_REQUIRED={required_c:.15e}",
        flush=True,
    )

    print(
        (
            "C1_PEAK_ENERGY_GAP="
            f"{c1_energy / budget:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "C006D_PEAK_ENERGY_GAP="
            f"{c006d_energy / budget:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "RAW_TEACHER_ORACLE_ENERGY_GAP="
            f"{raw_teacher_energy / budget:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "PAIRED_MEMORY_POWER_CHI0P25_W="
            f"{weak_memory_power:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "PAIRED_MEMORY_POWER_GAP_CHI0P25="
            f"{weak_memory_power / power_budget:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "CHI_REQUIRED_FOR_DYNAMIC_BUDGET="
            f"{chi_required:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "BUDGET_METRIC_WEAKNESS="
            f"{metric_weakness(budget, h):.15e}"
        ),
        flush=True,
    )

    for duty in DUTY_VALUES:

        scaling_rows.append(
            {
                "target":
                    (
                        target_name
                        + f"__DUTY_{duty:g}"
                    ),

                "acceleration_m_s2":
                    acceleration,

                "h_m":
                    h,

                "energy_budget_J":
                    budget,

                "duty":
                    duty,

                "near_zone_C1_peak_J":
                    (
                        c1_energy
                        / duty
                    ),

                "near_zone_C1_gap":
                    (
                        c1_energy
                        / (
                            duty
                            * budget
                        )
                    ),

                "near_zone_006D_peak_J":
                    (
                        c006d_energy
                        / duty
                    ),

                "near_zone_006D_gap":
                    (
                        c006d_energy
                        / (
                            duty
                            * budget
                        )
                    ),

                "selection_role":
                    "PHYSICAL_DUTY_CONTROL",
            }
        )

    for chi in ORACLE_CHI_VALUES:

        power = paired_memory_power(
            BETA_PAYLOAD,
            acceleration,
            h,
            chi,
        )

        oracle_rows.append(
            {
                "target":
                    target_name,

                "chi":
                    chi,

                "beta":
                    BETA_PAYLOAD,

                "power_W":
                    power,

                "power_gap":
                    (
                        power
                        / power_budget
                    ),

                "meets_budget":
                    bool(
                        power
                        <= power_budget
                    ),

                "selection_role":
                    "OUTWARD_MEMORY_ORACLE",
            }
        )

    for wildcard in BLIND_WILDCARDS:

        power = paired_memory_power(
            BETA_PAYLOAD,
            acceleration,
            h,
            wildcard,
        )

        wild_rows.append(
            {
                "target":
                    target_name,

                "wildcard_chi":
                    wildcard,

                "power_gap":
                    (
                        power
                        / power_budget
                    ),

                "selection_role":
                    "BLIND_NON_EVIDENTIARY_EXCLUDED",
            }
        )


macro = next(
    row
    for row in scaling_rows
    if row[
        "target"
    ]
    == "MACRO_1G_1M_1TJ_1S"
)

macro_oracle_1e12 = next(
    row
    for row in oracle_rows
    if (
        row[
            "target"
        ]
        == "MACRO_1G_1M_1TJ_1S"
        and row[
            "chi"
        ]
        == 1.0e12
    )
)


if not wave_green:

    decision = (
        "INVALID_NUMERICAL_VALIDATION"
    )

    next_step = (
        "REPAIR_030A_BEFORE_INTERPRETATION"
    )

elif (
    macro[
        "C1_energy_gap"
    ]
    > 1.0e12

    and macro_oracle_1e12[
        "power_gap"
    ]
    > 1.0e6

    and macro[
        "chi_required_to_meet_power_budget"
    ]
    > 1.0e18
):

    decision = (
        "RED_TESTED_DYNAMIC_PURE_GR_CLASSES_"
        "DO_NOT_ESCAPE_1_OVER_G_SCALING"
    )

    next_step = (
        "030B_POSITIVE_SPECTRAL_NONLOCAL_"
        "PROPAGATOR_SIGN_AND_KERNEL_GATE"
    )

else:

    decision = (
        "YELLOW_DYNAMIC_GR_SCALING_WINDOW_"
        "REQUIRES_FURTHER_FULL_SOURCE_TEST"
    )

    next_step = (
        "BUILD_EXPLICIT_CONSERVED_DYNAMIC_SOURCE_"
        "BEFORE_PROMOTION"
    )


summary = {
    "branch":
        "TRUE_ANTIGRAVITY",

    "simulation":
        "030A",

    "question":
        (
            "Can full-cycle time dependence, either reusable near-zone "
            "pulsing or finite-energy gravitational-wave memory, evade "
            "the pure-GR 1/G practicality scaling after 029A?"
        ),

    "lineage_029A":
        J029A.get(
            "decision"
        ),

    "compact_TT": {
        "waveform_cases":
            len(
                wave_rows
            ),

        "outward_radial_cases":
            outward_count,

        "signed_chi_mean":
            float(
                np.mean(
                    chi_values
                )
            ),

        "signed_chi_min":
            float(
                np.min(
                    chi_values
                )
            ),

        "signed_chi_max":
            float(
                np.max(
                    chi_values
                )
            ),

        "max_chi_error_from_minus_quarter":
            max_chi_error,

        "max_amplitude_squared_scaling_error":
            max_scaling_error,

        "first_order_velocity_memory":
            0.0,

        "second_order_formula":
            (
                "Delta v_parallel/L = "
                "-1/4 integral(hplus_dot^2+hcross_dot^2)dt"
            ),

        "validation_pass":
            wave_green,

        "scope":
            "compact weak TT strain pulses",
    },

    "near_zone_control": {
        "identity":
            (
                "E_peak = C_peak a_average c^2 h^2/(G D), D<=1"
            ),

        "interpretation":
            (
                "linear duty cycling cannot reduce peak stored field energy"
            ),

        "ideal_C1_is_favorable_oracle":
            True,

        "raw_teacher_C_is_non_evidentiary":
            True,
    },

    "radiative_memory_control": {
        "paired_recoil_balanced_beams":
            True,

        "payload_radius_over_h":
            PAYLOAD_RADIUS_OVER_H,

        "beta":
            BETA_PAYLOAD,

        "power_floor":
            (
                "P_pair >= beta a c^3 h/(16 G chi)"
            ),

        "weak_compact_TT_abs_chi":
            0.25,

        "outward_oracle_tested":
            True,

        "radiated_energy_recoverable":
            False,
    },

    "targets":
        [
            row
            for row in scaling_rows
            if "duty"
            not in row
        ],

    "decision":
        decision,

    "next":
        next_step,

    "route_level_80_heuristic_authorized":
        False,

    "overall_practical_antigravity_proven":
        False,

    "mandatory_parallel_credibility_branch":
        "026C_N89_FORCE_CONVERGENCE",

    "claims": {
        "universal_dynamic_GR_no_go":
            False,

        "compact_weak_TT_first_order_velocity_kick":
            False,

        "compact_weak_TT_second_order_outward_memory":
            False,

        "general_velocity_memory_exists_in_literature":
            True,

        "general_velocity_memory_practicality_established":
            False,

        "explicit_microscopic_dynamic_source":
            False,

        "full_nonlinear_GR_dynamic_solution":
            False,

        "practical_antigravity_device":
            False,
    },
}


DATA.mkdir(
    parents=True,
    exist_ok=True,
)


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


with OUT_WAVE.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=list(
            wave_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        wave_rows
    )


all_target_fields = sorted(
    {
        key
        for row in scaling_rows
        for key in row.keys()
    }
)


with OUT_TARGET.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=all_target_fields,
    )

    writer.writeheader()

    writer.writerows(
        scaling_rows
    )


with OUT_ORACLE.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=list(
            oracle_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        oracle_rows
    )


with OUT_WILD.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=list(
            wild_rows[
                0
            ].keys()
        ),
    )

    writer.writeheader()

    writer.writerows(
        wild_rows
    )


print(
    "\n=== 030A FINAL RESULT ===",
    flush=True,
)

print(
    (
        "MACRO_C1_ENERGY_GAP="
        f"{macro['C1_energy_gap']:.15e}"
    ),
    flush=True,
)

print(
    (
        "MACRO_CHI_REQUIRED="
        f"{macro['chi_required_to_meet_power_budget']:.15e}"
    ),
    flush=True,
)

print(
    (
        "MACRO_ORACLE_CHI1E12_POWER_GAP="
        f"{macro_oracle_1e12['power_gap']:.15e}"
    ),
    flush=True,
)

print(
    f"030A_DECISION={decision}",
    flush=True,
)

print(
    f"NEXT={next_step}",
    flush=True,
)

print(
    "ROUTE_LEVEL_80_HEURISTIC_AUTHORIZED=NO",
    flush=True,
)

print(
    "HEURISTIC_IS_PROBABILITY=NO",
    flush=True,
)

print(
    "UNIVERSAL_DYNAMIC_GR_NO_GO=NO",
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
    f"SUMMARY_JSON={OUT_JSON}",
    flush=True,
)

print(
    f"WAVEFORM_CSV={OUT_WAVE}",
    flush=True,
)

print(
    f"TARGET_CSV={OUT_TARGET}",
    flush=True,
)

print(
    f"ORACLE_CSV={OUT_ORACLE}",
    flush=True,
)

print(
    f"WILDCARD_CSV={OUT_WILD}",
    flush=True,
)

print(
    "030A_RUN_COMPLETE=YES",
    flush=True,
)
