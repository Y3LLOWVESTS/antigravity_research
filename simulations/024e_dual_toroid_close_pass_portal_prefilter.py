#!/usr/bin/env python3
"""024E dual-toroid non-colliding close-pass stress prefilter.

Question
--------
Can two distinct compact scalar-energy packets on side-by-side circular
tracks pass close to one another, without intersecting their centerlines,
and produce enough interaction stress through overlapping field support
to generate useful full-cycle outward gravity?

This is NOT an energy-collider model.

The two packet centers remain on distinct tracks. Only their field
distributions overlap near the common central throat.

All four circulation assignments are tested:

    left CCW, right CW
    left CW,  right CCW
    left CCW, right CCW
    left CW,  right CW

For the side-by-side geometry:

    opposite named circulation directions
        -> approximately parallel velocities at the throat

    same named circulation directions
        -> approximately antiparallel velocities at the throat.

Both global reversals must agree for the parity-even interaction tested here.

Minimal nonlinear field interaction
-----------------------------------
Use two distinct canonical complex scalar species:

    Phi
    Chi

with potential:

    V =
        m^2 |Phi|^2
        +
        m^2 |Chi|^2
        +
        g |Phi|^2 |Chi|^2.

The portal term is:

    V_int = g |Phi|^2 |Chi|^2 >= 0.

For a potential-dominated interaction term:

    rho_int = +V_int

    p_x,int = p_y,int = p_z,int = -V_int

and therefore:

    S_int
      =
    rho_int + p_x,int + p_y,int + p_z,int
      =
    -2 V_int.

Thus overlapping field support can create the desired negative active
stress without packet-center collision.

Linear-control results
----------------------
Pure linear Maxwell overlap is not promoted because the Maxwell stress
tensor is traceless and:

    S_EM = 2 rho_EM > 0.

Likewise a free harmonic canonical scalar field does not acquire a
negative cycle-averaged active source merely by coherent linear overlap.

A nonlinear potential interaction is therefore required.

Compact packet profile
----------------------
Each species uses:

    F(r)
      =
    A (1-r^2/a^2)^2
        for r < a,

    F(r)
      =
    0
        for r >= a.

The profile has finite support.

Track geometry
--------------
Payload:

    (0,0,h)

with:

    h = 1.

The packet tracks lie in:

    z_track = -(a + clearance).

Thus the complete compact packet support obeys:

    z <= -clearance <= 0.

Two ring centers are:

    x_left  = -(R+d0/2)

    x_right = +(R+d0/2).

Each has radius R.

Their closest track-center separation is:

    d0 > 0.

Therefore the tracks never geometrically intersect.

Primary promotion requires:

    d_min/a >= 0.5.

The field supports are allowed to overlap.

That is the interaction being tested and is not treated as a particle
collision.

Packet energy normalization
---------------------------
Each packet is normalized to unit rest energy from:

    internal frequency energy,
    mass energy,
    localization gradient energy.

The portal energy is then calculated from the actual normalized field
profiles rather than assigned manually.

Guide / confinement ledger
--------------------------
Circular packet motion requires centripetal guide stress.

Use the favorable inherited effective DEC support floor:

    E_guide,floor
      =
    E_mobile beta^2.

Scan an engineering multiplier:

    1 <= M_guide <= 3.

The minimum floor is treated as active-neutral in this optimistic
prefilter.

Additional guide energy above the floor is counted as ordinary
positive active energy.

Full-cycle compensation
-----------------------
A transient negative stress pulse is insufficient.

For the portal interaction define:

    B
      =
    2 <U_int>.

The full-cycle positive trace compensation is tested in three ways.

LOCAL REACTION

    The compensation occurs at the same interaction kernel.

    This has zero kernel leverage and is an exact control.

UNIFORM GUIDE REACTION

    The compensation is distributed over the complete two-ring guide.

OUTER ARC REACTION

    The compensation is optimistically routed through the outer
    quarter-arcs of the rings, which have lower payload kernel.

The outer-arc result is NOT automatically a microscopic field result.

It is a bound on what stress routing could achieve.

Exact coupling solution
-----------------------
For fixed packet profiles:

    U_int proportional to g.

Instead of randomly guessing g, solve analytically for:

    g_positive

    g_required_to_beat_006D

    g_required_to_beat_024D1R

    g_required_to_beat_024D.

The primary admissible coupling is capped by:

    g <= 4 pi

and by the condition:

    U_int,max / E_mobile <= 0.25.

This makes a RED result much more decisive than a finite random coupling
scan.

Observable
----------
Primary:

    full-cycle mean axial outward response

and:

    C
      =
    E_inventory / A_out.

Compare with:

    C_006D
      =
    23.591586299249

    C_024D1R
      =
    19.04617786197023

    C_024D relaxed scalar
      =
    6.610457607426174.

Claim class
-----------
PROJECT_DERIVED_DUAL_TOROID_NONCOLLIDING_CLOSE_PASS_PORTAL_PREFILTER

Does not establish
------------------
- a self-bound packet;
- a microscopic guide field;
- complete local dynamic T_munu conservation;
- nonlinear GR;
- stability;
- gravitational radiation emission;
- favorable 1/G scaling;
- a practical antigravity device.
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results/data"

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

OUTJ = (
    DATA
    / "024e_dual_toroid_close_pass_portal_summary.json"
)

OUTC = (
    DATA
    / "024e_dual_toroid_close_pass_portal_top.csv"
)

OUTD = (
    DATA
    / "024e_dual_toroid_close_pass_direction_summary.csv"
)

OUTN = (
    DATA
    / "024e_dual_toroid_close_pass_best_profile.npz"
)


C006D = 23.591586299249
C024D1R = 19.04617786197023
C024D = 6.610457607426174

GMAX = (
    4.0
    * math.pi
)

DISTORT = 0.25

SMOKE = (
    os.environ.get(
        "AG_SMOKE",
        "0",
    )
    ==
    "1"
)

POW = (
    10
    if SMOKE
    else 19
)

N = (
    2 ** POW
)

NP = (
    96
    if SMOKE
    else 320
)

NMED = (
    512
    if SMOKE
    else 4096
)

NHIGH = (
    1024
    if SMOKE
    else 16384
)

NIND = (
    2048
    if SMOKE
    else 65536
)

BATCH = (
    128
    if SMOKE
    else 768
)

TOP = (
    30
    if SMOKE
    else 100
)


MODES = (
    (
        "L_CCW_R_CW",
        +1.0,
        -1.0,
        +1.0,
        "PARALLEL_AT_THROAT",
    ),
    (
        "L_CW_R_CCW",
        -1.0,
        +1.0,
        -1.0,
        "PARALLEL_AT_THROAT_REVERSED",
    ),
    (
        "L_CCW_R_CCW",
        +1.0,
        +1.0,
        +1.0,
        "ANTIPARALLEL_AT_THROAT",
    ),
    (
        "L_CW_R_CW",
        -1.0,
        -1.0,
        -1.0,
        "ANTIPARALLEL_AT_THROAT_REVERSED",
    ),
)


def wrap(
    x: np.ndarray,
) -> np.ndarray:
    """Wrap angle to [-pi,pi)."""

    return (
        (
            x
            +
            math.pi
        )
        %
        (
            2.0
            * math.pi
        )
        -
        math.pi
    )


def profile_table():
    """Construct compact-profile integrals and overlap lookup."""

    xg, wg = leggauss(
        180
    )

    x = (
        0.5
        * (
            xg
            +
            1.0
        )
    )

    w = (
        0.5
        * wg
    )

    b = (
        1.0
        -
        x
        * x
    ) ** 2

    db = (
        -4.0
        * x
        * (
            1.0
            -
            x
            * x
        )
    )

    c2 = float(
        4.0
        * math.pi
        * np.sum(
            w
            * x
            * x
            * b
            * b
        )
    )

    cg = float(
        4.0
        * math.pi
        * np.sum(
            w
            * x
            * x
            * db
            * db
        )
    )

    nsep = (
        260
        if SMOKE
        else 420
    )

    sg = np.linspace(
        0.0,
        2.0,
        nsep,
    )

    ov = np.zeros_like(
        sg
    )

    gx, gw = leggauss(
        56
        if SMOKE
        else 88
    )

    gr, grw = leggauss(
        56
        if SMOKE
        else 88
    )

    for i, s in enumerate(
        sg
    ):

        if s >= 2.0:
            continue

        lo = (
            -1.0
            +
            s
            / 2.0
        )

        hi = (
            1.0
            -
            s
            / 2.0
        )

        xx = (
            0.5
            * (
                hi
                -
                lo
            )
            * gx
            +
            0.5
            * (
                hi
                +
                lo
            )
        )

        wx = (
            0.5
            * (
                hi
                -
                lo
            )
            * gw
        )

        total = 0.0

        for xv, wv in zip(
            xx,
            wx,
        ):

            a1 = (
                xv
                +
                s
                / 2.0
            ) ** 2

            a2 = (
                xv
                -
                s
                / 2.0
            ) ** 2

            r2 = max(
                0.0,
                min(
                    1.0
                    -
                    a1,
                    1.0
                    -
                    a2,
                ),
            )

            if r2 <= 0.0:
                continue

            rm = math.sqrt(
                r2
            )

            rr = (
                0.5
                * rm
                * (
                    gr
                    +
                    1.0
                )
            )

            wr = (
                0.5
                * rm
                * grw
            )

            r1 = (
                a1
                +
                rr
                * rr
            )

            r2v = (
                a2
                +
                rr
                * rr
            )

            total += (
                wv
                * float(
                    2.0
                    * math.pi
                    * np.sum(
                        wr
                        * rr
                        * np.maximum(
                            1.0
                            -
                            r1,
                            0.0,
                        ) ** 4
                        * np.maximum(
                            1.0
                            -
                            r2v,
                            0.0,
                        ) ** 4
                    )
                )
            )

        ov[
            i
        ] = total

    assert c2 > 0.0
    assert cg > 0.0
    assert ov[
        0
    ] > 0.0
    assert abs(
        ov[
            -1
        ]
    ) < 1.0e-12

    return (
        c2,
        cg,
        sg,
        ov,
    )


def build():
    """Build Sobol parameter population."""

    u = qmc.Sobol(
        d=9,
        scramble=True,
        seed=240500,
    ).random_base2(
        POW
    )

    R = 10.0 ** (
        math.log10(
            0.25
        )
        +
        (
            math.log10(
                5.0
            )
            -
            math.log10(
                0.25
            )
        )
        * u[
            :,
            0
        ]
    )

    a = 10.0 ** (
        math.log10(
            0.02
        )
        +
        (
            math.log10(
                0.32
            )
            -
            math.log10(
                0.02
            )
        )
        * u[
            :,
            1
        ]
    )

    clear = (
        0.45
        * u[
            :,
            2
        ]
    )

    sr = (
        0.50
        +
        1.45
        * u[
            :,
            3
        ]
    )

    d0 = (
        a
        * sr
    )

    beta = (
        0.02
        +
        0.93
        * u[
            :,
            4
        ]
    )

    m = 10.0 ** (
        math.log10(
            0.5
        )
        +
        (
            math.log10(
                20.0
            )
            -
            math.log10(
                0.5
            )
        )
        * u[
            :,
            5
        ]
    )

    om = (
        1.0
        +
        1.5
        * u[
            :,
            6
        ]
    )

    lag = (
        -0.45
        +
        0.90
        * u[
            :,
            7
        ]
    )

    gm = (
        1.0
        +
        2.0
        * u[
            :,
            8
        ]
    )

    return {
        "R":
            R,

        "a":
            a,

        "clear":
            clear,

        "sr":
            sr,

        "d0":
            d0,

        "beta":
            beta,

        "m":
            m,

        "om":
            om,

        "omega":
            m
            * om,

        "lag":
            lag,

        "gm":
            gm,
    }


def micro(
    c2,
    cg,
    p,
):
    """Normalize compact scalar packets."""

    a = p[
        "a"
    ]

    m = p[
        "m"
    ]

    o = p[
        "omega"
    ]

    b = p[
        "beta"
    ]

    A2 = (
        1.0
        /
        (
            a ** 3
            * c2
            * (
                o
                * o
                +
                m
                * m
            )
            +
            a
            * cg
        )
    )

    srest = (
        A2
        * a ** 3
        * c2
        * (
            4.0
            * o
            * o
            -
            2.0
            * m
            * m
        )
    )

    gam = (
        1.0
        /
        np.sqrt(
            1.0
            -
            b
            * b
        )
    )

    Em = (
        2.0
        * gam
    )

    Eg0 = (
        Em
        * b
        * b
    )

    Eg = (
        Eg0
        * p[
            "gm"
        ]
    )

    return {
        "A2":
            A2,

        "srest":
            srest,

        "gam":
            gam,

        "Em":
            Em,

        "Eg0":
            Eg0,

        "Eg":
            Eg,

        "Eextra":
            Eg
            -
            Eg0,
    }


def ring_k(
    R,
    d0,
    z,
    n,
):
    """Mean and outer-arc gravitational kernels."""

    ph = np.linspace(
        0.0,
        2.0
        * math.pi,
        n,
        endpoint=False,
    )[
        None,
        :
    ]

    R = R[
        :,
        None
    ]

    d0 = d0[
        :,
        None
    ]

    z = z[
        :,
        None
    ]

    cc = (
        R
        +
        d0
        / 2.0
    )

    dz = (
        1.0
        -
        z
    )

    xl = (
        -cc
        +
        R
        * np.cos(
            ph
        )
    )

    yl = (
        R
        * np.sin(
            ph
        )
    )

    xr = (
        cc
        +
        R
        * np.cos(
            ph
        )
    )

    yr = (
        R
        * np.sin(
            ph
        )
    )

    kl = (
        dz
        /
        (
            xl
            * xl
            +
            yl
            * yl
            +
            dz
            * dz
        ) ** 1.5
    )

    kr = (
        dz
        /
        (
            xr
            * xr
            +
            yr
            * yr
            +
            dz
            * dz
        ) ** 1.5
    )

    km = (
        0.5
        * (
            kl.mean(
                1
            )
            +
            kr.mean(
                1
            )
        )
    )

    ml = (
        np.abs(
            wrap(
                ph
                -
                math.pi
            )
        )
        <=
        math.pi
        / 4.0
    )

    mr = (
        np.abs(
            wrap(
                ph
            )
        )
        <=
        math.pi
        / 4.0
    )

    ko = (
        0.5
        * (
            (
                kl
                * ml
            ).sum(
                1
            )
            /
            ml.sum(
                1
            )
            +
            (
                kr
                * mr
            ).sum(
                1
            )
            /
            mr.sum(
                1
            )
        )
    )

    return (
        km,
        ko,
    )


def req_g(
    E0,
    base,
    gain,
    u1,
    target=None,
):
    """Exact coupling needed for response or target coefficient."""

    if target is None:

        return np.divide(
            base,
            gain,
            out=np.full_like(
                base,
                np.inf,
            ),
            where=(
                gain
                >
                0.0
            ),
        )

    den = (
        target
        * gain
        -
        u1
    )

    num = (
        E0
        +
        target
        * base
    )

    return np.divide(
        num,
        den,
        out=np.full_like(
            base,
            np.inf,
        ),
        where=(
            den
            >
            0.0
        ),
    )


def eval_mode(
    c2,
    cg,
    sg,
    ov,
    p,
    mi,
    mode,
    n,
):
    """Evaluate one circulation-direction assignment."""

    name, sL, sR, ls, klass = mode

    al = np.linspace(
        0.0,
        2.0
        * math.pi,
        n,
        endpoint=False,
    )[
        None,
        :
    ]

    R = p[
        "R"
    ][
        :,
        None
    ]

    a = p[
        "a"
    ][
        :,
        None
    ]

    d0 = p[
        "d0"
    ][
        :,
        None
    ]

    z0 = (
        -(
            p[
                "a"
            ]
            +
            p[
                "clear"
            ]
        )
    )

    z = z0[
        :,
        None
    ]

    cc = (
        R
        +
        d0
        / 2.0
    )

    lag = (
        ls
        * p[
            "lag"
        ]
    )[
        :,
        None
    ]

    tL = (
        sL
        * al
    )

    tR = (
        math.pi
        +
        sR
        * al
        +
        lag
    )

    xL = (
        -cc
        +
        R
        * np.cos(
            tL
        )
    )

    yL = (
        R
        * np.sin(
            tL
        )
    )

    xR = (
        cc
        +
        R
        * np.cos(
            tR
        )
    )

    yR = (
        R
        * np.sin(
            tR
        )
    )

    sep = np.sqrt(
        (
            xR
            -
            xL
        ) ** 2
        +
        (
            yR
            -
            yL
        ) ** 2
    )

    q = (
        sep
        /
        a
    )

    coef = np.interp(
        np.clip(
            q,
            0.0,
            2.0,
        ),
        sg,
        ov,
    )

    coef = np.where(
        q
        <
        2.0,
        coef,
        0.0,
    )

    U1 = (
        mi[
            "A2"
        ][
            :,
            None
        ] ** 2
        * p[
            "a"
        ][
            :,
            None
        ] ** 3
        * coef
    )

    xm = (
        0.5
        * (
            xL
            +
            xR
        )
    )

    ym = (
        0.5
        * (
            yL
            +
            yR
        )
    )

    dz = (
        1.0
        -
        z
    )

    Ki = (
        dz
        /
        (
            xm
            * xm
            +
            ym
            * ym
            +
            dz
            * dz
        ) ** 1.5
    )

    Kg, Ko = ring_k(
        p[
            "R"
        ],
        p[
            "d0"
        ],
        z0,
        n,
    )

    ua = U1.mean(
        1
    )

    u1 = U1.max(
        1
    )

    uk = (
        U1
        * Ki
    ).mean(
        1
    )

    KU = np.divide(
        uk,
        ua,
        out=np.zeros_like(
            ua
        ),
        where=(
            ua
            >
            0.0
        ),
    )

    B1 = (
        2.0
        * ua
    )

    Gu1 = (
        B1
        * np.maximum(
            KU
            -
            Kg,
            0.0,
        )
    )

    Go1 = (
        B1
        * np.maximum(
            KU
            -
            Ko,
            0.0,
        )
    )

    base = (
        mi[
            "Em"
        ]
        * np.maximum(
            1.0,
            mi[
                "srest"
            ],
        )
        * Kg
        +
        mi[
            "Eextra"
        ]
        * Kg
    )

    E0 = (
        mi[
            "Em"
        ]
        +
        mi[
            "Eg"
        ]
    )

    gdist = np.divide(
        DISTORT
        * mi[
            "Em"
        ],
        u1,
        out=np.full_like(
            u1,
            np.inf,
        ),
        where=(
            u1
            >
            0.0
        ),
    )

    gcap = np.minimum(
        GMAX,
        gdist,
    )

    U = (
        gcap
        * u1
    )

    E = (
        E0
        +
        U
    )

    Gu = (
        gcap
        * Gu1
    )

    Go = (
        gcap
        * Go1
    )

    Au = (
        -base
        +
        Gu
    )

    Ao = (
        -base
        +
        Go
    )

    Cu = np.where(
        Au
        >
        0.0,
        E
        /
        Au,
        np.inf,
    )

    Co = np.where(
        Ao
        >
        0.0,
        E
        /
        Ao,
        np.inf,
    )

    gp = req_g(
        E0,
        base,
        Go1,
        u1,
    )

    g6 = req_g(
        E0,
        base,
        Go1,
        u1,
        C006D,
    )

    gu6 = req_g(
        E0,
        base,
        Gu1,
        u1,
        C006D,
    )

    g19 = req_g(
        E0,
        base,
        Go1,
        u1,
        C024D1R,
    )

    g66 = req_g(
        E0,
        base,
        Go1,
        u1,
        C024D,
    )

    mu = np.divide(
        base
        +
        E
        /
        C006D,
        Go,
        out=np.full_like(
            base,
            np.inf,
        ),
        where=(
            Go
            >
            0.0
        ),
    )

    minq = q.min(
        1
    )

    strict = (
        (
            minq
            >=
            0.5
            -
            1.0e-10
        )
        &
        (
            p[
                "clear"
            ]
            >=
            0.0
        )
        &
        (
            U
            /
            mi[
                "Em"
            ]
            <=
            DISTORT
            +
            1.0e-12
        )
    )

    duty = (
        U1
        >=
        0.1
        * np.maximum(
            u1[
                :,
                None
            ],
            1.0e-300,
        )
    ).mean(
        1
    )

    return {
        "name":
            name,

        "klass":
            klass,

        "Kg":
            Kg,

        "Ko":
            Ko,

        "KU":
            KU,

        "u1":
            u1,

        "ua":
            ua,

        "gcap":
            gcap,

        "E":
            E,

        "base":
            base,

        "Gu1":
            Gu1,

        "Go1":
            Go1,

        "Cu":
            Cu,

        "Co":
            Co,

        "gp":
            gp,

        "g6":
            g6,

        "gu6":
            gu6,

        "g19":
            g19,

        "g66":
            g66,

        "mu":
            mu,

        "minq":
            minq,

        "frac":
            U
            /
            mi[
                "Em"
            ],

        "duty":
            duty,

        "strict":
            strict,
    }


def sub(
    d,
    sl,
):
    """Slice a parameter dict."""

    return {
        k:
            v[
                sl
            ]
        for k, v in d.items()
    }


def rec(
    idx,
    j,
    p,
    mi,
    r,
    mode,
):
    """Serialize one candidate."""

    out = {
        "index":
            int(
                idx
            ),

        "direction":
            mode[
                0
            ],

        "throat_class":
            mode[
                4
            ],
    }

    for k in (
        "R",
        "a",
        "clear",
        "sr",
        "d0",
        "beta",
        "m",
        "om",
        "omega",
        "lag",
        "gm",
    ):

        out[
            k
        ] = float(
            p[
                k
            ][
                j
            ]
        )

    for k in (
        "A2",
        "srest",
        "gam",
        "Em",
        "Eg0",
        "Eg",
        "Eextra",
    ):

        out[
            k
        ] = float(
            mi[
                k
            ][
                j
            ]
        )

    for k in (
        "Kg",
        "Ko",
        "KU",
        "u1",
        "ua",
        "gcap",
        "E",
        "base",
        "Gu1",
        "Go1",
        "Cu",
        "Co",
        "gp",
        "g6",
        "gu6",
        "g19",
        "g66",
        "mu",
        "minq",
        "frac",
        "duty",
    ):

        out[
            k
        ] = float(
            r[
                k
            ][
                j
            ]
        )

    out[
        "strict"
    ] = bool(
        r[
            "strict"
        ][
            j
        ]
    )

    return out


def keep(
    pool,
    rows,
    key,
    n=TOP,
):
    """Keep smallest finite candidate values."""

    pool.extend(
        rows
    )

    pool[
        :
    ] = [
        x
        for x in pool
        if math.isfinite(
            x[
                key
            ]
        )
    ]

    pool.sort(
        key=lambda x:
            x[
                key
            ]
    )

    del pool[
        n:
    ]


def single(
    c2,
    cg,
    sg,
    ov,
    x,
    n,
):
    """Reconstruct one candidate at higher phase resolution."""

    p = {
        k:
            np.array(
                [
                    x[
                        k
                    ]
                ],
                float,
            )
        for k in (
            "R",
            "a",
            "clear",
            "sr",
            "d0",
            "beta",
            "m",
            "om",
            "omega",
            "lag",
            "gm",
        )
    }

    mi = micro(
        c2,
        cg,
        p,
    )

    mode = next(
        m
        for m in MODES
        if (
            m[
                0
            ]
            ==
            x[
                "direction"
            ]
        )
    )

    r = eval_mode(
        c2,
        cg,
        sg,
        ov,
        p,
        mi,
        mode,
        n,
    )

    y = rec(
        x[
            "index"
        ],
        0,
        p,
        mi,
        r,
        mode,
    )

    y[
        "nphase"
    ] = n

    return y


def symmetry(
    c2,
    cg,
    sg,
    ov,
):
    """Time-reversal direction regression."""

    p = {
        "R":
            np.array(
                [
                    1.1
                ]
            ),

        "a":
            np.array(
                [
                    0.14
                ]
            ),

        "clear":
            np.array(
                [
                    0.05
                ]
            ),

        "sr":
            np.array(
                [
                    1.1
                ]
            ),

        "d0":
            np.array(
                [
                    0.154
                ]
            ),

        "beta":
            np.array(
                [
                    0.22
                ]
            ),

        "m":
            np.array(
                [
                    3.0
                ]
            ),

        "om":
            np.array(
                [
                    1.15
                ]
            ),

        "omega":
            np.array(
                [
                    3.45
                ]
            ),

        "lag":
            np.array(
                [
                    0.18
                ]
            ),

        "gm":
            np.array(
                [
                    1.3
                ]
            ),
    }

    mi = micro(
        c2,
        cg,
        p,
    )

    vals = {}

    for m in MODES:

        vals[
            m[
                0
            ]
        ] = float(
            eval_mode(
                c2,
                cg,
                sg,
                ov,
                p,
                mi,
                m,
                (
                    1024
                    if SMOKE
                    else 4096
                ),
            )[
                "ua"
            ][
                0
            ]
        )

    ep = (
        abs(
            vals[
                "L_CCW_R_CW"
            ]
            -
            vals[
                "L_CW_R_CCW"
            ]
        )
        /
        max(
            abs(
                vals[
                    "L_CCW_R_CW"
                ]
            ),
            1.0e-300,
        )
    )

    ea = (
        abs(
            vals[
                "L_CCW_R_CCW"
            ]
            -
            vals[
                "L_CW_R_CW"
            ]
        )
        /
        max(
            abs(
                vals[
                    "L_CCW_R_CCW"
                ]
            ),
            1.0e-300,
        )
    )

    if (
        ep
        >
        2.0e-3
        or
        ea
        >
        2.0e-3
    ):

        raise RuntimeError(
            "direction reversal failed "
            f"{ep=} {ea=}"
        )

    return (
        vals,
        ep,
        ea,
    )


def main():
    """Execute campaign."""

    print(
        "=== 024E DUAL-TOROID NONCOLLIDING CLOSE-PASS STRESS PREFILTER ==="
    )

    print(
        f"C_006D="
        f"{C006D:.15f}"
    )

    print(
        f"C_024D1R="
        f"{C024D1R:.15f}"
    )

    print(
        f"C_024D_SCALAR="
        f"{C024D:.15f}"
    )

    print(
        "ENERGY_COLLIDER_MODEL=NO"
    )

    print(
        "CENTERLINE_COLLISION=NO"
    )

    print(
        "FIELD_OVERLAP_INTERACTION=YES"
    )

    print(
        "PORTAL=G_ABS_PHI2_ABS_CHI2"
    )

    print(
        "PORTAL_ACTIVE_SOURCE="
        "S_INT_EQUALS_MINUS_2_V_INT"
    )

    print(
        "PURE_LINEAR_MAXWELL_CLOSE_PASS_NEGATIVE_ACTIVE=NO"
    )

    print(
        "FREE_HARMONIC_SCALAR_CYCLE_AVG_NEGATIVE_ACTIVE=NO"
    )

    c2, cg, sg, ov = profile_table()

    print(
        f"PROFILE_C2="
        f"{c2:.12e} "
        f"PROFILE_CGRAD="
        f"{cg:.12e}"
    )

    vals, ep, ea = symmetry(
        c2,
        cg,
        sg,
        ov,
    )

    print(
        f"PARALLEL_REVERSE_RELERR="
        f"{ep:.12e}"
    )

    print(
        f"ANTIPARALLEL_REVERSE_RELERR="
        f"{ea:.12e}"
    )

    print(
        "DIRECTION_REVERSAL_SYMMETRY=PASS"
    )

    p0 = build()

    mi0 = micro(
        c2,
        cg,
        p0,
    )

    print(
        f"BASE_SOBOL_CASES="
        f"{N}"
    )

    print(
        f"TOTAL_DIRECTION_CASES="
        f"{4 * N}"
    )

    pools = {
        "Co":
            [],

        "Cu":
            [],

        "g6":
            [],
    }

    counts = {
        m[
            0
        ]: {
            "strict":
                0,

            "outer_pos":
                0,

            "outer_006d":
                0,

            "uniform_pos":
                0,

            "uniform_006d":
                0,

            "greq_pert":
                0,
        }
        for m in MODES
    }

    for st in range(
        0,
        N,
        BATCH,
    ):

        en = min(
            st
            +
            BATCH,
            N,
        )

        sl = slice(
            st,
            en,
        )

        p = sub(
            p0,
            sl,
        )

        mi = sub(
            mi0,
            sl,
        )

        if (
            st
            %
            (
                BATCH
                * 80
            )
            ==
            0
        ):

            print(
                f"SCAN_PROGRESS="
                f"{st}/{N}",
                flush=True,
            )

        for mode in MODES:

            r = eval_mode(
                c2,
                cg,
                sg,
                ov,
                p,
                mi,
                mode,
                NP,
            )

            s = r[
                "strict"
            ]

            c = counts[
                mode[
                    0
                ]
            ]

            c[
                "strict"
            ] += int(
                s.sum()
            )

            c[
                "outer_pos"
            ] += int(
                (
                    s
                    &
                    np.isfinite(
                        r[
                            "Co"
                        ]
                    )
                ).sum()
            )

            c[
                "outer_006d"
            ] += int(
                (
                    s
                    &
                    (
                        r[
                            "Co"
                        ]
                        <
                        C006D
                    )
                ).sum()
            )

            c[
                "uniform_pos"
            ] += int(
                (
                    s
                    &
                    np.isfinite(
                        r[
                            "Cu"
                        ]
                    )
                ).sum()
            )

            c[
                "uniform_006d"
            ] += int(
                (
                    s
                    &
                    (
                        r[
                            "Cu"
                        ]
                        <
                        C006D
                    )
                ).sum()
            )

            c[
                "greq_pert"
            ] += int(
                (
                    s
                    &
                    (
                        r[
                            "g6"
                        ]
                        <=
                        GMAX
                    )
                ).sum()
            )

            for key in (
                "Co",
                "Cu",
                "g6",
            ):

                ids = np.flatnonzero(
                    s
                    &
                    np.isfinite(
                        r[
                            key
                        ]
                    )
                )

                if len(
                    ids
                ) > 8:

                    ids = ids[
                        np.argpartition(
                            r[
                                key
                            ][
                                ids
                            ],
                            7,
                        )[
                            :8
                        ]
                    ]

                keep(
                    pools[
                        key
                    ],
                    [
                        rec(
                            st
                            +
                            int(
                                j
                            ),
                            int(
                                j
                            ),
                            p,
                            mi,
                            r,
                            mode,
                        )
                        for j in ids
                    ],
                    key,
                )

    print(
        "=== COARSE COUNTS ==="
    )

    for m in MODES:

        for k, v in counts[
            m[
                0
            ]
        ].items():

            print(
                f"{m[0]}_"
                f"{k.upper()}="
                f"{v}"
            )

    merged = {
        (
            x[
                "index"
            ],
            x[
                "direction"
            ],
        ):
            x
        for z in pools.values()
        for x in z
    }

    cand = list(
        merged.values()
    )

    print(
        f"REFINEMENT_CANDIDATES="
        f"{len(cand)}"
    )

    refined = []

    for i, x in enumerate(
        cand
    ):

        if (
            i
            %
            25
            ==
            0
        ):

            print(
                f"REFINEMENT_PROGRESS="
                f"{i}/{len(cand)}",
                flush=True,
            )

        med = single(
            c2,
            cg,
            sg,
            ov,
            x,
            NMED,
        )

        hi = single(
            c2,
            cg,
            sg,
            ov,
            x,
            NHIGH,
        )

        hi[
            "Co_med"
        ] = med[
            "Co"
        ]

        hi[
            "Cu_med"
        ] = med[
            "Cu"
        ]

        if (
            math.isfinite(
                hi[
                    "Co"
                ]
            )
            and
            math.isfinite(
                med[
                    "Co"
                ]
            )
        ):

            hi[
                "Co_rel"
            ] = (
                abs(
                    hi[
                        "Co"
                    ]
                    -
                    med[
                        "Co"
                    ]
                )
                /
                max(
                    abs(
                        hi[
                            "Co"
                        ]
                    ),
                    abs(
                        med[
                            "Co"
                        ]
                    ),
                    1.0e-300,
                )
            )

        else:

            hi[
                "Co_rel"
            ] = math.inf

        refined.append(
            hi
        )

    ro = sorted(
        [
            x
            for x in refined
            if (
                x[
                    "strict"
                ]
                and
                math.isfinite(
                    x[
                        "Co"
                    ]
                )
            )
        ],
        key=lambda x:
            x[
                "Co"
            ],
    )

    ru = sorted(
        [
            x
            for x in refined
            if (
                x[
                    "strict"
                ]
                and
                math.isfinite(
                    x[
                        "Cu"
                    ]
                )
            )
        ],
        key=lambda x:
            x[
                "Cu"
            ],
    )

    rg = sorted(
        [
            x
            for x in refined
            if (
                x[
                    "strict"
                ]
                and
                math.isfinite(
                    x[
                        "g6"
                    ]
                )
            )
        ],
        key=lambda x:
            x[
                "g6"
            ],
    )

    bo = (
        ro[
            0
        ]
        if ro
        else None
    )

    bu = (
        ru[
            0
        ]
        if ru
        else None
    )

    bg = (
        rg[
            0
        ]
        if rg
        else None
    )

    def show(
        tag,
        x,
        key,
    ):

        if not x:

            print(
                f"{tag}_SURVIVOR=NO"
            )

            return

        print(
            f"{tag}_SURVIVOR=YES"
        )

        print(
            f"{tag}_{key.upper()}="
            f"{x[key]:.15e}"
        )

        print(
            f"{tag}_DIRECTION="
            f"{x['direction']}"
        )

        print(
            f"{tag}_THROAT_CLASS="
            f"{x['throat_class']}"
        )

        for k in (
            "R",
            "a",
            "clear",
            "minq",
            "beta",
            "m",
            "om",
            "lag",
            "gm",
            "gcap",
            "frac",
            "duty",
            "KU",
            "Kg",
            "Ko",
            "g6",
            "gu6",
            "g19",
            "g66",
            "mu",
        ):

            print(
                f"{tag}_"
                f"{k.upper()}="
                f"{x[k]:.15e}"
            )

    show(
        "BEST_OUTER",
        bo,
        "Co",
    )

    show(
        "BEST_UNIFORM",
        bu,
        "Cu",
    )

    show(
        "MIN_REQUIRED_G",
        bg,
        "g6",
    )

    independent = None

    if bo:

        independent = single(
            c2,
            cg,
            sg,
            ov,
            bo,
            NIND,
        )

        rd = (
            abs(
                independent[
                    "Co"
                ]
                -
                bo[
                    "Co"
                ]
            )
            /
            max(
                abs(
                    independent[
                        "Co"
                    ]
                ),
                abs(
                    bo[
                        "Co"
                    ]
                ),
                1.0e-300,
            )
        )

        print(
            f"INDEPENDENT_OUTER_C="
            f"{independent['Co']:.15e}"
        )

        print(
            f"INDEPENDENT_RELATIVE_DIFFERENCE="
            f"{rd:.15e}"
        )

        print(
            "INDEPENDENT_RECONSTRUCTION="
            +
            (
                "PASS"
                if rd
                <=
                5.0e-4
                else "FAIL"
            )
        )

        np.savez_compressed(
            OUTN,
            sep_grid=sg,
            overlap_grid=ov,
            best=np.array([
                independent[
                    k
                ]
                for k in (
                    "R",
                    "a",
                    "clear",
                    "d0",
                    "beta",
                    "m",
                    "om",
                    "gcap",
                    "lag",
                    "gm",
                )
            ]),
        )

    else:

        print(
            "INDEPENDENT_RECONSTRUCTION="
            "NOT_RUN_NO_SURVIVOR"
        )

    print(
        "=== DIRECTION COMPARISON ==="
    )

    direction_rows = []

    for m in MODES:

        rows = [
            x
            for x in ro
            if (
                x[
                    "direction"
                ]
                ==
                m[
                    0
                ]
            )
        ]

        x = (
            rows[
                0
            ]
            if rows
            else None
        )

        val = (
            x[
                "Co"
            ]
            if x
            else math.inf
        )

        print(
            f"{m[0]}_BEST_OUTER_C="
            f"{val:.15e}"
        )

        direction_rows.append({
            "direction":
                m[
                    0
                ],

            "throat_class":
                m[
                    4
                ],

            "best_outer_C":
                val,

            **counts[
                m[
                    0
                ]
            ],
        })

    pv = [
        x[
            "Co"
        ]
        for x in ro
        if x[
            "throat_class"
        ].startswith(
            "PARALLEL"
        )
    ]

    av = [
        x[
            "Co"
        ]
        for x in ro
        if x[
            "throat_class"
        ].startswith(
            "ANTIPARALLEL"
        )
    ]

    bp = (
        min(
            pv
        )
        if pv
        else math.inf
    )

    ba = (
        min(
            av
        )
        if av
        else math.inf
    )

    print(
        f"BEST_PARALLEL_C="
        f"{bp:.15e}"
    )

    print(
        f"BEST_ANTIPARALLEL_C="
        f"{ba:.15e}"
    )

    if (
        math.isfinite(
            bp
        )
        and
        math.isfinite(
            ba
        )
    ):

        print(
            f"PARALLEL_IMPROVEMENT_FACTOR="
            f"{ba / bp:.15e}"
        )

    outer6 = bool(
        bo
        and
        bo[
            "Co"
        ]
        <
        C006D
    )

    uniform6 = bool(
        bu
        and
        bu[
            "Cu"
        ]
        <
        C006D
    )

    outer19 = bool(
        bo
        and
        bo[
            "Co"
        ]
        <
        C024D1R
    )

    outer66 = bool(
        bo
        and
        bo[
            "Co"
        ]
        <
        C024D
    )

    min_g = (
        bg[
            "g6"
        ]
        if bg
        else math.inf
    )

    print(
        f"MIN_EXACT_G_REQUIRED_BEAT_006D="
        f"{min_g:.15e}"
    )

    print(
        f"PERTURBATIVE_G_LIMIT="
        f"{GMAX:.15e}"
    )

    if uniform6:

        decision = (
            "YELLOW_CLOSE_PASS_PORTAL_"
            "SURVIVES_UNIFORM_GUIDE_REACTION"
        )

        nxt = (
            "024E1_LOCAL_TWO_SCALAR_PORTAL_"
            "PLUS_GUIDE_DYNAMIC_TMUNU_PREFLIGHT"
        )

    elif outer6:

        decision = (
            "YELLOW_CLOSE_PASS_PORTAL_ONLY_WITH_"
            "LOW_KERNEL_STRESS_ROUTING"
        )

        nxt = (
            "024E1_TEST_MICROSCOPIC_STRESS_MEMORY_"
            "ROUTING_OR_RETURN_TO_024D2"
        )

    else:

        decision = (
            "RED_DUAL_TOROID_CLOSE_PASS_PORTAL_"
            "NO_STRICT_006D_ADVANCE"
        )

        nxt = (
            "CLOSE_024E_AND_RETURN_TO_024D2_"
            "MINIMAL_POLOIDAL_SCALAR_TRANSPORT_PREFLIGHT"
        )

    print(
        "PORTAL_OUTER_BEATS_006D="
        +
        (
            "YES"
            if outer6
            else "NO"
        )
    )

    print(
        "PORTAL_UNIFORM_BEATS_006D="
        +
        (
            "YES"
            if uniform6
            else "NO"
        )
    )

    print(
        "PORTAL_OUTER_BEATS_024D1R="
        +
        (
            "YES"
            if outer19
            else "NO"
        )
    )

    print(
        "PORTAL_OUTER_BEATS_024D_SCALAR="
        +
        (
            "YES"
            if outer66
            else "NO"
        )
    )

    print(
        f"024E_DECISION="
        f"{decision}"
    )

    print(
        f"NEXT="
        f"{nxt}"
    )

    print(
        "ENERGY_COLLISION_REQUIRED=NO"
    )

    print(
        "FIELD_OVERLAP_REQUIRED=YES"
    )

    print(
        "FULL_LOCAL_DYNAMIC_TMUNU_CONSERVATION="
        "NOT_ESTABLISHED"
    )

    print(
        "MICROSCOPIC_GUIDE_FIELD=NO"
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

    fields = sorted({
        k
        for x in refined
        for k, v in x.items()
        if isinstance(
            v,
            (
                int,
                float,
                bool,
                str,
                np.bool_,
            ),
        )
    })

    if refined:

        with OUTC.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as f:

            w = csv.DictWriter(
                f,
                fieldnames=fields,
                extrasaction="ignore",
            )

            w.writeheader()

            w.writerows(
                refined
            )

    with OUTD.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as f:

        w = csv.DictWriter(
            f,
            fieldnames=list(
                direction_rows[
                    0
                ]
            ),
        )

        w.writeheader()

        w.writerows(
            direction_rows
        )

    summary = {
        "claim":
            (
                "PROJECT_DERIVED_DUAL_TOROID_"
                "NONCOLLIDING_CLOSE_PASS_PORTAL_PREFILTER"
            ),

        "anchors": {
            "C006D":
                C006D,

            "C024D1R":
                C024D1R,

            "C024D":
                C024D,
        },

        "mechanism": {
            "collider":
                False,

            "centerline_intersection":
                False,

            "field_overlap":
                True,

            "portal":
                "g|Phi|^2|Chi|^2",

            "S_int":
                "-2V_int",
        },

        "scan": {
            "sobol":
                N,

            "total_direction_cases":
                4
                * N,

            "coarse":
                NP,

            "medium":
                NMED,

            "high":
                NHIGH,

            "independent":
                NIND,
        },

        "symmetry": {
            "parallel_relerr":
                ep,

            "antiparallel_relerr":
                ea,
        },

        "counts":
            counts,

        "best_outer":
            bo,

        "best_uniform":
            bu,

        "min_required_g":
            bg,

        "independent":
            independent,

        "decision": {
            "outer_beats_006D":
                outer6,

            "uniform_beats_006D":
                uniform6,

            "outer_beats_024D1R":
                outer19,

            "outer_beats_024D":
                outer66,

            "min_exact_g_required_006D":
                min_g,

            "result":
                decision,

            "next":
                nxt,

            "practical_device":
                False,
        },

        "limits": [
            "NO_SELF_BOUND_PACKET",
            "NO_MICROSCOPIC_GUIDE",
            "NO_FULL_LOCAL_DYNAMIC_TMUNU_CONSERVATION",
            "NO_FULL_STABILITY",
            "NO_NONLINEAR_GR",
            "NO_1_OVER_G_ESCAPE",
            "NO_RADIATIVE_EMISSION_CLAIM",
            "NO_DEVICE",
        ],
    }

    OUTJ.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
            allow_nan=True,
        )
        +
        "\n"
    )

    print(
        f"SUMMARY_JSON="
        f"{OUTJ.relative_to(ROOT)}"
    )

    print(
        f"TOP_CSV="
        f"{OUTC.relative_to(ROOT)}"
    )

    print(
        f"DIRECTION_CSV="
        f"{OUTD.relative_to(ROOT)}"
    )

    if OUTN.exists():

        print(
            f"BEST_PROFILE_NPZ="
            f"{OUTN.relative_to(ROOT)}"
        )

    print(
        "024E_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
