#!/usr/bin/env python3
"""024E1 — teacher-guided anisotropic non-colliding close-pass rescue.

PURPOSE
-------
Perform the final morphology/participation rescue of the 024E dual-toroid
non-colliding close-pass scalar-portal mechanism.

024E already gave the interaction the locally optimal negative-active
equation of state allowed by DEC:

    rho_int = V_int

    p_1 = p_2 = p_3 = -V_int

therefore:

    S_int = rho_int + p_1 + p_2 + p_3 = -2 V_int

and:

    -S_int/rho_int = 2.

Thus the remaining deficit cannot honestly be repaired by simply assigning
more negative stress per joule.

024E failed because only a very small fraction of the packet energy entered
the overlap interaction.

INTROSPECTIVE MOTIVATION
------------------------
The raw teacher showed:

    productive-energy scale ~ 0.197

    >92 percent gross outward influence associated with that energy fraction

    cancellation ~ 1.06

    ~59 percent of net response from spatial stress

and operated close to the DEC boundary.

The teacher itself is not a microscopic field and its huge raw coefficient
headroom is not continuum certified.

The lesson used here is only:

    concentrate the productive sector;

    place it at high payload kernel;

    route unavoidable positive/scaffolding energy to lower kernel;

    minimize cancellation.

024E BOUNDARY SIGNAL
--------------------
The best 024E required-coupling candidate pushed toward:

    packet radius near the upper scan boundary;

    source clearance near zero;

    closest separation near the lower allowed boundary;

    low orbital speed.

This suggests that the spherical packet parameterization may have artificially
coupled:

    horizontal interaction area

to

    vertical burial depth.

024E1 therefore separates those scales.

ANISOTROPIC PACKET
------------------
Use a compact ellipsoidal canonical complex-scalar profile:

    F(q)
      =
    A (1-r_e^2)^n

for:

    r_e^2
      =
    x^2/a_x^2
    +
    y^2/a_y^2
    +
    z^2/a_z^2
      < 1,

and F=0 outside.

The smoothness exponent is scanned over:

    n =
      1.25
      1.5
      2
      2.5
      3
      4
      6
      8.

Interpretation near the central throat:

    a_x:
        width toward the opposite toroid

    a_y:
        tangential / junction width

    a_z:
        vertical thickness.

The key new freedom is:

    a_y >> a_z

which creates a wide interaction lens without forcing the source center
far below the payload.

LAB-LOCKED SHAPE WARNING
------------------------
The coarse packet ellipsoids are treated as lab-axis-aligned stress lenses.

This is an optimistic morphology prefilter.

A real orbiting microscopic field would have to create, transport, or orient
this anisotropy dynamically.

No orientation-control energy is invented here because an arbitrary penalty
would become an accidental physics law.

A surviving result therefore authorizes a later orientation/field-equation
gate; it is not itself a field realization.

CORE NON-COLLISION
------------------
The user specifically does not want an energy collider.

Define the half-amplitude radius in transformed coordinates:

    r_1/2
      =
    sqrt(1 - 2^(-1/n)).

The dense half-amplitude core has x half-width:

    r_1/2 a_x.

For the strict non-collider class require at closest approach:

    d_min
      >=
    2 r_1/2 a_x.

Therefore the high-amplitude packet cores do not overlap.

The lower-amplitude field support may overlap.

A separate loose diagnostic permits deeper core overlap, but it can never
promote the requested non-collider mechanism.

PROFILE INTEGRALS
-----------------
Let:

    V_s = a_x a_y a_z.

For the unit transformed sphere define:

    C_2(n)
      =
    integral f^2 d^3q

and:

    C_g,axis(n)
      =
    integral (partial_x f)^2 d^3q.

By rotational symmetry in transformed coordinates, all three axis constants
are equal.

The canonical packet rest-energy normalization is:

    1
      =
    A^2 V_s
    [
      C_2 (omega^2 + m^2)
      +
      C_g,axis
      (
        1/a_x^2
        +
        1/a_y^2
        +
        1/a_z^2
      )
    ].

This reduces exactly to the 024E spherical expression when:

    a_x=a_y=a_z=a
    and
    n=2.

PORTAL
------
Retain exactly the 024E healthy positive quartic portal:

    V_int
      =
    g |Phi|^2 |Chi|^2,

with:

    g >= 0.

The active interaction source remains:

    S_int = -2 V_int.

For two equal aligned ellipsoids whose center separation in transformed
coordinates is s, the portal integral is:

    U_int
      =
    g A^4 V_s O_n(s).

The dimensionless overlap function O_n(s) is independently numerically
tabulated for every profile exponent.

The support overlap vanishes for:

    s >= 2.

DIRECTION CLASSES
-----------------
024E established global direction-reversal symmetry to numerical precision.

024E1 therefore tests only the two inequivalent throat kinematics:

    PARALLEL_AT_THROAT

    ANTIPARALLEL_AT_THROAT.

Their globally reversed copies are already a verified symmetry control.

The scalar magnitude portal is parity-even, so no directional advantage is
assumed.

TRACK GEOMETRY
--------------
Payload center:

    (0,0,1).

Packet vertical center:

    z_c = -(a_z + clearance).

Therefore packet support obeys:

    z <= -clearance <= 0.

Two side-by-side circular track centers are:

    x_c,L = -(R+d0/2)

    x_c,R = +(R+d0/2),

each with radius R.

Closest packet-center distance:

    d0 > 0.

The scan sets:

    d0
      =
    2 r_1/2 a_x gamma_core,

with:

    gamma_core in [0.25,2.5].

Strict requested non-collider:

    gamma_core >= 1.

Loose diagnostic:

    gamma_core < 1.

MORPHOLOGY GATE
---------------
For strict promotion also require:

    a_x/R <= 0.75

    a_y/R <= 0.75.

This prevents the packet lens from becoming larger than the track itself.

No arbitrary upper bound is imposed on density.

024A4R already established that numerical density caps must not become
accidental physical laws.

INTROSPECTIVE PARTICIPATION METRICS
-----------------------------------
Report:

    peak portal energy / total inventory

    cycle-average portal energy / total inventory

    gross outward interaction contribution

    gross inward baseline + reset contribution

    cancellation factor.

Reference only:

    teacher productive-energy fraction ~0.197

    teacher cancellation ~1.06.

These are NOT imposed as fit targets.

ACTUAL-RING LEDGER
------------------
The ordinary mobile packet and guide energy experience the actual ring-average
kernel.

The negative portal interaction experiences its actual overlap-weighted kernel.

Virial/stress compensation is routed to the low-kernel outer quarter-arcs,
the same optimistic routing used in 024E.

This is called:

    ACTUAL_RING_OUTER_RESET.

TEACHER-ROUTING CEILING
-----------------------
Construct an intentionally over-favorable bound:

    all nonproductive mobile/guide active source
        -> outer-arc kernel

    portal negative-active source
        -> actual high-kernel overlap

    positive compensation
        -> outer-arc kernel.

This is:

    TEACHER_ROUTING_CEILING.

It is NOT a physical orbiting-packet solution.

It answers the decisive question:

    If spatial organization were nearly ideal, could a perturbative
    close-pass portal possibly compete?

If even this ceiling fails, packet-shape polishing cannot save the branch.

COUPLING / DISTORTION
---------------------
Retain:

    g <= 4 pi.

Also require peak portal interaction energy:

    U_int,peak / E_mobile <= 0.25.

The allowed coupling is:

    g_cap
      =
    min(
      4 pi,
      0.25 E_mobile / U1_peak
    ).

As in 024E, analytically solve the exact coupling needed to:

    first become outward;

    beat 006D;

    beat 024D1R;

    beat the relaxed 024D scalar source.

CANCELLATION
------------
For outer-reset ledger:

    A_out,gross
      =
    2 <U_int> K_int

    A_in,gross
      =
    A_baseline
      +
    2 <U_int> K_reset

and:

    cancellation
      =
    (A_out,gross + A_in,gross)
    /
    |A_out,gross - A_in,gross|.

Low cancellation is favored but not forced.

SCAN
----
Use:

    2^19 = 524,288 Sobol morphology/microphysics cases

times:

    2 inequivalent direction classes.

Primary scanned parameters:

    R/h:
        0.4 to 8

    a_x/h:
        0.03 to 1.2

    a_y/a_x:
        0.5 to 8

    a_z/a_x:
        0.05 to 1

    clearance/h:
        0 to 0.20

    gamma_core:
        0.25 to 2.5

    beta:
        0.02 to 0.50

    m h:
        0.05 to 50

    omega/m:
        1 to 3

    phase lag:
        -0.35 to 0.35 rad

    guide multiplier:
        1 to 3

    profile exponent:
        eight discrete smooth profiles.

The user-requested wildcard numbers are not used as optimization targets.

They are not physics priors.

REFINEMENT
----------
Coarse phase samples:

    256.

Medium:

    4096.

High:

    16384.

The best strict candidate receives an independent 4-D cubature using:

    2048 orbital phases

    768 internal Sobol volume points

to independently reconstruct:

    packet finite-volume kernel;

    portal overlap integral;

    portal overlap-weighted kernel;

    peak interaction energy;

    cycle-average interaction energy;

    final coefficient.

This independently tests the centerline/overlap-table approximation.

SPHERICAL REGRESSION
--------------------
Before the full scan, rebuild the selected 024E minimum-required-g spherical
candidate using:

    a_x=a_y=a_z=a
    n=2.

Require close agreement with the stored 024E required coupling.

This protects continuity with the predecessor.

PROMOTION
---------
A strict morphology survivor requires:

    dense half-amplitude cores non-overlapping;

    source support entirely z<=0;

    ring morphology gate pass;

    g_cap <= 4 pi;

    portal peak distortion <=25 percent;

    full-cycle compensation included;

    actual-ring C < C_006D;

    medium/high convergence;

    independent cubature agreement.

A teacher-routing-ceiling success WITHOUT an actual-ring success is not a
mechanism promotion.

It means:

    close-pass portal has theoretical morphology headroom

but:

    the orbit keeps too much ordinary positive energy in the wrong kernel.

FALSIFIERS
----------
Strong closeout:

    STRICT_TEACHER_ROUTING_CEILING_BEATS_006D = NO.

Then even near-ideal Introspective-inspired source organization cannot save
the perturbative close-pass portal.

Core-overlap-only result:

    LOOSE_BEATS_006D = YES

    STRICT_BEATS_006D = NO.

Then the requested non-collider concept fails; success requires collision-like
core overlap.

Actual-ring failure but ceiling success:

    spatial routing, not close-pass stress generation, remains the dominant
    mechanism.

STOP RULE
---------
If strict actual-ring cases fail 006D and the teacher-routing ceiling gives no
large margin:

    CLOSE 024E/024E1.

Return to:

    024D2 minimal canonical-scalar poloidal transport field preflight.

Do not run another packet-profile scan.

CLAIM CLASS
-----------
PROJECT_DERIVED_TEACHER_GUIDED_ANISOTROPIC_CLOSE_PASS_PORTAL_PREFILTER

DOES NOT ESTABLISH
------------------
- a self-bound anisotropic packet;
- shape-orientation dynamics;
- a microscopic guide;
- full local dynamic T_munu conservation;
- stability;
- nonlinear GR;
- favorable absolute energy scaling;
- a practical device.
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

PREV_E = DATA / "024e_dual_toroid_close_pass_portal_summary.json"
PREV_D = DATA / "024d1r_kernel_adaptive_internal_orbit_repair_summary.json"

OUTJ = DATA / "024e1_teacher_guided_anisotropic_close_pass_summary.json"
OUTC = DATA / "024e1_teacher_guided_anisotropic_close_pass_top.csv"
OUTS = DATA / "024e1_teacher_guided_anisotropic_shape_summary.csv"
OUTN = DATA / "024e1_teacher_guided_anisotropic_best_profile.npz"

C006D = 23.591586299249
C024D1R = 19.04617786197023
C024D = 6.610457607426174

GMAX = 4.0 * math.pi
DISTORT = 0.25

TEACHER_PRODUCTIVE_REFERENCE = 0.197
TEACHER_GROSS_SHARE_REFERENCE = 0.92
TEACHER_CANCELLATION_REFERENCE = 1.06

EXPONENTS = np.asarray(
    [
        1.25,
        1.5,
        2.0,
        2.5,
        3.0,
        4.0,
        6.0,
        8.0,
    ],
    dtype=float,
)

SMOKE = os.environ.get("AG_SMOKE", "0") == "1"

SOBOL_POWER = 11 if SMOKE else 19
NCASE = 2 ** SOBOL_POWER

NPHASE = 96 if SMOKE else 256
NMED = 512 if SMOKE else 4096
NHIGH = 1024 if SMOKE else 16384

BATCH = 128 if SMOKE else 512
TOP_KEEP = 24 if SMOKE else 120

CUB_PHASE = 256 if SMOKE else 2048
CUB_POINTS = 192 if SMOKE else 768

MODES = (
    (
        "PARALLEL_AT_THROAT",
        +1.0,
        -1.0,
        +1.0,
    ),
    (
        "ANTIPARALLEL_AT_THROAT",
        +1.0,
        +1.0,
        +1.0,
    ),
)


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(f"Required file missing: {path}")


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def wrap(x: np.ndarray) -> np.ndarray:
    return (x + math.pi) % (2.0 * math.pi) - math.pi


def profile_tables():
    """Return profile normalization and overlap tables."""

    xr, wr = leggauss(240 if not SMOKE else 100)

    r = 0.5 * (xr + 1.0)
    w = 0.5 * wr

    c2 = np.empty(len(EXPONENTS))
    cg_axis = np.empty(len(EXPONENTS))
    rhalf = np.empty(len(EXPONENTS))

    for i, n in enumerate(EXPONENTS):

        f = np.maximum(1.0 - r * r, 0.0) ** n

        df = (
            -2.0
            * n
            * r
            * np.maximum(
                1.0 - r * r,
                0.0,
            ) ** (n - 1.0)
        )

        c2[i] = float(
            4.0
            * math.pi
            * np.sum(
                w * r * r * f * f
            )
        )

        cg_total = float(
            4.0
            * math.pi
            * np.sum(
                w * r * r * df * df
            )
        )

        cg_axis[i] = cg_total / 3.0

        rhalf[i] = math.sqrt(
            1.0
            -
            0.5 ** (1.0 / n)
        )

    nsep = 220 if SMOKE else 360

    sgrid = np.linspace(
        0.0,
        2.0,
        nsep,
    )

    overlap = np.zeros(
        (
            len(EXPONENTS),
            nsep,
        ),
        dtype=float,
    )

    gx, gw = leggauss(
        36 if SMOKE else 72
    )

    gr, grw = leggauss(
        36 if SMOKE else 72
    )

    for ie, n in enumerate(EXPONENTS):

        for isep, s in enumerate(sgrid):

            if s >= 2.0:
                continue

            lo = -1.0 + 0.5 * s
            hi = +1.0 - 0.5 * s

            xx = (
                0.5
                * (hi - lo)
                * gx
                +
                0.5
                * (hi + lo)
            )

            wx = (
                0.5
                * (hi - lo)
                * gw
            )

            total = 0.0

            for xv, wv in zip(xx, wx):

                q1x2 = (xv + 0.5 * s) ** 2
                q2x2 = (xv - 0.5 * s) ** 2

                rperp2_max = max(
                    0.0,
                    min(
                        1.0 - q1x2,
                        1.0 - q2x2,
                    ),
                )

                if rperp2_max <= 0.0:
                    continue

                rmax = math.sqrt(rperp2_max)

                rr = (
                    0.5
                    * rmax
                    * (gr + 1.0)
                )

                rw = (
                    0.5
                    * rmax
                    * grw
                )

                q1sq = (
                    q1x2
                    +
                    rr * rr
                )

                q2sq = (
                    q2x2
                    +
                    rr * rr
                )

                f1sq = (
                    np.maximum(
                        1.0 - q1sq,
                        0.0,
                    )
                    ** (2.0 * n)
                )

                f2sq = (
                    np.maximum(
                        1.0 - q2sq,
                        0.0,
                    )
                    ** (2.0 * n)
                )

                total += float(
                    wv
                    * 2.0
                    * math.pi
                    * np.sum(
                        rw
                        * rr
                        * f1sq
                        * f2sq
                    )
                )

            overlap[ie, isep] = total

    if not np.all(c2 > 0.0):
        raise RuntimeError("Invalid C2 table")

    if not np.all(cg_axis > 0.0):
        raise RuntimeError("Invalid gradient table")

    if not np.all(overlap[:, 0] > 0.0):
        raise RuntimeError("Invalid overlap table at zero separation")

    return {
        "c2":
            c2,

        "cg_axis":
            cg_axis,

        "rhalf":
            rhalf,

        "sgrid":
            sgrid,

        "overlap":
            overlap,
    }


def overlap_lookup(
    s: np.ndarray,
    exponent_index: np.ndarray,
    table: dict,
) -> np.ndarray:
    """Interpolate O_n(s) for a batch of exponents."""

    out = np.zeros_like(
        s,
        dtype=float,
    )

    sg = table["sgrid"]
    ot = table["overlap"]

    for ie in range(len(EXPONENTS)):

        rows = np.flatnonzero(
            exponent_index == ie
        )

        if len(rows) == 0:
            continue

        vals = np.clip(
            s[rows],
            0.0,
            2.0,
        )

        out[rows] = np.interp(
            vals,
            sg,
            ot[ie],
        )

        out[rows] = np.where(
            s[rows] < 2.0,
            out[rows],
            0.0,
        )

    return out


def build_parameters(
    table: dict,
) -> dict[str, np.ndarray]:
    """Build the teacher-guided morphology population."""

    sampler = qmc.Sobol(
        d=12,
        scramble=True,
        seed=240501,
    )

    u = sampler.random_base2(
        SOBOL_POWER
    )

    R = 10.0 ** (
        math.log10(0.4)
        +
        (
            math.log10(8.0)
            -
            math.log10(0.4)
        )
        * u[:, 0]
    )

    ax = 10.0 ** (
        math.log10(0.03)
        +
        (
            math.log10(1.2)
            -
            math.log10(0.03)
        )
        * u[:, 1]
    )

    ay_ratio = 10.0 ** (
        math.log10(0.5)
        +
        (
            math.log10(8.0)
            -
            math.log10(0.5)
        )
        * u[:, 2]
    )

    az_ratio = 10.0 ** (
        math.log10(0.05)
        +
        (
            math.log10(1.0)
            -
            math.log10(0.05)
        )
        * u[:, 3]
    )

    ay = ax * ay_ratio
    az = ax * az_ratio

    clearance = (
        0.20
        * u[:, 4]
    )

    core_gap_factor = (
        0.25
        +
        2.25
        * u[:, 5]
    )

    beta = (
        0.02
        +
        0.48
        * u[:, 6]
    )

    m = 10.0 ** (
        math.log10(0.05)
        +
        (
            math.log10(50.0)
            -
            math.log10(0.05)
        )
        * u[:, 7]
    )

    omega_ratio = (
        1.0
        +
        2.0
        * u[:, 8]
    )

    lag = (
        -0.35
        +
        0.70
        * u[:, 9]
    )

    guide_multiplier = (
        1.0
        +
        2.0
        * u[:, 10]
    )

    exponent_index = np.minimum(
        (
            u[:, 11]
            * len(EXPONENTS)
        ).astype(int),
        len(EXPONENTS) - 1,
    )

    exponent = EXPONENTS[
        exponent_index
    ]

    rhalf = table["rhalf"][
        exponent_index
    ]

    d0 = (
        2.0
        * rhalf
        * ax
        * core_gap_factor
    )

    omega = (
        m
        * omega_ratio
    )

    return {
        "R":
            R,

        "ax":
            ax,

        "ay":
            ay,

        "az":
            az,

        "ay_ratio":
            ay_ratio,

        "az_ratio":
            az_ratio,

        "clearance":
            clearance,

        "core_gap_factor":
            core_gap_factor,

        "d0":
            d0,

        "beta":
            beta,

        "m":
            m,

        "omega_ratio":
            omega_ratio,

        "omega":
            omega,

        "lag":
            lag,

        "guide_multiplier":
            guide_multiplier,

        "exponent_index":
            exponent_index,

        "exponent":
            exponent,
    }


def microphysics(
    p: dict[str, np.ndarray],
    table: dict,
) -> dict[str, np.ndarray]:
    """Normalize the anisotropic canonical scalar packets."""

    idx = p["exponent_index"]

    c2 = table["c2"][idx]
    cga = table["cg_axis"][idx]

    V = (
        p["ax"]
        * p["ay"]
        * p["az"]
    )

    gradient_factor = (
        1.0 / p["ax"] ** 2
        +
        1.0 / p["ay"] ** 2
        +
        1.0 / p["az"] ** 2
    )

    denom = (
        V
        * (
            c2
            * (
                p["omega"] ** 2
                +
                p["m"] ** 2
            )
            +
            cga
            * gradient_factor
        )
    )

    A2 = (
        1.0
        /
        np.maximum(
            denom,
            1.0e-300,
        )
    )

    srest = (
        A2
        * V
        * c2
        * (
            4.0
            * p["omega"] ** 2
            -
            2.0
            * p["m"] ** 2
        )
    )

    gamma = (
        1.0
        /
        np.sqrt(
            1.0
            -
            p["beta"] ** 2
        )
    )

    Em = (
        2.0
        * gamma
    )

    Eg0 = (
        Em
        * p["beta"] ** 2
    )

    Eg = (
        Eg0
        * p["guide_multiplier"]
    )

    return {
        "V":
            V,

        "A2":
            A2,

        "srest":
            srest,

        "gamma":
            gamma,

        "Em":
            Em,

        "Eg0":
            Eg0,

        "Eg":
            Eg,

        "Eextra":
            Eg - Eg0,
    }


def ring_kernels(
    R: np.ndarray,
    d0: np.ndarray,
    zc: np.ndarray,
    nphase: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Centerline ring-average and low-kernel outer-arc kernels."""

    phase = np.linspace(
        0.0,
        2.0 * math.pi,
        nphase,
        endpoint=False,
    )[None, :]

    R2 = R[:, None]
    d2 = d0[:, None]
    z2 = zc[:, None]

    cc = (
        R2
        +
        0.5 * d2
    )

    dz = (
        1.0
        -
        z2
    )

    xl = (
        -cc
        +
        R2 * np.cos(phase)
    )

    yl = (
        R2 * np.sin(phase)
    )

    xr = (
        +cc
        +
        R2 * np.cos(phase)
    )

    yr = (
        R2 * np.sin(phase)
    )

    kl = (
        dz
        /
        (
            xl * xl
            +
            yl * yl
            +
            dz * dz
        ) ** 1.5
    )

    kr = (
        dz
        /
        (
            xr * xr
            +
            yr * yr
            +
            dz * dz
        ) ** 1.5
    )

    kmean = (
        0.5
        * (
            np.mean(kl, axis=1)
            +
            np.mean(kr, axis=1)
        )
    )

    left_outer = (
        np.abs(
            wrap(
                phase
                -
                math.pi
            )
        )
        <=
        math.pi / 4.0
    )

    right_outer = (
        np.abs(
            wrap(phase)
        )
        <=
        math.pi / 4.0
    )

    kouter = (
        0.5
        * (
            np.sum(
                kl * left_outer,
                axis=1,
            )
            /
            np.sum(
                left_outer,
                axis=1,
            )
            +
            np.sum(
                kr * right_outer,
                axis=1,
            )
            /
            np.sum(
                right_outer,
                axis=1,
            )
        )
    )

    return (
        kmean,
        kouter,
    )


