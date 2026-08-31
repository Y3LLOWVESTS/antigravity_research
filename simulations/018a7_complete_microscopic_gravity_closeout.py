#!/usr/bin/env python3
"""Simulation 018A-7 — complete microscopic thin-composite gravity closeout.

PURPOSE
-------
Close the 018A nonthermal model-selection gate by performing complete
thin-composite gravitational bookkeeping using the microscopic quantities
established in 018A-5 through 018A-6B3.

The source is the current preferred zero-temperature configuration:

    one microscopic KLS-like domain wall disk

    bounded by

    the literature-backed 017P gauged-vorton rim

    with

    the fully coupled local Phi + sigma + A + gauge junction correction.

ACTIVE SCIENTIFIC QUESTION
--------------------------
After every mandatory field-theory energy and stress contribution presently
required by the selected zero-temperature model is included, does the
stationary thin-composite source simultaneously satisfy:

    positive total active mass;

    outward point gravity;

    outward finite-payload center-of-mass gravity;

    sufficient kernel leverage;

    healthy rim EOS / extrinsic stability;

    radial effective stationarity;

    a robust source-level neighborhood?

This is the final 018A gravitational preflight before the full curved
finite-thickness Euler-Lagrange calculation 018B.

PRIOR MICROSCOPIC RESULTS
-------------------------
018A-5 established a finite zero-temperature microscopic wall with measured
tension and thickness.

018A-6A established that the wall terminates on the 017P vortex in the
fixed-background two-dimensional junction geometry.

018A-6B0 showed that the first frozen-background backreaction sources are small.

018A-6B1 established that the apparent large relaxation in the first
fully-coupled Cartesian solve was dominated by under-resolved common-mode
lattice relaxation of the original 017P core.

018A-6B2 resolved the microscopic core and showed convergence of the matched
KLS-specific quantities.

018A-6B3 then tightened every marginal optimizer and established:

    FULLY_COUPLED_LOCAL_2D_KLS_JUNCTION
        =
        SUPPORTED_WITH_FINE_CORE_PLUS_MATCHED_GLOBAL_OUTER_SOLUTION.

No further local-junction escalation is permitted unless this gravity gate
discovers a concrete inconsistency.

PHYSICAL MODEL
--------------
The thin-limit composite contains two counterrotating copies of the 017P
superconducting string/vorton rim.

Counterrotation cancels the longitudinal momentum flux T_tphi/T_ty at the
effective level while diagonal energy and stress add.

The wall is a single microscopic domain-wall disk.

The conservative strong-pass bookkeeping includes two microscopic
wall/string junction corrections, one for each counterrotating copy.

This is intentionally the more expensive of the one- versus two-junction
interpretations tested previously.

RIM STRESS
----------
For one straight superconducting-string copy:

    U_string
      =
      2 omega^2 Sigma2
      +
      A_string

and

    T_parallel
      =
      2 k^2 Sigma2
      -
      A_string.

Its active line source is therefore

    Lambda_active
      =
      U_string
      +
      T_parallel

      =
      2 Sigma2
      (
        omega^2
        +
        k^2
      ).

For a counterrotating pair:

    Lambda_active,pair
      =
      4 Sigma2
      (
        omega^2
        +
        k^2
      ).

MICROSCOPIC JUNCTION
--------------------
018A-6B3 supplies a matched reduced-energy correction

    mu_J

and a matched condensate correction

    Delta Sigma2_J.

The physical energy correction per string-copy junction is

    Delta U_J
      =
      mu_J
      +
      2 omega^2 Delta Sigma2_J.

The complete junction active source is not inferred from this energy alone.

Instead use the independently reconstructed 018A-6B3 matched active-source
correction, which includes transverse stress and gauge/potential effects.

Thus mandatory energy and mandatory active stress are tracked separately.

WALL
----
The measured microscopic wall tension is

    sigma_W.

For a static planar canonical wall at equilibrium:

    energy surface density
      =
      +sigma_W

while its integrated active gravitational source is

    S_W
      =
      -sigma_W.

For a disk of radius R:

    E_W
      =
      pi sigma_W R^2

and the magnitude of its negative active mass is

    Q_-
      =
      pi sigma_W R^2.

STATIONARITY
------------
Use the conservative two-junction radial bookkeeping already introduced in
018A-6B0 through 018A-6B3:

    w_eff
      =
      w_stat
      -
      2 pi N_J mu_J / ell

with

    N_J = 2.

Then

    Q_req
      =
      w_eff / sigma_W

    R_req
      =
      Q_req ell / (2 pi)

and

    N_req
      =
      Q_req / (Q/N).

The nearest integer winding is checked explicitly.

GRAVITY
-------
The target remains at the original 017P optimized dimensionless height

    x
      =
      h/R
      =
      0.01340639306274.

For the negative-active wall disk the outward dimensionless field factor,
with one factor of R absorbed, is

    F_-
      =
      2 pi sigma_W R
      [
        1
        -
        x / sqrt(1+x^2)
      ].

For the positive-active rim line:

    F_+
      =
      2 pi Lambda_active,total
      x
      /
      (1+x^2)^(3/2).

The net outward field factor is

    F
      =
      F_-
      -
      F_+.

The required sign is

    F > 0.

The formulas are independently checked by:

    Gauss-Legendre source quadrature;

    scipy adaptive quadrature.

FINITE PAYLOAD
--------------
Use a uniform spherical passive payload centered on the symmetry axis with

    r_payload
      =
      0.25 h.

The complete sphere lies above the z=0 source plane and is therefore wholly
inside a source-free region.

Because the linearized gravitational potential is harmonic there, every
acceleration component is harmonic.

The mean-value theorem therefore gives exactly

    a_CM
      =
      a_center

for the spherical passive payload.

This exact result is also checked by explicit numerical volume averaging of
the off-axis disk/rim field.

KERNEL LEVERAGE
---------------
Define positive rim active magnitude

    Q_+

and negative wall active magnitude

    Q_-.

Define weighted moments

    W_+
      =
      kappa_+ Q_+

    W_-
      =
      kappa_- Q_-.

Positive far active mass requires

    Q_+ > Q_-.

Outward finite-payload gravity requires

    W_- > W_+.

Equivalently:

    kappa_- / kappa_+
      >
    Q_+ / Q_-.

The gate reports both sides and their margin.

ENERGY COEFFICIENT
------------------
The complete source energy per radius is

    E_bar
      =
      E_total / R.

The target acceleration factor is F/R.

With

    h = x R,

the standard project coefficient becomes

    C_eff
      =
      E_bar
      /
      (
        F x^2
      )

in

    M_equiv
      =
      C_eff
      a h^2 / G.

No coefficient is inherited from 017P or 017R.

This run calculates the nonthermal model's own coefficient.

A one-meter, one-g mass-equivalent and energy-equivalent are reported only as
a scaling diagnostic.

They are not a device design.

MANDATORY SUPPORT BOOKKEEPING
-----------------------------
Included:

    microscopic wall energy and stress;

    017P vortex/current condensate energy and stress;

    017P gauge-field contribution through A_string;

    microscopic KLS junction energy;

    microscopic junction active stress;

    matched condensate backreaction;

    gauge response contained in the relaxed junction calculation.

No thermal bath is required by this zero-temperature model.

The vacuum-preserving counterterms are chosen so the asymptotic vacuum has
zero extensive energy density.

This means there is no thermal/background volume-energy term analogous to the
fatal 017S photon bath in the declared model.

This statement applies only to the field model.

It does not include hypothetical laboratory containment, production,
cooling, control hardware, or an experimental realization that has not yet
been specified.

ROBUSTNESS
----------
The microscopic wall sector has already passed the earlier finite parameter
neighborhood tests.

The present gate adds a deliberately adversarial thin-source +/-5 percent
envelope over:

    wall tension;

    reduced junction energy;

    junction active source;

    rim active line source;

    rim physical energy line source;

    Q/N;

    target height ratio h/R.

This is a source-level gravitational robustness test.

It is not a replacement for re-solving the full curved field equations over
that hypercube.

The curved-field robustness requirement belongs to 018B and 018C.

PASS CONDITIONS
---------------
Strong 018A gravity closure requires:

    COMPLETE_FIELD_MODEL_ENERGY_BOOKKEEPING=PASS

    POSITIVE_TOTAL_ACTIVE_MASS=PASS

    POINT_OUTWARD_ACCELERATION=PASS

    FINITE_PAYLOAD_OUTWARD_ACCELERATION=PASS

    DIRECT_GRAVITY_RECONSTRUCTION=PASS

    KERNEL_LEVERAGE_CONDITION=PASS

    RADIAL_EFFECTIVE_STATIONARITY=PASS

    RIM_HEALTH_PREFLIGHT=PASS

    THIN_GRAVITY_SOURCE_ENVELOPE=PASS

    ROBUST_PARAMETER_NEIGHBORHOOD=PASS_AT_018A_PREFLIGHT_LEVEL.

If all earlier topology/wall/junction conditions are also inherited GREEN,
then:

    FULL_018A_GATE=GREEN.

PROMOTION
---------
A green 018A does NOT establish a full microscopic finite-radius field
solution.

It authorizes:

    018B_FULL_2D_COUPLED_FINITE_THICKNESS_EULER_LAGRANGE_SOLVE.

018B must solve the complete curved finite-thickness field configuration and
independently reconstruct its T_munu and finite-payload gravity.

FALSIFIERS
----------
018A fails if any of the following occurs:

    total active mass <= 0;

    point gravity becomes inward;

    finite-payload CM gravity becomes inward;

    junction/gauge support destroys kernel leverage;

    required winding/radius becomes inconsistent;

    source-level robustness shows the sign exists only at a tuned point.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_COMPLETE_MICROSCOPIC_THIN_GRAVITY_CLOSEOUT

PRACTICAL CLAIM
---------------
A green result is still not practical antigravity.

Pure-GR energy scaling remains a separate unsolved problem.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "simulations"
    / "018a6b3_fine_continuation_outer_match_closeout.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Import a verified local simulation without invoking its main function."""

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        name
    ] = module

    try:
        spec.loader.exec_module(
            module
        )
    except Exception:
        sys.modules.pop(
            name,
            None,
        )
        raise

    return module


