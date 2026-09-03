#!/usr/bin/env python3
"""027A — canonical-scalar stress-cycle / true-stand-off transport preflight.

PURPOSE
-------
Test a microscopic-source bridge exposed by 026P.

For a canonical scalar,

    rho = 1/2 phi_dot^2 + 1/2 |grad phi|^2 + V

and

    S = rho + p_x + p_y + p_z
      = 2 phi_dot^2 - 2 V.

Therefore the spatial-gradient contribution cancels from the active trace.

In a locally homogeneous oscillating core:

    potential turning point:
        S/rho = -2

    kinetic crossing with V approximately zero:
        S/rho = +4.

These are exactly the local type-I DEC endpoints explored by the relaxed
026P fixed-rho optimization.

SCIENTIFIC QUESTION
-------------------
Can a conservative canonical-scalar stress cycle close a large fraction of
the approximately 9.7x B7 negative-active participation gap and retain a
true one-sided finite-payload outward response after:

    finite localization;
    counterflow momentum cancellation;
    cycle-averaged Laue compensation;
    guide/support energy;
    curvature/confinement proxies;
    finite reset windows;
    phase jitter;
    resolution refinement;
    independent reconstruction?

This is deliberately a cheap pre-PDE falsification gate.

ANALYTIC HARMONIC CONTROL
-------------------------
For

    phi = A cos(theta)

one has

    S/rho = 1 - 3 cos(2 theta).

The negative-active duty is

    f_neg = acos(1/3) / pi.

The gross negative source is

    Q_neg = [2 sqrt(2) - acos(1/3)] / pi.

For an ideal two-kernel conveyor, outward sign requires

    K_high / K_low
        >
    Q_pos / Q_neg.

A constant-radius circular path has K_high/K_low=1 and is therefore an exact
RED control.

POTENTIAL FAMILY
----------------
Scan the bounded positive sextic family

    V/E
      =
    (1+a+b) x^2
    -
    (a+2b) x^4
    +
    b x^6,

with

    x = phi/A.

Require

    0 <= a < 1

and

    b >= a^2/4.

The second condition makes the quadratic bracket in x^2 globally
nonnegative.  The family therefore has:

    positive quadratic term;
    attractive negative quartic term;
    stabilizing positive sextic term.

For every potential, compute:

    omega / m_vacuum;
    negative-active duty;
    gross negative source;
    cycle-mean active source;
    minimum DEC-saturating compensation;
    ideal kernel-ratio threshold;
    ideal separated coefficient.

TRUE-STANDOFF GEOMETRY
----------------------
The payload center is at

    (0,0,h), h=1.

All finite source tubes are kept at or below

    z=0.

Two closed-path families are tested:

    ELLIPSE

and

    2n-LOBED ROSETTE.

The internal oscillator phase is locked to arclength so that potential
turning points preferentially occupy high-kernel regions and kinetic/reset
phases occupy low-kernel regions.

For counterpropagating equal streams, local T_0s cancels by construction.
Kinetic and pressure stresses remain in the ledger.

FINITE LOCALIZATION
-------------------
For oscillator frequency omega and vacuum mass m,

    chi = omega/m < 1

gives the asymptotic massive-scalar tail scale

    kappa_tail = sqrt(m^2 - omega^2).

The diagnostic core radius is

    R_core = N_tail/kappa_tail

for

    N_tail = 1, 2.

This is a localization prefilter, not a solved oscillon profile.

Finite tubes use an adverse five-point kernel envelope:

    useful negative-active source gets K_min;
    opposing positive-active source gets K_max.

SUPPORT MODELS
--------------
Three finite support ledgers are separated.

LOC_GUIDE_NEUTRAL:

    Gaussian localization-energy proxy;
    024D-like beta^2 guide floor;
    both active-neutral before Laue closure.

FULL_NEUTRAL:

    same;
    plus local curvature/traction energy proxy;
    support remains active-neutral before Laue closure.

FULL_MASSLIKE:

    same total support energy;
    support contributes positive masslike active source.

These are explicit prefield brackets.

They are not microscopic support solutions.

CYCLE-AVERAGED LAUE CLOSURE
---------------------------
After mobile and support sectors are assembled, impose

    <S_total> = E_total

with the minimum DEC-saturating compensation sector.

If more positive active source is required:

    q_comp = +4.

If more negative active source is required:

    q_comp = -2.

Compensation is placed in a finite 10-percent low- or high-kernel window,
not at a mathematical point.

PROMOTION
---------
A finite source-engine survivor requires:

    C < C_006D;
    finite one-sided core;
    negative-active participation > current B7;
    tube_curvature <= 0.5.

A major preflight additionally requires:

    C < C_024D_scalar;
    medium/high C change <= 10 percent;
    high/independent C change <= 3 percent;
    every declared phase-jitter case outward;
    worst phase-jitter C < C_006D.

FALSIFIERS
----------
If even point-source phase locking is inward, close this transport class.

If point-source transport survives but every finite localized source dies,
record localization/support obstruction and do not launch a full PDE.

If a robust finite survivor exists, authorize 027B.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_CANONICAL_SCALAR_STRESS_TRANSPORT_PREFLIGHT

DOES NOT ESTABLISH
------------------
- a microscopic field solution;
- full dynamic local T_munu conservation;
- reaction-momentum closure;
- oscillon radiation lifetime;
- full stability;
- nonlinear Einstein-matter consistency;
- escape from 1/G scaling;
- an experiment;
- a practical antigravity device.
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from typing import Any

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import solve_ivp
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

OUT_JSON = (
    DATA
    / "027a_phase_locked_scalar_transport_summary.json"
)

OUT_POT = (
    DATA
    / "027a_scalar_potential_frontier.csv"
)

OUT_GEO = (
    DATA
    / "027a_phase_locked_geometry_top.csv"
)

OUT_WILD = (
    DATA
    / "027a_phase_locked_wildcard_audit.csv"
)


C_006D = 23.591586299249

C_024D_SCALAR = 6.610457607426174

PAYLOAD_RADIUS_OVER_H = (
    0.043298860805059215
)

DEFAULT_B7_NEGATIVE_ACTIVE_FRACTION = (
    0.051465043743791114
)


POT_POWER = int(
    os.environ.get(
        "AG027_POT_POWER",
        "13",
    )
)

GEO_POWER = int(
    os.environ.get(
        "AG027_GEO_POWER",
        "13",
    )
)

COARSE_N = int(
    os.environ.get(
        "AG027_COARSE_N",
        "384",
    )
)

MEDIUM_N = int(
    os.environ.get(
        "AG027_MEDIUM_N",
        "4096",
    )
)

HIGH_N = int(
    os.environ.get(
        "AG027_HIGH_N",
        "16384",
    )
)

INDEPENDENT_N = int(
    os.environ.get(
        "AG027_INDEPENDENT_N",
        "65536",
    )
)


TOP_KEEP = 60

WINDOW_FRACTION = 0.10

PHASE_JITTERS = (
    -0.20,
    -0.10,
    0.0,
    0.10,
    0.20,
)

TAIL_LEVELS = (
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


# Endpoint-removing quadrature for oscillator quarter-cycle integrals.
_gx, _gw = leggauss(
    192
)

_y = (
    _gx
    +
    1.0
) / 2.0

_wy = (
    _gw
    /
    2.0
)

_xq = (
    1.0
    -
    _y * _y
)

_jac = (
    2.0
    *
    _y
)


def f64(
    x: Any,
) -> float:

    return float(
        np.asarray(
            x
        )
    )


def read_b7_fraction(
) -> tuple[
    float,
    str,
]:

    p = (
        DATA
        / "026p_true_antigravity_practicality_escape_summary.json"
    )

    if not p.exists():

        return (
            DEFAULT_B7_NEGATIVE_ACTIVE_FRACTION,
            "CARRY_OVER_CONSTANT",
        )

    try:

        d = json.loads(
            p.read_text()
        )

        val = float(
            d[
                "field_comparison"
            ][
                "N81"
            ][
                "negative_active_energy_fraction"
            ]
        )

        return (
            val,
            "026P_JSON",
        )

    except Exception:

        return (
            DEFAULT_B7_NEGATIVE_ACTIVE_FRACTION,
            "CARRY_OVER_CONSTANT_PARSE_FALLBACK",
        )


def potential_v(
    x: np.ndarray | float,
    a: float,
    b: float,
) -> np.ndarray | float:

    return (
        (
            1.0
            +
            a
            +
            b
        )
        *
        x**2
        -
        (
            a
            +
            2.0 * b
        )
        *
        x**4
        +
        b
        *
        x**6
    )


def potential_dv(
    x: np.ndarray | float,
    a: float,
    b: float,
) -> np.ndarray | float:

    return (
        2.0
        *
        (
            1.0
            +
            a
            +
            b
        )
        *
        x
        -
        4.0
        *
        (
            a
            +
            2.0 * b
        )
        *
        x**3
        +
        6.0
        *
        b
        *
        x**5
    )


def potential_metrics(
    a: float,
    b: float,
) -> dict[
    str,
    float,
] | None:

    if not (
        0.0
        <=
        a
        <
        0.9995
        and
        b
        >=
        0.0
        and
        a * a
        <=
        4.0 * b
        +
        1e-14
    ):

        return None

    xx = np.linspace(
        0.0,
        1.0,
        1201,
    )

    vv = np.asarray(
        potential_v(
            xx,
            a,
            b,
        ),
        dtype=float,
    )

    dv = np.asarray(
        potential_dv(
            xx,
            a,
            b,
        ),
        dtype=float,
    )

    if (
        vv.min()
        <
        -2e-11
        or
        vv.max()
        >
        1.0
        +
        2e-10
        or
        dv.min()
        <
        -2e-8
    ):

        return None

    v = np.asarray(
        potential_v(
            _xq,
            a,
            b,
        ),
        dtype=float,
    )

    denom = np.sqrt(
        np.maximum(
            1.0
            -
            v,
            1e-300,
        )
    )

    base = (
        _jac
        /
        denom
    )

    I = f64(
        np.sum(
            _wy
            *
            base
        )
    )

    vpp0 = (
        2.0
        *
        (
            1.0
            +
            a
            +
            b
        )
    )

    chi = (
        math.pi
        *
        math.sqrt(
            2.0
        )
        /
        (
            2.0
            *
            I
            *
            math.sqrt(
                vpp0
            )
        )
    )

    if (
        chi
        >
        1.0
        and
        chi
        <
        1.0
        +
        5e-10
    ):

        chi = 1.0

    if not (
        0.0
        <
        chi
        <=
        1.0
        +
        1e-8
    ):

        return None

    q = (
        4.0
        -
        6.0
        *
        v
    )

    qbar = f64(
        np.sum(
            _wy
            *
            base
            *
            q
        )
        /
        I
    )

    qneg = f64(
        np.sum(
            _wy
            *
            base
            *
            np.maximum(
                -q,
                0.0,
            )
        )
        /
        I
    )

    qpos = f64(
        np.sum(
            _wy
            *
            base
            *
            np.maximum(
                q,
                0.0,
            )
        )
        /
        I
    )

    neg_duty = f64(
        np.sum(
            _wy
            *
            base
            *
            (
                q
                <
                0.0
            )
        )
        /
        I
    )

    # Minimum source-level DEC-saturating compensation needed for
    # cycle-averaged Laue closure.
    if (
        qbar
        <=
        1.0
    ):

        e_comp = (
            1.0
            -
            qbar
        ) / 3.0

        q_comp = (
            4.0
        )

        ratio_crit = (
            qpos
            +
            4.0
            *
            e_comp
        ) / max(
            qneg,
            1e-300,
        )

        separated_outward = (
            qneg
        )

    else:

        e_comp = (
            qbar
            -
            1.0
        ) / 3.0

        q_comp = (
            -2.0
        )

        ratio_crit = (
            qpos
            /
            max(
                qneg
                +
                2.0
                *
                e_comp,
                1e-300,
            )
        )

        separated_outward = (
            qneg
            +
            2.0
            *
            e_comp
        )

    c_separated = (
        1.0
        +
        e_comp
    ) / max(
        separated_outward,
        1e-300,
    )

    return {
        "a":
            float(
                a
            ),

        "b":
            float(
                b
            ),

        "chi_omega_over_m":
            float(
                min(
                    chi,
                    1.0,
                )
            ),

        "qbar_mobile":
            qbar,

        "gross_negative_q":
            qneg,

        "gross_positive_q":
            qpos,

        "negative_duty":
            neg_duty,

        "minimal_compensation_energy":
            e_comp,

        "compensation_q":
            q_comp,

        "ideal_kernel_ratio_threshold":
            ratio_crit,

        "ideal_separated_C":
            c_separated,
    }


def harmonic_exact(
) -> dict[
    str,
    float,
]:

    alpha = math.acos(
        1.0
        /
        3.0
    )

    fneg = (
        alpha
        /
        math.pi
    )

    qneg = (
        2.0
        *
        math.sqrt(
            2.0
        )
        -
        alpha
    ) / math.pi

    qpos = (
        1.0
        +
        qneg
    )

    return {
        "a":
            0.0,

        "b":
            0.0,

        "chi_omega_over_m":
            1.0,

        "qbar_mobile":
            1.0,

        "gross_negative_q":
            qneg,

        "gross_positive_q":
            qpos,

        "negative_duty":
            fneg,

        "minimal_compensation_energy":
            0.0,

        "compensation_q":
            0.0,

        "ideal_kernel_ratio_threshold":
            qpos
            /
            qneg,

        "ideal_separated_C":
            1.0
            /
            qneg,
    }


def make_waveform(
    pot: dict[
        str,
        float,
    ],
    n: int = 8192,
) -> dict[
    str,
    np.ndarray,
]:

    a = pot[
        "a"
    ]

    b = pot[
        "b"
    ]

    if (
        a
        ==
        0.0
        and
        b
        ==
        0.0
    ):

        tau = (
            np.arange(
                n,
                dtype=float,
            )
            +
            0.5
        ) / n

        q = (
            1.0
            -
            3.0
            *
            np.cos(
                4.0
                *
                math.pi
                *
                tau
            )
        )

        return {
            "tau":
                tau,

            "q":
                q,
        }

    vpp0 = (
        2.0
        *
        (
            1.0
            +
            a
            +
            b
        )
    )

    omega = (
        pot[
            "chi_omega_over_m"
        ]
        *
        math.sqrt(
            vpp0
        )
    )

    period = (
        2.0
        *
        math.pi
        /
        omega
    )

    def rhs(
        _t: float,
        y: np.ndarray,
    ) -> list[
        float
    ]:

        return [
            float(
                y[
                    1
                ]
            ),
            -float(
                potential_dv(
                    y[
                        0
                    ],
                    a,
                    b,
                )
            ),
        ]

    sol = solve_ivp(
        rhs,
        (
            0.0,
            period,
        ),
        np.array(
            [
                1.0,
                0.0,
            ]
        ),
        rtol=2e-10,
        atol=2e-12,
        dense_output=True,
        max_step=(
            period
            /
            1600.0
        ),
    )

    if not sol.success:

        raise RuntimeError(
            "waveform integration failed"
        )

    tau = (
        np.arange(
            n,
            dtype=float,
        )
        +
        0.5
    ) / n

    x = sol.sol(
        tau
        *
        period
    )[
        0
    ]

    v = np.asarray(
        potential_v(
            x,
            a,
            b,
        ),
        dtype=float,
    )

    q = (
        4.0
        -
        6.0
        *
        v
    )

    return {
        "tau":
            tau,

        "q":
            q,
    }


def build_curve(
    kind: str,
    p1: float,
    p2: float,
    ncycle: int,
    n: int,
) -> dict[
    str,
    np.ndarray | float,
]:

    u = (
        np.arange(
            n,
            dtype=float,
        )
        +
        0.5
    ) * (
        2.0
        *
        math.pi
        /
        n
    )

    if (
        kind
        ==
        "ELLIPSE"
    ):

        semimajor = (
            p1
        )

        aspect = (
            p2
        )

        semiminor = (
            semimajor
            *
            aspect
        )

        x = (
            semimajor
            *
            np.sin(
                u
            )
        )

        y = (
            semiminor
            *
            np.cos(
                u
            )
        )

        dx = (
            semimajor
            *
            np.cos(
                u
            )
        )

        dy = (
            -semiminor
            *
            np.sin(
                u
            )
        )

        ddx = (
            -semimajor
            *
            np.sin(
                u
            )
        )

        ddy = (
            -semiminor
            *
            np.cos(
                u
            )
        )

    elif (
        kind
        ==
        "ROSETTE"
    ):

        R = (
            p1
        )

        e = (
            p2
        )

        r0 = (
            R
            *
            (
                1.0
                -
                e
                *
                np.cos(
                    2.0
                    *
                    ncycle
                    *
                    u
                )
            )
        )

        dr = (
            2.0
            *
            ncycle
            *
            R
            *
            e
            *
            np.sin(
                2.0
                *
                ncycle
                *
                u
            )
        )

        d2r = (
            4.0
            *
            ncycle
            *
            ncycle
            *
            R
            *
            e
            *
            np.cos(
                2.0
                *
                ncycle
                *
                u
            )
        )

        cu = np.cos(
            u
        )

        su = np.sin(
            u
        )

        x = (
            r0
            *
            cu
        )

        y = (
            r0
            *
            su
        )

        dx = (
            dr
            *
            cu
            -
            r0
            *
            su
        )

        dy = (
            dr
            *
            su
            +
            r0
            *
            cu
        )

        ddx = (
            (
                d2r
                -
                r0
            )
            *
            cu
            -
            2.0
            *
            dr
            *
            su
        )

        ddy = (
            (
                d2r
                -
                r0
            )
            *
            su
            +
            2.0
            *
            dr
            *
            cu
        )

    else:

        raise ValueError(
            kind
        )

    speed = np.sqrt(
        dx * dx
        +
        dy * dy
    )

    ds = (
        speed
        *
        (
            2.0
            *
            math.pi
            /
            n
        )
    )

    length = f64(
        np.sum(
            ds
        )
    )

    w = (
        ds
        /
        length
    )

    sfrac = (
        np.cumsum(
            ds
        )
        -
        0.5
        *
        ds
    ) / length

    radius = np.sqrt(
        x * x
        +
        y * y
    )

    curvature = (
        np.abs(
            dx
            *
            ddy
            -
            dy
            *
            ddx
        )
        /
        np.maximum(
            speed**3,
            1e-300,
        )
    )

    return {
        "radius":
            radius,

        "curvature":
            curvature,

        "w":
            w,

        "sfrac":
            sfrac,

        "length":
            length,
    }


def kernel(
    radius: np.ndarray,
    z: float,
) -> np.ndarray:

    dz = (
        1.0
        -
        z
    )

    return (
        dz
        /
        np.maximum(
            radius
            *
            radius
            +
            dz
            *
            dz,
            1e-300,
        ) ** 1.5
    )


def finite_window_mean(
    values: np.ndarray,
    fraction: float,
    high: bool,
) -> float:

    n = len(
        values
    )

    k = max(
        1,
        int(
            math.ceil(
                fraction
                *
                n
            )
        ),
    )

    idx = np.argpartition(
        values,
        n - k
        if high
        else
        k - 1,
    )

    if high:

        sel = idx[
            -k:
        ]

    else:

        sel = idx[
            :k
        ]

    return f64(
        np.mean(
            values[
                sel
            ]
        )
    )


def evaluate_geometry(
    kind: str,
    p1: float,
    p2: float,
    ncycle: int,
    beta: float,
    pot: dict[
        str,
        float,
    ],
    wave: dict[
        str,
        np.ndarray,
    ],
    n: int,
    tail_n: float | None,
    model: str,
    phase_delta: float = 0.0,
) -> dict[
    str,
    Any,
]:

    c = build_curve(
        kind,
        p1,
        p2,
        ncycle,
        n,
    )

    radius = np.asarray(
        c[
            "radius"
        ],
        dtype=float,
    )

    curvature = np.asarray(
        c[
            "curvature"
        ],
        dtype=float,
    )

    w = np.asarray(
        c[
            "w"
        ],
        dtype=float,
    )

    sfrac = np.asarray(
        c[
            "sfrac"
        ],
        dtype=float,
    )

    length = float(
        c[
            "length"
        ]
    )

    gamma = (
        1.0
        /
        math.sqrt(
            1.0
            -
            beta
            *
            beta
        )
    )

    phase = (
        ncycle
        *
        sfrac
        +
        phase_delta
        /
        (
            2.0
            *
            math.pi
        )
    ) % 1.0

    q_rest = np.interp(
        phase,
        wave[
            "tau"
        ],
        wave[
            "q"
        ],
        period=1.0,
    )

    p_rest = (
        q_rest
        -
        1.0
    ) / 3.0

    # Exact Lorentz transform of a locally homogeneous scalar stress state.
    e_mobile = (
        gamma
        *
        gamma
        *
        (
            1.0
            +
            beta
            *
            beta
            *
            p_rest
        )
    )

    s_mobile = (
        gamma
        *
        gamma
        *
        (
            1.0
            +
            beta
            *
            beta
        )
        *
        (
            1.0
            +
            p_rest
        )
        +
        2.0
        *
        p_rest
    )

    t_stream = (
        gamma
        *
        gamma
        *
        (
            p_rest
            +
            beta
            *
            beta
        )
    )

    E_mobile = f64(
        np.sum(
            w
            *
            e_mobile
        )
    )

    S_mobile = f64(
        np.sum(
            w
            *
            s_mobile
        )
    )

    if (
        tail_n
        is None
    ):

        core = (
            0.0
        )

        z = (
            0.0
        )

        kcenter = kernel(
            radius,
            z,
        )

        ksel = (
            kcenter
        )

        tube_curvature = (
            0.0
        )

        finite_core_clear = (
            True
        )

        loc_energy = (
            0.0
        )

        guide_energy = (
            0.0
        )

        curvature_energy = (
            0.0
        )

    else:

        chi = max(
            min(
                pot[
                    "chi_omega_over_m"
                ],
                1.0
                -
                1e-12,
            ),
            1e-12,
        )

        # ncycle proper oscillator cycles per coordinate loop.
        omega_rest = (
            2.0
            *
            math.pi
            *
            ncycle
            *
            gamma
            *
            beta
            /
            length
        )

        kappa_tail = (
            omega_rest
            *
            math.sqrt(
                1.0
                /
                (
                    chi
                    *
                    chi
                )
                -
                1.0
            )
        )

        if (
            kappa_tail
            <=
            0.0
        ):

            return {
                "valid":
                    False,

                "reason":
                    "NO_LOCALIZED_MASS_GAP",
            }

        core = float(
            tail_n
            /
            kappa_tail
        )

        z = (
            -core
        )

        rmin = f64(
            np.min(
                radius
            )
        )

        kappa_max = f64(
            np.max(
                curvature
            )
        )

        tube_curvature = (
            core
            *
            kappa_max
        )

        finite_core_clear = bool(
            rmin
            -
            core
            >
            0.02
            and
            z
            +
            core
            <=
            1e-12
        )

        if not (
            finite_core_clear
        ):

            return {
                "valid":
                    False,

                "reason":
                    "FINITE_CORE_AXIS_OR_STANDOFF_FAILURE",
            }

        kc = kernel(
            radius,
            z,
        )

        kvals = np.stack(
            [
                kc,

                kernel(
                    np.maximum(
                        radius
                        -
                        core,
                        1e-9,
                    ),
                    z,
                ),

                kernel(
                    radius
                    +
                    core,
                    z,
                ),

                kernel(
                    radius,
                    z
                    -
                    core,
                ),

                kernel(
                    radius,
                    z
                    +
                    core,
                ),
            ]
        )

        kmin = np.min(
            kvals,
            axis=0,
        )

        kmax = np.max(
            kvals,
            axis=0,
        )

        # Adverse finite-tube envelope.
        ksel = np.where(
            s_mobile
            <
            0.0,
            kmin,
            kmax,
        )

        kcenter = (
            kc
        )

        # Explicitly diagnostic, not exact field energies.
        loc_energy = (
            1.5
            *
            (
                1.0
                -
                chi
                *
                chi
            )
            /
            (
                tail_n
                *
                tail_n
            )
        )

        guide_energy = (
            beta
            *
            beta
            *
            E_mobile
        )

        curvature_energy = f64(
            np.sum(
                w
                *
                core
                *
                curvature
                *
                np.abs(
                    t_stream
                )
            )
        )

    I_mobile = f64(
        np.sum(
            w
            *
            s_mobile
            *
            ksel
        )
    )

    K_low = finite_window_mean(
        kcenter,
        WINDOW_FRACTION,
        high=False,
    )

    K_high = finite_window_mean(
        kcenter,
        WINDOW_FRACTION,
        high=True,
    )

    K_avg = f64(
        np.sum(
            w
            *
            kcenter
        )
    )

    if (
        model
        ==
        "POINT_VIRIAL"
    ):

        E_support = (
            0.0
        )

        S_support = (
            0.0
        )

        I_support = (
            0.0
        )

    elif (
        model
        ==
        "LOC_GUIDE_NEUTRAL"
    ):

        E_support = (
            loc_energy
            +
            guide_energy
        )

        S_support = (
            0.0
        )

        I_support = (
            0.0
        )

    elif (
        model
        ==
        "FULL_NEUTRAL"
    ):

        E_support = (
            loc_energy
            +
            guide_energy
            +
            curvature_energy
        )

        S_support = (
            0.0
        )

        I_support = (
            0.0
        )

    elif (
        model
        ==
        "FULL_MASSLIKE"
    ):

        E_support = (
            loc_energy
            +
            guide_energy
            +
            curvature_energy
        )

        S_support = (
            E_support
        )

        I_support = (
            E_support
            *
            K_avg
        )

    else:

        raise ValueError(
            model
        )

    E0 = (
        E_mobile
        +
        E_support
    )

    S0 = (
        S_mobile
        +
        S_support
    )

    # Minimal finite-window DEC compensation enforcing:
    #
    #     S_total = E_total.
    if (
        E0
        >=
        S0
    ):

        E_comp = (
            E0
            -
            S0
        ) / 3.0

        q_comp = (
            4.0
        )

        K_comp = (
            K_low
        )

    else:

        E_comp = (
            S0
            -
            E0
        ) / 3.0

        q_comp = (
            -2.0
        )

        K_comp = (
            K_high
        )

    I_comp = (
        q_comp
        *
        E_comp
        *
        K_comp
    )

    E_total = (
        E0
        +
        E_comp
    )

    S_total = (
        S0
        +
        q_comp
        *
        E_comp
    )

    I_total = (
        I_mobile
        +
        I_support
        +
        I_comp
    )

    A_out = (
        -I_total
    )

    C = (
        E_total
        /
        A_out
        if
        A_out
        >
        0.0
        else
        math.inf
    )

    negative_mobile_energy = f64(
        np.sum(
            w
            *
            e_mobile
            *
            (
                s_mobile
                <
                0.0
            )
        )
    )

    negative_participation = (
        negative_mobile_energy
        /
        E_total
    )

    cancellation = (
        f64(
            np.sum(
                w
                *
                np.abs(
                    s_mobile
                    *
                    ksel
                )
            )
        )
        /
        max(
            abs(
                I_mobile
            ),
            1e-300,
        )
    )

    return {
        "valid":
            True,

        "kind":
            kind,

        "p1":
            float(
                p1
            ),

        "p2":
            float(
                p2
            ),

        "ncycle":
            int(
                ncycle
            ),

        "beta":
            float(
                beta
            ),

        "pot_a":
            float(
                pot[
                    "a"
                ]
            ),

        "pot_b":
            float(
                pot[
                    "b"
                ]
            ),

        "chi":
            float(
                pot[
                    "chi_omega_over_m"
                ]
            ),

        "tail_n":
            None
            if
            tail_n
            is None
            else
            float(
                tail_n
            ),

        "model":
            model,

        "phase_delta":
            float(
                phase_delta
            ),

        "nphase":
            int(
                n
            ),

        "length":
            length,

        "core_radius":
            core,

        "tube_curvature":
            tube_curvature,

        "finite_core_clear":
            finite_core_clear,

        "K_low_window":
            K_low,

        "K_high_window":
            K_high,

        "K_ratio":
            K_high
            /
            max(
                K_low,
                1e-300,
            ),

        "E_mobile":
            E_mobile,

        "S_mobile":
            S_mobile,

        "E_localization_proxy":
            loc_energy,

        "E_guide_floor":
            guide_energy,

        "E_curvature_proxy":
            curvature_energy,

        "E_support":
            E_support,

        "E_compensation":
            E_comp,

        "q_compensation":
            q_comp,

        "E_total":
            E_total,

        "S_total":
            S_total,

        "laue_residual":
            S_total
            -
            E_total,

        "A_out":
            A_out,

        "C":
            C,

        "negative_active_participation":
            negative_participation,

        "cancellation":
            cancellation,
    }


def scan_potentials(
) -> list[
    dict[
        str,
        float,
    ]
]:

    rows: list[
        dict[
            str,
            float,
        ]
    ] = [
        harmonic_exact()
    ]

    sob = qmc.Sobol(
        d=2,
        scramble=True,
        seed=27001,
    ).random_base2(
        POT_POWER
    )

    for u in sob:

        a = (
            0.995
            *
            float(
                u[
                    0
                ]
            )
        )

        b = (
            a
            *
            a
            /
            4.0
            +
            2.75
            *
            float(
                u[
                    1
                ]
            )
        )

        m = potential_metrics(
            a,
            b,
        )

        if (
            m
            is not None
        ):

            rows.append(
                m
            )

    rows.sort(
        key=lambda r:
            r[
                "ideal_separated_C"
            ]
    )

    return rows


def select_potentials(
    rows: list[
        dict[
            str,
            float,
        ]
    ],
) -> list[
    dict[
        str,
        float,
    ]
]:

    selected: list[
        dict[
            str,
            float,
        ]
    ] = [
        harmonic_exact()
    ]

    bins = [
        (
            0.0,
            0.15,
        ),
        (
            0.15,
            0.30,
        ),
        (
            0.30,
            0.50,
        ),
        (
            0.50,
            0.70,
        ),
        (
            0.70,
            0.90,
        ),
        (
            0.90,
            1.000001,
        ),
    ]

    for (
        lo,
        hi,
    ) in bins:

        candidates = [
            r
            for r in rows
            if
            lo
            <=
            r[
                "chi_omega_over_m"
            ]
            <
            hi
        ]

        if candidates:

            selected.append(
                min(
                    candidates,
                    key=lambda r:
                        r[
                            "ideal_separated_C"
                        ],
                )
            )

    selected.extend(
        rows[
            :5
        ]
    )

    unique: dict[
        tuple[
            float,
            float,
        ],
        dict[
            str,
            float,
        ],
    ] = {}

    for r in selected:

        unique[
            (
                round(
                    r[
                        "a"
                    ],
                    12,
                ),
                round(
                    r[
                        "b"
                    ],
                    12,
                ),
            )
        ] = r

    return list(
        unique.values()
    )


def geometry_cases(
    selected: list[
        dict[
            str,
            float,
        ]
    ],
) -> list[
    tuple[
        str,
        float,
        float,
        int,
        float,
        dict[
            str,
            float,
        ],
    ]
]:

    rows: list[
        tuple[
            str,
            float,
            float,
            int,
            float,
            dict[
                str,
                float,
            ],
        ]
    ] = []

    se = qmc.Sobol(
        d=4,
        scramble=True,
        seed=27002,
    ).random_base2(
        GEO_POWER
        -
        1
    )

    for u in se:

        semimajor = math.exp(
            math.log(
                0.35
            )
            +
            float(
                u[
                    0
                ]
            )
            *
            math.log(
                7.0
                /
                0.35
            )
        )

        aspect = (
            0.04
            +
            0.90
            *
            float(
                u[
                    1
                ]
            )
        )

        beta = (
            0.03
            +
            0.82
            *
            float(
                u[
                    2
                ]
            )
        )

        pot = selected[
            min(
                len(
                    selected
                )
                -
                1,
                int(
                    float(
                        u[
                            3
                        ]
                    )
                    *
                    len(
                        selected
                    )
                ),
            )
        ]

        rows.append(
            (
                "ELLIPSE",
                semimajor,
                aspect,
                1,
                beta,
                pot,
            )
        )

    sr = qmc.Sobol(
        d=5,
        scramble=True,
        seed=27003,
    ).random_base2(
        GEO_POWER
        -
        1
    )

    for u in sr:

        R = math.exp(
            math.log(
                0.30
            )
            +
            float(
                u[
                    0
                ]
            )
            *
            math.log(
                6.0
                /
                0.30
            )
        )

        e = (
            0.02
            +
            0.76
            *
            float(
                u[
                    1
                ]
            )
        )

        ncycle = (
            1
            +
            min(
                15,
                int(
                    float(
                        u[
                            2
                        ]
                    )
                    *
                    16.0
                ),
            )
        )

        beta = (
            0.03
            +
            0.82
            *
            float(
                u[
                    3
                ]
            )
        )

        pot = selected[
            min(
                len(
                    selected
                )
                -
                1,
                int(
                    float(
                        u[
                            4
                        ]
                    )
                    *
                    len(
                        selected
                    )
                ),
            )
        ]

        rows.append(
            (
                "ROSETTE",
                R,
                e,
                ncycle,
                beta,
                pot,
            )
        )

    return rows


def row_key(
    row: dict[
        str,
        Any,
    ],
) -> float:

    return float(
        row.get(
            "C",
            math.inf,
        )
    )


def evaluate_campaign(
    selected: list[
        dict[
            str,
            float,
        ]
    ],
) -> list[
    dict[
        str,
        Any,
    ]
]:

    waves = {
        (
            r[
                "a"
            ],
            r[
                "b"
            ],
        ):
            make_waveform(
                r
            )
        for r in selected
    }

    top: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for (
        kind,
        p1,
        p2,
        ncycle,
        beta,
        pot,
    ) in geometry_cases(
        selected
    ):

        wave = waves[
            (
                pot[
                    "a"
                ],
                pot[
                    "b"
                ],
            )
        ]

        point = evaluate_geometry(
            kind,
            p1,
            p2,
            ncycle,
            beta,
            pot,
            wave,
            COARSE_N,
            None,
            "POINT_VIRIAL",
        )

        if (
            point.get(
                "valid"
            )
            and
            math.isfinite(
                point[
                    "C"
                ]
            )
        ):

            top.append(
                point
            )

        for tail in TAIL_LEVELS:

            for model in (
                "LOC_GUIDE_NEUTRAL",
                "FULL_NEUTRAL",
                "FULL_MASSLIKE",
            ):

                r = evaluate_geometry(
                    kind,
                    p1,
                    p2,
                    ncycle,
                    beta,
                    pot,
                    wave,
                    COARSE_N,
                    tail,
                    model,
                )

                if (
                    r.get(
                        "valid"
                    )
                    and
                    math.isfinite(
                        r[
                            "C"
                        ]
                    )
                ):

                    top.append(
                        r
                    )

    top.sort(
        key=row_key
    )

    keep = top[
        :TOP_KEEP
    ]

    for model in (
        "POINT_VIRIAL",
        "LOC_GUIDE_NEUTRAL",
        "FULL_NEUTRAL",
        "FULL_MASSLIKE",
    ):

        model_rows = [
            r
            for r in top
            if
            r[
                "model"
            ]
            ==
            model
        ]

        keep.extend(
            model_rows[
                :TOP_KEEP
            ]
        )

    unique: dict[
        tuple[
            Any,
            ...,
        ],
        dict[
            str,
            Any,
        ],
    ] = {}

    for r in keep:

        k = (
            r[
                "kind"
            ],
            round(
                r[
                    "p1"
                ],
                10,
            ),
            round(
                r[
                    "p2"
                ],
                10,
            ),
            r[
                "ncycle"
            ],
            round(
                r[
                    "beta"
                ],
                10,
            ),
            round(
                r[
                    "pot_a"
                ],
                10,
            ),
            round(
                r[
                    "pot_b"
                ],
                10,
            ),
            r[
                "tail_n"
            ],
            r[
                "model"
            ],
        )

        unique[
            k
        ] = r

    rows = list(
        unique.values()
    )

    rows.sort(
        key=row_key
    )

    return rows


def refine(
    row: dict[
        str,
        Any,
    ],
    n: int,
    phase_delta: float = 0.0,
) -> dict[
    str,
    Any,
]:

    pot = potential_metrics(
        row[
            "pot_a"
        ],
        row[
            "pot_b"
        ],
    )

    if (
        row[
            "pot_a"
        ]
        ==
        0.0
        and
        row[
            "pot_b"
        ]
        ==
        0.0
    ):

        pot = harmonic_exact()

    if (
        pot
        is None
    ):

        raise RuntimeError(
            "selected potential failed reconstruction"
        )

    wave = make_waveform(
        pot
    )

    return evaluate_geometry(
        row[
            "kind"
        ],
        row[
            "p1"
        ],
        row[
            "p2"
        ],
        row[
            "ncycle"
        ],
        row[
            "beta"
        ],
        pot,
        wave,
        n,
        row[
            "tail_n"
        ],
        row[
            "model"
        ],
        phase_delta=phase_delta,
    )


def relerr(
    a: float,
    b: float,
) -> float:

    return (
        abs(
            a
            -
            b
        )
        /
        max(
            abs(
                a
            ),
            abs(
                b
            ),
            1e-300,
        )
    )


def best_of(
    rows: list[
        dict[
            str,
            Any,
        ]
    ],
    model: str,
) -> dict[
    str,
    Any,
] | None:

    cand = [
        r
        for r in rows
        if
        r[
            "model"
        ]
        ==
        model
        and
        math.isfinite(
            r[
                "C"
            ]
        )
    ]

    return (
        min(
            cand,
            key=row_key,
        )
        if
        cand
        else
        None
    )


def write_csv(
    path: Path,
    rows: list[
        dict[
            str,
            Any,
        ]
    ],
) -> None:

    if not rows:

        path.write_text(
            ""
        )

        return

    keys: list[
        str
    ] = []

    seen: set[
        str
    ] = set()

    for r in rows:

        for k in r:

            if (
                k
                not in
                seen
            ):

                seen.add(
                    k
                )

                keys.append(
                    k
                )

    with path.open(
        "w",
        newline="",
    ) as f:

        w = csv.DictWriter(
            f,
            fieldnames=keys,
        )

        w.writeheader()

        for r in rows:

            w.writerow(
                r
            )


def main(
) -> None:

    (
        b7_fraction,
        b7_source,
    ) = read_b7_fraction()

    harm = harmonic_exact()

    print(
        "=== 027A CANONICAL-SCALAR STRESS-CYCLE BRIDGE ==="
    )

    print(
        f"C_006D={C_006D:.15e}"
    )

    print(
        f"C_024D_SCALAR={C_024D_SCALAR:.15e}"
    )

    print(
        f"B7_NEGATIVE_ACTIVE_FRACTION={b7_fraction:.15e}"
    )

    print(
        f"B7_FRACTION_SOURCE={b7_source}"
    )

    print(
        "CANONICAL_ENDPOINT_S_OVER_RHO_MIN=-2"
    )

    print(
        "CANONICAL_ENDPOINT_S_OVER_RHO_MAX=+4"
    )

    print(
        "HARMONIC_NEGATIVE_DUTY="
        f"{harm['negative_duty']:.15e}"
    )

    print(
        "HARMONIC_PARTICIPATION_MULTIPLIER_VS_B7="
        f"{harm['negative_duty']/b7_fraction:.15e}"
    )

    print(
        "HARMONIC_GROSS_NEGATIVE_Q="
        f"{harm['gross_negative_q']:.15e}"
    )

    print(
        "HARMONIC_IDEAL_KERNEL_RATIO_THRESHOLD="
        f"{harm['ideal_kernel_ratio_threshold']:.15e}"
    )

    print(
        "HARMONIC_IDEAL_SEPARATED_C="
        f"{harm['ideal_separated_C']:.15e}"
    )

    print(
        "PURE_CIRCULAR_CONSTANT_RADIUS_KERNEL_CONTROL="
        "RED_BY_IDENTITY"
    )

    print(
        "\n=== POTENTIAL-WAVEFORM FRONTIER ===",
        flush=True,
    )

    pots = scan_potentials()

    selected = select_potentials(
        pots
    )

    print(
        f"POTENTIAL_CASES_VALID={len(pots)}"
    )

    print(
        "POTENTIALS_SELECTED_FOR_GEOMETRY="
        f"{len(selected)}"
    )

    for (
        i,
        p,
    ) in enumerate(
        pots[
            :10
        ]
    ):

        print(
            f"POT_RANK={i+1} "
            f"A={p['a']:.8f} "
            f"B={p['b']:.8f} "
            f"CHI={p['chi_omega_over_m']:.8f} "
            f"QNEG={p['gross_negative_q']:.8f} "
            f"NEG_DUTY={p['negative_duty']:.8f} "
            f"QBAR={p['qbar_mobile']:.8f} "
            f"ECOMP={p['minimal_compensation_energy']:.8f} "
            f"RCRIT={p['ideal_kernel_ratio_threshold']:.8f} "
            f"CSEP={p['ideal_separated_C']:.8f}"
        )

    write_csv(
        OUT_POT,
        pots,
    )

    print(
        "\n=== TRUE-STANDOFF GEOMETRY CAMPAIGN ===",
        flush=True,
    )

    coarse = evaluate_campaign(
        selected
    )

    print(
        f"COARSE_TOP_ROWS={len(coarse)}"
    )

    refinement_seed: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for model in (
        "POINT_VIRIAL",
        "LOC_GUIDE_NEUTRAL",
        "FULL_NEUTRAL",
        "FULL_MASSLIKE",
    ):

        mr = [
            r
            for r in coarse
            if
            r[
                "model"
            ]
            ==
            model
        ]

        refinement_seed.extend(
            mr[
                :12
            ]
        )

    refined: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for r in refinement_seed:

        rr = refine(
            r,
            MEDIUM_N,
        )

        if (
            rr.get(
                "valid"
            )
            and
            math.isfinite(
                rr[
                    "C"
                ]
            )
        ):

            refined.append(
                rr
            )

    refined.sort(
        key=row_key
    )

    high: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for model in (
        "POINT_VIRIAL",
        "LOC_GUIDE_NEUTRAL",
        "FULL_NEUTRAL",
        "FULL_MASSLIKE",
    ):

        mr = [
            r
            for r in refined
            if
            r[
                "model"
            ]
            ==
            model
        ]

        for r in mr[
            :4
        ]:

            hh = refine(
                r,
                HIGH_N,
            )

            if (
                hh.get(
                    "valid"
                )
                and
                math.isfinite(
                    hh[
                        "C"
                    ]
                )
            ):

                high.append(
                    hh
                )

    high.sort(
        key=row_key
    )

    all_out = (
        coarse
        +
        refined
        +
        high
    )

    all_out.sort(
        key=row_key
    )

    write_csv(
        OUT_GEO,
        all_out[
            :400
        ],
    )

    ranking_pool = (
        high
        or
        refined
        or
        coarse
    )

    point_best = best_of(
        ranking_pool,
        "POINT_VIRIAL",
    )

    finite_best = best_of(
        ranking_pool,
        "FULL_NEUTRAL",
    )

    masslike_best = best_of(
        ranking_pool,
        "FULL_MASSLIKE",
    )

    def print_best(
        name: str,
        row: dict[
            str,
            Any,
        ] | None,
    ) -> None:

        if (
            row
            is None
        ):

            print(
                f"{name}=NONE"
            )

            return

        print(
            f"{name}="
            f"C:{row['C']:.12e} "
            f"A:{row['A_out']:.12e} "
            f"K_RATIO:{row['K_ratio']:.8f} "
            f"NEG_PART:{row['negative_active_participation']:.8f} "
            f"CORE:{row['core_radius']:.8f} "
            f"TUBE_CURV:{row['tube_curvature']:.8f} "
            f"KIND:{row['kind']} "
            f"NCYCLE:{row['ncycle']} "
            f"BETA:{row['beta']:.6f} "
            f"CHI:{row['chi']:.6f} "
            f"A_POT:{row['pot_a']:.6f} "
            f"B_POT:{row['pot_b']:.6f}"
        )

    print(
        "\n=== BEST SURVIVORS ==="
    )

    print_best(
        "BEST_POINT",
        point_best,
    )

    print_best(
        "BEST_FINITE_FULL_NEUTRAL",
        finite_best,
    )

    print_best(
        "BEST_FINITE_FULL_MASSLIKE",
        masslike_best,
    )

    audit: dict[
        str,
        Any,
    ] = {}

    strict = (
        finite_best
    )

    if (
        strict
        is not None
    ):

        medium = refine(
            strict,
            MEDIUM_N,
        )

        highrow = refine(
            strict,
            HIGH_N,
        )

        independent = refine(
            strict,
            INDEPENDENT_N,
        )

        phase_rows = [
            refine(
                strict,
                HIGH_N,
                d,
            )
            for d in PHASE_JITTERS
        ]

        phase_rows = [
            r
            for r in phase_rows
            if
            r.get(
                "valid"
            )
        ]

        worst_phase_C = max(
            (
                r[
                    "C"
                ]
                for r in phase_rows
            ),
            default=math.inf,
        )

        audit = {
            "medium":
                medium,

            "high":
                highrow,

            "independent":
                independent,

            "medium_high_C_relerr":
                relerr(
                    medium[
                        "C"
                    ],
                    highrow[
                        "C"
                    ],
                ),

            "high_independent_C_relerr":
                relerr(
                    highrow[
                        "C"
                    ],
                    independent[
                        "C"
                    ],
                ),

            "worst_phase_jitter_C":
                worst_phase_C,

            "phase_jitter_all_outward":
                all(
                    r[
                        "A_out"
                    ]
                    >
                    0.0
                    for r in phase_rows
                ),
        }

        print(
            "STRICT_MEDIUM_HIGH_C_RELERR="
            f"{audit['medium_high_C_relerr']:.15e}"
        )

        print(
            "STRICT_HIGH_INDEPENDENT_C_RELERR="
            f"{audit['high_independent_C_relerr']:.15e}"
        )

        print(
            "STRICT_WORST_PHASE_JITTER_C="
            f"{audit['worst_phase_jitter_C']:.15e}"
        )

        print(
            "STRICT_PHASE_JITTER_ALL_OUTWARD="
            +
            (
                "PASS"
                if
                audit[
                    "phase_jitter_all_outward"
                ]
                else
                "FAIL"
            )
        )

    wildcard_rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    wildcard_seed = (
        finite_best
        if
        finite_best
        is not None
        else
        point_best
    )

    if (
        wildcard_seed
        is not None
    ):

        for mult in WILDCARDS:

            r = dict(
                wildcard_seed
            )

            r[
                "p1"
            ] = (
                wildcard_seed[
                    "p1"
                ]
                *
                mult
            )

            wr = refine(
                r,
                MEDIUM_N,
            )

            if (
                wr.get(
                    "valid"
                )
            ):

                wr = dict(
                    wr
                )

                wr[
                    "blind_wildcard_scale_multiplier"
                ] = mult

                wr[
                    "used_for_selection"
                ] = False

                wildcard_rows.append(
                    wr
                )

                print(
                    f"WILDCARD_SCALE={mult:.6f} "
                    f"C={wr['C']:.12e} "
                    f"A={wr['A_out']:.12e}"
                )

    write_csv(
        OUT_WILD,
        wildcard_rows,
    )

    point_green = bool(
        point_best
        is not None
        and
        point_best[
            "C"
        ]
        <
        C_006D
    )

    finite_green = bool(
        finite_best
        is not None
        and
        finite_best[
            "C"
        ]
        <
        C_006D
        and
        finite_best[
            "tube_curvature"
        ]
        <=
        0.5
        and
        finite_best[
            "negative_active_participation"
        ]
        >
        b7_fraction
    )

    major_green = bool(
        finite_green
        and
        finite_best[
            "C"
        ]
        <
        C_024D_SCALAR
        and
        audit
        and
        audit[
            "medium_high_C_relerr"
        ]
        <=
        0.10
        and
        audit[
            "high_independent_C_relerr"
        ]
        <=
        0.03
        and
        audit[
            "phase_jitter_all_outward"
        ]
        and
        audit[
            "worst_phase_jitter_C"
        ]
        <
        C_006D
    )

    if (
        major_green
    ):

        decision = (
            "GREEN_MAJOR_SOURCE_ENGINE_PREFLIGHT_"
            "AUTHORIZE_027B_MICROSCOPIC_PDE"
        )

        next_step = (
            "027B_EXPLICIT_QUADRATIC_NEGATIVE_QUARTIC_"
            "POSITIVE_SEXTIC_LOCALIZED_FIELD_CYCLE"
        )

    elif (
        finite_green
    ):

        decision = (
            "YELLOW_FINITE_SOURCE_ENGINE_SURVIVOR_"
            "NEEDS_SUPPORT_AND_RADIATION_CLOSURE"
        )

        next_step = (
            "027A1_SUPPORT_REACTION_RADIATION_"
            "STRESS_TEST_BEFORE_PDE"
        )

    elif (
        point_green
    ):

        decision = (
            "YELLOW_POINT_SOURCE_RECTIFICATION_SURVIVES_"
            "BUT_LOCALIZATION_SUPPORT_OBSTRUCTS"
        )

        next_step = (
            "DIAGNOSE_LOCALIZATION_CURVATURE_OR_REPLACE_"
            "PHYSICAL_TRANSPORT_WITH_FIELD_STATE_SHUTTLE"
        )

    else:

        decision = (
            "RED_PHASE_LOCKED_CANONICAL_SCALAR_"
            "TRANSPORT_IN_TESTED_CLASS"
        )

        next_step = (
            "RERANK_SOURCE_ENGINE_DO_NOT_LAUNCH_027B_PDE"
        )

    summary = {
        "simulation":
            "027A",

        "branch":
            "TRUE_ANTIGRAVITY",

        "question":
            (
                "Can a conservative canonical-scalar stress cycle close most "
                "of the 026P participation gap and remain outward at true "
                "stand-off after finite localization, cycle-averaged Laue "
                "compensation and support proxies?"
            ),

        "analytic_bridge":
            {
                "S_over_rho_turning_point":
                    -2.0,

                "S_over_rho_kinetic_crossing":
                    4.0,

                "harmonic_negative_duty":
                    harm[
                        "negative_duty"
                    ],

                "harmonic_participation_multiplier_vs_B7":
                    (
                        harm[
                            "negative_duty"
                        ]
                        /
                        b7_fraction
                    ),

                "harmonic_gross_negative_q":
                    harm[
                        "gross_negative_q"
                    ],

                "harmonic_kernel_ratio_threshold":
                    harm[
                        "ideal_kernel_ratio_threshold"
                    ],

                "harmonic_ideal_separated_C":
                    harm[
                        "ideal_separated_C"
                    ],
            },

        "potential_scan":
            {
                "valid_count":
                    len(
                        pots
                    ),

                "selected_count":
                    len(
                        selected
                    ),

                "best":
                    pots[
                        0
                    ]
                    if
                    pots
                    else
                    None,
            },

        "best_point":
            point_best,

        "best_finite_full_neutral":
            finite_best,

        "best_finite_full_masslike":
            masslike_best,

        "refinement_audit":
            audit,

        "decision":
            decision,

        "next":
            next_step,

        "claims":
            {
                "microscopic_field_realization":
                    False,

                "full_dynamic_local_Tmunu_conservation":
                    False,

                "reaction_momentum_closed":
                    False,

                "radiation_lifetime_closed":
                    False,

                "full_stability":
                    False,

                "nonlinear_GR":
                    False,

                "removes_1_over_G_scaling":
                    False,

                "practical_antigravity_device":
                    False,

                "new_physics_discovery":
                    False,

                "90_percent_heuristic_authorized":
                    False,
            },

        "mandatory_parallel_credibility_branch":
            "026C_N89_FORCE_CONVERGENCE",
    }

    OUT_JSON.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        +
        "\n"
    )

    print(
        "\n=== 027A DECISION ==="
    )

    print(
        f"027A_DECISION={decision}"
    )

    print(
        f"NEXT={next_step}"
    )

    print(
        "026C_N89_STILL_REQUIRED=YES"
    )

    print(
        "MICROSCOPIC_FIELD_REALIZATION=NO"
    )

    print(
        "FULL_DYNAMIC_LOCAL_TMUNU_CONSERVATION=NO"
    )

    print(
        "REACTION_MOMENTUM_CLOSED=NO"
    )

    print(
        "RADIATION_LIFETIME_CLOSED=NO"
    )

    print(
        "FULL_STABILITY=NO"
    )

    print(
        "NONLINEAR_GR=NO"
    )

    print(
        "REMOVES_1_OVER_G_SCALING=NO"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "HEURISTIC_90_PERCENT_AUTHORIZED=NO"
    )

    print(
        f"SUMMARY_JSON={OUT_JSON}"
    )

    print(
        f"POTENTIAL_CSV={OUT_POT}"
    )

    print(
        f"GEOMETRY_CSV={OUT_GEO}"
    )

    print(
        f"WILDCARD_CSV={OUT_WILD}"
    )

    print(
        "027A_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":

    main()