def required_g(
    E0: np.ndarray,
    baseline: np.ndarray,
    gain_per_g: np.ndarray,
    peak_u1: np.ndarray,
    target: float | None,
) -> np.ndarray:
    """Exact g required for positivity or target coefficient."""

    if target is None:

        return np.divide(
            baseline,
            gain_per_g,
            out=np.full_like(
                baseline,
                np.inf,
            ),
            where=(
                gain_per_g > 0.0
            ),
        )

    denominator = (
        target
        * gain_per_g
        -
        peak_u1
    )

    numerator = (
        E0
        +
        target
        * baseline
    )

    return np.divide(
        numerator,
        denominator,
        out=np.full_like(
            baseline,
            np.inf,
        ),
        where=(
            denominator > 0.0
        ),
    )


def slice_dict(
    d: dict[str, np.ndarray],
    sl: slice,
) -> dict[str, np.ndarray]:
    return {
        k: v[sl]
        for k, v in d.items()
    }


def evaluate_mode(
    p: dict[str, np.ndarray],
    micro: dict[str, np.ndarray],
    table: dict,
    mode,
    nphase: int,
) -> dict[str, np.ndarray]:
    """Evaluate one inequivalent close-pass direction class."""

    mode_name, sign_left, sign_right, lag_sign = mode

    phase = np.linspace(
        0.0,
        2.0 * math.pi,
        nphase,
        endpoint=False,
    )[None, :]

    R = p["R"][:, None]
    d0 = p["d0"][:, None]

    cc = (
        R
        +
        0.5 * d0
    )

    lag = (
        lag_sign
        * p["lag"]
    )[:, None]

    theta_left = (
        sign_left
        * phase
    )

    theta_right = (
        math.pi
        +
        sign_right
        * phase
        +
        lag
    )

    x_left = (
        -cc
        +
        R * np.cos(theta_left)
    )

    y_left = (
        R * np.sin(theta_left)
    )

    x_right = (
        +cc
        +
        R * np.cos(theta_right)
    )

    y_right = (
        R * np.sin(theta_right)
    )

    dx = (
        x_right
        -
        x_left
    )

    dy = (
        y_right
        -
        y_left
    )

    scaled_separation = np.sqrt(
        (
            dx
            /
            p["ax"][:, None]
        ) ** 2
        +
        (
            dy
            /
            p["ay"][:, None]
        ) ** 2
    )

    overlap = overlap_lookup(
        scaled_separation,
        p["exponent_index"],
        table,
    )

    U1 = (
        micro["A2"][:, None] ** 2
        *
        micro["V"][:, None]
        *
        overlap
    )

    x_mid = (
        0.5
        * (
            x_left
            +
            x_right
        )
    )

    y_mid = (
        0.5
        * (
            y_left
            +
            y_right
        )
    )

    zc = (
        -(
            p["az"]
            +
            p["clearance"]
        )
    )

    dz_payload = (
        1.0
        -
        zc[:, None]
    )

    K_interaction = (
        dz_payload
        /
        (
            x_mid * x_mid
            +
            y_mid * y_mid
            +
            dz_payload * dz_payload
        ) ** 1.5
    )

    Kg, Ko = ring_kernels(
        p["R"],
        p["d0"],
        zc,
        nphase,
    )

    ua = np.mean(
        U1,
        axis=1,
    )

    u1 = np.max(
        U1,
        axis=1,
    )

    uk = np.mean(
        U1
        * K_interaction,
        axis=1,
    )

    KU = np.divide(
        uk,
        ua,
        out=np.zeros_like(ua),
        where=(
            ua > 0.0
        ),
    )

    B1 = (
        2.0
        * ua
    )

    gain_outer_per_g = (
        B1
        * np.maximum(
            KU
            -
            Ko,
            0.0,
        )
    )

    gain_uniform_per_g = (
        B1
        * np.maximum(
            KU
            -
            Kg,
            0.0,
        )
    )

    active_mobile_factor = np.maximum(
        1.0,
        micro["srest"],
    )

    mobile_active = (
        micro["Em"]
        * active_mobile_factor
    )

    baseline_actual = (
        mobile_active
        * Kg
        +
        micro["Eextra"]
        * Kg
    )

    baseline_teacher = (
        (
            mobile_active
            +
            micro["Eextra"]
        )
        * Ko
    )

    E0 = (
        micro["Em"]
        +
        micro["Eg"]
    )

    g_distortion = np.divide(
        DISTORT
        * micro["Em"],
        u1,
        out=np.full_like(
            u1,
            np.inf,
        ),
        where=(
            u1 > 0.0
        ),
    )

    gcap = np.minimum(
        GMAX,
        g_distortion,
    )

    Upeak = (
        gcap
        * u1
    )

    Uavg = (
        gcap
        * ua
    )

    inventory = (
        E0
        +
        Upeak
    )

    A_actual_outer = (
        -baseline_actual
        +
        gcap
        * gain_outer_per_g
    )

    A_actual_uniform = (
        -baseline_actual
        +
        gcap
        * gain_uniform_per_g
    )

    A_teacher_ceiling = (
        -baseline_teacher
        +
        gcap
        * gain_outer_per_g
    )

    C_actual_outer = np.where(
        A_actual_outer > 0.0,
        inventory / A_actual_outer,
        np.inf,
    )

    C_actual_uniform = np.where(
        A_actual_uniform > 0.0,
        inventory / A_actual_uniform,
        np.inf,
    )

    C_teacher_ceiling = np.where(
        A_teacher_ceiling > 0.0,
        inventory / A_teacher_ceiling,
        np.inf,
    )

    gpos_actual = required_g(
        E0,
        baseline_actual,
        gain_outer_per_g,
        u1,
        None,
    )

    g006d_actual = required_g(
        E0,
        baseline_actual,
        gain_outer_per_g,
        u1,
        C006D,
    )

    g19_actual = required_g(
        E0,
        baseline_actual,
        gain_outer_per_g,
        u1,
        C024D1R,
    )

    g66_actual = required_g(
        E0,
        baseline_actual,
        gain_outer_per_g,
        u1,
        C024D,
    )

    g006d_teacher = required_g(
        E0,
        baseline_teacher,
        gain_outer_per_g,
        u1,
        C006D,
    )

    peak_participation = np.divide(
        Upeak,
        inventory,
        out=np.zeros_like(
            Upeak,
        ),
        where=(
            inventory > 0.0
        ),
    )

    cycle_participation = np.divide(
        Uavg,
        inventory,
        out=np.zeros_like(
            Uavg,
        ),
        where=(
            inventory > 0.0
        ),
    )

    gross_out = (
        2.0
        * Uavg
        * KU
    )

    gross_in_actual = (
        baseline_actual
        +
        2.0
        * Uavg
        * Ko
    )

    cancellation_actual = np.divide(
        gross_out
        +
        gross_in_actual,
        np.abs(
            gross_out
            -
            gross_in_actual
        ),
        out=np.full_like(
            gross_out,
            np.inf,
        ),
        where=(
            np.abs(
                gross_out
                -
                gross_in_actual
            )
            >
            1.0e-15
        ),
    )

    core_strict = (
        p["core_gap_factor"]
        >=
        1.0
    )

    morphology_strict = (
        (p["ax"] / p["R"] <= 0.75)
        &
        (p["ay"] / p["R"] <= 0.75)
    )

    strict = (
        core_strict
        &
        morphology_strict
        &
        (p["clearance"] >= 0.0)
        &
        (
            Upeak
            /
            micro["Em"]
            <=
            DISTORT
            +
            1.0e-12
        )
    )

    loose = (
        (p["core_gap_factor"] >= 0.25)
        &
        (p["ax"] / p["R"] <= 1.0)
        &
        (p["ay"] / p["R"] <= 1.0)
    )

    overlap_duty = np.mean(
        U1
        >=
        0.1
        * np.maximum(
            u1[:, None],
            1.0e-300,
        ),
        axis=1,
    )

    return {
        "mode_name":
            mode_name,

        "Kg":
            Kg,

        "Ko":
            Ko,

        "KU":
            KU,

        "ua":
            ua,

        "u1":
            u1,

        "gcap":
            gcap,

        "Upeak":
            Upeak,

        "Uavg":
            Uavg,

        "inventory":
            inventory,

        "baseline_actual":
            baseline_actual,

        "baseline_teacher":
            baseline_teacher,

        "gain_outer_per_g":
            gain_outer_per_g,

        "gain_uniform_per_g":
            gain_uniform_per_g,

        "A_actual_outer":
            A_actual_outer,

        "A_actual_uniform":
            A_actual_uniform,

        "A_teacher_ceiling":
            A_teacher_ceiling,

        "C_actual_outer":
            C_actual_outer,

        "C_actual_uniform":
            C_actual_uniform,

        "C_teacher_ceiling":
            C_teacher_ceiling,

        "gpos_actual":
            gpos_actual,

        "g006d_actual":
            g006d_actual,

        "g19_actual":
            g19_actual,

        "g66_actual":
            g66_actual,

        "g006d_teacher":
            g006d_teacher,

        "peak_participation":
            peak_participation,

        "cycle_participation":
            cycle_participation,

        "cancellation_actual":
            cancellation_actual,

        "overlap_duty":
            overlap_duty,

        "strict":
            strict,

        "loose":
            loose,
    }


