r"""016C — global gauge-integrability prerequisite for thick 006D.

PURPOSE
-------
Test whether the simplest global realization of the local Maxwell/gauge
stress decomposition found in 008F can actually arise from smooth static
gauge potentials over a finite 006D collar.

BACKGROUND
----------
008F established the local algebraic gauge-sector stress

    T_g = (g, 0, g, 0)

in the ordering

    (epsilon, p_r, p_phi, p_z),

where

    g = epsilon + p_r.

That local algebraic decomposition did not establish globally smooth gauge
potentials.

016A and 016B promoted thick delta=0.10--0.20 sources as the preferred
006D physical-realization targets, so global integrability must now be tested
before attempting an expensive nonlinear field-equation solve.

SINGLE-MAXWELL OBSTRUCTION
--------------------------
A single static Maxwell field with zero Poynting momentum has electric and
magnetic fields parallel in its zero-momentum frame.  Its spatial principal
pressures have the Maxwell pattern

    (-u, +u, +u)

up to permutation.

The target gauge sector instead requires

    (0, +g, 0).

Therefore one zero-momentum Maxwell field cannot exactly equal the 008F
gauge-sector tensor.

TWO-ELECTROSTATIC-FIELD TEST
----------------------------
Consider two independent static electrostatic gauge fields with scalar
potentials Phi_1(r,z) and Phi_2(r,z).

Their total stress matches

    (epsilon, p_r, p_phi, p_z)
    =
    (g, 0, g, 0)

with zero r-z shear iff

    sum_a E_r,a^2 = g,

    sum_a E_z,a^2 = g,

    sum_a E_r,a E_z,a = 0.

Since E_a = -grad Phi_a, defining

    Phi = (Phi_1, Phi_2)

gives the Jacobian condition

    J^T J = g I.

Thus Phi would have to be a local conformal map with scale factor sqrt(g).

For any nondegenerate C^2 two-dimensional conformal map, log(sqrt(g)) is
harmonic.  Equivalently a necessary condition is

    (d_r^2 + d_z^2) log(g) = 0.

EXACT 006D COLLAR
-----------------
For the outer smoothstep collar,

    q = (1-s(v)) (-alpha^2/r),

    v = (r-beta)/delta,

and

    p_r = q/r,

    p_phi = dq/dr,

    epsilon = p_phi

inside the positive-gauge part of the collar.

Using

    s'(v)=6v(1-v),

one obtains exactly

    g_surface
        =
        epsilon + p_r
        =
        alpha^2 s'(v)/(delta r).

The finite vertical profile is proportional to

    y^2 (1-y)^2,

with

    y=(z+delta)/delta.

Therefore, ignoring positive constants that disappear from log derivatives,

    g(r,z)
        proportional to
        [v(1-v)/r] y^2(1-y)^2.

Its logarithmic Laplacian is

    Delta log g
        =
        1/r^2
        -
        1/delta^2 [
            1/v^2
            + 1/(1-v)^2
            + 2/y^2
            + 2/(1-y)^2
        ].

For the tested delta <= 0.4 collar family this expression is strictly
negative throughout the open collar.

Therefore the exact two-electrostatic-potential realization is incompatible
with the target finite 006D gauge stress.

CLAIM SCOPE
-----------
A failure proves only that the simplest two-independent-electrostatic-field
global realization cannot exactly reproduce the finite 006D gauge sector.

It does NOT exclude:
- three or more independent gauge sectors;
- mixed electric/magnetic configurations with additional compensation;
- charged scalar plus gauge solutions;
- time-dependent gauge configurations;
- a modified allocation of the 006D stress;
- the validity of the 006D gravitational source itself.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_006D_GAUGE_INTEGRABILITY_PREFLIGHT
"""

from __future__ import annotations

import math

import numpy as np


ALPHA = 1.437500564637
BETA = 4.701437405300

DELTAS = (
    0.10,
    0.20,
    0.40,
)


def log_target_g(
    radius: float,
    z_value: float,
    delta: float,
) -> float:
    """Return log target gauge density up to an irrelevant additive constant."""

    v = (
        radius
        - BETA
    ) / delta

    y = (
        z_value
        + delta
    ) / delta

    if not (
        0.0 < v < 1.0
        and 0.0 < y < 1.0
    ):
        raise ValueError(
            "Point must lie strictly inside the finite collar."
        )

    return (
        math.log(v)
        + math.log(1.0 - v)
        - math.log(radius)
        + 2.0 * math.log(y)
        + 2.0 * math.log(1.0 - y)
    )


def analytic_log_laplacian(
    radius: float,
    v: float,
    y: float,
    delta: float,
) -> float:
    """Return exact flat r-z Laplacian of log target gauge density."""

    return (
        1.0
        / (
            radius
            * radius
        )
        -
        (
            1.0
            / (
                delta
                * delta
            )
        )
        * (
            1.0
            / (
                v
                * v
            )
            +
            1.0
            / (
                (1.0 - v)
                * (1.0 - v)
            )
            +
            2.0
            / (
                y
                * y
            )
            +
            2.0
            / (
                (1.0 - y)
                * (1.0 - y)
            )
        )
    )


def finite_difference_log_laplacian(
    radius: float,
    z_value: float,
    delta: float,
) -> float:
    """Independently finite-difference the logarithmic Laplacian."""

    step = (
        1.0e-5
        * delta
    )

    center = log_target_g(
        radius,
        z_value,
        delta,
    )

    radial_second = (
        log_target_g(
            radius + step,
            z_value,
            delta,
        )
        -
        2.0 * center
        +
        log_target_g(
            radius - step,
            z_value,
            delta,
        )
    ) / (
        step
        * step
    )

    vertical_second = (
        log_target_g(
            radius,
            z_value + step,
            delta,
        )
        -
        2.0 * center
        +
        log_target_g(
            radius,
            z_value - step,
            delta,
        )
    ) / (
        step
        * step
    )

    return (
        radial_second
        +
        vertical_second
    )


