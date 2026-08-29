r"""016B — thick-006D fixed-charge and gauge-takeover capacity gate.

PURPOSE
-------
Determine whether the practicality-optimized thick 006D candidates identified
by Simulation 016A retain the local field-theory stabilization margins found
earlier in Simulations 008C and 008F.

016A showed that increasing the finite 006D regularization thickness from

    delta = 0.00625

to approximately

    delta = 0.10 to 0.20

raises the total gravitational energy coefficient only modestly while reducing
the peak stress by hundreds of times.

However, the previous fixed-charge and gauge-boundary calculations were
performed only on the finest delta=0.00625 source.

It would therefore be scientifically invalid to assume that their stability
budget automatically survives the thicker source.

SCIENTIFIC QUESTIONS
--------------------
1. Does the fixed-charge temporal kinetic capacity still satisfy

       T_max / E > 1/8

   at delta=0.10 and delta=0.20?

2. Does a finite outer Maxwell/gauge takeover layer remain compatible with
   positive Derrick dilation curvature?

3. How much of the outer collar can be transferred to the gauge sector before

       T_remaining / E = 1/8?

4. Does the new thick-source realization retain a substantial margin at
   30% and 35% gauge takeover?

PHYSICAL MODEL
--------------
The exact finite 006D normalized radial stress construction is reconstructed
independently from the documented q=r*p_r representation.

The source has

    p_z = 0

and

    epsilon = max(|p_r|, |p_phi|).

The normalized finite vertical bump integrates to unity, so integrated ratios
such as T/E can be computed directly from the radial surface profiles.

FIXED-CHARGE CAPACITY
---------------------
For a stationary charged canonical scalar sector, define the local temporal
kinetic capacity

    D_max
        =
        min(
            epsilon + p_r,
            epsilon + p_phi,
            epsilon + p_z
        ).

Since p_z=0,

    D_max
        =
        min(
            epsilon + p_r,
            epsilon + p_phi,
            epsilon
        ).

The maximum fixed-charge temporal contribution is

    T_max
        =
        (1/2) integral D_max dV.

Under fixed-charge dilation,

    E_Q(lambda)
        =
        lambda^3 T
        +
        K/lambda
        +
        U/lambda^3.

The second derivative at lambda=1 is

    E_Q''(1)
        =
        24 T
        -
        3 E
        -
        5 P,

where

    P
        =
        integral(
            p_r + p_phi + p_z
        ) dV.

The finite 006D source obeys integrated Laue balance,

    P approximately 0.

Therefore positive curvature requires

    T/E > 1/8.

GAUGE TAKEOVER
--------------
In the 006D outer collar,

    p_phi = epsilon

and

    p_r <= 0.

Define

    g = epsilon + p_r.

The exact local stress decomposition used by 008F is

Gauge sector:

    T_g = (g, 0, g, 0)

Residual scalar sector:

    T_s = (-p_r, p_r, -p_r, 0).

The residual scalar Gram matrix is positive semidefinite.

For a gauge takeover fraction f, the outer fraction f of the finite support
collar is assigned to this gauge sector.

Following the conservative 008F gate, all temporal fixed-charge capacity in
that gauge-assigned layer is removed.

The critical takeover fraction solves

    T_remaining(f_critical) / E = 1/8.

INDEPENDENCE / VALIDATION
-------------------------
This file does not import the original 008C or 008F implementation.

Before evaluating the new thick candidates it must independently reproduce the
historical delta=0.00625 values:

    T_max / E approximately 0.186185265139

    critical gauge fraction approximately 0.383694

    at 30% takeover:
        T/E approximately 0.1459769
        curvature/E approximately 0.50344
        gauge energy/E approximately 0.08042

This historical reproduction is a prerequisite for trusting the thick-source
extension.

APPROXIMATION LEVEL
-------------------
- static flat-background stress decomposition;
- canonical positive-sign scalar local capacity;
- fixed conserved charge under one isotropic Derrick dilation mode;
- local Maxwell/gauge stress decomposition;
- finite normalized 006D radial source;
- no global field equations solved.

LIMITATIONS
-----------
A green result does not establish:

- a global complex-scalar field;
- globally smooth gauge potentials;
- a nonlinear field-theory soliton;
- stability against all perturbation modes;
- exact nonlinear Einstein-matter equilibrium;
- practical energy scale;
- a practical antigravity device.

Its purpose is to determine whether the thick 006D architecture is worth the
much more expensive global field-equation calculation.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_006D_THICK_FIXED_CHARGE_GAUGE_CAPACITY_GATE
"""