def candidate_record(
    global_index: int,
    local_index: int,
    p: dict[str, np.ndarray],
    micro: dict[str, np.ndarray],
    result: dict[str, np.ndarray],
    mode,
) -> dict:
    """Serialize one candidate."""

    j = local_index

    out = {
        "index":
            int(global_index),

        "direction_class":
            mode[0],
    }

    for key in (
        "R",
        "ax",
        "ay",
        "az",
        "ay_ratio",
        "az_ratio",
        "clearance",
        "core_gap_factor",
        "d0",
        "beta",
        "m",
        "omega_ratio",
        "omega",
        "lag",
        "guide_multiplier",
        "exponent_index",
        "exponent",
    ):

        value = p[key][j]

        if key == "exponent_index":
            out[key] = int(value)
        else:
            out[key] = float(value)

    for key in (
        "V",
        "A2",
        "srest",
        "gamma",
        "Em",
        "Eg0",
        "Eg",
        "Eextra",
    ):

        out[key] = float(
            micro[key][j]
        )

    for key in (
        "Kg",
        "Ko",
        "KU",
        "ua",
        "u1",
        "gcap",
        "Upeak",
        "Uavg",
        "inventory",
        "baseline_actual",
        "baseline_teacher",
        "gain_outer_per_g",
        "gain_uniform_per_g",
        "A_actual_outer",
        "A_actual_uniform",
        "A_teacher_ceiling",
        "C_actual_outer",
        "C_actual_uniform",
        "C_teacher_ceiling",
        "gpos_actual",
        "g006d_actual",
        "g19_actual",
        "g66_actual",
        "g006d_teacher",
        "peak_participation",
        "cycle_participation",
        "cancellation_actual",
        "overlap_duty",
    ):

        out[key] = float(
            result[key][j]
        )

    out["strict"] = bool(
        result["strict"][j]
    )

    out["loose"] = bool(
        result["loose"][j]
    )

    return out