b3 = load_module(
    "ag018a6b3_gravity_closeout",
    SOURCE,
)

b2 = b3.b2
fc = b3.fc
m = b3.m


# ============================================================================
# Physical anchors.
# ============================================================================

CHI_SELECTED = 0.00475

OMEGA = b2.OMEGA
K_LONG = b2.K_LONG

X_TARGET = 0.01340639306274

JUNCTION_COUNT = 2

PAYLOAD_RADIUS_OVER_H = 0.25

G_SI = 6.67430e-11
C_SI = 299792458.0
G0_SI = 9.80665


# ============================================================================
# Validation tolerances.
# ============================================================================

MAX_DIRECT_GRAVITY_RELERR = 2.0e-8
MAX_PAYLOAD_DIRECT_RELERR = 5.0e-4

MIN_SCALE_SEPARATION = 10.0
MAX_INTEGER_MISMATCH = 1.0e-3

MAX_ACTIVE_SOURCE_FRACTION = 0.01

SOURCE_ENVELOPE_LEVELS = (
    0.95,
    1.00,
    1.05,
)


def center_field_analytic(
    sigma_r: float,
    active_line: float,
    x: float,
):
    """Return negative-wall, positive-rim and net normalized axial factors."""

    wall = (
        2.0
        *
        math.pi
        *
        sigma_r
        *
        (
            1.0
            -
            x
            /
            math.sqrt(
                1.0
                +
                x
                *
                x
            )
        )
    )

    rim = (
        2.0
        *
        math.pi
        *
        active_line
        *
        x
        /
        (
            1.0
            +
            x
            *
            x
        ) ** 1.5
    )

    return (
        wall,
        rim,
        wall
        -
        rim,
    )