from __future__ import annotations

import math

from scipy.integrate import quad
from scipy.optimize import brentq


ALPHA = 1.437500564637
BETA = 4.701437405300

DERRICK_CRITICAL_T_OVER_E = 1.0 / 8.0

DELTAS = (
    0.00625,
    0.01250,
    0.02500,
    0.05000,
    0.10000,
    0.20000,
    0.40000,
)

EXPECTED_MASS_FACTORS = {
    0.00625: 11.100764905398,
    0.01250: 11.105073553053,
    0.02500: 11.113686825672,
    0.05000: 11.130897375158,
    0.10000: 11.165255241660,
    0.20000: 11.233723934208,
    0.40000: 11.369718516276,
}

HISTORICAL_FINE_T_OVER_E = (
    0.186185265139
)

HISTORICAL_FINE_CRITICAL_GAUGE_FRACTION = (
    0.383694
)

HISTORICAL_30_PERCENT_T_OVER_E = (
    0.14598
)

HISTORICAL_30_PERCENT_CURVATURE_OVER_E = (
    0.50344
)

HISTORICAL_30_PERCENT_GAUGE_ENERGY_OVER_E = (
    0.08042
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


def q_and_prime(
    radius: float,
    delta: float,
) -> tuple[float, float]:
    """Return q=r*p_r and dq/dr for the exact finite 006D profile."""

    inner_width = (
        delta / 4.0
    )

    outer_width = delta

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

    if radius <= (
        BETA
        + outer_width
    ):
        v = (
            (
                radius
                - BETA
            )
            / outer_width
        )

        s = smoothstep(
            v
        )

        sp = (
            smoothstep_prime(
                v
            )
            / outer_width
        )

        q = (
            (
                1.0
                - s
            )
            * q_annulus
        )

        qp = (
            (
                1.0
                - s
            )
            * qp_annulus
            -
            sp
            * q_annulus
        )

        return (
            q,
            qp,
        )

    return (
        0.0,
        0.0,
    )


def stress(
    radius: float,
    delta: float,
) -> tuple[
    float,
    float,
    float,
]:
    """Return epsilon, p_r, and p_phi."""

    q, qp = q_and_prime(
        radius,
        delta,
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


def integration_breakpoints(
    delta: float,
) -> tuple[float, ...]:
    """Return radial stress interfaces."""

    return (
        0.0,
        ALPHA
        - delta / 4.0,
        ALPHA
        + delta / 4.0,
        BETA,
        BETA
        + delta,
    )


def piecewise_integral(
    function,
    delta: float,
    lower: float = 0.0,
    upper: float | None = None,
) -> float:
    """Integrate across exact stress interfaces."""

    if upper is None:
        upper = (
            BETA
            + delta
        )

    interior = [
        point
        for point
        in integration_breakpoints(
            delta
        )
        if (
            lower
            < point
            < upper
        )
    ]

    boundaries = [
        lower,
        *interior,
        upper,
    ]

    total = 0.0

    for left, right in zip(
        boundaries[:-1],
        boundaries[1:],
    ):
        value, _ = quad(
            function,
            left,
            right,
            epsabs=2.0e-11,
            epsrel=2.0e-11,
            limit=500,
        )

        total += value

    return float(
        total
    )


def integrated_quantities(
    delta: float,
) -> dict[str, float]:
    """Return E, P, Dmax, Tmax, and mass factor."""

    energy = (
        2.0
        * math.pi
        * piecewise_integral(
            lambda radius:
                radius
                * stress(
                    radius,
                    delta,
                )[0],
            delta,
        )
    )

    pressure_trace = (
        2.0
        * math.pi
        * piecewise_integral(
            lambda radius:
                radius
                * (
                    stress(
                        radius,
                        delta,
                    )[1]
                    +
                    stress(
                        radius,
                        delta,
                    )[2]
                ),
            delta,
        )
    )

    d_capacity = (
        2.0
        * math.pi
        * piecewise_integral(
            lambda radius:
                radius
                * min(
                    stress(
                        radius,
                        delta,
                    )[0]
                    +
                    stress(
                        radius,
                        delta,
                    )[1],
                    stress(
                        radius,
                        delta,
                    )[0]
                    +
                    stress(
                        radius,
                        delta,
                    )[2],
                    stress(
                        radius,
                        delta,
                    )[0],
                ),
            delta,
        )
    )

    t_max = (
        0.5
        * d_capacity
    )

    mass_factor = (
        energy
        / math.pi
    )

    return {
        "energy":
            energy,
        "pressure_trace":
            pressure_trace,
        "d_capacity":
            d_capacity,
        "t_max":
            t_max,
        "t_over_e":
            t_max
            / energy,
        "mass_factor":
            mass_factor,
    }


def takeover_metrics(
    delta: float,
    fraction: float,
) -> dict[str, float]:
    """Return fixed-charge and gauge metrics after outer-collar takeover."""

    base = integrated_quantities(
        delta
    )

    lower = (
        BETA
        +
        (
            1.0
            - fraction
        )
        * delta
    )

    upper = (
        BETA
        + delta
    )

    removed_d = (
        2.0
        * math.pi
        * piecewise_integral(
            lambda radius:
                radius
                * min(
                    stress(
                        radius,
                        delta,
                    )[0]
                    +
                    stress(
                        radius,
                        delta,
                    )[1],
                    stress(
                        radius,
                        delta,
                    )[0]
                    +
                    stress(
                        radius,
                        delta,
                    )[2],
                    stress(
                        radius,
                        delta,
                    )[0],
                ),
            delta,
            lower=lower,
            upper=upper,
        )
    )

    remaining_t = (
        base[
            "t_max"
        ]
        -
        0.5
        * removed_d
    )

    gauge_energy = (
        2.0
        * math.pi
        * piecewise_integral(
            lambda radius:
                radius
                * (
                    stress(
                        radius,
                        delta,
                    )[0]
                    +
                    stress(
                        radius,
                        delta,
                    )[1]
                ),
            delta,
            lower=lower,
            upper=upper,
        )
    )

    t_over_e = (
        remaining_t
        / base[
            "energy"
        ]
    )

    p_over_e = (
        base[
            "pressure_trace"
        ]
        / base[
            "energy"
        ]
    )

    curvature_over_e = (
        24.0
        * t_over_e
        -
        3.0
        -
        5.0
        * p_over_e
    )

    return {
        "t_over_e":
            t_over_e,
        "curvature_over_e":
            curvature_over_e,
        "gauge_energy_over_e":
            gauge_energy
            / base[
                "energy"
            ],
    }


def critical_takeover_fraction(
    delta: float,
) -> float:
    """Solve for takeover fraction where fixed-charge dilation margin vanishes."""

    return float(
        brentq(
            lambda fraction:
                (
                    takeover_metrics(
                        delta,
                        fraction,
                    )[
                        "t_over_e"
                    ]
                    -
                    DERRICK_CRITICAL_T_OVER_E
                ),
            0.0,
            1.0,
            xtol=1.0e-13,
            rtol=1.0e-13,
        )
    )


def main() -> None:
    """Run historical reconstruction and thick-source extension."""

    print(
        "=== 016B — THICK 006D "
        "FIXED-CHARGE / GAUGE CAPACITY GATE ==="
    )

    print()
    print(
        "=== HISTORICAL 008C / 008F "
        "INDEPENDENT RECONSTRUCTION ==="
    )

    fine_delta = 0.00625

    fine = integrated_quantities(
        fine_delta
    )

    fine_30 = takeover_metrics(
        fine_delta,
        0.30,
    )

    fine_critical = (
        critical_takeover_fraction(
            fine_delta
        )
    )

    print(
        "FINE_TMAX_OVER_E="
        f"{fine['t_over_e']:.15e}"
    )

    print(
        "FINE_CRITICAL_GAUGE_FRACTION="
        f"{fine_critical:.15e}"
    )

    print(
        "FINE_30_PERCENT_T_OVER_E="
        f"{fine_30['t_over_e']:.15e}"
    )

    print(
        "FINE_30_PERCENT_CURVATURE_OVER_E="
        f"{fine_30['curvature_over_e']:.15e}"
    )

    print(
        "FINE_30_PERCENT_GAUGE_ENERGY_OVER_E="
        f"{fine_30['gauge_energy_over_e']:.15e}"
    )

    historical_match = bool(
        abs(
            fine[
                "t_over_e"
            ]
            -
            HISTORICAL_FINE_T_OVER_E
        )
        < 5.0e-10
        and abs(
            fine_critical
            -
            HISTORICAL_FINE_CRITICAL_GAUGE_FRACTION
        )
        < 5.0e-6
        and abs(
            fine_30[
                "t_over_e"
            ]
            -
            HISTORICAL_30_PERCENT_T_OVER_E
        )
        < 5.0e-5
        and abs(
            fine_30[
                "curvature_over_e"
            ]
            -
            HISTORICAL_30_PERCENT_CURVATURE_OVER_E
        )
        < 5.0e-5
        and abs(
            fine_30[
                "gauge_energy_over_e"
            ]
            -
            HISTORICAL_30_PERCENT_GAUGE_ENERGY_OVER_E
        )
        < 5.0e-5
    )

    print(
        "HISTORICAL_008C_008F_RECONSTRUCTION="
        f"{'PASS' if historical_match else 'FAIL'}"
    )

    print()
    print(
        "=== THICKNESS SCAN ==="
    )

    records = {}

    for delta in DELTAS:
        base = integrated_quantities(
            delta
        )

        gauge_30 = takeover_metrics(
            delta,
            0.30,
        )

        gauge_35 = takeover_metrics(
            delta,
            0.35,
        )

        critical = (
            critical_takeover_fraction(
                delta
            )
        )

        mass_reference = (
            EXPECTED_MASS_FACTORS[
                delta
            ]
        )

        mass_error = abs(
            base[
                "mass_factor"
            ]
            -
            mass_reference
        )

        capacity_ratio = (
            base[
                "t_over_e"
            ]
            / DERRICK_CRITICAL_T_OVER_E
        )

        record = {
            "delta":
                delta,
            "base":
                base,
            "gauge_30":
                gauge_30,
            "gauge_35":
                gauge_35,
            "critical":
                critical,
            "capacity_ratio":
                capacity_ratio,
            "mass_error":
                mass_error,
        }

        records[
            delta
        ] = record

        print(
            "CASE "
            f"DELTA={delta:.8f} "
            f"MASS_FACTOR={base['mass_factor']:.15e} "
            f"MASS_REFERENCE_ERROR={mass_error:.3e} "
            f"P_OVER_E="
            f"{base['pressure_trace']/base['energy']:+.3e} "
            f"TMAX_OVER_E={base['t_over_e']:.15e} "
            f"CAPACITY_OVER_CRITICAL="
            f"{capacity_ratio:.12f} "
            f"GAUGE_CRITICAL_FRACTION="
            f"{critical:.12f} "
            f"TAKEOVER30_T_OVER_E="
            f"{gauge_30['t_over_e']:.15e} "
            f"TAKEOVER30_CURVATURE_OVER_E="
            f"{gauge_30['curvature_over_e']:.15e} "
            f"TAKEOVER30_GAUGE_ENERGY_OVER_E="
            f"{gauge_30['gauge_energy_over_e']:.15e} "
            f"TAKEOVER35_T_OVER_E="
            f"{gauge_35['t_over_e']:.15e} "
            f"TAKEOVER35_CURVATURE_OVER_E="
            f"{gauge_35['curvature_over_e']:.15e}"
        )

    print()
    print(
        "=== PRACTICALITY-CANDIDATE DECISION ==="
    )

    candidate_green = True

    for delta in (
        0.10,
        0.20,
    ):
        record = records[
            delta
        ]

        base_green = bool(
            record[
                "base"
            ][
                "t_over_e"
            ]
            >
            DERRICK_CRITICAL_T_OVER_E
        )

        gauge_30_green = bool(
            record[
                "gauge_30"
            ][
                "t_over_e"
            ]
            >
            DERRICK_CRITICAL_T_OVER_E
        )

        gauge_35_green = bool(
            record[
                "gauge_35"
            ][
                "t_over_e"
            ]
            >
            DERRICK_CRITICAL_T_OVER_E
        )

        critical_above_35 = bool(
            record[
                "critical"
            ]
            >
            0.35
        )

        mass_reconstruction_green = bool(
            record[
                "mass_error"
            ]
            <
            1.0e-8
        )

        case_green = bool(
            base_green
            and gauge_30_green
            and gauge_35_green
            and critical_above_35
            and mass_reconstruction_green
        )

        candidate_green = (
            candidate_green
            and case_green
        )

        print(
            f"DELTA_{str(delta).replace('.', 'P')}_"
            "FIXED_CHARGE_CAPACITY="
            f"{'PASS' if base_green else 'FAIL'}"
        )

        print(
            f"DELTA_{str(delta).replace('.', 'P')}_"
            "30_PERCENT_GAUGE_TAKEOVER="
            f"{'PASS' if gauge_30_green else 'FAIL'}"
        )

        print(
            f"DELTA_{str(delta).replace('.', 'P')}_"
            "35_PERCENT_GAUGE_TAKEOVER="
            f"{'PASS' if gauge_35_green else 'FAIL'}"
        )

        print(
            f"DELTA_{str(delta).replace('.', 'P')}_"
            "CRITICAL_GAUGE_FRACTION="
            f"{record['critical']:.15e}"
        )

    print()
    print(
        "=== 016B FINAL DECISION ==="
    )

    print(
        "HISTORICAL_RECONSTRUCTION_VALID="
        f"{historical_match}"
    )

    print(
        "THICK_006D_FIXED_CHARGE_STABILITY_WINDOW="
        f"{'SURVIVES' if candidate_green else 'NOT_ESTABLISHED'}"
    )

    print(
        "THICK_006D_30_PERCENT_GAUGE_WINDOW="
        f"{'SURVIVES' if candidate_green else 'NOT_ESTABLISHED'}"
    )

    print(
        "THICK_006D_35_PERCENT_GAUGE_WINDOW="
        f"{'SURVIVES' if candidate_green else 'NOT_ESTABLISHED'}"
    )

    if (
        historical_match
        and candidate_green
    ):
        print(
            "016A_PRACTICALITY_AUGMENTATION="
            "PROMOTED_TO_FIELD_REALIZATION_TARGET"
        )

        print(
            "PREFERRED_DELTA_BRACKET="
            "0.10_TO_0.20"
        )

        print(
            "NEXT="
            "016C_GLOBAL_SMOOTH_CHARGED_GAUGE_"
            "FIELD_BOUNDARY_VALUE_PROBLEM"
        )

    else:
        print(
            "016A_PRACTICALITY_AUGMENTATION="
            "REQUIRES_REVIEW"
        )

        print(
            "NEXT="
            "AUDIT_FIXED_CHARGE_OR_GAUGE_CAPACITY_FORMULATION"
        )

    print(
        "GLOBAL_FIELD_SOLUTION="
        "NOT_YET_ESTABLISHED"
    )

    print(
        "FULL_DYNAMIC_STABILITY="
        "NOT_YET_ESTABLISHED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_006D_THICK_FIXED_CHARGE_"
        "GAUGE_CAPACITY_GATE"
    )


if __name__ == "__main__":
    main()