def keep_best(
    pool: list[dict],
    candidates: list[dict],
    key: str,
    count: int = TOP_KEEP,
) -> None:
    """Retain smallest finite values."""

    pool.extend(candidates)

    pool[:] = [
        row
        for row in pool
        if math.isfinite(
            float(
                row[key]
            )
        )
    ]

    pool.sort(
        key=lambda row:
            float(
                row[key]
            )
    )

    del pool[count:]


def scalar_parameter_dict(
    row: dict,
) -> dict[str, np.ndarray]:
    """Convert one stored row back to a one-case array dict."""

    return {
        "R":
            np.asarray([row["R"]]),

        "ax":
            np.asarray([row["ax"]]),

        "ay":
            np.asarray([row["ay"]]),

        "az":
            np.asarray([row["az"]]),

        "ay_ratio":
            np.asarray([row["ay_ratio"]]),

        "az_ratio":
            np.asarray([row["az_ratio"]]),

        "clearance":
            np.asarray([row["clearance"]]),

        "core_gap_factor":
            np.asarray([row["core_gap_factor"]]),

        "d0":
            np.asarray([row["d0"]]),

        "beta":
            np.asarray([row["beta"]]),

        "m":
            np.asarray([row["m"]]),

        "omega_ratio":
            np.asarray([row["omega_ratio"]]),

        "omega":
            np.asarray([row["omega"]]),

        "lag":
            np.asarray([row["lag"]]),

        "guide_multiplier":
            np.asarray([row["guide_multiplier"]]),

        "exponent_index":
            np.asarray(
                [
                    int(
                        row["exponent_index"]
                    )
                ],
                dtype=int,
            ),

        "exponent":
            np.asarray([row["exponent"]]),
    }


def refine_one(
    row: dict,
    table: dict,
    nphase: int,
) -> dict:
    """Re-evaluate one candidate."""

    p = scalar_parameter_dict(row)

    micro = microphysics(
        p,
        table,
    )

    mode = next(
        item
        for item in MODES
        if item[0]
        ==
        row["direction_class"]
    )

    result = evaluate_mode(
        p,
        micro,
        table,
        mode,
        nphase,
    )

    refined = candidate_record(
        row["index"],
        0,
        p,
        micro,
        result,
        mode,
    )

    refined["nphase"] = nphase

    return refined


def reconstruct_024e_spherical(
    previous: dict,
    table: dict,
) -> dict:
    """Regression against the 024E selected minimum-required-g case."""

    old = previous["min_required_g"]

    n2_index = int(
        np.argmin(
            np.abs(
                EXPONENTS
                -
                2.0
            )
        )
    )

    n = EXPONENTS[n2_index]

    rhalf = table["rhalf"][
        n2_index
    ]

    a = float(
        old["a"]
    )

    d0 = float(
        old["d0"]
    )

    core_gap = (
        d0
        /
        (
            2.0
            * rhalf
            * a
        )
    )

    p = {
        "R":
            np.asarray(
                [
                    old["R"]
                ]
            ),

        "ax":
            np.asarray([a]),

        "ay":
            np.asarray([a]),

        "az":
            np.asarray([a]),

        "ay_ratio":
            np.asarray([1.0]),

        "az_ratio":
            np.asarray([1.0]),

        "clearance":
            np.asarray(
                [
                    old["clear"]
                ]
            ),

        "core_gap_factor":
            np.asarray(
                [
                    core_gap
                ]
            ),

        "d0":
            np.asarray([d0]),

        "beta":
            np.asarray(
                [
                    old["beta"]
                ]
            ),

        "m":
            np.asarray(
                [
                    old["m"]
                ]
            ),

        "omega_ratio":
            np.asarray(
                [
                    old["om"]
                ]
            ),

        "omega":
            np.asarray(
                [
                    old["omega"]
                ]
            ),

        "lag":
            np.asarray(
                [
                    old["lag"]
                ]
            ),

        "guide_multiplier":
            np.asarray(
                [
                    old["gm"]
                ]
            ),

        "exponent_index":
            np.asarray(
                [
                    n2_index
                ],
                dtype=int,
            ),

        "exponent":
            np.asarray([n]),
    }

    micro = microphysics(
        p,
        table,
    )

    mode = MODES[0]

    result = evaluate_mode(
        p,
        micro,
        table,
        mode,
        NMED,
    )

    g_new = float(
        result[
            "g006d_actual"
        ][0]
    )

    g_old = float(
        old["g6"]
    )

    return {
        "old_g006d":
            g_old,

        "rebuilt_g006d":
            g_new,

        "relative_error":
            relerr(
                g_old,
                g_new,
            ),
    }


