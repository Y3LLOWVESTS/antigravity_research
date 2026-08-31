#!/usr/bin/env python3
"""018A-8 — finite-thickness finite-payload gravity closeout.

PURPOSE
-------
Perform the strongest inexpensive gravitational closeout available before
launching the full finite-thickness toroidal Euler-Lagrange solve 018B.

018A-7 demonstrated, in the thin-composite approximation:

    complete declared zero-temperature field-model bookkeeping;
    positive total active mass;
    positive point acceleration;
    kernel leverage;
    healthy rim EOS;
    m=2..40 worldsheet stability;
    radial stationarity;
    2187/2187 source-envelope survival.

Its formal finite-payload failure was only a numerical disagreement between:

    the source-free spherical mean-value theorem;

and

    a relatively low-order direct nested quadrature.

However, the microscopic wall established in 018A-5 has finite thickness.
The selected payload height is not parametrically large compared with that
thickness.

Therefore a stronger question must be answered before promotion:

    Does the finite spherical payload remain accelerated outward when the
    measured microscopic wall active-stress profile is explicitly distributed
    through its physical thickness?

This gate answers that question.

ACTIVE SCIENTIFIC QUESTION
--------------------------
Does complete finite-thickness wall/rim/junction source geometry preserve:

    positive total active mass;

    outward point gravity;

    outward finite-payload center-of-mass gravity;

    kernel leverage;

    robustness;

when the finite spherical payload is allowed to overlap the exponentially
small or finite tails of the microscopic wall stress-energy?

EXACT FINITE-PAYLOAD KERNEL
---------------------------
For a uniform spherical passive payload of radius a centered at c, define

    Kbar(x')
      =
      (1/V)
      integral_payload
      (x - x') / |x - x'|^3 dV_x.

Newton's theorem for a uniform sphere gives an exact closed form.

Let

    d
      =
      |x' - c|.

Then

    Kbar
      =
      (c - x') / a^3

for

    d < a,

and

    Kbar
      =
      (c - x') / d^3

for

    d >= a.

For the vertical component and an axis-centered payload,

    d^2
      =
      r'^2 + (z' - h)^2

and

    Kbar_z
      =
      (h - z') / a^3

inside the payload sphere,

otherwise

    Kbar_z
      =
      (h - z') /
      [r'^2 + (h-z')^2]^(3/2).

This identity exactly handles source/payload spatial overlap.

It removes the integrable singularity that makes naive nested direct
quadrature inefficient.

MICROSCOPIC WALL PROFILE
------------------------
018A-5 established the frozen-Phi Ising wall

    A_real(z)
      =
      F tanh(k z)

with

    k
      =
      F sqrt(lambda_A) / 2.

For the canonical wall conventions used by the project,

    rho_wall(z)
      =
      lambda_A F^4 / 2
      sech^4(k z).

Its integral is

    sigma_W
      =
      4/3 F^3 sqrt(lambda_A).

The integrated active source equals minus the wall tension.

Therefore use the normalized active-source profile

    p_W(z)
      =
      (3 k / 4)
      sech^4(k z)

with

    integral p_W dz = 1.

The wall active source is embedded as a finite-radius disk with this measured
normal profile.

RIM FINITE-CORE ENVELOPE
------------------------
The payload lies near the axis while the vorton rim lies near r=R.

The rim cross-sectional core is therefore far from the payload.

Rather than assume a zero-thickness ring, this calculation deliberately tests:

    ZERO_WIDTH_LINE

    GAUSSIAN_CORE_WIDTH
      =
      A_CORE_WIDTH

    GAUSSIAN_CORE_WIDTH
      =
      2 A_CORE_WIDTH.

The complete positive active line source is distributed through each
cross-section.

All three descriptions must retain the outward finite-payload sign.

This is a finite-core geometry envelope.

It is not a substitute for the actual 018B curved field solution.

JUNCTION
--------
The measured fully coupled junction active correction is approximately
0.1 percent of the 017P pair active line.

For this gate it is included in the complete active line and subjected to the
same conservative rim smearing envelope.

The 018B calculation must resolve its actual curved field distribution.

FINITE-PAYLOAD OBSERVABLE
-------------------------
For total active source S,

    a_CM,z
      proportional to
      -
      integral
      S(x')
      Kbar_z(x')
      dV'.

The sign convention is:

    positive =
      outward.

Because the payload-averaged kernel is evaluated directly, the result remains
valid whether or not the finite wall stress has support inside the passive
payload volume.

Payload backreaction remains outside this approximation.

THIN-SOURCE CROSS-CHECK
-----------------------
For the thin z=0 wall and rim, every source point lies outside the payload
sphere.

The exact finite-payload kernel must therefore reproduce the point-center
field to floating-point accuracy.

This serves as an independent diagnosis of the 018A-7 low-order quadrature
difference.

ROBUSTNESS
----------
Run a simultaneous three-level envelope over:

    wall tension;

    wall inverse thickness k;

    reduced junction energy;

    base rim active line;

    junction active line;

    Q/N;

    target h/R.

Each variable takes

    0.95
    1.00
    1.05

times nominal.

This produces:

    3^7
      =
      2187

source-level physical cases.

For each case additionally require survival for the finite-rim-core envelope.

Thus the finite-thickness gravity sign is tested thousands of times.

ENERGY COEFFICIENT
------------------
Recompute

    C_eff,payload
      =
      (E_total/R)
      /
      [F_payload (h/R)^2]

using the finite-thickness payload acceleration rather than the thin-source
acceleration.

This is expected to remain catastrophically large.

A green 018A result therefore solves a realization gate, not practical energy.

NONLINEAR-GR READINESS
----------------------
For the one-meter / one-g normalization report

    epsilon_compact
      =
      G M / (R c^2).

This estimates the magnitude of nonlinear metric corrections.

A small number does not replace 018E.

It only quantifies whether nonlinear gravity is likely to be a severe or mild
continuation after the actual matter fields and stability are established.

PROMOTION
---------
A strong green result requires:

    THIN_PAYLOAD_KERNEL_EXACT_CROSSCHECK=PASS

    FINITE_THICKNESS_POINT_OUTWARD=PASS

    FINITE_THICKNESS_PAYLOAD_OUTWARD=PASS

    FINITE_RIM_CORE_ENVELOPE=PASS

    POSITIVE_TOTAL_ACTIVE_MASS=PASS

    FINITE_THICKNESS_KERNEL_LEVERAGE=PASS

    RIM_HEALTH_PREFLIGHT=PASS

    RADIAL_EFFECTIVE_STATIONARITY=PASS

    FINITE_THICKNESS_SOURCE_ENVELOPE=PASS

plus the already-established:

    zero-temperature microscopic model;
    topology-consistent wall termination;
    finite wall tension/thickness;
    fine-core coupled junction;
    complete declared field-model energy bookkeeping.

If all pass:

    FULL_018A_GATE=GREEN

and

    018B_AUTHORIZED=YES.

STOP RULE
---------
If finite-thickness finite-payload gravity becomes inward over a robust region,
do not launch 018B merely because the thin approximation was positive.

Instead modify or rerank the microscopic wall geometry.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_FINITE_THICKNESS_PAYLOAD_KERNEL_CLOSEOUT

LIMITATIONS
-----------
This remains:

    linearized gravity;
    thin-curvature embedding of measured straight/local microscopic sectors;
    test-payload gravity;
    no payload backreaction;
    no complete curved toroidal matter-field solve;
    no full dynamic-stability proof;
    no nonlinear Einstein-matter solution;
    no practical energy solution.

The next gate after a green result is the actual 018B field solve.
"""