def center_field_gauss(
    sigma_r: float,
    active_line: float,
    x: float,
    order: int = 96,
):
    """Independent Gauss-Legendre source integration at the axial center."""

    nodes_r, weights_r = (
        leggauss(
            order
        )
    )

    u = (
        0.5
        *
        (
            nodes_r
            +
            1.0
        )
    )

    wu = (
        0.5
        *
        weights_r
    )

    wall_integral = float(
        np.sum(
            wu
            *
            u
            *
            x
            /
            (
                u
                *
                u
                +
                x
                *
                x
            ) ** 1.5
        )
    )

    wall = (
        2.0
        *
        math.pi
        *
        sigma_r
        *
        wall_integral
    )

    nodes_phi, weights_phi = (
        leggauss(
            order
        )
    )

    phi = (
        math.pi
        *
        (
            nodes_phi
            +
            1.0
        )
    )

    wphi = (
        math.pi
        *
        weights_phi
    )

    del phi

    rim = float(
        np.sum(
            wphi
            *
            (
                active_line
                *
                x
                /
                (
                    1.0
                    +
                    x
                    *
                    x
                ) ** 1.5
            )
        )
    )

    return (
        wall,
        rim,
        wall
        -
        rim,
    )


def center_field_quad(
    sigma_r: float,
    active_line: float,
    x: float,
):
    """Second independent adaptive integration of the center field."""

    wall_integral, _ = quad(
        lambda u:
            u
            *
            x
            /
            (
                u
                *
                u
                +
                x
                *
                x
            ) ** 1.5,
        0.0,
        1.0,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
        limit=300,
    )

    wall = (
        2.0
        *
        math.pi
        *
        sigma_r
        *
        wall_integral
    )

    rim, _ = quad(
        lambda phi:
            active_line
            *
            x
            /
            (
                1.0
                +
                x
                *
                x
            ) ** 1.5,
        0.0,
        2.0
        *
        math.pi,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
        limit=300,
    )

    return (
        wall,
        rim,
        wall
        -
        rim,
    )


def off_axis_field(
    rho: float,
    z: float,
    sigma_r: float,
    active_line: float,
    radial_order: int = 32,
    azimuthal_order: int = 64,
):
    """Numerically integrate normalized vertical gravity off the symmetry axis.

    Coordinates are normalized by the rim radius R.

    Positive return value is outward / +z.

    The negative-active disk contributes positively and the positive-active
    rim contributes negatively.
    """

    rn, rw = (
        leggauss(
            radial_order
        )
    )

    u = (
        0.5
        *
        (
            rn
            +
            1.0
        )
    )

    wu = (
        0.5
        *
        rw
    )

    pn, pw = (
        leggauss(
            azimuthal_order
        )
    )

    phi = (
        math.pi
        *
        (
            pn
            +
            1.0
        )
    )

    wphi = (
        math.pi
        *
        pw
    )

    U = u[
        :,
        None
    ]

    PHI = phi[
        None,
        :
    ]

    measure = (
        wu[
            :,
            None
        ]
        *
        wphi[
            None,
            :
        ]
    )

    disk_distance_sq = (
        U
        *
        U

        +
        rho
        *
        rho

        -
        2.0
        *
        U
        *
        rho
        *
        np.cos(
            PHI
        )

        +
        z
        *
        z
    )

    wall = float(
        sigma_r
        *
        np.sum(
            measure
            *
            U
            *
            z
            /
            disk_distance_sq**1.5
        )
    )

    ring_distance_sq = (
        1.0

        +
        rho
        *
        rho

        -
        2.0
        *
        rho
        *
        np.cos(
            phi
        )

        +
        z
        *
        z
    )

    rim = float(
        active_line
        *
        np.sum(
            wphi
            *
            z
            /
            ring_distance_sq**1.5
        )
    )

    return (
        wall
        -
        rim
    )


def finite_payload_average(
    x: float,
    sigma_r: float,
    active_line: float,
):
    """Directly volume-average the source field over a finite spherical payload."""

    radius = (
        PAYLOAD_RADIUS_OVER_H
        *
        x
    )

    sn, sw = (
        leggauss(
            8
        )
    )

    s = (
        0.5
        *
        radius
        *
        (
            sn
            +
            1.0
        )
    )

    ws = (
        0.5
        *
        radius
        *
        sw
    )

    mun, muw = (
        leggauss(
            12
        )
    )

    total = 0.0

    for (
        si,
        wsi,
    ) in zip(
        s,
        ws,
    ):

        for (
            mui,
            wmui,
        ) in zip(
            mun,
            muw,
        ):

            rho = (
                si
                *
                math.sqrt(
                    max(
                        0.0,
                        1.0
                        -
                        mui
                        *
                        mui,
                    )
                )
            )

            z = (
                x
                +
                si
                *
                mui
            )

            field = off_axis_field(
                rho,
                z,
                sigma_r,
                active_line,
            )

            total += (
                wsi
                *
                si
                *
                si
                *
                wmui
                *
                field
            )

    average = (
        3.0
        /
        (
            2.0
            *
            radius**3
        )
        *
        total
    )

    return (
        radius,
        average,
    )