def uniform_ball_sobol(
    n: int,
) -> np.ndarray:
    """Deterministic quasi-uniform points in the unit ball."""

    power = int(
        math.ceil(
            math.log2(
                max(
                    n,
                    2,
                )
            )
        )
    )

    raw = qmc.Sobol(
        d=3,
        scramble=True,
        seed=240599,
    ).random_base2(
        power
    )[:n]

    radius = (
        raw[:, 0]
        ** (1.0 / 3.0)
    )

    cos_theta = (
        2.0
        * raw[:, 1]
        -
        1.0
    )

    sin_theta = np.sqrt(
        np.maximum(
            0.0,
            1.0
            -
            cos_theta
            * cos_theta
        )
    )

    phi = (
        2.0
        * math.pi
        * raw[:, 2]
    )

    return np.column_stack(
        (
            radius
            * sin_theta
            * np.cos(phi),

            radius
            * sin_theta
            * np.sin(phi),

            radius
            * cos_theta,
        )
    )


def independent_cubature(
    row: dict,
    table: dict,
) -> dict:
    """Independent finite-volume packet + portal reconstruction."""

    points = uniform_ball_sobol(
        CUB_POINTS
    )

    n = float(
        row["exponent"]
    )

    ax = float(
        row["ax"]
    )

    ay = float(
        row["ay"]
    )

    az = float(
        row["az"]
    )

    Vscale = (
        ax
        * ay
        * az
    )

    Vball = (
        4.0
        * math.pi
        / 3.0
        *
        Vscale
    )

    qsq = np.sum(
        points * points,
        axis=1,
    )

    f1sq = (
        np.maximum(
            1.0
            -
            qsq,
            0.0,
        )
        ** (2.0 * n)
    )

    coords = np.column_stack(
        (
            ax * points[:, 0],
            ay * points[:, 1],
            az * points[:, 2],
        )
    )

    phase = np.linspace(
        0.0,
        2.0 * math.pi,
        CUB_PHASE,
        endpoint=False,
    )

    R = float(
        row["R"]
    )

    d0 = float(
        row["d0"]
    )

    cc = (
        R
        +
        0.5 * d0
    )

    lag = float(
        row["lag"]
    )

    if (
        row["direction_class"]
        ==
        "PARALLEL_AT_THROAT"
    ):

        theta_left = phase
        theta_right = (
            math.pi
            -
            phase
            +
            lag
        )

    else:

        theta_left = phase
        theta_right = (
            math.pi
            +
            phase
            +
            lag
        )

    zc = -(
        az
        +
        float(
            row["clearance"]
        )
    )

    A2 = float(
        row["A2"]
    )

    portal_phase = np.zeros(
        CUB_PHASE,
        dtype=float,
    )

    portal_k_phase = np.zeros(
        CUB_PHASE,
        dtype=float,
    )

    baseline_k_left_num = 0.0
    baseline_k_right_num = 0.0
    baseline_weight = 0.0

    chunk = 64

    for start in range(
        0,
        CUB_PHASE,
        chunk,
    ):

        stop = min(
            start + chunk,
            CUB_PHASE,
        )

        tl = theta_left[
            start:stop
        ]

        tr = theta_right[
            start:stop
        ]

        xl = (
            -cc
            +
            R * np.cos(tl)
        )

        yl = (
            R * np.sin(tl)
        )

        xr = (
            +cc
            +
            R * np.cos(tr)
        )

        yr = (
            R * np.sin(tr)
        )

        for local in range(
            stop - start
        ):

            left_center = np.asarray(
                [
                    xl[local],
                    yl[local],
                    zc,
                ]
            )

            right_center = np.asarray(
                [
                    xr[local],
                    yr[local],
                    zc,
                ]
            )

            physical_left = (
                left_center[None, :]
                +
                coords
            )

            physical_right = (
                right_center[None, :]
                +
                coords
            )

            # Baseline finite-volume kernel.
            for physical, side in (
                (
                    physical_left,
                    "L",
                ),
                (
                    physical_right,
                    "R",
                ),
            ):

                dzp = (
                    1.0
                    -
                    physical[:, 2]
                )

                kval = (
                    dzp
                    /
                    (
                        physical[:, 0] ** 2
                        +
                        physical[:, 1] ** 2
                        +
                        dzp ** 2
                    ) ** 1.5
                )

                num = float(
                    np.sum(
                        f1sq
                        * kval
                    )
                )

                if side == "L":
                    baseline_k_left_num += num
                else:
                    baseline_k_right_num += num

            baseline_weight += float(
                np.sum(
                    f1sq
                )
            )

            # Portal: integrate using points inside left ellipsoid.
            delta_right = (
                physical_left
                -
                right_center[None, :]
            )

            q2_right = (
                (
                    delta_right[:, 0]
                    / ax
                ) ** 2
                +
                (
                    delta_right[:, 1]
                    / ay
                ) ** 2
                +
                (
                    delta_right[:, 2]
                    / az
                ) ** 2
            )

            f2sq = (
                np.maximum(
                    1.0
                    -
                    q2_right,
                    0.0,
                )
                ** (2.0 * n)
            )

            portal_weight = (
                f1sq
                * f2sq
            )

            portal_integral = (
                A2 ** 2
                *
                Vball
                *
                float(
                    np.mean(
                        portal_weight
                    )
                )
            )

            portal_phase[
                start + local
            ] = portal_integral

            if portal_integral > 0.0:

                dzp = (
                    1.0
                    -
                    physical_left[:, 2]
                )

                kval = (
                    dzp
                    /
                    (
                        physical_left[:, 0] ** 2
                        +
                        physical_left[:, 1] ** 2
                        +
                        dzp ** 2
                    ) ** 1.5
                )

                portal_k_phase[
                    start + local
                ] = (
                    A2 ** 2
                    *
                    Vball
                    *
                    float(
                        np.mean(
                            portal_weight
                            * kval
                        )
                    )
                )

    Kg_volume = (
        0.5
        * (
            baseline_k_left_num
            +
            baseline_k_right_num
        )
        /
        max(
            baseline_weight,
            1.0e-300,
        )
    )

    ua = float(
        np.mean(
            portal_phase
        )
    )

    u1 = float(
        np.max(
            portal_phase
        )
    )

    uk = float(
        np.mean(
            portal_k_phase
        )
    )

    KU = (
        uk
        /
        max(
            ua,
            1.0e-300,
        )
    )

    _, Ko_arr = ring_kernels(
        np.asarray([R]),
        np.asarray([d0]),
        np.asarray([zc]),
        CUB_PHASE,
    )

    Kg_line_arr, _ = ring_kernels(
        np.asarray([R]),
        np.asarray([d0]),
        np.asarray([zc]),
        CUB_PHASE,
    )

    Ko = float(
        Ko_arr[0]
    )

    Kg_line = float(
        Kg_line_arr[0]
    )

    Em = float(
        row["Em"]
    )

    Eextra = float(
        row["Eextra"]
    )

    Eg = float(
        row["Eg"]
    )

    srest = float(
        row["srest"]
    )

    gcap = min(
        GMAX,
        DISTORT
        * Em
        /
        max(
            u1,
            1.0e-300,
        ),
    )

    Upeak = (
        gcap
        * u1
    )

    inventory = (
        Em
        +
        Eg
        +
        Upeak
    )

    baseline = (
        Em
        * max(
            1.0,
            srest,
        )
        * Kg_volume
        +
        Eextra
        * Kg_line
    )

    gain = (
        2.0
        * gcap
        * ua
        * max(
            KU
            -
            Ko,
            0.0,
        )
    )

    A = (
        -baseline
        +
        gain
    )

    C = (
        inventory
        / A
        if A > 0.0
        else math.inf
    )

    return {
        "Kg_volume":
            Kg_volume,

        "Kg_line":
            Kg_line,

        "Ko":
            Ko,

        "KU":
            KU,

        "ua":
            ua,

        "u1":
            u1,

        "gcap":
            gcap,

        "Upeak":
            Upeak,

        "inventory":
            inventory,

        "baseline":
            baseline,

        "gain":
            gain,

        "A":
            A,

        "C":
            C,

        "overlap_ua_relative_error":
            relerr(
                ua,
                float(
                    row["ua"]
                ),
            ),

        "overlap_KU_relative_error":
            relerr(
                KU,
                float(
                    row["KU"]
                ),
            ),

        "C_relative_error":
            (
                relerr(
                    C,
                    float(
                        row["C_actual_outer"]
                    ),
                )
                if (
                    math.isfinite(C)
                    and
                    math.isfinite(
                        float(
                            row["C_actual_outer"]
                        )
                    )
                )
                else math.inf
            ),
    }