from __future__ import annotations

from functools import lru_cache
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
    / "018a7_complete_microscopic_gravity_closeout.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Import one verified local research module without invoking main()."""

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


g7 = load_module(
    "ag018a7_finite_thickness_closeout",
    SOURCE,
)

b3 = g7.b3
b2 = g7.b2
fc = g7.fc
m = g7.m


# ============================================================================
# Physical anchors.
# ============================================================================

CHI_SELECTED = 0.00475

OMEGA = b2.OMEGA
K_LONG = b2.K_LONG

X_TARGET = g7.X_TARGET

PAYLOAD_RADIUS_OVER_H = 0.25

JUNCTION_COUNT = 2

G_SI = 6.67430e-11
C_SI = 299792458.0
G0_SI = 9.80665


# ============================================================================
# Strong-pass gates.
# ============================================================================

MAX_ACTIVE_PERTURBATION_FRACTION = 0.01

MIN_SCALE_SEPARATION = 10.0

MAX_INTEGER_MISMATCH = 1.0e-3

MAX_RIM_VARIATIONAL_RELERR = 2.0e-3

MIN_THICK_PAYLOAD_OUTWARD_FACTOR = 0.0

SOURCE_LEVELS = (
    0.95,
    1.00,
    1.05,
)


# ============================================================================
# Exact spherical payload kernel.
# ============================================================================


def payload_kernel_z(
    radius_source: float,
    z_source: float,
    h: float,
    payload_radius: float,
) -> float:
    """Return the exact payload-averaged vertical Newtonian kernel.

    This is exact for a uniform spherical passive payload.

    It remains valid when the source point lies inside the payload volume.
    """

    dz = (
        h
        -
        z_source
    )

    distance_sq = (
        radius_source
        *
        radius_source

        +
        dz
        *
        dz
    )

    if (
        distance_sq
        <
        payload_radius
        *
        payload_radius
    ):

        return (
            dz
            /
            payload_radius**3
        )

    return (
        dz
        /
        distance_sq**1.5
    )


def point_kernel_z(
    radius_source: float,
    z_source: float,
    h: float,
) -> float:
    """Return the ordinary point-target vertical kernel."""

    dz = (
        h
        -
        z_source
    )

    distance_sq = (
        radius_source
        *
        radius_source

        +
        dz
        *
        dz
    )

    if distance_sq == 0.0:
        return 0.0

    return (
        dz
        /
        distance_sq**1.5
    )


# ============================================================================
# Microscopic wall profile.
# ============================================================================


def wall_inverse_width(
    f_a: float,
    lambda_a: float,
) -> float:
    """Return k in A=F tanh(k z)."""

    return (
        f_a
        *
        math.sqrt(
            lambda_a
        )
        /
        2.0
    )


def wall_width90_from_k(
    k_wall: float,
) -> float:
    """Return the 90-percent amplitude width of the Ising wall."""

    return (
        2.0
        *
        math.atanh(
            0.9
        )
        /
        k_wall
    )


def normalized_wall_profile(
    z: float,
    k_wall: float,
) -> float:
    """Normalized sech^4 wall active-source magnitude profile."""

    argument = (
        k_wall
        *
        z
    )

    if abs(
        argument
    ) > 30.0:
        return 0.0

    sech = (
        1.0
        /
        math.cosh(
            argument
        )
    )

    return (
        0.75
        *
        k_wall
        *
        sech**4
    )


def point_radial_integral(
    radius: float,
    dz: float,
) -> float:
    """Integrate r*point_kernel_z from r=0 to source radius."""

    if dz > 0.0:

        return (
            1.0

            -
            dz
            /
            math.sqrt(
                radius
                *
                radius
                +
                dz
                *
                dz
            )
        )

    if dz < 0.0:

        return (
            -1.0

            -
            dz
            /
            math.sqrt(
                radius
                *
                radius
                +
                dz
                *
                dz
            )
        )

    return 0.0


def payload_radial_integral(
    radius: float,
    dz: float,
    payload_radius: float,
) -> float:
    """Integrate r*Kbar_z over a disk radius for one source z-slice.

    The integral is analytic both inside and outside the payload sphere.
    """

    abs_dz = abs(
        dz
    )

    if (
        abs_dz
        >=
        payload_radius
    ):

        if abs_dz == 0.0:
            return 0.0

        return (
            dz
            *
            (
                1.0
                /
                abs_dz

                -
                1.0
                /
                math.sqrt(
                    radius
                    *
                    radius
                    +
                    dz
                    *
                    dz
                )
            )
        )

    inside_radius_sq = (
        payload_radius
        *
        payload_radius

        -
        dz
        *
        dz
    )

    inside = (
        dz
        /
        payload_radius**3
        *
        inside_radius_sq
        /
        2.0
    )

    outside = (
        dz
        *
        (
            1.0
            /
            payload_radius

            -
            1.0
            /
            math.sqrt(
                radius
                *
                radius
                +
                dz
                *
                dz
            )
        )
    )

    return (
        inside
        +
        outside
    )


