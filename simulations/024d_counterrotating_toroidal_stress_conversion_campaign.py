#!/usr/bin/env python3
"""024D — counterrotating toroidal stress-conversion campaign.

PURPOSE
-------
Test whether the user's physical intuition that rapid circulation can create
large stress can be turned into a useful antigravity mechanism once the entire
stress-energy and confinement ledger is included.

This run does NOT assume that rotation itself creates repulsive gravity.

Instead it separates:

    CIRCULATION

    CONFINEMENT

    COLLISION / INTERACTION

    NEGATIVE-ACTIVE STRESS CONVERSION

    FULL-CYCLE VIRIAL COMPENSATION

    SPATIAL KERNEL LEVERAGE

    FINITE-PAYLOAD RESPONSE.

The campaign is intentionally broad and attempts to falsify the idea before
any new microscopic PDE is authorized.

SCIENTIFIC QUESTION
-------------------
Can two equal counterrotating field-energy packets moving around closed
toroidal channels use their large internal momentum flow and periodic
intersection to create a localized tension/potential-dominated state whose
finite-payload outward gravity survives:

    complete confinement energy,

    DEC,

    energy conservation,

    full-cycle stress-trace compensation,

    return/reset stress,

    spatial kernel weighting,

    finite payload,

    and realistic collision kinematics?

CORE DISTINCTION
----------------
Counterrotation cancels momentum but not stress.

For two equal cold counterstreams with total packet energy E_p and speed beta:

    T_0s,total = 0

but:

    P_stream = beta^2 E_p.

A stationary closed curved trajectory must provide compensating tension:

    P_guide = -beta^2 E_p.

DEC requires at least:

    E_guide >= |P_guide|
            = beta^2 E_p.

At the minimum:

    E_total
      =
    (1+beta^2) E_p.

The packet active source is:

    S_packet
      =
    (1+beta^2) E_p.

The minimum guide has:

    S_guide
      =
    E_guide + P_guide
      =
    0.

Therefore the complete minimum-support stationary counterflow has:

    S_total = E_total > 0.

Hence:

    COUNTERROTATION_ALONE_DOES_NOT_CREATE_NEGATIVE_ACTIVE_GRAVITY.

This is the first analytical gate.

LINEAR ELECTROMAGNETIC LIMIT
----------------------------
For a source-free Maxwell field:

    T^mu_mu = 0.

Therefore:

    p_x+p_y+p_z = rho

and:

    S_EM = rho + sum p_i = 2 rho > 0.

Pure linear electromagnetic circulation is therefore attractive in the
gravitoelectric source combination.

Any useful EM-based route would require another nonlinear / confining /
potential sector whose complete T_munu must be counted.

CANONICAL SCALAR CONVERTER
--------------------------
For a canonical scalar field:

    S
      =
    rho + p_x+p_y+p_z
      =
    2 phidot^2 - 2 V.

Spatial gradients cancel from this active-source trace combination.

Thus a potential-dominated interaction zone can reach:

    S/rho -> -2

at the DEC-saturating limit.

A kinetic-dominated scalar reset can reach the opposite DEC limit:

    trace(T_ij)/rho -> +3

and:

    S/rho -> +4.

This gives a natural idealized negative-phase / positive-reset pair.

FULL-CYCLE VIRIAL REPAIR
------------------------
For a closed isolated cycle whose quadrupole derivatives return to their
initial values:

    integral dt integral d^3x T_ii = 0.

The run therefore does NOT allow a negative-stress collision without an
explicit compensating positive-stress phase.

Let a fraction f of packet energy be converted during an interaction duty d.

Outside interaction, the packet trace per unit packet energy is:

    beta^2.

During conversion, let:

    S_conv / rho = -q

with:

    0 <= q <= 2.

Then the converted trace ratio is:

    -(q+1).

Relative to the circulating state, the trace change is:

    Delta_trace_int
      =
    -f (q+1+beta^2).

If the reset state has positive trace ratio chi_plus, then its positive
capacity relative to circulation is:

    chi_plus - beta^2.

The minimum reset duty required by the virial identity is:

    d_reset
      =
    d f (q+1+beta^2)
    /
    (chi_plus-beta^2).

This must satisfy:

    d_reset <= 1-d.

The most favorable DEC limit is:

    chi_plus = 3.

The negative and positive unweighted stress-time budgets then cancel exactly.
Only their DIFFERENT SPATIAL KERNELS can produce net useful impulse.

This is directly aligned with the project's permanent kernel-leverage
principle.

TOROIDAL / ORBIT GEOMETRY
-------------------------
The central path of each field channel is modeled by a vertical ellipse:

    x(theta) = a cos(theta)

    z(theta) = -b + b sin(theta).

The top point is always:

    z = 0,

directly below the payload.

The bottom point is:

    z = -2b.

The payload center is at:

    z = +h,

with:

    h = 1.

A second channel lies in another vertical plane.

The two channel planes intersect at the top and bottom points.

The angle between packet velocities at the top interaction is scanned.

Special cases:

    crossing angle = 180 degrees:
        head-on counterrotation,
        coincident / nearly coincident channels.

    crossing angle = 90 degrees:
        orthogonal toroidal channels.

The orbit aspect ratio:

    b/a

is scanned widely.

Large b/a produces a deep return path and strong spatial kernel leverage but
also strongly concentrated curvature, which increases the confinement burden.

CONSTANT-SPEED TIME WEIGHTING
-----------------------------
Packets are assumed to move at constant speed along arclength.

For the ellipse:

    ds/dtheta
      =
    sqrt(
        a^2 sin^2(theta)
        +
        b^2 cos^2(theta)
    ).

All cycle averages therefore use ds weighting rather than uniform theta.

PAYLOAD KERNEL
--------------
For an on-axis payload center at z=1:

    K(theta)
      =
    (1-z)
    /
    [r^2+(1-z)^2]^(3/2).

This positive quantity measures attraction produced by positive S.

The desired outward acceleration functional is:

    A_out
      =
    - < S K >.

Positive A_out is outward.

The interaction occurs near the high-kernel top point.

The mandatory positive reset is placed near the lowest-kernel bottom point.

FINITE PAYLOAD
--------------
Use the project's matched uniform spherical payload radius:

    R_P/h
      =
    0.043298860805059215.

Every modeled source lies at z<=0 while the payload sphere lies around z=1.

The complete payload sphere is therefore source-free.

Each acceleration component is harmonic inside it, so the mean-value theorem
gives exactly:

    a_CM = a(center).

The on-axis point result is therefore an exact finite spherical payload
center-of-mass result within this linearized source model.

MODEL FAMILIES
--------------
The same large low-discrepancy geometry/kinematic sample is tested under
several distinct physical ledgers.

1. IDEAL_DEC_SPINNING_CEILING

   beta = 1
   f = 1
   q = 2
   chi_plus = 3
   minimum circular-confinement energy
   no converter overhead.

   This is an absolute optimistic source-level ceiling.

   It is NOT a field realization.

2. CANONICAL_SCALAR_TRANSPORT

   Counterrotating transport plus a canonical-scalar-like potential converter.

   q is scanned from 0 to 2.

   f is scanned from 0 to 1.

   chi_plus = 3.

   Gradient/localization overhead is included in peak energy but is treated
   as active-neutral, which is favorable because canonical scalar gradients
   cancel from S.

   This tests whether circulation can transport an otherwise viable scalar
   stress converter.

3. MASSIVE_HEADON_COLLIDER

   Massive packets can convert no more than the collision center-of-momentum
   kinetic energy.

   For equal packet speed beta and crossing angle psi:

       f_COM,max
         =
       sqrt(
           1-beta^2 cos^2(psi/2)
       )
       -
       sqrt(
           1-beta^2
       ).

   At psi=pi:

       f_COM,max = 1-1/gamma.

   The actual converted fraction is:

       min(f_scan, f_COM,max).

   Structural converter overhead is positive-active.

4. MASSLESS_HYBRID_COLLIDER

   For massless equal-energy packets, the fraction of lab energy available as
   center-of-momentum invariant energy is bounded by:

       f_COM,max = sin(psi/2).

   beta = 1.

   A scalar-like nonlinear conversion/reset sector is still required because
   a pure radiation reset has the same trace ratio as the circulating
   massless field and cannot repair the negative trace excursion.

5. ELASTIC_VORTON_CONVERTER

   Same kinematic conversion limit as the massive packet family, but with a
   stronger curvature/confinement penalty to approximate an elastic
   current-carrying ring rather than an ideal external track.

   This is a generic vorton-like bound.

   It is NOT the old 018B KLS model.

ANALYTIC CLOSED FAMILIES
------------------------
The following are recorded without numerical promotion:

    PURE_COUNTERROTATION_NO_CONVERTER:
        RED

    PURE_LINEAR_EM_COUNTERROTATION:
        RED

    FREE_STATIONARY_VORTON_WITHOUT_NEGATIVE_CONVERTER:
        positive active source at the local equilibrium level.

The existence of stable vortons in the literature does not change these
active-source identities.

CURVATURE / CONFINEMENT PENALTY
-------------------------------
For a convex ellipse:

    kappa_max
      =
    max(
        a/b^2,
        b/a^2
    ).

Its average curvature by total turning is:

    kappa_mean = 2 pi / L.

Define:

    curvature_concentration
      =
    kappa_max / kappa_mean
      >=
    1.

Different families apply:

    no shape penalty,
    sqrt(curvature_concentration),
    or
    curvature_concentration^0.75

to the minimum guide energy.

This prevents arbitrarily deep needle-like orbits from receiving free
confinement.

The no-penalty DEC family remains as an explicit optimistic ceiling.

SOURCE COEFFICIENT
------------------
Normalize total moving-packet energy to:

    E_packet = 1.

Guide and converter overhead are then added explicitly.

For cycle-average outward acceleration A_avg:

    C_cycle = E_peak / A_avg.

Lower is better.

Compare against:

    C_006D
      =
    23.591586299249.

This is a source/inventory efficiency comparator.

It does NOT remove the absolute 1/G scaling of pure GR.

INTERACTION DUTY CLASSIFICATION
-------------------------------
A true collision-like mechanism should be localized in time.

Classify:

    d <= 0.10:
        SHORT_COLLISION

    0.10 < d <= 0.20:
        PULSE_LIKE

    0.20 < d <= 0.35:
        BROAD_INTERACTION

    d > 0.35:
        QUASISTATIC_CONVERTER.

A result that beats 006D only by spending most of the orbit in the negative
state is not evidence that "spin collisions" are the mechanism.

It would instead indicate a transported static stress converter.

SCAN
----
Use a scrambled Sobol sequence with:

    2^19 = 524,288 base cases.

Each base case is evaluated under multiple physical families.

Scanned variables:

    a/h:
        0.4 to 8, logarithmic

    b/a:
        0.5 to 4, logarithmic

    beta:
        0.05 to 0.9995

    crossing angle:
        30 to 180 degrees

    q:
        0 to 2

    nominal conversion fraction:
        0 to 1

    interaction half-angle:
        0.02 to 1.25 rad, logarithmic

    guide multiplier:
        1 to 4

    converter overhead / packet energy:
        0 to 1.5

    cycle loss diagnostic:
        0 to 0.5.

The user-requested blind values:

    0.625
    1.6
    1.875
    3.125
    5

are tested separately as a/h values.

They are:

    BLIND_WILDCARD_NOT_PHYSICS_PRIOR.

REFINEMENT
----------
The top coarse candidates from every family are recomputed with:

    32768 phase samples.

Unlike the coarse scan, which gives the positive reset the exact bottom-point
kernel as an optimistic upper bound, refinement constructs a finite contiguous
bottom reset window whose arclength duty equals the required virial
compensation duty.

Thus a candidate can lose promotion during refinement.

DIRECTIONAL / PLANAR AUDIT
--------------------------
For the best refined candidate in every family, construct both toroidal
channels explicitly in 3-D.

Evaluate the cycle-averaged vector acceleration over:

    target radii:
        0
        0.125
        0.25
        0.375
        0.5

and multiple target-plane azimuths.

Report:

    all axial signs,
    axial flatness,
    maximum transverse / axial ratio,
    on-axis agreement with the scalar kernel calculation.

This is a secondary morphology diagnostic.

The primary 024D question is whether the stress-conversion mechanism exists.

SPIN-DEPENDENCE AUDIT
---------------------
Take the best scalar-transport geometry and hold its geometry/conversion
parameters fixed while sweeping beta.

Perform two curves:

    UNRESTRICTED_CONVERSION

and

    KINETIC_COM_LIMITED_CONVERSION.

This directly answers:

    DOES MORE SPIN IMPROVE STRESS PER TOTAL CONSERVED ENERGY?

Possible interpretations:

    UNRESTRICTED optimum at low beta:
        spin is an overhead, not the antigravity mechanism.

    KINETIC_LIMITED optimum at high beta:
        spin can be an enabler because it supplies convertible COM energy.

    both improve strongly with beta:
        genuine spin leverage survives the confinement ledger.

RETURN / LOSS ROBUSTNESS
------------------------
For every refined source with positive A, report coefficients after hypothetical
additional useful-impulse losses of:

    10%
    25%
    50%.

These are NOT substitutes for a dynamic field calculation.

They quantify how much omitted radiation/reaction/reset loss can be tolerated.

PROMOTION CONDITION
-------------------
A kinematically constrained 024D survivor requires:

    refined cycle-average A > 0;

    exact virial reset duty feasible;

    refined finite reset window included;

    C_refined < C_006D;

    finite-payload source-free condition pass;

    no omitted minimum confinement energy;

    family is not IDEAL_DEC_SPINNING_CEILING;

    family is not unrestricted CANONICAL_SCALAR_TRANSPORT unless a later
    microscopic interaction field is supplied.

A true "counterrotation helps" interpretation additionally requires:

    beta >= 0.5

and:

    conversion is limited by collision kinematics

and:

    interaction duty <= 0.20.

FALSIFIERS
----------
If even the ideal DEC spinning ceiling cannot beat 006D:

    kill the orbital stress-conversion branch immediately.

If only the ideal or unrestricted scalar family beats 006D:

    conclude that stress conversion / kernel leverage is interesting but
    counterrotation itself has not earned promotion.

If collision-limited families produce positive average response but cannot
beat 006D:

    retain as mechanism information only.

If a collision-limited family beats 006D but requires:

    d > 0.35

or:

    extreme curvature concentration

or:

    near-perfect q=2 and f=1

then classify it as a demanding transported converter rather than a practical
collision mechanism.

STOP RULE
---------
Do not launch a microscopic toroidal PDE merely because one relaxed source
case is positive.

A microscopic 024D successor is authorized only if a constrained family
survives the refined full-cycle ledger with a meaningful margin or if the run
identifies a sharply defined scalar/gauge interaction worth testing
analytically.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_COUNTERROTATING_TOROIDAL_STRESS_CONVERSION_PREFILTER

DOES NOT ESTABLISH
------------------
- a microscopic new field solution;
- stability;
- nonlinear GR;
- favorable absolute energy scaling;
- experimental antigravity;
- reactionless propulsion;
- a practical device.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "results/data"

B3_SUMMARY = (
    DATA
    / "024b3_free_outward_annular_wall_pulse_summary.json"
)

C1_SUMMARY = (
    DATA
    / "024c1_intuitive_guarded_stress_sandwich_summary.json"
)

OUT_SUMMARY = (
    DATA
    / "024d_counterrotating_toroidal_stress_conversion_summary.json"
)

OUT_TOP = (
    DATA
    / "024d_counterrotating_toroidal_stress_conversion_top.csv"
)

OUT_BETA = (
    DATA
    / "024d_counterrotating_toroidal_beta_sweeps.csv"
)

OUT_NPZ = (
    DATA
    / "024d_counterrotating_toroidal_best_profiles.npz"
)


C006D = 23.591586299249

PAYLOAD_RADIUS_OVER_H = 0.043298860805059215

SOBOL_POWER = 19
N_CASES = 2 ** SOBOL_POWER

COARSE_NPHASE = 256
REFINE_NPHASE = 32768
VECTOR_NPHASE = 8192

BATCH = 2048
TOP_PER_FAMILY = 40

BETA_SPIN_THRESHOLD = 0.50
PULSE_DUTY_MAX = 0.20

BLIND_WILDCARDS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)

FAMILY_NAMES = (
    "IDEAL_DEC_SPINNING_CEILING",
    "CANONICAL_SCALAR_TRANSPORT",
    "MASSIVE_HEADON_COLLIDER",
    "MASSLESS_HYBRID_COLLIDER",
    "ELASTIC_VORTON_CONVERTER",
)


def require(
    path: Path,
) -> None:
    """Require one input artifact."""

    if not path.is_file():
        raise RuntimeError(
            f"Required input missing: {path}"
        )


def relative_error(
    a: float,
    b: float,
) -> float:
    """Stable relative error."""

    return (
        abs(
            a - b
        )
        /
        max(
            abs(a),
            abs(b),
            1.0e-300,
        )
    )


def wrapped_distance(
    theta: np.ndarray,
    center: float,
) -> np.ndarray:
    """Shortest angular distance."""

    return np.abs(
        (
            theta
            - center
            + math.pi
        )
        %
        (
            2.0
            * math.pi
        )
        - math.pi
    )


def duty_class(
    duty: float,
) -> str:
    """Human-readable interaction-duty class."""

    if duty <= 0.10:
        return "SHORT_COLLISION"

    if duty <= 0.20:
        return "PULSE_LIKE"

    if duty <= 0.35:
        return "BROAD_INTERACTION"

    return "QUASISTATIC_CONVERTER"


def build_sobol_parameters() -> dict[str, np.ndarray]:
    """Generate the common low-discrepancy campaign."""

    sampler = qmc.Sobol(
        d=10,
        scramble=True,
        seed=240024,
    )

    u = sampler.random_base2(
        SOBOL_POWER
    )

    a = 10.0 ** (
        math.log10(
            0.4
        )
        +
        (
            math.log10(
                8.0
            )
            -
            math.log10(
                0.4
            )
        )
        * u[
            :,
            0
        ]
    )

    aspect = 10.0 ** (
        math.log10(
            0.5
        )
        +
        (
            math.log10(
                4.0
            )
            -
            math.log10(
                0.5
            )
        )
        * u[
            :,
            1
        ]
    )

    b = (
        a
        * aspect
    )

    beta = (
        0.05
        +
        (
            0.9995
            - 0.05
        )
        * u[
            :,
            2
        ]
    )

    psi = (
        math.radians(
            30.0
        )
        +
        (
            math.pi
            -
            math.radians(
                30.0
            )
        )
        * u[
            :,
            3
        ]
    )

    q = (
        2.0
        * u[
            :,
            4
        ]
    )

    f_raw = u[
        :,
        5
    ]

    halfwidth = np.exp(
        math.log(
            0.02
        )
        +
        (
            math.log(
                1.25
            )
            -
            math.log(
                0.02
            )
        )
        * u[
            :,
            6
        ]
    )

    guide_multiplier = (
        1.0
        +
        3.0
        * u[
            :,
            7
        ]
    )

    overhead = (
        1.5
        * u[
            :,
            8
        ]
    )

    loss = (
        0.5
        * u[
            :,
            9
        ]
    )

    return {
        "a":
            a,

        "b":
            b,

        "aspect":
            aspect,

        "beta":
            beta,

        "psi":
            psi,

        "q":
            q,

        "f_raw":
            f_raw,

        "halfwidth":
            halfwidth,

        "guide_multiplier":
            guide_multiplier,

        "overhead":
            overhead,

        "loss":
            loss,
    }


def coarse_geometry_features(
    parameters: dict[str, np.ndarray],
) -> dict[str, np.ndarray]:
    """Compute arclength-weighted orbital kernel features in batches."""

    a_all = parameters[
        "a"
    ]

    b_all = parameters[
        "b"
    ]

    hw_all = parameters[
        "halfwidth"
    ]

    n = len(
        a_all
    )

    k_avg = np.empty(
        n,
        dtype=float,
    )

    duty = np.empty_like(
        k_avg
    )

    k_interaction = np.empty_like(
        k_avg
    )

    perimeter = np.empty_like(
        k_avg
    )

    curvature_concentration = np.empty_like(
        k_avg
    )

    theta = np.linspace(
        0.0,
        2.0
        * math.pi,
        COARSE_NPHASE,
        endpoint=False,
        dtype=float,
    )

    sin_theta = np.sin(
        theta
    )[None, :]

    cos_theta = np.cos(
        theta
    )[None, :]

    top_distance = wrapped_distance(
        theta,
        0.5
        * math.pi,
    )[None, :]

    dtheta = (
        2.0
        * math.pi
        / COARSE_NPHASE
    )

    for start in range(
        0,
        n,
        BATCH,
    ):

        stop = min(
            start
            + BATCH,
            n,
        )

        a = a_all[
            start:stop
        ][
            :,
            None
        ]

        b = b_all[
            start:stop
        ][
            :,
            None
        ]

        hw = hw_all[
            start:stop
        ][
            :,
            None
        ]

        ds_dtheta = np.sqrt(
            (
                a
                * sin_theta
            ) ** 2
            +
            (
                b
                * cos_theta
            ) ** 2
        )

        x = (
            a
            * cos_theta
        )

        z = (
            b
            * (
                sin_theta
                - 1.0
            )
        )

        dz_payload = (
            1.0
            - z
        )

        kernel = (
            dz_payload
            /
            (
                x
                * x
                +
                dz_payload
                * dz_payload
            ) ** 1.5
        )

        total_weight = np.sum(
            ds_dtheta,
            axis=1,
        )

        k_avg[
            start:stop
        ] = (
            np.sum(
                kernel
                * ds_dtheta,
                axis=1,
            )
            /
            total_weight
        )

        mask = (
            top_distance
            <= hw
        )

        top_weight = (
            ds_dtheta
            * mask
        )

        top_weight_sum = np.sum(
            top_weight,
            axis=1,
        )

        duty[
            start:stop
        ] = (
            top_weight_sum
            /
            total_weight
        )

        k_interaction[
            start:stop
        ] = (
            np.sum(
                kernel
                * top_weight,
                axis=1,
            )
            /
            np.maximum(
                top_weight_sum,
                1.0e-300,
            )
        )

        L = (
            total_weight
            * dtheta
        )

        perimeter[
            start:stop
        ] = L

        a1 = a[
            :,
            0
        ]

        b1 = b[
            :,
            0
        ]

        kappa_max = np.maximum(
            a1
            /
            (
                b1
                * b1
            ),
            b1
            /
            (
                a1
                * a1
            ),
        )

        kappa_mean = (
            2.0
            * math.pi
            /
            L
        )

        curvature_concentration[
            start:stop
        ] = (
            kappa_max
            /
            kappa_mean
        )

    # Exact bottom point:
    #
    # r=0,
    # z=-2b,
    #
    # so K_bottom = 1/(1+2b)^2.

    k_bottom = (
        1.0
        /
        (
            1.0
            +
            2.0
            * parameters[
                "b"
            ]
        ) ** 2
    )

    return {
        "k_avg":
            k_avg,

        "duty":
            duty,

        "k_interaction":
            k_interaction,

        "k_bottom":
            k_bottom,

        "perimeter":
            perimeter,

        "curvature_concentration":
            curvature_concentration,
    }


def massive_com_fraction(
    beta: np.ndarray,
    psi: np.ndarray,
) -> np.ndarray:
    """Maximum massive-packet COM internal-energy fraction."""

    gamma_inverse = np.sqrt(
        np.maximum(
            0.0,
            1.0
            - beta
            * beta,
        )
    )

    invariant_fraction = np.sqrt(
        np.maximum(
            0.0,
            1.0
            -
            beta
            * beta
            * np.cos(
                0.5
                * psi
            ) ** 2,
        )
    )

    return np.maximum(
        0.0,
        invariant_fraction
        - gamma_inverse,
    )


def evaluate_family(
    family: str,
    p: dict[str, np.ndarray],
    g: dict[str, np.ndarray],
) -> dict[str, np.ndarray]:
    """Evaluate one complete family on the common sample."""

    beta_scan = p[
        "beta"
    ]

    psi = p[
        "psi"
    ]

    q_scan = p[
        "q"
    ]

    f_raw = p[
        "f_raw"
    ]

    curvature = np.maximum(
        g[
            "curvature_concentration"
        ],
        1.0,
    )

    guide_mult = p[
        "guide_multiplier"
    ]

    overhead_scan = p[
        "overhead"
    ]

    if family == "IDEAL_DEC_SPINNING_CEILING":

        beta = np.ones_like(
            beta_scan
        )

        q = np.full_like(
            beta,
            2.0,
        )

        f = np.ones_like(
            beta
        )

        guide_factor = np.ones_like(
            beta
        )

        overhead = np.zeros_like(
            beta
        )

        overhead_active_ratio = 0.0

        chi_plus = 3.0

    elif family == "CANONICAL_SCALAR_TRANSPORT":

        beta = beta_scan

        q = q_scan

        f = f_raw

        guide_factor = (
            (
                1.0
                +
                1.0
                * (
                    guide_mult
                    - 1.0
                )
                / 3.0
            )
            *
            np.sqrt(
                curvature
            )
        )

        overhead = (
            overhead_scan
        )

        # Canonical spatial gradients are active-neutral in S.
        overhead_active_ratio = 0.0

        chi_plus = 3.0

    elif family == "MASSIVE_HEADON_COLLIDER":

        beta = beta_scan

        q = q_scan

        f_cap = massive_com_fraction(
            beta,
            psi,
        )

        f = np.minimum(
            f_raw,
            f_cap,
        )

        guide_factor = (
            guide_mult
            *
            np.sqrt(
                curvature
            )
        )

        overhead = (
            0.25
            +
            1.25
            * overhead_scan
            / 1.5
        )

        overhead_active_ratio = 1.0

        chi_plus = 3.0

    elif family == "MASSLESS_HYBRID_COLLIDER":

        beta = np.ones_like(
            beta_scan
        )

        q = q_scan

        f_cap = np.sin(
            0.5
            * psi
        )

        f = np.minimum(
            f_raw,
            f_cap,
        )

        guide_factor = (
            guide_mult
            *
            np.sqrt(
                curvature
            )
        )

        overhead = (
            0.25
            +
            1.25
            * overhead_scan
            / 1.5
        )

        # Favorable hybrid scalar localization overhead.
        overhead_active_ratio = 0.0

        chi_plus = 3.0

    elif family == "ELASTIC_VORTON_CONVERTER":

        beta = beta_scan

        q = q_scan

        f_cap = massive_com_fraction(
            beta,
            psi,
        )

        f = np.minimum(
            f_raw,
            f_cap,
        )

        guide_factor = (
            guide_mult
            *
            curvature ** 0.75
        )

        overhead = (
            0.50
            +
            1.50
            * overhead_scan
            / 1.5
        )

        overhead_active_ratio = 0.0

        chi_plus = 3.0

    else:
        raise RuntimeError(
            f"Unknown family: {family}"
        )

    beta_sq = (
        beta
        * beta
    )

    # Packet + complete guide baseline.
    #
    # Minimum guide energy beta^2.
    # Shape / implementation overhead increases guide energy.
    #
    # Guide tension still cancels the packet hoop stress, so extra guide
    # energy contributes ordinary positive active source.

    baseline_active = (
        1.0
        +
        guide_factor
        * beta_sq
    )

    inventory_energy = (
        1.0
        +
        guide_factor
        * beta_sq
        +
        overhead
    )

    conversion_trace_amplitude = (
        f
        *
        (
            q
            +
            1.0
            +
            beta_sq
        )
    )

    reset_capacity = (
        chi_plus
        -
        beta_sq
    )

    reset_duty = np.divide(
        g[
            "duty"
        ]
        *
        conversion_trace_amplitude,
        reset_capacity,
        out=np.full_like(
            beta,
            np.inf,
        ),
        where=(
            reset_capacity
            >
            1.0e-12
        ),
    )

    virial_feasible = (
        reset_duty
        <=
        (
            1.0
            -
            g[
                "duty"
            ]
        )
    )

    # Coarse scan gives the reset the exact bottom-point kernel.
    # This is deliberately optimistic.
    #
    # Refinement replaces this by a finite bottom window.

    conversion_gain = (
        g[
            "duty"
        ]
        *
        conversion_trace_amplitude
        *
        (
            g[
                "k_interaction"
            ]
            -
            g[
                "k_bottom"
            ]
        )
    )

    overhead_attraction = (
        g[
            "duty"
        ]
        *
        overhead_active_ratio
        *
        overhead
        *
        g[
            "k_interaction"
        ]
    )

    average_outward = (
        -
        baseline_active
        *
        g[
            "k_avg"
        ]
        +
        conversion_gain
        -
        overhead_attraction
    )

    coefficient = np.where(
        virial_feasible
        &
        (
            average_outward
            > 0.0
        ),
        inventory_energy
        /
        average_outward,
        np.inf,
    )

    packet_active_during_interaction = (
        (
            1.0
            -
            f
        )
        *
        (
            1.0
            +
            beta_sq
        )
        -
        q
        * f
    )

    negative_packet_during_interaction = (
        packet_active_during_interaction
        <
        0.0
    )

    interaction_arc_length = (
        g[
            "duty"
        ]
        *
        g[
            "perimeter"
        ]
    )

    return {
        "beta":
            beta,

        "q":
            q,

        "f":
            f,

        "guide_factor":
            guide_factor,

        "overhead":
            overhead,

        "overhead_active_ratio":
            np.full_like(
                beta,
                overhead_active_ratio,
            ),

        "chi_plus":
            np.full_like(
                beta,
                chi_plus,
            ),

        "baseline_active":
            baseline_active,

        "inventory_energy":
            inventory_energy,

        "conversion_trace_amplitude":
            conversion_trace_amplitude,

        "reset_capacity":
            reset_capacity,

        "reset_duty":
            reset_duty,

        "virial_feasible":
            virial_feasible,

        "conversion_gain":
            conversion_gain,

        "average_outward":
            average_outward,

        "coefficient":
            coefficient,

        "packet_active_during_interaction":
            packet_active_during_interaction,

        "negative_packet_during_interaction":
            negative_packet_during_interaction,

        "interaction_arc_length":
            interaction_arc_length,
    }


def top_indices(
    coefficient: np.ndarray,
    count: int,
) -> np.ndarray:
    """Indices of the lowest finite coefficients."""

    finite = np.flatnonzero(
        np.isfinite(
            coefficient
        )
    )

    if len(
        finite
    ) == 0:
        return np.asarray(
            [],
            dtype=int,
        )

    if len(
        finite
    ) <= count:
        return finite[
            np.argsort(
                coefficient[
                    finite
                ]
            )
        ]

    local = np.argpartition(
        coefficient[
            finite
        ],
        count - 1,
    )[
        :count
    ]

    selected = finite[
        local
    ]

    return selected[
        np.argsort(
            coefficient[
                selected
            ]
        )
    ]


def highres_orbit(
    a: float,
    b: float,
    halfwidth: float,
    nphase: int,
) -> dict[str, np.ndarray | float]:
    """High-resolution time-weighted ellipse kernel."""

    theta = np.linspace(
        0.0,
        2.0
        * math.pi,
        nphase,
        endpoint=False,
        dtype=float,
    )

    sin_t = np.sin(
        theta
    )

    cos_t = np.cos(
        theta
    )

    ds = np.sqrt(
        (
            a
            * sin_t
        ) ** 2
        +
        (
            b
            * cos_t
        ) ** 2
    )

    weights = (
        ds
        /
        np.sum(
            ds
        )
    )

    x = (
        a
        * cos_t
    )

    z = (
        b
        * (
            sin_t
            - 1.0
        )
    )

    dz = (
        1.0
        - z
    )

    kernel = (
        dz
        /
        (
            x
            * x
            +
            dz
            * dz
        ) ** 1.5
    )

    top_mask = (
        wrapped_distance(
            theta,
            0.5
            * math.pi,
        )
        <=
        halfwidth
    )

    top_duty = float(
        np.sum(
            weights[
                top_mask
            ]
        )
    )

    top_kernel = float(
        np.sum(
            weights[
                top_mask
            ]
            * kernel[
                top_mask
            ]
        )
        /
        max(
            top_duty,
            1.0e-300,
        )
    )

    return {
        "theta":
            theta,

        "weights":
            weights,

        "x":
            x,

        "z":
            z,

        "kernel":
            kernel,

        "top_mask":
            top_mask,

        "top_duty":
            top_duty,

        "top_kernel":
            top_kernel,

        "k_avg":
            float(
                np.sum(
                    weights
                    * kernel
                )
            ),

        "perimeter":
            float(
                2.0
                * math.pi
                * np.mean(
                    ds
                )
            ),
    }


def bottom_window_for_duty(
    orbit: dict[str, np.ndarray | float],
    target_duty: float,
) -> tuple[
    np.ndarray,
    float,
    float,
]:
    """Construct a contiguous bottom window with requested arclength duty."""

    theta = np.asarray(
        orbit[
            "theta"
        ],
        dtype=float,
    )

    weights = np.asarray(
        orbit[
            "weights"
        ],
        dtype=float,
    )

    kernel = np.asarray(
        orbit[
            "kernel"
        ],
        dtype=float,
    )

    if target_duty <= 0.0:

        mask = np.zeros_like(
            theta,
            dtype=bool,
        )

        return (
            mask,
            0.0,
            float(
                np.min(
                    kernel
                )
            ),
        )

    lo = 0.0
    hi = math.pi

    for _ in range(
        60
    ):

        mid = (
            0.5
            * (
                lo
                +
                hi
            )
        )

        mask = (
            wrapped_distance(
                theta,
                1.5
                * math.pi,
            )
            <= mid
        )

        duty = float(
            np.sum(
                weights[
                    mask
                ]
            )
        )

        if duty < target_duty:
            lo = mid
        else:
            hi = mid

    mask = (
        wrapped_distance(
            theta,
            1.5
            * math.pi,
        )
        <= hi
    )

    duty = float(
        np.sum(
            weights[
                mask
            ]
        )
    )

    k = float(
        np.sum(
            weights[
                mask
            ]
            * kernel[
                mask
            ]
        )
        /
        max(
            duty,
            1.0e-300,
        )
    )

    return (
        mask,
        duty,
        k,
    )


def scalar_family_parameters(
    family: str,
    index: int,
    p: dict[str, np.ndarray],
    g: dict[str, np.ndarray],
    result: dict[str, np.ndarray],
) -> dict[str, float]:
    """Extract all scalar parameters for one candidate."""

    return {
        "a":
            float(
                p[
                    "a"
                ][
                    index
                ]
            ),

        "b":
            float(
                p[
                    "b"
                ][
                    index
                ]
            ),

        "aspect":
            float(
                p[
                    "aspect"
                ][
                    index
                ]
            ),

        "psi":
            float(
                p[
                    "psi"
                ][
                    index
                ]
            ),

        "halfwidth":
            float(
                p[
                    "halfwidth"
                ][
                    index
                ]
            ),

        "loss":
            float(
                p[
                    "loss"
                ][
                    index
                ]
            ),

        "curvature_concentration":
            float(
                g[
                    "curvature_concentration"
                ][
                    index
                ]
            ),

        "beta":
            float(
                result[
                    "beta"
                ][
                    index
                ]
            ),

        "q":
            float(
                result[
                    "q"
                ][
                    index
                ]
            ),

        "f":
            float(
                result[
                    "f"
                ][
                    index
                ]
            ),

        "guide_factor":
            float(
                result[
                    "guide_factor"
                ][
                    index
                ]
            ),

        "overhead":
            float(
                result[
                    "overhead"
                ][
                    index
                ]
            ),

        "overhead_active_ratio":
            float(
                result[
                    "overhead_active_ratio"
                ][
                    index
                ]
            ),

        "chi_plus":
            float(
                result[
                    "chi_plus"
                ][
                    index
                ]
            ),

        "coarse_C":
            float(
                result[
                    "coefficient"
                ][
                    index
                ]
            ),

        "family":
            family,
    }


def refine_candidate(
    candidate: dict[str, float],
) -> dict[str, Any]:
    """Replace point-bottom reset by a finite contiguous bottom reset."""

    orbit = highres_orbit(
        candidate[
            "a"
        ],
        candidate[
            "b"
        ],
        candidate[
            "halfwidth"
        ],
        REFINE_NPHASE,
    )

    beta = candidate[
        "beta"
    ]

    q = candidate[
        "q"
    ]

    f = candidate[
        "f"
    ]

    guide_factor = candidate[
        "guide_factor"
    ]

    overhead = candidate[
        "overhead"
    ]

    overhead_active_ratio = candidate[
        "overhead_active_ratio"
    ]

    chi_plus = candidate[
        "chi_plus"
    ]

    beta_sq = (
        beta
        * beta
    )

    D = (
        f
        *
        (
            q
            +
            1.0
            +
            beta_sq
        )
    )

    cap = (
        chi_plus
        -
        beta_sq
    )

    top_duty = float(
        orbit[
            "top_duty"
        ]
    )

    if cap <= 1.0e-12:

        reset_duty_required = math.inf

    else:

        reset_duty_required = (
            top_duty
            * D
            / cap
        )

    virial_feasible = bool(
        reset_duty_required
        <=
        1.0
        -
        top_duty
    )

    if virial_feasible:

        (
            bottom_mask,
            bottom_duty,
            bottom_kernel,
        ) = bottom_window_for_duty(
            orbit,
            reset_duty_required,
        )

    else:

        theta = np.asarray(
            orbit[
                "theta"
            ]
        )

        bottom_mask = np.zeros_like(
            theta,
            dtype=bool,
        )

        bottom_duty = math.nan
        bottom_kernel = math.nan

    baseline_active = (
        1.0
        +
        guide_factor
        * beta_sq
    )

    inventory_energy = (
        1.0
        +
        guide_factor
        * beta_sq
        +
        overhead
    )

    if virial_feasible:

        conversion_gain = (
            top_duty
            * D
            * float(
                orbit[
                    "top_kernel"
                ]
            )
            -
            bottom_duty
            * cap
            * bottom_kernel
        )

        overhead_attraction = (
            top_duty
            *
            overhead_active_ratio
            *
            overhead
            *
            float(
                orbit[
                    "top_kernel"
                ]
            )
        )

        A = (
            -
            baseline_active
            *
            float(
                orbit[
                    "k_avg"
                ]
            )
            +
            conversion_gain
            -
            overhead_attraction
        )

    else:

        conversion_gain = -math.inf
        overhead_attraction = math.inf
        A = -math.inf

    C = (
        inventory_energy
        / A
        if (
            virial_feasible
            and A > 0.0
        )
        else math.inf
    )

    packet_active_interaction = (
        (
            1.0
            -
            f
        )
        *
        (
            1.0
            +
            beta_sq
        )
        -
        q
        * f
    )

    interaction_arc_length = (
        top_duty
        * float(
            orbit[
                "perimeter"
            ]
        )
    )

    if math.isfinite(
        C
    ):

        c_loss10 = (
            C
            / 0.90
        )

        c_loss25 = (
            C
            / 0.75
        )

        c_loss50 = (
            C
            / 0.50
        )

        max_loss_to_006d = max(
            0.0,
            1.0
            -
            C
            / C006D,
        )

    else:

        c_loss10 = math.inf
        c_loss25 = math.inf
        c_loss50 = math.inf
        max_loss_to_006d = 0.0

    return {
        **candidate,

        "orbit":
            orbit,

        "bottom_mask":
            bottom_mask,

        "bottom_duty":
            bottom_duty,

        "bottom_kernel":
            bottom_kernel,

        "top_duty":
            top_duty,

        "top_kernel":
            float(
                orbit[
                    "top_kernel"
                ]
            ),

        "k_avg":
            float(
                orbit[
                    "k_avg"
                ]
            ),

        "reset_duty_required":
            reset_duty_required,

        "virial_feasible_refined":
            virial_feasible,

        "baseline_active":
            baseline_active,

        "inventory_energy":
            inventory_energy,

        "conversion_gain_refined":
            conversion_gain,

        "overhead_attraction_refined":
            overhead_attraction,

        "A_refined":
            A,

        "C_refined":
            C,

        "packet_active_interaction":
            packet_active_interaction,

        "negative_packet_interaction":
            bool(
                packet_active_interaction
                <
                0.0
            ),

        "interaction_arc_length_over_h":
            interaction_arc_length,

        "duty_class":
            duty_class(
                top_duty
            ),

        "C_after_10pct_impulse_loss":
            c_loss10,

        "C_after_25pct_impulse_loss":
            c_loss25,

        "C_after_50pct_impulse_loss":
            c_loss50,

        "max_additional_impulse_loss_to_still_beat_006D":
            max_loss_to_006d,
    }


def vector_audit(
    refined: dict[str, Any],
) -> dict[str, Any]:
    """Cycle-average vector field for two intersecting toroidal channels."""

    orbit = highres_orbit(
        refined[
            "a"
        ],
        refined[
            "b"
        ],
        refined[
            "halfwidth"
        ],
        VECTOR_NPHASE,
    )

    theta = np.asarray(
        orbit[
            "theta"
        ],
        dtype=float,
    )

    weights = np.asarray(
        orbit[
            "weights"
        ],
        dtype=float,
    )

    top_mask = np.asarray(
        orbit[
            "top_mask"
        ],
        dtype=bool,
    )

    (
        bottom_mask,
        bottom_duty,
        _bottom_kernel,
    ) = bottom_window_for_duty(
        orbit,
        refined[
            "reset_duty_required"
        ],
    )

    beta = refined[
        "beta"
    ]

    D = (
        refined[
            "f"
        ]
        *
        (
            refined[
                "q"
            ]
            +
            1.0
            +
            beta
            * beta
        )
    )

    cap = (
        refined[
            "chi_plus"
        ]
        -
        beta
        * beta
    )

    source_phase = np.full(
        len(
            theta
        ),
        refined[
            "baseline_active"
        ],
        dtype=float,
    )

    source_phase[
        top_mask
    ] -= D

    source_phase[
        bottom_mask
    ] += cap

    source_phase[
        top_mask
    ] += (
        refined[
            "overhead_active_ratio"
        ]
        *
        refined[
            "overhead"
        ]
    )

    # Two vertical planes.
    #
    # The velocity crossing angle psi is produced by choosing plane separation
    # delta = pi-psi with opposite propagation directions.

    delta = (
        math.pi
        -
        refined[
            "psi"
        ]
    )

    plane_angles = (
        -0.5
        * delta,
        +0.5
        * delta,
    )

    a = refined[
        "a"
    ]

    b = refined[
        "b"
    ]

    radial_coordinate = (
        a
        * np.cos(
            theta
        )
    )

    z_source = (
        b
        * (
            np.sin(
                theta
            )
            - 1.0
        )
    )

    target_radii = np.asarray(
        [
            0.0,
            0.125,
            0.25,
            0.375,
            0.5,
        ],
        dtype=float,
    )

    target_azimuths = np.linspace(
        0.0,
        math.pi,
        9,
        endpoint=False,
    )

    rows = []

    for target_r in target_radii:

        az_values = []
        transverse_values = []

        for target_phi in target_azimuths:

            tx = (
                target_r
                * math.cos(
                    target_phi
                )
            )

            ty = (
                target_r
                * math.sin(
                    target_phi
                )
            )

            tz = 1.0

            acc = np.zeros(
                3,
                dtype=float,
            )

            for plane_angle in plane_angles:

                ux = math.cos(
                    plane_angle
                )

                uy = math.sin(
                    plane_angle
                )

                sx = (
                    radial_coordinate
                    * ux
                )

                sy = (
                    radial_coordinate
                    * uy
                )

                dx = (
                    sx
                    - tx
                )

                dy = (
                    sy
                    - ty
                )

                dz = (
                    z_source
                    - tz
                )

                d2 = (
                    dx
                    * dx
                    +
                    dy
                    * dy
                    +
                    dz
                    * dz
                )

                inv_d3 = (
                    d2
                    ** -1.5
                )

                common = (
                    0.5
                    *
                    weights
                    *
                    source_phase
                    *
                    inv_d3
                )

                acc[
                    0
                ] += float(
                    np.sum(
                        common
                        * dx
                    )
                )

                acc[
                    1
                ] += float(
                    np.sum(
                        common
                        * dy
                    )
                )

                acc[
                    2
                ] += float(
                    np.sum(
                        common
                        * dz
                    )
                )

            az_values.append(
                acc[
                    2
                ]
            )

            transverse_values.append(
                math.hypot(
                    acc[
                        0
                    ],
                    acc[
                        1
                    ],
                )
            )

        rows.append({
            "r":
                float(
                    target_r
                ),

            "az_min":
                float(
                    np.min(
                        az_values
                    )
                ),

            "az_max":
                float(
                    np.max(
                        az_values
                    )
                ),

            "az_mean":
                float(
                    np.mean(
                        az_values
                    )
                ),

            "transverse_max":
                float(
                    np.max(
                        transverse_values
                    )
                ),
        })

    all_az = np.asarray(
        [
            value
            for row in rows
            for value in (
                row[
                    "az_min"
                ],
                row[
                    "az_max"
                ],
            )
        ],
        dtype=float,
    )

    min_az = float(
        np.min(
            all_az
        )
    )

    max_az = float(
        np.max(
            all_az
        )
    )

    mean_az = float(
        np.mean(
            [
                row[
                    "az_mean"
                ]
                for row in rows
            ]
        )
    )

    flatness = (
        (
            max_az
            -
            min_az
        )
        /
        max(
            abs(
                mean_az
            ),
            1.0e-300,
        )
    )

    transverse_fraction = float(
        max(
            row[
                "transverse_max"
            ]
            /
            max(
                abs(
                    row[
                        "az_min"
                    ]
                ),
                1.0e-300,
            )
            for row in rows
        )
    )

    on_axis_az = rows[
        0
    ][
        "az_mean"
    ]

    scalar_A = refined[
        "A_refined"
    ]

    on_axis_relerr = relative_error(
        on_axis_az,
        scalar_A,
    )

    return {
        "rows":
            rows,

        "minimum_axial":
            min_az,

        "maximum_axial":
            max_az,

        "mean_axial":
            mean_az,

        "axial_flatness":
            flatness,

        "maximum_transverse_fraction":
            transverse_fraction,

        "all_axial_outward":
            bool(
                min_az
                >
                0.0
            ),

        "on_axis_A":
            on_axis_az,

        "scalar_A":
            scalar_A,

        "on_axis_relative_error":
            on_axis_relerr,

        "on_axis_consistency_pass":
            bool(
                on_axis_relerr
                <=
                5.0e-3
            ),

        "bottom_duty_vector_grid":
            bottom_duty,
    }


def beta_sweep(
    best_scalar: dict[str, Any],
) -> list[dict[str, Any]]:
    """Directly test whether increasing circulation speed helps."""

    beta_grid = np.linspace(
        0.05,
        0.999,
        240,
    )

    rows = []

    orbit = highres_orbit(
        best_scalar[
            "a"
        ],
        best_scalar[
            "b"
        ],
        best_scalar[
            "halfwidth"
        ],
        8192,
    )

    top_duty = float(
        orbit[
            "top_duty"
        ]
    )

    top_kernel = float(
        orbit[
            "top_kernel"
        ]
    )

    k_avg = float(
        orbit[
            "k_avg"
        ]
    )

    for beta in beta_grid:

        beta_sq = (
            beta
            * beta
        )

        guide_factor = (
            best_scalar[
                "guide_factor"
            ]
        )

        q = best_scalar[
            "q"
        ]

        for mode in (
            "UNRESTRICTED_CONVERSION",
            "HEADON_KINETIC_LIMITED",
        ):

            if mode == "UNRESTRICTED_CONVERSION":

                f = best_scalar[
                    "f"
                ]

            else:

                f_cap = (
                    1.0
                    -
                    math.sqrt(
                        max(
                            0.0,
                            1.0
                            -
                            beta_sq,
                        )
                    )
                )

                f = min(
                    best_scalar[
                        "f"
                    ],
                    f_cap,
                )

            D = (
                f
                *
                (
                    q
                    +
                    1.0
                    +
                    beta_sq
                )
            )

            cap = (
                3.0
                -
                beta_sq
            )

            reset_duty = (
                top_duty
                * D
                / cap
                if cap > 0.0
                else math.inf
            )

            feasible = (
                reset_duty
                <=
                1.0
                -
                top_duty
            )

            if feasible:

                (
                    _mask,
                    actual_reset_duty,
                    bottom_kernel,
                ) = bottom_window_for_duty(
                    orbit,
                    reset_duty,
                )

                baseline_active = (
                    1.0
                    +
                    guide_factor
                    * beta_sq
                )

                inventory_energy = (
                    1.0
                    +
                    guide_factor
                    * beta_sq
                    +
                    best_scalar[
                        "overhead"
                    ]
                )

                gain = (
                    top_duty
                    * D
                    * top_kernel
                    -
                    actual_reset_duty
                    * cap
                    * bottom_kernel
                )

                A = (
                    -
                    baseline_active
                    * k_avg
                    +
                    gain
                )

                C = (
                    inventory_energy
                    / A
                    if A > 0.0
                    else math.inf
                )

            else:

                actual_reset_duty = math.inf
                A = -math.inf
                C = math.inf

            rows.append({
                "mode":
                    mode,

                "beta":
                    float(
                        beta
                    ),

                "f":
                    float(
                        f
                    ),

                "reset_duty":
                    float(
                        actual_reset_duty
                    ),

                "A":
                    float(
                        A
                    ),

                "C":
                    float(
                        C
                    ),
            })

    return rows


def wildcard_checks() -> list[dict[str, Any]]:
    """Blind user-number geometry diagnostics."""

    rows = []

    for a in BLIND_WILDCARDS:

        b = a

        beta = 0.95
        q = 2.0
        f = 0.80
        halfwidth = 0.75

        orbit = highres_orbit(
            a,
            b,
            halfwidth,
            8192,
        )

        beta_sq = (
            beta
            * beta
        )

        D = (
            f
            *
            (
                q
                +
                1.0
                +
                beta_sq
            )
        )

        cap = (
            3.0
            -
            beta_sq
        )

        reset_duty = (
            float(
                orbit[
                    "top_duty"
                ]
            )
            * D
            / cap
        )

        feasible = bool(
            reset_duty
            <=
            1.0
            -
            float(
                orbit[
                    "top_duty"
                ]
            )
        )

        if feasible:

            (
                _mask,
                bottom_duty,
                bottom_kernel,
            ) = bottom_window_for_duty(
                orbit,
                reset_duty,
            )

            baseline = (
                1.0
                +
                beta_sq
            )

            A = (
                -
                baseline
                * float(
                    orbit[
                        "k_avg"
                    ]
                )
                +
                float(
                    orbit[
                        "top_duty"
                    ]
                )
                * D
                * float(
                    orbit[
                        "top_kernel"
                    ]
                )
                -
                bottom_duty
                * cap
                * bottom_kernel
            )

            C = (
                (
                    1.0
                    +
                    beta_sq
                )
                / A
                if A > 0.0
                else math.inf
            )

        else:

            A = -math.inf
            C = math.inf

        rows.append({
            "a_over_h":
                float(
                    a
                ),

            "A":
                float(
                    A
                ),

            "C":
                float(
                    C
                ),

            "virial_feasible":
                feasible,
        })

    return rows


def clean_refined_for_json(
    item: dict[str, Any],
) -> dict[str, Any]:
    """Remove large phase arrays."""

    return {
        key: value
        for key, value
        in item.items()
        if key not in (
            "orbit",
            "bottom_mask",
        )
    }


def main() -> None:
    """Execute the full campaign."""

    print(
        "=== 024D COUNTERROTATING TOROIDAL STRESS-CONVERSION CAMPAIGN ===",
        flush=True,
    )

    require(
        B3_SUMMARY
    )

    require(
        C1_SUMMARY
    )

    b3 = json.loads(
        B3_SUMMARY.read_text(
            encoding="utf-8"
        )
    )

    c1 = json.loads(
        C1_SUMMARY.read_text(
            encoding="utf-8"
        )
    )

    if (
        b3[
            "decisions"
        ][
            "PURE_GR_DOMAIN_WALL_PULSE_FAMILY"
        ]
        !=
        "PAUSE_CURRENT_PURE_GR_DOMAIN_WALL_PULSE_FAMILY"
    ):
        raise RuntimeError(
            "Unexpected 024B3 branch state."
        )

    if (
        c1[
            "decision"
        ]
        !=
        "RED_INTUITIVE_SANDWICH_NO_PLANAR_FEASIBLE_SCOUT"
    ):
        raise RuntimeError(
            "Unexpected 024C1 branch state."
        )

    print(
        "\n=== A — ANALYTIC STRESS IDENTITIES ==="
    )

    print(
        f"C_006D="
        f"{C006D:.15f}"
    )

    print(
        "COUNTERROTATION_CANCELS_T0S=YES"
    )

    print(
        "COUNTERROTATION_CANCELS_TSS=NO"
    )

    print(
        "TWO_STREAM_TANGENTIAL_PRESSURE="
        "BETA2_TIMES_PACKET_ENERGY"
    )

    print(
        "MINIMUM_DEC_GUIDE_ENERGY="
        "BETA2_TIMES_PACKET_ENERGY"
    )

    print(
        "MINIMUM_SUPPORT_COUNTERFLOW_ACTIVE_OVER_TOTAL_ENERGY=1"
    )

    print(
        "CIRCULATION_ALONE_NEGATIVE_ACTIVE_SOURCE=NO"
    )

    print(
        "LINEAR_MAXWELL_ACTIVE_OVER_RHO=2"
    )

    print(
        "PURE_LINEAR_EM_COUNTERROTATION=RED"
    )

    print(
        "CANONICAL_SCALAR_ACTIVE_IDENTITY="
        "S_EQUALS_2_PHIDOT2_MINUS_2V"
    )

    print(
        "DEC_NEGATIVE_ACTIVE_LIMIT_MINUS_S_OVER_RHO=2"
    )

    print(
        "DEC_POSITIVE_TRACE_LIMIT_TRACE_OVER_RHO=3"
    )

    print(
        "FULL_CYCLE_VIRIAL_COMPENSATION=MANDATORY"
    )

    print(
        "OLD_018B_KLS_REALIZATION_REOPENED=NO"
    )

    # ------------------------------------------------------------
    # B. Build common scan.
    # ------------------------------------------------------------

    print(
        "\n=== B — BUILD 2^19 LOW-DISCREPANCY CAMPAIGN ===",
        flush=True,
    )

    p = build_sobol_parameters()

    print(
        f"BASE_SOBOL_CASES="
        f"{N_CASES}"
    )

    print(
        "GEOMETRY_FEATURE_BUILD=BEGIN",
        flush=True,
    )

    g = coarse_geometry_features(
        p
    )

    print(
        "GEOMETRY_FEATURE_BUILD=PASS",
        flush=True,
    )

    print(
        f"GEOMETRY_A_MIN="
        f"{float(np.min(p['a'])):.9e}"
    )

    print(
        f"GEOMETRY_A_MAX="
        f"{float(np.max(p['a'])):.9e}"
    )

    print(
        f"GEOMETRY_B_MIN="
        f"{float(np.min(p['b'])):.9e}"
    )

    print(
        f"GEOMETRY_B_MAX="
        f"{float(np.max(p['b'])):.9e}"
    )

    print(
        f"CURVATURE_CONCENTRATION_MAX="
        f"{float(np.max(g['curvature_concentration'])):.9e}"
    )

    # ------------------------------------------------------------
    # C. Family campaign.
    # ------------------------------------------------------------

    print(
        "\n=== C — MULTI-FAMILY STRESS-CONVERSION CAMPAIGN ===",
        flush=True,
    )

    results: dict[
        str,
        dict[
            str,
            np.ndarray
        ]
    ] = {}

    family_summaries = {}

    top_candidates: list[
        dict[str, float]
    ] = []

    for family in FAMILY_NAMES:

        print(
            f"FAMILY_BEGIN={family}",
            flush=True,
        )

        result = evaluate_family(
            family,
            p,
            g,
        )

        results[
            family
        ] = result

        coefficient = result[
            "coefficient"
        ]

        finite = np.isfinite(
            coefficient
        )

        positive_count = int(
            np.count_nonzero(
                finite
            )
        )

        beat_count = int(
            np.count_nonzero(
                coefficient
                <
                C006D
            )
        )

        spin_beat_count = int(
            np.count_nonzero(
                (
                    coefficient
                    <
                    C006D
                )
                &
                (
                    result[
                        "beta"
                    ]
                    >=
                    BETA_SPIN_THRESHOLD
                )
                &
                (
                    g[
                        "duty"
                    ]
                    <=
                    PULSE_DUTY_MAX
                )
            )
        )

        if positive_count:

            best_index = int(
                np.argmin(
                    coefficient
                )
            )

            best_c = float(
                coefficient[
                    best_index
                ]
            )

            best_a = float(
                result[
                    "average_outward"
                ][
                    best_index
                ]
            )

            best_beta = float(
                result[
                    "beta"
                ][
                    best_index
                ]
            )

            best_duty = float(
                g[
                    "duty"
                ][
                    best_index
                ]
            )

        else:

            best_index = -1
            best_c = math.inf
            best_a = -math.inf
            best_beta = math.nan
            best_duty = math.nan

        family_summaries[
            family
        ] = {
            "coarse_positive_cases":
                positive_count,

            "coarse_beats_006D_cases":
                beat_count,

            "coarse_spin_pulselike_beats_006D_cases":
                spin_beat_count,

            "best_coarse_index":
                best_index,

            "best_coarse_C":
                best_c,

            "best_coarse_A":
                best_a,

            "best_coarse_beta":
                best_beta,

            "best_coarse_duty":
                best_duty,
        }

        print(
            f"{family}_COARSE_POSITIVE_CASES="
            f"{positive_count}"
        )

        print(
            f"{family}_COARSE_BEATS_006D_CASES="
            f"{beat_count}"
        )

        print(
            f"{family}_COARSE_SPIN_PULSELIKE_BEATS_006D_CASES="
            f"{spin_beat_count}"
        )

        print(
            f"{family}_BEST_COARSE_C="
            f"{best_c:.15e}"
        )

        print(
            f"{family}_BEST_COARSE_BETA="
            f"{best_beta:.15e}"
        )

        print(
            f"{family}_BEST_COARSE_DUTY="
            f"{best_duty:.15e}"
        )

        indices = top_indices(
            coefficient,
            TOP_PER_FAMILY,
        )

        for index in indices:

            top_candidates.append(
                scalar_family_parameters(
                    family,
                    int(
                        index
                    ),
                    p,
                    g,
                    result,
                )
            )

        print(
            f"FAMILY_END={family}",
            flush=True,
        )

    # ------------------------------------------------------------
    # D. High-resolution candidate refinement.
    # ------------------------------------------------------------

    print(
        "\n=== D — HIGH-RESOLUTION FINITE-RESET-WINDOW REFINEMENT ===",
        flush=True,
    )

    refined_all = []

    for candidate in top_candidates:

        refined = refine_candidate(
            candidate
        )

        refined_all.append(
            refined
        )

    refined_by_family = {}

    for family in FAMILY_NAMES:

        family_rows = [
            item
            for item in refined_all
            if item[
                "family"
            ]
            ==
            family
        ]

        finite_rows = [
            item
            for item in family_rows
            if math.isfinite(
                item[
                    "C_refined"
                ]
            )
        ]

        finite_rows.sort(
            key=lambda item: item[
                "C_refined"
            ]
        )

        refined_by_family[
            family
        ] = finite_rows

        if finite_rows:

            best = finite_rows[
                0
            ]

            print(
                f"{family}_BEST_REFINED_C="
                f"{best['C_refined']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_A="
                f"{best['A_refined']:+.15e}"
            )

            print(
                f"{family}_BEST_REFINED_A_OVER_H="
                f"{best['a']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_B_OVER_H="
                f"{best['b']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_ASPECT="
                f"{best['aspect']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_BETA="
                f"{best['beta']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_CROSSING_DEG="
                f"{math.degrees(best['psi']):.15e}"
            )

            print(
                f"{family}_BEST_REFINED_Q="
                f"{best['q']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_F="
                f"{best['f']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_INTERACTION_DUTY="
                f"{best['top_duty']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_RESET_DUTY="
                f"{best['reset_duty_required']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_DUTY_CLASS="
                f"{best['duty_class']}"
            )

            print(
                f"{family}_BEST_REFINED_INTERACTION_ARC_OVER_H="
                f"{best['interaction_arc_length_over_h']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_CURVATURE_CONCENTRATION="
                f"{best['curvature_concentration']:.15e}"
            )

            print(
                f"{family}_BEST_REFINED_NEGATIVE_PACKET_AT_INTERACTION="
                + (
                    "YES"
                    if best[
                        "negative_packet_interaction"
                    ]
                    else "NO"
                )
            )

            print(
                f"{family}_BEST_REFINED_BEATS_006D="
                + (
                    "YES"
                    if best[
                        "C_refined"
                    ]
                    <
                    C006D
                    else "NO"
                )
            )

            print(
                f"{family}_BEST_REFINED_C_AFTER_25PCT_LOSS="
                f"{best['C_after_25pct_impulse_loss']:.15e}"
            )

        else:

            print(
                f"{family}_REFINED_POSITIVE_CASES=0"
            )

    # ------------------------------------------------------------
    # E. Directional vector audit.
    # ------------------------------------------------------------

    print(
        "\n=== E — FINITE-PAYLOAD / DIRECTIONAL VECTOR AUDIT ===",
        flush=True,
    )

    vector_audits = {}

    for family in FAMILY_NAMES:

        rows = refined_by_family[
            family
        ]

        if not rows:
            continue

        best = rows[
            0
        ]

        audit = vector_audit(
            best
        )

        vector_audits[
            family
        ] = audit

        print(
            f"{family}_VECTOR_ONAXIS_RELERR="
            f"{audit['on_axis_relative_error']:.15e}"
        )

        print(
            f"{family}_VECTOR_ONAXIS_CONSISTENCY="
            + (
                "PASS"
                if audit[
                    "on_axis_consistency_pass"
                ]
                else "FAIL"
            )
        )

        print(
            f"{family}_PLANE_ALL_AXIAL_OUTWARD="
            + (
                "YES"
                if audit[
                    "all_axial_outward"
                ]
                else "NO"
            )
        )

        print(
            f"{family}_PLANE_AXIAL_FLATNESS="
            f"{audit['axial_flatness']:.15e}"
        )

        print(
            f"{family}_PLANE_MAX_TRANSVERSE_FRACTION="
            f"{audit['maximum_transverse_fraction']:.15e}"
        )

    # ------------------------------------------------------------
    # F. Blind wildcard geometry diagnostics.
    # ------------------------------------------------------------

    print(
        "\n=== F — BLIND WILDCARD GEOMETRY CHECK ==="
    )

    wildcard_rows = wildcard_checks()

    for row in wildcard_rows:

        print(
            f"WILDCARD_A_OVER_H="
            f"{row['a_over_h']:.6f} "
            f"A={row['A']:+.12e} "
            f"C={row['C']:.12e} "
            f"VIRIAL={'YES' if row['virial_feasible'] else 'NO'}"
        )

    print(
        "WILDCARDS_ARE_PHYSICS_PRIORS=NO"
    )

    # ------------------------------------------------------------
    # G. Direct spin-speed audit.
    # ------------------------------------------------------------

    print(
        "\n=== G — DOES MORE SPIN ACTUALLY HELP? ===",
        flush=True,
    )

    scalar_rows = refined_by_family[
        "CANONICAL_SCALAR_TRANSPORT"
    ]

    if scalar_rows:

        best_scalar = scalar_rows[
            0
        ]

        beta_rows = beta_sweep(
            best_scalar
        )

        unrestricted = [
            row
            for row in beta_rows
            if (
                row[
                    "mode"
                ]
                ==
                "UNRESTRICTED_CONVERSION"
                and math.isfinite(
                    row[
                        "C"
                    ]
                )
            )
        ]

        kinetic = [
            row
            for row in beta_rows
            if (
                row[
                    "mode"
                ]
                ==
                "HEADON_KINETIC_LIMITED"
                and math.isfinite(
                    row[
                        "C"
                    ]
                )
            )
        ]

        if unrestricted:

            best_u = min(
                unrestricted,
                key=lambda row: row[
                    "C"
                ],
            )

            print(
                f"SPIN_SWEEP_UNRESTRICTED_BEST_BETA="
                f"{best_u['beta']:.15e}"
            )

            print(
                f"SPIN_SWEEP_UNRESTRICTED_BEST_C="
                f"{best_u['C']:.15e}"
            )

        else:

            best_u = None

            print(
                "SPIN_SWEEP_UNRESTRICTED_POSITIVE_CASES=0"
            )

        if kinetic:

            best_k = min(
                kinetic,
                key=lambda row: row[
                    "C"
                ],
            )

            print(
                f"SPIN_SWEEP_KINETIC_LIMITED_BEST_BETA="
                f"{best_k['beta']:.15e}"
            )

            print(
                f"SPIN_SWEEP_KINETIC_LIMITED_BEST_C="
                f"{best_k['C']:.15e}"
            )

        else:

            best_k = None

            print(
                "SPIN_SWEEP_KINETIC_LIMITED_POSITIVE_CASES=0"
            )

    else:

        best_scalar = None
        beta_rows = []
        best_u = None
        best_k = None

        print(
            "SPIN_SWEEP_NOT_RUN_NO_SCALAR_SURVIVOR"
        )

    # ------------------------------------------------------------
    # H. Interpretation / decision.
    # ------------------------------------------------------------

    print(
        "\n=== H — 024D DECISION ==="
    )

    ideal_rows = refined_by_family[
        "IDEAL_DEC_SPINNING_CEILING"
    ]

    ideal_beats = bool(
        ideal_rows
        and ideal_rows[
            0
        ][
            "C_refined"
        ]
        <
        C006D
    )

    constrained_families = (
        "MASSIVE_HEADON_COLLIDER",
        "MASSLESS_HYBRID_COLLIDER",
        "ELASTIC_VORTON_CONVERTER",
    )

    constrained_record_survivors = []

    constrained_positive_survivors = []

    spin_pulselike_survivors = []

    for family in constrained_families:

        rows = refined_by_family[
            family
        ]

        if not rows:
            continue

        best = rows[
            0
        ]

        constrained_positive_survivors.append(
            best
        )

        if best[
            "C_refined"
        ] < C006D:

            constrained_record_survivors.append(
                best
            )

            if (
                best[
                    "beta"
                ]
                >=
                BETA_SPIN_THRESHOLD
                and
                best[
                    "top_duty"
                ]
                <=
                PULSE_DUTY_MAX
            ):

                spin_pulselike_survivors.append(
                    best
                )

    scalar_beats = bool(
        scalar_rows
        and scalar_rows[
            0
        ][
            "C_refined"
        ]
        <
        C006D
    )

    if not ideal_beats:

        decision = (
            "RED_COUNTERROTATING_ORBITAL_STRESS_CONVERSION_"
            "IDEAL_CEILING_FAILS_006D"
        )

        next_action = (
            "CLOSE_024D_AND_RERANK_006D_MICROSCOPIC_"
            "REALIZATION_VS_ANALOGUE_ANTIGRAVITY"
        )

        interpretation = (
            "NO_ORBITAL_STRESS_CONVERSION_HEADROOM"
        )

    elif spin_pulselike_survivors:

        decision = (
            "YELLOW_COUNTERROTATING_COLLIDER_SURVIVOR_"
            "REQUIRES_MICROSCOPIC_INTERACTION_PREFILTER"
        )

        next_action = (
            "024D1_DERIVE_MINIMAL_NONLINEAR_SCALAR_GAUGE_"
            "COLLISION_LAGRANGIAN_AND_CHARACTERISTIC_STABILITY"
        )

        interpretation = (
            "SPIN_CAN_BE_KINEMATIC_ENABLER_IN_SURVIVING_PREFILTER"
        )

    elif constrained_record_survivors:

        decision = (
            "YELLOW_TRANSPORTED_STRESS_CONVERTER_BEATS_006D_"
            "BUT_NOT_AS_SHORT_COLLISION"
        )

        next_action = (
            "024D1_TEST_MINIMAL_POTENTIAL_DOMINATED_FIELD_CONVERTER_"
            "WITHOUT_ASSUMING_COLLISION_IS_THE_CORE_MECHANISM"
        )

        interpretation = (
            "KERNEL_TRANSPORT_AND_STRESS_CONVERSION_DOMINATE_OVER_SPIN"
        )

    elif scalar_beats:

        decision = (
            "YELLOW_SCALAR_STRESS_CONVERSION_HEADROOM_"
            "COUNTERROTATION_NOT_YET_PROMOTED"
        )

        next_action = (
            "024D1_MINIMAL_CANONICAL_SCALAR_INTERACTION_ZONE_"
            "FIELD_PREFILTER_WITH_FULL_CONSERVATION"
        )

        interpretation = (
            "STRESS_CONVERSION_IS_PROMISING_SPIN_IS_NOT_YET_THE_DRIVER"
        )

    elif constrained_positive_survivors:

        decision = (
            "YELLOW_COUNTERROTATING_CYCLE_CAN_POINT_OUTWARD_"
            "BUT_DOES_NOT_BEAT_006D"
        )

        next_action = (
            "DEPRIORITIZE_024D_UNLESS_AN_INDEPENDENT_FIELD_"
            "MECHANISM_REDUCES_CONFINEMENT_OR_CONVERSION_OVERHEAD"
        )

        interpretation = (
            "MECHANISM_EXISTS_BUT_NO_SOURCE_EFFICIENCY_RECORD"
        )

    else:

        decision = (
            "RED_KINEMATICALLY_CONSTRAINED_COUNTERROTATING_"
            "FAMILIES_NO_SURVIVOR"
        )

        next_action = (
            "CLOSE_024D_AND_RERANK_006D_MICROSCOPIC_"
            "REALIZATION_VS_ANALOGUE_ANTIGRAVITY"
        )

        interpretation = (
            "IDEAL_HEADROOM_DOES_NOT_SURVIVE_CONSTRAINED_FAMILIES"
        )

    print(
        "CIRCULATION_ALONE=RED_ANALYTIC"
    )

    print(
        "PURE_LINEAR_EM_COUNTERROTATION=RED_ANALYTIC"
    )

    print(
        "IDEAL_DEC_SPINNING_CEILING_BEATS_006D="
        + (
            "YES"
            if ideal_beats
            else "NO"
        )
    )

    print(
        "CANONICAL_SCALAR_TRANSPORT_BEATS_006D="
        + (
            "YES"
            if scalar_beats
            else "NO"
        )
    )

    print(
        "KINEMATICALLY_CONSTRAINED_FAMILY_BEATS_006D="
        + (
            "YES"
            if constrained_record_survivors
            else "NO"
        )
    )

    print(
        "SPIN_BETA_GE0P5_PULSELIKE_CONSTRAINED_BEATS_006D="
        + (
            "YES"
            if spin_pulselike_survivors
            else "NO"
        )
    )

    print(
        f"SPIN_INTERPRETATION="
        f"{interpretation}"
    )

    print(
        f"024D_DECISION="
        f"{decision}"
    )

    print(
        f"NEXT="
        f"{next_action}"
    )

    print(
        "MICROSCOPIC_FIELD_REALIZATION=NO"
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
        "70_TO_71_PERCENT_RETAIN_UNLESS_A_LATER_MICROSCOPIC_PROMOTION_IS_EARNED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    # ------------------------------------------------------------
    # I. Persist compact results.
    # ------------------------------------------------------------

    csv_rows = []

    for item in refined_all:

        clean = clean_refined_for_json(
            item
        )

        csv_rows.append(
            clean
        )

    if csv_rows:

        fields = sorted(
            {
                key
                for row in csv_rows
                for key in row.keys()
                if not isinstance(
                    row[
                        key
                    ],
                    (
                        dict,
                        list,
                        np.ndarray,
                    ),
                )
            }
        )

        with OUT_TOP.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
                extrasaction="ignore",
            )

            writer.writeheader()

            writer.writerows(
                csv_rows
            )

    if beta_rows:

        with OUT_BETA.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "mode",
                    "beta",
                    "f",
                    "reset_duty",
                    "A",
                    "C",
                ],
            )

            writer.writeheader()

            writer.writerows(
                beta_rows
            )

    best_profiles = {}

    best_refined_json = {}

    for family in FAMILY_NAMES:

        rows = refined_by_family[
            family
        ]

        if not rows:
            continue

        best = rows[
            0
        ]

        best_refined_json[
            family
        ] = clean_refined_for_json(
            best
        )

        orbit = best[
            "orbit"
        ]

        prefix = (
            family
            .lower()
            .replace(
                "-",
                "_",
            )
        )

        best_profiles[
            prefix
            + "_theta"
        ] = np.asarray(
            orbit[
                "theta"
            ]
        )

        best_profiles[
            prefix
            + "_kernel"
        ] = np.asarray(
            orbit[
                "kernel"
            ]
        )

        best_profiles[
            prefix
            + "_weights"
        ] = np.asarray(
            orbit[
                "weights"
            ]
        )

        best_profiles[
            prefix
            + "_top_mask"
        ] = np.asarray(
            orbit[
                "top_mask"
            ],
            dtype=np.int8,
        )

        best_profiles[
            prefix
            + "_bottom_mask"
        ] = np.asarray(
            best[
                "bottom_mask"
            ],
            dtype=np.int8,
        )

    if best_profiles:

        np.savez_compressed(
            OUT_NPZ,
            **best_profiles,
        )

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_COUNTERROTATING_TOROIDAL_"
                "STRESS_CONVERSION_PREFILTER"
            ),

        "analytic_results": {
            "counterrotation_cancels_momentum":
                True,

            "counterrotation_cancels_tangential_stress":
                False,

            "minimum_DEC_guide_energy_over_packet":
                "beta^2",

            "minimum_complete_counterflow_active_over_total_energy":
                1.0,

            "circulation_alone_negative_active":
                False,

            "linear_Maxwell_S_over_rho":
                2.0,

            "pure_linear_EM_counterrotation":
                "RED",

            "canonical_scalar_identity":
                "S=2*phidot^2-2*V",

            "DEC_negative_active_limit_minus_S_over_rho":
                2.0,

            "full_cycle_virial_compensation_required":
                True,
        },

        "scan": {
            "base_sobol_cases":
                N_CASES,

            "families":
                list(
                    FAMILY_NAMES
                ),

            "effective_family_case_evaluations":
                N_CASES
                * len(
                    FAMILY_NAMES
                ),

            "family_summaries":
                family_summaries,
        },

        "best_refined":
            best_refined_json,

        "vector_audits":
            vector_audits,

        "blind_wildcards": {
            "physics_prior":
                False,

            "results":
                wildcard_rows,
        },

        "spin_sweep": {
            "best_unrestricted":
                best_u,

            "best_kinetic_limited":
                best_k,
        },

        "decision": {
            "ideal_DEC_ceiling_beats_006D":
                ideal_beats,

            "canonical_scalar_beats_006D":
                scalar_beats,

            "kinematically_constrained_family_beats_006D":
                bool(
                    constrained_record_survivors
                ),

            "spin_pulselike_constrained_beats_006D":
                bool(
                    spin_pulselike_survivors
                ),

            "interpretation":
                interpretation,

            "024D":
                decision,

            "next":
                next_action,

            "practical_antigravity_device":
                False,
        },

        "claim_limits": [
            "NO_MICROSCOPIC_NEW_FIELD_SOLUTION",
            "NO_FULL_STABILITY",
            "NO_NONLINEAR_GR",
            "NO_1_OVER_G_SCALING_ESCAPE",
            "NO_EXPERIMENT",
            "NO_REACTIONLESS_PROPULSION",
            "NO_PRACTICAL_DEVICE",
        ],
    }

    OUT_SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
            allow_nan=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"SUMMARY_JSON="
        f"{OUT_SUMMARY.relative_to(ROOT)}"
    )

    print(
        f"TOP_CSV="
        f"{OUT_TOP.relative_to(ROOT)}"
    )

    if OUT_BETA.is_file():

        print(
            f"BETA_SWEEP_CSV="
            f"{OUT_BETA.relative_to(ROOT)}"
        )

    if OUT_NPZ.is_file():

        print(
            f"BEST_PROFILES_NPZ="
            f"{OUT_NPZ.relative_to(ROOT)}"
        )

    print(
        "024D_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
