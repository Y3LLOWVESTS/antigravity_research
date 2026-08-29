r"""016F — charge/winding coexistence and inner-transition optimization.

PURPOSE
-------
Test whether the fixed-charge stabilizer and the gauged winding sector
required by the current 006D realization program can coexist inside the same
stress-energy budget.

This is the cheapest decisive prerequisite before attempting the full
two-sector gauged-scalar Euler-Lagrange boundary-value problem.

SCIENTIFIC STATE ENTERING THIS GATE
-----------------------------------
The research chain currently gives:

006D:
    finite positive-energy locally conserved linearized-GR repulsive source.

008B:
    local canonical-scalar Gram representability.

008C:
    sufficient temporal kinetic capacity exists for one fixed-charge
    Derrick mode.

008D:
    one charged+winding complex scalar is insufficient;
    temporal and angular sectors must be separated.

008E:
    finite ungauged winding fails at the exact compact termination.

008F:
    local gauge takeover exists, but no global gauge solution was proved.

016A:
    thicker 006D sources reduce peak stress enormously.

016B:
    thick sources retain the fixed-charge/gauge budget.

016C:
    the simplest one/two electrostatic Maxwell realizations are globally
    obstructed.

016D:
    smooth noncompact tails preserve the gravitational result.

016E:
    exponential tails are unsuitable for the minimum gauged winding sector,
    while C2 power-law tails pass the tested asymptotic finite-gauge-energy
    condition.

016E nevertheless evaluated winding integrability and fixed-charge capacity
mostly as separate prerequisites.

016F couples those requirements.

TARGET FIELD CONTENT
--------------------
The minimal architecture remains:

Sector Q:
    stationary nonwinding complex scalar carrying conserved temporal charge.

Sector W:
    static winding complex scalar carrying angular gradient stress.

Gauge sector:
    U(1) field controlling the covariant winding mismatch

        k = n - e A_phi.

The sectors are separated so the forbidden one-field T_tphi cross term is
avoided.

TEMPORAL-KINETIC ALLOCATION
---------------------------
For a diagonal target stress,

    D_max
        =
        min(
            epsilon+p_r,
            epsilon+p_phi,
            epsilon+p_z
        ).

Since p_z=0,

    D_max
        =
        min(
            epsilon+p_r,
            epsilon+p_phi,
            epsilon
        ).

Choose a simple proportional charge allocation

    D(r)
        =
        eta D_max(r).

The integrated temporal kinetic fraction is

    T/E
        =
        eta (T_max/E).

Rather than sitting directly at the marginal Derrick threshold 1/8, this gate
demands

    TARGET_T_OVER_E = 0.14.

For approximately zero integrated pressure,

    E_Q''(1)/E
        =
        24(T/E)-3,

so this target gives

    E_Q''(1)/E = 0.36 > 0.

This is still only one-mode Derrick stability.

REMAINING WINDING GRAM BUDGET
-----------------------------
After allocating D,

    G_r
        =
        epsilon+p_r-D

and

    A
        =
        epsilon+p_phi-D

are respectively the remaining radial and angular canonical spatial Gram
budgets.

INNER TURN-ON NECESSARY CONDITION
---------------------------------
The winding amplitude must vanish in the inner zero-angular-stress region.

Let r_minus be the beginning of the inner transition.

Since

    |F'|^2 <= G_r,

any field grown from

    F(r_minus)=0

obeys

    F(r)
        <=
        I_inner(r),

where

    I_inner(r)
        =
        integral_(r_minus)^r sqrt(G_r(s)) ds.

Exact reproduction of angular Gram A requires

    |k(r)| F(r)
        =
        r sqrt(A(r)).

Therefore

    |k(r)|
        >=
        K_inner(r)

with

    K_inner(r)
        =
        r sqrt(A(r))
        /
        I_inner(r).

This is a necessary pointwise condition.

OUTER DECAY NECESSARY CONDITION
-------------------------------
Finite energy requires the winding amplitude to decay to zero.

Therefore

    F(r)
        <=
        I_outer(r),

where

    I_outer(r)
        =
        integral_r^infinity sqrt(G_r(s)) ds.

Hence

    |k(r)|
        >=
        K_outer(r)

with

    K_outer(r)
        =
        r sqrt(A(r))
        /
        I_outer(r).

The global minimum mismatch requirement is therefore at least

    K_required
        =
        max(
            max K_inner,
            max K_outer
        ).

INTEGER WINDING INTERPRETATION
------------------------------
For the simplest non-overshooting gauge ansatz, where the gauge-covariant
mismatch never needs to exceed the bare integer winding magnitude,

    n >= ceil(K_required).

This integer is NOT a universal theorem.

A gauge field can in principle overshoot the bare winding value, and more
general multi-field configurations may reduce this requirement.

The quantity K_required itself is the stronger kinematic result.

INNER-TRANSITION AUGMENTATION
-----------------------------
The original 006D construction tied the inner smoothing half-width to

    delta/4.

That choice optimized compactness and energy, not field integrability.

016F therefore frees the dimensionless inner half-width W:

    r_minus = alpha-W
    r_plus  = alpha+W.

The same cubic smoothstep interpolation is retained, so

    q = r p_r

and

    p_phi = dq/dr

continue to give exact flat-background radial conservation.

POWER-LAW OUTER TAIL
--------------------
Use the 016E-promoted minimum-complexity tail

    m = 2

with

    f(x)
        =
        (1+x^3)^(-2/3),

    x
        =
        (r-beta)/ell.

The vertical profile remains the normalized sech^2 profile from 016D/016E.

SCAN
----
Fix

    delta = 0.20

and scan:

    inner half-width W:
        0.05
        0.10
        0.20
        0.30
        0.40
        0.50
        0.60
        0.80
        1.00
        1.20

    tail length ell:
        0.40
        0.60
        0.80
        1.00
        1.20
        1.60

For every candidate recompute:

- total energy;
- integrated stress trace;
- outward field;
- coefficient C;
- maximum fixed-charge capacity;
- required charge fraction eta;
- positive fixed-charge Derrick curvature;
- inner winding mismatch bound;
- outer winding mismatch bound;
- conservative integer winding estimate;
- peak physical stress relative to the original fine 006D source.

INTERPRETATION
--------------
A green result means there exists a finite kinematic budget for simultaneous
charge stabilization and winding/gauge stress support in this explicit
allocation.

It does NOT prove:

- a solution of the Euler-Lagrange equations;
- existence of a single microscopic potential;
- absence of gauge overshoot;
- stability of high-winding configurations;
- stability against vortex splitting;
- full perturbative stability;
- nonlinear Einstein-matter equilibrium;
- practical energy scaling.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_006D_CHARGE_WINDING_COEXISTENCE_OPTIMIZATION_GATE
"""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import cumulative_trapezoid
from scipy.integrate import quad