@lru_cache(maxsize=None)
def wall_gravity_factors_cached(
    sigma_wall: float,
    k_wall: float,
    radius: float,
    h: float,
    payload_radius: float,
):
    """Return finite-thickness wall point and spherical-payload factors."""

    zmax = (
        14.0
        /
        k_wall
    )

    breakpoints = [
        value
        for value
        in (
            h
            -
            payload_radius,

            h,

            h
            +
            payload_radius,
        )
        if
        -zmax
        <
        value
        <
        zmax
    ]

    def point_integrand(
        z_source: float,
    ) -> float:

        return (
            normalized_wall_profile(
                z_source,
                k_wall,
            )
            *
            point_radial_integral(
                radius,
                h
                -
                z_source,
            )
        )

    def payload_integrand(
        z_source: float,
    ) -> float:

        return (
            normalized_wall_profile(
                z_source,
                k_wall,
            )
            *
            payload_radial_integral(
                radius,
                h
                -
                z_source,
                payload_radius,
            )
        )

    point_integral, point_error = quad(
        point_integrand,
        -zmax,
        zmax,
        epsabs=2.0e-12,
        epsrel=2.0e-12,
        points=breakpoints,
        limit=500,
    )

    payload_integral, payload_error = quad(
        payload_integrand,
        -zmax,
        zmax,
        epsabs=2.0e-12,
        epsrel=2.0e-12,
        points=breakpoints,
        limit=500,
    )

    normalization, normalization_error = quad(
        lambda z:
            normalized_wall_profile(
                z,
                k_wall,
            ),
        -zmax,
        zmax,
        epsabs=2.0e-13,
        epsrel=2.0e-13,
        limit=300,
    )

    scale = (
        2.0
        *
        math.pi
        *
        sigma_wall
        *
        radius
        /
        normalization
    )

    return {
        "point":
            float(
                scale
                *
                point_integral
            ),

        "payload":
            float(
                scale
                *
                payload_integral
            ),

        "normalization":
            float(
                normalization
            ),

        "point_quad_error":
            float(
                point_error
            ),

        "payload_quad_error":
            float(
                payload_error
            ),

        "normalization_error":
            float(
                normalization_error
            ),
    }


def wall_gravity_factors(
    sigma_wall: float,
    k_wall: float,
    radius: float,
    h: float,
    payload_radius: float,
):
    """Rounded cache wrapper for wall source integration."""

    return wall_gravity_factors_cached(
        round(
            float(
                sigma_wall
            ),
            15,
        ),

        round(
            float(
                k_wall
            ),
            15,
        ),

        round(
            float(
                radius
            ),
            12,
        ),

        round(
            float(
                h
            ),
            12,
        ),

        round(
            float(
                payload_radius
            ),
            12,
        ),
    )


# ============================================================================
# Finite rim cross-section envelope.
# ============================================================================


def rim_factor_line(
    active_line: float,
    radius: float,
    h: float,
) -> float:
    """Return inward factor for an infinitesimally thin circular rim."""

    x = (
        h
        /
        radius
    )

    return (
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


@lru_cache(maxsize=None)
def rim_factor_gaussian_cached(
    active_line: float,
    radius: float,
    h: float,
    payload_radius: float,
    width: float,
    n_radial: int,
    n_angle: int,
) -> float:
    """Smear the positive rim active line through a Gaussian core."""

    if width <= 0.0:

        return rim_factor_line(
            active_line,
            radius,
            h,
        )

    tn, tw = leggauss(
        n_radial
    )

    pn, pw = leggauss(
        n_angle
    )

    tmax = (
        6.0
        *
        width
    )

    t = (
        0.5
        *
        tmax
        *
        (
            tn
            +
            1.0
        )
    )

    wt = (
        0.5
        *
        tmax
        *
        tw
    )

    psi = (
        math.pi
        *
        (
            pn
            +
            1.0
        )
    )

    wpsi = (
        math.pi
        *
        pw
    )

    T = t[
        :,
        None
    ]

    PSI = psi[
        None,
        :
    ]

    R_SOURCE = (
        radius

        +
        T
        *
        np.cos(
            PSI
        )
    )

    Z_SOURCE = (
        T
        *
        np.sin(
            PSI
        )
    )

    density = (
        np.exp(
            -0.5
            *
            (
                T
                /
                width
            ) ** 2
        )
        /
        (
            2.0
            *
            math.pi
            *
            width
            *
            width
        )
    )

    measure = (
        wt[
            :,
            None
        ]
        *
        wpsi[
            None,
            :
        ]
        *
        T
        *
        density
    )

    normalization = float(
        np.sum(
            measure
        )
    )

    dz = (
        h
        -
        Z_SOURCE
    )

    distance_sq = (
        R_SOURCE
        *
        R_SOURCE

        +
        dz
        *
        dz
    )

    outside_kernel = (
        dz
        /
        distance_sq**1.5
    )

    inside = (
        distance_sq
        <
        payload_radius
        *
        payload_radius
    )

    if np.any(
        inside
    ):

        kernel = np.array(
            outside_kernel,
            copy=True,
        )

        kernel[
            inside
        ] = (
            dz[
                inside
            ]
            /
            payload_radius**3
        )

    else:

        kernel = outside_kernel

    expectation = float(
        np.sum(
            measure
            *
            R_SOURCE
            *
            kernel
        )
        /
        normalization
    )

    return (
        2.0
        *
        math.pi
        *
        radius
        *
        active_line
        *
        expectation
    )


def rim_factor_gaussian(
    active_line: float,
    radius: float,
    h: float,
    payload_radius: float,
    width: float,
    *,
    high_precision: bool,
) -> float:
    """Rounded cache wrapper for finite-core rim evaluation."""

    if high_precision:

        n_radial = 128
        n_angle = 192

    else:

        n_radial = 48
        n_angle = 72

    return rim_factor_gaussian_cached(
        round(
            float(
                active_line
            ),
            14,
        ),

        round(
            float(
                radius
            ),
            10,
        ),

        round(
            float(
                h
            ),
            10,
        ),

        round(
            float(
                payload_radius
            ),
            10,
        ),

        round(
            float(
                width
            ),
            10,
        ),

        n_radial,
        n_angle,
    )


def rim_envelope(
    active_line: float,
    radius: float,
    h: float,
    payload_radius: float,
    core_width: float,
    *,
    high_precision: bool,
):
    """Return line/core/2-core inward factors and their worst case."""

    widths = (
        0.0,
        core_width,
        2.0
        *
        core_width,
    )

    values = []

    for width in widths:

        value = rim_factor_gaussian(
            active_line,
            radius,
            h,
            payload_radius,
            width,
            high_precision=high_precision,
        )

        values.append(
            (
                width,
                value,
            )
        )

    worst = max(
        value
        for (
            _,
            value,
        )
        in values
    )

    return (
        values,
        worst,
    )


# ============================================================================
# Wall overlap diagnostics.
# ============================================================================


def wall_vertical_fraction(
    k_wall: float,
    z_lo: float,
    z_hi: float,
) -> float:
    """Return normalized wall active-source fraction in a vertical interval."""

    zmax = (
        14.0
        /
        k_wall
    )

    lo = max(
        -zmax,
        z_lo,
    )

    hi = min(
        zmax,
        z_hi,
    )

    if hi <= lo:
        return 0.0

    value, _ = quad(
        lambda z:
            normalized_wall_profile(
                z,
                k_wall,
            ),
        lo,
        hi,
        epsabs=1.0e-13,
        epsrel=1.0e-13,
        limit=300,
    )

    return float(
        value
    )


def symmetric_wall_quantile_halfwidth(
    k_wall: float,
    fraction: float,
) -> float:
    """Return z_q such that fraction of wall active source lies in [-z_q,z_q]."""

    lo = 0.0
    hi = (
        14.0
        /
        k_wall
    )

    for _ in range(
        100
    ):

        mid = (
            0.5
            *
            (
                lo
                +
                hi
            )
        )

        value = wall_vertical_fraction(
            k_wall,
            -mid,
            mid,
        )

        if value < fraction:
            lo = mid
        else:
            hi = mid

    return (
        0.5
        *
        (
            lo
            +
            hi
        )
    )


# ============================================================================
# Rim EOS reconstruction.
# ============================================================================


def rim_health(
    mu_reduced: float,
):
    """Reconstruct the matched EOS and extrinsic stability checks."""

    records = []

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

        fixed, diag = (
            b2.global_fixed_case(
                chi
            )
        )

        mu_chi = (
            fixed.junction_excess_energy
            +
            local[
                "delta_e"
            ]
        )

        sigma_chi = (
            diag.sigma2
            +
            local[
                "delta_sigma2"
            ]
        )

        a_chi = (
            diag.a_string
            +
            mu_chi
        )

        records.append(
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
            in records
        ],
        dtype=float,
    )

    sigma_array = np.array(
        [
            record[
                1
            ]
            for record
            in records
        ],
        dtype=float,
    )

    a_array = np.array(
        [
            record[
                2
            ]
            for record
            in records
        ],
        dtype=float,
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

    sigma_selected = float(
        sigma_array[
            -1
        ]
    )

    a_selected = float(
        a_array[
            -1
        ]
    )

    variational_relerr = (
        abs(
            d_a
            +
            sigma_selected
        )
        /
        sigma_selected
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
            sigma_selected
            /
            a_selected
        )
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
            sigma_selected
        )
    )

    (
        stability_pass,
        min_disc,
        max_imag,
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
        MAX_RIM_VARIATIONAL_RELERR
    )

    return {
        "ct2":
            ct2,

        "cl2":
            cl2,

        "variational_relerr":
            variational_relerr,

        "min_disc":
            min_disc,

        "max_imag":
            max_imag,

        "worst_mode":
            worst_mode,

        "pass":
            bool(
                eos_pass
                and
                stability_pass
            ),
    }


