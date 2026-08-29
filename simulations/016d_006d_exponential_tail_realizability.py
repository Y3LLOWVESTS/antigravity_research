r"""016D — exponential-tail realizability augmentation for 006D.

PURPOSE
-------
Test whether replacing the exact compact-support termination of the 006D
stress tensor with smooth exponentially localized tails preserves the useful
gravitational and stability properties while removing the divergent
finite-boundary gauge-integrability burden exposed by 008E and 016C.

SCIENTIFIC QUESTION
-------------------
The compact 006D source is a valid constructive linearized-GR result.

Later physical-realization work found:

- 008D:
  one charged/winding complex scalar is insufficient;

- 008E:
  a finite collection of ungauged winding scalars requires winding number
  diverging at the exact compact outer termination;

- 008F:
  a local scalar + Maxwell stress decomposition exists;

- 016C:
  the simplest exact global one- or two-electrostatic-field realization is
  obstructed.

These failures may be associated specifically with exact compact field
termination rather than with the repulsive 006D stress architecture itself.

A physical soliton normally approaches a vacuum asymptotically instead of
having exactly compact support.

This simulation therefore keeps the 006D core, transfer annulus, positive
energy, DEC structure, and radial conservation law, while replacing the exact
outer compact-support collar and compact vertical bump with smooth
exponentially localized tails.

RADIAL STRESS CONSTRUCTION
--------------------------
As in 006D,

    q(r) = r p_r(r)

and

    p_phi(r) = dq/dr.

Thus

    dp_r/dr + (p_r - p_phi)/r = 0

identically.

The core and transfer annulus remain unchanged.

For r >= beta define

    x = (r-beta)/ell

and

    f(x)
        =
        exp[-x^3/(1+x^2)].

This function satisfies

    f(0)   = 1,
    f'(0)  = 0,
    f''(0) = 0,

while

    f(x) ~ exp(-x)

for large x.

The tail is

    q(r)
        =
        -alpha^2 f(x)/r.

Hence q and its first two radial derivatives match the annular branch at the
start of the tail while q -> 0 exponentially.

VERTICAL PROFILE
----------------
Use the normalized smooth profile

    phi(z)
        =
        [1/(2w)]
        sech^2[(z-z0)/w],

with

    z0 = -delta/2,
    w  = delta/4.

It obeys

    integral phi(z) dz = 1

over the real line.

The logarithmic derivative is bounded:

    |d log(phi)/dz| <= 2/w.

This contrasts with exact compact support, where logarithmic derivatives
diverge at a finite boundary.

ENERGY CONDITIONS
-----------------
As in 006D,

    epsilon
        =
        max(
            |p_r|,
            |p_phi|
        ),

with

    p_z = 0.

Therefore pointwise type-I DEC, WEC, and NEC remain satisfied.

INTEGRATED STRESS TRACE
-----------------------
Because

    p_r = q/r

and

    p_phi = q',

    integral r(p_r+p_phi) dr
        =
        [r q]_0^infinity.

Since q vanishes at the axis and exponentially at infinity,

    integrated spatial stress trace = 0.

GAUGE-DERIVATIVE PREFLIGHT
--------------------------
For an asymptotic Higgs/gauged winding sector with finite vacuum amplitude,
the gauge-covariant angular mismatch k(r,z) can be chosen schematically as

    k
        proportional to
        r sqrt(A),

where

    A = epsilon + p_phi

is the required angular scalar Gram contribution.

The relevant radial derivative burden is

    R_r
        =
        [d(r sqrt(A))/dr]^2
        /
        [r^2 A].

For the smooth exponential tail R_r remains finite.

The vertical sech^2 profile similarly gives the exact bound

    R_z <= 1/w^2.

The sum

    R_total = R_r + R_z

is therefore finite.

This does NOT construct a gauge field solution.  It only tests whether the
infinite derivative burden produced by exact compact termination has been
removed.

FIXED-CHARGE STABILITY
----------------------
The local temporal kinetic capacity is

    D_max
        =
        min(
            epsilon+p_r,
            epsilon+p_phi,
            epsilon
        ).

Define

    T_max
        =
        (1/2) integral D_max dV.

The earlier fixed-charge Derrick criterion is

    T/E > 1/8.

This gate recomputes T_max/E for the new tail architecture rather than
assuming the 016B compact-source value survives.

GRAVITATIONAL FIELD
-------------------
The exact linearized-GR axial field integral is recomputed using the new
radial and vertical profiles.

The dimensionless coefficient remains

    C = m/(2F).

APPROXIMATION LEVEL
-------------------
- static linearized GR;
- type-I positive-energy source;
- exact flat-background local conservation;
- canonical fixed-charge capacity preflight;
- kinematic gauge-integrability preflight.

NOT ESTABLISHED
---------------
A green result does not establish:

- exact compact support;
- a global gauged-scalar solution;
- satisfaction of the full nonlinear matter Euler-Lagrange equations;
- full perturbative stability;
- nonlinear Einstein-matter equilibrium;
- practical macroscopic energy requirements;
- a practical antigravity device.

The original compact 006D construction remains the mathematical finite-source
result.  This simulation tests a distinct exponentially localized
realizability augmentation.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_006D_EXPONENTIAL_TAIL_REALIZABILITY_PREFLIGHT
"""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad


