r"""016G — asymptotic Euler-Lagrange gate for the 006D field target.

PURPOSE
-------
Test whether the power-law outer-tail stress architecture promoted by
Simulations 016E and 016F is asymptotically compatible with the actual
Euler-Lagrange equation of the minimum canonical winding sector.

This is intentionally cheaper and more decisive than launching the full
two-dimensional nonlinear boundary-value solver.

SCIENTIFIC QUESTION
-------------------
The current preferred realization architecture contains:

1. a stationary nonwinding complex scalar carrying temporal charge;
2. a separate static winding complex scalar carrying angular stress;
3. a U(1) gauge field controlling the covariant winding mismatch.

Simulation 016F established a finite kinematic coexistence window for the
charge and winding requirements.

However, a kinematic stress decomposition does not guarantee that the winding
field can satisfy its own canonical Euler-Lagrange equation while approaching
a stable vacuum.

016G tests that missing requirement analytically and numerically.

INPUT FROM 016F
---------------
The preferred tested candidate was:

    delta = 0.20
    inner transition half-width W = 1.00
    outer tail length ell = 0.60
    power exponent m = 2

with

    C = 40.749886771113
    T_max/E = 0.180278569163
    target T/E = 0.14
    eta = 0.776575943831
    K_required = 9.589406109611
    conservative integer winding = 10
    peak-stress relief = 1400.489001

The asymptotic argument below does not depend on W or ell.

ASYMPTOTIC POWER-LAW TARGET
---------------------------
For the m-power outer tail,

    q(r)
        proportional to
        -r^(-m-1).

Therefore asymptotically

    p_r
        proportional to
        -C_inf r^(-m-2),

    p_phi
        proportional to
        +(m+1) C_inf r^(-m-2),

and

    epsilon
        =
        p_phi.

The unallocated radial Gram capacity is

    epsilon + p_r
        =
        m C_inf r^(-m-2).

The temporal-capacity minimum is asymptotically the same radial quantity.

Allocate

    D
        =
        eta m C_inf r^(-m-2)

to the nonwinding charged stabilizer.

The remaining radial scalar-gradient budget is

    G_r
        =
        (1-eta) m C_inf r^(-m-2).

The remaining required angular Gram component is

    A
        =
        [
            2(m+1)
            -
            eta m
        ]
        C_inf r^(-m-2).

AMPLITUDE BOUND
---------------
Let F(r) be the winding-field amplitude.

Finite energy requires

    F(infinity)=0.

Because its radial gradient obeys

    F'(r)^2 <= G_r(r),

we obtain

    F(r)
        <=
        integral_r^infinity sqrt(G_r(s)) ds.

For the asymptotic power law,

    integral_r^infinity sqrt(G_r(s)) ds
        proportional to
        r^(-m/2).

Thus the slowest possible finite-energy power-law amplitude is

    F(r)
        proportional to
        r^(-s),

with

    s = m/2.

Any faster power-law decay has

    s > m/2.

GAUGE-COVARIANT WINDING BOUND
-----------------------------
Let

    k(r)
        =
        n
        -
        e A_phi(r)

be the gauge-covariant winding mismatch.

The angular stress requires

    k(r)^2 F(r)^2 / r^2
        =
        A(r).

Using the maximum allowed amplitude gives the smallest possible asymptotic
mismatch:

    k_inf^2
        >=
        m [
            2(m+1)
            -
            eta m
        ]
        /
        [
            4(1-eta)
        ].

Since

    s^2
        =
        m^2/4,

the difference simplifies exactly to

    k_inf^2 - s^2
        =
        m(m+2)
        /
        [
            4(1-eta)
        ].

For every

    m > 0

and

    0 <= eta < 1,

this quantity is strictly positive.

Therefore even the smallest asymptotically allowed gauge mismatch satisfies

    k_inf > s.

CANONICAL EULER-LAGRANGE EQUATION
---------------------------------
After projection onto the asymptotic vertical mode, a power-law radial tail
requires zero positive mass gap.

A positive effective mass gap would instead produce exponential radial
localization and would not reproduce the tested power-law target.

For the gapless canonical winding amplitude, the radial equation is

    F''
    +
    (1/r) F'
    -
    (k^2/r^2) F
    -
    U_eff'(F)
    =
    0.

For

    F = A r^(-s),

the radial Laplacian is

    F''
    +
    (1/r) F'
    =
    (s^2/r^2) F.

Therefore the potential force required by exact asymptotic stress matching is

    U_eff'(F)
        =
        (s^2-k^2)
        F/r^2.

Since

    k^2 > s^2,

the required force is negative for positive F near the vacuum.

For a regular asymptotically decoupled canonical field whose vacuum F=0 is a
stable local minimum, the leading small-positive-F potential force has the
opposite sign:

    U_eff'(F) >= 0

sufficiently near the vacuum.

Thus the exact current power-law target is incompatible with the minimum
asymptotically decoupled canonical winding self-potential under these
assumptions.

M=2 SPECIALIZATION
------------------
For the preferred m=2 target,

    s = 1.

The matching nonlinear power is quartic:

    U_eff(F)
        ~
        lambda F^4/4.

The Euler-Lagrange coefficient condition becomes

    lambda A^2
        =
        s^2-k_inf^2.

A stable standalone quartic vacuum requires positive lambda.

The current target instead predicts a strictly negative right-hand side.

FASTER AMPLITUDE DECAY
----------------------
Choosing

    s > m/2

does not rescue the exact target.

Angular matching then requires

    k^2
        proportional to
        r^(2s-m).

Because

    2s-m > 0,

the angular term eventually dominates the positive radial-Laplacian term.

The same negative-sign Euler-Lagrange obstruction remains asymptotically.

SCOPE OF THE RESULT
-------------------
A red result DOES NOT invalidate:

- the 006D gravitational construction;
- the positive-energy / DEC result;
- 016A thickness optimization;
- 016B fixed-charge capacity;
- 016E finite-energy power-law gauge asymptotics;
- 016F charge/winding kinematic coexistence.

It rejects only the exact current power-law stress target when the winding
tail is supplied by a minimum asymptotically decoupled canonical scalar with a
regular stable-vacuum self-potential.

POSSIBLE ESCAPES
----------------
The obstruction can potentially be avoided by:

1. relaxing exact stress matching and solving an actual field model while
   optimizing only the gravitational observable;

2. retaining an additional asymptotically coupled gapless field so that
   cross-potential forces participate in the winding Euler-Lagrange equation;

3. a justified counter-winding or enlarged field multiplet;

4. noncanonical or higher-derivative kinetic physics;

5. a gauge configuration whose additional stress materially changes the
   target asymptotics.

These possibilities are NOT established by this gate.

STOP RULE
---------
016G is the planned pause-point gate for the current research slice.

After this run, documentation should be updated regardless of whether the
minimal canonical target passes or fails.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_006D_ASYMPTOTIC_EULER_LAGRANGE_GATE
"""