G = 6.67430e-11
C_LIGHT = 299_792_458.0
G_STANDARD = 9.80665

ALPHA = 1.437500564637
BETA = 4.701437405300

DELTA = 0.20
POWER_EXPONENT = 2

TARGET_T_OVER_E = 0.14

FINE_006D_PEAK_J_M3_TIMES_H = (
    2.826392305523e32
)

INNER_HALF_WIDTHS = (
    0.05,
    0.10,
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.80,
    1.00,
    1.20,
)

TAIL_LENGTHS = (
    0.40,
    0.60,
    0.80,
    1.00,
    1.20,
    1.60,
)


def smoothstep(
    value: np.ndarray | float,
) -> np.ndarray | float:
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
    value: np.ndarray | float,
) -> np.ndarray | float:
    """Return derivative of cubic smoothstep."""

    return (
        6.0
        * value
        * (
            1.0
            - value
        )
    )


def power_tail(
    x: np.ndarray | float,
) -> tuple[
    np.ndarray | float,
    np.ndarray | float,
]:
    """Return m=2 C2 power tail and derivative with respect to x."""

    denominator = (
        1.0
        + x**3
    )

    value = (
        denominator
        ** (
            -POWER_EXPONENT
            / 3.0
        )
    )

    derivative_log = (
        -POWER_EXPONENT
        * x**2
        / denominator
    )

    return (
        value,
        value
        * derivative_log,
    )