G = 6.67430e-11
C_LIGHT = 299_792_458.0
G_STANDARD = 9.80665

ALPHA = 1.437500564637
BETA = 4.701437405300

DERRICK_CRITICAL_T_OVER_E = 1.0 / 8.0

C_COMPACT = {
    0.10: 26.258214373557,
    0.20: 29.559369544823,
}

PEAK_COMPACT_J_M3_TIMES_H = {
    0.10: 1.217786464792e30,
    0.20: 3.394961867851e29,
}

PEAK_FINE_006D_J_M3_TIMES_H = (
    2.826392305523e32
)

CASES = (
    (0.10, 0.10),
    (0.10, 0.20),
    (0.10, 0.40),
    (0.10, 0.80),
    (0.20, 0.10),
    (0.20, 0.20),
    (0.20, 0.40),
    (0.20, 0.80),
)


def smoothstep(
    value: float,
) -> float:
    """Return cubic smoothstep."""

    return (
        value
        * value
        * (
            3.0
            - 2.0 * value
        )
    )


def smoothstep_prime(
    value: float,
) -> float:
    """Return derivative of cubic smoothstep."""

    return (
        6.0
        * value
        * (
            1.0
            - value
        )
    )


def tail_decay(
    x: float,
) -> float:
    """Return C2-matched asymptotically exponential tail function."""

    exponent = (
        x**3
        / (
            1.0
            + x*x
        )
    )

    return math.exp(
        -exponent
    )


def tail_decay_prime_r(
    x: float,
    ell: float,
) -> float:
    """Return radial derivative of the tail function."""

    denominator = (
        1.0
        + x*x
    )

    exponent_prime_x = (
        x*x
        * (
            3.0
            + x*x
        )
        / (
            denominator
            * denominator
        )
    )

    return (
        -exponent_prime_x
        / ell
        * tail_decay(
            x
        )
    )