from __future__ import annotations

import math


PREFERRED_M = 2

PREFERRED_TMAX_OVER_E = (
    0.180278569163
)

TARGET_T_OVER_E = (
    0.14
)

REPORTED_ETA = (
    0.776575943831
)

REPORTED_K_INFINITY = (
    3.154613692977
)

REPORTED_K_REQUIRED = (
    9.589406109611
)

REPORTED_CONSERVATIVE_WINDING = (
    10
)

REPORTED_C = (
    40.749886771113
)

REPORTED_PEAK_STRESS_RELIEF = (
    1400.489001
)


def amplitude_exponent(
    power_exponent: float,
) -> float:
    """Return slowest finite-energy winding-amplitude power exponent."""

    return (
        power_exponent
        / 2.0
    )


def k_min_squared(
    power_exponent: float,
    eta: float,
) -> float:
    """Return asymptotic lower bound on gauge-covariant mismatch squared."""

    numerator = (
        power_exponent
        * (
            2.0
            * (
                power_exponent
                + 1.0
            )
            -
            eta
            * power_exponent
        )
    )

    denominator = (
        4.0
        * (
            1.0
            -
            eta
        )
    )

    return (
        numerator
        / denominator
    )


def gap_direct(
    power_exponent: float,
    eta: float,
) -> float:
    """Return k_min^2-s^2 from its direct definitions."""

    s = amplitude_exponent(
        power_exponent
    )

    return (
        k_min_squared(
            power_exponent,
            eta,
        )
        -
        s
        * s
    )