def main() -> None:
    """Execute 024E1."""

    print(
        "=== 024E1 TEACHER-GUIDED ANISOTROPIC CLOSE-PASS RESCUE ===",
        flush=True,
    )

    require(PREV_E)
    require(PREV_D)

    previous_e = json.loads(
        PREV_E.read_text(
            encoding="utf-8"
        )
    )

    previous_d = json.loads(
        PREV_D.read_text(
            encoding="utf-8"
        )
    )

    if (
        previous_e["decision"]["result"]
        !=
        "RED_DUAL_TOROID_CLOSE_PASS_PORTAL_NO_STRICT_006D_ADVANCE"
    ):
        raise RuntimeError(
            "Unexpected 024E predecessor state"
        )

    print(
        "\n=== A — SCIENTIFIC ANCHORS ==="
    )

    print(
        f"C_006D="
        f"{C006D:.15e}"
    )

    print(
        f"C_024D1R="
        f"{C024D1R:.15e}"
    )

    print(
        f"C_024D_SCALAR="
        f"{C024D:.15e}"
    )

    print(
        f"TEACHER_PRODUCTIVE_ENERGY_REFERENCE="
        f"{TEACHER_PRODUCTIVE_REFERENCE:.15e}"
    )

    print(
        f"TEACHER_GROSS_OUTWARD_SHARE_REFERENCE="
        f"{TEACHER_GROSS_SHARE_REFERENCE:.15e}"
    )

    print(
        f"TEACHER_CANCELLATION_REFERENCE="
        f"{TEACHER_CANCELLATION_REFERENCE:.15e}"
    )

    print(
        "PORTAL_NEGATIVE_ACTIVE_DEC_RATIO="
        "MINUS_S_OVER_RHO_EQUALS_2"
    )

    print(
        "LOCAL_NEGATIVE_ACTIVE_CONSTITUTIVE_HEADROOM_LEFT="
        "NONE_WITHIN_TYPE_I_DEC"
    )

    print(
        "PRIMARY_REMAINING_LEVER="
        "PARTICIPATION_PLUS_KERNEL_PLACEMENT"
    )

    print(
        "ENERGY_COLLIDER_MODEL=NO"
    )

    print(
        "STRICT_HALF_AMPLITUDE_CORE_OVERLAP=FORBIDDEN"
    )

    print(
        "LOW_AMPLITUDE_FIELD_SUPPORT_OVERLAP=ALLOWED"
    )

    print(
        "LAB_LOCKED_ANISOTROPIC_SHAPE="
        "OPTIMISTIC_PREFILTER_NOT_FIELD_REALIZATION"
    )

    table = profile_tables()

    print(
        "\n=== B — PROFILE TABLES ==="
    )

    for i, n in enumerate(EXPONENTS):

        print(
            f"PROFILE_N={n:.6f} "
            f"C2={table['c2'][i]:.12e} "
            f"CG_AXIS={table['cg_axis'][i]:.12e} "
            f"R_HALF={table['rhalf'][i]:.12e}"
        )

    print(
        "\n=== C — 024E SPHERICAL REGRESSION ==="
    )

    regression = reconstruct_024e_spherical(
        previous_e,
        table,
    )

    print(
        f"SPHERICAL_024E_OLD_G006D="
        f"{regression['old_g006d']:.15e}"
    )

    print(
        f"SPHERICAL_024E_REBUILT_G006D="
        f"{regression['rebuilt_g006d']:.15e}"
    )

    print(
        f"SPHERICAL_024E_G006D_RELERR="
        f"{regression['relative_error']:.15e}"
    )

    regression_pass = bool(
        regression[
            "relative_error"
        ]
        <=
        2.0e-2
    )

    print(
        "SPHERICAL_024E_REGRESSION="
        +
        (
            "PASS"
            if regression_pass
            else "FAIL"
        )
    )

    if not regression_pass:
        raise RuntimeError(
            "024E spherical regression failed"
        )

    print(
        "\n=== D — BUILD 2^19 MORPHOLOGY CAMPAIGN ==="
    )

    p_all = build_parameters(
        table
    )

    micro_all = microphysics(
        p_all,
        table,
    )

    print(
        f"BASE_SOBOL_CASES="
        f"{NCASE}"
    )

    print(
        f"TOTAL_KINEMATIC_CASES="
        f"{2 * NCASE}"
    )

    pools = {
        "actual":
            [],

        "ceiling":
            [],

        "gactual":
            [],

        "gceiling":
            [],

        "participation":
            [],
    }

    counts = {
        mode[0]: {
            "strict":
                0,

            "loose":
                0,

            "strict_actual_positive":
                0,

            "strict_actual_beats_006D":
                0,

            "strict_ceiling_positive":
                0,

            "strict_ceiling_beats_006D":
                0,

            "loose_actual_beats_006D":
                0,
        }
        for mode in MODES
    }

    max_strict_peak_participation = 0.0
    max_strict_cycle_participation = 0.0

    for start in range(
        0,
        NCASE,
        BATCH,
    ):

        stop = min(
            start + BATCH,
            NCASE,
        )

        if (
            start
            %
            (
                BATCH * 80
            )
            ==
            0
        ):

            print(
                f"SCAN_PROGRESS="
                f"{start}/{NCASE}",
                flush=True,
            )

        sl = slice(
            start,
            stop,
        )

        p = slice_dict(
            p_all,
            sl,
        )

        micro = slice_dict(
            micro_all,
            sl,
        )

        for mode in MODES:

            result = evaluate_mode(
                p,
                micro,
                table,
                mode,
                NPHASE,
            )

            strict = result[
                "strict"
            ]

            loose = result[
                "loose"
            ]

            c = counts[
                mode[0]
            ]

            c["strict"] += int(
                np.count_nonzero(
                    strict
                )
            )

            c["loose"] += int(
                np.count_nonzero(
                    loose
                )
            )

            c[
                "strict_actual_positive"
            ] += int(
                np.count_nonzero(
                    strict
                    &
                    np.isfinite(
                        result[
                            "C_actual_outer"
                        ]
                    )
                )
            )

            c[
                "strict_actual_beats_006D"
            ] += int(
                np.count_nonzero(
                    strict
                    &
                    (
                        result[
                            "C_actual_outer"
                        ]
                        <
                        C006D
                    )
                )
            )

            c[
                "strict_ceiling_positive"
            ] += int(
                np.count_nonzero(
                    strict
                    &
                    np.isfinite(
                        result[
                            "C_teacher_ceiling"
                        ]
                    )
                )
            )

            c[
                "strict_ceiling_beats_006D"
            ] += int(
                np.count_nonzero(
                    strict
                    &
                    (
                        result[
                            "C_teacher_ceiling"
                        ]
                        <
                        C006D
                    )
                )
            )

            c[
                "loose_actual_beats_006D"
            ] += int(
                np.count_nonzero(
                    loose
                    &
                    ~strict
                    &
                    (
                        result[
                            "C_actual_outer"
                        ]
                        <
                        C006D
                    )
                )
            )

            if np.any(strict):

                max_strict_peak_participation = max(
                    max_strict_peak_participation,
                    float(
                        np.max(
                            result[
                                "peak_participation"
                            ][strict]
                        )
                    ),
                )

                max_strict_cycle_participation = max(
                    max_strict_cycle_participation,
                    float(
                        np.max(
                            result[
                                "cycle_participation"
                            ][strict]
                        )
                    ),
                )

            selection_specs = (
                (
                    "actual",
                    "C_actual_outer",
                    strict,
                    False,
                ),
                (
                    "ceiling",
                    "C_teacher_ceiling",
                    strict,
                    False,
                ),
                (
                    "gactual",
                    "g006d_actual",
                    strict,
                    False,
                ),
                (
                    "gceiling",
                    "g006d_teacher",
                    strict,
                    False,
                ),
                (
                    "participation",
                    "peak_participation",
                    strict,
                    True,
                ),
            )

            for (
                pool_name,
                key,
                mask,
                reverse,
            ) in selection_specs:

                ids = np.flatnonzero(
                    mask
                    &
                    np.isfinite(
                        result[key]
                    )
                )

                if len(ids) == 0:
                    continue

                local_count = min(
                    10,
                    len(ids),
                )

                vals = result[key][ids]

                if reverse:

                    if len(ids) > local_count:
                        choose = np.argpartition(
                            -vals,
                            local_count - 1,
                        )[:local_count]
                    else:
                        choose = np.arange(
                            len(ids)
                        )

                    selected = ids[choose]

                    candidates = [
                        candidate_record(
                            start + int(j),
                            int(j),
                            p,
                            micro,
                            result,
                            mode,
                        )
                        for j in selected
                    ]

                    pools[
                        pool_name
                    ].extend(
                        candidates
                    )

                    pools[
                        pool_name
                    ].sort(
                        key=lambda row:
                            -row[key]
                    )

                    del pools[
                        pool_name
                    ][TOP_KEEP:]

                else:

                    if len(ids) > local_count:
                        choose = np.argpartition(
                            vals,
                            local_count - 1,
                        )[:local_count]
                    else:
                        choose = np.arange(
                            len(ids)
                        )

                    selected = ids[choose]

                    keep_best(
                        pools[
                            pool_name
                        ],
                        [
                            candidate_record(
                                start + int(j),
                                int(j),
                                p,
                                micro,
                                result,
                                mode,
                            )
                            for j in selected
                        ],
                        key,
                    )

    print(
        "\n=== E — COARSE COUNTS ==="
    )

    for mode in MODES:

        name = mode[0]

        for key, value in counts[name].items():

            print(
                f"{name}_{key.upper()}="
                f"{value}"
            )

    print(
        f"MAX_STRICT_PEAK_PORTAL_PARTICIPATION="
        f"{max_strict_peak_participation:.15e}"
    )

    print(
        f"MAX_STRICT_CYCLE_PORTAL_PARTICIPATION="
        f"{max_strict_cycle_participation:.15e}"
    )

    print(
        f"PARTICIPATION_FACTOR_VS_024E_BEST="
        f"{max_strict_peak_participation / 0.006241800831483099:.15e}"
    )

    print(
        f"PARTICIPATION_RATIO_VS_TEACHER_REFERENCE="
        f"{max_strict_peak_participation / TEACHER_PRODUCTIVE_REFERENCE:.15e}"
    )

    merged = {}

    for pool in pools.values():

        for row in pool:

            merged[
                (
                    row["index"],
                    row["direction_class"],
                )
            ] = row

    candidates = list(
        merged.values()
    )

    print(
        f"REFINEMENT_CANDIDATES="
        f"{len(candidates)}"
    )

    refined = []

    print(
        "\n=== F — MEDIUM/HIGH REFINEMENT ===",
        flush=True,
    )

    for i, row in enumerate(candidates):

        if i % 30 == 0:

            print(
                f"REFINEMENT_PROGRESS="
                f"{i}/{len(candidates)}",
                flush=True,
            )

        medium = refine_one(
            row,
            table,
            NMED,
        )

        high = refine_one(
            row,
            table,
            NHIGH,
        )

        high[
            "C_actual_outer_medium"
        ] = medium[
            "C_actual_outer"
        ]

        high[
            "C_teacher_ceiling_medium"
        ] = medium[
            "C_teacher_ceiling"
        ]

        if (
            math.isfinite(
                high[
                    "C_actual_outer"
                ]
            )
            and
            math.isfinite(
                medium[
                    "C_actual_outer"
                ]
            )
        ):

            high[
                "actual_medium_high_relerr"
            ] = relerr(
                high[
                    "C_actual_outer"
                ],
                medium[
                    "C_actual_outer"
                ],
            )

        else:

            high[
                "actual_medium_high_relerr"
            ] = math.inf

        if (
            math.isfinite(
                high[
                    "C_teacher_ceiling"
                ]
            )
            and
            math.isfinite(
                medium[
                    "C_teacher_ceiling"
                ]
            )
        ):

            high[
                "ceiling_medium_high_relerr"
            ] = relerr(
                high[
                    "C_teacher_ceiling"
                ],
                medium[
                    "C_teacher_ceiling"
                ],
            )

        else:

            high[
                "ceiling_medium_high_relerr"
            ] = math.inf

        refined.append(
            high
        )

    strict_rows = [
        row
        for row in refined
        if row["strict"]
    ]

    loose_only_rows = [
        row
        for row in refined
        if (
            row["loose"]
            and
            not row["strict"]
        )
    ]

    actual_rows = sorted(
        [
            row
            for row in strict_rows
            if math.isfinite(
                row[
                    "C_actual_outer"
                ]
            )
        ],
        key=lambda row:
            row[
                "C_actual_outer"
            ],
    )

    ceiling_rows = sorted(
        [
            row
            for row in strict_rows
            if math.isfinite(
                row[
                    "C_teacher_ceiling"
                ]
            )
        ],
        key=lambda row:
            row[
                "C_teacher_ceiling"
            ],
    )

    g_actual_rows = sorted(
        [
            row
            for row in strict_rows
            if math.isfinite(
                row[
                    "g006d_actual"
                ]
            )
        ],
        key=lambda row:
            row[
                "g006d_actual"
            ],
    )

    g_ceiling_rows = sorted(
        [
            row
            for row in strict_rows
            if math.isfinite(
                row[
                    "g006d_teacher"
                ]
            )
        ],
        key=lambda row:
            row[
                "g006d_teacher"
            ],
    )

    loose_rows = sorted(
        [
            row
            for row in loose_only_rows
            if math.isfinite(
                row[
                    "C_actual_outer"
                ]
            )
        ],
        key=lambda row:
            row[
                "C_actual_outer"
            ],
    )

    best_actual = (
        actual_rows[0]
        if actual_rows
        else None
    )

    best_ceiling = (
        ceiling_rows[0]
        if ceiling_rows
        else None
    )

    min_g_actual = (
        g_actual_rows[0]
        if g_actual_rows
        else None
    )

    min_g_ceiling = (
        g_ceiling_rows[0]
        if g_ceiling_rows
        else None
    )

    best_loose = (
        loose_rows[0]
        if loose_rows
        else None
    )

    def show(
        tag: str,
        row: dict | None,
        key: str,
    ) -> None:

        if row is None:

            print(
                f"{tag}_SURVIVOR=NO"
            )

            return

        print(
            f"{tag}_SURVIVOR=YES"
        )

        print(
            f"{tag}_{key.upper()}="
            f"{row[key]:.15e}"
        )

        for field in (
            "direction_class",
            "R",
            "ax",
            "ay",
            "az",
            "ay_ratio",
            "az_ratio",
            "clearance",
            "core_gap_factor",
            "d0",
            "exponent",
            "beta",
            "m",
            "omega_ratio",
            "guide_multiplier",
            "gcap",
            "peak_participation",
            "cycle_participation",
            "overlap_duty",
            "KU",
            "Kg",
            "Ko",
            "cancellation_actual",
            "g006d_actual",
            "g006d_teacher",
            "g19_actual",
            "g66_actual",
            "actual_medium_high_relerr",
            "ceiling_medium_high_relerr",
        ):

            if field not in row:
                continue

            value = row[field]

            if isinstance(
                value,
                str,
            ):

                print(
                    f"{tag}_{field.upper()}="
                    f"{value}"
                )

            else:

                print(
                    f"{tag}_{field.upper()}="
                    f"{float(value):.15e}"
                )

    print(
        "\n=== G — BEST REFINED RESULTS ==="
    )

    show(
        "BEST_STRICT_ACTUAL",
        best_actual,
        "C_actual_outer",
    )

    show(
        "BEST_STRICT_TEACHER_CEILING",
        best_ceiling,
        "C_teacher_ceiling",
    )

    show(
        "MIN_STRICT_G_ACTUAL",
        min_g_actual,
        "g006d_actual",
    )

    show(
        "MIN_STRICT_G_TEACHER_CEILING",
        min_g_ceiling,
        "g006d_teacher",
    )

    show(
        "BEST_LOOSE_CORE_OVERLAP",
        best_loose,
        "C_actual_outer",
    )

    # ------------------------------------------------------------
    # H. Independent cubature.
    # ------------------------------------------------------------

    print(
        "\n=== H — INDEPENDENT 4-D FINITE-VOLUME CUBATURE ===",
        flush=True,
    )

    independent_seed = (
        best_actual
        or
        min_g_actual
        or
        best_ceiling
        or
        min_g_ceiling
    )

    independent = None

    if independent_seed is not None:

        independent = independent_cubature(
            independent_seed,
            table,
        )

        print(
            f"INDEPENDENT_SEED_DIRECTION="
            f"{independent_seed['direction_class']}"
        )

        print(
            f"INDEPENDENT_SEED_EXPONENT="
            f"{independent_seed['exponent']:.8f}"
        )

        for key in (
            "Kg_volume",
            "Kg_line",
            "Ko",
            "KU",
            "ua",
            "u1",
            "gcap",
            "Upeak",
            "inventory",
            "baseline",
            "gain",
            "A",
            "C",
            "overlap_ua_relative_error",
            "overlap_KU_relative_error",
            "C_relative_error",
        ):

            print(
                f"INDEPENDENT_{key.upper()}="
                f"{float(independent[key]):.15e}"
            )

        overlap_pass = bool(
            independent[
                "overlap_ua_relative_error"
            ]
            <=
            5.0e-2
        )

        kernel_pass = bool(
            independent[
                "overlap_KU_relative_error"
            ]
            <=
            5.0e-2
        )

        coefficient_pass = bool(
            (
                not math.isfinite(
                    independent[
                        "C"
                    ]
                )
            )
            or
            (
                not math.isfinite(
                    independent_seed[
                        "C_actual_outer"
                    ]
                )
            )
            or
            independent[
                "C_relative_error"
            ]
            <=
            0.10
        )

        independent_pass = bool(
            overlap_pass
            and
            kernel_pass
            and
            coefficient_pass
        )

        print(
            "INDEPENDENT_CUBATURE="
            +
            (
                "PASS"
                if independent_pass
                else "FAIL"
            )
        )

    else:

        independent_pass = False

        print(
            "INDEPENDENT_CUBATURE="
            "NOT_RUN_NO_CANDIDATE"
        )

    # ------------------------------------------------------------
    # I. Shape-family summary.
    # ------------------------------------------------------------

    shape_rows = []

    print(
        "\n=== I — PROFILE-EXPONENT SUMMARY ==="
    )

    for exponent in EXPONENTS:

        local_actual = [
            row
            for row in strict_rows
            if (
                abs(
                    row["exponent"]
                    -
                    exponent
                )
                <
                1.0e-12
                and
                math.isfinite(
                    row[
                        "C_actual_outer"
                    ]
                )
            )
        ]

        local_ceiling = [
            row
            for row in strict_rows
            if (
                abs(
                    row["exponent"]
                    -
                    exponent
                )
                <
                1.0e-12
                and
                math.isfinite(
                    row[
                        "C_teacher_ceiling"
                    ]
                )
            )
        ]

        best_a = (
            min(
                local_actual,
                key=lambda row:
                    row[
                        "C_actual_outer"
                    ],
            )
            if local_actual
            else None
        )

        best_c = (
            min(
                local_ceiling,
                key=lambda row:
                    row[
                        "C_teacher_ceiling"
                    ],
            )
            if local_ceiling
            else None
        )

        actual_c = (
            best_a[
                "C_actual_outer"
            ]
            if best_a
            else math.inf
        )

        ceiling_c = (
            best_c[
                "C_teacher_ceiling"
            ]
            if best_c
            else math.inf
        )

        shape_rows.append({
            "exponent":
                float(
                    exponent
                ),

            "best_actual_C":
                actual_c,

            "best_teacher_ceiling_C":
                ceiling_c,
        })

        print(
            f"PROFILE_EXPONENT={exponent:.6f} "
            f"BEST_ACTUAL_C={actual_c:.12e} "
            f"BEST_CEILING_C={ceiling_c:.12e}"
        )

    # ------------------------------------------------------------
    # J. Decision.
    # ------------------------------------------------------------

    print(
        "\n=== J — 024E1 DECISION ==="
    )

    strict_actual_beats_006d = bool(
        best_actual is not None
        and
        best_actual[
            "C_actual_outer"
        ]
        <
        C006D
    )

    strict_actual_beats_024d1r = bool(
        best_actual is not None
        and
        best_actual[
            "C_actual_outer"
        ]
        <
        C024D1R
    )

    strict_actual_beats_024d = bool(
        best_actual is not None
        and
        best_actual[
            "C_actual_outer"
        ]
        <
        C024D
    )

    ceiling_beats_006d = bool(
        best_ceiling is not None
        and
        best_ceiling[
            "C_teacher_ceiling"
        ]
        <
        C006D
    )

    ceiling_beats_024d1r = bool(
        best_ceiling is not None
        and
        best_ceiling[
            "C_teacher_ceiling"
        ]
        <
        C024D1R
    )

    loose_beats_006d = bool(
        best_loose is not None
        and
        best_loose[
            "C_actual_outer"
        ]
        <
        C006D
    )

    teacher_like_participation = bool(
        max_strict_peak_participation
        >=
        0.10
    )

    if (
        strict_actual_beats_006d
        and
        independent_pass
    ):

        decision = (
            "YELLOW_STRICT_NONCOLLIDING_ANISOTROPIC_"
            "CLOSE_PASS_SURVIVOR"
        )

        next_action = (
            "024E2_DERIVE_ORIENTATION_DYNAMICS_AND_"
            "FULL_LOCAL_TWO_SCALAR_FIELD_EQUATIONS"
        )

        interpretation = (
            "MORPHOLOGY_RAISES_PORTAL_PARTICIPATION_ENOUGH_"
            "TO_REOPEN_MICROSCOPIC_CLOSE_PASS_GATE"
        )

    elif (
        ceiling_beats_006d
        and
        not strict_actual_beats_006d
    ):

        decision = (
            "RED_ACTUAL_CLOSE_PASS_BUT_YELLOW_TEACHER_ROUTING_CEILING"
        )

        next_action = (
            "CLOSE_CLOSE_PASS_PORTAL_AND_RETURN_TO_024D2_"
            "BECAUSE_STRESS_ROUTING_NOT_PROXIMITY_IS_THE_DRIVER"
        )

        interpretation = (
            "PROFILE_SHAPING_HELPS_BUT_ORBITAL_BASELINE_"
            "POSITIVE_ENERGY_ERASES_THE_GAIN"
        )

    elif (
        loose_beats_006d
        and
        not strict_actual_beats_006d
    ):

        decision = (
            "RED_REQUESTED_NONCOLLIDER_ONLY_CORE_OVERLAP_CASES_SURVIVE"
        )

        next_action = (
            "CLOSE_024E1_AND_RETURN_TO_024D2_"
            "MINIMAL_POLOIDAL_SCALAR_TRANSPORT_PREFLIGHT"
        )

        interpretation = (
            "USEFUL_PORTAL_REQUIRES_COLLISION_LIKE_DENSE_CORE_OVERLAP"
        )

    else:

        decision = (
            "RED_TEACHER_GUIDED_ANISOTROPIC_CLOSE_PASS_"
            "NO_STRICT_006D_ADVANCE"
        )

        next_action = (
            "CLOSE_024E_AND_024E1_PER_STOP_RULE_"
            "RETURN_TO_024D2_MINIMAL_POLOIDAL_SCALAR_TRANSPORT_PREFLIGHT"
        )

        interpretation = (
            "EVEN_INTROSPECTIVE_GUIDED_PROFILE_SHAPING_"
            "DOES_NOT_RESCUE_PERTURBATIVE_CLOSE_PASS_PORTAL"
        )

    print(
        "STRICT_ACTUAL_BEATS_006D="
        +
        (
            "YES"
            if strict_actual_beats_006d
            else "NO"
        )
    )

    print(
        "STRICT_ACTUAL_BEATS_024D1R="
        +
        (
            "YES"
            if strict_actual_beats_024d1r
            else "NO"
        )
    )

    print(
        "STRICT_ACTUAL_BEATS_024D_SCALAR="
        +
        (
            "YES"
            if strict_actual_beats_024d
            else "NO"
        )
    )

    print(
        "STRICT_TEACHER_ROUTING_CEILING_BEATS_006D="
        +
        (
            "YES"
            if ceiling_beats_006d
            else "NO"
        )
    )

    print(
        "STRICT_TEACHER_ROUTING_CEILING_BEATS_024D1R="
        +
        (
            "YES"
            if ceiling_beats_024d1r
            else "NO"
        )
    )

    print(
        "LOOSE_CORE_OVERLAP_BEATS_006D="
        +
        (
            "YES"
            if loose_beats_006d
            else "NO"
        )
    )

    print(
        "TEACHER_LIKE_GE10PCT_PEAK_PARTICIPATION="
        +
        (
            "YES"
            if teacher_like_participation
            else "NO"
        )
    )

    print(
        f"024E1_INTERPRETATION="
        f"{interpretation}"
    )

    print(
        f"024E1_DECISION="
        f"{decision}"
    )

    print(
        f"NEXT="
        f"{next_action}"
    )

    print(
        "MICROSCOPIC_ANISOTROPIC_PACKET_FIELD=NO"
    )

    print(
        "SHAPE_ORIENTATION_DYNAMICS=NOT_ESTABLISHED"
    )

    print(
        "FULL_LOCAL_DYNAMIC_TMUNU_CONSERVATION=NOT_ESTABLISHED"
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
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "70_TO_71_PERCENT_RETAIN_UNLESS_LATER_MICROSCOPIC_PROMOTION_IS_EARNED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    # ------------------------------------------------------------
    # K. Persist artifacts.
    # ------------------------------------------------------------

    clean_rows = []

    for row in refined:

        clean = {
            key: value
            for key, value in row.items()
            if isinstance(
                value,
                (
                    int,
                    float,
                    bool,
                    str,
                    np.integer,
                    np.floating,
                    np.bool_,
                ),
            )
        }

        clean_rows.append(clean)

    if clean_rows:

        fields = sorted({
            key
            for row in clean_rows
            for key in row.keys()
        })

        with OUTC.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
                extrasaction="ignore",
            )

            writer.writeheader()

            writer.writerows(
                clean_rows
            )

    with OUTS.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "exponent",
                "best_actual_C",
                "best_teacher_ceiling_C",
            ],
        )

        writer.writeheader()

        writer.writerows(
            shape_rows
        )

    if independent_seed is not None:

        np.savez_compressed(
            OUTN,
            exponents=EXPONENTS,
            c2=table["c2"],
            cg_axis=table["cg_axis"],
            rhalf=table["rhalf"],
            separation_grid=table["sgrid"],
            overlap_tables=table["overlap"],
            best_parameters=np.asarray(
                [
                    independent_seed["R"],
                    independent_seed["ax"],
                    independent_seed["ay"],
                    independent_seed["az"],
                    independent_seed["clearance"],
                    independent_seed["d0"],
                    independent_seed["beta"],
                    independent_seed["m"],
                    independent_seed["omega_ratio"],
                    independent_seed["guide_multiplier"],
                    independent_seed["exponent"],
                ],
                dtype=float,
            ),
        )

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_TEACHER_GUIDED_"
                "ANISOTROPIC_CLOSE_PASS_PORTAL_PREFILTER"
            ),

        "anchors": {
            "C_006D":
                C006D,

            "C_024D1R":
                C024D1R,

            "C_024D":
                C024D,

            "teacher_productive_reference":
                TEACHER_PRODUCTIVE_REFERENCE,

            "teacher_gross_share_reference":
                TEACHER_GROSS_SHARE_REFERENCE,

            "teacher_cancellation_reference":
                TEACHER_CANCELLATION_REFERENCE,
        },

        "regression":
            regression,

        "scan": {
            "sobol_cases":
                NCASE,

            "kinematic_cases":
                2 * NCASE,

            "coarse_phase":
                NPHASE,

            "medium_phase":
                NMED,

            "high_phase":
                NHIGH,

            "cubature_phase":
                CUB_PHASE,

            "cubature_internal_points":
                CUB_POINTS,

            "exponents":
                [
                    float(x)
                    for x in EXPONENTS
                ],
        },

        "counts":
            counts,

        "participation": {
            "max_strict_peak":
                max_strict_peak_participation,

            "max_strict_cycle":
                max_strict_cycle_participation,

            "factor_vs_024E_best_peak":
                (
                    max_strict_peak_participation
                    /
                    0.006241800831483099
                ),

            "ratio_vs_teacher_reference":
                (
                    max_strict_peak_participation
                    /
                    TEACHER_PRODUCTIVE_REFERENCE
                ),
        },

        "best_strict_actual":
            best_actual,

        "best_strict_teacher_ceiling":
            best_ceiling,

        "min_strict_g_actual":
            min_g_actual,

        "min_strict_g_teacher_ceiling":
            min_g_ceiling,

        "best_loose":
            best_loose,

        "independent":
            independent,

        "decision": {
            "strict_actual_beats_006D":
                strict_actual_beats_006d,

            "strict_actual_beats_024D1R":
                strict_actual_beats_024d1r,

            "strict_actual_beats_024D":
                strict_actual_beats_024d,

            "teacher_ceiling_beats_006D":
                ceiling_beats_006d,

            "teacher_ceiling_beats_024D1R":
                ceiling_beats_024d1r,

            "loose_beats_006D":
                loose_beats_006d,

            "teacher_like_ge10pct_peak_participation":
                teacher_like_participation,

            "independent_pass":
                independent_pass,

            "interpretation":
                interpretation,

            "024E1":
                decision,

            "next":
                next_action,

            "practical_device":
                False,
        },

        "limits": [
            "NO_SELF_BOUND_ANISOTROPIC_PACKET",
            "NO_SHAPE_ORIENTATION_DYNAMICS",
            "NO_MICROSCOPIC_GUIDE",
            "NO_FULL_LOCAL_DYNAMIC_TMUNU_CONSERVATION",
            "NO_FULL_STABILITY",
            "NO_NONLINEAR_GR",
            "NO_1_OVER_G_ESCAPE",
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
        "\n",
        encoding="utf-8",
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
        f"SHAPE_CSV="
        f"{OUTS.relative_to(ROOT)}"
    )

    if OUTN.is_file():

        print(
            f"BEST_PROFILE_NPZ="
            f"{OUTN.relative_to(ROOT)}"
        )

    print(
        "024E1_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