def q_and_prime(
    radius: float,
    inner_width: float,
    ell: float,
) -> tuple[float, float]:
    """Return q=r*p_r and dq/dr."""

    r_minus = (
        ALPHA
        - inner_width
    )

    r_plus = (
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

    if radius < r_minus:
        return (
            q_core,
            qp_core,
        )

    if radius <= r_plus:
        u = (
            (
                radius
                - r_minus
            )
            / (
                2.0
                * inner_width
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
                2.0
                * inner_width
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
            float(q),
            float(qp),
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

    tail, derivative_x = (
        power_tail(
            x
        )
    )

    derivative_r = (
        derivative_x
        / ell
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
        * derivative_r
        / radius
    )

    return (
        float(q),
        float(qp),
    )


def stress(
    radius: float,
    inner_width: float,
    ell: float,
) -> tuple[
    float,
    float,
    float,
]:
    """Return epsilon, p_r, and p_phi."""

    q, qp = q_and_prime(
        radius,
        inner_width,
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


def radial_integral(
    function,
    inner_width: float,
) -> float:
    """Integrate piecewise from axis to infinity."""

    points = (
        0.0,
        ALPHA
        - inner_width,
        ALPHA
        + inner_width,
        BETA,
    )

    total = 0.0

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

    tail_value, _ = quad(
        function,
        BETA,
        np.inf,
        epsabs=2.0e-10,
        epsrel=2.0e-10,
        limit=1200,
    )

    return float(
        total
        + tail_value
    )


def vertical_kernel_setup() -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """Return normalized sech^2 vertical quadrature."""

    nodes, weights = leggauss(
        128
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

    profile_weights = (
        0.5
        / np.cosh(
            u
        )**2
        * du_weights
    )

    profile_weights = (
        profile_weights
        / np.sum(
            profile_weights
        )
    )

    width = (
        DELTA
        / 4.0
    )

    center = (
        -DELTA
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


ZETA, Z_WEIGHTS = (
    vertical_kernel_setup()
)

SEPARATION = (
    1.0
    - ZETA
)


def integrated_metrics(
    inner_width: float,
    ell: float,
) -> dict[str, float]:
    """Return energy, trace, field, C, and maximum T/E."""

    energy_radial = radial_integral(
        lambda radius:
            radius
            * stress(
                radius,
                inner_width,
                ell,
            )[0],
        inner_width,
    )

    trace_radial = radial_integral(
        lambda radius:
            radius
            * (
                stress(
                    radius,
                    inner_width,
                    ell,
                )[1]
                +
                stress(
                    radius,
                    inner_width,
                    ell,
                )[2]
            ),
        inner_width,
    )

    d_capacity_radial = radial_integral(
        lambda radius:
            radius
            * max(
                0.0,
                min(
                    stress(
                        radius,
                        inner_width,
                        ell,
                    )[0]
                    +
                    stress(
                        radius,
                        inner_width,
                        ell,
                    )[1],
                    stress(
                        radius,
                        inner_width,
                        ell,
                    )[0]
                    +
                    stress(
                        radius,
                        inner_width,
                        ell,
                    )[2],
                    stress(
                        radius,
                        inner_width,
                        ell,
                    )[0],
                ),
            ),
        inner_width,
    )

    def field_integrand(
        radius: float,
    ) -> float:
        epsilon, p_r, p_phi = (
            stress(
                radius,
                inner_width,
                ell,
            )
        )

        active = (
            epsilon
            + p_r
            + p_phi
        )

        kernel = float(
            np.sum(
                Z_WEIGHTS
                * SEPARATION
                / (
                    radius
                    * radius
                    +
                    SEPARATION
                    * SEPARATION
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
            inner_width,
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

    tmax_over_e = (
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
        "energy_radial":
            energy_radial,
        "mass_factor":
            mass_factor,
        "trace_factor":
            trace_factor,
        "field_factor":
            field_factor,
        "coefficient":
            coefficient,
        "tmax_over_e":
            tmax_over_e,
    }


def build_inner_grid(
    inner_width: float,
) -> np.ndarray:
    """Return dense grid resolving the inner stress transition."""

    return np.linspace(
        ALPHA
        - inner_width,
        ALPHA
        + inner_width,
        60_001,
    )


def build_tail_grid(
    ell: float,
) -> np.ndarray:
    """Return mixed linear/log grid resolving tail and asymptotics."""

    x_linear = np.linspace(
        0.0,
        8.0,
        60_000,
        endpoint=False,
    )

    x_log = np.logspace(
        math.log10(
            8.0
        ),
        5.0,
        40_000,
    )

    return (
        BETA
        +
        ell
        * np.concatenate(
            (
                x_linear,
                x_log,
            )
        )
    )


def vector_stress(
    radius: np.ndarray,
    inner_width: float,
    ell: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Vectorized stress evaluation for kinematic mismatch integrals."""

    epsilon = np.empty_like(
        radius
    )

    p_r = np.empty_like(
        radius
    )

    p_phi = np.empty_like(
        radius
    )

    for index, value in enumerate(
        radius
    ):
        (
            epsilon[index],
            p_r[index],
            p_phi[index],
        ) = stress(
            float(value),
            inner_width,
            ell,
        )

    return (
        epsilon,
        p_r,
        p_phi,
    )


def remaining_grams(
    radius: np.ndarray,
    inner_width: float,
    ell: float,
    eta: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """Return remaining radial and angular Gram after charge allocation."""

    epsilon, p_r, p_phi = (
        vector_stress(
            radius,
            inner_width,
            ell,
        )
    )

    d_max = np.maximum(
        0.0,
        np.minimum.reduce(
            (
                epsilon
                + p_r,
                epsilon
                + p_phi,
                epsilon,
            )
        ),
    )

    temporal = (
        eta
        * d_max
    )

    gram_r = np.maximum(
        epsilon
        + p_r
        - temporal,
        0.0,
    )

    angular = np.maximum(
        epsilon
        + p_phi
        - temporal,
        0.0,
    )

    return (
        gram_r,
        angular,
    )


def inner_mismatch_bound(
    inner_width: float,
    ell: float,
    eta: float,
) -> tuple[
    float,
    float,
]:
    """Return maximum inner turn-on mismatch and its radius."""

    radius = build_inner_grid(
        inner_width
    )

    gram_r, angular = (
        remaining_grams(
            radius,
            inner_width,
            ell,
            eta,
        )
    )

    integral = cumulative_trapezoid(
        np.sqrt(
            gram_r
        ),
        radius,
        initial=0.0,
    )

    mismatch = np.zeros_like(
        radius
    )

    mask = (
        (angular > 1.0e-14)
        &
        (integral > 1.0e-14)
    )

    mismatch[mask] = (
        radius[mask]
        * np.sqrt(
            angular[mask]
        )
        / integral[mask]
    )

    index = int(
        np.argmax(
            mismatch
        )
    )

    return (
        float(
            mismatch[index]
        ),
        float(
            radius[index]
        ),
    )


def tail_mismatch_bound(
    inner_width: float,
    ell: float,
    eta: float,
) -> tuple[
    float,
    float,
    float,
]:
    """Return maximum outer mismatch, location, and asymptotic value."""

    radius = build_tail_grid(
        ell
    )

    gram_r, angular = (
        remaining_grams(
            radius,
            inner_width,
            ell,
            eta,
        )
    )

    root_gram = np.sqrt(
        gram_r
    )

    r_max = float(
        radius[-1]
    )

    asymptotic_coefficient = (
        (
            1.0
            - eta
        )
        * POWER_EXPONENT
        * ALPHA**2
        * ell**POWER_EXPONENT
    )

    remainder = (
        2.0
        / POWER_EXPONENT
        * math.sqrt(
            asymptotic_coefficient
        )
        * r_max
        ** (
            -POWER_EXPONENT
            / 2.0
        )
    )

    reversed_integral = cumulative_trapezoid(
        root_gram[::-1],
        radius[::-1],
        initial=0.0,
    )

    integral_to_infinity = (
        -reversed_integral[::-1]
        +
        remainder
    )

    mismatch = np.zeros_like(
        radius
    )

    mask = (
        (angular > 1.0e-16)
        &
        (integral_to_infinity > 1.0e-16)
    )

    mismatch[mask] = (
        radius[mask]
        * np.sqrt(
            angular[mask]
        )
        / integral_to_infinity[mask]
    )

    index = int(
        np.argmax(
            mismatch
        )
    )

    asymptotic_value = math.sqrt(
        POWER_EXPONENT
        * (
            2.0
            * (
                POWER_EXPONENT
                + 1.0
            )
            -
            eta
            * POWER_EXPONENT
        )
        / (
            4.0
            * (
                1.0
                - eta
            )
        )
    )

    return (
        float(
            mismatch[index]
        ),
        float(
            radius[index]
        ),
        asymptotic_value,
    )


def peak_stress_relief(
    inner_width: float,
    ell: float,
    field_factor: float,
) -> tuple[
    float,
    float,
]:
    """Return peak epsilon and relief relative to original fine 006D."""

    radius = np.concatenate(
        (
            np.linspace(
                0.0,
                BETA
                + 5.0 * ell,
                100_001,
            ),
            BETA
            + ell
            * np.logspace(
                -6.0,
                3.0,
                25_000,
            ),
        )
    )

    epsilon = np.array(
        [
            stress(
                float(value),
                inner_width,
                ell,
            )[0]
            for value
            in radius
        ]
    )

    epsilon_max = float(
        np.max(
            epsilon
        )
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

    vertical_peak = (
        2.0
        / DELTA
    )

    peak_times_h = (
        surface_energy
        * epsilon_max
        * vertical_peak
    )

    relief = (
        FINE_006D_PEAK_J_M3_TIMES_H
        / peak_times_h
    )

    return (
        epsilon_max,
        relief,
    )


def main() -> None:
    """Run simultaneous charge/winding coexistence scan."""

    print(
        "=== 016F — 006D CHARGE / WINDING "
        "COEXISTENCE OPTIMIZER ==="
    )

    print(
        "DELTA="
        f"{DELTA:.8f}"
    )

    print(
        "POWER_EXPONENT="
        f"{POWER_EXPONENT}"
    )

    print(
        "TARGET_T_OVER_E="
        f"{TARGET_T_OVER_E:.12f}"
    )

    print(
        "TARGET_DERRICK_CURVATURE_OVER_E="
        f"{24.0 * TARGET_T_OVER_E - 3.0:.12f}"
    )

    records: list[
        dict[str, float]
    ] = []

    for inner_width in INNER_HALF_WIDTHS:
        if (
            ALPHA
            - inner_width
            <= 0.0
        ):
            continue

        if (
            ALPHA
            + inner_width
            >= BETA
        ):
            continue

        for ell in TAIL_LENGTHS:
            metrics = integrated_metrics(
                inner_width,
                ell,
            )

            if (
                metrics[
                    "tmax_over_e"
                ]
                <= TARGET_T_OVER_E
            ):
                print(
                    "CASE "
                    f"W={inner_width:.8f} "
                    f"ELL={ell:.8f} "
                    "STATUS=INSUFFICIENT_CHARGE_CAPACITY "
                    f"TMAX_OVER_E="
                    f"{metrics['tmax_over_e']:.12f}"
                )

                continue

            eta = (
                TARGET_T_OVER_E
                / metrics[
                    "tmax_over_e"
                ]
            )

            inner_k, inner_radius = (
                inner_mismatch_bound(
                    inner_width,
                    ell,
                    eta,
                )
            )

            (
                outer_k,
                outer_radius,
                k_infinity,
            ) = tail_mismatch_bound(
                inner_width,
                ell,
                eta,
            )

            required_k = max(
                inner_k,
                outer_k,
            )

            conservative_integer = (
                math.ceil(
                    required_k
                    - 1.0e-10
                )
            )

            (
                epsilon_max,
                peak_relief,
            ) = peak_stress_relief(
                inner_width,
                ell,
                metrics[
                    "field_factor"
                ],
            )

            record = {
                "W":
                    inner_width,
                "ell":
                    ell,
                "C":
                    metrics[
                        "coefficient"
                    ],
                "Tmax":
                    metrics[
                        "tmax_over_e"
                    ],
                "eta":
                    eta,
                "inner_k":
                    inner_k,
                "inner_radius":
                    inner_radius,
                "outer_k":
                    outer_k,
                "outer_radius":
                    outer_radius,
                "k_inf":
                    k_infinity,
                "required_k":
                    required_k,
                "n":
                    float(
                        conservative_integer
                    ),
                "peak_relief":
                    peak_relief,
                "epsilon_max":
                    epsilon_max,
                "trace":
                    metrics[
                        "trace_factor"
                    ],
                "field":
                    metrics[
                        "field_factor"
                    ],
            }

            records.append(
                record
            )

            print(
                "CASE "
                f"W={inner_width:.8f} "
                f"ELL={ell:.8f} "
                f"C={metrics['coefficient']:.12f} "
                f"FIELD_FACTOR="
                f"{metrics['field_factor']:.12e} "
                f"TRACE_FACTOR="
                f"{metrics['trace_factor']:.3e} "
                f"TMAX_OVER_E="
                f"{metrics['tmax_over_e']:.12f} "
                f"ETA_FOR_TARGET_CHARGE="
                f"{eta:.12f} "
                f"INNER_K_MAX="
                f"{inner_k:.12f} "
                f"INNER_K_RADIUS="
                f"{inner_radius:.12f} "
                f"OUTER_K_MAX="
                f"{outer_k:.12f} "
                f"OUTER_K_RADIUS="
                f"{outer_radius:.12f} "
                f"K_INFINITY="
                f"{k_infinity:.12f} "
                f"K_REQUIRED="
                f"{required_k:.12f} "
                f"N_NONOVERSHOOT="
                f"{conservative_integer:d} "
                f"PEAK_STRESS_RELIEF="
                f"{peak_relief:.6f}"
            )

    print()
    print(
        "=== PARETO FRONTIER BY CONSERVATIVE INTEGER WINDING ==="
    )

    winding_values = sorted(
        {
            int(
                record[
                    "n"
                ]
            )
            for record
            in records
        }
    )

    for winding in winding_values:
        subset = [
            record
            for record
            in records
            if int(
                record[
                    "n"
                ]
            )
            == winding
        ]

        best = min(
            subset,
            key=lambda item:
                item[
                    "C"
                ],
        )

        print(
            "PARETO "
            f"N={winding:d} "
            f"W={best['W']:.8f} "
            f"ELL={best['ell']:.8f} "
            f"C={best['C']:.12f} "
            f"TMAX_OVER_E={best['Tmax']:.12f} "
            f"K_REQUIRED={best['required_k']:.12f} "
            f"PEAK_STRESS_RELIEF="
            f"{best['peak_relief']:.6f}"
        )

    low_complexity = [
        record
        for record
        in records
        if record[
            "n"
        ]
        <= 10.0
    ]

    print()
    print(
        "=== 016F DECISION ==="
    )

    if low_complexity:
        preferred = min(
            low_complexity,
            key=lambda item:
                item[
                    "C"
                ],
        )

        print(
            "FINITE_CHARGE_WINDING_COEXISTENCE_WINDOW="
            "YES_IN_TESTED_KINEMATIC_ALLOCATION"
        )

        print(
            "LOWER_COMPLEXITY_NONOVERSHOOT_TARGET_FOUND="
            "YES"
        )

        print(
            "PREFERRED_W="
            f"{preferred['W']:.12f}"
        )

        print(
            "PREFERRED_ELL="
            f"{preferred['ell']:.12f}"
        )

        print(
            "PREFERRED_C="
            f"{preferred['C']:.12f}"
        )

        print(
            "PREFERRED_TMAX_OVER_E="
            f"{preferred['Tmax']:.12f}"
        )

        print(
            "PREFERRED_REQUIRED_K="
            f"{preferred['required_k']:.12f}"
        )

        print(
            "PREFERRED_CONSERVATIVE_INTEGER_WINDING="
            f"{int(preferred['n'])}"
        )

        print(
            "PREFERRED_PEAK_STRESS_RELIEF_VS_FINE_006D="
            f"{preferred['peak_relief']:.6f}"
        )

        print(
            "NEXT="
            "016G_TWO_SECTOR_GAUGED_SCALAR_"
            "EULER_LAGRANGE_BOUNDARY_VALUE_PREFLIGHT"
        )

    else:
        preferred = min(
            records,
            key=lambda item:
                (
                    item[
                        "required_k"
                    ],
                    item[
                        "C"
                    ],
                ),
        )

        print(
            "FINITE_CHARGE_WINDING_COEXISTENCE_WINDOW="
            "YES_BUT_HIGH_MISMATCH_IN_TESTED_SCAN"
        )

        print(
            "LOWER_COMPLEXITY_NONOVERSHOOT_TARGET_FOUND="
            "NO"
        )

        print(
            "BEST_REQUIRED_K="
            f"{preferred['required_k']:.12f}"
        )

        print(
            "NEXT="
            "OPTIMIZE_INNER_TRANSITION_OR_ALLOW_"
            "CONTROLLED_GAUGE_OVERSHOOT"
        )

    print(
        "FULL_EULER_LAGRANGE_SOLUTION="
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
        "PROJECT_DERIVED_006D_CHARGE_WINDING_"
        "COEXISTENCE_OPTIMIZATION_GATE"
    )


if __name__ == "__main__":
    main()
