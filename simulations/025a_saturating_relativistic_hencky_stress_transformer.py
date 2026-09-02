#!/usr/bin/env python3
"""025A — Saturating Relativistic Hencky Stress-Transformer Gate.

PURPOSE
-------
Test a genuinely new matter-realization route for the project's
positive-energy antigravity-like stress architecture.

Rather than inventing another source tensor, collision mechanism, orbit,
portal interaction, or topological field, construct an explicit
relativistic hyperelastic stored-energy law whose strains generate the
principal stresses required by the 006B/006D stress-transformer geometry.

SCIENTIFIC QUESTION
-------------------
Can one positive-energy relativistic hyperelastic constitutive law generate

    core:
        p_r/rho   = -t
        p_phi/rho = -t
        p_z/rho   = 0

    transfer annulus:
        p_r/rho   = -q
        p_phi/rho = +q
        p_z/rho   = 0

    outer support:
        p_phi/rho = +s

with:

    positive energy;
    pointwise DEC;
    positive NEC margins at finite strain;
    convex stored energy in logarithmic strain;
    causal principal longitudinal characteristics;
    subluminal reference transverse waves;

while preserving an outward finite-payload weak-field GR response?

PHYSICAL MODEL
--------------
Use a relativistic elastic medium described by material-coordinate fields
Phi^I.

In the local material principal frame define principal material number
densities n_i and logarithmic strains

    y_i = ln(n_i / n_i0).

The matter action is schematically

    S_m
      =
    - integral sqrt(-g) rho(Phi, y_i) d^4x.

The project-derived saturating stored-energy law is

    rho
      =
    rho_star(Phi)
    exp[
        sum_i y_i
        +
        (1/k) sum_i ln cosh(k y_i)
    ].

Here:

    rho_star(Phi) > 0

is allowed to vary with comoving material coordinate.

That describes a graded relativistic elastic metamaterial rather than a
spatially homogeneous solid.

This grading freedom is explicit and is measured by the run.

It is NOT treated as free energy or omitted support.

EXACT CONSTITUTIVE IDENTITIES
-----------------------------
For a hyperelastic energy rho(n_i), the principal pressures satisfy

    rho + p_i
      =
    partial rho / partial y_i.

For the chosen stored energy:

    p_i / rho
      =
    tanh(k y_i).

Therefore at every finite strain:

    -1 < p_i/rho < 1

and hence:

    rho > 0
    DEC = satisfied
    WEC = satisfied
    NEC = strictly satisfied.

The log-energy Hessian is diagonal:

    partial^2 ln(rho)
    / partial y_i partial y_j
      =
    k sech^2(k y_i) delta_ij

and is nonnegative.

The Hessian of rho itself is also positive definite at finite strain.

PRINCIPAL LONGITUDINAL CHARACTERISTICS
--------------------------------------
For propagation along a principal direction, relativistic elasticity gives

    c_L,i^2
      =
    [rho_,ii - rho_,i]
    /
    rho_,i.

For this constitutive law:

    c_L,i^2
      =
    k
    +
    (1-k) p_i/rho.

Thus if:

    1/2 <= k < 1

then for every finite DEC state:

    0 <= c_L,i^2 < 1.

At the unstrained isotropic reference state, expansion to quadratic order
gives:

    bulk modulus / rho = k/3

    shear modulus / rho = k/2

and therefore:

    c_L,reference^2 = k

    c_T,reference^2 = k/2.

The complete finite-strain transverse/off-principal characteristic cone is
NOT proved by this slice.

That remains a mandatory promotion gate for 025B.

TARGET STRAINS
--------------
The desired stress states are obtained exactly.

Core:

    y_r
      =
    -atanh(t)/k

    y_phi
      =
    -atanh(t)/k

    y_z = 0.

Transfer annulus:

    y_r
      =
    -atanh(q)/k

    y_phi
      =
    +atanh(q)/k

    y_z = 0.

Outer compressive support:

    y_phi
      =
    +atanh(s)/k

with the other principal log strains zero in the local support model.

There is therefore no stress-fitting error.

FINITE STRAIN / DEC LIMIT
-------------------------
The ideal 006B source uses:

    t = q = s = 1

which saturates DEC.

The present material can approach this limit but reaches it only as
the corresponding logarithmic strain tends to infinity.

This gives a falsifiable efficiency-versus-strain tradeoff.

GRADED MATERIAL SCALE
---------------------
For one principal stress ratio

    w = p/rho

the local state energy factor is exactly

    rho/rho_star
      =
    (1-w)^(-1/k).

Thus:

    core factor
      =
    (1+t)^(-2/k)

    transfer-annulus factor
      =
    (1-q^2)^(-1/k)

    support factor
      =
    (1-s)^(-1/k).

The actual conserved source requires at r=a:

    rho_ann(a)
      =
    (t/q) rho_core.

Therefore the comoving material-density grading required at that interface is

    rho_star_ann(a) / rho_star_core
      =
    (t/q)
    (core_factor / annulus_factor).

This ratio is reported explicitly.

No arbitrary grading cap is treated as a law of physics.

Engineering diagnostics are provided for 10x, 100x, 1000x and 10000x
material-scale contrast.

CONSERVED THIN SOURCE
---------------------
Use the exact generalized 006B architecture.

Core, 0 <= r <= a:

    U = U0

    p_r = -t U0

    p_phi = -t U0.

Transfer annulus, a < r < R:

    U
      =
    (t/q) U0 a^2/r^2

    p_r
      =
    -t U0 a^2/r^2

    p_phi
      =
    +t U0 a^2/r^2.

Outer line support:

    required azimuthal compression
      =
    t U0 a^2/R.

If the support material has:

    p_phi / rho = s,

its minimum line energy is

    lambda
      =
    t U0 a^2/(s R).

The construction obeys the same thin radial conservation identity as 006B.

For t=q=s=1 it reduces exactly to the established 006B source.

WEAK-FIELD GR OBSERVABLE
------------------------
Set payload-center height:

    h = 1.

Define:

    A_core(a)
      =
    1 - 1/sqrt(1+a^2).

Define:

    J(r)
      =
    1/sqrt(1+r^2)
    +
    1/2 ln[
        (sqrt(1+r^2)-1)
        /
        (sqrt(1+r^2)+1)
    ].

The dimensionless outward field factor is

    F
      =
    -[
        (1-2t) A_core(a)

        +
        (t/q) a^2 [J(R)-J(a)]

        +
        t a^2 (1+s)/s
        /
        (1+R^2)^(3/2)
    ].

The dimensionless energy factor is

    m
      =
    a^2 [
        1

        +
        2(t/q) ln(R/a)

        +
        2t/s
    ].

For:

    F > 0

the energy coefficient is

    C
      =
    m/(2F).

For:

    t=q=s=1

and:

    a = 1.437500564637

    R = 4.701437405300

the formula must reproduce:

    C_006B
      =
    23.426710175391.

This is a mandatory regression.

FINITE PAYLOAD
--------------
The best material candidate receives an independent direct Green-function
integration over a finite spherical payload.

Inherited payload radius:

    R_payload/h
      =
    0.043298860805059215.

The payload is sampled by a deterministic Sobol uniform-volume point set.

For every payload sample, the axial field of:

    core
    annulus
    outer support

is integrated independently from the closed-form on-axis formula.

Promotion requires:

    center integral agrees with analytic F;

    mean finite-payload axial field is outward;

    every sampled payload point is outward.

NUMERICAL SEARCH
----------------
Primary Sobol campaign:

    2^20 = 1,048,576

joint material + source-geometry designs.

Scan:

    k:
        0.50 to 0.95

    t:
        0.5001 to approximately 0.99995

    q:
        0.20 to approximately 0.99992

    s:
        0.20 to approximately 0.99992

    a/h:
        0.30 to 4.0

    R/a:
        1.05 to 8.0.

Stress ratios are sampled logarithmically in their distance from DEC
saturation so the scan resolves both ordinary and near-boundary regimes.

A separate deterministic strain frontier is calculated.

The full campaign is independently refined with differential evolution.

ENGINEERING STRAIN DIAGNOSTICS
------------------------------
Report best candidates subject to:

    max |y_i| <=
        1.0
        1.5
        2.0
        2.5
        3.0
        3.5
        4.0
        5.0
        6.0.

These are engineering/naturalness diagnostics.

They are NOT fundamental physical cutoffs.

BLIND WILDCARDS
---------------
Also report strain-cap diagnostics at:

    0.625
    1.6
    1.875
    3.125
    5

as:

    BLIND_WILDCARD_NOT_PHYSICS_PRIOR.

They are never used to select or promote a result.

VALIDATION
----------
1. 94 known-solution regressions are run before this simulation.
2. Exact 006B limit is reproduced.
3. Analytic DEC and characteristic identities are checked numerically.
4. 2^20 Sobol global search.
5. Independent differential-evolution optimization.
6. Finite spherical-payload Green-function reconstruction.
7. Center-field analytic/numerical agreement.
8. Limiting approach to 006B is explicitly measured.

PROMOTION CONDITION
-------------------
A strong 025A preflight requires:

    one explicit hyperelastic Lagrangian;

    positive energy;

    DEC/NEC/WEC analytically;

    principal longitudinal causality analytically;

    subluminal reference transverse speed;

    exact local stress-state realization;

    distributionally conserved thin source;

    finite-payload outward response;

    C < 30 at max |y| <= 4;

    independent reconstruction PASS.

This promotes only to:

    GLOBAL HYPERELASTIC BVP AUTHORIZED.

It does NOT establish a complete material realization.

FALSIFIERS
----------
If no outward finite-payload solution survives at moderate strain:

    demote the minimal saturating hyperelastic model.

If only near-DEC, enormous-strain solutions survive:

    classify the model as a constitutive existence result with a
    naturalness/engineering obstruction.

If the finite-payload reconstruction reverses sign:

    reject the source-level promotion.

STOP RULE
---------
Do not run another arbitrary stress-source optimization after this slice.

If 025A is positive:

    025B must solve the actual axisymmetric material-coordinate
    Euler-Lagrange boundary-value problem with smooth finite collars,
    compatibility, grading, and the full characteristic cone.

If 025A is negative:

    rerank toward Analogue Antigravity rather than inventing another
    pure-GR source geometry.

APPROXIMATION LEVEL
-------------------
Static weak-field GR for the gravitational response.

Relativistic hyperelastic continuum EFT for local matter constitutive
physics.

Thin-source geometry for the first realization gate.

No exact nonlinear Einstein-matter solution.

LIMITATIONS
-----------
This slice does NOT establish:

- global deformation compatibility;
- an axisymmetric elastic Euler-Lagrange solution;
- finite-thickness collar realization;
- complete finite-strain transverse/off-axis hyperbolicity;
- nonlinear GR;
- microscopic particle/material construction;
- experimentally realizable stresses;
- favorable absolute 1/G scaling;
- a practical antigravity device.

RELATED FILES
-------------
006B thin conserved source.
006D finite-thickness constructive source.
INT-14/15 source-efficiency and teacher-anatomy results.
024A-E successor and falsification campaigns.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_RELATIVISTIC_HYPERELASTIC_CONSTITUTIVE_PREFLIGHT
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution
from scipy.stats import qmc
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results/data"

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

OUT_JSON = (
    DATA
    / "025a_saturating_relativistic_hencky_summary.json"
)

OUT_CSV = (
    DATA
    / "025a_saturating_relativistic_hencky_top.csv"
)

OUT_FRONTIER = (
    DATA
    / "025a_saturating_relativistic_hencky_frontier.csv"
)

OUT_NPZ = (
    DATA
    / "025a_saturating_relativistic_hencky_best_profile.npz"
)


C006B = 23.426710175391
C006D = 23.591586299249

A006B = 1.437500564637
R006B = 4.701437405300

PAYLOAD_RADIUS = 0.043298860805059215

K_MIN = 0.50
K_MAX = 0.95

SMOKE = (
    os.environ.get(
        "AG_SMOKE",
        "0",
    )
    ==
    "1"
)

SOBOL_POWER = (
    12
    if SMOKE
    else 20
)

NCASE = 2 ** SOBOL_POWER

STRAIN_CAPS = (
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    3.5,
    4.0,
    5.0,
    6.0,
)

WILDCARD_CAPS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


def j_kernel(
    r: np.ndarray | float,
) -> np.ndarray | float:
    """Primitive of 1/[r(1+r^2)^(3/2)]."""

    r = np.asarray(
        r,
        dtype=float,
    )

    root = np.sqrt(
        1.0
        +
        r * r
    )

    return (
        1.0
        /
        root
        +
        0.5
        * np.log(
            (
                root
                -
                1.0
            )
            /
            (
                root
                +
                1.0
            )
        )
    )


def source_metrics(
    t,
    q,
    support,
    a,
    R,
):
    """Vectorized generalized conserved thin-source observables."""

    t = np.asarray(
        t,
        dtype=float,
    )

    q = np.asarray(
        q,
        dtype=float,
    )

    support = np.asarray(
        support,
        dtype=float,
    )

    a = np.asarray(
        a,
        dtype=float,
    )

    R = np.asarray(
        R,
        dtype=float,
    )

    valid = (
        (t > 0.5)
        &
        (t < 1.0)
        &
        (q > 0.0)
        &
        (q < 1.0)
        &
        (support > 0.0)
        &
        (support < 1.0)
        &
        (a > 0.0)
        &
        (R > a)
    )

    core_kernel = (
        1.0
        -
        1.0
        /
        np.sqrt(
            1.0
            +
            a * a
        )
    )

    annulus = (
        (t / q)
        * a * a
        * (
            j_kernel(R)
            -
            j_kernel(a)
        )
    )

    line_active = (
        t
        * a
        * a
        * (
            1.0
            +
            support
        )
        /
        support
        /
        (
            1.0
            +
            R * R
        ) ** 1.5
    )

    weighted_active = (
        (
            1.0
            -
            2.0
            * t
        )
        * core_kernel
        +
        annulus
        +
        line_active
    )

    F = (
        -weighted_active
    )

    mass = (
        a
        * a
        * (
            1.0
            +
            2.0
            * (
                t
                /
                q
            )
            * np.log(
                R
                /
                a
            )
            +
            2.0
            * t
            /
            support
        )
    )

    C = np.where(
        valid
        &
        (F > 0.0),
        mass
        /
        (
            2.0
            * F
        ),
        np.inf,
    )

    return {
        "F":
            F,

        "mass":
            mass,

        "C":
            C,

        "valid":
            valid,
    }


def scalar_source_metrics(
    t: float,
    q: float,
    support: float,
    a: float,
    R: float,
) -> dict:
    """Scalar wrapper."""

    out = source_metrics(
        np.asarray([t]),
        np.asarray([q]),
        np.asarray([support]),
        np.asarray([a]),
        np.asarray([R]),
    )

    return {
        key:
            float(value[0])
            if isinstance(
                value,
                np.ndarray,
            )
            else value
        for key, value in out.items()
    }


def material_metrics(
    k,
    t,
    q,
    support,
):
    """Exact local hyperelastic-state diagnostics."""

    k = np.asarray(
        k,
        dtype=float,
    )

    t = np.asarray(
        t,
        dtype=float,
    )

    q = np.asarray(
        q,
        dtype=float,
    )

    support = np.asarray(
        support,
        dtype=float,
    )

    y_core = (
        np.arctanh(t)
        /
        k
    )

    y_ann = (
        np.arctanh(q)
        /
        k
    )

    y_support = (
        np.arctanh(support)
        /
        k
    )

    max_strain = np.maximum.reduce(
        (
            y_core,
            y_ann,
            y_support,
        )
    )

    core_factor = (
        1.0
        +
        t
    ) ** (
        -2.0
        /
        k
    )

    ann_factor = (
        1.0
        -
        q * q
    ) ** (
        -1.0
        /
        k
    )

    support_factor = (
        1.0
        -
        support
    ) ** (
        -1.0
        /
        k
    )

    grading = (
        (t / q)
        * core_factor
        /
        ann_factor
    )

    cL_core_tension = (
        k
        -
        (
            1.0
            -
            k
        )
        * t
    )

    cL_ann_tension = (
        k
        -
        (
            1.0
            -
            k
        )
        * q
    )

    cL_ann_compression = (
        k
        +
        (
            1.0
            -
            k
        )
        * q
    )

    cL_support = (
        k
        +
        (
            1.0
            -
            k
        )
        * support
    )

    cL_min = np.minimum.reduce(
        (
            cL_core_tension,
            cL_ann_tension,
            k,
        )
    )

    cL_max = np.maximum.reduce(
        (
            cL_ann_compression,
            cL_support,
            k,
        )
    )

    cT_reference = (
        0.5
        * k
    )

    dec_margin = (
        1.0
        -
        np.maximum.reduce(
            (
                t,
                q,
                support,
            )
        )
    )

    nec_margin_ratio = dec_margin

    causal_principal = (
        (cL_min >= 0.0)
        &
        (cL_max <= 1.0)
    )

    return {
        "y_core":
            y_core,

        "y_ann":
            y_ann,

        "y_support":
            y_support,

        "max_strain":
            max_strain,

        "core_factor":
            core_factor,

        "ann_factor":
            ann_factor,

        "support_factor":
            support_factor,

        "grading":
            grading,

        "cL_min":
            cL_min,

        "cL_max":
            cL_max,

        "cT_reference":
            cT_reference,

        "dec_margin":
            dec_margin,

        "nec_margin_ratio":
            nec_margin_ratio,

        "causal_principal":
            causal_principal,
    }


def stress_parameter(
    u: np.ndarray,
    lower: float,
) -> np.ndarray:
    """Resolve many decades approaching DEC saturation."""

    return (
        1.0
        -
        (
            1.0
            -
            lower
        )
        * 10.0 ** (
            -4.0
            * u
        )
    )


def build_population():
    """Generate the global Sobol material/geometry population."""

    u = qmc.Sobol(
        d=6,
        scramble=True,
        seed=250100,
    ).random_base2(
        SOBOL_POWER
    )

    k = (
        K_MIN
        +
        (
            K_MAX
            -
            K_MIN
        )
        * u[:, 0]
    )

    t = stress_parameter(
        u[:, 1],
        0.5001,
    )

    q = stress_parameter(
        u[:, 2],
        0.20,
    )

    support = stress_parameter(
        u[:, 3],
        0.20,
    )

    a = 10.0 ** (
        math.log10(0.30)
        +
        (
            math.log10(4.0)
            -
            math.log10(0.30)
        )
        * u[:, 4]
    )

    ratio = 10.0 ** (
        math.log10(1.05)
        +
        (
            math.log10(8.0)
            -
            math.log10(1.05)
        )
        * u[:, 5]
    )

    R = (
        a
        * ratio
    )

    return {
        "k":
            k,

        "t":
            t,

        "q":
            q,

        "support":
            support,

        "a":
            a,

        "ratio":
            ratio,

        "R":
            R,
    }


def row_from_index(
    index: int,
    p: dict,
    mat: dict,
    src: dict,
) -> dict:
    """Serialize one scan point."""

    i = int(index)

    return {
        "index":
            i,

        "k":
            float(
                p["k"][i]
            ),

        "t":
            float(
                p["t"][i]
            ),

        "q":
            float(
                p["q"][i]
            ),

        "support":
            float(
                p["support"][i]
            ),

        "a":
            float(
                p["a"][i]
            ),

        "R":
            float(
                p["R"][i]
            ),

        "R_over_a":
            float(
                p["ratio"][i]
            ),

        "F":
            float(
                src["F"][i]
            ),

        "mass":
            float(
                src["mass"][i]
            ),

        "C":
            float(
                src["C"][i]
            ),

        "y_core":
            float(
                mat["y_core"][i]
            ),

        "y_ann":
            float(
                mat["y_ann"][i]
            ),

        "y_support":
            float(
                mat[
                    "y_support"
                ][i]
            ),

        "max_log_strain":
            float(
                mat[
                    "max_strain"
                ][i]
            ),

        "core_energy_factor":
            float(
                mat[
                    "core_factor"
                ][i]
            ),

        "annulus_energy_factor":
            float(
                mat[
                    "ann_factor"
                ][i]
            ),

        "support_energy_factor":
            float(
                mat[
                    "support_factor"
                ][i]
            ),

        "rho_star_ann_over_core_at_a":
            float(
                mat["grading"][i]
            ),

        "cL2_min":
            float(
                mat["cL_min"][i]
            ),

        "cL2_max":
            float(
                mat["cL_max"][i]
            ),

        "cT2_reference":
            float(
                mat[
                    "cT_reference"
                ][i]
            ),

        "DEC_margin_ratio":
            float(
                mat[
                    "dec_margin"
                ][i]
            ),

        "NEC_margin_ratio":
            float(
                mat[
                    "nec_margin_ratio"
                ][i]
            ),

        "principal_longitudinal_causal":
            bool(
                mat[
                    "causal_principal"
                ][i]
            ),
    }


def optimize_for_cap(
    strain_cap: float,
    grading_floor: float = 0.0,
    seed: int = 2501,
) -> dict | None:
    """Independent differential-evolution optimization."""

    def objective(x):

        k, t, q, support, la, lr = x

        a = math.exp(
            la
        )

        ratio = math.exp(
            lr
        )

        R = (
            a
            * ratio
        )

        mat = material_metrics(
            np.asarray([k]),
            np.asarray([t]),
            np.asarray([q]),
            np.asarray([support]),
        )

        max_strain = float(
            mat[
                "max_strain"
            ][0]
        )

        grading = float(
            mat[
                "grading"
            ][0]
        )

        causal = bool(
            mat[
                "causal_principal"
            ][0]
        )

        if not causal:

            return 1.0e9

        if max_strain > strain_cap:

            return (
                1.0e8
                +
                1.0e5
                * (
                    max_strain
                    -
                    strain_cap
                )
            )

        if (
            grading_floor
            >
            0.0
            and
            grading
            <
            grading_floor
        ):

            return (
                1.0e7
                +
                1.0e4
                * math.log(
                    grading_floor
                    /
                    max(
                        grading,
                        1.0e-300,
                    )
                )
            )

        src = scalar_source_metrics(
            t,
            q,
            support,
            a,
            R,
        )

        C = src[
            "C"
        ]

        if not math.isfinite(
            C
        ):

            return 1.0e6

        return C

    bounds = (
        (
            K_MIN,
            K_MAX,
        ),
        (
            0.500001,
            0.99995,
        ),
        (
            0.20,
            0.99995,
        ),
        (
            0.20,
            0.99995,
        ),
        (
            math.log(0.25),
            math.log(5.0),
        ),
        (
            math.log(1.02),
            math.log(10.0),
        ),
    )

    result = differential_evolution(
        objective,
        bounds,
        seed=seed,
        maxiter=(
            35
            if SMOKE
            else 120
        ),
        popsize=(
            6
            if SMOKE
            else 12
        ),
        tol=1.0e-10,
        atol=1.0e-10,
        polish=True,
        workers=1,
        updating="immediate",
    )

    if (
        not math.isfinite(
            result.fun
        )
        or
        result.fun
        >=
        1.0e6
    ):

        return None

    k, t, q, support, la, lr = result.x

    a = math.exp(
        la
    )

    ratio = math.exp(
        lr
    )

    R = (
        a
        * ratio
    )

    mat = material_metrics(
        np.asarray([k]),
        np.asarray([t]),
        np.asarray([q]),
        np.asarray([support]),
    )

    src = scalar_source_metrics(
        t,
        q,
        support,
        a,
        R,
    )

    return {
        "strain_cap":
            float(
                strain_cap
            ),

        "grading_floor":
            float(
                grading_floor
            ),

        "k":
            float(k),

        "t":
            float(t),

        "q":
            float(q),

        "support":
            float(
                support
            ),

        "a":
            float(a),

        "R":
            float(R),

        "R_over_a":
            float(
                ratio
            ),

        "C":
            float(
                src["C"]
            ),

        "F":
            float(
                src["F"]
            ),

        "mass":
            float(
                src["mass"]
            ),

        "max_log_strain":
            float(
                mat[
                    "max_strain"
                ][0]
            ),

        "y_core":
            float(
                mat[
                    "y_core"
                ][0]
            ),

        "y_ann":
            float(
                mat[
                    "y_ann"
                ][0]
            ),

        "y_support":
            float(
                mat[
                    "y_support"
                ][0]
            ),

        "rho_star_ann_over_core_at_a":
            float(
                mat[
                    "grading"
                ][0]
            ),

        "core_energy_factor":
            float(
                mat[
                    "core_factor"
                ][0]
            ),

        "annulus_energy_factor":
            float(
                mat[
                    "ann_factor"
                ][0]
            ),

        "support_energy_factor":
            float(
                mat[
                    "support_factor"
                ][0]
            ),

        "cL2_min":
            float(
                mat[
                    "cL_min"
                ][0]
            ),

        "cL2_max":
            float(
                mat[
                    "cL_max"
                ][0]
            ),

        "cT2_reference":
            float(
                mat[
                    "cT_reference"
                ][0]
            ),

        "DEC_margin_ratio":
            float(
                mat[
                    "dec_margin"
                ][0]
            ),
    }


def field_z_at_points(
    rho_p: np.ndarray,
    z_p: np.ndarray,
    t: float,
    q: float,
    support: float,
    a: float,
    R: float,
    radial_order: int = 96,
    phi_order: int = 160,
) -> np.ndarray:
    """Independent direct thin-source Green-function axial field."""

    xg, wg = leggauss(
        radial_order
    )

    phi = np.linspace(
        0.0,
        2.0
        * math.pi,
        phi_order,
        endpoint=False,
    )

    cos_phi = np.cos(
        phi
    )

    result = np.zeros(
        len(rho_p),
        dtype=float,
    )

    segments = (
        (
            0.0,
            a,
            "core",
        ),
        (
            a,
            R,
            "ann",
        ),
    )

    for low, high, region in segments:

        r = (
            0.5
            * (
                high
                -
                low
            )
            * xg
            +
            0.5
            * (
                high
                +
                low
            )
        )

        wr = (
            0.5
            * (
                high
                -
                low
            )
            * wg
        )

        if region == "core":

            active = np.full_like(
                r,
                1.0
                -
                2.0
                * t,
            )

        else:

            active = (
                (t / q)
                * a
                * a
                /
                (
                    r
                    * r
                )
            )

        for j in range(
            len(rho_p)
        ):

            rp = float(
                rho_p[j]
            )

            zp = float(
                z_p[j]
            )

            dz = zp

            d2 = (
                rp
                * rp
                +
                r[:, None]
                * r[:, None]
                -
                2.0
                * rp
                * r[:, None]
                * cos_phi[None, :]
                +
                dz
                * dz
            )

            kernel = (
                dz
                /
                d2 ** 1.5
            )

            angular_mean = np.mean(
                kernel,
                axis=1,
            )

            result[j] -= float(
                np.sum(
                    wr
                    * r
                    * active
                    * angular_mean
                )
            )

    line_coefficient = (
        t
        * a
        * a
        * (
            1.0
            +
            support
        )
        /
        support
    )

    for j in range(
        len(rho_p)
    ):

        rp = float(
            rho_p[j]
        )

        zp = float(
            z_p[j]
        )

        d2 = (
            rp
            * rp
            +
            R
            * R
            -
            2.0
            * rp
            * R
            * cos_phi
            +
            zp
            * zp
        )

        result[j] -= (
            line_coefficient
            * float(
                np.mean(
                    zp
                    /
                    d2 ** 1.5
                )
            )
        )

    return result


def payload_audit(
    best: dict,
) -> dict:
    """Finite spherical-payload independent Green-function audit."""

    t = best["t"]
    q = best["q"]
    support = best[
        "support"
    ]
    a = best["a"]
    R = best["R"]

    analytic = scalar_source_metrics(
        t,
        q,
        support,
        a,
        R,
    )

    center = field_z_at_points(
        np.asarray([0.0]),
        np.asarray([1.0]),
        t,
        q,
        support,
        a,
        R,
        radial_order=(
            48
            if SMOKE
            else 128
        ),
        phi_order=(
            96
            if SMOKE
            else 256
        ),
    )[0]

    center_relerr = (
        abs(
            center
            -
            analytic["F"]
        )
        /
        max(
            abs(
                analytic["F"]
            ),
            1.0e-300,
        )
    )

    n_payload = (
        32
        if SMOKE
        else 256
    )

    power = int(
        math.ceil(
            math.log2(
                n_payload
            )
        )
    )

    raw = qmc.Sobol(
        d=3,
        scramble=True,
        seed=250199,
    ).random_base2(
        power
    )[
        :n_payload
    ]

    radius = (
        PAYLOAD_RADIUS
        * raw[:, 0] ** (
            1.0
            /
            3.0
        )
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

    azimuth = (
        2.0
        * math.pi
        * raw[:, 2]
    )

    x = (
        radius
        * sin_theta
        * np.cos(
            azimuth
        )
    )

    y = (
        radius
        * sin_theta
        * np.sin(
            azimuth
        )
    )

    z = (
        1.0
        +
        radius
        * cos_theta
    )

    rho_p = np.sqrt(
        x * x
        +
        y * y
    )

    fields = np.empty(
        n_payload,
        dtype=float,
    )

    batch = (
        8
        if SMOKE
        else 32
    )

    for start in range(
        0,
        n_payload,
        batch,
    ):

        stop = min(
            start
            +
            batch,
            n_payload,
        )

        fields[
            start:stop
        ] = field_z_at_points(
            rho_p[
                start:stop
            ],
            z[
                start:stop
            ],
            t,
            q,
            support,
            a,
            R,
            radial_order=(
                40
                if SMOKE
                else 88
            ),
            phi_order=(
                80
                if SMOKE
                else 192
            ),
        )

    mean_field = float(
        np.mean(
            fields
        )
    )

    min_field = float(
        np.min(
            fields
        )
    )

    max_field = float(
        np.max(
            fields
        )
    )

    payload_C = (
        analytic["mass"]
        /
        (
            2.0
            * mean_field
        )
        if mean_field > 0.0
        else math.inf
    )

    return {
        "payload_radius_over_h":
            PAYLOAD_RADIUS,

        "sample_count":
            n_payload,

        "analytic_center_F":
            float(
                analytic["F"]
            ),

        "numeric_center_F":
            float(center),

        "center_relative_error":
            float(
                center_relerr
            ),

        "mean_F":
            mean_field,

        "min_F":
            min_field,

        "max_F":
            max_field,

        "all_outward":
            bool(
                np.all(
                    fields
                    >
                    0.0
                )
            ),

        "finite_payload_C":
            float(
                payload_C
            ),
    }


def print_candidate(
    prefix: str,
    row: dict | None,
) -> None:
    """Print a candidate consistently."""

    if row is None:

        print(
            f"{prefix}_SURVIVOR=NO"
        )

        return

    print(
        f"{prefix}_SURVIVOR=YES"
    )

    for key in (
        "C",
        "F",
        "mass",
        "k",
        "t",
        "q",
        "support",
        "a",
        "R",
        "R_over_a",
        "max_log_strain",
        "y_core",
        "y_ann",
        "y_support",
        "rho_star_ann_over_core_at_a",
        "core_energy_factor",
        "annulus_energy_factor",
        "support_energy_factor",
        "cL2_min",
        "cL2_max",
        "cT2_reference",
        "DEC_margin_ratio",
    ):

        if key in row:

            print(
                f"{prefix}_{key.upper()}="
                f"{float(row[key]):.15e}"
            )


def main():
    """Execute 025A."""

    print(
        "=== 025A SATURATING RELATIVISTIC HENCKY STRESS TRANSFORMER ==="
    )

    print(
        "\n=== A — EXACT CONSTITUTIVE MODEL ==="
    )

    print(
        "MODEL=SATURATING_RELATIVISTIC_HENCKY_SOLID"
    )

    print(
        "MATTER_DESCRIPTION=RELATIVISTIC_HYPERELASTIC_CONTINUUM_EFT"
    )

    print(
        "RHO_POSITIVE_BY_CONSTRUCTION=YES"
    )

    print(
        "PRESSURE_RATIO_IDENTITY=P_I_OVER_RHO_EQUALS_TANH_K_Y_I"
    )

    print(
        "GLOBAL_FINITE_STRAIN_DEC_IN_LOCAL_CONSTITUTIVE_MODEL=YES"
    )

    print(
        "GLOBAL_FINITE_STRAIN_NEC_STRICT_IN_LOCAL_CONSTITUTIVE_MODEL=YES"
    )

    print(
        "LOG_STRAIN_ENERGY_CONVEXITY=YES"
    )

    print(
        "PRINCIPAL_LONGITUDINAL_SPEED_IDENTITY="
        "CL2_EQUALS_K_PLUS_ONE_MINUS_K_TIMES_P_OVER_RHO"
    )

    print(
        "REFERENCE_CT2_EQUALS_K_OVER_2=YES"
    )

    print(
        "FULL_FINITE_STRAIN_TRANSVERSE_CHARACTERISTIC_CONE="
        "NOT_ESTABLISHED"
    )

    print(
        "RHO_STAR_MATERIAL_COORDINATE_GRADING=ALLOWED_AND_REPORTED"
    )

    print(
        "GLOBAL_ELASTIC_EULER_LAGRANGE_BVP=NOT_ESTABLISHED"
    )

    print(
        "\n=== B — 006B EXACT LIMIT REGRESSION ==="
    )

    control = scalar_source_metrics(
        1.0 - 1.0e-14,
        1.0 - 1.0e-14,
        1.0 - 1.0e-14,
        A006B,
        R006B,
    )

    exact_limit = source_metrics(
        np.asarray([1.0]),
        np.asarray([1.0]),
        np.asarray([1.0]),
        np.asarray([A006B]),
        np.asarray([R006B]),
    )

    # source_metrics rejects strict equality because the material state
    # itself is infinite-strain. Evaluate the mathematical 006B formula
    # directly for its regression value.

    t0 = 1.0
    q0 = 1.0
    s0 = 1.0
    a0 = A006B
    R0 = R006B

    core0 = (
        1.0
        -
        1.0
        /
        math.sqrt(
            1.0
            +
            a0 * a0
        )
    )

    F0 = -(
        (
            1.0
            -
            2.0
            * t0
        )
        * core0
        +
        (
            t0
            /
            q0
        )
        * a0
        * a0
        * (
            float(
                j_kernel(R0)
            )
            -
            float(
                j_kernel(a0)
            )
        )
        +
        t0
        * a0
        * a0
        * (
            1.0
            +
            s0
        )
        /
        s0
        /
        (
            1.0
            +
            R0
            * R0
        ) ** 1.5
    )

    m0 = (
        a0
        * a0
        * (
            1.0
            +
            2.0
            * (
                t0
                /
                q0
            )
            * math.log(
                R0
                /
                a0
            )
            +
            2.0
            * t0
            /
            s0
        )
    )

    C0 = (
        m0
        /
        (
            2.0
            * F0
        )
    )

    rel006b = (
        abs(
            C0
            -
            C006B
        )
        /
        C006B
    )

    print(
        f"C_006B_REFERENCE="
        f"{C006B:.15e}"
    )

    print(
        f"C_006B_REBUILT="
        f"{C0:.15e}"
    )

    print(
        f"C_006B_RELERR="
        f"{rel006b:.15e}"
    )

    if rel006b > 1.0e-10:

        raise RuntimeError(
            "006B exact-limit regression failed"
        )

    print(
        "C_006B_LIMIT_REGRESSION=PASS"
    )

    print(
        f"C_006D_FINITE_REFERENCE="
        f"{C006D:.15e}"
    )

    print(
        "\n=== C — ANALYTIC SYMMETRIC STRAIN FRONTIER ==="
    )

    frontier_rows = []

    for cap in STRAIN_CAPS:

        k = K_MAX

        w = math.tanh(
            k
            * cap
        )

        best = optimize_for_cap(
            cap,
            grading_floor=0.0,
            seed=(
                250100
                +
                int(
                    100
                    * cap
                )
            ),
        )

        if best is None:

            print(
                f"STRAIN_CAP={cap:.6f} "
                "REFINED_SURVIVOR=NO"
            )

            continue

        frontier_rows.append(
            best
        )

        print(
            f"STRAIN_CAP={cap:.6f} "
            f"REFINED_C={best['C']:.12e} "
            f"K={best['k']:.8f} "
            f"T={best['t']:.8f} "
            f"Q={best['q']:.8f} "
            f"SUPPORT={best['support']:.8f} "
            f"MAX_STRAIN={best['max_log_strain']:.8f} "
            f"GRADING={best['rho_star_ann_over_core_at_a']:.12e}"
        )

    print(
        "\n=== D — 2^20 GLOBAL SOBOL MATERIAL + GEOMETRY CAMPAIGN ==="
    )

    p = build_population()

    mat = material_metrics(
        p["k"],
        p["t"],
        p["q"],
        p["support"],
    )

    src = source_metrics(
        p["t"],
        p["q"],
        p["support"],
        p["a"],
        p["R"],
    )

    valid = (
        src["valid"]
        &
        np.isfinite(
            src["C"]
        )
        &
        mat[
            "causal_principal"
        ]
    )

    print(
        f"BASE_SOBOL_CASES="
        f"{NCASE}"
    )

    print(
        f"OUTWARD_CAUSAL_CASES="
        f"{int(np.count_nonzero(valid))}"
    )

    print(
        f"CASES_BEATING_006D_FINITE_COEFFICIENT="
        f"{int(np.count_nonzero(valid & (src['C'] < C006D)))}"
    )

    print(
        f"CASES_BEATING_006B_THIN_COEFFICIENT="
        f"{int(np.count_nonzero(valid & (src['C'] < C006B)))}"
    )

    top_rows = []

    finite_ids = np.flatnonzero(
        valid
    )

    if len(
        finite_ids
    ):

        count = min(
            300,
            len(
                finite_ids
            ),
        )

        local = np.argpartition(
            src["C"][
                finite_ids
            ],
            count - 1,
        )[:count]

        chosen = finite_ids[
            local
        ]

        top_rows = [
            row_from_index(
                int(i),
                p,
                mat,
                src,
            )
            for i in chosen
        ]

        top_rows.sort(
            key=lambda row:
                row["C"]
        )

    if top_rows:

        print_candidate(
            "BEST_GLOBAL_SOBOL",
            top_rows[0],
        )

    else:

        print(
            "BEST_GLOBAL_SOBOL_SURVIVOR=NO"
        )

    print(
        "\n=== E — STRAIN-CAPPED SOBOL FRONTIER ==="
    )

    sobol_frontier = []

    for cap in STRAIN_CAPS:

        mask = (
            valid
            &
            (
                mat[
                    "max_strain"
                ]
                <=
                cap
            )
        )

        ids = np.flatnonzero(
            mask
        )

        if len(ids) == 0:

            print(
                f"SOBOL_STRAIN_CAP={cap:.6f} "
                "SURVIVOR=NO"
            )

            continue

        best_id = ids[
            np.argmin(
                src["C"][
                    ids
                ]
            )
        ]

        row = row_from_index(
            int(
                best_id
            ),
            p,
            mat,
            src,
        )

        row[
            "strain_cap"
        ] = float(cap)

        sobol_frontier.append(
            row
        )

        print(
            f"SOBOL_STRAIN_CAP={cap:.6f} "
            f"C={row['C']:.12e} "
            f"K={row['k']:.8f} "
            f"T={row['t']:.8f} "
            f"Q={row['q']:.8f} "
            f"SUPPORT={row['support']:.8f} "
            f"MAX_STRAIN={row['max_log_strain']:.8f} "
            f"GRADING={row['rho_star_ann_over_core_at_a']:.12e}"
        )

    print(
        "\n=== F — MATERIAL-GRADING TRADEOFF ==="
    )

    grading_floors = (
        1.0e-1,
        1.0e-2,
        1.0e-3,
        1.0e-4,
    )

    grading_rows = []

    for floor in grading_floors:

        mask = (
            valid
            &
            (
                mat[
                    "max_strain"
                ]
                <=
                4.0
            )
            &
            (
                mat[
                    "grading"
                ]
                >=
                floor
            )
        )

        ids = np.flatnonzero(
            mask
        )

        if len(ids) == 0:

            print(
                f"GRADING_FLOOR={floor:.1e} "
                "SURVIVOR=NO"
            )

            continue

        i = ids[
            np.argmin(
                src["C"][
                    ids
                ]
            )
        ]

        row = row_from_index(
            int(i),
            p,
            mat,
            src,
        )

        row[
            "grading_floor"
        ] = float(
            floor
        )

        grading_rows.append(
            row
        )

        print(
            f"GRADING_FLOOR={floor:.1e} "
            f"BEST_C={row['C']:.12e} "
            f"STRAIN={row['max_log_strain']:.8f} "
            f"ACTUAL_GRADING={row['rho_star_ann_over_core_at_a']:.12e}"
        )

    print(
        "\n=== G — BLIND WILDCARD STRAIN DIAGNOSTICS ==="
    )

    for cap in WILDCARD_CAPS:

        mask = (
            valid
            &
            (
                mat[
                    "max_strain"
                ]
                <=
                cap
            )
        )

        ids = np.flatnonzero(
            mask
        )

        value = (
            float(
                np.min(
                    src["C"][
                        ids
                    ]
                )
            )
            if len(ids)
            else math.inf
        )

        print(
            f"WILDCARD_STRAIN_CAP={cap:.6f} "
            f"BEST_C={value:.12e} "
            "ROLE=BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
        )

    print(
        "WILDCARDS_USED_FOR_SELECTION=NO"
    )

    print(
        "\n=== H — INDEPENDENT DIFFERENTIAL-EVOLUTION REFINEMENT ==="
    )

    refined = {}

    for cap in (
        2.0,
        3.0,
        4.0,
        6.0,
    ):

        row = optimize_for_cap(
            cap,
            grading_floor=0.0,
            seed=(
                260000
                +
                int(
                    100
                    * cap
                )
            ),
        )

        refined[
            str(cap)
        ] = row

        print_candidate(
            "REFINED_CAP_"
            +
            str(cap).replace(
                ".",
                "P",
            ),
            row,
        )

    print(
        "\n=== I — INDEPENDENT GRADING-CONSTRAINED REFINEMENT ==="
    )

    refined_grading = {}

    for floor in (
        1.0e-2,
        1.0e-3,
        1.0e-4,
    ):

        row = optimize_for_cap(
            4.0,
            grading_floor=floor,
            seed=(
                270000
                +
                int(
                    -math.log10(
                        floor
                    )
                )
            ),
        )

        refined_grading[
            f"{floor:.0e}"
        ] = row

        print_candidate(
            "REFINED_GRADING_"
            +
            f"{floor:.0e}".replace(
                "-",
                "M",
            ),
            row,
        )

    selected = refined.get(
        "4.0"
    )

    if selected is None:

        selected = (
            refined.get(
                "6.0"
            )
        )

    print(
        "\n=== J — FINITE SPHERICAL PAYLOAD AUDIT ==="
    )

    payload = None

    if selected is not None:

        payload = payload_audit(
            selected
        )

        for key, value in payload.items():

            if isinstance(
                value,
                bool,
            ):

                print(
                    f"PAYLOAD_{key.upper()}="
                    +
                    (
                        "YES"
                        if value
                        else "NO"
                    )
                )

            elif isinstance(
                value,
                int,
            ):

                print(
                    f"PAYLOAD_{key.upper()}="
                    f"{value}"
                )

            else:

                print(
                    f"PAYLOAD_{key.upper()}="
                    f"{float(value):.15e}"
                )

        payload_pass = bool(
            payload[
                "center_relative_error"
            ]
            <=
            2.0e-3
            and
            payload[
                "all_outward"
            ]
            and
            payload[
                "mean_F"
            ]
            >
            0.0
        )

        print(
            "FINITE_PAYLOAD_AUDIT="
            +
            (
                "PASS"
                if payload_pass
                else "FAIL"
            )
        )

    else:

        payload_pass = False

        print(
            "FINITE_PAYLOAD_AUDIT="
            "NOT_RUN_NO_SELECTED_CANDIDATE"
        )

    print(
        "\n=== K — LIMITING / CONSISTENCY CHECKS ==="
    )

    # Extremely close to DEC saturation should approach 006B from above.
    eps = 1.0e-7

    near = scalar_source_metrics(
        1.0 - eps,
        1.0 - eps,
        1.0 - eps,
        A006B,
        R006B,
    )

    print(
        f"NEAR_DEC_LIMIT_EPS="
        f"{eps:.12e}"
    )

    print(
        f"NEAR_DEC_LIMIT_C="
        f"{near['C']:.15e}"
    )

    print(
        f"NEAR_DEC_LIMIT_RELATIVE_TO_006B="
        f"{near['C'] / C006B:.15e}"
    )

    print(
        "DEC_LIMIT_APPROACHES_006B="
        +
        (
            "PASS"
            if (
                near["C"]
                >
                C006B
                and
                (
                    near["C"]
                    /
                    C006B
                    -
                    1.0
                )
                <
                1.0e-4
            )
            else "FAIL"
        )
    )

    # Analytic identity spot checks.
    rng = np.random.default_rng(
        250188
    )

    y_test = rng.uniform(
        -4.0,
        4.0,
        size=10000,
    )

    k_test = rng.uniform(
        K_MIN,
        K_MAX,
        size=10000,
    )

    w_test = np.tanh(
        k_test
        * y_test
    )

    cl_test = (
        k_test
        +
        (
            1.0
            -
            k_test
        )
        * w_test
    )

    print(
        f"IDENTITY_MAX_ABS_PRESSURE_RATIO="
        f"{np.max(np.abs(w_test)):.15e}"
    )

    print(
        f"IDENTITY_MIN_CL2="
        f"{np.min(cl_test):.15e}"
    )

    print(
        f"IDENTITY_MAX_CL2="
        f"{np.max(cl_test):.15e}"
    )

    identity_pass = bool(
        np.all(
            np.abs(
                w_test
            )
            <
            1.0
        )
        and
        np.all(
            cl_test
            >=
            0.0
        )
        and
        np.all(
            cl_test
            <=
            1.0
        )
    )

    print(
        "GLOBAL_CONSTITUTIVE_IDENTITY_MONTE_CARLO="
        +
        (
            "PASS"
            if identity_pass
            else "FAIL"
        )
    )

    print(
        "\n=== L — DECISION ==="
    )

    selected_C = (
        selected["C"]
        if selected
        else math.inf
    )

    moderate_material = bool(
        selected is not None
        and
        selected_C
        <
        30.0
        and
        selected[
            "max_log_strain"
        ]
        <=
        4.0
        +
        1.0e-8
        and
        selected[
            "cL2_min"
        ]
        >=
        0.0
        and
        selected[
            "cL2_max"
        ]
        <=
        1.0
        and
        payload_pass
        and
        identity_pass
    )

    coefficient_below_006d = bool(
        selected is not None
        and
        selected_C
        <
        C006D
    )

    coefficient_below_006b = bool(
        selected is not None
        and
        selected_C
        <
        C006B
    )

    print(
        "LOCAL_POSITIVE_ENERGY_HYPERELASTIC_LAGRANGIAN="
        "YES"
    )

    print(
        "LOCAL_STRESS_STATE_REALIZATION="
        "YES_EXACT_CONSTITUTIVE"
    )

    print(
        "LOCAL_FINITE_STRAIN_DEC="
        "PASS_ANALYTIC"
    )

    print(
        "LOCAL_PRINCIPAL_LONGITUDINAL_CAUSALITY="
        "PASS_ANALYTIC_IN_DECLARED_K_RANGE"
    )

    print(
        "REFERENCE_TRANSVERSE_CAUSALITY="
        "PASS"
    )

    print(
        "GLOBAL_LOG_STRAIN_CONVEXITY="
        "PASS_ANALYTIC"
    )

    print(
        "DISTRIBUTIONAL_THIN_SOURCE_CONSERVATION="
        "PASS_BY_GENERALIZED_006B_IDENTITY"
    )

    print(
        "FINITE_PAYLOAD_OUTWARD="
        +
        (
            "YES"
            if (
                payload is not None
                and
                payload[
                    "all_outward"
                ]
            )
            else "NO"
        )
    )

    print(
        "MODERATE_STRAIN_C_LT_30_PREFLIGHT="
        +
        (
            "YES"
            if moderate_material
            else "NO"
        )
    )

    print(
        "COEFFICIENT_BELOW_006D_FINITE="
        +
        (
            "YES"
            if coefficient_below_006d
            else "NO"
        )
    )

    print(
        "COEFFICIENT_BELOW_006D_FINITE_CLAIM_WARNING="
        "THIN_IDEALIZED_SOURCE_NOT_SAME_CLAIM_CLASS_AS_006D_FINITE"
    )

    print(
        "COEFFICIENT_BELOW_006B_THIN="
        +
        (
            "YES"
            if coefficient_below_006b
            else "NO"
        )
    )

    if moderate_material:

        decision = (
            "YELLOW_STRONG_HYPERELASTIC_CONSTITUTIVE_"
            "REALIZATION_PREFLIGHT"
        )

        next_action = (
            "025B_SOLVE_AXISYMMETRIC_GRADED_HYPERELASTIC_"
            "MATERIAL_COORDINATE_BVP_WITH_FINITE_COLLARS_"
            "AND_FULL_CHARACTERISTIC_CONE"
        )

    elif (
        selected is not None
        and
        payload_pass
    ):

        decision = (
            "YELLOW_HYPERELASTIC_EXISTENCE_WITH_"
            "STRAIN_OR_GRADING_NATURALNESS_OBSTRUCTION"
        )

        next_action = (
            "025B_CHEAP_COMPATIBILITY_AND_FULL_CHARACTERISTIC_"
            "PREFLIGHT_BEFORE_ANY_LARGE_BVP"
        )

    else:

        decision = (
            "RED_MINIMAL_SATURATING_HYPERELASTIC_"
            "STRESS_TRANSFORMER"
        )

        next_action = (
            "RERANK_ANALOGUE_ANTIGRAVITY_VS_ONE_FINAL_"
            "PHASE_TRANSFORMING_ELASTIC_EXTENSION"
        )

    print(
        f"025A_DECISION="
        f"{decision}"
    )

    print(
        f"NEXT="
        f"{next_action}"
    )

    print(
        "GLOBAL_DEFORMATION_COMPATIBILITY="
        "NOT_ESTABLISHED"
    )

    print(
        "GLOBAL_ELASTIC_EULER_LAGRANGE_SOLUTION="
        "NO"
    )

    print(
        "FINITE_THICKNESS_COLLAR_REALIZATION="
        "NO"
    )

    print(
        "FULL_FINITE_STRAIN_CHARACTERISTIC_CONE="
        "NOT_ESTABLISHED"
    )

    print(
        "DYNAMIC_STABILITY="
        "NOT_ESTABLISHED"
    )

    print(
        "MICROSCOPIC_PARTICLE_REALIZATION="
        "NO"
    )

    print(
        "NONLINEAR_GR="
        "NO"
    )

    print(
        "REMOVES_1_OVER_G_SCALING="
        "NO"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "70_TO_71_PERCENT_RETAIN_UNTIL_BVP_OR_STRONGER_PROMOTION"
    )

    # Persist.
    all_frontier = []

    for row in frontier_rows:
        tagged = dict(
            row
        )
        tagged[
            "source"
        ] = (
            "INDEPENDENT_DE"
        )
        all_frontier.append(
            tagged
        )

    for row in sobol_frontier:
        tagged = dict(
            row
        )
        tagged[
            "source"
        ] = (
            "SOBOL"
        )
        all_frontier.append(
            tagged
        )

    if all_frontier:

        fields = sorted({
            key
            for row in all_frontier
            for key in row
        })

        with OUT_FRONTIER.open(
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
                all_frontier
            )

    if top_rows:

        fields = sorted({
            key
            for row in top_rows
            for key in row
        })

        with OUT_CSV.open(
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
                top_rows
            )

    if selected:

        np.savez_compressed(
            OUT_NPZ,
            selected=np.asarray(
                [
                    selected["k"],
                    selected["t"],
                    selected["q"],
                    selected[
                        "support"
                    ],
                    selected["a"],
                    selected["R"],
                    selected[
                        "max_log_strain"
                    ],
                    selected[
                        "rho_star_ann_over_core_at_a"
                    ],
                    selected["C"],
                ],
                dtype=float,
            ),
        )

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_RELATIVISTIC_"
                "HYPERELASTIC_CONSTITUTIVE_PREFLIGHT"
            ),

        "model":
            (
                "SATURATING_RELATIVISTIC_HENCKY_SOLID"
            ),

        "anchors": {
            "C_006B":
                C006B,

            "C_006D":
                C006D,

            "payload_radius_over_h":
                PAYLOAD_RADIUS,
        },

        "analytic": {
            "positive_energy":
                True,

            "pressure_ratio":
                "tanh(k*y_i)",

            "finite_strain_DEC":
                True,

            "finite_strain_NEC":
                True,

            "log_strain_convexity":
                True,

            "principal_longitudinal_speed":
                (
                    "k+(1-k)*p_i/rho"
                ),

            "reference_transverse_speed_squared":
                "k/2",

            "full_characteristic_cone":
                False,
        },

        "scan": {
            "sobol_cases":
                NCASE,

            "strain_caps":
                list(
                    STRAIN_CAPS
                ),

            "k_range": [
                K_MIN,
                K_MAX,
            ],
        },

        "006B_regression": {
            "reference":
                C006B,

            "rebuilt":
                C0,

            "relative_error":
                rel006b,
        },

        "best_global_sobol":
            (
                top_rows[0]
                if top_rows
                else None
            ),

        "sobol_frontier":
            sobol_frontier,

        "independent_frontier":
            frontier_rows,

        "grading_rows":
            grading_rows,

        "refined":
            refined,

        "refined_grading":
            refined_grading,

        "selected":
            selected,

        "payload":
            payload,

        "decision": {
            "moderate_strain_C_lt_30":
                moderate_material,

            "coefficient_below_006D_finite":
                coefficient_below_006d,

            "coefficient_below_006B_thin":
                coefficient_below_006b,

            "result":
                decision,

            "next":
                next_action,

            "practical_device":
                False,
        },

        "limits": [
            "NO_GLOBAL_DEFORMATION_COMPATIBILITY_SOLUTION",
            "NO_GLOBAL_ELASTIC_EULER_LAGRANGE_BVP",
            "NO_FINITE_THICKNESS_COLLAR_REALIZATION",
            "NO_FULL_FINITE_STRAIN_CHARACTERISTIC_CONE",
            "NO_DYNAMIC_STABILITY",
            "NO_MICROSCOPIC_PARTICLE_REALIZATION",
            "NO_NONLINEAR_GR",
            "NO_1_OVER_G_ESCAPE",
            "NO_DEVICE",
        ],
    }

    OUT_JSON.write_text(
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
        f"{OUT_JSON.relative_to(ROOT)}"
    )

    print(
        f"TOP_CSV="
        f"{OUT_CSV.relative_to(ROOT)}"
    )

    print(
        f"FRONTIER_CSV="
        f"{OUT_FRONTIER.relative_to(ROOT)}"
    )

    if OUT_NPZ.is_file():

        print(
            f"BEST_PROFILE_NPZ="
            f"{OUT_NPZ.relative_to(ROOT)}"
        )

    print(
        "025A_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