def gap_closed_form(
    power_exponent: float,
    eta: float,
) -> float:
    """Return exact simplified positive gap."""

    return (
        power_exponent
        * (
            power_exponent
            + 2.0
        )
        /
        (
            4.0
            * (
                1.0
                -
                eta
            )
        )
    )


def matching_potential_power(
    power_exponent: float,
) -> float:
    """Return monomial potential power matching the slowest tail scaling."""

    s = amplitude_exponent(
        power_exponent
    )

    return (
        2.0
        +
        2.0
        / s
    )


def finite_difference_effective_coefficient(
    power_exponent: float,
    eta: float,
    radius: float,
) -> float:
    """Independently recover the asymptotic Euler-Lagrange force coefficient.

    The test chooses unit amplitude

        F(r)=r^(-s)

    and evaluates

        F'' + F'/r - k_min^2 F/r^2

    by finite differences.

    Dividing by the matching small-field power F^(p-1) must recover

        s^2-k_min^2.

    Field normalization can change positive multiplicative factors but cannot
    change the sign tested here.
    """

    s = amplitude_exponent(
        power_exponent
    )

    k_squared = k_min_squared(
        power_exponent,
        eta,
    )

    potential_power = (
        matching_potential_power(
            power_exponent
        )
    )

    step = (
        1.0e-4
        * radius
    )

    def field(
        location: float,
    ) -> float:
        return (
            location
            ** (
                -s
            )
        )

    f_minus = field(
        radius
        -
        step
    )

    f_center = field(
        radius
    )

    f_plus = field(
        radius
        +
        step
    )

    first_derivative = (
        f_plus
        -
        f_minus
    ) / (
        2.0
        * step
    )

    second_derivative = (
        f_plus
        -
        2.0
        * f_center
        +
        f_minus
    ) / (
        step
        * step
    )

    radial_laplacian = (
        second_derivative
        +
        first_derivative
        / radius
    )

    residual = (
        radial_laplacian
        -
        k_squared
        * f_center
        / (
            radius
            * radius
        )
    )

    denominator = (
        f_center
        ** (
            potential_power
            -
            1.0
        )
    )

    return (
        residual
        / denominator
    )


def faster_decay_normalized_residual(
    power_exponent: float,
    eta: float,
    amplitude_power: float,
    radius: float,
) -> float:
    """Return a normalized E-L derivative-minus-angular coefficient.

    The asymptotic target angular coefficient is normalized by setting the
    common positive stress constant C_inf=1 and the winding amplitude
    coefficient to one.

    For F=r^(-s), exact angular matching requires

        k^2
            =
            A0 r^(2s-m),

    where

        A0
            =
            2(m+1)-eta*m.

    The quantity returned is

        s^2-k^2.

    For every s>m/2 it becomes increasingly negative as r grows.
    """

    m = power_exponent

    angular_coefficient = (
        2.0
        * (
            m
            +
            1.0
        )
        -
        eta
        * m
    )

    k_squared = (
        angular_coefficient
        * radius
        ** (
            2.0
            * amplitude_power
            -
            m
        )
    )

    return (
        amplitude_power
        * amplitude_power
        -
        k_squared
    )