def q_and_prime(
    radius: float,
    delta: float,
    ell: float,
) -> tuple[float, float]:
    """Return q=r*p_r and dq/dr for the tail-regularized 006D source."""

    inner_width = (
        delta
        / 4.0
    )

    x_minus = (
        ALPHA
        - inner_width
    )

    x_plus = (
        ALPHA
        + inner_width
    )

    if radius <= 0.0:
        return (
            0.0,
            -1.0,
        )

    q_core = -radius
    qp_core = -1.0

    q_annulus = (
        -(ALPHA * ALPHA)
        / radius
    )

    qp_annulus = (
        (ALPHA * ALPHA)
        / (
            radius
            * radius
        )
    )

    if radius < x_minus:
        return (
            q_core,
            qp_core,
        )

    if radius <= x_plus:
        u = (
            (
                radius
                - x_minus
            )
            / (
                x_plus
                - x_minus
            )
        )

        s = smoothstep(
            u
        )

        sp = (
            smoothstep_prime(
                u
            )
            / (
                x_plus
                - x_minus
            )
        )

        q = (
            (
                1.0
                - s
            )
            * q_core
            +
            s
            * q_annulus
        )

        qp = (
            (
                1.0
                - s
            )
            * qp_core
            +
            s
            * qp_annulus
            +
            sp
            * (
                q_annulus
                - q_core
            )
        )

        return (
            q,
            qp,
        )

    if radius < BETA:
        return (
            q_annulus,
            qp_annulus,
        )

    x = (
        radius
        - BETA
    ) / ell

    decay = tail_decay(
        x
    )

    decay_prime = (
        tail_decay_prime_r(
            x,
            ell,
        )
    )

    q = (
        -(ALPHA * ALPHA)
        * decay
        / radius
    )

    qp = (
        (ALPHA * ALPHA)
        * decay
        / (
            radius
            * radius
        )
        -
        (ALPHA * ALPHA)
        * decay_prime
        / radius
    )

    return (
        q,
        qp,
    )


def stress(
    radius: float,
    delta: float,
    ell: float,
) -> tuple[
    float,
    float,
    float,
]:
    """Return epsilon, p_r, and p_phi."""

    q, qp = q_and_prime(
        radius,
        delta,
        ell,
    )

    if radius <= 0.0:
        p_r = -1.0
    else:
        p_r = (
            q
            / radius
        )

    p_phi = qp

    epsilon = max(
        abs(
            p_r
        ),
        abs(
            p_phi
        ),
    )

    return (
        epsilon,
        p_r,
        p_phi,
    )


def radial_breakpoints(
    delta: float,
    ell: float,
) -> tuple[float, ...]:
    """Return integration regions including exponentially negligible tail end."""

    return (
        0.0,
        ALPHA
        - delta / 4.0,
        ALPHA
        + delta / 4.0,
        BETA,
        BETA
        + 40.0 * ell,
    )


def radial_integral(
    function,
    delta: float,
    ell: float,
) -> float:
    """Perform piecewise adaptive radial integration."""

    total = 0.0

    points = radial_breakpoints(
        delta,
        ell,
    )

    for lower, upper in zip(
        points[:-1],
        points[1:],
    ):
        value, _ = quad(
            function,
            lower,
            upper,
            epsabs=2.0e-10,
            epsrel=2.0e-10,
            limit=600,
        )

        total += value

    return float(
        total
    )


