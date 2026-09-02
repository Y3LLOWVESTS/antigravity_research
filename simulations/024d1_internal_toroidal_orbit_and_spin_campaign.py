#!/usr/bin/env python3
"""024D1 — internal toroidal-orbit and orbit-plus-spin campaign.

PURPOSE
-------
Extend 024D by replacing the simple elliptical transport orbit with actual
orbits inside a toroidal volume.

A torus has two independent cycles:

    TOROIDAL:
        around the major ring,

    POLOIDAL:
        around the tube cross-section.

Their combination produces a helical / torus-knot trajectory labelled by:

    (p, q),

where:

    p = toroidal winding,

    q = poloidal winding.

The campaign asks whether these additional orbital degrees of freedom provide
useful GR stress/kernel leverage once the complete orbital-curvature,
confinement, virial/reset, spin-energy and finite-payload ledgers are included.

This run separately tests:

    orbital motion without intrinsic spin,

    orbital motion plus internal spin,

    unrestricted scalar stress conversion,

    kinetic-energy-limited conversion,

    an elastic torus-knot implementation,

    and an ideal DEC ceiling.

SCIENTIFIC QUESTION
-------------------
Can field energy following poloidal or helical paths inside a toroidal volume
outperform:

    C_006D
        =
    23.591586299249

and/or the 024D relaxed scalar-transport result:

    C_024D_scalar
        =
    6.610457607426174

while satisfying:

    positive total energy,

    DEC-compatible confinement accounting,

    closed-orbit curvature burden,

    full-cycle virial compensation,

    finite reset windows,

    source-free finite-payload response,

    and independent vector-field reconstruction?

SECOND QUESTION
---------------
If an orbiting energy packet also possesses internal spin, does that improve
useful gravitational response per total conserved energy?

The run does NOT give spin free stress.

Internal spin is assigned:

    explicit spin energy,

    explicit internal kinetic stress,

    explicit DEC-compatible confinement cost.

The run then tests whether the spin reservoir can improve stress conversion
after total energy is normalized.

TORUS GEOMETRY
--------------
Let:

    R = major radius,

    a = minor radius,

with:

    a/R < 1.

Use the standard toroidal trajectory:

    rho(u)
        =
    R + a cos(theta),

    theta(u)
        =
    q u + delta,

    phi(u)
        =
    p u,

    x
        =
    rho cos(phi),

    y
        =
    rho sin(phi),

    z
        =
    -g - a + a sin(theta),

where:

    0 <= u < 2 pi,

and:

    g >= 0

is the source-to-top gap.

Thus the entire orbit satisfies:

    z <= -g <= 0.

The payload center is:

    (0,0,1).

WINDING FAMILIES
----------------
The primary discrete winding set is:

    (1,0)
        pure toroidal orbit

    (0,1)
        pure poloidal orbit

    (1,1)
    (2,1)
    (3,1)
    (1,2)
    (2,3)
    (3,2)
    (5,2)
    (5,3)

The mixed cases are coprime torus-knot / helical paths.

For q>0, the orbit naturally passes through:

    the top of the toroidal tube

and:

    the bottom of the toroidal tube.

These become candidate high-kernel negative-stress and low-kernel
positive-reset regions.

PURE TOROIDAL CONTROL
---------------------
For:

    q = 0,

the path remains at one fixed height and radius.

Its gravitational kernel is therefore constant around the orbit for an
on-axis payload.

Consequently spatial separation of negative and compensating positive stress
cannot provide axial kernel leverage.

The run retains this family as an important control.

TOTAL CURVATURE
---------------
For a space curve r(u), compute:

    kappa
      =
    |r' x r''|
    /
    |r'|^3.

The total curvature is:

    K_total
      =
    integral kappa ds.

Fenchel's theorem requires for every closed regular space curve:

    K_total >= 2 pi.

Define:

    curvature_norm
      =
    K_total/(2 pi)
      >=
    1.

This is used as the minimum geometric multiplier on orbital confinement
burden.

A complicated winding cannot receive large centripetal stress for free.

CURVATURE CONCENTRATION
-----------------------
Also compute:

    curvature_concentration
      =
    kappa_max
    /
    <kappa>_s.

The ordinary orbital models pay:

    guide_factor
      =
    guide_multiplier
    *
    curvature_norm.

The elastic torus-knot family additionally pays:

    sqrt(curvature_concentration).

COUNTERORBIT PAIR
-----------------
Each trajectory represents an equal counterpropagating pair.

Their net momentum and orbital angular momentum may cancel:

    T_0i,total approximately 0,

while their kinetic stresses add.

As established in 024D:

    counterrotation does not cancel stress.

The pair normalization is absorbed into the unit packet-energy convention.

ORBITAL ENERGY / CONFINEMENT
----------------------------
Normalize non-spin mobile packet energy to:

    E_orbit = 1.

For orbital speed beta_o:

    S_orbit
      =
    (1 + beta_o^2) E_orbit.

Minimum circular-orbit DEC confinement requires energy:

    E_guide,min
      =
    beta_o^2 E_orbit.

A non-circular path pays the total-curvature multiplier.

INTERNAL SPIN
-------------
Let:

    s
      =
    E_spin/E_orbit.

The spin-energy reservoir is therefore:

    E_spin = s.

Let beta_s characterize its internal rotational speed.

Before conversion its active source is modeled by the same one-dimensional
kinetic-stress identity:

    S_spin
      =
    s (1 + beta_s^2).

Its minimum DEC-compatible internal confinement energy is:

    E_spin_guide
      =
    s beta_s^2

times an independently scanned guide multiplier.

This is deliberately conservative with respect to claims:

    spin does not receive negative pressure for free.

SPIN ORIENTATION
----------------
For a stationary payload the leading weak-field gravitoelectric response uses
the scalar active combination:

    S = T00 + Tii.

At fixed energy and stress trace, merely rotating the intrinsic spin axis does
not change this scalar combination.

Spin-orbit alignment is therefore not treated as an independent source of
antigravity in the primary coefficient scan.

Its possible gravitomagnetic influence would matter for moving payloads, not
the stationary finite payload used here.

CANONICAL-SCALAR STRESS CONVERTER
---------------------------------
Retain the 024D identity:

    S_scalar
      =
    2 phidot^2 - 2 V.

A potential-dominated state can reach:

    S/rho -> -2.

Let:

    q_s
      =
    -S/rho

during conversion, with:

    0 <= q_s <= 2.

Let:

    f

be the fraction of mobile orbit-plus-spin energy converted.

MOBILE ACTIVE RATIO
-------------------
Total mobile energy:

    E_m
      =
    1 + s.

Before conversion:

    S_m
      =
    (1+beta_o^2)
    +
    s(1+beta_s^2).

Define:

    r_m
      =
    S_m/E_m.

Converting fraction f from its original state to:

    S/rho = -q_s

changes active source by:

    D
      =
    f E_m (q_s + r_m).

FULL-CYCLE VIRIAL RESET
-----------------------
The spatial-trace ratio of the mobile state is:

    r_m - 1.

The most favorable DEC-saturating positive reset has:

    trace/rho = +3.

Its trace capacity relative to the mobile state is:

    4 - r_m.

Therefore the required reset duty is:

    d_reset
      =
    d_int
    *
    f (q_s+r_m)
    /
    (4-r_m).

This must satisfy:

    d_reset <= 1-d_int.

The reset is placed in a finite contiguous low-kernel orbital window.

No pointlike free reset is allowed in refined results.

INTERACTION REGION
------------------
For q>0, the interaction zone is centered on the top-of-tube condition:

    theta = pi/2.

Because q may exceed one, the trajectory may pass through the top region
multiple times during a closed torus-knot orbit.

For q=0, a control interaction interval is defined in toroidal angle.

RESET REGION
------------
For q>0, the reset region is centered on:

    theta = 3 pi/2,

the bottom of the toroidal tube.

For q=0, the reset is placed opposite the interaction azimuth.

Because the on-axis kernel of a pure toroidal orbit is constant, this cannot
create source-level kernel rectification.

KINETIC-LIMITED CONVERSION
--------------------------
For the no-spin collision-limited family, the maximum convertible fraction is
the head-on massive-packet kinetic fraction:

    f_orbit,max
      =
    1 - sqrt(1-beta_o^2).

For orbit-plus-spin, spin is allowed to contribute only the internal kinetic
fraction:

    f_spin,max
      =
    1 - sqrt(1-beta_s^2).

The total convertible mobile energy is bounded by:

    E_convert,max
      =
    f_orbit,max
    +
    s f_spin,max.

Therefore:

    f_max
      =
    E_convert,max/(1+s).

The actual conversion fraction is:

    min(f_scan, f_max).

This is the decisive "does orbit plus spin really help?" family.

MODEL FAMILIES
--------------
1. IDEAL_DEC_ORBIT_SPIN_CEILING

   beta_o = 1
   beta_s = 1
   q_s = 2
   f = 1
   minimum curvature guide
   minimum spin guide
   zero converter overhead.

   This is only a theoretical ceiling.

2. ORBIT_SCALAR_NO_SPIN

   Internal toroidal/poloidal/helical orbit.

   s = 0.

   Unrestricted canonical-scalar conversion.

3. ORBIT_KINETIC_LIMITED_NO_SPIN

   Same orbital geometries.

   Conversion limited to head-on orbital kinetic energy.

4. ORBIT_PLUS_SPIN_SCALAR

   Orbital plus internal-spin energy.

   Scalar conversion may draw from the complete mobile reservoir.

   This determines whether adding spin helps when conversion is otherwise
   available.

5. ORBIT_PLUS_SPIN_KINETIC_LIMITED

   Conversion can draw only from orbital kinetic plus internal spin-kinetic
   energy.

   This is the strongest fair test of the user's orbit-plus-spin hypothesis.

6. ELASTIC_TORUS_KNOT_SCALAR

   Orbit-plus-spin scalar conversion with stronger curvature/concentration
   and converter overhead penalties.

   This is a generic elastic-field implementation prefilter.

PURE LINEAR EM / ORBIT-ONLY CONTROLS
------------------------------------
The following remain analytically RED:

    pure linear Maxwell orbiting energy,

    pure counterorbit circulation,

    orbit without negative-active conversion.

The campaign does not waste compute re-optimizing identities already settled
by 024D.

GRAVITATIONAL OBSERVABLE
------------------------
For an on-axis payload at z=1:

    K_z
      =
    (1-z)
    /
    [rho^2 + (1-z)^2]^(3/2).

Positive active source gives attraction.

Define desired outward acceleration:

    A_out
      =
    - <S K_z>.

Positive A_out is outward.

The source coefficient is:

    C
      =
    E_inventory/A_out.

Compare against:

    C_006D
      =
    23.591586299249,

and:

    C_024D_scalar
      =
    6.610457607426174.

FINITE PAYLOAD
--------------
Use:

    R_payload/h
      =
    0.043298860805059215.

The complete orbit must remain outside the payload sphere.

Since all tested source points satisfy z<=0 while the payload is centered at
z=1, this condition has a large margin but is checked numerically.

DIRECTIONAL FIELD / ORBIT BUNDLES
---------------------------------
A single poloidal loop is strongly non-axisymmetric.

Therefore the best candidates are independently reconstructed as phase-offset
bundles containing:

    N =
        1
        2
        4
        8

identical orbit pairs rotated uniformly around the symmetry axis.

Total source energy is held fixed and divided among the bundle components.

The bundle test asks whether several internal orbits can suppress transverse
gravity without changing the source-level energy coefficient.

Evaluate targets across:

    r/h =
        0
        0.125
        0.25
        0.375
        0.5

and 12 target-plane azimuths.

Report:

    axial flatness,

    minimum axial response,

    maximum transverse/axial fraction.

LARGE CAMPAIGN
--------------
Generate:

    2^20
      =
    1,048,576

scrambled Sobol geometries.

Each is evaluated in six families:

    6,291,456

family-level source evaluations.

Scanned variables include:

    R/h:
        0.35 to 8, logarithmic

    a/R:
        0.08 to 0.65

    gap/h:
        0 to 1

    winding pair:
        ten discrete families

    torus phase delta:
        0 to 2 pi

    orbital beta:
        0.02 to 0.9995

    spin-energy fraction s:
        0 to 2.5

    internal spin beta:
        0 to 0.999

    q_s:
        0 to 2

    nominal conversion fraction:
        0 to 1

    interaction half-width:
        0.01 to 1.20 rad, logarithmic

    orbital guide multiplier:
        1 to 3

    spin guide multiplier:
        1 to 3

    converter overhead:
        0 to 1.5.

COARSE PHASE RESOLUTION
-----------------------
Each orbital geometry is integrated with:

    384 phase points

in batches.

HIGH-RESOLUTION REFINEMENT
--------------------------
Retain:

    top 50 overall cases per family

plus:

    top 6 cases per winding per family.

Deduplicate and refine using:

    32768 phase samples.

The refinement uses an explicitly finite bottom reset window.

SPIN-SPEED / SPIN-ENERGY AUDIT
------------------------------
Take the best refined no-spin scalar orbital geometry.

Hold its geometry and scalar conversion parameters fixed.

Sweep:

    beta_orbit

    spin-energy fraction

    beta_spin

for both:

    unrestricted conversion

and:

    kinetic-limited conversion.

This directly determines whether spin helps after its energy and confinement
are included.

PROMOTION CONDITIONS
--------------------
An internal-orbit source-level survivor must have:

    refined A > 0;

    virial reset feasible;

    finite reset window included;

    finite-payload separation PASS;

    C_refined < C_006D.

A major new source-headroom signal additionally requires:

    C_refined < C_024D_scalar.

An ORBITAL-TOPOLOGY promotion requires the winning winding to satisfy:

    q > 0

and outperform the best pure toroidal control.

A genuine ORBIT-PLUS-SPIN promotion requires:

    kinetic-limited family,

    s >= 0.10,

    beta_spin >= 0.25,

    C < C_006D,

and:

    at least 5 percent improvement over the corresponding no-spin
    kinetic-limited optimum.

Otherwise spin remains an overhead or merely an auxiliary reservoir.

FALSIFIERS
----------
If pure toroidal and mixed/helical orbits perform equivalently once curvature
is counted:

    internal toroidal topology provides no useful source leverage.

If pure poloidal wins but helical winding worsens monotonically with total
curvature:

    top/bottom kernel transport is useful,
    knot complexity is not.

If unrestricted spin chooses:

    s -> 0

or:

    beta_spin -> 0,

spin is an overhead.

If kinetic-limited spin cannot beat the no-spin kinetic family:

    spin does not improve realizable collision conversion.

If only unrestricted scalar models beat 006D:

    the promising mechanism remains scalar stress conversion,
    not orbital motion or spin.

STOP RULE
---------
If no constrained orbit/spin family beats 006D:

    do not launch a microscopic torus-knot field PDE.

Return to the previously identified:

    minimal canonical-scalar stress-converter field prefilter.

If an orbital topology materially improves C but spin does not:

    build the microscopic successor around poloidal/helical transport,
    without an internal spin sector.

If orbit-plus-spin survives the kinetic-limited gate:

    derive the minimal field Lagrangian that actually carries both conserved
    orbital and spin/angular-momentum currents.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INTERNAL_TOROIDAL_ORBIT_AND_SPIN_STRESS_CONVERSION_CAMPAIGN

DOES NOT ESTABLISH
------------------
- a microscopic torus-knot field;
- stability;
- nonlinear GR;
- favorable absolute 1/G scaling;
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

INPUT = (
    DATA
    / "024d_counterrotating_toroidal_stress_conversion_summary.json"
)

OUT_SUMMARY = (
    DATA
    / "024d1_internal_toroidal_orbit_and_spin_summary.json"
)

OUT_TOP = (
    DATA
    / "024d1_internal_toroidal_orbit_and_spin_top.csv"
)

OUT_WINDING = (
    DATA
    / "024d1_internal_toroidal_winding_summary.csv"
)

OUT_SPIN = (
    DATA
    / "024d1_internal_toroidal_spin_sweep.csv"
)

OUT_NPZ = (
    DATA
    / "024d1_internal_toroidal_best_profiles.npz"
)


C006D = 23.591586299249
C024D_SCALAR = 6.610457607426174

PAYLOAD_RADIUS_OVER_H = 0.043298860805059215

SOBOL_POWER = 20
N_CASES = 2 ** SOBOL_POWER

COARSE_NPHASE = 384
REFINE_NPHASE = 32768
VECTOR_NPHASE = 16384

BATCH = 768

TOP_OVERALL_PER_FAMILY = 50
TOP_PER_WINDING_PER_FAMILY = 6

WINDINGS = (
    (1, 0),
    (0, 1),
    (1, 1),
    (2, 1),
    (3, 1),
    (1, 2),
    (2, 3),
    (3, 2),
    (5, 2),
    (5, 3),
)

FAMILIES = (
    "IDEAL_DEC_ORBIT_SPIN_CEILING",
    "ORBIT_SCALAR_NO_SPIN",
    "ORBIT_KINETIC_LIMITED_NO_SPIN",
    "ORBIT_PLUS_SPIN_SCALAR",
    "ORBIT_PLUS_SPIN_KINETIC_LIMITED",
    "ELASTIC_TORUS_KNOT_SCALAR",
)

BUNDLE_COUNTS = (
    1,
    2,
    4,
    8,
)

BLIND_WILDCARD_VALUES = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


def require(
    path: Path,
) -> None:
    """Require one artifact."""

    if not path.is_file():
        raise RuntimeError(
            f"Required file missing: {path}"
        )


def relerr(
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


def wrap_distance(
    angle: np.ndarray,
    center: float,
) -> np.ndarray:
    """Shortest circular angular distance."""

    return np.abs(
        (
            angle
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


def build_parameters() -> dict[str, np.ndarray]:
    """Generate the complete Sobol parameter population."""

    sampler = qmc.Sobol(
        d=14,
        scramble=True,
        seed=240101,
    )

    u = sampler.random_base2(
        SOBOL_POWER
    )

    major = 10.0 ** (
        math.log10(
            0.35
        )
        +
        (
            math.log10(
                8.0
            )
            -
            math.log10(
                0.35
            )
        )
        * u[
            :,
            0
        ]
    )

    minor_ratio = (
        0.08
        +
        (
            0.65
            - 0.08
        )
        * u[
            :,
            1
        ]
    )

    minor = (
        major
        * minor_ratio
    )

    gap = u[
        :,
        2
    ]

    winding_index = np.minimum(
        (
            u[
                :,
                3
            ]
            * len(
                WINDINGS
            )
        ).astype(
            int
        ),
        len(
            WINDINGS
        )
        - 1,
    )

    p = np.asarray(
        [
            WINDINGS[
                index
            ][
                0
            ]
            for index in winding_index
        ],
        dtype=float,
    )

    q_winding = np.asarray(
        [
            WINDINGS[
                index
            ][
                1
            ]
            for index in winding_index
        ],
        dtype=float,
    )

    phase = (
        2.0
        * math.pi
        * u[
            :,
            4
        ]
    )

    beta_orbit = (
        0.02
        +
        (
            0.9995
            - 0.02
        )
        * u[
            :,
            5
        ]
    )

    spin_fraction = (
        2.5
        * u[
            :,
            6
        ]
    )

    beta_spin = (
        0.999
        * u[
            :,
            7
        ]
    )

    q_scalar = (
        2.0
        * u[
            :,
            8
        ]
    )

    f_raw = u[
        :,
        9
    ]

    halfwidth = np.exp(
        math.log(
            0.01
        )
        +
        (
            math.log(
                1.20
            )
            -
            math.log(
                0.01
            )
        )
        * u[
            :,
            10
        ]
    )

    guide_multiplier = (
        1.0
        +
        2.0
        * u[
            :,
            11
        ]
    )

    spin_guide_multiplier = (
        1.0
        +
        2.0
        * u[
            :,
            12
        ]
    )

    overhead = (
        1.5
        * u[
            :,
            13
        ]
    )

    return {
        "major":
            major,

        "minor":
            minor,

        "minor_ratio":
            minor_ratio,

        "gap":
            gap,

        "winding_index":
            winding_index,

        "p":
            p,

        "q_winding":
            q_winding,

        "phase":
            phase,

        "beta_orbit":
            beta_orbit,

        "spin_fraction":
            spin_fraction,

        "beta_spin":
            beta_spin,

        "q_scalar":
            q_scalar,

        "f_raw":
            f_raw,

        "halfwidth":
            halfwidth,

        "guide_multiplier":
            guide_multiplier,

        "spin_guide_multiplier":
            spin_guide_multiplier,

        "overhead":
            overhead,
    }


def geometry_features(
    pset: dict[str, np.ndarray],
) -> dict[str, np.ndarray]:
    """Compute torus-orbit geometry, curvature and payload kernel."""

    n = len(
        pset[
            "major"
        ]
    )

    k_avg = np.empty(
        n,
        dtype=float,
    )

    interaction_duty = np.empty_like(
        k_avg
    )

    interaction_kernel = np.empty_like(
        k_avg
    )

    optimistic_reset_kernel = np.empty_like(
        k_avg
    )

    length = np.empty_like(
        k_avg
    )

    total_curvature_norm = np.empty_like(
        k_avg
    )

    curvature_concentration = np.empty_like(
        k_avg
    )

    min_payload_distance = np.empty_like(
        k_avg
    )

    u = np.linspace(
        0.0,
        2.0
        * math.pi,
        COARSE_NPHASE,
        endpoint=False,
        dtype=float,
    )[
        None,
        :
    ]

    du = (
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

        R = pset[
            "major"
        ][
            start:stop
        ][
            :,
            None
        ]

        a = pset[
            "minor"
        ][
            start:stop
        ][
            :,
            None
        ]

        gap = pset[
            "gap"
        ][
            start:stop
        ][
            :,
            None
        ]

        p = pset[
            "p"
        ][
            start:stop
        ][
            :,
            None
        ]

        q = pset[
            "q_winding"
        ][
            start:stop
        ][
            :,
            None
        ]

        phase = pset[
            "phase"
        ][
            start:stop
        ][
            :,
            None
        ]

        halfwidth = pset[
            "halfwidth"
        ][
            start:stop
        ][
            :,
            None
        ]

        theta = (
            q
            * u
            +
            phase
        )

        phi = (
            p
            * u
        )

        sin_theta = np.sin(
            theta
        )

        cos_theta = np.cos(
            theta
        )

        sin_phi = np.sin(
            phi
        )

        cos_phi = np.cos(
            phi
        )

        rho = (
            R
            +
            a
            * cos_theta
        )

        z = (
            -gap
            - a
            +
            a
            * sin_theta
        )

        drho = (
            -a
            * q
            * sin_theta
        )

        d2rho = (
            -a
            * q
            * q
            * cos_theta
        )

        dz = (
            a
            * q
            * cos_theta
        )

        d2z = (
            -a
            * q
            * q
            * sin_theta
        )

        dx = (
            drho
            * cos_phi
            -
            rho
            * p
            * sin_phi
        )

        dy = (
            drho
            * sin_phi
            +
            rho
            * p
            * cos_phi
        )

        d2x = (
            d2rho
            * cos_phi
            -
            2.0
            * drho
            * p
            * sin_phi
            -
            rho
            * p
            * p
            * cos_phi
        )

        d2y = (
            d2rho
            * sin_phi
            +
            2.0
            * drho
            * p
            * cos_phi
            -
            rho
            * p
            * p
            * sin_phi
        )

        speed = np.sqrt(
            dx
            * dx
            +
            dy
            * dy
            +
            dz
            * dz
        )

        cross_x = (
            dy
            * d2z
            -
            dz
            * d2y
        )

        cross_y = (
            dz
            * d2x
            -
            dx
            * d2z
        )

        cross_z = (
            dx
            * d2y
            -
            dy
            * d2x
        )

        cross_norm = np.sqrt(
            cross_x
            * cross_x
            +
            cross_y
            * cross_y
            +
            cross_z
            * cross_z
        )

        curvature = np.divide(
            cross_norm,
            np.maximum(
                speed ** 3,
                1.0e-300,
            ),
        )

        weights_sum = np.sum(
            speed,
            axis=1,
        )

        weights = (
            speed
            /
            weights_sum[
                :,
                None
            ]
        )

        dz_payload = (
            1.0
            - z
        )

        distance_sq = (
            rho
            * rho
            +
            dz_payload
            * dz_payload
        )

        kernel = (
            dz_payload
            /
            distance_sq ** 1.5
        )

        k_avg[
            start:stop
        ] = np.sum(
            weights
            * kernel,
            axis=1,
        )

        q_positive = (
            q
            >
            0.5
        )

        top_distance_minor = wrap_distance(
            theta,
            0.5
            * math.pi,
        )

        top_distance_major = wrap_distance(
            phi,
            0.0,
        )

        top_mask = np.where(
            q_positive,
            top_distance_minor
            <= halfwidth,
            top_distance_major
            <= halfwidth,
        )

        top_weights = (
            weights
            * top_mask
        )

        top_duty = np.sum(
            top_weights,
            axis=1,
        )

        interaction_duty[
            start:stop
        ] = top_duty

        interaction_kernel[
            start:stop
        ] = np.divide(
            np.sum(
                top_weights
                * kernel,
                axis=1,
            ),
            np.maximum(
                top_duty,
                1.0e-300,
            ),
        )

        optimistic_reset_kernel[
            start:stop
        ] = np.min(
            kernel,
            axis=1,
        )

        L = (
            weights_sum
            * du
        )

        length[
            start:stop
        ] = L

        total_curvature = np.sum(
            curvature
            * speed,
            axis=1,
        ) * du

        curvature_norm = (
            total_curvature
            /
            (
                2.0
                * math.pi
            )
        )

        total_curvature_norm[
            start:stop
        ] = curvature_norm

        mean_curvature = np.divide(
            total_curvature,
            np.maximum(
                L,
                1.0e-300,
            ),
        )

        curvature_concentration[
            start:stop
        ] = np.divide(
            np.max(
                curvature,
                axis=1,
            ),
            np.maximum(
                mean_curvature,
                1.0e-300,
            ),
        )

        min_payload_distance[
            start:stop
        ] = np.sqrt(
            np.min(
                distance_sq,
                axis=1,
            )
        )

    return {
        "k_avg":
            k_avg,

        "interaction_duty":
            interaction_duty,

        "interaction_kernel":
            interaction_kernel,

        "optimistic_reset_kernel":
            optimistic_reset_kernel,

        "length":
            length,

        "total_curvature_norm":
            total_curvature_norm,

        "curvature_concentration":
            curvature_concentration,

        "min_payload_distance":
            min_payload_distance,
    }


def kinetic_fraction(
    beta: np.ndarray,
) -> np.ndarray:
    """Relativistic kinetic fraction 1-1/gamma."""

    return (
        1.0
        -
        np.sqrt(
            np.maximum(
                0.0,
                1.0
                -
                beta
                * beta,
            )
        )
    )


def evaluate_family(
    family: str,
    pset: dict[str, np.ndarray],
    geom: dict[str, np.ndarray],
) -> dict[str, np.ndarray]:
    """Evaluate one source ledger over the complete common population."""

    beta_o_scan = pset[
        "beta_orbit"
    ]

    s_scan = pset[
        "spin_fraction"
    ]

    beta_s_scan = pset[
        "beta_spin"
    ]

    q_scan = pset[
        "q_scalar"
    ]

    f_scan = pset[
        "f_raw"
    ]

    curvature_norm = np.maximum(
        geom[
            "total_curvature_norm"
        ],
        1.0,
    )

    curvature_conc = np.maximum(
        geom[
            "curvature_concentration"
        ],
        1.0,
    )

    if family == "IDEAL_DEC_ORBIT_SPIN_CEILING":

        beta_o = np.ones_like(
            beta_o_scan
        )

        s = s_scan

        beta_s = np.ones_like(
            beta_o
        )

        q_scalar = np.full_like(
            beta_o,
            2.0,
        )

        f = np.ones_like(
            beta_o
        )

        guide_o = curvature_norm

        guide_s = np.ones_like(
            beta_o
        )

        overhead = np.zeros_like(
            beta_o
        )

        overhead_active_ratio = 0.0

    elif family == "ORBIT_SCALAR_NO_SPIN":

        beta_o = beta_o_scan

        s = np.zeros_like(
            beta_o
        )

        beta_s = np.zeros_like(
            beta_o
        )

        q_scalar = q_scan

        f = f_scan

        guide_o = (
            pset[
                "guide_multiplier"
            ]
            *
            curvature_norm
        )

        guide_s = np.ones_like(
            beta_o
        )

        overhead = (
            pset[
                "overhead"
            ]
        )

        overhead_active_ratio = 0.0

    elif family == "ORBIT_KINETIC_LIMITED_NO_SPIN":

        beta_o = beta_o_scan

        s = np.zeros_like(
            beta_o
        )

        beta_s = np.zeros_like(
            beta_o
        )

        q_scalar = q_scan

        f_cap = kinetic_fraction(
            beta_o
        )

        f = np.minimum(
            f_scan,
            f_cap,
        )

        guide_o = (
            pset[
                "guide_multiplier"
            ]
            *
            curvature_norm
        )

        guide_s = np.ones_like(
            beta_o
        )

        overhead = (
            0.20
            +
            pset[
                "overhead"
            ]
        )

        overhead_active_ratio = 1.0

    elif family == "ORBIT_PLUS_SPIN_SCALAR":

        beta_o = beta_o_scan

        s = s_scan

        beta_s = beta_s_scan

        q_scalar = q_scan

        f = f_scan

        guide_o = (
            pset[
                "guide_multiplier"
            ]
            *
            curvature_norm
        )

        guide_s = pset[
            "spin_guide_multiplier"
        ]

        overhead = pset[
            "overhead"
        ]

        overhead_active_ratio = 0.0

    elif family == "ORBIT_PLUS_SPIN_KINETIC_LIMITED":

        beta_o = beta_o_scan

        s = s_scan

        beta_s = beta_s_scan

        q_scalar = q_scan

        mobile = (
            1.0
            +
            s
        )

        accessible = (
            kinetic_fraction(
                beta_o
            )
            +
            s
            * kinetic_fraction(
                beta_s
            )
        )

        f_cap = np.divide(
            accessible,
            mobile,
        )

        f = np.minimum(
            f_scan,
            f_cap,
        )

        guide_o = (
            pset[
                "guide_multiplier"
            ]
            *
            curvature_norm
        )

        guide_s = pset[
            "spin_guide_multiplier"
        ]

        overhead = (
            0.20
            +
            pset[
                "overhead"
            ]
        )

        overhead_active_ratio = 1.0

    elif family == "ELASTIC_TORUS_KNOT_SCALAR":

        beta_o = beta_o_scan

        s = s_scan

        beta_s = beta_s_scan

        q_scalar = q_scan

        f = f_scan

        guide_o = (
            pset[
                "guide_multiplier"
            ]
            *
            curvature_norm
            *
            np.sqrt(
                curvature_conc
            )
        )

        guide_s = (
            pset[
                "spin_guide_multiplier"
            ]
            *
            np.sqrt(
                curvature_conc
            )
        )

        overhead = (
            0.50
            +
            pset[
                "overhead"
            ]
        )

        overhead_active_ratio = 0.5

    else:

        raise RuntimeError(
            f"Unknown family: {family}"
        )

    beta_o_sq = (
        beta_o
        * beta_o
    )

    beta_s_sq = (
        beta_s
        * beta_s
    )

    mobile_energy = (
        1.0
        +
        s
    )

    mobile_active = (
        1.0
        +
        beta_o_sq
        +
        s
        * (
            1.0
            +
            beta_s_sq
        )
    )

    mobile_active_ratio = np.divide(
        mobile_active,
        mobile_energy,
    )

    orbit_guide_energy = (
        guide_o
        * beta_o_sq
    )

    spin_guide_energy = (
        guide_s
        * s
        * beta_s_sq
    )

    extra_orbit_guide_active = (
        np.maximum(
            guide_o
            - 1.0,
            0.0,
        )
        *
        beta_o_sq
    )

    extra_spin_guide_active = (
        np.maximum(
            guide_s
            - 1.0,
            0.0,
        )
        *
        s
        *
        beta_s_sq
    )

    inventory_energy = (
        mobile_energy
        +
        orbit_guide_energy
        +
        spin_guide_energy
        +
        overhead
    )

    baseline_active = (
        mobile_active
        +
        extra_orbit_guide_active
        +
        extra_spin_guide_active
        +
        overhead_active_ratio
        * overhead
    )

    conversion_change = (
        f
        *
        mobile_energy
        *
        (
            q_scalar
            +
            mobile_active_ratio
        )
    )

    reset_capacity = (
        mobile_energy
        *
        (
            4.0
            -
            mobile_active_ratio
        )
    )

    reset_duty = np.divide(
        geom[
            "interaction_duty"
        ]
        *
        conversion_change,
        reset_capacity,
        out=np.full_like(
            conversion_change,
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
            geom[
                "interaction_duty"
            ]
        )
    )

    conversion_gain = (
        geom[
            "interaction_duty"
        ]
        *
        conversion_change
        *
        (
            geom[
                "interaction_kernel"
            ]
            -
            geom[
                "optimistic_reset_kernel"
            ]
        )
    )

    overhead_attraction = (
        geom[
            "interaction_duty"
        ]
        *
        overhead_active_ratio
        *
        overhead
        *
        geom[
            "interaction_kernel"
        ]
    )

    average_outward = (
        -
        baseline_active
        *
        geom[
            "k_avg"
        ]
        +
        conversion_gain
        -
        overhead_attraction
    )

    payload_clear = (
        geom[
            "min_payload_distance"
        ]
        >
        PAYLOAD_RADIUS_OVER_H
    )

    coefficient = np.where(
        virial_feasible
        &
        payload_clear
        &
        (
            average_outward
            >
            0.0
        ),
        inventory_energy
        /
        average_outward,
        np.inf,
    )

    return {
        "beta_orbit":
            beta_o,

        "spin_fraction":
            s,

        "beta_spin":
            beta_s,

        "q_scalar":
            q_scalar,

        "f":
            f,

        "guide_orbit":
            guide_o,

        "guide_spin":
            guide_s,

        "overhead":
            overhead,

        "overhead_active_ratio":
            np.full_like(
                beta_o,
                overhead_active_ratio,
            ),

        "mobile_energy":
            mobile_energy,

        "mobile_active_ratio":
            mobile_active_ratio,

        "inventory_energy":
            inventory_energy,

        "baseline_active":
            baseline_active,

        "conversion_change":
            conversion_change,

        "reset_capacity":
            reset_capacity,

        "reset_duty":
            reset_duty,

        "virial_feasible":
            virial_feasible,

        "average_outward":
            average_outward,

        "coefficient":
            coefficient,
    }


def top_indices(
    values: np.ndarray,
    count: int,
) -> np.ndarray:
    """Return indices for the lowest finite values."""

    finite = np.flatnonzero(
        np.isfinite(
            values
        )
    )

    if not len(
        finite
    ):
        return np.asarray(
            [],
            dtype=int,
        )

    if len(
        finite
    ) <= count:

        return finite[
            np.argsort(
                values[
                    finite
                ]
            )
        ]

    selected_local = np.argpartition(
        values[
            finite
        ],
        count - 1,
    )[
        :count
    ]

    selected = finite[
        selected_local
    ]

    return selected[
        np.argsort(
            values[
                selected
            ]
        )
    ]


def candidate_from_index(
    family: str,
    index: int,
    pset: dict[str, np.ndarray],
    geom: dict[str, np.ndarray],
    result: dict[str, np.ndarray],
) -> dict[str, Any]:
    """Serialize one coarse candidate."""

    winding_index = int(
        pset[
            "winding_index"
        ][
            index
        ]
    )

    winding = WINDINGS[
        winding_index
    ]

    return {
        "family":
            family,

        "index":
            index,

        "winding_index":
            winding_index,

        "p":
            int(
                winding[
                    0
                ]
            ),

        "q_winding":
            int(
                winding[
                    1
                ]
            ),

        "major":
            float(
                pset[
                    "major"
                ][
                    index
                ]
            ),

        "minor":
            float(
                pset[
                    "minor"
                ][
                    index
                ]
            ),

        "minor_ratio":
            float(
                pset[
                    "minor_ratio"
                ][
                    index
                ]
            ),

        "gap":
            float(
                pset[
                    "gap"
                ][
                    index
                ]
            ),

        "phase":
            float(
                pset[
                    "phase"
                ][
                    index
                ]
            ),

        "halfwidth":
            float(
                pset[
                    "halfwidth"
                ][
                    index
                ]
            ),

        "beta_orbit":
            float(
                result[
                    "beta_orbit"
                ][
                    index
                ]
            ),

        "spin_fraction":
            float(
                result[
                    "spin_fraction"
                ][
                    index
                ]
            ),

        "beta_spin":
            float(
                result[
                    "beta_spin"
                ][
                    index
                ]
            ),

        "q_scalar":
            float(
                result[
                    "q_scalar"
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

        "guide_orbit":
            float(
                result[
                    "guide_orbit"
                ][
                    index
                ]
            ),

        "guide_spin":
            float(
                result[
                    "guide_spin"
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

        "coarse_C":
            float(
                result[
                    "coefficient"
                ][
                    index
                ]
            ),

        "coarse_A":
            float(
                result[
                    "average_outward"
                ][
                    index
                ]
            ),

        "coarse_interaction_duty":
            float(
                geom[
                    "interaction_duty"
                ][
                    index
                ]
            ),

        "coarse_reset_duty":
            float(
                result[
                    "reset_duty"
                ][
                    index
                ]
            ),

        "total_curvature_norm":
            float(
                geom[
                    "total_curvature_norm"
                ][
                    index
                ]
            ),

        "curvature_concentration":
            float(
                geom[
                    "curvature_concentration"
                ][
                    index
                ]
            ),

        "min_payload_distance":
            float(
                geom[
                    "min_payload_distance"
                ][
                    index
                ]
            ),
    }


def highres_orbit(
    candidate: dict[str, Any],
    nphase: int,
) -> dict[str, Any]:
    """High-resolution torus-knot trajectory."""

    u = np.linspace(
        0.0,
        2.0
        * math.pi,
        nphase,
        endpoint=False,
        dtype=float,
    )

    R = candidate[
        "major"
    ]

    a = candidate[
        "minor"
    ]

    gap = candidate[
        "gap"
    ]

    p = float(
        candidate[
            "p"
        ]
    )

    q = float(
        candidate[
            "q_winding"
        ]
    )

    phase = candidate[
        "phase"
    ]

    theta = (
        q
        * u
        +
        phase
    )

    phi = (
        p
        * u
    )

    sin_theta = np.sin(
        theta
    )

    cos_theta = np.cos(
        theta
    )

    sin_phi = np.sin(
        phi
    )

    cos_phi = np.cos(
        phi
    )

    rho = (
        R
        +
        a
        * cos_theta
    )

    x = (
        rho
        * cos_phi
    )

    y = (
        rho
        * sin_phi
    )

    z = (
        -gap
        - a
        +
        a
        * sin_theta
    )

    drho = (
        -a
        * q
        * sin_theta
    )

    d2rho = (
        -a
        * q
        * q
        * cos_theta
    )

    dz = (
        a
        * q
        * cos_theta
    )

    d2z = (
        -a
        * q
        * q
        * sin_theta
    )

    dx = (
        drho
        * cos_phi
        -
        rho
        * p
        * sin_phi
    )

    dy = (
        drho
        * sin_phi
        +
        rho
        * p
        * cos_phi
    )

    d2x = (
        d2rho
        * cos_phi
        -
        2.0
        * drho
        * p
        * sin_phi
        -
        rho
        * p
        * p
        * cos_phi
    )

    d2y = (
        d2rho
        * sin_phi
        +
        2.0
        * drho
        * p
        * cos_phi
        -
        rho
        * p
        * p
        * sin_phi
    )

    speed = np.sqrt(
        dx
        * dx
        +
        dy
        * dy
        +
        dz
        * dz
    )

    cross_x = (
        dy
        * d2z
        -
        dz
        * d2y
    )

    cross_y = (
        dz
        * d2x
        -
        dx
        * d2z
    )

    cross_z = (
        dx
        * d2y
        -
        dy
        * d2x
    )

    curvature = np.sqrt(
        cross_x
        * cross_x
        +
        cross_y
        * cross_y
        +
        cross_z
        * cross_z
    ) / np.maximum(
        speed ** 3,
        1.0e-300,
    )

    weights = (
        speed
        /
        np.sum(
            speed
        )
    )

    dz_payload = (
        1.0
        - z
    )

    distance_sq = (
        x
        * x
        +
        y
        * y
        +
        dz_payload
        * dz_payload
    )

    kernel = (
        dz_payload
        /
        distance_sq ** 1.5
    )

    if candidate[
        "q_winding"
    ] > 0:

        interaction_phase = theta
        interaction_center = (
            0.5
            * math.pi
        )

        reset_center = (
            1.5
            * math.pi
        )

    else:

        interaction_phase = phi
        interaction_center = 0.0
        reset_center = math.pi

    top_mask = (
        wrap_distance(
            interaction_phase,
            interaction_center,
        )
        <=
        candidate[
            "halfwidth"
        ]
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

    du = (
        2.0
        * math.pi
        / nphase
    )

    length = float(
        np.sum(
            speed
        )
        * du
    )

    total_curvature = float(
        np.sum(
            curvature
            * speed
        )
        * du
    )

    return {
        "u":
            u,

        "theta":
            theta,

        "phi":
            phi,

        "interaction_phase":
            interaction_phase,

        "reset_center":
            reset_center,

        "x":
            x,

        "y":
            y,

        "z":
            z,

        "weights":
            weights,

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

        "length":
            length,

        "total_curvature_norm":
            (
                total_curvature
                /
                (
                    2.0
                    * math.pi
                )
            ),

        "curvature_concentration":
            float(
                np.max(
                    curvature
                )
                /
                max(
                    total_curvature
                    / length,
                    1.0e-300,
                )
            ),

        "min_payload_distance":
            float(
                np.sqrt(
                    np.min(
                        distance_sq
                    )
                )
            ),
    }


def reset_window(
    orbit: dict[str, Any],
    target_duty: float,
) -> tuple[
    np.ndarray,
    float,
    float,
]:
    """Finite contiguous reset windows centered on the low-kernel phase."""

    phase = np.asarray(
        orbit[
            "interaction_phase"
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

    center = float(
        orbit[
            "reset_center"
        ]
    )

    if target_duty <= 0.0:

        mask = np.zeros_like(
            phase,
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
            wrap_distance(
                phase,
                center,
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
        wrap_distance(
            phase,
            center,
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

    reset_kernel = float(
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
        reset_kernel,
    )


def refine_candidate(
    candidate: dict[str, Any],
) -> dict[str, Any]:
    """High-resolution full-cycle reconstruction."""

    orbit = highres_orbit(
        candidate,
        REFINE_NPHASE,
    )

    beta_o = candidate[
        "beta_orbit"
    ]

    beta_s = candidate[
        "beta_spin"
    ]

    s = candidate[
        "spin_fraction"
    ]

    q_scalar = candidate[
        "q_scalar"
    ]

    f = candidate[
        "f"
    ]

    guide_o = candidate[
        "guide_orbit"
    ]

    guide_s = candidate[
        "guide_spin"
    ]

    overhead = candidate[
        "overhead"
    ]

    overhead_active_ratio = candidate[
        "overhead_active_ratio"
    ]

    beta_o_sq = (
        beta_o
        * beta_o
    )

    beta_s_sq = (
        beta_s
        * beta_s
    )

    mobile_energy = (
        1.0
        +
        s
    )

    mobile_active = (
        1.0
        +
        beta_o_sq
        +
        s
        * (
            1.0
            +
            beta_s_sq
        )
    )

    mobile_active_ratio = (
        mobile_active
        / mobile_energy
    )

    inventory = (
        mobile_energy
        +
        guide_o
        * beta_o_sq
        +
        guide_s
        * s
        * beta_s_sq
        +
        overhead
    )

    baseline_active = (
        mobile_active
        +
        max(
            guide_o
            - 1.0,
            0.0,
        )
        * beta_o_sq
        +
        max(
            guide_s
            - 1.0,
            0.0,
        )
        * s
        * beta_s_sq
        +
        overhead_active_ratio
        * overhead
    )

    conversion_change = (
        f
        *
        mobile_energy
        *
        (
            q_scalar
            +
            mobile_active_ratio
        )
    )

    reset_capacity = (
        mobile_energy
        *
        (
            4.0
            -
            mobile_active_ratio
        )
    )

    reset_duty_required = (
        orbit[
            "top_duty"
        ]
        *
        conversion_change
        /
        reset_capacity
        if reset_capacity > 1.0e-12
        else math.inf
    )

    virial_feasible = bool(
        reset_duty_required
        <=
        1.0
        -
        orbit[
            "top_duty"
        ]
    )

    if virial_feasible:

        (
            bottom_mask,
            bottom_duty,
            bottom_kernel,
        ) = reset_window(
            orbit,
            reset_duty_required,
        )

        conversion_gain = (
            orbit[
                "top_duty"
            ]
            *
            conversion_change
            *
            orbit[
                "top_kernel"
            ]
            -
            bottom_duty
            *
            reset_capacity
            *
            bottom_kernel
        )

        overhead_attraction = (
            orbit[
                "top_duty"
            ]
            *
            overhead_active_ratio
            *
            overhead
            *
            orbit[
                "top_kernel"
            ]
        )

        A = (
            -
            baseline_active
            *
            orbit[
                "k_avg"
            ]
            +
            conversion_gain
            -
            overhead_attraction
        )

    else:

        bottom_mask = np.zeros(
            REFINE_NPHASE,
            dtype=bool,
        )

        bottom_duty = math.nan
        bottom_kernel = math.nan

        conversion_gain = -math.inf
        overhead_attraction = math.inf

        A = -math.inf

    C = (
        inventory
        / A
        if (
            virial_feasible
            and A > 0.0
        )
        else math.inf
    )

    return {
        **candidate,

        "orbit":
            orbit,

        "bottom_mask":
            bottom_mask,

        "C_refined":
            C,

        "A_refined":
            A,

        "inventory_energy":
            inventory,

        "baseline_active":
            baseline_active,

        "mobile_active_ratio":
            mobile_active_ratio,

        "interaction_duty_refined":
            orbit[
                "top_duty"
            ],

        "reset_duty_refined":
            bottom_duty,

        "reset_duty_required":
            reset_duty_required,

        "interaction_kernel_refined":
            orbit[
                "top_kernel"
            ],

        "reset_kernel_refined":
            bottom_kernel,

        "virial_feasible_refined":
            virial_feasible,

        "total_curvature_norm_refined":
            orbit[
                "total_curvature_norm"
            ],

        "curvature_concentration_refined":
            orbit[
                "curvature_concentration"
            ],

        "min_payload_distance_refined":
            orbit[
                "min_payload_distance"
            ],

        "finite_payload_clear":
            bool(
                orbit[
                    "min_payload_distance"
                ]
                >
                PAYLOAD_RADIUS_OVER_H
            ),

        "beats_006D":
            bool(
                C
                <
                C006D
            ),

        "beats_024D_scalar":
            bool(
                C
                <
                C024D_SCALAR
            ),
    }


def vector_bundle_audit(
    refined: dict[str, Any],
    bundle_count: int,
) -> dict[str, Any]:
    """3-D finite-payload vector field for a rotated orbit bundle."""

    candidate = {
        key: value
        for key, value in refined.items()
        if key not in (
            "orbit",
            "bottom_mask",
        )
    }

    orbit = highres_orbit(
        candidate,
        VECTOR_NPHASE,
    )

    (
        bottom_mask,
        bottom_duty,
        _bottom_kernel,
    ) = reset_window(
        orbit,
        refined[
            "reset_duty_required"
        ],
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

    source_phase = np.full(
        VECTOR_NPHASE,
        refined[
            "baseline_active"
        ],
        dtype=float,
    )

    conversion_change = (
        refined[
            "f"
        ]
        *
        (
            1.0
            +
            refined[
                "spin_fraction"
            ]
        )
        *
        (
            refined[
                "q_scalar"
            ]
            +
            refined[
                "mobile_active_ratio"
            ]
        )
    )

    reset_capacity = (
        (
            1.0
            +
            refined[
                "spin_fraction"
            ]
        )
        *
        (
            4.0
            -
            refined[
                "mobile_active_ratio"
            ]
        )
    )

    source_phase[
        top_mask
    ] -= (
        conversion_change
    )

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

    source_phase[
        bottom_mask
    ] += (
        reset_capacity
    )

    x0 = np.asarray(
        orbit[
            "x"
        ],
        dtype=float,
    )

    y0 = np.asarray(
        orbit[
            "y"
        ],
        dtype=float,
    )

    z0 = np.asarray(
        orbit[
            "z"
        ],
        dtype=float,
    )

    target_radii = (
        0.0,
        0.125,
        0.25,
        0.375,
        0.5,
    )

    target_azimuths = np.linspace(
        0.0,
        2.0
        * math.pi,
        12,
        endpoint=False,
    )

    rows = []

    all_axial = []

    maximum_transverse_fraction = 0.0

    for target_r in target_radii:

        local_axial = []
        local_transverse = []

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

            for k in range(
                bundle_count
            ):

                angle = (
                    2.0
                    * math.pi
                    * k
                    / bundle_count
                )

                ca = math.cos(
                    angle
                )

                sa = math.sin(
                    angle
                )

                sx = (
                    ca
                    * x0
                    -
                    sa
                    * y0
                )

                sy = (
                    sa
                    * x0
                    +
                    ca
                    * y0
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
                    z0
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
                    weights
                    *
                    source_phase
                    *
                    inv_d3
                    /
                    bundle_count
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

            axial = float(
                acc[
                    2
                ]
            )

            transverse = float(
                math.hypot(
                    acc[
                        0
                    ],
                    acc[
                        1
                    ],
                )
            )

            local_axial.append(
                axial
            )

            local_transverse.append(
                transverse
            )

            all_axial.append(
                axial
            )

            if abs(
                axial
            ) > 1.0e-300:

                maximum_transverse_fraction = max(
                    maximum_transverse_fraction,
                    transverse
                    /
                    abs(
                        axial
                    ),
                )

        rows.append({
            "radius":
                target_r,

            "axial_min":
                float(
                    np.min(
                        local_axial
                    )
                ),

            "axial_max":
                float(
                    np.max(
                        local_axial
                    )
                ),

            "axial_mean":
                float(
                    np.mean(
                        local_axial
                    )
                ),

            "transverse_max":
                float(
                    np.max(
                        local_transverse
                    )
                ),
        })

    min_axial = float(
        np.min(
            all_axial
        )
    )

    max_axial = float(
        np.max(
            all_axial
        )
    )

    mean_axial = float(
        np.mean(
            all_axial
        )
    )

    flatness = (
        (
            max_axial
            -
            min_axial
        )
        /
        max(
            abs(
                mean_axial
            ),
            1.0e-300,
        )
    )

    on_axis = rows[
        0
    ][
        "axial_mean"
    ]

    return {
        "bundle_count":
            bundle_count,

        "rows":
            rows,

        "minimum_axial":
            min_axial,

        "maximum_axial":
            max_axial,

        "mean_axial":
            mean_axial,

        "axial_flatness":
            flatness,

        "maximum_transverse_fraction":
            maximum_transverse_fraction,

        "all_axial_outward":
            bool(
                min_axial
                >
                0.0
            ),

        "on_axis_A":
            on_axis,

        "scalar_A":
            refined[
                "A_refined"
            ],

        "on_axis_relative_error":
            relerr(
                on_axis,
                refined[
                    "A_refined"
                ],
            ),

        "bottom_duty":
            bottom_duty,
    }


def choose_candidates(
    family: str,
    pset: dict[str, np.ndarray],
    geom: dict[str, np.ndarray],
    result: dict[str, np.ndarray],
) -> list[dict[str, Any]]:
    """Overall plus per-winding candidate selection."""

    selected_indices = set()

    overall = top_indices(
        result[
            "coefficient"
        ],
        TOP_OVERALL_PER_FAMILY,
    )

    selected_indices.update(
        int(
            index
        )
        for index in overall
    )

    for winding_index in range(
        len(
            WINDINGS
        )
    ):

        mask = (
            pset[
                "winding_index"
            ]
            ==
            winding_index
        )

        indices = np.flatnonzero(
            mask
            &
            np.isfinite(
                result[
                    "coefficient"
                ]
            )
        )

        if not len(
            indices
        ):
            continue

        values = result[
            "coefficient"
        ][
            indices
        ]

        count = min(
            TOP_PER_WINDING_PER_FAMILY,
            len(
                indices
            ),
        )

        if len(
            indices
        ) <= count:

            local = np.argsort(
                values
            )

        else:

            local = np.argpartition(
                values,
                count - 1,
            )[
                :count
            ]

        for local_index in local:

            selected_indices.add(
                int(
                    indices[
                        local_index
                    ]
                )
            )

    return [
        candidate_from_index(
            family,
            index,
            pset,
            geom,
            result,
        )
        for index in sorted(
            selected_indices
        )
    ]


def spin_sweep(
    best_no_spin: dict[str, Any],
) -> list[dict[str, Any]]:
    """Exhaustive fixed-geometry orbit+spin comparison."""

    candidate = {
        key: value
        for key, value in best_no_spin.items()
        if key not in (
            "orbit",
            "bottom_mask",
        )
    }

    orbit = highres_orbit(
        candidate,
        8192,
    )

    beta_orbit_grid = np.linspace(
        0.03,
        0.999,
        72,
    )

    spin_fraction_grid = np.linspace(
        0.0,
        2.0,
        48,
    )

    beta_spin_grid = np.linspace(
        0.0,
        0.999,
        48,
    )

    rows = []

    for mode in (
        "UNRESTRICTED",
        "KINETIC_LIMITED",
    ):

        for beta_o in beta_orbit_grid:

            bo2 = (
                beta_o
                * beta_o
            )

            for s in spin_fraction_grid:

                for beta_s in beta_spin_grid:

                    bs2 = (
                        beta_s
                        * beta_s
                    )

                    mobile_energy = (
                        1.0
                        +
                        s
                    )

                    mobile_active = (
                        1.0
                        +
                        bo2
                        +
                        s
                        * (
                            1.0
                            +
                            bs2
                        )
                    )

                    mobile_ratio = (
                        mobile_active
                        /
                        mobile_energy
                    )

                    if mode == "UNRESTRICTED":

                        f = best_no_spin[
                            "f"
                        ]

                    else:

                        accessible = (
                            (
                                1.0
                                -
                                math.sqrt(
                                    max(
                                        0.0,
                                        1.0
                                        -
                                        bo2,
                                    )
                                )
                            )
                            +
                            s
                            * (
                                1.0
                                -
                                math.sqrt(
                                    max(
                                        0.0,
                                        1.0
                                        -
                                        bs2,
                                    )
                                )
                            )
                        )

                        f = min(
                            best_no_spin[
                                "f"
                            ],
                            accessible
                            /
                            mobile_energy,
                        )

                    guide_o = (
                        best_no_spin[
                            "total_curvature_norm_refined"
                        ]
                    )

                    guide_s = 1.0

                    inventory = (
                        mobile_energy
                        +
                        guide_o
                        * bo2
                        +
                        guide_s
                        * s
                        * bs2
                    )

                    baseline_active = (
                        mobile_active
                        +
                        max(
                            guide_o
                            - 1.0,
                            0.0,
                        )
                        * bo2
                    )

                    D = (
                        f
                        *
                        mobile_energy
                        *
                        (
                            best_no_spin[
                                "q_scalar"
                            ]
                            +
                            mobile_ratio
                        )
                    )

                    cap = (
                        mobile_energy
                        *
                        (
                            4.0
                            -
                            mobile_ratio
                        )
                    )

                    reset_duty = (
                        orbit[
                            "top_duty"
                        ]
                        * D
                        / cap
                        if cap
                        > 1.0e-12
                        else math.inf
                    )

                    if (
                        reset_duty
                        >
                        1.0
                        -
                        orbit[
                            "top_duty"
                        ]
                    ):

                        C = math.inf
                        A = -math.inf

                    else:

                        (
                            _mask,
                            actual_reset_duty,
                            reset_kernel,
                        ) = reset_window(
                            orbit,
                            reset_duty,
                        )

                        A = (
                            -
                            baseline_active
                            * orbit[
                                "k_avg"
                            ]
                            +
                            orbit[
                                "top_duty"
                            ]
                            * D
                            * orbit[
                                "top_kernel"
                            ]
                            -
                            actual_reset_duty
                            * cap
                            * reset_kernel
                        )

                        C = (
                            inventory
                            / A
                            if A > 0.0
                            else math.inf
                        )

                    rows.append({
                        "mode":
                            mode,

                        "beta_orbit":
                            beta_o,

                        "spin_fraction":
                            s,

                        "beta_spin":
                            beta_s,

                        "f":
                            f,

                        "A":
                            A,

                        "C":
                            C,
                    })

    return rows


def clean_refined(
    item: dict[str, Any],
) -> dict[str, Any]:
    """Remove large phase arrays."""

    return {
        key: value
        for key, value in item.items()
        if key not in (
            "orbit",
            "bottom_mask",
        )
    }


def main() -> None:
    """Execute 024D1."""

    print(
        "=== 024D1 INTERNAL TOROIDAL ORBIT + SPIN CAMPAIGN ===",
        flush=True,
    )

    require(
        INPUT
    )

    prior = json.loads(
        INPUT.read_text(
            encoding="utf-8"
        )
    )

    if (
        prior[
            "decision"
        ][
            "024D"
        ]
        !=
        "YELLOW_SCALAR_STRESS_CONVERSION_HEADROOM_COUNTERROTATION_NOT_YET_PROMOTED"
    ):
        raise RuntimeError(
            "Unexpected 024D predecessor decision."
        )

    print(
        "\n=== A — FIXED SCIENTIFIC ANCHORS ==="
    )

    print(
        f"C_006D="
        f"{C006D:.15f}"
    )

    print(
        f"C_024D_SCALAR="
        f"{C024D_SCALAR:.15f}"
    )

    print(
        "PURE_COUNTERORBIT_WITHOUT_CONVERSION=RED_ANALYTIC"
    )

    print(
        "PURE_LINEAR_EM_ORBIT=RED_ANALYTIC"
    )

    print(
        "SPIN_RECEIVES_FREE_NEGATIVE_STRESS=NO"
    )

    print(
        "SPIN_ENERGY_AND_CONFINEMENT_INCLUDED=YES"
    )

    print(
        "TOTAL_CURVATURE_LOWER_BOUND=2_PI"
    )

    print(
        "CURVATURE_NORMALIZED_BY_FENCHEL_BOUND=YES"
    )

    print(
        "FINITE_PAYLOAD_RADIUS_OVER_H="
        f"{PAYLOAD_RADIUS_OVER_H:.15f}"
    )

    # ------------------------------------------------------------
    # B. Parameter population + geometry.
    # ------------------------------------------------------------

    print(
        "\n=== B — BUILD 2^20 TORUS-ORBIT POPULATION ===",
        flush=True,
    )

    pset = build_parameters()

    print(
        f"BASE_SOBOL_CASES="
        f"{N_CASES}"
    )

    print(
        f"FAMILY_EVALUATIONS="
        f"{N_CASES * len(FAMILIES)}"
    )

    print(
        "WINDINGS="
        + ",".join(
            f"({p},{q})"
            for p, q in WINDINGS
        )
    )

    print(
        "GEOMETRY_FEATURE_BUILD=BEGIN",
        flush=True,
    )

    geom = geometry_features(
        pset
    )

    print(
        "GEOMETRY_FEATURE_BUILD=PASS",
        flush=True,
    )

    print(
        f"CURVATURE_NORM_MIN="
        f"{float(np.min(geom['total_curvature_norm'])):.12e}"
    )

    print(
        f"CURVATURE_NORM_MAX="
        f"{float(np.max(geom['total_curvature_norm'])):.12e}"
    )

    print(
        f"CURVATURE_CONCENTRATION_MAX="
        f"{float(np.max(geom['curvature_concentration'])):.12e}"
    )

    print(
        f"MIN_PAYLOAD_DISTANCE_MIN="
        f"{float(np.min(geom['min_payload_distance'])):.12e}"
    )

    # ------------------------------------------------------------
    # C. Multi-family campaign.
    # ------------------------------------------------------------

    print(
        "\n=== C — MULTI-FAMILY ORBIT / SPIN CAMPAIGN ===",
        flush=True,
    )

    results = {}

    coarse_family_summary = {}

    winding_rows = []

    candidate_pool = []

    for family in FAMILIES:

        print(
            f"FAMILY_BEGIN={family}",
            flush=True,
        )

        result = evaluate_family(
            family,
            pset,
            geom,
        )

        results[
            family
        ] = result

        coefficient = result[
            "coefficient"
        ]

        positive_count = int(
            np.count_nonzero(
                np.isfinite(
                    coefficient
                )
            )
        )

        beat_006d_count = int(
            np.count_nonzero(
                coefficient
                <
                C006D
            )
        )

        beat_024d_count = int(
            np.count_nonzero(
                coefficient
                <
                C024D_SCALAR
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

            best_winding_index = int(
                pset[
                    "winding_index"
                ][
                    best_index
                ]
            )

            best_winding = WINDINGS[
                best_winding_index
            ]

        else:

            best_index = -1
            best_c = math.inf
            best_winding = (
                -1,
                -1,
            )

        coarse_family_summary[
            family
        ] = {
            "positive_cases":
                positive_count,

            "beats_006D_cases":
                beat_006d_count,

            "beats_024D_scalar_cases":
                beat_024d_count,

            "best_index":
                best_index,

            "best_C":
                best_c,

            "best_winding":
                list(
                    best_winding
                ),
        }

        print(
            f"{family}_COARSE_POSITIVE_CASES="
            f"{positive_count}"
        )

        print(
            f"{family}_COARSE_BEATS_006D_CASES="
            f"{beat_006d_count}"
        )

        print(
            f"{family}_COARSE_BEATS_024D_SCALAR_CASES="
            f"{beat_024d_count}"
        )

        print(
            f"{family}_BEST_COARSE_C="
            f"{best_c:.15e}"
        )

        print(
            f"{family}_BEST_COARSE_WINDING="
            f"{best_winding[0]},{best_winding[1]}"
        )

        for winding_index, winding in enumerate(
            WINDINGS
        ):

            mask = (
                pset[
                    "winding_index"
                ]
                ==
                winding_index
            )

            local_indices = np.flatnonzero(
                mask
                &
                np.isfinite(
                    coefficient
                )
            )

            if len(
                local_indices
            ):

                local_best_index = int(
                    local_indices[
                        np.argmin(
                            coefficient[
                                local_indices
                            ]
                        )
                    ]
                )

                local_best_c = float(
                    coefficient[
                        local_best_index
                    ]
                )

                local_positive = int(
                    len(
                        local_indices
                    )
                )

                local_beat_006d = int(
                    np.count_nonzero(
                        coefficient[
                            mask
                        ]
                        <
                        C006D
                    )
                )

                local_beat_024d = int(
                    np.count_nonzero(
                        coefficient[
                            mask
                        ]
                        <
                        C024D_SCALAR
                    )
                )

            else:

                local_best_index = -1
                local_best_c = math.inf
                local_positive = 0
                local_beat_006d = 0
                local_beat_024d = 0

            winding_rows.append({
                "family":
                    family,

                "p":
                    winding[
                        0
                    ],

                "q":
                    winding[
                        1
                    ],

                "positive_cases":
                    local_positive,

                "beats_006D_cases":
                    local_beat_006d,

                "beats_024D_scalar_cases":
                    local_beat_024d,

                "best_coarse_C":
                    local_best_c,

                "best_coarse_index":
                    local_best_index,
            })

            print(
                f"WINDING_FAMILY={family} "
                f"P={winding[0]} "
                f"Q={winding[1]} "
                f"POSITIVE={local_positive} "
                f"BEAT006D={local_beat_006d} "
                f"BEAT024D={local_beat_024d} "
                f"BEST_C={local_best_c:.12e}"
            )

        candidate_pool.extend(
            choose_candidates(
                family,
                pset,
                geom,
                result,
            )
        )

        print(
            f"FAMILY_END={family}",
            flush=True,
        )

    # ------------------------------------------------------------
    # D. High-resolution refinement.
    # ------------------------------------------------------------

    print(
        "\n=== D — 32768-PHASE FINITE-RESET REFINEMENT ===",
        flush=True,
    )

    refined_all = []

    for index, candidate in enumerate(
        candidate_pool
    ):

        if (
            index
            %
            50
            ==
            0
        ):

            print(
                f"REFINEMENT_PROGRESS="
                f"{index}/{len(candidate_pool)}",
                flush=True,
            )

        refined_all.append(
            refine_candidate(
                candidate
            )
        )

    refined_by_family = {}

    for family in FAMILIES:

        rows = [
            item
            for item in refined_all
            if (
                item[
                    "family"
                ]
                ==
                family
                and math.isfinite(
                    item[
                        "C_refined"
                    ]
                )
            )
        ]

        rows.sort(
            key=lambda item: item[
                "C_refined"
            ]
        )

        refined_by_family[
            family
        ] = rows

        if not rows:

            print(
                f"{family}_REFINED_POSITIVE_CASES=0"
            )

            continue

        best = rows[
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
            f"{family}_BEST_REFINED_WINDING="
            f"{best['p']},{best['q_winding']}"
        )

        print(
            f"{family}_BEST_REFINED_MAJOR_R="
            f"{best['major']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_MINOR_R="
            f"{best['minor']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_GAP="
            f"{best['gap']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_BETA_ORBIT="
            f"{best['beta_orbit']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_SPIN_FRACTION="
            f"{best['spin_fraction']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_BETA_SPIN="
            f"{best['beta_spin']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_Q_SCALAR="
            f"{best['q_scalar']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_F="
            f"{best['f']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_INTERACTION_DUTY="
            f"{best['interaction_duty_refined']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_RESET_DUTY="
            f"{best['reset_duty_refined']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_CURVATURE_NORM="
            f"{best['total_curvature_norm_refined']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_CURVATURE_CONCENTRATION="
            f"{best['curvature_concentration_refined']:.15e}"
        )

        print(
            f"{family}_BEST_REFINED_PAYLOAD_CLEAR="
            + (
                "YES"
                if best[
                    "finite_payload_clear"
                ]
                else "NO"
            )
        )

        print(
            f"{family}_BEST_REFINED_BEATS_006D="
            + (
                "YES"
                if best[
                    "beats_006D"
                ]
                else "NO"
            )
        )

        print(
            f"{family}_BEST_REFINED_BEATS_024D_SCALAR="
            + (
                "YES"
                if best[
                    "beats_024D_scalar"
                ]
                else "NO"
            )
        )

    # ------------------------------------------------------------
    # E. Refined winding rankings.
    # ------------------------------------------------------------

    print(
        "\n=== E — REFINED WINDING TOPOLOGY RANKING ==="
    )

    refined_winding_summary = []

    for family in FAMILIES:

        rows = refined_by_family[
            family
        ]

        for winding in WINDINGS:

            local = [
                item
                for item in rows
                if (
                    item[
                        "p"
                    ]
                    ==
                    winding[
                        0
                    ]
                    and
                    item[
                        "q_winding"
                    ]
                    ==
                    winding[
                        1
                    ]
                )
            ]

            if local:

                best = min(
                    local,
                    key=lambda item: item[
                        "C_refined"
                    ],
                )

                best_c = best[
                    "C_refined"
                ]

            else:

                best = None
                best_c = math.inf

            refined_winding_summary.append({
                "family":
                    family,

                "p":
                    winding[
                        0
                    ],

                "q":
                    winding[
                        1
                    ],

                "best_refined_C":
                    best_c,

                "beats_006D":
                    bool(
                        best_c
                        <
                        C006D
                    ),

                "beats_024D_scalar":
                    bool(
                        best_c
                        <
                        C024D_SCALAR
                    ),
            })

            print(
                f"REFINED_WINDING_FAMILY={family} "
                f"P={winding[0]} "
                f"Q={winding[1]} "
                f"BEST_C={best_c:.12e} "
                f"BEAT006D={'YES' if best_c < C006D else 'NO'} "
                f"BEAT024D={'YES' if best_c < C024D_SCALAR else 'NO'}"
            )

    # ------------------------------------------------------------
    # F. Pure toroidal vs poloidal vs helical.
    # ------------------------------------------------------------

    print(
        "\n=== F — ORBIT-TYPE COMPARISON ==="
    )

    scalar_rows = refined_by_family[
        "ORBIT_SCALAR_NO_SPIN"
    ]

    def best_for_winding(
        winding: tuple[int, int],
    ) -> dict[str, Any] | None:

        choices = [
            row
            for row in scalar_rows
            if (
                row[
                    "p"
                ]
                ==
                winding[
                    0
                ]
                and
                row[
                    "q_winding"
                ]
                ==
                winding[
                    1
                ]
            )
        ]

        if not choices:
            return None

        return min(
            choices,
            key=lambda row: row[
                "C_refined"
            ],
        )

    toroidal_best = best_for_winding(
        (
            1,
            0,
        )
    )

    poloidal_best = best_for_winding(
        (
            0,
            1,
        )
    )

    helical_rows = [
        row
        for row in scalar_rows
        if (
            row[
                "p"
            ]
            >
            0
            and
            row[
                "q_winding"
            ]
            >
            0
        )
    ]

    helical_best = (
        min(
            helical_rows,
            key=lambda row: row[
                "C_refined"
            ],
        )
        if helical_rows
        else None
    )

    pure_toroidal_c = (
        toroidal_best[
            "C_refined"
        ]
        if toroidal_best
        else math.inf
    )

    pure_poloidal_c = (
        poloidal_best[
            "C_refined"
        ]
        if poloidal_best
        else math.inf
    )

    best_helical_c = (
        helical_best[
            "C_refined"
        ]
        if helical_best
        else math.inf
    )

    print(
        f"PURE_TOROIDAL_BEST_SCALAR_C="
        f"{pure_toroidal_c:.15e}"
    )

    print(
        f"PURE_POLOIDAL_BEST_SCALAR_C="
        f"{pure_poloidal_c:.15e}"
    )

    print(
        f"BEST_HELICAL_SCALAR_C="
        f"{best_helical_c:.15e}"
    )

    if helical_best:

        print(
            f"BEST_HELICAL_WINDING="
            f"{helical_best['p']},{helical_best['q_winding']}"
        )

    # ------------------------------------------------------------
    # G. Bundle directionality.
    # ------------------------------------------------------------

    print(
        "\n=== G — MULTI-ORBIT BUNDLE DIRECTIONAL AUDIT ===",
        flush=True,
    )

    best_family_candidates = {}

    bundle_audits = {}

    for family in FAMILIES:

        rows = refined_by_family[
            family
        ]

        if not rows:
            continue

        best = rows[
            0
        ]

        best_family_candidates[
            family
        ] = best

        family_bundle = {}

        for count in BUNDLE_COUNTS:

            audit = vector_bundle_audit(
                best,
                count,
            )

            family_bundle[
                str(
                    count
                )
            ] = audit

            print(
                f"{family}_BUNDLE_N={count} "
                f"ALL_OUTWARD={'YES' if audit['all_axial_outward'] else 'NO'} "
                f"FLATNESS={audit['axial_flatness']:.12e} "
                f"TRANSVERSE={audit['maximum_transverse_fraction']:.12e} "
                f"ONAXIS_RELERR={audit['on_axis_relative_error']:.12e}"
            )

        bundle_audits[
            family
        ] = family_bundle

    # ------------------------------------------------------------
    # H. Direct spin audit.
    # ------------------------------------------------------------

    print(
        "\n=== H — FIXED-GEOMETRY SPIN ENERGY / SPEED AUDIT ===",
        flush=True,
    )

    if not scalar_rows:

        spin_rows = []

        print(
            "SPIN_AUDIT_NOT_RUN_NO_SCALAR_ORBIT_SURVIVOR"
        )

        best_unrestricted_spin = None
        best_kinetic_spin = None

    else:

        best_no_spin = scalar_rows[
            0
        ]

        spin_rows = spin_sweep(
            best_no_spin
        )

        unrestricted = [
            row
            for row in spin_rows
            if (
                row[
                    "mode"
                ]
                ==
                "UNRESTRICTED"
                and math.isfinite(
                    row[
                        "C"
                    ]
                )
            )
        ]

        kinetic = [
            row
            for row in spin_rows
            if (
                row[
                    "mode"
                ]
                ==
                "KINETIC_LIMITED"
                and math.isfinite(
                    row[
                        "C"
                    ]
                )
            )
        ]

        best_unrestricted_spin = (
            min(
                unrestricted,
                key=lambda row: row[
                    "C"
                ],
            )
            if unrestricted
            else None
        )

        best_kinetic_spin = (
            min(
                kinetic,
                key=lambda row: row[
                    "C"
                ],
            )
            if kinetic
            else None
        )

        if best_unrestricted_spin:

            print(
                f"SPIN_AUDIT_UNRESTRICTED_BEST_C="
                f"{best_unrestricted_spin['C']:.15e}"
            )

            print(
                f"SPIN_AUDIT_UNRESTRICTED_BEST_BETA_ORBIT="
                f"{best_unrestricted_spin['beta_orbit']:.15e}"
            )

            print(
                f"SPIN_AUDIT_UNRESTRICTED_BEST_SPIN_FRACTION="
                f"{best_unrestricted_spin['spin_fraction']:.15e}"
            )

            print(
                f"SPIN_AUDIT_UNRESTRICTED_BEST_BETA_SPIN="
                f"{best_unrestricted_spin['beta_spin']:.15e}"
            )

        if best_kinetic_spin:

            print(
                f"SPIN_AUDIT_KINETIC_BEST_C="
                f"{best_kinetic_spin['C']:.15e}"
            )

            print(
                f"SPIN_AUDIT_KINETIC_BEST_BETA_ORBIT="
                f"{best_kinetic_spin['beta_orbit']:.15e}"
            )

            print(
                f"SPIN_AUDIT_KINETIC_BEST_SPIN_FRACTION="
                f"{best_kinetic_spin['spin_fraction']:.15e}"
            )

            print(
                f"SPIN_AUDIT_KINETIC_BEST_BETA_SPIN="
                f"{best_kinetic_spin['beta_spin']:.15e}"
            )

    # ------------------------------------------------------------
    # I. Blind wildcard diagnostic.
    # ------------------------------------------------------------

    print(
        "\n=== I — BLIND WILDCARD MAJOR-RADIUS CHECK ==="
    )

    wildcard_results = []

    for value in BLIND_WILDCARD_VALUES:

        wildcard_results.append({
            "major_radius_over_h":
                value,

            "role":
                "BLIND_WILDCARD_NOT_PHYSICS_PRIOR",
        })

        print(
            f"WILDCARD_MAJOR_RADIUS_OVER_H="
            f"{value:.6f} "
            f"ROLE=BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
        )

    print(
        "WILDCARDS_USED_FOR_SELECTION=NO"
    )

    # ------------------------------------------------------------
    # J. Decision.
    # ------------------------------------------------------------

    print(
        "\n=== J — 024D1 DECISION ==="
    )

    constrained_no_spin_rows = refined_by_family[
        "ORBIT_KINETIC_LIMITED_NO_SPIN"
    ]

    constrained_spin_rows = refined_by_family[
        "ORBIT_PLUS_SPIN_KINETIC_LIMITED"
    ]

    best_constrained_no_spin = (
        constrained_no_spin_rows[
            0
        ]
        if constrained_no_spin_rows
        else None
    )

    best_constrained_spin = (
        constrained_spin_rows[
            0
        ]
        if constrained_spin_rows
        else None
    )

    constrained_no_spin_c = (
        best_constrained_no_spin[
            "C_refined"
        ]
        if best_constrained_no_spin
        else math.inf
    )

    constrained_spin_c = (
        best_constrained_spin[
            "C_refined"
        ]
        if best_constrained_spin
        else math.inf
    )

    scalar_best_c = (
        scalar_rows[
            0
        ][
            "C_refined"
        ]
        if scalar_rows
        else math.inf
    )

    orbital_topology_beats_024d = bool(
        min(
            pure_poloidal_c,
            best_helical_c,
        )
        <
        C024D_SCALAR
    )

    constrained_orbit_beats_006d = bool(
        constrained_no_spin_c
        <
        C006D
    )

    constrained_spin_beats_006d = bool(
        constrained_spin_c
        <
        C006D
    )

    if (
        math.isfinite(
            constrained_spin_c
        )
        and math.isfinite(
            constrained_no_spin_c
        )
    ):

        spin_improvement_factor = (
            constrained_no_spin_c
            /
            constrained_spin_c
        )

    else:

        spin_improvement_factor = 0.0

    genuine_spin_promotion = bool(
        best_constrained_spin
        is not None
        and best_constrained_spin[
            "spin_fraction"
        ]
        >=
        0.10
        and best_constrained_spin[
            "beta_spin"
        ]
        >=
        0.25
        and constrained_spin_beats_006d
        and spin_improvement_factor
        >=
        1.05
    )

    pure_toroidal_beats = bool(
        pure_toroidal_c
        <
        C006D
    )

    print(
        f"BEST_SCALAR_INTERNAL_ORBIT_C="
        f"{scalar_best_c:.15e}"
    )

    print(
        "INTERNAL_ORBIT_SCALAR_BEATS_024D_SCALAR="
        + (
            "YES"
            if orbital_topology_beats_024d
            else "NO"
        )
    )

    print(
        "PURE_TOROIDAL_CONTROL_BEATS_006D="
        + (
            "YES"
            if pure_toroidal_beats
            else "NO"
        )
    )

    print(
        "KINETIC_LIMITED_INTERNAL_ORBIT_BEATS_006D="
        + (
            "YES"
            if constrained_orbit_beats_006d
            else "NO"
        )
    )

    print(
        "KINETIC_LIMITED_ORBIT_PLUS_SPIN_BEATS_006D="
        + (
            "YES"
            if constrained_spin_beats_006d
            else "NO"
        )
    )

    print(
        f"SPIN_CONSTRAINED_IMPROVEMENT_FACTOR="
        f"{spin_improvement_factor:.15e}"
    )

    print(
        "GENUINE_SPIN_PROMOTION="
        + (
            "YES"
            if genuine_spin_promotion
            else "NO"
        )
    )

    if genuine_spin_promotion:

        decision = (
            "YELLOW_ORBIT_PLUS_SPIN_KINETIC_SURVIVOR_"
            "MICROSCOPIC_FIELD_PREFILTER_AUTHORIZED"
        )

        next_action = (
            "024D2_MINIMAL_FIELD_WITH_CONSERVED_ORBITAL_AND_"
            "INTRINSIC_ANGULAR_MOMENTUM_CURRENTS"
        )

        interpretation = (
            "ORBIT_AND_SPIN_BOTH_SURVIVE_COMPLETE_EFFECTIVE_LEDGER"
        )

    elif constrained_orbit_beats_006d:

        decision = (
            "YELLOW_INTERNAL_ORBIT_KINETIC_SURVIVOR_"
            "SPIN_NOT_REQUIRED"
        )

        next_action = (
            "024D2_MINIMAL_POLoidal_OR_HELICAL_FIELD_TRANSPORT_"
            "LAGRANGIAN_WITH_SCALAR_CONVERSION"
        )

        interpretation = (
            "ORBITAL_TOPOLOGY_HELPS_BUT_SPIN_DOES_NOT_EARN_PROMOTION"
        )

    elif orbital_topology_beats_024d:

        decision = (
            "YELLOW_INTERNAL_ORBIT_IMPROVES_RELAXED_SCALAR_HEADROOM_"
            "BUT_COLLISION_LIMIT_NOT_SURVIVED"
        )

        next_action = (
            "024D2_MINIMAL_CANONICAL_SCALAR_POLoidal_TRANSPORT_"
            "FIELD_PREFILTER_WITH_FULL_LOCAL_CONSERVATION"
        )

        interpretation = (
            "POLoidal_HELICAL_KERNEL_TRANSPORT_IS_USEFUL_"
            "SPIN_REMAINS_UNPROVEN"
        )

    elif scalar_best_c < C006D:

        decision = (
            "YELLOW_SCALAR_CONVERTER_SURVIVES_"
            "INTERNAL_ORBIT_TOPOLOGY_ADDS_NO_RECORD"
        )

        next_action = (
            "RETURN_TO_024D_MINIMAL_CANONICAL_SCALAR_"
            "INTERACTION_ZONE_FIELD_PREFILTER"
        )

        interpretation = (
            "STRESS_CONVERSION_REMAINS_DRIVER_"
            "ORBIT_COMPLEXITY_AND_SPIN_ARE_OVERHEAD"
        )

    else:

        decision = (
            "RED_INTERNAL_TOROIDAL_ORBIT_AND_SPIN_"
            "NO_USEFUL_SOURCE_ADVANCE"
        )

        next_action = (
            "CLOSE_ORBIT_SPIN_BRANCH_AND_RETURN_TO_"
            "MINIMAL_SCALAR_CONVERTER_OR_ANALOGUE_ANTIGRAVITY"
        )

        interpretation = (
            "NO_NEW_ORBITAL_OR_SPIN_LEVERAGE"
        )

    print(
        f"ORBIT_SPIN_INTERPRETATION="
        f"{interpretation}"
    )

    print(
        f"024D1_DECISION="
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
        "70_TO_71_PERCENT_RETAIN_UNLESS_MICROSCOPIC_PROMOTION_IS_EARNED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    # ------------------------------------------------------------
    # K. Persist.
    # ------------------------------------------------------------

    clean_rows = [
        clean_refined(
            row
        )
        for row in refined_all
    ]

    if clean_rows:

        fields = sorted(
            {
                key
                for row in clean_rows
                for key, value in row.items()
                if not isinstance(
                    value,
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
                clean_rows
            )

    with OUT_WINDING.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "family",
                "p",
                "q",
                "best_refined_C",
                "beats_006D",
                "beats_024D_scalar",
            ],
        )

        writer.writeheader()

        writer.writerows(
            refined_winding_summary
        )

    if spin_rows:

        with OUT_SPIN.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "mode",
                    "beta_orbit",
                    "spin_fraction",
                    "beta_spin",
                    "f",
                    "A",
                    "C",
                ],
            )

            writer.writeheader()

            writer.writerows(
                spin_rows
            )

    profile_payload = {}

    for family, best in best_family_candidates.items():

        orbit = best[
            "orbit"
        ]

        prefix = family.lower()

        for key in (
            "u",
            "x",
            "y",
            "z",
            "weights",
            "kernel",
            "top_mask",
        ):

            value = np.asarray(
                orbit[
                    key
                ]
            )

            if key == "top_mask":
                value = value.astype(
                    np.int8
                )

            profile_payload[
                f"{prefix}_{key}"
            ] = value

        profile_payload[
            f"{prefix}_bottom_mask"
        ] = np.asarray(
            best[
                "bottom_mask"
            ],
            dtype=np.int8,
        )

    if profile_payload:

        np.savez_compressed(
            OUT_NPZ,
            **profile_payload,
        )

    best_refined_json = {
        family: (
            clean_refined(
                rows[
                    0
                ]
            )
            if rows
            else None
        )
        for family, rows in refined_by_family.items()
    }

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_INTERNAL_TOROIDAL_ORBIT_"
                "AND_SPIN_STRESS_CONVERSION_CAMPAIGN"
            ),

        "anchors": {
            "C_006D":
                C006D,

            "C_024D_scalar":
                C024D_SCALAR,

            "payload_radius_over_h":
                PAYLOAD_RADIUS_OVER_H,
        },

        "scan": {
            "sobol_cases":
                N_CASES,

            "families":
                list(
                    FAMILIES
                ),

            "family_evaluations":
                N_CASES
                * len(
                    FAMILIES
                ),

            "windings":
                [
                    list(
                        winding
                    )
                    for winding in WINDINGS
                ],

            "coarse_phase_points":
                COARSE_NPHASE,

            "refine_phase_points":
                REFINE_NPHASE,
        },

        "analytic_controls": {
            "pure_counterorbit":
                "RED",

            "pure_linear_EM_orbit":
                "RED",

            "spin_free_negative_stress":
                False,

            "Fenchel_total_curvature_bound":
                "K_total >= 2*pi",
        },

        "coarse_family_summary":
            coarse_family_summary,

        "best_refined":
            best_refined_json,

        "refined_winding_summary":
            refined_winding_summary,

        "bundle_audits":
            bundle_audits,

        "orbit_type_comparison": {
            "pure_toroidal_C":
                pure_toroidal_c,

            "pure_poloidal_C":
                pure_poloidal_c,

            "best_helical_C":
                best_helical_c,

            "best_helical_winding":
                (
                    [
                        helical_best[
                            "p"
                        ],
                        helical_best[
                            "q_winding"
                        ],
                    ]
                    if helical_best
                    else None
                ),
        },

        "spin_audit": {
            "best_unrestricted":
                best_unrestricted_spin,

            "best_kinetic_limited":
                best_kinetic_spin,

            "constrained_improvement_factor":
                spin_improvement_factor,

            "genuine_spin_promotion":
                genuine_spin_promotion,
        },

        "decision": {
            "internal_orbit_scalar_beats_024D_scalar":
                orbital_topology_beats_024d,

            "kinetic_limited_internal_orbit_beats_006D":
                constrained_orbit_beats_006d,

            "kinetic_limited_orbit_plus_spin_beats_006D":
                constrained_spin_beats_006d,

            "genuine_spin_promotion":
                genuine_spin_promotion,

            "interpretation":
                interpretation,

            "024D1":
                decision,

            "next":
                next_action,

            "practical_antigravity_device":
                False,
        },

        "claim_limits": [
            "NO_MICROSCOPIC_TORUS_KNOT_FIELD",
            "NO_FULL_DYNAMIC_STABILITY",
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

    print(
        f"WINDING_CSV="
        f"{OUT_WINDING.relative_to(ROOT)}"
    )

    if OUT_SPIN.is_file():

        print(
            f"SPIN_SWEEP_CSV="
            f"{OUT_SPIN.relative_to(ROOT)}"
        )

    if OUT_NPZ.is_file():

        print(
            f"BEST_PROFILES_NPZ="
            f"{OUT_NPZ.relative_to(ROOT)}"
        )

    print(
        "024D1_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
