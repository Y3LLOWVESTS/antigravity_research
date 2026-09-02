#!/usr/bin/env python3
"""024B3 — free outward annular domain-wall pulse gate.

PURPOSE
-------
Test the final cheap pure-GR pulse architecture motivated by 024B–024B2
before spending compute on another microscopic PDE.

024B established that a negative-active domain wall can have an excellent
instantaneous source coefficient.

024B1 showed that ordinary outer-edge collapse converts wall energy into
positive kinetic string stress moving inward and gives a negative integrated
payload response.

024B2 showed that holding the outer edge stationary with a local physical
DEC-compatible rim destroys the compact outward solution and independently
reconstructs the historical C approximately 79.753 supported-disk result.

The remaining simple possibility is therefore:

    DO NOT HOLD THE OUTER EDGE.

Instead give the outer boundary outward momentum and let it create an annular
wall while a supercritical inner boundary follows it outward and consumes the
wall.

Both compensating string stresses then move away from the payload.

This is the most favorable simple Nambu-Goto realization of the project's
spatiotemporal kernel-leverage idea that does not use a stationary local
support.

SCIENTIFIC QUESTION
-------------------
Can a freely evolving annular wall pulse whose inner and outer boundaries both
move outward produce positive finite-standoff gravitational impulse before the
inner boundary catches the outer one?

MODEL
-----
Use c=h=sigma=1.

Let

    b(t)

be the outer wall radius and

    a(t)

the inner-hole radius.

The wall exists for

    a < r < b.

The reduced Nambu-Goto actions separate:

Outer boundary:

    L_o
        =
    -2 pi mu_o b sqrt(1-bdot^2)
    - pi b^2

with conserved quantity

    E_o
        =
    2 pi mu_o b gamma_o
    + pi b^2.

Inner boundary:

    L_i
        =
    -2 pi mu_i a sqrt(1-adot^2)
    + pi a^2

with conserved quantity

    E_i
        =
    2 pi mu_i a gamma_i
    - pi a^2.

The complete physical annulus-plus-boundaries energy is

    E
        =
    E_o + E_i

        =
    2 pi mu_o b gamma_o
    +
    2 pi mu_i a gamma_i
    +
    pi (b^2-a^2).

INITIAL STATE
-------------
At t=0 take

    a=b=r0.

The wall area initially vanishes.

Two coincident boundary defects have outward velocities

    v_o > v_i >= 0.

The faster outer boundary separates from the inner boundary and creates a wall
annulus.

The inner boundary is restricted to the supercritical regime

    mu_i/(sigma r0) < 1

so it can propagate outward.

The pulse is considered successfully geometrically closed only if

    a=b

again before the outer boundary reaches its outward turning point.

Thus the tested wall episode begins with zero wall area and ends with zero wall
area while both boundaries have moved outward.

This is not yet a complete microscopic creation/annihilation cycle for the
boundary fields.

ACTIVE GRAVITATIONAL SOURCE
---------------------------
A static domain wall has active surface source

    S_wall = -sigma.

For an annulus in the plane z=0, payload height h=1, its outward axial kernel
moment is

    A_wall
        =
    2 pi
    [
        1/sqrt(1+a^2)
        -
        1/sqrt(1+b^2)
    ].

A transversely moving Nambu-Goto string has active line source

    Lambda_string
        =
    2 mu gamma v^2.

After integration around the circumference,

    Q_string
        =
    4 pi mu r gamma v^2.

Its contribution to the desired outward acceleration is inward:

    A_string
        =
    -
    Q_string
    /
    (1+r^2)^(3/2).

Therefore

    A_total
        =
    A_wall
    -
    Q_o/(1+b^2)^(3/2)
    -
    Q_i/(1+a^2)^(3/2).

Positive A_total means outward.

The stage impulse observable is

    J
        =
    integral A_total dt.

Define

    eta_J
        =
    J/E.

Positive eta_J is required for promotion.

PEAK COEFFICIENT
----------------
If the stage ever becomes outward, define

    C_peak
        =
    E/max(A_total).

If A_total never becomes positive,

    C_peak

is undefined/infinite.

PARAMETERS
----------
Use

    x0
        =
    r0/h,

    q_o
        =
    mu_o/(sigma r0),

    q_i
        =
    mu_i/(sigma r0),

    v_o,

and

    f
        =
    v_i/v_o.

Primary Sobol ranges:

    0.05 <= x0 <= 5
    0.003 <= q_o <= 0.9
    0.003 <= q_i <= 0.9
    0.2 <= v_o <= 0.999
    0 <= f <= 0.95.

The scan deliberately spans several orders of magnitude in string/wall
tension ratio and both slow and ultrarelativistic outer-boundary motion.

BLIND WILDCARDS
---------------
The project wildcard values

    0.625
    1.6
    1.875
    3.125
    5

are tested explicitly as x0 values.

They are not physics priors, evidence, optimization targets, or privileged
parameters.

NUMERICAL METHOD
----------------
The primary solver uses conserved boundary energies to construct each
monotonic outward trajectory independently.

The outer trajectory is followed to its turning point.

The inner trajectory is followed over the same radial interval.

Coordinate time is reconstructed by

    dt = dr/v(r).

A transformed radial variable removes the integrable turning-point behavior.

The two trajectories are interpolated onto a common time grid.

A trajectory is promoted to the closed sample only if the inner boundary
catches the outer boundary before the outer boundary turns inward.

For the cases closest to changing sign, a second implementation integrates
the boundary ODEs directly with scipy.integrate.solve_ivp at tight tolerances.

This independent implementation is used only as a sign/refinement audit.

CONSERVATION
------------
The complete reduced energy

    E
        =
    2 pi mu_o b gamma_o
    +
    2 pi mu_i a gamma_i
    +
    pi(b^2-a^2)

must remain constant.

The maximum numerical relative residual is reported.

OPTIMISTIC NATURE OF THE GATE
-----------------------------
This run deliberately stops when the two boundaries meet.

It does NOT add:

- boundary annihilation radiation;
- scalar radiation;
- gravitational radiation;
- formation energy for the initial coincident defects;
- reset;
- repetition hardware;
- nonlinear gravity.

Ordinary outgoing radiation has positive active stress.

Therefore a negative impulse before annihilation cannot be rescued merely by
adding an omitted conventional radiation sector.

A positive result would still require a microscopic field evolution.

PROMOTION CONDITION
-------------------
A candidate survives only if a geometrically closed outward-only trajectory
has

    eta_J > 0

and

    max(A_total) > 0.

A major source-efficiency candidate additionally requires

    C_peak <= C_006D/10.

FALSIFIER
---------
The simple free outward-annular pulse class is falsified in the tested domain
if:

    CLOSED_POSITIVE_ETA_CASES = 0

and

    CLOSED_POSITIVE_INSTANTANEOUS_CASES = 0

across the primary low-discrepancy scans, with independent ODE refinement of
the closest-to-zero cases preserving the sign.

STOP RULE
---------
If this gate is RED:

Do not immediately invent another unsupported pure-GR pulse.

Pause the current Nambu-Goto/domain-wall pulse family absent a genuinely new
microscopic mechanism that changes the stress transport.

Rerank:

    006D microscopic realization,
    023C/023D fallback,
    Analogue Antigravity.

This is not a universal theorem against every possible transient GR source.

LITERATURE CONTEXT
------------------
The leading low-curvature dynamics of scalar-field domain walls is
Nambu-Goto-like, with calculable finite-width/curvature corrections.

String-bounded wall holes and wall decay are established topological-defect
dynamics.

Real microscopic annihilation introduces additional radiation and field
degrees of freedom; therefore this reduced test is a deliberately optimistic
prefilter rather than a final field calculation.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_FREE_NAMBU_GOTO_ANNULAR_PULSE_IMPULSE_PREFILTER

DOES NOT ESTABLISH
------------------
- a universal transient-GR no-go;
- a microscopic creation/annihilation solution;
- nonlinear Einstein-matter dynamics;
- practical energy scaling;
- experimental antigravity;
- a practical device.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np

from scipy.integrate import (
    cumulative_trapezoid,
    solve_ivp,
)

from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]

INPUT = (
    ROOT
    / "results/data/"
    "024b2_stationary_rim_support_no_go_summary.json"
)

OUT_SUMMARY = (
    ROOT
    / "results/data/"
    "024b3_free_outward_annular_wall_pulse_summary.json"
)

OUT_SCAN = (
    ROOT
    / "results/data/"
    "024b3_free_outward_annular_wall_pulse_scan.csv"
)

C006D = 23.591586299249

WILDCARD_X = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


def map_parameters(
    u: np.ndarray,
) -> tuple[
    float,
    float,
    float,
    float,
    float,
]:
    """Map one Sobol point into the physical scan box."""

    log_x_min = math.log10(
        0.05
    )

    log_x_max = math.log10(
        5.0
    )

    log_q_min = math.log10(
        0.003
    )

    log_q_max = math.log10(
        0.9
    )

    x0 = 10.0 ** (
        log_x_min
        + (
            log_x_max
            - log_x_min
        )
        * float(
            u[0]
        )
    )

    q_outer = 10.0 ** (
        log_q_min
        + (
            log_q_max
            - log_q_min
        )
        * float(
            u[1]
        )
    )

    q_inner = 10.0 ** (
        log_q_min
        + (
            log_q_max
            - log_q_min
        )
        * float(
            u[2]
        )
    )

    v_outer = (
        0.2
        + (
            0.999
            - 0.2
        )
        * float(
            u[3]
        )
    )

    fraction = (
        0.95
        * float(
            u[4]
        )
    )

    return (
        x0,
        q_outer,
        q_inner,
        v_outer,
        fraction,
    )


def evaluate_fast(
    x0: float,
    q_outer: float,
    q_inner: float,
    v_outer: float,
    fraction: float,
    n: int,
) -> dict[str, Any] | None:
    """Conserved-energy trajectory reconstruction."""

    v_inner = (
        v_outer
        * fraction
    )

    if not (
        x0 > 0.0
        and 0.0 < q_outer < 1.0
        and 0.0 < q_inner < 1.0
        and 0.0 < v_outer < 1.0
        and 0.0 <= v_inner < v_outer
    ):
        return None

    mu_outer = (
        q_outer
        * x0
    )

    mu_inner = (
        q_inner
        * x0
    )

    gamma_outer_0 = (
        1.0
        / math.sqrt(
            1.0
            - v_outer
            * v_outer
        )
    )

    gamma_inner_0 = (
        1.0
        / math.sqrt(
            1.0
            - v_inner
            * v_inner
        )
    )

    energy_outer = (
        2.0
        * math.pi
        * mu_outer
        * x0
        * gamma_outer_0
        + math.pi
        * x0
        * x0
    )

    energy_inner = (
        2.0
        * math.pi
        * mu_inner
        * x0
        * gamma_inner_0
        - math.pi
        * x0
        * x0
    )

    energy_total = (
        energy_outer
        + energy_inner
    )

    # Outer turning radius from gamma_outer=1.
    r_turn = (
        -mu_outer
        + math.sqrt(
            mu_outer
            * mu_outer
            + energy_outer
            / math.pi
        )
    )

    if r_turn <= x0:
        return None

    delta = (
        r_turn
        - x0
    )

    # ------------------------------------------------------------
    # Outer trajectory.
    #
    # r(s)=r0+delta(2s-s^2) makes dr/ds vanish at the
    # turning point and regularizes dt/dr.
    # ------------------------------------------------------------

    s_outer = np.linspace(
        0.0,
        1.0
        - 1.0e-8,
        n,
    )

    r_outer = (
        x0
        + delta
        * (
            2.0
            * s_outer
            - s_outer
            * s_outer
        )
    )

    dr_outer_ds = (
        2.0
        * delta
        * (
            1.0
            - s_outer
        )
    )

    gamma_outer = (
        energy_outer
        - math.pi
        * r_outer
        * r_outer
    ) / (
        2.0
        * math.pi
        * mu_outer
        * r_outer
    )

    beta_outer_sq = np.maximum(
        0.0,
        1.0
        - 1.0
        / (
            gamma_outer
            * gamma_outer
        ),
    )

    beta_outer = np.sqrt(
        beta_outer_sq
    )

    dt_outer_ds = np.divide(
        dr_outer_ds,
        beta_outer,
        out=np.zeros_like(
            beta_outer
        ),
        where=(
            beta_outer
            > 1.0e-14
        ),
    )

    t_outer = np.concatenate(
        (
            [0.0],
            cumulative_trapezoid(
                dt_outer_ds,
                s_outer,
            ),
        )
    )

    # ------------------------------------------------------------
    # Inner trajectory.
    #
    # r(s)=r0+delta*s^2 regularizes the v_inner=0 endpoint.
    # ------------------------------------------------------------

    s_inner = np.linspace(
        0.0,
        1.0,
        n,
    )

    r_inner = (
        x0
        + delta
        * s_inner
        * s_inner
    )

    dr_inner_ds = (
        2.0
        * delta
        * s_inner
    )

    gamma_inner = (
        energy_inner
        + math.pi
        * r_inner
        * r_inner
    ) / (
        2.0
        * math.pi
        * mu_inner
        * r_inner
    )

    if (
        float(
            np.min(
                gamma_inner
            )
        )
        <
        1.0
        - 2.0e-8
    ):
        return None

    beta_inner_sq = np.maximum(
        0.0,
        1.0
        - 1.0
        / (
            gamma_inner
            * gamma_inner
        ),
    )

    beta_inner = np.sqrt(
        beta_inner_sq
    )

    dt_inner_ds = np.divide(
        dr_inner_ds,
        beta_inner,
        out=np.zeros_like(
            beta_inner
        ),
        where=(
            beta_inner
            > 1.0e-14
        ),
    )

    if (
        dt_inner_ds[0]
        == 0.0
    ):
        dt_inner_ds[0] = (
            dt_inner_ds[1]
        )

    t_inner = np.concatenate(
        (
            [0.0],
            cumulative_trapezoid(
                dt_inner_ds,
                s_inner,
            ),
        )
    )

    t_max = min(
        float(
            t_outer[-1]
        ),
        float(
            t_inner[-1]
        ),
    )

    if t_max <= 0.0:
        return None

    t = np.linspace(
        0.0,
        t_max,
        n,
    )

    ro = np.interp(
        t,
        t_outer,
        r_outer,
    )

    ri = np.interp(
        t,
        t_inner,
        r_inner,
    )

    width = (
        ro
        - ri
    )

    if (
        len(
            width
        )
        < 3
        or width[1]
        <= 0.0
    ):
        return None

    crossings = np.flatnonzero(
        width[1:]
        <= 0.0
    )

    if crossings.size == 0:
        return {
            "status":
                "OUTER_TURN_BEFORE_CLOSURE",

            "x0":
                x0,

            "q_outer":
                q_outer,

            "q_inner":
                q_inner,

            "v_outer":
                v_outer,

            "v_inner_over_v_outer":
                fraction,

            "v_inner":
                v_inner,

            "energy":
                energy_total,

            "eta":
                None,

            "max_outward":
                None,

            "C_peak":
                None,

            "duration":
                None,

            "meeting_radius":
                None,

            "energy_conservation_relative":
                None,
        }

    stop = int(
        crossings[0]
        + 1
    )

    if stop < 3:
        return None

    t = t[
        : stop + 1
    ]

    ro = ro[
        : stop + 1
    ]

    ri = ri[
        : stop + 1
    ]

    gamma_o = (
        energy_outer
        - math.pi
        * ro
        * ro
    ) / (
        2.0
        * math.pi
        * mu_outer
        * ro
    )

    gamma_i = (
        energy_inner
        + math.pi
        * ri
        * ri
    ) / (
        2.0
        * math.pi
        * mu_inner
        * ri
    )

    beta_o_sq = np.maximum(
        0.0,
        1.0
        - 1.0
        / (
            gamma_o
            * gamma_o
        ),
    )

    beta_i_sq = np.maximum(
        0.0,
        1.0
        - 1.0
        / (
            gamma_i
            * gamma_i
        ),
    )

    wall_outward = (
        2.0
        * math.pi
        * (
            1.0
            / np.sqrt(
                1.0
                + ri
                * ri
            )
            -
            1.0
            / np.sqrt(
                1.0
                + ro
                * ro
            )
        )
    )

    q_active_outer = (
        4.0
        * math.pi
        * mu_outer
        * ro
        * gamma_o
        * beta_o_sq
    )

    q_active_inner = (
        4.0
        * math.pi
        * mu_inner
        * ri
        * gamma_i
        * beta_i_sq
    )

    outer_inward = (
        q_active_outer
        / (
            1.0
            + ro
            * ro
        ) ** 1.5
    )

    inner_inward = (
        q_active_inner
        / (
            1.0
            + ri
            * ri
        ) ** 1.5
    )

    outward = (
        wall_outward
        - outer_inward
        - inner_inward
    )

    impulse = float(
        np.trapezoid(
            outward,
            t,
        )
    )

    eta = (
        impulse
        / energy_total
    )

    max_outward = float(
        np.max(
            outward
        )
    )

    c_peak = (
        energy_total
        / max_outward
        if max_outward > 0.0
        else None
    )

    energy_history = (
        2.0
        * math.pi
        * mu_outer
        * ro
        * gamma_o
        + math.pi
        * ro
        * ro
        + 2.0
        * math.pi
        * mu_inner
        * ri
        * gamma_i
        - math.pi
        * ri
        * ri
    )

    conservation = float(
        np.max(
            np.abs(
                energy_history
                - energy_total
            )
        )
        / energy_total
    )

    return {
        "status":
            "CLOSED_BEFORE_OUTER_TURN",

        "x0":
            x0,

        "q_outer":
            q_outer,

        "q_inner":
            q_inner,

        "v_outer":
            v_outer,

        "v_inner_over_v_outer":
            fraction,

        "v_inner":
            v_inner,

        "energy":
            energy_total,

        "eta":
            eta,

        "max_outward":
            max_outward,

        "min_outward":
            float(
                np.min(
                    outward
                )
            ),

        "C_peak":
            c_peak,

        "duration":
            float(
                t[-1]
            ),

        "meeting_radius":
            0.5
            * float(
                ro[-1]
                + ri[-1]
            ),

        "energy_conservation_relative":
            conservation,
    }


def refine_with_ivp(
    case: dict[str, Any],
) -> dict[str, Any]:
    """Independent direct-ODE sign audit."""

    x0 = float(
        case[
            "x0"
        ]
    )

    q_outer = float(
        case[
            "q_outer"
        ]
    )

    q_inner = float(
        case[
            "q_inner"
        ]
    )

    v_outer = float(
        case[
            "v_outer"
        ]
    )

    fraction = float(
        case[
            "v_inner_over_v_outer"
        ]
    )

    v_inner = (
        v_outer
        * fraction
    )

    fast_duration = float(
        case[
            "duration"
        ]
    )

    mu_outer = (
        q_outer
        * x0
    )

    mu_inner = (
        q_inner
        * x0
    )

    gamma_outer_0 = (
        1.0
        / math.sqrt(
            1.0
            - v_outer
            * v_outer
        )
    )

    gamma_inner_0 = (
        1.0
        / math.sqrt(
            1.0
            - v_inner
            * v_inner
        )
    )

    energy_outer = (
        2.0
        * math.pi
        * mu_outer
        * x0
        * gamma_outer_0
        + math.pi
        * x0
        * x0
    )

    energy_inner = (
        2.0
        * math.pi
        * mu_inner
        * x0
        * gamma_inner_0
        - math.pi
        * x0
        * x0
    )

    energy_total = (
        energy_outer
        + energy_inner
    )

    def gamma_o(
        radius: float,
    ) -> float:

        return (
            energy_outer
            - math.pi
            * radius
            * radius
        ) / (
            2.0
            * math.pi
            * mu_outer
            * radius
        )

    def gamma_i(
        radius: float,
    ) -> float:

        return (
            energy_inner
            + math.pi
            * radius
            * radius
        ) / (
            2.0
            * math.pi
            * mu_inner
            * radius
        )

    def rhs(
        _time: float,
        y: np.ndarray,
    ) -> list[float]:

        ro = float(
            y[0]
        )

        ri = float(
            y[1]
        )

        go = gamma_o(
            ro
        )

        gi = gamma_i(
            ri
        )

        if (
            go < 1.0
            or gi < 1.0
        ):
            return [
                0.0,
                0.0,
            ]

        bo = math.sqrt(
            max(
                0.0,
                1.0
                - 1.0
                / (
                    go
                    * go
                ),
            )
        )

        bi = math.sqrt(
            max(
                0.0,
                1.0
                - 1.0
                / (
                    gi
                    * gi
                ),
            )
        )

        return [
            bo,
            bi,
        ]

    def catch_event(
        _time: float,
        y: np.ndarray,
    ) -> float:

        return float(
            y[0]
            - y[1]
        )

    catch_event.terminal = True
    catch_event.direction = -1

    def turn_event(
        _time: float,
        y: np.ndarray,
    ) -> float:

        return (
            gamma_o(
                float(
                    y[0]
                )
            )
            - 1.0
        )

    turn_event.terminal = True
    turn_event.direction = -1

    epsilon = max(
        1.0e-12,
        fast_duration
        * 1.0e-6,
    )

    y0 = np.array(
        [
            x0
            + v_outer
            * epsilon,

            x0
            + v_inner
            * epsilon,
        ],
        dtype=float,
    )

    t_end = max(
        3.0
        * fast_duration,
        100.0
        * epsilon,
    )

    solution = solve_ivp(
        rhs,
        (
            epsilon,
            t_end,
        ),
        y0,
        events=[
            catch_event,
            turn_event,
        ],
        rtol=1.0e-11,
        atol=1.0e-13,
        max_step=max(
            fast_duration
            / 500.0,
            1.0e-12,
        ),
        dense_output=True,
    )

    if (
        len(
            solution.t_events[
                0
            ]
        )
        == 0
    ):
        return {
            "closed":
                False,

            "outer_turn_detected":
                (
                    len(
                        solution.t_events[
                            1
                        ]
                    )
                    > 0
                ),
        }

    t_close = float(
        solution.t_events[
            0
        ][
            0
        ]
    )

    t = np.linspace(
        epsilon,
        t_close,
        4001,
    )

    values = solution.sol(
        t
    )

    ro = values[
        0
    ]

    ri = values[
        1
    ]

    go = (
        energy_outer
        - math.pi
        * ro
        * ro
    ) / (
        2.0
        * math.pi
        * mu_outer
        * ro
    )

    gi = (
        energy_inner
        + math.pi
        * ri
        * ri
    ) / (
        2.0
        * math.pi
        * mu_inner
        * ri
    )

    bo_sq = np.maximum(
        0.0,
        1.0
        - 1.0
        / (
            go
            * go
        ),
    )

    bi_sq = np.maximum(
        0.0,
        1.0
        - 1.0
        / (
            gi
            * gi
        ),
    )

    wall_outward = (
        2.0
        * math.pi
        * (
            1.0
            / np.sqrt(
                1.0
                + ri
                * ri
            )
            -
            1.0
            / np.sqrt(
                1.0
                + ro
                * ro
            )
        )
    )

    q_outer_active = (
        4.0
        * math.pi
        * mu_outer
        * ro
        * go
        * bo_sq
    )

    q_inner_active = (
        4.0
        * math.pi
        * mu_inner
        * ri
        * gi
        * bi_sq
    )

    outward = (
        wall_outward
        -
        q_outer_active
        / (
            1.0
            + ro
            * ro
        ) ** 1.5
        -
        q_inner_active
        / (
            1.0
            + ri
            * ri
        ) ** 1.5
    )

    impulse = float(
        np.trapezoid(
            outward,
            t,
        )
    )

    return {
        "closed":
            True,

        "eta":
            impulse
            / energy_total,

        "max_outward":
            float(
                np.max(
                    outward
                )
            ),

        "duration":
            t_close,
    }


def main() -> None:
    """Execute 024B3."""

    if not INPUT.is_file():
        raise RuntimeError(
            f"Missing required input: {INPUT}"
        )

    prior = json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )

    decisions = prior[
        "decisions"
    ]

    if (
        decisions[
            "PULSE_BRANCH"
        ]
        !=
        "RED_LOCAL_STATIONARY_RIM_SUPPORT"
    ):
        raise RuntimeError(
            "Unexpected 024B2 pulse state."
        )

    c_input = float(
        prior[
            "006D"
        ][
            "C"
        ]
    )

    if (
        abs(
            c_input
            - C006D
        )
        > 5.0e-13
    ):
        raise RuntimeError(
            "006D coefficient regression."
        )

    all_rows: list[
        dict[str, Any]
    ] = []

    closed_cases: list[
        dict[str, Any]
    ] = []

    turned_cases = 0
    invalid_cases = 0

    scan_specs = [
        (
            "SOBOL_BASE",
            False,
            None,
            13,
            321,
        ),
        (
            "SOBOL_SCRAMBLE_1",
            True,
            1,
            11,
            241,
        ),
        (
            "SOBOL_SCRAMBLE_7",
            True,
            7,
            11,
            241,
        ),
        (
            "SOBOL_SCRAMBLE_23",
            True,
            23,
            11,
            241,
        ),
        (
            "SOBOL_SCRAMBLE_101",
            True,
            101,
            11,
            241,
        ),
    ]

    for (
        label,
        scramble,
        seed,
        power,
        n,
    ) in scan_specs:

        sampler = qmc.Sobol(
            d=5,
            scramble=scramble,
            seed=seed,
        )

        points = sampler.random_base2(
            power
        )

        for index, u in enumerate(
            points
        ):

            (
                x0,
                q_outer,
                q_inner,
                v_outer,
                fraction,
            ) = map_parameters(
                u
            )

            result = evaluate_fast(
                x0,
                q_outer,
                q_inner,
                v_outer,
                fraction,
                n=n,
            )

            if result is None:
                invalid_cases += 1

                all_rows.append({
                    "scan":
                        label,

                    "index":
                        index,

                    "status":
                        "INVALID_MONOTONIC_BRANCH",

                    "x0":
                        x0,

                    "q_outer":
                        q_outer,

                    "q_inner":
                        q_inner,

                    "v_outer":
                        v_outer,

                    "v_inner_over_v_outer":
                        fraction,

                    "eta":
                        "",

                    "max_outward":
                        "",

                    "C_peak":
                        "",

                    "duration":
                        "",

                    "meeting_radius":
                        "",

                    "energy_conservation_relative":
                        "",
                })

                continue

            if (
                result[
                    "status"
                ]
                ==
                "OUTER_TURN_BEFORE_CLOSURE"
            ):
                turned_cases += 1

            else:
                closed_cases.append(
                    result
                )

            all_rows.append({
                "scan":
                    label,

                "index":
                    index,

                "status":
                    result[
                        "status"
                    ],

                "x0":
                    result[
                        "x0"
                    ],

                "q_outer":
                    result[
                        "q_outer"
                    ],

                "q_inner":
                    result[
                        "q_inner"
                    ],

                "v_outer":
                    result[
                        "v_outer"
                    ],

                "v_inner_over_v_outer":
                    result[
                        "v_inner_over_v_outer"
                    ],

                "eta":
                    (
                        result[
                            "eta"
                        ]
                        if result[
                            "eta"
                        ]
                        is not None
                        else ""
                    ),

                "max_outward":
                    (
                        result[
                            "max_outward"
                        ]
                        if result[
                            "max_outward"
                        ]
                        is not None
                        else ""
                    ),

                "C_peak":
                    (
                        result[
                            "C_peak"
                        ]
                        if result[
                            "C_peak"
                        ]
                        is not None
                        else ""
                    ),

                "duration":
                    (
                        result[
                            "duration"
                        ]
                        if result[
                            "duration"
                        ]
                        is not None
                        else ""
                    ),

                "meeting_radius":
                    (
                        result[
                            "meeting_radius"
                        ]
                        if result[
                            "meeting_radius"
                        ]
                        is not None
                        else ""
                    ),

                "energy_conservation_relative":
                    (
                        result[
                            "energy_conservation_relative"
                        ]
                        if result[
                            "energy_conservation_relative"
                        ]
                        is not None
                        else ""
                    ),
            })

    if not closed_cases:
        raise RuntimeError(
            "No geometrically closed cases found."
        )

    positive_eta_cases = [
        case
        for case
        in closed_cases
        if float(
            case[
                "eta"
            ]
        )
        > 0.0
    ]

    positive_instant_cases = [
        case
        for case
        in closed_cases
        if float(
            case[
                "max_outward"
            ]
        )
        > 0.0
    ]

    ge10_positive_cases = [
        case
        for case
        in closed_cases
        if (
            float(
                case[
                    "eta"
                ]
            )
            > 0.0
            and
            case[
                "C_peak"
            ]
            is not None
            and
            float(
                case[
                    "C_peak"
                ]
            )
            <=
            C006D
            / 10.0
        )
    ]

    best_eta = max(
        closed_cases,
        key=lambda item: float(
            item[
                "eta"
            ]
        ),
    )

    best_instant = max(
        closed_cases,
        key=lambda item: float(
            item[
                "max_outward"
            ]
        ),
    )

    max_energy_residual = max(
        float(
            case[
                "energy_conservation_relative"
            ]
        )
        for case
        in closed_cases
    )

    # Independent direct-ODE checks on the two points
    # closest to changing sign.

    refined_best_eta = (
        refine_with_ivp(
            best_eta
        )
    )

    refined_best_instant = (
        refine_with_ivp(
            best_instant
        )
    )

    refinement_pass = (
        bool(
            refined_best_eta.get(
                "closed",
                False,
            )
        )
        and
        bool(
            refined_best_instant.get(
                "closed",
                False,
            )
        )
        and
        float(
            refined_best_eta[
                "eta"
            ]
        )
        < 0.0
        and
        float(
            refined_best_eta[
                "max_outward"
            ]
        )
        < 0.0
        and
        float(
            refined_best_instant[
                "eta"
            ]
        )
        < 0.0
        and
        float(
            refined_best_instant[
                "max_outward"
            ]
        )
        < 0.0
    )

    if not refinement_pass:
        raise RuntimeError(
            "Independent ODE sign audit did not preserve "
            "the primary scan conclusion."
        )

    wildcard_results: list[
        dict[str, Any]
    ] = []

    for x0 in WILDCARD_X:

        item = evaluate_fast(
            x0=x0,
            q_outer=0.03,
            q_inner=0.03,
            v_outer=0.95,
            fraction=0.25,
            n=1001,
        )

        if item is None:
            raise RuntimeError(
                "Wildcard trajectory invalid."
            )

        wildcard_results.append(
            item
        )

    free_annular_red = (
        len(
            positive_eta_cases
        )
        == 0
        and
        len(
            positive_instant_cases
        )
        == 0
        and
        refinement_pass
    )

    if free_annular_red:

        pulse_branch = (
            "PAUSE_CURRENT_PURE_GR_"
            "DOMAIN_WALL_PULSE_FAMILY"
        )

        next_action = (
            "RERANK_006D_MICROSCOPIC_REALIZATION_"
            "VS_023C_023D_AND_ANALOGUE_ANTIGRAVITY"
        )

        analogue = (
            "PRIMARY_RERANK_CANDIDATE_IN_TANDEM"
        )

    else:

        pulse_branch = (
            "YELLOW_SURVIVOR_REQUIRES_REVIEW"
        )

        next_action = (
            "024B3R_REVIEW_SURVIVING_FREE_ANNULAR_CASE"
        )

        analogue = (
            "ACTIVE_IN_TANDEM"
        )

    fieldnames = [
        "scan",
        "index",
        "status",
        "x0",
        "q_outer",
        "q_inner",
        "v_outer",
        "v_inner_over_v_outer",
        "eta",
        "max_outward",
        "C_peak",
        "duration",
        "meeting_radius",
        "energy_conservation_relative",
    ]

    with OUT_SCAN.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(
            all_rows
        )

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_FREE_NAMBU_GOTO_"
                "ANNULAR_PULSE_IMPULSE_PREFILTER"
            ),

        "006D": {
            "C":
                C006D,
        },

        "model": {
            "wall":
                "Nambu-Goto thin domain wall",

            "outer_boundary":
                "free outward-moving Nambu-Goto string",

            "inner_boundary":
                "free outward-moving supercritical "
                "Nambu-Goto string",

            "stationary_support":
                False,

            "initial_wall_area":
                0.0,

            "closure_condition":
                "inner catches outer before outer turns",
        },

        "scan": {
            "requested_cases":
                sum(
                    2 ** spec[
                        3
                    ]
                    for spec
                    in scan_specs
                ),

            "closed_cases":
                len(
                    closed_cases
                ),

            "outer_turn_before_closure_cases":
                turned_cases,

            "invalid_cases":
                invalid_cases,

            "closed_positive_eta_cases":
                len(
                    positive_eta_cases
                ),

            "closed_positive_instantaneous_cases":
                len(
                    positive_instant_cases
                ),

            "closed_ge10_positive_cases":
                len(
                    ge10_positive_cases
                ),

            "maximum_energy_conservation_relative":
                max_energy_residual,

            "best_eta_case":
                best_eta,

            "best_instantaneous_case":
                best_instant,
        },

        "independent_ode_refinement": {
            "pass":
                refinement_pass,

            "best_eta_case":
                refined_best_eta,

            "best_instantaneous_case":
                refined_best_instant,
        },

        "blind_wildcards": {
            "physics_prior":
                False,

            "results":
                wildcard_results,
        },

        "decisions": {
            "FREE_OUTWARD_ANNULAR_WALL_PULSE":
                (
                    "RED_IN_TESTED_NAMBU_GOTO_CLASS"
                    if free_annular_red
                    else
                    "YELLOW_REVIEW"
                ),

            "PURE_GR_DOMAIN_WALL_PULSE_FAMILY":
                pulse_branch,

            "PULSE_MICROSCOPIC_PDE_AUTHORIZED":
                (
                    "NO"
                    if free_annular_red
                    else
                    "REVIEW"
                ),

            "STATIC_006D":
                "KEEP_AS_STRONGEST_TRUE_STANDOFF_SOURCE",

            "STATIC_023C":
                "KEEP_AS_ACTUAL_FIELD_FALLBACK",

            "ANALOGUE_ANTIGRAVITY":
                analogue,

            "NEXT":
                next_action,

            "CURRENT_KNOWLEDGE_HEURISTIC":
                "70_TO_71_PERCENT_RETAINED",

            "PRACTICAL_ANTIGRAVITY_DEVICE":
                "NO",
        },

        "claim_limits": [
            "NO_UNIVERSAL_TRANSIENT_GR_NO_GO",
            "NO_MICROSCOPIC_BOUNDARY_CREATION_SOLUTION",
            "NO_ANNIHILATION_RADIATION_LEDGER",
            "NO_NONLINEAR_GR",
            "NO_PRACTICAL_DEVICE",
        ],
    }

    OUT_SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== 024B3 FREE OUTWARD ANNULAR "
        "WALL PULSE GATE ==="
    )

    print(
        "C_006D="
        f"{C006D:.15f}"
    )

    print()

    print(
        "=== PRIMARY LOW-DISCREPANCY SCAN ==="
    )

    requested = sum(
        2 ** spec[
            3
        ]
        for spec
        in scan_specs
    )

    print(
        "ANNULAR_REQUESTED_CASES="
        f"{requested}"
    )

    print(
        "ANNULAR_CLOSED_BEFORE_TURN_CASES="
        f"{len(closed_cases)}"
    )

    print(
        "ANNULAR_OUTER_TURN_BEFORE_CLOSURE_CASES="
        f"{turned_cases}"
    )

    print(
        "ANNULAR_INVALID_MONOTONIC_CASES="
        f"{invalid_cases}"
    )

    print(
        "ANNULAR_CLOSED_POSITIVE_ETA_CASES="
        f"{len(positive_eta_cases)}"
    )

    print(
        "ANNULAR_CLOSED_POSITIVE_"
        "INSTANTANEOUS_CASES="
        f"{len(positive_instant_cases)}"
    )

    print(
        "ANNULAR_CLOSED_GE10_POSITIVE_CASES="
        f"{len(ge10_positive_cases)}"
    )

    print(
        "ANNULAR_MAX_ENERGY_CONSERVATION_REL="
        f"{max_energy_residual:.3e}"
    )

    print()

    print(
        "=== CLOSEST-TO-ZERO CASES ==="
    )

    print(
        "ANNULAR_BEST_ETA="
        f"{float(best_eta['eta']):+.15e}"
    )

    print(
        "ANNULAR_BEST_ETA_MAX_OUTWARD="
        f"{float(best_eta['max_outward']):+.15e}"
    )

    print(
        "ANNULAR_BEST_INSTANTANEOUS="
        f"{float(best_instant['max_outward']):+.15e}"
    )

    print(
        "ANNULAR_BEST_INSTANTANEOUS_ETA="
        f"{float(best_instant['eta']):+.15e}"
    )

    print()

    print(
        "=== INDEPENDENT DIRECT-ODE AUDIT ==="
    )

    print(
        "REFINEMENT_PASS="
        + (
            "YES"
            if refinement_pass
            else
            "NO"
        )
    )

    print(
        "REFINED_BEST_ETA="
        f"{float(refined_best_eta['eta']):+.15e}"
    )

    print(
        "REFINED_BEST_ETA_MAX_OUTWARD="
        f"{float(refined_best_eta['max_outward']):+.15e}"
    )

    print(
        "REFINED_BEST_INSTANTANEOUS="
        f"{float(refined_best_instant['max_outward']):+.15e}"
    )

    print(
        "REFINED_BEST_INSTANTANEOUS_ETA="
        f"{float(refined_best_instant['eta']):+.15e}"
    )

    print()

    print(
        "=== BLIND WILDCARD X0 CHECK ==="
    )

    for item in wildcard_results:

        print(
            "WILDCARD_X="
            f"{float(item['x0']):.6f}"
            " "
            "ETA="
            f"{float(item['eta']):+.12e}"
            " "
            "MAX_OUTWARD="
            f"{float(item['max_outward']):+.12e}"
        )

    print(
        "WILDCARDS_ARE_PHYSICS_PRIORS=NO"
    )

    print()

    print(
        "=== 024B3 DECISION ==="
    )

    print(
        "FREE_OUTWARD_ANNULAR_WALL_PULSE="
        + (
            "RED_IN_TESTED_NAMBU_GOTO_CLASS"
            if free_annular_red
            else
            "YELLOW_REVIEW"
        )
    )

    print(
        "PURE_GR_DOMAIN_WALL_PULSE_FAMILY="
        f"{pulse_branch}"
    )

    print(
        "PULSE_MICROSCOPIC_PDE_AUTHORIZED="
        + (
            "NO"
            if free_annular_red
            else
            "REVIEW"
        )
    )

    print(
        "STATIC_006D="
        "KEEP_AS_STRONGEST_TRUE_STANDOFF_SOURCE"
    )

    print(
        "STATIC_023C="
        "KEEP_AS_ACTUAL_FIELD_FALLBACK"
    )

    print(
        "ANALOGUE_ANTIGRAVITY="
        f"{analogue}"
    )

    print(
        "NEXT="
        f"{next_action}"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "70_TO_71_PERCENT_RETAINED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "SUMMARY_JSON="
        f"{OUT_SUMMARY.relative_to(ROOT)}"
    )

    print(
        "SCAN_CSV="
        f"{OUT_SCAN.relative_to(ROOT)}"
    )

    print(
        "024B3_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