def main() -> None:
    """Execute the asymptotic Euler-Lagrange gate."""

    print(
        "=== 016G — MINIMAL TWO-SECTOR "
        "ASYMPTOTIC EULER-LAGRANGE GATE ==="
    )

    print()

    print(
        "=== 016F PREFERRED TARGET RECONSTRUCTION ==="
    )

    eta = (
        TARGET_T_OVER_E
        / PREFERRED_TMAX_OVER_E
    )

    eta_error = abs(
        eta
        -
        REPORTED_ETA
    )

    print(
        "PREFERRED_C="
        f"{REPORTED_C:.12f}"
    )

    print(
        "PREFERRED_TMAX_OVER_E="
        f"{PREFERRED_TMAX_OVER_E:.12f}"
    )

    print(
        "TARGET_T_OVER_E="
        f"{TARGET_T_OVER_E:.12f}"
    )

    print(
        "ETA_RECOMPUTED="
        f"{eta:.15e}"
    )

    print(
        "ETA_REPORTED="
        f"{REPORTED_ETA:.15e}"
    )

    print(
        "ETA_RECONSTRUCTION_ERROR="
        f"{eta_error:.3e}"
    )

    print(
        "PREFERRED_K_REQUIRED="
        f"{REPORTED_K_REQUIRED:.12f}"
    )

    print(
        "PREFERRED_CONSERVATIVE_WINDING="
        f"{REPORTED_CONSERVATIVE_WINDING:d}"
    )

    print(
        "PREFERRED_PEAK_STRESS_RELIEF="
        f"{REPORTED_PEAK_STRESS_RELIEF:.6f}"
    )

    assert eta_error < 2.0e-12

    print()

    print(
        "=== GENERAL ASYMPTOTIC IDENTITY ==="
    )

    identity_green = True
    positivity_green = True

    eta_values = (
        0.0,
        0.25,
        0.50,
        eta,
        0.90,
    )

    for m in range(
        1,
        13,
    ):
        for eta_case in eta_values:
            s = amplitude_exponent(
                float(
                    m
                )
            )

            k_squared = (
                k_min_squared(
                    float(
                        m
                    ),
                    eta_case,
                )
            )

            direct = gap_direct(
                float(
                    m
                ),
                eta_case,
            )

            closed = gap_closed_form(
                float(
                    m
                ),
                eta_case,
            )

            identity_error = abs(
                direct
                -
                closed
            )

            positive = bool(
                direct
                >
                0.0
            )

            identity_green = (
                identity_green
                and identity_error
                <
                5.0e-12
            )

            positivity_green = (
                positivity_green
                and positive
            )

            print(
                "IDENTITY_CASE "
                f"M={m:d} "
                f"ETA={eta_case:.12f} "
                f"S={s:.12f} "
                f"K_MIN={math.sqrt(k_squared):.12f} "
                f"K2_MINUS_S2_DIRECT={direct:.12e} "
                f"K2_MINUS_S2_CLOSED={closed:.12e} "
                f"IDENTITY_ERROR={identity_error:.3e} "
                f"STRICTLY_POSITIVE={positive}"
            )

    print()

    print(
        "ASYMPTOTIC_GAP_IDENTITY="
        f"{'PASS' if identity_green else 'FAIL'}"
    )

    print(
        "K_MIN_GREATER_THAN_AMPLITUDE_EXPONENT="
        f"{'YES_ALL_TESTED_CASES' if positivity_green else 'NO'}"
    )

    assert identity_green
    assert positivity_green

    print()

    print(
        "=== PREFERRED M=2 EULER-LAGRANGE SPECIALIZATION ==="
    )

    m = float(
        PREFERRED_M
    )

    s = amplitude_exponent(
        m
    )

    preferred_k_squared = (
        k_min_squared(
            m,
            eta,
        )
    )

    preferred_k = math.sqrt(
        preferred_k_squared
    )

    k_reconstruction_error = abs(
        preferred_k
        -
        REPORTED_K_INFINITY
    )

    gap = (
        preferred_k_squared
        -
        s
        * s
    )

    required_force_coefficient = (
        -gap
    )

    potential_power = (
        matching_potential_power(
            m
        )
    )

    print(
        "M="
        f"{PREFERRED_M:d}"
    )

    print(
        "AMPLITUDE_POWER_S="
        f"{s:.12f}"
    )

    print(
        "MATCHING_SMALL_FIELD_POTENTIAL_POWER="
        f"{potential_power:.12f}"
    )

    print(
        "K_INFINITY_RECOMPUTED="
        f"{preferred_k:.15e}"
    )

    print(
        "K_INFINITY_REPORTED="
        f"{REPORTED_K_INFINITY:.15e}"
    )

    print(
        "K_INFINITY_RECONSTRUCTION_ERROR="
        f"{k_reconstruction_error:.3e}"
    )

    print(
        "K_INFINITY_SQUARED_MINUS_S_SQUARED="
        f"{gap:.15e}"
    )

    print(
        "S_SQUARED_MINUS_K_INFINITY_SQUARED="
        f"{required_force_coefficient:.15e}"
    )

    print(
        "REQUIRED_EFFECTIVE_QUARTIC_COEFFICIENT_SIGN="
        "NEGATIVE"
    )

    print(
        "STABLE_DECOUPLED_QUARTIC_VACUUM_SIGN="
        "POSITIVE"
    )

    assert k_reconstruction_error < 2.0e-9
    assert gap > 0.0
    assert abs(
        potential_power
        -
        4.0
    ) < 1.0e-12

    print()

    print(
        "=== INDEPENDENT FINITE-DIFFERENCE E-L CHECK ==="
    )

    expected_coefficient = (
        s
        * s
        -
        preferred_k_squared
    )

    finite_difference_green = True

    for radius in (
        10.0,
        100.0,
        1_000.0,
        10_000.0,
    ):
        coefficient = (
            finite_difference_effective_coefficient(
                m,
                eta,
                radius,
            )
        )

        absolute_error = abs(
            coefficient
            -
            expected_coefficient
        )

        relative_error = (
            absolute_error
            /
            abs(
                expected_coefficient
            )
        )

        finite_difference_green = (
            finite_difference_green
            and relative_error
            <
            2.0e-8
        )

        print(
            "FD_CASE "
            f"R={radius:.1f} "
            f"EFFECTIVE_COEFFICIENT="
            f"{coefficient:.15e} "
            f"ANALYTIC="
            f"{expected_coefficient:.15e} "
            f"RELATIVE_ERROR="
            f"{relative_error:.3e}"
        )

    print(
        "FINITE_DIFFERENCE_EULER_LAGRANGE_CHECK="
        f"{'PASS' if finite_difference_green else 'FAIL'}"
    )

    assert finite_difference_green

    print()

    print(
        "=== NO-CHARGE CONTROL ==="
    )

    no_charge_k_squared = (
        k_min_squared(
            m,
            0.0,
        )
    )

    no_charge_gap = (
        no_charge_k_squared
        -
        s
        * s
    )

    print(
        "ETA=0"
    )

    print(
        "K_INFINITY_NO_CHARGE="
        f"{math.sqrt(no_charge_k_squared):.12f}"
    )

    print(
        "K2_MINUS_S2_NO_CHARGE="
        f"{no_charge_gap:.12f}"
    )

    print(
        "OBSTRUCTION_EXISTS_WITHOUT_TEMPORAL_CHARGE="
        f"{no_charge_gap > 0.0}"
    )

    print(
        "TEMPORAL_CHARGE_CREATES_OBSTRUCTION="
        "NO"
    )

    print(
        "TEMPORAL_CHARGE_WORSENS_OBSTRUCTION="
        f"{gap > no_charge_gap}"
    )

    assert no_charge_gap > 0.0
    assert gap > no_charge_gap

    print()

    print(
        "=== FASTER POWER-LAW AMPLITUDE CHECK ==="
    )

    faster_decay_green = True

    for excess in (
        0.10,
        0.25,
        0.50,
        0.90,
    ):
        amplitude_power = (
            s
            +
            excess
        )

        residual_1e3 = (
            faster_decay_normalized_residual(
                m,
                eta,
                amplitude_power,
                1.0e3,
            )
        )

        residual_1e6 = (
            faster_decay_normalized_residual(
                m,
                eta,
                amplitude_power,
                1.0e6,
            )
        )

        increasingly_negative = bool(
            residual_1e6
            <
            residual_1e3
            <
            0.0
        )

        faster_decay_green = (
            faster_decay_green
            and increasingly_negative
        )

        print(
            "FASTER_CASE "
            f"S={amplitude_power:.12f} "
            f"RESIDUAL_R1E3={residual_1e3:.12e} "
            f"RESIDUAL_R1E6={residual_1e6:.12e} "
            f"ANGULAR_TERM_DOMINATES="
            f"{increasingly_negative}"
        )

    print(
        "FASTER_POWER_LAW_DECAY_RESCUES_STABLE_SELF_POTENTIAL="
        f"{not faster_decay_green}"
    )

    assert faster_decay_green

    print()

    print(
        "=== MASS-GAP DICHOTOMY ==="
    )

    print(
        "POSITIVE_EFFECTIVE_MASS_GAP="
        "EXPONENTIAL_NOT_CURRENT_POWER_LAW"
    )

    print(
        "CURRENT_POWER_LAW_TARGET_REQUIRES="
        "ASYMPTOTIC_EFFECTIVE_ZERO_MODE"
    )

    print(
        "ZERO_MODE_PLUS_STABLE_DECOUPLED_SELF_POTENTIAL="
        "INCOMPATIBLE_WITH_REQUIRED_ANGULAR_STRESS"
    )

    print()

    print(
        "=== 016G FINAL DECISION ==="
    )

    gate_red = bool(
        identity_green
        and positivity_green
        and finite_difference_green
        and faster_decay_green
        and gap
        >
        0.0
    )

    if gate_red:
        print(
            "MINIMAL_ASYMPTOTICALLY_DECOUPLED_CANONICAL_"
            "WINDING_EXACT_POWER_LAW_TARGET="
            "REJECTED"
        )

        print(
            "REJECTION_REASON="
            "EULER_LAGRANGE_FORCE_SIGN_CONFLICT"
        )

        print(
            "PREFERRED_016F_TARGET_AS_EXACT_MINIMAL_FIELD_SOLUTION="
            "DEMOTED"
        )

        print(
            "REQUIRED_NEXT_REALIZATION_CLASS="
            "RELAX_EXACT_STRESS_MATCH_OR_ADD_JUSTIFIED_"
            "ASYMPTOTIC_COUPLING"
        )

        print(
            "NEXT_AFTER_DOCUMENTATION="
            "SOLVE_ACTUAL_COUPLED_FIELD_MODEL_WITH_OUTWARD_"
            "GRAVITY_AS_OBJECTIVE_NOT_EXACT_T_TARGET"
        )

    else:
        print(
            "ASYMPTOTIC_EULER_LAGRANGE_NO_GO="
            "NOT_ESTABLISHED"
        )

        print(
            "NEXT_AFTER_DOCUMENTATION="
            "AUDIT_016G_DERIVATION"
        )

    print(
        "006D_GRAVITATIONAL_CONSTRUCTION_INVALIDATED="
        "NO"
    )

    print(
        "016F_KINEMATIC_CHARGE_WINDING_COEXISTENCE_INVALIDATED="
        "NO"
    )

    print(
        "016E_POWER_LAW_FINITE_GAUGE_ENERGY_PREFLIGHT_INVALIDATED="
        "NO"
    )

    print(
        "GLOBAL_FIELD_EULER_LAGRANGE_SOLUTION="
        "NOT_ESTABLISHED"
    )

    print(
        "FULL_DYNAMIC_STABILITY="
        "NOT_ESTABLISHED"
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
        "PAUSE_AND_UPDATE_DOCUMENTATION_AFTER_016G="
        "YES"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_ASYMPTOTIC_NO_GO_"
        "UNDER_STATED_CANONICAL_DECOUPLING_ASSUMPTIONS"
    )


if __name__ == "__main__":
    main()