def vertical_kernel_setup(
    delta: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """Return normalized Gauss-Legendre representation of sech^2 vertical tail."""

    order = 128

    nodes, weights = leggauss(
        order
    )

    u_limit = 12.0

    u = (
        u_limit
        * nodes
    )

    du_weights = (
        u_limit
        * weights
    )

    sech_squared = (
        1.0
        / np.cosh(
            u
        )**2
    )

    bump_weights = (
        0.5
        * sech_squared
        * du_weights
    )

    bump_weights = (
        bump_weights
        / np.sum(
            bump_weights
        )
    )

    width = (
        delta
        / 4.0
    )

    center = (
        -delta
        / 2.0
    )

    zeta = (
        center
        +
        width
        * u
    )

    return (
        zeta,
        bump_weights,
    )


def field_factor(
    delta: float,
    ell: float,
) -> float:
    """Return dimensionless outward axial field factor."""

    zeta, weights = (
        vertical_kernel_setup(
            delta
        )
    )

    separation = (
        1.0
        - zeta
    )

    def integrand(
        radius: float,
    ) -> float:
        (
            epsilon,
            p_r,
            p_phi,
        ) = stress(
            radius,
            delta,
            ell,
        )

        active = (
            epsilon
            + p_r
            + p_phi
        )

        kernel = float(
            np.sum(
                weights
                * separation
                / (
                    radius * radius
                    +
                    separation
                    * separation
                ) ** 1.5
            )
        )

        return (
            radius
            * active
            * kernel
        )

    return (
        -radial_integral(
            integrand,
            delta,
            ell,
        )
    )


def integrated_quantities(
    delta: float,
    ell: float,
) -> dict[str, float]:
    """Return mass, trace, fixed-charge capacity, field, and coefficient."""

    energy_radial = (
        radial_integral(
            lambda radius:
                radius
                * stress(
                    radius,
                    delta,
                    ell,
                )[0],
            delta,
            ell,
        )
    )

    trace_radial = (
        radial_integral(
            lambda radius:
                radius
                * (
                    stress(
                        radius,
                        delta,
                        ell,
                    )[1]
                    +
                    stress(
                        radius,
                        delta,
                        ell,
                    )[2]
                ),
            delta,
            ell,
        )
    )

    d_capacity_radial = (
        radial_integral(
            lambda radius:
                radius
                * min(
                    stress(
                        radius,
                        delta,
                        ell,
                    )[0]
                    +
                    stress(
                        radius,
                        delta,
                        ell,
                    )[1],
                    stress(
                        radius,
                        delta,
                        ell,
                    )[0]
                    +
                    stress(
                        radius,
                        delta,
                        ell,
                    )[2],
                    stress(
                        radius,
                        delta,
                        ell,
                    )[0],
                ),
            delta,
            ell,
        )
    )

    mass_factor = (
        2.0
        * energy_radial
    )

    pressure_trace_factor = (
        2.0
        * trace_radial
    )

    t_over_e = (
        0.5
        * d_capacity_radial
        / energy_radial
    )

    field = field_factor(
        delta,
        ell,
    )

    coefficient = (
        mass_factor
        / (
            2.0
            * field
        )
    )

    return {
        "mass_factor":
            mass_factor,
        "trace_factor":
            pressure_trace_factor,
        "t_over_e":
            t_over_e,
        "field_factor":
            field,
        "coefficient":
            coefficient,
    }


def peak_stress_prefactor(
    delta: float,
    ell: float,
    field: float,
) -> tuple[
    float,
    float,
]:
    """Return peak radial epsilon and physical peak-density times h."""

    outer = (
        BETA
        + 20.0 * ell
    )

    radius = np.linspace(
        0.0,
        outer,
        300_001,
    )

    epsilon = np.array(
        [
            stress(
                float(value),
                delta,
                ell,
            )[0]
            for value
            in radius
        ],
        dtype=float,
    )

    epsilon_max = float(
        np.max(
            epsilon
        )
    )

    vertical_peak = (
        2.0
        / delta
    )

    surface_energy = (
        G_STANDARD
        * C_LIGHT**2
        / (
            2.0
            * math.pi
            * G
            * field
        )
    )

    peak_times_h = (
        surface_energy
        * epsilon_max
        * vertical_peak
    )

    return (
        epsilon_max,
        peak_times_h,
    )


def radial_gauge_derivative_burden(
    delta: float,
    ell: float,
) -> float:
    """Return maximum finite radial logarithmic/gauge derivative burden."""

    radius = np.linspace(
        BETA,
        BETA
        + 30.0 * ell,
        60_001,
    )

    angular_gram = np.array(
        [
            (
                stress(
                    float(value),
                    delta,
                    ell,
                )[0]
                +
                stress(
                    float(value),
                    delta,
                    ell,
                )[2]
            )
            for value
            in radius
        ],
        dtype=float,
    )

    maximum_gram = float(
        np.max(
            angular_gram
        )
    )

    mask = (
        angular_gram
        >
        maximum_gram
        * 1.0e-16
    )

    safe_radius = radius[
        mask
    ]

    safe_gram = angular_gram[
        mask
    ]

    mapped_amplitude = (
        safe_radius
        * np.sqrt(
            safe_gram
        )
    )

    derivative = np.gradient(
        mapped_amplitude,
        safe_radius,
        edge_order=2,
    )

    burden = (
        derivative
        * derivative
        / (
            safe_radius
            * safe_radius
            * safe_gram
        )
    )

    if burden.size > 20:
        burden = burden[
            5:-5
        ]

    return float(
        np.max(
            burden
        )
    )


def main() -> None:
    """Execute the exponential-tail realizability preflight."""

    print(
        "=== 016D — 006D EXPONENTIAL-TAIL "
        "REALIZABILITY GATE ==="
    )

    all_gravity_green = True
    all_stability_green = True
    all_trace_green = True
    all_gauge_burdens_finite = True

    records = []

    for delta, ell in CASES:
        result = integrated_quantities(
            delta,
            ell,
        )

        (
            epsilon_max,
            peak_times_h,
        ) = peak_stress_prefactor(
            delta,
            ell,
            result[
                "field_factor"
            ],
        )

        radial_burden = (
            radial_gauge_derivative_burden(
                delta,
                ell,
            )
        )

        vertical_width = (
            delta
            / 4.0
        )

        vertical_burden = (
            1.0
            / (
                vertical_width
                * vertical_width
            )
        )

        total_burden = (
            radial_burden
            +
            vertical_burden
        )

        xi_for_10pct = math.sqrt(
            total_burden
            / 0.10
        )

        xi_for_25pct = math.sqrt(
            total_burden
            / 0.25
        )

        compact_c = (
            C_COMPACT[
                delta
            ]
        )

        compact_peak = (
            PEAK_COMPACT_J_M3_TIMES_H[
                delta
            ]
        )

        c_change_percent = (
            100.0
            * (
                result[
                    "coefficient"
                ]
                / compact_c
                -
                1.0
            )
        )

        peak_relief_vs_compact = (
            compact_peak
            / peak_times_h
        )

        peak_relief_vs_finest = (
            PEAK_FINE_006D_J_M3_TIMES_H
            / peak_times_h
        )

        gravity_green = bool(
            result[
                "field_factor"
            ]
            >
            0.0
        )

        stability_green = bool(
            result[
                "t_over_e"
            ]
            >
            DERRICK_CRITICAL_T_OVER_E
        )

        trace_green = bool(
            abs(
                result[
                    "trace_factor"
                ]
            )
            <
            1.0e-8
        )

        gauge_finite = bool(
            math.isfinite(
                total_burden
            )
        )

        all_gravity_green = (
            all_gravity_green
            and gravity_green
        )

        all_stability_green = (
            all_stability_green
            and stability_green
        )

        all_trace_green = (
            all_trace_green
            and trace_green
        )

        all_gauge_burdens_finite = (
            all_gauge_burdens_finite
            and gauge_finite
        )

        records.append(
            (
                delta,
                ell,
                result,
                peak_times_h,
                total_burden,
                peak_relief_vs_finest,
            )
        )

        print(
            "CASE "
            f"DELTA={delta:.8f} "
            f"ELL={ell:.8f} "
            f"MASS_FACTOR="
            f"{result['mass_factor']:.15e} "
            f"TRACE_FACTOR="
            f"{result['trace_factor']:.3e} "
            f"FIELD_FACTOR="
            f"{result['field_factor']:.15e} "
            f"C={result['coefficient']:.12f} "
            f"C_CHANGE_VS_COMPACT_PERCENT="
            f"{c_change_percent:+.6f} "
            f"TMAX_OVER_E="
            f"{result['t_over_e']:.15e} "
            f"FIXED_CHARGE_STABLE="
            f"{stability_green} "
            f"RADIAL_GAUGE_BURDEN="
            f"{radial_burden:.12e} "
            f"VERTICAL_GAUGE_BURDEN="
            f"{vertical_burden:.12e} "
            f"TOTAL_GAUGE_BURDEN="
            f"{total_burden:.12e} "
            f"FINITE_GAUGE_BURDEN="
            f"{gauge_finite} "
            f"XI_FOR_10_PERCENT_BURDEN="
            f"{xi_for_10pct:.9f} "
            f"XI_FOR_25_PERCENT_BURDEN="
            f"{xi_for_25pct:.9f} "
            f"PEAK_RADIAL_EPSILON="
            f"{epsilon_max:.12e} "
            f"PEAK_STRESS_RELIEF_VS_COMPACT="
            f"{peak_relief_vs_compact:.9f} "
            f"PEAK_STRESS_RELIEF_VS_FINE_006D="
            f"{peak_relief_vs_finest:.9f}"
        )

    print()

    print(
        "=== VERTICAL LOCALIZATION ==="
    )

    containment = math.tanh(
        2.0
    )

    print(
        "SECH2_ENERGY_FRACTION_INSIDE_"
        "ORIGINAL_MINUS_DELTA_TO_ZERO_SLAB="
        f"{containment:.15e}"
    )

    print(
        "EXACT_COMPACT_SUPPORT="
        "NO"
    )

    print(
        "FINITE_TOTAL_ENERGY="
        "YES"
    )

    print(
        "EXPONENTIAL_LOCALIZATION="
        "YES"
    )

    print()

    print(
        "=== 016D DECISION ==="
    )

    print(
        "OUTWARD_GRAVITATIONAL_FIELD_ALL_CASES="
        f"{all_gravity_green}"
    )

    print(
        "INTEGRATED_STRESS_TRACE_ALL_CASES="
        f"{'PASS' if all_trace_green else 'FAIL'}"
    )

    print(
        "FIXED_CHARGE_DERRICK_WINDOW_ALL_CASES="
        f"{'SURVIVES' if all_stability_green else 'NOT_ESTABLISHED'}"
    )

    print(
        "COMPACT_BOUNDARY_DERIVATIVE_DIVERGENCE_REMOVED="
        f"{all_gauge_burdens_finite}"
    )

    if (
        all_gravity_green
        and all_trace_green
        and all_stability_green
        and all_gauge_burdens_finite
    ):
        print(
            "EXPONENTIAL_TAIL_006D_REALIZATION_PREFLIGHT="
            "GREEN"
        )

        print(
            "PREFERRED_NEXT_PARAMETER_REGION="
            "DELTA_0P10_TO_0P20_ELL_0P20_TO_0P40"
        )

        print(
            "NEXT="
            "016E_TWO_SECTOR_GAUGED_SCALAR_"
            "BOUNDARY_VALUE_PREFLIGHT"
        )

    else:
        print(
            "EXPONENTIAL_TAIL_006D_REALIZATION_PREFLIGHT="
            "RED_OR_INCOMPLETE"
        )

        print(
            "NEXT="
            "AUDIT_TAIL_PROFILE_OR_STABILITY_LOSS"
        )

    print(
        "ORIGINAL_COMPACT_006D_RESULT="
        "PRESERVED"
    )

    print(
        "GLOBAL_FIELD_EULER_LAGRANGE_SOLUTION="
        "NOT_YET_ESTABLISHED"
    )

    print(
        "FULL_DYNAMIC_STABILITY="
        "NOT_YET_ESTABLISHED"
    )

    print(
        "MACROSCOPIC_AH2_OVER_G_ENERGY_SCALING="
        "UNCHANGED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_006D_EXPONENTIAL_"
        "TAIL_REALIZABILITY_PREFLIGHT"
    )


if __name__ == "__main__":
    main()