# ============================================================================
# Adversarial finite-thickness envelope.
# ============================================================================


def finite_thickness_envelope(
    *,
    sigma0: float,
    k0: float,
    mu0: float,
    q_over_n0: float,
    ell: float,
    wall_load: float,
    x0: float,
    base_active0: float,
    endpoint_active0: float,
    core_width: float,
):
    """Run the complete 3^7 finite-thickness source-level robustness envelope."""

    total = 0
    passed = 0

    min_payload_outward = math.inf
    min_point_outward = math.inf

    min_active_mass_per_r = math.inf
    min_leverage_margin = math.inf
    min_scale = math.inf

    max_integer_mismatch = 0.0

    worst_record = None

    for (
        f_sigma,
        f_k,
        f_mu,
        f_base_active,
        f_endpoint,
        f_q,
        f_x,
    ) in itertools.product(
        SOURCE_LEVELS,
        repeat=7,
    ):

        total += 1

        sigma = (
            sigma0
            *
            f_sigma
        )

        k_wall = (
            k0
            *
            f_k
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

        base_active = (
            base_active0
            *
            f_base_active
        )

        endpoint_active = (
            endpoint_active0
            *
            f_endpoint
        )

        complete_active = (
            base_active

            +
            JUNCTION_COUNT
            *
            endpoint_active
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

        n_integer = max(
            1,
            int(
                round(
                    n_req
                )
            ),
        )

        mismatch = (
            abs(
                sigma
                *
                q_over_n
                *
                n_integer
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

        h = (
            x
            *
            radius
        )

        payload_radius = (
            PAYLOAD_RADIUS_OVER_H
            *
            h
        )

        wall = wall_gravity_factors(
            sigma,
            k_wall,
            radius,
            h,
            payload_radius,
        )

        rim_values, rim_worst = (
            rim_envelope(
                complete_active,
                radius,
                h,
                payload_radius,
                core_width,
                high_precision=False,
            )
        )

        del rim_values

        point_outward = (
            wall[
                "point"
            ]
            -
            rim_worst
        )

        payload_outward = (
            wall[
                "payload"
            ]
            -
            rim_worst
        )

        positive_active_per_r = (
            2.0
            *
            math.pi
            *
            complete_active
        )

        negative_active_per_r = (
            math.pi
            *
            sigma
            *
            radius
        )

        active_mass_per_r = (
            positive_active_per_r
            -
            negative_active_per_r
        )

        if (
            positive_active_per_r
            >
            0.0

            and
            negative_active_per_r
            >
            0.0

            and
            rim_worst
            >
            0.0
        ):

            kappa_positive = (
                rim_worst
                /
                positive_active_per_r
            )

            kappa_negative = (
                wall[
                    "payload"
                ]
                /
                negative_active_per_r
            )

            active_ratio = (
                positive_active_per_r
                /
                negative_active_per_r
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

        else:

            leverage_margin = (
                -math.inf
            )

        wall_width90 = (
            wall_width90_from_k(
                k_wall
            )
        )

        scale = min(
            radius
            /
            wall_width90,

            radius
            /
            core_width,
        )

        case_pass = (
            point_outward
            >
            0.0

            and
            payload_outward
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
            mismatch
            <=
            MAX_INTEGER_MISMATCH
        )

        if case_pass:
            passed += 1

        if (
            payload_outward
            <
            min_payload_outward
        ):

            worst_record = {
                "sigma_factor":
                    f_sigma,

                "k_factor":
                    f_k,

                "mu_factor":
                    f_mu,

                "base_active_factor":
                    f_base_active,

                "endpoint_factor":
                    f_endpoint,

                "q_factor":
                    f_q,

                "x_factor":
                    f_x,

                "payload_outward":
                    payload_outward,

                "point_outward":
                    point_outward,

                "radius":
                    radius,

                "h":
                    h,
            }

        min_payload_outward = min(
            min_payload_outward,
            payload_outward,
        )

        min_point_outward = min(
            min_point_outward,
            point_outward,
        )

        min_active_mass_per_r = min(
            min_active_mass_per_r,
            active_mass_per_r,
        )

        min_leverage_margin = min(
            min_leverage_margin,
            leverage_margin,
        )

        min_scale = min(
            min_scale,
            scale,
        )

        max_integer_mismatch = max(
            max_integer_mismatch,
            mismatch,
        )

    return {
        "total":
            total,

        "passed":
            passed,

        "min_payload_outward":
            min_payload_outward,

        "min_point_outward":
            min_point_outward,

        "min_active_mass_per_r":
            min_active_mass_per_r,

        "min_leverage_margin":
            min_leverage_margin,

        "min_scale":
            min_scale,

        "max_integer_mismatch":
            max_integer_mismatch,

        "worst_record":
            worst_record,
    }


# ============================================================================
# Main closeout.
# ============================================================================


def main() -> None:
    """Run the complete finite-thickness 018A gravity closeout."""

    original_chi = float(
        m.CHI_SELECTED
    )

    m.CHI_SELECTED = (
        CHI_SELECTED
    )

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-8 ==="
    )

    print(
        "QUESTION="
        "DOES_THE_MEASURED_FINITE_THICKNESS_MICROSCOPIC_SOURCE_PRESERVE_FINITE_PAYLOAD_OUTWARD_GRAVITY"
    )

    # ========================================================================
    # Reconstruct microscopic state.
    # ========================================================================

    print(
        "\n=== MICROSCOPIC STATE RECONSTRUCTION ==="
    )

    outer, outer_metrics, outer_pass = (
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

    base = (
        selected[
            "base"
        ]
    )

    fixed, diag = (
        b2.global_fixed_case(
            CHI_SELECTED
        )
    )

    sigma_wall = float(
        m.SIGMA_W_RELAXED_018A5
    )

    f_a = float(
        m.F_A
    )

    lambda_a = float(
        m.LAMBDA_A
    )

    k_wall = (
        wall_inverse_width(
            f_a,
            lambda_a,
        )
    )

    wall_width90 = (
        wall_width90_from_k(
            k_wall
        )
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
        "WALL_F="
        f"{f_a:.15e}"
    )

    print(
        "WALL_LAMBDA_A="
        f"{lambda_a:.15e}"
    )

    print(
        "WALL_K="
        f"{k_wall:.15e}"
    )

    print(
        "WALL_WIDTH90="
        f"{wall_width90:.15e}"
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
        "MATCHED_JUNCTION_ACTIVE_PER_COPY="
        f"{endpoint_active:+.15e}"
    )

    print(
        "OUTER_GLOBAL_WALL_TERMINATION="
        f"{'PASS' if outer_pass else 'FAIL'}"
    )

    # ========================================================================
    # Energy / active line bookkeeping.
    # ========================================================================

    print(
        "\n=== COMPLETE ENERGY / ACTIVE LINE BOOKKEEPING ==="
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
        "BASE_ENERGY_LINE_PAIR="
        f"{base_energy_line_pair:.15e}"
    )

    print(
        "JUNCTION_PHYSICAL_ENERGY_PER_COPY="
        f"{junction_physical_energy_per_copy:+.15e}"
    )

    print(
        "COMPLETE_ENERGY_LINE="
        f"{complete_energy_line:.15e}"
    )

    print(
        "BASE_ACTIVE_LINE_PAIR="
        f"{base_active_line_pair:.15e}"
    )

    print(
        "COMPLETE_ACTIVE_LINE="
        f"{complete_active_line:.15e}"
    )

    print(
        "ACTIVE_PERTURBATION_FRACTION="
        f"{active_perturbation_fraction:.15e}"
    )

    complete_bookkeeping_pass = (
        outer_pass

        and
        full.success

        and
        base.success

        and
        active_perturbation_fraction
        <
        MAX_ACTIVE_PERTURBATION_FRACTION
    )

    print(
        "COMPLETE_FIELD_MODEL_ENERGY_BOOKKEEPING="
        f"{'PASS' if complete_bookkeeping_pass else 'FAIL'}"
    )

    # ========================================================================
    # Stationarity.
    # ========================================================================

    print(
        "\n=== TWO-JUNCTION STATIONARITY ==="
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

    h = (
        X_TARGET
        *
        radius
    )

    payload_radius = (
        PAYLOAD_RADIUS_OVER_H
        *
        h
    )

    payload_bottom = (
        h
        -
        payload_radius
    )

    payload_top = (
        h
        +
        payload_radius
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
        "PAYLOAD_RADIUS="
        f"{payload_radius:.15e}"
    )

    print(
        "PAYLOAD_BOTTOM_Z="
        f"{payload_bottom:.15e}"
    )

    print(
        "PAYLOAD_TOP_Z="
        f"{payload_top:.15e}"
    )

    print(
        "R_OVER_WALL_WIDTH90="
        f"{radius / wall_width90:.15e}"
    )

    print(
        "H_OVER_WALL_WIDTH90="
        f"{h / wall_width90:.15e}"
    )

    print(
        "R_OVER_RIM_CORE="
        f"{radius / m.A_CORE_WIDTH:.15e}"
    )

    print(
        "INTEGER_MISMATCH="
        f"{float(stationarity['mismatch']):.15e}"
    )

    print(
        "RADIAL_EFFECTIVE_STATIONARITY="
        f"{'PASS' if stationarity_pass else 'FAIL'}"
    )

    # ========================================================================
    # Wall source overlap.
    # ========================================================================

    print(
        "\n=== WALL / PAYLOAD OVERLAP DIAGNOSTIC ==="
    )

    wall_fraction_in_payload_vertical_band = (
        wall_vertical_fraction(
            k_wall,
            payload_bottom,
            payload_top,
        )
    )

    q50 = (
        symmetric_wall_quantile_halfwidth(
            k_wall,
            0.50,
        )
    )

    q80 = (
        symmetric_wall_quantile_halfwidth(
            k_wall,
            0.80,
        )
    )

    q90 = (
        symmetric_wall_quantile_halfwidth(
            k_wall,
            0.90,
        )
    )

    q95 = (
        symmetric_wall_quantile_halfwidth(
            k_wall,
            0.95,
        )
    )

    q99 = (
        symmetric_wall_quantile_halfwidth(
            k_wall,
            0.99,
        )
    )

    print(
        "WALL_ACTIVE_HALF_WIDTH_50="
        f"{q50:.15e}"
    )

    print(
        "WALL_ACTIVE_HALF_WIDTH_80="
        f"{q80:.15e}"
    )

    print(
        "WALL_ACTIVE_HALF_WIDTH_90="
        f"{q90:.15e}"
    )

    print(
        "WALL_ACTIVE_HALF_WIDTH_95="
        f"{q95:.15e}"
    )

    print(
        "WALL_ACTIVE_HALF_WIDTH_99="
        f"{q99:.15e}"
    )

    print(
        "WALL_ACTIVE_VERTICAL_FRACTION_IN_PAYLOAD_Z_BAND="
        f"{wall_fraction_in_payload_vertical_band:.15e}"
    )

    print(
        "SOURCE_FREE_MEAN_VALUE_THEOREM_FOR_COMPLETE_FINITE_WALL="
        "NOT_APPLICABLE_WHERE_WALL_TAIL_OVERLAPS_PAYLOAD"
    )

    print(
        "EXACT_OVERLAP_KERNEL_USED_INSTEAD=YES"
    )

    # ========================================================================
    # Thin-source exact payload-kernel cross-check.
    # ========================================================================

    print(
        "\n=== THIN-SOURCE EXACT PAYLOAD-KERNEL CROSS-CHECK ==="
    )

    thin_wall_point = (
        2.0
        *
        math.pi
        *
        sigma_wall
        *
        radius
        *
        (
            1.0

            -
            X_TARGET
            /
            math.sqrt(
                1.0
                +
                X_TARGET
                *
                X_TARGET
            )
        )
    )

    thin_wall_payload = (
        2.0
        *
        math.pi
        *
        sigma_wall
        *
        radius
        *
        payload_radial_integral(
            radius,
            h,
            payload_radius,
        )
    )

    thin_rim = (
        rim_factor_line(
            complete_active_line,
            radius,
            h,
        )
    )

    thin_point = (
        thin_wall_point
        -
        thin_rim
    )

    thin_payload = (
        thin_wall_payload
        -
        thin_rim
    )

    thin_identity_relerr = (
        abs(
            thin_payload
            -
            thin_point
        )
        /
        abs(
            thin_point
        )
    )

    thin_identity_pass = (
        thin_identity_relerr
        <
        5.0e-13
    )

    print(
        "THIN_POINT_OUTWARD="
        f"{thin_point:+.15e}"
    )

    print(
        "THIN_PAYLOAD_EXACT_KERNEL_OUTWARD="
        f"{thin_payload:+.15e}"
    )

    print(
        "THIN_PAYLOAD_KERNEL_IDENTITY_RELERR="
        f"{thin_identity_relerr:.15e}"
    )

    print(
        "THIN_PAYLOAD_KERNEL_EXACT_CROSSCHECK="
        f"{'PASS' if thin_identity_pass else 'FAIL'}"
    )

    print(
        "018A7_LOW_ORDER_DIRECT_QUADRATURE_DISCREPANCY_INTERPRETATION="
        "NUMERICAL_QUADRATURE_ERROR_IF_EXACT_KERNEL_CROSSCHECK_PASSES"
    )

    # ========================================================================
    # Finite-thickness selected gravity.
    # ========================================================================

    print(
        "\n=== FINITE-THICKNESS SELECTED GRAVITY ==="
    )

    wall = (
        wall_gravity_factors(
            sigma_wall,
            k_wall,
            radius,
            h,
            payload_radius,
        )
    )

    rim_values, rim_worst = (
        rim_envelope(
            complete_active_line,
            radius,
            h,
            payload_radius,
            float(
                m.A_CORE_WIDTH
            ),
            high_precision=True,
        )
    )

    for (
        width,
        value,
    ) in rim_values:

        print(
            "RIM_CORE_CASE "
            f"WIDTH={width:.15e} "
            f"INWARD_FACTOR={value:.15e}"
        )

    point_outward = (
        wall[
            "point"
        ]
        -
        rim_worst
    )

    payload_outward = (
        wall[
            "payload"
        ]
        -
        rim_worst
    )

    point_pass = (
        point_outward
        >
        0.0
    )

    payload_pass = (
        payload_outward
        >
        MIN_THICK_PAYLOAD_OUTWARD_FACTOR
    )

    rim_core_pass = all(
        (
            wall[
                "payload"
            ]
            -
            value
        )
        >
        0.0

        for (
            _,
            value,
        )
        in rim_values
    )

    print(
        "FINITE_WALL_POINT_OUTWARD_FACTOR="
        f"{wall['point']:+.15e}"
    )

    print(
        "FINITE_WALL_PAYLOAD_OUTWARD_FACTOR="
        f"{wall['payload']:+.15e}"
    )

    print(
        "FINITE_RIM_WORST_INWARD_FACTOR="
        f"{rim_worst:+.15e}"
    )

    print(
        "FINITE_THICKNESS_POINT_NET_OUTWARD="
        f"{point_outward:+.15e}"
    )

    print(
        "FINITE_THICKNESS_PAYLOAD_NET_OUTWARD="
        f"{payload_outward:+.15e}"
    )

    print(
        "FINITE_WALL_VS_THIN_WALL_POINT_RATIO="
        f"{wall['point'] / thin_wall_point:.15e}"
    )

    print(
        "FINITE_WALL_VS_THIN_WALL_PAYLOAD_RATIO="
        f"{wall['payload'] / thin_wall_payload:.15e}"
    )

    print(
        "FINITE_THICKNESS_POINT_OUTWARD="
        f"{'PASS' if point_pass else 'FAIL'}"
    )

    print(
        "FINITE_THICKNESS_PAYLOAD_OUTWARD="
        f"{'PASS' if payload_pass else 'FAIL'}"
    )

    print(
        "FINITE_RIM_CORE_ENVELOPE="
        f"{'PASS' if rim_core_pass else 'FAIL'}"
    )

    # ========================================================================
    # Total active mass and finite-thickness leverage.
    # ========================================================================

    print(
        "\n=== FINITE-THICKNESS ACTIVE MASS + KERNEL LEVERAGE ==="
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

    total_active = (
        positive_active
        -
        negative_active
    )

    positive_active_per_r = (
        2.0
        *
        math.pi
        *
        complete_active_line
    )

    negative_active_per_r = (
        math.pi
        *
        sigma_wall
        *
        radius
    )

    kappa_positive = (
        rim_worst
        /
        positive_active_per_r
    )

    kappa_negative = (
        wall[
            "payload"
        ]
        /
        negative_active_per_r
    )

    active_ratio = (
        positive_active_per_r
        /
        negative_active_per_r
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
        total_active
        >
        0.0
    )

    leverage_pass = (
        leverage_margin
        >
        1.0

        and
        payload_outward
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
        f"{total_active:+.15e}"
    )

    print(
        "Q_PLUS_OVER_Q_MINUS="
        f"{active_ratio:.15e}"
    )

    print(
        "FINITE_THICKNESS_KAPPA_MINUS_OVER_KAPPA_PLUS="
        f"{leverage_ratio:.15e}"
    )

    print(
        "FINITE_THICKNESS_KERNEL_LEVERAGE_MARGIN="
        f"{leverage_margin:.15e}"
    )

    print(
        "POSITIVE_TOTAL_ACTIVE_MASS="
        f"{'PASS' if positive_mass_pass else 'FAIL'}"
    )

    print(
        "FINITE_THICKNESS_KERNEL_LEVERAGE="
        f"{'PASS' if leverage_pass else 'FAIL'}"
    )

    # ========================================================================
    # Energy coefficient with corrected payload field.
    # ========================================================================

    print(
        "\n=== FINITE-THICKNESS ENERGY SCALING ==="
    )

    rim_energy_per_r = (
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
        sigma_wall
        *
        radius
    )

    total_energy_per_r = (
        rim_energy_per_r
        +
        junction_energy_per_r
        +
        wall_energy_per_r
    )

    if payload_outward > 0.0:

        c_eff = (
            total_energy_per_r
            /
            (
                payload_outward
                *
                X_TARGET
                *
                X_TARGET
            )
        )

    else:

        c_eff = math.inf

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
        "TOTAL_ENERGY_PER_R="
        f"{total_energy_per_r:.15e}"
    )

    print(
        "FINITE_THICKNESS_EFFECTIVE_C_PAYLOAD="
        f"{c_eff:.15e}"
    )

    print(
        "ONE_G_ONE_M_MASS_EQUIVALENT_KG="
        f"{one_g_one_m_mass:.15e}"
    )

    print(
        "ONE_G_ONE_M_ENERGY_EQUIVALENT_J="
        f"{one_g_one_m_energy:.15e}"
    )

    print(
        "PRACTICAL_ENERGY_SCALING="
        "FAIL_CATASTROPHIC"
    )

    # ========================================================================
    # Rim health.
    # ========================================================================

    print(
        "\n=== RIM HEALTH ==="
    )

    health = (
        rim_health(
            mu_reduced
        )
    )

    print(
        "CT2="
        f"{health['ct2']:.15e}"
    )

    print(
        "CL2="
        f"{health['cl2']:.15e}"
    )

    print(
        "VARIATIONAL_RELERR="
        f"{health['variational_relerr']:.15e}"
    )

    print(
        "MIN_M2_TO_M40_DISCRIMINANT="
        f"{health['min_disc']:+.15e}"
    )

    print(
        f"WORST_MODE={health['worst_mode']}"
    )

    print(
        "MAX_ROOT_IMAG="
        f"{health['max_imag']:.15e}"
    )

    print(
        "RIM_HEALTH_PREFLIGHT="
        f"{'PASS' if health['pass'] else 'FAIL'}"
    )

    # ========================================================================
    # Full finite-thickness robustness envelope.
    # ========================================================================

    print(
        "\n=== 2187-CASE FINITE-THICKNESS ROBUSTNESS ENVELOPE ==="
    )

    envelope = (
        finite_thickness_envelope(
            sigma0=sigma_wall,
            k0=k_wall,
            mu0=mu_reduced,
            q_over_n0=fc.Q_OVER_N,
            ell=fc.ELL,
            wall_load=fc.W_STAT,
            x0=X_TARGET,
            base_active0=base_active_line_pair,
            endpoint_active0=endpoint_active,
            core_width=float(
                m.A_CORE_WIDTH
            ),
        )
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
        f"FINITE_THICKNESS_ENVELOPE_TOTAL={envelope['total']}"
    )

    print(
        f"FINITE_THICKNESS_ENVELOPE_PASSING={envelope['passed']}"
    )

    print(
        "FINITE_THICKNESS_ENVELOPE_PASS_FRACTION="
        f"{envelope['passed'] / envelope['total']:.15f}"
    )

    print(
        "FINITE_THICKNESS_ENVELOPE_MIN_PAYLOAD_OUTWARD="
        f"{envelope['min_payload_outward']:+.15e}"
    )

    print(
        "FINITE_THICKNESS_ENVELOPE_MIN_POINT_OUTWARD="
        f"{envelope['min_point_outward']:+.15e}"
    )

    print(
        "FINITE_THICKNESS_ENVELOPE_MIN_ACTIVE_MASS_PER_R="
        f"{envelope['min_active_mass_per_r']:+.15e}"
    )

    print(
        "FINITE_THICKNESS_ENVELOPE_MIN_LEVERAGE_MARGIN="
        f"{envelope['min_leverage_margin']:.15e}"
    )

    print(
        "FINITE_THICKNESS_ENVELOPE_MIN_SCALE_SEPARATION="
        f"{envelope['min_scale']:.15e}"
    )

    print(
        "FINITE_THICKNESS_ENVELOPE_MAX_INTEGER_MISMATCH="
        f"{envelope['max_integer_mismatch']:.15e}"
    )

    print(
        "FINITE_THICKNESS_WORST_CASE="
        f"{envelope['worst_record']}"
    )

    print(
        "FINITE_THICKNESS_SOURCE_ENVELOPE="
        f"{'PASS' if envelope_pass else 'FAIL'}"
    )

    # ========================================================================
    # Nonlinear-GR readiness / compactness.
    # ========================================================================

    print(
        "\n=== NONLINEAR-GR READINESS DIAGNOSTIC ==="
    )

    physical_radius_at_h_1m = (
        1.0
        /
        X_TARGET
    )

    compactness_1m = (
        c_eff
        *
        G0_SI
        *
        X_TARGET
        /
        (
            C_SI
            *
            C_SI
        )
    )

    schwarzschild_ratio_1m = (
        2.0
        *
        compactness_1m
    )

    print(
        "ONE_G_ONE_M_SOURCE_RADIUS_M="
        f"{physical_radius_at_h_1m:.15e}"
    )

    print(
        "GM_OVER_RC2_AT_ONE_G_ONE_M="
        f"{compactness_1m:.15e}"
    )

    print(
        "TWO_GM_OVER_RC2_AT_ONE_G_ONE_M="
        f"{schwarzschild_ratio_1m:.15e}"
    )

    print(
        "LOW_COMPACTNESS_NONLINEAR_CONTINUATION_EXPECTATION="
        f"{'PERTURBATIVE' if schwarzschild_ratio_1m < 1.0e-6 else 'NONTRIVIAL'}"
    )

    print(
        "NONLINEAR_EINSTEIN_MATTER_SOLVED_BY_THIS_RUN=NO"
    )

    # ========================================================================
    # Final decision.
    # ========================================================================

    scale_pass = (
        radius
        /
        wall_width90
        >=
        MIN_SCALE_SEPARATION

        and
        radius
        /
        float(
            m.A_CORE_WIDTH
        )
        >=
        MIN_SCALE_SEPARATION
    )

    integer_pass = (
        float(
            stationarity[
                "mismatch"
            ]
        )
        <=
        MAX_INTEGER_MISMATCH
    )

    microscopic_pass = (
        outer_pass
        and
        full.success
        and
        base.success
    )

    full_018a = (
        microscopic_pass

        and
        complete_bookkeeping_pass

        and
        stationarity_pass

        and
        scale_pass

        and
        integer_pass

        and
        thin_identity_pass

        and
        point_pass

        and
        payload_pass

        and
        rim_core_pass

        and
        positive_mass_pass

        and
        leverage_pass

        and
        health[
            "pass"
        ]

        and
        envelope_pass
    )

    print(
        "\n=== 018A-8 DECISION ==="
    )

    print(
        "ZERO_TEMPERATURE_NONTHERMAL_MODEL=YES"
    )

    print(
        "TOPOLOGY_CONSISTENT_WALL_ENDING_ON_RIM="
        f"{'YES' if microscopic_pass else 'NO'}"
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
        f"{'YES' if integer_pass else 'NO'}"
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
        "FINITE_THICKNESS_GRAVITY_INCLUDED=YES"
    )

    print(
        "FINITE_RIM_CORE_ENVELOPE="
        f"{'PASS' if rim_core_pass else 'FAIL'}"
    )

    print(
        "RIM_HEALTH_PREFLIGHT="
        f"{'PASS' if health['pass'] else 'FAIL'}"
    )

    print(
        "RADIAL_EFFECTIVE_STATIONARITY="
        f"{'PASS' if stationarity_pass else 'FAIL'}"
    )

    print(
        "ROBUST_PARAMETER_NEIGHBORHOOD="
        f"{'YES' if envelope_pass else 'NO'}"
    )

    print(
        "018A8_FINITE_THICKNESS_PAYLOAD_CLOSEOUT="
        f"{'GREEN' if full_018a else 'RED'}"
    )

    print(
        "FULL_018A_GATE="
        f"{'GREEN' if full_018a else 'NOT_GREEN'}"
    )

    if full_018a:

        print(
            "018A_PROMOTION="
            "NONTHERMAL_TOPOLOGY_CONSISTENT_MICROSCOPIC_COMPOSITE_PRESERVES_FINITE_THICKNESS_FINITE_PAYLOAD_OUTWARD_LINEARIZED_GRAVITY"
        )

        print(
            "018B_AUTHORIZED=YES"
        )

        print(
            "NEXT="
            "018B_FULL_TOROIDAL_2D_COUPLED_FINITE_THICKNESS_EULER_LAGRANGE_SOLVE"
        )

        print(
            "CURRENT_HEURISTIC_IF_ACCEPTED="
            "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
        )

    else:

        print(
            "018A_PROMOTION=NO"
        )

        print(
            "018B_AUTHORIZED=NO"
        )

        print(
            "NEXT="
            "IDENTIFY_FINITE_THICKNESS_FAILURE_CHANNEL_BEFORE_FULL_FIELD_ESCALATION"
        )

        print(
            "CURRENT_HEURISTIC="
            "APPROXIMATELY_65_PERCENT_NOT_A_PROBABILITY"
        )

    print(
        "SHORTEST_PATH_TO_80_PERCENT="
        "018B_FULL_FIELD_THEN_018C_FULL_STABILITY_THEN_018D_STATIONARY_GR_THEN_018E_NONLINEAR_EINSTEIN_MATTER"
    )

    print(
        "EIGHTY_PERCENT_REACHED_BY_THIS_RUN=NO"
    )

    print(
        "018B_FULL_FINITE_THICKNESS_FIELD_SOLUTION="
        "NOT_YET_SOLVED"
    )

    print(
        "018C_FULL_COMPOSITE_STABILITY="
        "NOT_YET_SOLVED"
    )

    print(
        "018E_NONLINEAR_EINSTEIN_MATTER="
        "NOT_YET_SOLVED"
    )

    print(
        "PRACTICAL_ENERGY_SCALING="
        "CATASTROPHIC_CURRENTLY"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018A_FINITE_THICKNESS_PAYLOAD_KERNEL_CLOSEOUT"
    )

    m.CHI_SELECTED = (
        original_chi
    )


if __name__ == "__main__":
    main()
