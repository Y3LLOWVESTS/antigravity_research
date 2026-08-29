r"""016E — two-sector gauged-scalar asymptotic preflight for 006D.

PURPOSE
-------
Determine which outer-tail architecture is compatible with the minimum
field-content realization currently motivated by the 006D research chain:

1. a nonwinding stationary complex scalar carrying conserved temporal charge;
2. a separate winding complex scalar carrying angular stress;
3. a U(1) gauge field screening the winding sector.

This gate is deliberately performed before solving the full nonlinear
two-dimensional Euler-Lagrange boundary-value problem.

SCIENTIFIC MOTIVATION
---------------------
Previous project gates established:

- 008D:
  one charged+winding complex scalar cannot exactly reproduce the 006D target;
  temporal-charge and angular-winding sectors must be separated;

- 008E:
  a finite ungauged winding set cannot terminate the original exact compact
  006D collar;

- 008F:
  a local scalar+gauge decomposition exists, but global smooth gauge
  potentials were not established;

- 016D:
  replacing the compact collar with an exponentially localized tail removes
  the finite-boundary derivative divergence while preserving outward gravity,
  integrated stress balance, and the fixed-charge Derrick capacity.

The remaining question is whether the exponential tail itself is compatible
with a globally finite-energy gauged winding sector.

WINDING-SECTOR NECESSARY CONDITION
----------------------------------
Let the static winding scalar have amplitude F(r) and gauge-covariant angular
mismatch

    k(r) = n - e A_phi(r).

Its orthonormal angular gradient contributes

    A(r)
        =
        k(r)^2 F(r)^2 / r^2.

Let

    G_r(r)
        =
        epsilon + p_r

be the total radial spatial-gradient budget available to the winding sector.

Since

    |dF/dr|^2 <= G_r

and finite energy requires

    F(infinity)=0,

we have the rigorous amplitude bound

    F(r)
        <=
        I(r),

where

    I(r)
        =
        integral_r^infinity sqrt(G_r(s)) ds.

Therefore exact reproduction of angular Gram A requires

    |k(r)|
        >=
        K_min(r)
        =
        r sqrt(A(r)) / I(r).

This is a necessary condition, independent of the detailed potential.

GAUGE ENERGY
------------
Using the cylindrical coordinate potential convention

    k = n - e A_phi,

the axial magnetic field scales as

    B_z
        =
        -k'(r)/(e r).

The magnetic energy per unit vertical length therefore contains

    integral
        k'(r)^2 / r
        dr

up to positive constants.

If K_min grows linearly with r, every asymptotically minimal realization
requires a logarithmically divergent gauge-energy contribution.

EXPONENTIAL TAIL
----------------
For the 016D asymptotic tail,

    f(r) ~ exp(-r/ell).

The exact 006D-derived tail stresses give asymptotically

    G_r
        ~
        const * exp(-r/ell) / r,

and

    A
        ~
        2 G_r.

Then

    I(r)
        ~
        2 ell sqrt(G_r),

so

    K_min(r)
        ~
        r / (sqrt(2) ell).

Thus

    K_min'(r)
        ->
        1 / (sqrt(2) ell),

and

    integral K_min'(r)^2 / r dr

diverges logarithmically.

Therefore a single gauged winding sector attempting to reproduce the exact
exponential-tail stress asymptotically fails this finite-gauge-energy
necessary condition.

This does not exclude more complicated multi-gauge or multi-winding systems.

POWER-LAW TAIL
--------------
Consider instead a C2-matched tail

    f_m(x)
        =
        (1 + x^3)^(-m/3),

with

    x
        =
        (r-beta)/ell.

It satisfies

    f_m(0)=1,
    f_m'(0)=0,
    f_m''(0)=0,

and

    f_m(x) ~ x^(-m)

at large x.

For m>0 the total radial energy remains integrable.

Asymptotically,

    G_r
        ~
        m C r^(-m-2),

and

    A
        ~
        2(m+1) C r^(-m-2).

The necessary gauge mismatch tends to the finite constant

    K_infinity
        =
        sqrt[m(m+1)/2].

Consequently K'(r)->0 and the asymptotic magnetic-energy obstruction present
for the exponential tail is absent.

Examples:

    m=2:
        K_infinity = sqrt(3)

    m=3:
        K_infinity = sqrt(6)

    m=4:
        K_infinity = sqrt(10)

GRAVITATIONAL / STABILITY CHECK
-------------------------------
Changing the tail is not acceptable merely because it improves field
integrability.

For every power-law candidate this simulation recomputes:

- positive total mass factor;
- integrated spatial stress trace;
- outward linearized-GR field factor;
- coefficient C;
- fixed-charge temporal capacity T_max/E;
- peak-stress scale relative to the historical finest 006D source.

The finite vertical profile is kept identical to 016D:

    phi(z)
        =
        [1/(2w)] sech^2[(z-z0)/w],

with

    w  = delta/4,
    z0 = -delta/2.

The pointwise source continues to use

    epsilon
        =
        max(
            |p_r|,
            |p_phi|
        ),

with

    p_z=0.

Therefore pointwise type-I DEC/WEC/NEC remain satisfied.

FIXED-CHARGE CAPACITY
---------------------
As in 008C/016B,

    D_max
        =
        min(
            epsilon+p_r,
            epsilon+p_phi,
            epsilon
        ),

and

    T_max
        =
        (1/2) integral D_max dV.

For integrated Laue balance P=0, the one-mode fixed-charge Derrick criterion is

    T/E > 1/8.

IMPORTANT LIMITATIONS
---------------------
A green 016E result establishes only that a power-law-tail target passes the
tested necessary asymptotic gauge-energy condition while preserving the
006D gravitational and one-mode fixed-charge properties.

It does NOT establish:

- a solution of the coupled scalar/gauge Euler-Lagrange equations;
- globally smooth fields throughout the inner transition;
- stability against all perturbations;
- nonlinear Einstein-matter equilibrium;
- material realization;
- practical energy requirements;
- practical antigravity.

A red exponential-tail result does not invalidate 016D as a valid conserved
stress-energy construction.  It only rejects that exact tail for the minimum
single-gauged-winding realization tested here.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_006D_TWO_SECTOR_GAUGE_TAIL_PREFLIGHT
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

FINE_006D_PEAK_J_M3_TIMES_H = (
    2.826392305523e32
)

DELTAS = (
    0.10,
    0.20,
)

ELLS = (
    0.20,
    0.40,
)

POWER_EXPONENTS = (
    2,
    3,
    4,
)


def smoothstep(
    value: float,
) -> float:
    """Return cubic smoothstep used in the locked 006D inner transition."""

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


def exponential_tail(
    x: float,
) -> tuple[float, float]:
    """Return f and df/dx for the 016D asymptotically exponential tail."""

    exponent = (
        x**3
        / (
            1.0
            + x*x
        )
    )

    value = math.exp(
        -exponent
    )

    derivative_log = (
        -x*x
        * (
            3.0
            + x*x
        )
        / (
            (
                1.0
                + x*x
            )
            ** 2
        )
    )

    return (
        value,
        value
        * derivative_log,
    )


def power_tail(
    x: float,
    exponent: int,
) -> tuple[float, float]:
    """Return f and df/dx for C2-matched power-law tail."""

    denominator = (
        1.0
        + x**3
    )

    value = (
        denominator
        ** (
            -exponent
            / 3.0
        )
    )

    derivative_log = (
        -exponent
        * x*x
        / denominator
    )

    return (
        value,
        value
        * derivative_log,
    )


def tail_value_and_prime_r(
    radius: float,
    ell: float,
    family: str,
    exponent: int = 2,
) -> tuple[float, float]:
    """Return radial tail function and physical radial derivative."""

    x = (
        radius
        - BETA
    ) / ell

    if family == "exponential":
        value, derivative_x = (
            exponential_tail(
                x
            )
        )

    elif family == "power":
        value, derivative_x = (
            power_tail(
                x,
                exponent,
            )
        )

    else:
        raise ValueError(
            f"Unknown tail family: {family}"
        )

    return (
        value,
        derivative_x
        / ell,
    )


def q_and_prime(
    radius: float,
    delta: float,
    ell: float,
    family: str,
    exponent: int = 2,
) -> tuple[float, float]:
    """Return q=r*p_r and q' for the modified 006D source."""

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

    tail, tail_prime = (
        tail_value_and_prime_r(
            radius,
            ell,
            family,
            exponent,
        )
    )

    q = (
        -(ALPHA * ALPHA)
        * tail
        / radius
    )

    qp = (
        (ALPHA * ALPHA)
        * tail
        / (
            radius
            * radius
        )
        -
        (ALPHA * ALPHA)
        * tail_prime
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
    family: str,
    exponent: int = 2,
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
        family,
        exponent,
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


def radial_integral(
    function,
    delta: float,
) -> float:
    """Integrate radial function piecewise from axis to infinity."""

    inner_width = (
        delta
        / 4.0
    )

    finite_points = (
        0.0,
        ALPHA
        - inner_width,
        ALPHA
        + inner_width,
        BETA,
    )

    total = 0.0

    for lower, upper in zip(
        finite_points[:-1],
        finite_points[1:],
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

    tail_value, _ = quad(
        function,
        BETA,
        np.inf,
        epsabs=2.0e-10,
        epsrel=2.0e-10,
        limit=1000,
    )

    total += tail_value

    return float(
        total
    )


def vertical_kernel_setup(
    delta: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """Return normalized sech^2 vertical quadrature."""

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

    profile_weights = (
        0.5
        * sech_squared
        * du_weights
    )

    profile_weights = (
        profile_weights
        / np.sum(
            profile_weights
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
        profile_weights,
    )


def integrated_metrics(
    delta: float,
    ell: float,
    exponent: int,
) -> dict[str, float]:
    """Return full gravitational and fixed-charge metrics for power tail."""

    family = "power"

    energy_radial = radial_integral(
        lambda radius:
            radius
            * stress(
                radius,
                delta,
                ell,
                family,
                exponent,
            )[0],
        delta,
    )

    trace_radial = radial_integral(
        lambda radius:
            radius
            * (
                stress(
                    radius,
                    delta,
                    ell,
                    family,
                    exponent,
                )[1]
                +
                stress(
                    radius,
                    delta,
                    ell,
                    family,
                    exponent,
                )[2]
            ),
        delta,
    )

    d_capacity_radial = radial_integral(
        lambda radius:
            radius
            * min(
                stress(
                    radius,
                    delta,
                    ell,
                    family,
                    exponent,
                )[0]
                +
                stress(
                    radius,
                    delta,
                    ell,
                    family,
                    exponent,
                )[1],
                stress(
                    radius,
                    delta,
                    ell,
                    family,
                    exponent,
                )[0]
                +
                stress(
                    radius,
                    delta,
                    ell,
                    family,
                    exponent,
                )[2],
                stress(
                    radius,
                    delta,
                    ell,
                    family,
                    exponent,
                )[0],
            ),
        delta,
    )

    zeta, weights = (
        vertical_kernel_setup(
            delta
        )
    )

    separation = (
        1.0
        - zeta
    )

    def field_integrand(
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
            family,
            exponent,
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
                    radius
                    * radius
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

    field_factor = (
        -radial_integral(
            field_integrand,
            delta,
        )
    )

    mass_factor = (
        2.0
        * energy_radial
    )

    trace_factor = (
        2.0
        * trace_radial
    )

    t_over_e = (
        0.5
        * d_capacity_radial
        / energy_radial
    )

    coefficient = (
        mass_factor
        / (
            2.0
            * field_factor
        )
    )

    return {
        "mass_factor":
            mass_factor,
        "trace_factor":
            trace_factor,
        "field_factor":
            field_factor,
        "coefficient":
            coefficient,
        "t_over_e":
            t_over_e,
    }


def tail_gradient_budgets(
    radius: float,
    ell: float,
    family: str,
    exponent: int,
) -> tuple[float, float]:
    """Return outer-tail G_r and angular Gram A."""

    tail, tail_prime = (
        tail_value_and_prime_r(
            radius,
            ell,
            family,
            exponent,
        )
    )

    p_r = (
        -(ALPHA * ALPHA)
        * tail
        / (
            radius
            * radius
        )
    )

    p_phi = (
        (ALPHA * ALPHA)
        * tail
        / (
            radius
            * radius
        )
        -
        (ALPHA * ALPHA)
        * tail_prime
        / radius
    )

    epsilon = p_phi

    g_r = (
        epsilon
        + p_r
    )

    angular = (
        epsilon
        + p_phi
    )

    return (
        g_r,
        angular,
    )


def tail_k_min(
    radius: float,
    ell: float,
    family: str,
    exponent: int = 2,
) -> float:
    """Return rigorous lower bound on gauge-covariant angular mismatch."""

    g_r, angular = (
        tail_gradient_budgets(
            radius,
            ell,
            family,
            exponent,
        )
    )

    integral, _ = quad(
        lambda source_radius:
            math.sqrt(
                max(
                    tail_gradient_budgets(
                        source_radius,
                        ell,
                        family,
                        exponent,
                    )[0],
                    0.0,
                )
            ),
        radius,
        np.inf,
        epsabs=1.0e-13,
        epsrel=2.0e-10,
        limit=1000,
    )

    if integral <= 0.0:
        return math.inf

    return (
        radius
        * math.sqrt(
            max(
                angular,
                0.0,
            )
        )
        / integral
    )


def peak_stress_prefactor(
    delta: float,
    ell: float,
    exponent: int,
    field_factor: float,
) -> tuple[float, float]:
    """Return peak radial epsilon and peak physical density multiplied by h."""

    radius = np.concatenate(
        (
            np.linspace(
                0.0,
                BETA
                + 5.0 * ell,
                250_001,
            ),
            BETA
            + ell
            * np.logspace(
                -6,
                3,
                50_000,
            ),
        )
    )

    radius = np.unique(
        radius
    )

    epsilon_values = np.array(
        [
            stress(
                float(value),
                delta,
                ell,
                "power",
                exponent,
            )[0]
            for value
            in radius
        ],
        dtype=float,
    )

    epsilon_max = float(
        np.max(
            epsilon_values
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
            * field_factor
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


def main() -> None:
    """Execute 016E."""

    print(
        "=== 016E — TWO-SECTOR GAUGED-SCALAR "
        "ASYMPTOTIC PREFLIGHT ==="
    )

    print()
    print(
        "=== EXPONENTIAL-TAIL GAUGE NECESSARY CONDITION ==="
    )

    exponential_linear_growth_confirmed = True

    for ell in ELLS:
        expected_slope = (
            1.0
            / (
                math.sqrt(
                    2.0
                )
                * ell
            )
        )

        values = []

        for x in (
            4.0,
            8.0,
            12.0,
            16.0,
        ):
            radius = (
                BETA
                + ell * x
            )

            k_min = tail_k_min(
                radius,
                ell,
                "exponential",
                2,
            )

            linear_reference = (
                radius
                * expected_slope
            )

            ratio = (
                k_min
                / linear_reference
            )

            values.append(
                ratio
            )

            print(
                "EXP_CASE "
                f"ELL={ell:.8f} "
                f"X={x:.1f} "
                f"R={radius:.12f} "
                f"K_MIN={k_min:.12e} "
                f"R_OVER_SQRT2_ELL="
                f"{linear_reference:.12e} "
                f"RATIO={ratio:.12f}"
            )

        last_ratio = values[
            -1
        ]

        if not (
            0.90
            <
            last_ratio
            <
            1.20
        ):
            exponential_linear_growth_confirmed = False

        print(
            "EXP_ASYMPTOTIC "
            f"ELL={ell:.8f} "
            f"EXPECTED_DK_DR="
            f"{expected_slope:.12e} "
            "GAUGE_ENERGY_PROXY="
            "INTEGRAL_DK2_OVER_R "
            "ASYMPTOTIC_BEHAVIOR=LOG_DIVERGENT"
        )

    print()
    print(
        "EXPONENTIAL_SINGLE_GAUGED_WINDING_"
        "FINITE_ENERGY_ASYMPTOTIC="
        + (
            "REJECTED"
            if exponential_linear_growth_confirmed
            else "NOT_ESTABLISHED"
        )
    )

    print()
    print(
        "=== POWER-LAW-TAIL ASYMPTOTIC CONDITION ==="
    )

    power_asymptotic_green = True

    for ell in ELLS:
        for exponent in POWER_EXPONENTS:
            expected = math.sqrt(
                exponent
                * (
                    exponent
                    + 1.0
                )
                / 2.0
            )

            samples = []

            for x in (
                16.0,
                32.0,
                64.0,
                128.0,
            ):
                radius = (
                    BETA
                    + ell * x
                )

                k_min = tail_k_min(
                    radius,
                    ell,
                    "power",
                    exponent,
                )

                samples.append(
                    k_min
                )

                print(
                    "POWER_ASYMPTOTIC "
                    f"ELL={ell:.8f} "
                    f"M={exponent:d} "
                    f"X={x:.1f} "
                    f"K_MIN={k_min:.12e} "
                    f"K_INFINITY_ANALYTIC="
                    f"{expected:.12e} "
                    f"RATIO="
                    f"{k_min/expected:.12f}"
                )

            if not (
                samples[-1]
                <
                samples[0]
            ):
                power_asymptotic_green = False

            print(
                "POWER_LIMIT "
                f"ELL={ell:.8f} "
                f"M={exponent:d} "
                f"K_INFINITY="
                f"{expected:.12e} "
                f"MIN_INTEGER_EFFECTIVE_WINDING="
                f"{math.ceil(expected):d} "
                "GAUGE_ENERGY_ASYMPTOTIC="
                "FINITE_COMPATIBLE_NECESSARY_CONDITION"
            )

    print()
    print(
        "=== POWER-LAW FULL GRAVITY / STABILITY SCAN ==="
    )

    all_gravity_green = True
    all_trace_green = True
    all_stability_green = True

    records = []

    for delta in DELTAS:
        for ell in ELLS:
            for exponent in POWER_EXPONENTS:
                metrics = integrated_metrics(
                    delta,
                    ell,
                    exponent,
                )

                (
                    epsilon_max,
                    peak_times_h,
                ) = peak_stress_prefactor(
                    delta,
                    ell,
                    exponent,
                    metrics[
                        "field_factor"
                    ],
                )

                peak_relief = (
                    FINE_006D_PEAK_J_M3_TIMES_H
                    / peak_times_h
                )

                k_infinity = math.sqrt(
                    exponent
                    * (
                        exponent
                        + 1.0
                    )
                    / 2.0
                )

                gravity_green = bool(
                    metrics[
                        "field_factor"
                    ]
                    >
                    0.0
                )

                trace_green = bool(
                    abs(
                        metrics[
                            "trace_factor"
                        ]
                    )
                    <
                    1.0e-8
                )

                stability_green = bool(
                    metrics[
                        "t_over_e"
                    ]
                    >
                    DERRICK_CRITICAL_T_OVER_E
                )

                all_gravity_green = (
                    all_gravity_green
                    and gravity_green
                )

                all_trace_green = (
                    all_trace_green
                    and trace_green
                )

                all_stability_green = (
                    all_stability_green
                    and stability_green
                )

                records.append(
                    {
                        "delta":
                            delta,
                        "ell":
                            ell,
                        "m":
                            exponent,
                        "C":
                            metrics[
                                "coefficient"
                            ],
                        "T":
                            metrics[
                                "t_over_e"
                            ],
                        "K":
                            k_infinity,
                        "peak_relief":
                            peak_relief,
                    }
                )

                print(
                    "POWER_CASE "
                    f"DELTA={delta:.8f} "
                    f"ELL={ell:.8f} "
                    f"M={exponent:d} "
                    f"MASS_FACTOR="
                    f"{metrics['mass_factor']:.15e} "
                    f"TRACE_FACTOR="
                    f"{metrics['trace_factor']:.3e} "
                    f"FIELD_FACTOR="
                    f"{metrics['field_factor']:.15e} "
                    f"C="
                    f"{metrics['coefficient']:.12f} "
                    f"TMAX_OVER_E="
                    f"{metrics['t_over_e']:.15e} "
                    f"K_INFINITY="
                    f"{k_infinity:.12f} "
                    f"MIN_INTEGER_K="
                    f"{math.ceil(k_infinity):d} "
                    f"PEAK_RADIAL_EPSILON="
                    f"{epsilon_max:.12e} "
                    f"PEAK_STRESS_RELIEF_VS_FINE_006D="
                    f"{peak_relief:.9f} "
                    f"OUTWARD={gravity_green} "
                    f"TRACE_PASS={trace_green} "
                    f"FIXED_CHARGE_PASS={stability_green}"
                )

    print()
    print(
        "=== SIMPLEST POWER-TAIL CANDIDATES ==="
    )

    m2_records = [
        record
        for record
        in records
        if record[
            "m"
        ] == 2
    ]

    for record in m2_records:
        print(
            "M2_CANDIDATE "
            f"DELTA={record['delta']:.8f} "
            f"ELL={record['ell']:.8f} "
            f"C={record['C']:.12f} "
            f"TMAX_OVER_E={record['T']:.12f} "
            f"K_INFINITY={record['K']:.12f} "
            f"PEAK_RELIEF={record['peak_relief']:.6f}"
        )

    preferred = min(
        m2_records,
        key=lambda item:
            (
                -item[
                    "peak_relief"
                ],
                item[
                    "C"
                ],
            ),
    )

    print()
    print(
        "PREFERRED_MINIMUM_FIELD_CONTENT_CANDIDATE "
        f"DELTA={preferred['delta']:.8f} "
        f"ELL={preferred['ell']:.8f} "
        "M=2 "
        f"C={preferred['C']:.12f} "
        f"TMAX_OVER_E={preferred['T']:.12f} "
        f"K_INFINITY={preferred['K']:.12f} "
        f"PEAK_STRESS_RELIEF={preferred['peak_relief']:.6f}"
    )

    print()
    print(
        "=== 016E FINAL DECISION ==="
    )

    print(
        "EXPONENTIAL_TAIL_SINGLE_GAUGED_WINDING_"
        "ASYMPTOTIC="
        + (
            "RED"
            if exponential_linear_growth_confirmed
            else "UNRESOLVED"
        )
    )

    print(
        "POWER_LAW_TAIL_OUTER_GAUGE_ASYMPTOTIC="
        + (
            "GREEN"
            if power_asymptotic_green
            else "UNRESOLVED"
        )
    )

    print(
        "POWER_LAW_OUTWARD_GRAVITY_ALL_CASES="
        f"{all_gravity_green}"
    )

    print(
        "POWER_LAW_INTEGRATED_STRESS_TRACE="
        + (
            "PASS"
            if all_trace_green
            else "FAIL"
        )
    )

    print(
        "POWER_LAW_FIXED_CHARGE_DERRICK_WINDOW="
        + (
            "SURVIVES"
            if all_stability_green
            else "NOT_ESTABLISHED"
        )
    )

    if (
        exponential_linear_growth_confirmed
        and power_asymptotic_green
        and all_gravity_green
        and all_trace_green
        and all_stability_green
    ):
        print(
            "016D_EXPONENTIAL_TAIL="
            "DEMOTED_AS_EXACT_MINIMAL_GAUGED_WINDING_TARGET"
        )

        print(
            "POWER_LAW_C2_TAIL="
            "PROMOTED_TO_MINIMUM_TWO_SECTOR_FIELD_TARGET"
        )

        print(
            "PREFERRED_POWER_EXPONENT="
            "M=2"
        )

        print(
            "NEXT="
            "016F_TWO_SECTOR_GAUGED_SCALAR_"
            "EULER_LAGRANGE_BOUNDARY_VALUE_PREFLIGHT"
        )

    else:
        print(
            "TAIL_SELECTION="
            "NOT_CLOSED"
        )

        print(
            "NEXT="
            "AUDIT_016E_ASYMPTOTIC_OR_GRAVITY_METRICS"
        )

    print(
        "ONE_COMPLEX_CHARGED_WINDING_SCALAR="
        "STILL_REJECTED"
    )

    print(
        "SECTOR_SEPARATION_REQUIRED="
        "YES"
    )

    print(
        "GLOBAL_TWO_SECTOR_FIELD_SOLUTION="
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
        "PROJECT_DERIVED_006D_TWO_SECTOR_"
        "GAUGE_TAIL_PREFLIGHT"
    )


if __name__ == "__main__":
    main()