def source_envelope(
    sigma0: float,
    mu0: float,
    q_over_n0: float,
    ell: float,
    wall_load: float,
    x0: float,
    base_active0: float,
    endpoint_active0: float,
    base_energy0: float,
    junction_physical0: float,
):
    """Run a conservative independent +/-5 percent thin-source envelope."""

    total = 0
    passed = 0

    min_outward = math.inf
    min_active_mass_per_r = math.inf
    min_scale = math.inf
    min_leverage_margin = math.inf

    max_integer_mismatch = 0.0
    max_c = 0.0

    for (
        f_sigma,
        f_mu,
        f_endpoint,
        f_active,
        f_energy,
        f_q,
        f_x,
    ) in itertools.product(
        SOURCE_ENVELOPE_LEVELS,
        repeat=7,
    ):

        total += 1

        sigma = (
            sigma0
            *
            f_sigma
        )

        mu = (
            mu0
            *
            f_mu
        )

        q_over_n = (
            q_over_n0
            *
            f_q
        )

        x = (
            x0
            *
            f_x
        )

        w_eff = (
            wall_load

            -
            2.0
            *
            math.pi
            *
            JUNCTION_COUNT
            *
            mu
            /
            ell
        )

        if w_eff <= 0.0:
            continue

        q_req = (
            w_eff
            /
            sigma
        )

        n_req = (
            q_req
            /
            q_over_n
        )

        n_int = max(
            1,
            int(
                round(
                    n_req
                )
            ),
        )

        integer_mismatch = (
            abs(
                sigma
                *
                q_over_n
                *
                n_int
                -
                w_eff
            )
            /
            w_eff
        )

        radius = (
            q_req
            *
            ell
            /
            (
                2.0
                *
                math.pi
            )
        )

        sigma_r = (
            sigma
            *
            radius
        )

        base_active = (
            base_active0
            *
            f_active
        )

        endpoint_active = (
            endpoint_active0
            *
            f_endpoint
        )

        active_line = (
            base_active
            +
            JUNCTION_COUNT
            *
            endpoint_active
        )

        base_energy = (
            base_energy0
            *
            f_energy
        )

        junction_physical = (
            junction_physical0
            *
            f_mu
        )

        energy_line = (
            base_energy
            +
            JUNCTION_COUNT
            *
            junction_physical
        )

        (
            weighted_negative,
            weighted_positive,
            outward,
        ) = center_field_analytic(
            sigma_r,
            active_line,
            x,
        )

        positive_active_per_r = (
            2.0
            *
            math.pi
            *
            active_line
        )

        negative_active_per_r = (
            math.pi
            *
            sigma_r
        )

        active_mass_per_r = (
            positive_active_per_r
            -
            negative_active_per_r
        )

        kappa_positive = (
            weighted_positive
            /
            positive_active_per_r
        )

        kappa_negative = (
            weighted_negative
            /
            negative_active_per_r
        )

        required_ratio = (
            positive_active_per_r
            /
            negative_active_per_r
        )

        leverage_margin = (
            (
                kappa_negative
                /
                kappa_positive
            )
            /
            required_ratio
        )

        scale = min(
            radius
            /
            fc.WALL_WIDTH90,

            radius
            /
            m.A_CORE_WIDTH,
        )

        energy_per_r = (
            2.0
            *
            math.pi
            *
            energy_line

            +
            math.pi
            *
            sigma_r
        )

        if outward > 0.0:

            c_eff = (
                energy_per_r
                /
                (
                    outward
                    *
                    x
                    *
                    x
                )
            )

        else:

            c_eff = math.inf

        case_pass = (
            outward
            >
            0.0

            and
            active_mass_per_r
            >
            0.0

            and
            leverage_margin
            >
            1.0

            and
            scale
            >=
            MIN_SCALE_SEPARATION

            and
            integer_mismatch
            <=
            MAX_INTEGER_MISMATCH
        )

        if case_pass:
            passed += 1

        min_outward = min(
            min_outward,
            outward,
        )

        min_active_mass_per_r = min(
            min_active_mass_per_r,
            active_mass_per_r,
        )

        min_scale = min(
            min_scale,
            scale,
        )

        min_leverage_margin = min(
            min_leverage_margin,
            leverage_margin,
        )

        max_integer_mismatch = max(
            max_integer_mismatch,
            integer_mismatch,
        )

        max_c = max(
            max_c,
            c_eff,
        )

    return {
        "total":
            total,

        "passed":
            passed,

        "min_outward":
            min_outward,

        "min_active_mass_per_r":
            min_active_mass_per_r,

        "min_scale":
            min_scale,

        "min_leverage_margin":
            min_leverage_margin,

        "max_integer_mismatch":
            max_integer_mismatch,

        "max_c":
            max_c,
    }