def scan_delta(
    delta: float,
) -> dict[str, float]:
    """Scan the open collar away from endpoint singularities."""

    v_values = np.linspace(
        0.05,
        0.95,
        181,
    )

    y_values = np.linspace(
        0.05,
        0.95,
        181,
    )

    values = []

    for v in v_values:
        radius = (
            BETA
            + delta * float(v)
        )

        for y in y_values:
            values.append(
                analytic_log_laplacian(
                    radius,
                    float(v),
                    float(y),
                    delta,
                )
            )

    center_radius = (
        BETA
        + 0.5 * delta
    )

    center_z = (
        -0.5 * delta
    )

    analytic_center = (
        analytic_log_laplacian(
            center_radius,
            0.5,
            0.5,
            delta,
        )
    )

    finite_center = (
        finite_difference_log_laplacian(
            center_radius,
            center_z,
            delta,
        )
    )

    relative_difference = (
        abs(
            finite_center
            -
            analytic_center
        )
        /
        abs(
            analytic_center
        )
    )

    return {
        "maximum":
            float(
                np.max(
                    values
                )
            ),
        "minimum":
            float(
                np.min(
                    values
                )
            ),
        "analytic_center":
            analytic_center,
        "finite_center":
            finite_center,
        "relative_difference":
            relative_difference,
    }


def main() -> None:
    """Execute the gauge-integrability preflight."""

    print(
        "=== 016C — 006D GLOBAL GAUGE "
        "INTEGRABILITY PREFLIGHT ==="
    )

    print()

    print(
        "=== ALGEBRAIC SINGLE-MAXWELL CHECK ==="
    )

    print(
        "SINGLE_STATIC_ZERO_MOMENTUM_MAXWELL_"
        "PRINCIPAL_PRESSURES=(-u,+u,+u)_UP_TO_PERMUTATION"
    )

    print(
        "TARGET_GAUGE_PRINCIPAL_PRESSURES="
        "(0,+g,0)"
    )

    print(
        "SINGLE_STATIC_ZERO_MOMENTUM_MAXWELL_"
        "EXACT_TARGET_REALIZATION=NO"
    )

    print()

    print(
        "=== TWO-ELECTROSTATIC-POTENTIAL "
        "INTEGRABILITY CHECK ==="
    )

    all_strictly_negative = True
    finite_difference_green = True

    for delta in DELTAS:
        result = scan_delta(
            delta
        )

        strictly_negative = bool(
            result[
                "maximum"
            ]
            < 0.0
        )

        finite_match = bool(
            result[
                "relative_difference"
            ]
            < 2.0e-5
        )

        all_strictly_negative = (
            all_strictly_negative
            and strictly_negative
        )

        finite_difference_green = (
            finite_difference_green
            and finite_match
        )

        print(
            "CASE "
            f"DELTA={delta:.8f} "
            f"MAX_DELTA_LOG_G="
            f"{result['maximum']:.12e} "
            f"MIN_DELTA_LOG_G="
            f"{result['minimum']:.12e} "
            f"CENTER_ANALYTIC="
            f"{result['analytic_center']:.12e} "
            f"CENTER_FINITE_DIFFERENCE="
            f"{result['finite_center']:.12e} "
            f"FD_RELATIVE_ERROR="
            f"{result['relative_difference']:.12e} "
            f"STRICTLY_NONHARMONIC="
            f"{strictly_negative}"
        )

    print()

    print(
        "=== ANALYTIC BOUND ==="
    )

    print(
        "MIN_BRACKET_AT_V_EQ_Y_EQ_HALF="
        "24"
    )

    print(
        "DELTA_LOG_G_BOUND="
        "1/r^2-24/delta^2"
    )

    print(
        "TARGET_LOG_CONFORMAL_FACTOR_HARMONIC="
        f"{not all_strictly_negative}"
    )

    print(
        "FINITE_DIFFERENCE_INDEPENDENT_CHECK="
        f"{'PASS' if finite_difference_green else 'FAIL'}"
    )

    print()

    print(
        "=== 016C DECISION ==="
    )

    if (
        all_strictly_negative
        and finite_difference_green
    ):
        print(
            "TWO_INDEPENDENT_STATIC_ELECTROSTATIC_"
            "U1_EXACT_GLOBAL_TARGET="
            "REJECTED_BY_CONFORMAL_INTEGRABILITY"
        )

        print(
            "008F_LOCAL_GAUGE_STRESS_DECOMPOSITION="
            "PRESERVED"
        )

        print(
            "016B_FIXED_CHARGE_GAUGE_CAPACITY="
            "PRESERVED"
        )

        print(
            "GLOBAL_GAUGE_FIELD_REALIZATION="
            "NOT_CLOSED"
        )

        print(
            "REQUIRED_NEXT_REALIZATION_CLASS="
            "MIXED_GAUGED_SCALAR_OR_HIGHER_GAUGE_"
            "DEGREE_OF_FREEDOM"
        )

        print(
            "NEXT="
            "016D_MINIMAL_GLOBAL_GAUGED_SCALAR_"
            "INTEGRABILITY_GATE"
        )

    else:
        print(
            "TWO_FIELD_NO_GO="
            "NOT_ESTABLISHED"
        )

        print(
            "NEXT="
            "AUDIT_016C_DERIVATION"
        )

    print(
        "006D_GRAVITATIONAL_CONSTRUCTION_INVALIDATED="
        "NO"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_006D_GAUGE_"
        "INTEGRABILITY_PREFLIGHT"
    )


if __name__ == "__main__":
    main()