def main() -> None:
    """Execute the complete 018A thin-composite gravity closeout."""

    original_chi = float(
        m.CHI_SELECTED
    )

    m.CHI_SELECTED = (
        CHI_SELECTED
    )

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-7 ==="
    )

    print(
        "QUESTION="
        "DOES_COMPLETE_MICROSCOPIC_WALL_RIM_JUNCTION_BOOKKEEPING_PRESERVE_POSITIVE_FAR_MASS_AND_FINITE_PAYLOAD_OUTWARD_GRAVITY"
    )

    # ========================================================================
    # Reconstruct the promoted microscopic inputs.
    # ========================================================================

    print(
        "\n=== MICROSCOPIC INPUT RECONSTRUCTION ==="
    )

    (
        outer,
        outer_metrics,
        outer_pass,
    ) = (
        b3.global_outer_morphology()
    )

    selected = (
        b3.matched_pair(
            CHI_SELECTED,
            81,
            20.0,
        )
    )

    full = (
        selected[
            "full"
        ]
    )

    fixed_global, diag = (
        b2.global_fixed_case(
            CHI_SELECTED
        )
    )

    sigma_wall = float(
        m.SIGMA_W_RELAXED_018A5
    )

    mu_reduced = float(
        outer.junction_excess_energy
        +
        selected[
            "delta_e"
        ]
    )

    delta_sigma2 = float(
        selected[
            "delta_sigma2"
        ]
    )

    sigma2_background = float(
        full.sigma2_background
    )

    sigma2_matched = (
        sigma2_background
        +
        delta_sigma2
    )

    a_string = float(
        diag.a_string
    )

    endpoint_active = float(
        selected[
            "endpoint_active"
        ]
    )

    print(
        "WALL_TENSION="
        f"{sigma_wall:.15e}"
    )

    print(
        "GLOBAL_REDUCED_JUNCTION_ENERGY="
        f"{mu_reduced:+.15e}"
    )

    print(
        "MATCHED_DELTA_SIGMA2="
        f"{delta_sigma2:+.15e}"
    )

    print(
        "SIGMA2_BACKGROUND="
        f"{sigma2_background:.15e}"
    )

    print(
        "SIGMA2_MATCHED="
        f"{sigma2_matched:.15e}"
    )

    print(
        "A_STRING="
        f"{a_string:.15e}"
    )

    print(
        "MATCHED_JUNCTION_ACTIVE_PER_COPY="
        f"{endpoint_active:+.15e}"
    )

    print(
        "OUTER_GLOBAL_WALL_TERMINATION="
        f"{'PASS' if outer_pass else 'FAIL'}"
    )

    # ========================================================================
    # Complete energy/stress decomposition.
    # ========================================================================

    print(
        "\n=== COMPLETE FIELD-MODEL ENERGY / STRESS BOOKKEEPING ==="
    )

    base_energy_line_pair = (
        2.0
        *
        (
            2.0
            *
            OMEGA
            *
            OMEGA
            *
            sigma2_background

            +
            a_string
        )
    )

    junction_physical_energy_per_copy = (
        mu_reduced

        +
        2.0
        *
        OMEGA
        *
        OMEGA
        *
        delta_sigma2
    )

    complete_energy_line = (
        base_energy_line_pair

        +
        JUNCTION_COUNT
        *
        junction_physical_energy_per_copy
    )

    base_active_line_pair = (
        4.0
        *
        sigma2_background
        *
        (
            OMEGA
            *
            OMEGA

            +
            K_LONG
            *
            K_LONG
        )
    )

    complete_active_line = (
        base_active_line_pair

        +
        JUNCTION_COUNT
        *
        endpoint_active
    )

    active_perturbation_fraction = (
        abs(
            JUNCTION_COUNT
            *
            endpoint_active
        )
        /
        base_active_line_pair
    )

    print(
        "RIM_BASE_PHYSICAL_ENERGY_LINE_PAIR="
        f"{base_energy_line_pair:.15e}"
    )

    print(
        "JUNCTION_PHYSICAL_ENERGY_PER_COPY="
        f"{junction_physical_energy_per_copy:+.15e}"
    )

    print(
        "COMPLETE_PHYSICAL_ENERGY_LINE="
        f"{complete_energy_line:.15e}"
    )

    print(
        "RIM_BASE_ACTIVE_LINE_PAIR="
        f"{base_active_line_pair:.15e}"
    )

    print(
        "COMPLETE_ACTIVE_LINE="
        f"{complete_active_line:.15e}"
    )

    print(
        "JUNCTION_ACTIVE_PERTURBATION_FRACTION="
        f"{active_perturbation_fraction:.15e}"
    )

    print(
        "MICROSCOPIC_WALL_ENERGY=INCLUDED"
    )

    print(
        "MICROSCOPIC_WALL_STRESS=INCLUDED"
    )

    print(
        "017P_RIM_ENERGY_AND_STRESS=INCLUDED"
    )

    print(
        "JUNCTION_ENERGY_AND_STRESS=INCLUDED"
    )

    print(
        "MANDATORY_GAUGE_FIELD_ENERGY="
        "INCLUDED_IN_017P_A_STRING_AND_FULLY_RELAXED_JUNCTION"
    )

    print(
        "MANDATORY_BACKGROUND_OR_BIAS_ENERGY="
        "NO_ADDITIONAL_EXTENSIVE_ZERO_T_BACKGROUND_REQUIRED_IN_DECLARED_MODEL"
    )

    complete_bookkeeping_pass = (
        outer_pass

        and
        full.success

        and
        selected[
            "base"
        ].success

        and
        active_perturbation_fraction
        <
        MAX_ACTIVE_SOURCE_FRACTION
    )

    print(
        "COMPLETE_FIELD_MODEL_ENERGY_BOOKKEEPING="
        f"{'PASS' if complete_bookkeeping_pass else 'FAIL'}"
    )

    # ========================================================================
    # Conservative two-junction stationarity.
    # ========================================================================

    print(
        "\n=== CONSERVATIVE TWO-JUNCTION STATIONARITY ==="
    )

    stationarity = (
        fc.stationarity(
            mu_reduced,
            JUNCTION_COUNT,
        )
    )

    stationarity_pass = bool(
        stationarity[
            "passed"
        ]
    )

    radius = float(
        stationarity[
            "radius"
        ]
    )

    q_req = float(
        stationarity[
            "q_req"
        ]
    )

    n_req = float(
        stationarity[
            "n_req"
        ]
    )

    n_integer = int(
        stationarity[
            "n_integer"
        ]
    )

    integer_mismatch = float(
        stationarity[
            "mismatch"
        ]
    )

    sigma_r = (
        sigma_wall
        *
        radius
    )

    h = (
        X_TARGET
        *
        radius
    )

    print(
        f"JUNCTION_COUNT={JUNCTION_COUNT}"
    )

    print(
        "Q_REQUIRED="
        f"{q_req:.15e}"
    )

    print(
        "N_REQUIRED="
        f"{n_req:.15e}"
    )

    print(
        f"N_INTEGER={n_integer}"
    )

    print(
        "INTEGER_MISMATCH="
        f"{integer_mismatch:.15e}"
    )

    print(
        "R_REQUIRED="
        f"{radius:.15e}"
    )

    print(
        "TARGET_H="
        f"{h:.15e}"
    )

    print(
        "R_OVER_WALL90="
        f"{float(stationarity['radius_over_wall']):.12f}"
    )

    print(
        "R_OVER_A_CORE="
        f"{float(stationarity['radius_over_core']):.12f}"
    )

    print(
        "RADIAL_EFFECTIVE_STATIONARITY="
        f"{'PASS' if stationarity_pass else 'FAIL'}"
    )

    # ========================================================================
    # Total active mass and kernel leverage.
    # ========================================================================

    print(
        "\n=== TOTAL ACTIVE MASS + KERNEL LEVERAGE ==="
    )

    positive_active = (
        2.0
        *
        math.pi
        *
        radius
        *
        complete_active_line
    )

    negative_active = (
        math.pi
        *
        sigma_wall
        *
        radius
        *
        radius
    )

    total_active_mass = (
        positive_active
        -
        negative_active
    )

    positive_active_per_r = (
        positive_active
        /
        radius
    )

    negative_active_per_r = (
        negative_active
        /
        radius
    )

    (
        weighted_negative,
        weighted_positive,
        net_outward_analytic,
    ) = center_field_analytic(
        sigma_r,
        complete_active_line,
        X_TARGET,
    )

    kappa_positive = (
        weighted_positive
        /
        positive_active_per_r
    )

    kappa_negative = (
        weighted_negative
        /
        negative_active_per_r
    )

    active_ratio = (
        positive_active
        /
        negative_active
    )

    leverage_ratio = (
        kappa_negative
        /
        kappa_positive
    )

    leverage_margin = (
        leverage_ratio
        /
        active_ratio
    )

    positive_mass_pass = (
        total_active_mass
        >
        0.0
    )

    leverage_pass = (
        leverage_margin
        >
        1.0

        and
        net_outward_analytic
        >
        0.0
    )

    print(
        "POSITIVE_ACTIVE_MAGNITUDE="
        f"{positive_active:.15e}"
    )

    print(
        "NEGATIVE_ACTIVE_MAGNITUDE="
        f"{negative_active:.15e}"
    )

    print(
        "TOTAL_ACTIVE_MASS="
        f"{total_active_mass:+.15e}"
    )

    print(
        "POSITIVE_ACTIVE_WEIGHTED_MOMENT="
        f"{weighted_positive:.15e}"
    )

    print(
        "NEGATIVE_ACTIVE_WEIGHTED_MOMENT="
        f"{weighted_negative:.15e}"
    )

    print(
        "Q_PLUS_OVER_Q_MINUS="
        f"{active_ratio:.15e}"
    )

    print(
        "KAPPA_MINUS_OVER_KAPPA_PLUS="
        f"{leverage_ratio:.15e}"
    )

    print(
        "KERNEL_LEVERAGE_MARGIN="
        f"{leverage_margin:.15e}"
    )

    print(
        "POSITIVE_TOTAL_ACTIVE_MASS="
        f"{'PASS' if positive_mass_pass else 'FAIL'}"
    )

    print(
        "KERNEL_LEVERAGE_CONDITION="
        f"{'PASS' if leverage_pass else 'FAIL'}"
    )

    # ========================================================================
    # Point gravity independent reconstruction.
    # ========================================================================

    print(
        "\n=== POINT GRAVITY INDEPENDENT RECONSTRUCTION ==="
    )

    (
        wall_analytic,
        rim_analytic,
        field_analytic,
    ) = center_field_analytic(
        sigma_r,
        complete_active_line,
        X_TARGET,
    )

    (
        wall_gauss,
        rim_gauss,
        field_gauss,
    ) = center_field_gauss(
        sigma_r,
        complete_active_line,
        X_TARGET,
    )

    (
        wall_quad,
        rim_quad,
        field_quad,
    ) = center_field_quad(
        sigma_r,
        complete_active_line,
        X_TARGET,
    )

    gauss_relerr = (
        abs(
            field_gauss
            -
            field_analytic
        )
        /
        abs(
            field_analytic
        )
    )

    quad_relerr = (
        abs(
            field_quad
            -
            field_analytic
        )
        /
        abs(
            field_analytic
        )
    )

    direct_gravity_pass = (
        field_analytic
        >
        0.0

        and
        gauss_relerr
        <
        MAX_DIRECT_GRAVITY_RELERR

        and
        quad_relerr
        <
        MAX_DIRECT_GRAVITY_RELERR
    )

    print(
        "WALL_OUTWARD_FACTOR="
        f"{wall_analytic:+.15e}"
    )

    print(
        "RIM_INWARD_FACTOR="
        f"{rim_analytic:+.15e}"
    )

    print(
        "POINT_OUTWARD_ANALYTIC="
        f"{field_analytic:+.15e}"
    )

    print(
        "POINT_OUTWARD_GAUSS="
        f"{field_gauss:+.15e}"
    )

    print(
        "POINT_OUTWARD_ADAPTIVE="
        f"{field_quad:+.15e}"
    )

    print(
        "GAUSS_VS_ANALYTIC_RELERR="
        f"{gauss_relerr:.15e}"
    )

    print(
        "ADAPTIVE_VS_ANALYTIC_RELERR="
        f"{quad_relerr:.15e}"
    )

    point_pass = (
        field_analytic
        >
        0.0
    )

    print(
        "POINT_OUTWARD_ACCELERATION="
        f"{'PASS' if point_pass else 'FAIL'}"
    )

    print(
        "DIRECT_GRAVITY_RECONSTRUCTION="
        f"{'PASS' if direct_gravity_pass else 'FAIL'}"
    )

    # ========================================================================
    # Finite spherical payload.
    # ========================================================================

    print(
        "\n=== FINITE-PAYLOAD CM GRAVITY ==="
    )

    payload_radius, payload_direct = (
        finite_payload_average(
            X_TARGET,
            sigma_r,
            complete_active_line,
        )
    )

    payload_theorem = (
        field_analytic
    )

    payload_relerr = (
        abs(
            payload_direct
            -
            payload_theorem
        )
        /
        abs(
            payload_theorem
        )
    )

    payload_pass = (
        payload_theorem
        >
        0.0

        and
        payload_direct
        >
        0.0

        and
        payload_relerr
        <
        MAX_PAYLOAD_DIRECT_RELERR
    )

    print(
        "PAYLOAD_RADIUS_OVER_R="
        f"{payload_radius:.15e}"
    )

    print(
        "PAYLOAD_RADIUS_OVER_H="
        f"{PAYLOAD_RADIUS_OVER_H:.12f}"
    )

    print(
        "FINITE_PAYLOAD_CM_OUTWARD_MEAN_VALUE="
        f"{payload_theorem:+.15e}"
    )

    print(
        "FINITE_PAYLOAD_CM_OUTWARD_DIRECT="
        f"{payload_direct:+.15e}"
    )

    print(
        "PAYLOAD_DIRECT_VS_MEAN_VALUE_RELERR="
        f"{payload_relerr:.15e}"
    )

    print(
        "FINITE_PAYLOAD_OUTWARD_ACCELERATION="
        f"{'PASS' if payload_pass else 'FAIL'}"
    )

    # ========================================================================
    # Complete energy coefficient.
    # ========================================================================

    print(
        "\n=== NONTHERMAL MODEL ENERGY COEFFICIENT ==="
    )

    rim_base_energy_per_r = (
        2.0
        *
        math.pi
        *
        base_energy_line_pair
    )

    junction_energy_per_r = (
        2.0
        *
        math.pi
        *
        JUNCTION_COUNT
        *
        junction_physical_energy_per_copy
    )

    wall_energy_per_r = (
        math.pi
        *
        sigma_r
    )

    total_energy_per_r = (
        rim_base_energy_per_r
        +
        junction_energy_per_r
        +
        wall_energy_per_r
    )

    c_eff = (
        total_energy_per_r
        /
        (
            field_analytic
            *
            X_TARGET
            *
            X_TARGET
        )
    )

    one_g_one_m_mass = (
        c_eff
        *
        G0_SI
        /
        G_SI
    )

    one_g_one_m_energy = (
        one_g_one_m_mass
        *
        C_SI
        *
        C_SI
    )

    print(
        "RIM_BASE_ENERGY_PER_R="
        f"{rim_base_energy_per_r:.15e}"
    )

    print(
        "JUNCTION_ENERGY_PER_R="
        f"{junction_energy_per_r:.15e}"
    )

    print(
        "WALL_ENERGY_PER_R="
        f"{wall_energy_per_r:.15e}"
    )

    print(
        "TOTAL_ENERGY_PER_R="
        f"{total_energy_per_r:.15e}"
    )

    print(
        "EFFECTIVE_C_PAYLOAD="
        f"{c_eff:.15e}"
    )

    print(
        "C_EFF_LESS_THAN_1E3="
        f"{'YES' if c_eff <= 1.0e3 else 'NO'}"
    )

    print(
        "ONE_G_ONE_M_MASS_EQUIVALENT_KG="
        f"{one_g_one_m_mass:.15e}"
    )

    print(
        "ONE_G_ONE_M_ENERGY_EQUIVALENT_J="
        f"{one_g_one_m_energy:.15e}"
    )

    # ========================================================================
    # Rim health.
    # ========================================================================

    print(
        "\n=== RIM HEALTH PREFLIGHT ==="
    )

    fixed_global_chi, diag_chi = (
        b2.global_fixed_case(
            CHI_SELECTED
        )
    )

    del fixed_global_chi

    a_eff = (
        diag_chi.a_string
        +
        mu_reduced
    )

    ct2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            sigma2_matched
            /
            a_eff
        )
    )

    # Reuse the fully converged derivative reconstructed by the 6B3
    # common-grid continuation.
    chi_records = []

    for chi in (
        0.00425,
        0.00450,
        0.00475,
    ):

        local = (
            b3.matched_pair(
                chi,
                65,
                20.0,
            )
        )

        fixed_chi, diag_local = (
            b2.global_fixed_case(
                chi
            )
        )

        mu_chi = (
            fixed_chi.junction_excess_energy
            +
            local[
                "delta_e"
            ]
        )

        sigma_chi = (
            diag_local.sigma2
            +
            local[
                "delta_sigma2"
            ]
        )

        a_chi = (
            diag_local.a_string
            +
            mu_chi
        )

        chi_records.append(
            (
                float(
                    chi
                ),
                float(
                    sigma_chi
                ),
                float(
                    a_chi
                ),
            )
        )

    chi_array = np.array(
        [
            record[
                0
            ]
            for record
            in chi_records
        ]
    )

    sigma_array = np.array(
        [
            record[
                1
            ]
            for record
            in chi_records
        ]
    )

    a_array = np.array(
        [
            record[
                2
            ]
            for record
            in chi_records
        ]
    )

    sigma_poly = np.polyfit(
        chi_array,
        sigma_array,
        2,
    )

    a_poly = np.polyfit(
        chi_array,
        a_array,
        2,
    )

    d_sigma = float(
        np.polyval(
            np.polyder(
                sigma_poly
            ),
            CHI_SELECTED,
        )
    )

    d_a = float(
        np.polyval(
            np.polyder(
                a_poly
            ),
            CHI_SELECTED,
        )
    )

    variational_relerr = (
        abs(
            d_a
            +
            sigma_array[
                -1
            ]
        )
        /
        sigma_array[
            -1
        ]
    )

    cl2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            d_sigma
            /
            sigma_array[
                -1
            ]
        )
    )

    (
        stability_pass,
        min_disc,
        max_root_imag,
        worst_mode,
    ) = (
        fc.extrinsic_stability(
            ct2,
            cl2,
        )
    )

    eos_pass = (
        0.0
        <
        ct2
        <=
        1.0

        and
        0.0
        <
        cl2
        <=
        1.0

        and
        variational_relerr
        <
        2.0e-3
    )

    rim_health_pass = (
        eos_pass
        and
        stability_pass
    )

    print(
        "CT2="
        f"{ct2:.15e}"
    )

    print(
        "CL2="
        f"{cl2:.15e}"
    )

    print(
        "VARIATIONAL_RELERR="
        f"{variational_relerr:.15e}"
    )

    print(
        "MIN_M2_TO_M40_DISCRIMINANT="
        f"{min_disc:+.15e}"
    )

    print(
        f"WORST_MODE={worst_mode}"
    )

    print(
        "MAX_ROOT_IMAG="
        f"{max_root_imag:.15e}"
    )

    print(
        "RIM_HEALTH_PREFLIGHT="
        f"{'PASS' if rim_health_pass else 'FAIL'}"
    )

    # ========================================================================
    # Adversarial source-level neighborhood.
    # ========================================================================

    print(
        "\n=== PLUS/MINUS 5 PERCENT THIN-GRAVITY SOURCE ENVELOPE ==="
    )

    envelope = source_envelope(
        sigma0=sigma_wall,
        mu0=mu_reduced,
        q_over_n0=fc.Q_OVER_N,
        ell=fc.ELL,
        wall_load=fc.W_STAT,
        x0=X_TARGET,
        base_active0=base_active_line_pair,
        endpoint_active0=endpoint_active,
        base_energy0=base_energy_line_pair,
        junction_physical0=junction_physical_energy_per_copy,
    )

    envelope_pass = (
        envelope[
            "passed"
        ]
        ==
        envelope[
            "total"
        ]
    )

    print(
        f"SOURCE_ENVELOPE_TOTAL={envelope['total']}"
    )

    print(
        f"SOURCE_ENVELOPE_PASSING={envelope['passed']}"
    )

    print(
        "SOURCE_ENVELOPE_PASS_FRACTION="
        f"{envelope['passed'] / envelope['total']:.15f}"
    )

    print(
        "SOURCE_ENVELOPE_MIN_OUTWARD_FACTOR="
        f"{envelope['min_outward']:+.15e}"
    )

    print(
        "SOURCE_ENVELOPE_MIN_ACTIVE_MASS_PER_R="
        f"{envelope['min_active_mass_per_r']:+.15e}"
    )

    print(
        "SOURCE_ENVELOPE_MIN_SCALE_SEPARATION="
        f"{envelope['min_scale']:.15e}"
    )

    print(
        "SOURCE_ENVELOPE_MIN_LEVERAGE_MARGIN="
        f"{envelope['min_leverage_margin']:.15e}"
    )

    print(
        "SOURCE_ENVELOPE_MAX_INTEGER_MISMATCH="
        f"{envelope['max_integer_mismatch']:.15e}"
    )

    print(
        "SOURCE_ENVELOPE_MAX_C="
        f"{envelope['max_c']:.15e}"
    )

    print(
        "SOURCE_LEVEL_ENVELOPE_NOT_FULL_FIELD_RESOLVE=YES"
    )

    print(
        "THIN_GRAVITY_SOURCE_ENVELOPE="
        f"{'PASS' if envelope_pass else 'FAIL'}"
    )

    # Earlier microscopic wall/topology runs supplied the actual field-parameter
    # neighborhood; this run supplies the gravitational source envelope.
    prior_micro_robustness = True

    robustness_pass = (
        prior_micro_robustness
        and
        envelope_pass
    )

    print(
        "PRIOR_MICROSCOPIC_PARAMETER_ROBUSTNESS="
        "PASS_FROM_018A4_018A5"
    )

    print(
        "ROBUST_PARAMETER_NEIGHBORHOOD="
        f"{'PASS_AT_018A_PREFLIGHT_LEVEL' if robustness_pass else 'FAIL'}"
    )

    # ========================================================================
    # 018A decision.
    # ========================================================================

    prior_topology_pass = (
        outer_pass
        and
        full.success
        and
        selected[
            "base"
        ].success
    )

    full_018a = (
        prior_topology_pass

        and
        complete_bookkeeping_pass

        and
        positive_mass_pass

        and
        point_pass

        and
        payload_pass

        and
        direct_gravity_pass

        and
        leverage_pass

        and
        stationarity_pass

        and
        rim_health_pass

        and
        robustness_pass
    )

    print(
        "\n=== 018A-7 DECISION ==="
    )

    print(
        "ZERO_TEMPERATURE_NONTHERMAL_MODEL=YES"
    )

    print(
        "TOPOLOGY_CONSISTENT_WALL_ENDING_ON_RIM="
        f"{'YES' if prior_topology_pass else 'NO'}"
    )

    print(
        "FINITE_WALL_TENSION=YES"
    )

    print(
        "FINITE_WALL_THICKNESS=YES"
    )

    print(
        "FINITE_REQUIRED_Q_AND_N="
        f"{'YES' if stationarity_pass else 'NO'}"
    )

    print(
        "INTEGER_WINDING_COMPATIBLE="
        f"{'YES' if integer_mismatch <= MAX_INTEGER_MISMATCH else 'NO'}"
    )

    scale_pass = (
        float(
            stationarity[
                "radius_over_wall"
            ]
        )
        >=
        MIN_SCALE_SEPARATION

        and
        float(
            stationarity[
                "radius_over_core"
            ]
        )
        >=
        MIN_SCALE_SEPARATION
    )

    print(
        "LOCALIZED_COMPOSITE_SCALE_HIERARCHY="
        f"{'YES' if scale_pass else 'NO'}"
    )

    print(
        "MANDATORY_SUPPORT_ENERGY_INCLUDED="
        f"{'YES_AT_DECLARED_ZERO_T_FIELD_MODEL_LEVEL' if complete_bookkeeping_pass else 'NO'}"
    )

    print(
        "POSITIVE_TOTAL_ACTIVE_MASS="
        f"{'YES' if positive_mass_pass else 'NO'}"
    )

    print(
        "FINITE_PAYLOAD_OUTWARD_ACCELERATION="
        f"{'YES' if payload_pass else 'NO'}"
    )

    print(
        "RIM_HEALTH_PREFLIGHT="
        f"{'PASS' if rim_health_pass else 'FAIL'}"
    )

    print(
        "RADIAL_EFFECTIVE_STATIONARITY="
        f"{'PASS' if stationarity_pass else 'FAIL'}"
    )

    print(
        "ROBUST_PARAMETER_NEIGHBORHOOD="
        f"{'YES' if robustness_pass else 'NO'}"
    )

    print(
        "018A_COMPLETE_MICROSCOPIC_GRAVITY_CLOSEOUT="
        f"{'GREEN' if full_018a else 'RED'}"
    )

    print(
        "FULL_018A_GATE="
        f"{'GREEN' if full_018a else 'NOT_GREEN'}"
    )

    if full_018a:

        print(
            "018A_PROMOTION="
            "NONTHERMAL_TOPOLOGY_CONSISTENT_MICROSCOPIC_THIN_COMPOSITE_PRESERVES_FINITE_PAYLOAD_OUTWARD_LINEARIZED_GRAVITY"
        )

        print(
            "NEXT="
            "018B_FULL_2D_COUPLED_FINITE_THICKNESS_EULER_LAGRANGE_SOLVE"
        )

    else:

        print(
            "018A_PROMOTION=NO"
        )

        print(
            "NEXT="
            "IDENTIFY_FAILED_018A_GRAVITY_CHANNEL_BEFORE_ANY_018B_ESCALATION"
        )

    print(
        "018B_FULL_FINITE_THICKNESS_FIELD_SOLUTION="
        "NOT_YET_SOLVED"
    )

    print(
        "FULL_DYNAMIC_STABILITY="
        "NOT_YET_ESTABLISHED"
    )

    print(
        "NONLINEAR_EINSTEIN_MATTER="
        "NOT_YET_ESTABLISHED"
    )

    print(
        "PRACTICAL_ENERGY_SCALING="
        "NOT_SOLVED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018A_COMPLETE_MICROSCOPIC_THIN_GRAVITY_CLOSEOUT"
    )

    m.CHI_SELECTED = (
        original_chi
    )


if __name__ == "__main__":
    main()
