"""032V19R4 theorem-first UV-completion atlas.

PURPOSE
-------
R3 closed the simplest healthy UV completion:

    one canonical
    linear
    unscreened
    universal-trace scalar mediator.

R4 asks which nearby UV-completion ideas are genuinely distinct and which
are already killed analytically before expensive field solves.

The principal new result is a Cauchy-Schwarz bound for arbitrary collections
of healthy linearly coupled scalar mediators.

LINEAR MULTI-SCALAR COMPLETION
------------------------------
For canonical scalar mediators sigma_i,

    L_int
        =
        sum_i sigma_i (a_i T - c_i X),

with positive masses m_i, tree-level matching gives

    C1
        =
        sum_i a_i c_i / m_i^2

    D_X
        =
        1/2 sum_i c_i^2 / m_i^2

    D_T
        =
        1/2 sum_i a_i^2 / m_i^2.

Define

    u_i = c_i/m_i
    v_i = a_i/m_i.

Cauchy-Schwarz gives

    C1^2
        <=
        4 D_X D_T.

Therefore distributing the desired C1 among many healthy linear scalar
mediators cannot independently suppress both companion operators.

NARROW-BAND EMPIRICAL BOUND
---------------------------
For mediators with

    m_i >= m_min

and total off-state matter spectral strength

    G^2
        =
        sum_i a_i^2,

one has

    D_T
        <=
        G^2/(2 m_min^2).

Combining this with Cauchy gives

    D_X
        >=
        C1^2 m_min^2/(2 G^2).

This theorem is directly applicable when the mediators are degenerate or
narrow enough that one common experimental Yukawa-strength envelope can
conservatively constrain their summed positive spectral strength.

It is NOT automatically a theorem for an arbitrary broad mass spectrum.
A broad spectrum requires the experimental likelihood to be recomputed with
the full multi-Yukawa kernel.

SCREENING
---------
If an ordinary density-screening mechanism suppresses the same matter
coupling a_i which creates C1, then the active C1 is suppressed by the same
amplitude factor unless an explicit active-state descreening mechanism is
added.

Thus ordinary screening is not by itself a rescue of the R3 template.

An X-dependent active-state descreening mechanism is genuinely new physics
and remains open.

Z2 LOOP SCAFFOLD
----------------
A Z2-odd mediator S can couple quadratically,

    S^2 X/F_X^2
    S^2 T/F_T^2,

without generating a one-particle off-state Yukawa force.

A loop can generate XT.

For an order-one logarithm a dimensional estimate is

    C1
        ~
        1/(32 pi^2 F_X^2 F_T^2).

However the same diagram is logarithmically UV sensitive and the local XT
operator is symmetry allowed.  Therefore the finite coefficient and sign
are not predicted without higher-scale matching.

This is a scaffold, not a completed UV theory.

CLAIM LIMITS
------------
R4 does not close the entire kinetic-conformal class.

It does not close:

- broad spectral scalar completions without a likelihood reconstruction;
- nonlinear active-X-dependent screening/descreening;
- direct shift-protected Goldstone kinetic-metric UV origins;
- properly matched collective or loop-generated completions.

No negative mass is assumed anywhere.
"""

from __future__ import annotations

import math
from typing import Iterable


FOUR_PI = 4.0 * math.pi


def gev_m2_to_ev_m2(
    value_gev_m2: float,
) -> float:
    """Convert GeV^-2 to eV^-2."""

    value = float(
        value_gev_m2
    )

    if value <= 0.0:
        raise ValueError(
            "coupling-strength bound must be positive"
        )

    return (
        value
        * 1.0e-18
    )


def linear_scalar_tower_coefficients(
    *,
    masses_ev: Iterable[float],
    matter_couplings_ev_m1: Iterable[float],
    x_couplings_ev_m1: Iterable[float],
) -> dict[str, float | bool]:
    """Return C1, D_X and D_T for healthy linearly coupled scalars."""

    masses = [
        float(
            value
        )
        for value in masses_ev
    ]

    matter = [
        float(
            value
        )
        for value in matter_couplings_ev_m1
    ]

    x_values = [
        float(
            value
        )
        for value in x_couplings_ev_m1
    ]

    if not (
        len(
            masses
        )
        ==
        len(
            matter
        )
        ==
        len(
            x_values
        )
    ):
        raise ValueError(
            "tower arrays must have equal length"
        )

    if not masses:
        raise ValueError(
            "tower cannot be empty"
        )

    if any(
        value <= 0.0
        for value in masses
    ):
        raise ValueError(
            "all scalar masses must be positive"
        )

    c1 = sum(
        a_value
        * c_value
        / mass**2
        for (
            mass,
            a_value,
            c_value,
        )
        in zip(
            masses,
            matter,
            x_values,
        )
    )

    d_x = (
        0.5
        * sum(
            c_value**2
            / mass**2
            for (
                mass,
                c_value,
            )
            in zip(
                masses,
                x_values,
            )
        )
    )

    d_t = (
        0.5
        * sum(
            a_value**2
            / mass**2
            for (
                mass,
                a_value,
            )
            in zip(
                masses,
                matter,
            )
        )
    )

    left = (
        c1**2
    )

    right = (
        4.0
        * d_x
        * d_t
    )

    tolerance = (
        1.0e-12
        * max(
            1.0,
            abs(
                left
            ),
            abs(
                right
            ),
        )
    )

    return {
        "c1_ev_m4":
            c1,

        "d_x_ev_m4":
            d_x,

        "d_t_ev_m4":
            d_t,

        "c1_squared":
            left,

        "four_dx_dt":
            right,

        "cauchy_satisfied":
            (
                left
                <=
                right
                + tolerance
            ),

        "cauchy_saturation_ratio":
            (
                left
                / right
                if right > 0.0
                else 0.0
            ),

        "negative_mass_required":
            False,
    }


def narrow_band_linear_scalar_bound(
    *,
    target_c1_ev_m4: float,
    minimum_mediator_mass_ev: float,
    total_yukawa_g2_limit_gev_m2: float,
    source_x_inventory_j_per_ev_m4: float,
    base_static_energy_j: float,
    energy_limit_j: float,
) -> dict[str, float | bool]:
    """Return Cauchy + fifth-force lower bound on the X^2 companion.

    Assumptions:

    - canonical positive-energy linearly coupled scalars;
    - all mediator masses >= minimum_mediator_mass_ev;
    - narrow enough spectral support that one conservative experimental
      envelope applies to the summed positive Yukawa strength;
    - the current source X profile is retained.

    The result is candidate-specific and is not a theorem for arbitrary
    source reoptimization or broad mass spectra.
    """

    c1 = float(
        target_c1_ev_m4
    )

    mass = float(
        minimum_mediator_mass_ev
    )

    g2_limit_gev = float(
        total_yukawa_g2_limit_gev_m2
    )

    inventory = float(
        source_x_inventory_j_per_ev_m4
    )

    base = float(
        base_static_energy_j
    )

    limit = float(
        energy_limit_j
    )

    if (
        c1 <= 0.0
        or mass <= 0.0
        or g2_limit_gev <= 0.0
        or inventory <= 0.0
        or base < 0.0
        or limit <= 0.0
    ):
        raise ValueError(
            "invalid narrow-band scalar bound input"
        )

    g2_limit_ev = (
        gev_m2_to_ev_m2(
            g2_limit_gev
        )
    )

    d_t_max = (
        g2_limit_ev
        /
        (
            2.0
            * mass**2
        )
    )

    d_x_min = (
        c1**2
        * mass**2
        /
        (
            2.0
            * g2_limit_ev
        )
    )

    x_energy_min = (
        d_x_min
        * inventory
    )

    total_floor = (
        base
        + x_energy_min
    )

    remaining_before_x = (
        limit
        - base
    )

    return {
        "target_c1_ev_m4":
            c1,

        "minimum_mediator_mass_ev":
            mass,

        "total_yukawa_g2_limit_gev_m2":
            g2_limit_gev,

        "total_yukawa_g2_limit_ev_m2":
            g2_limit_ev,

        "d_t_max_ev_m4":
            d_t_max,

        "d_x_min_ev_m4":
            d_x_min,

        "source_x_inventory_j_per_ev_m4":
            inventory,

        "x_companion_energy_min_j":
            x_energy_min,

        "base_static_energy_j":
            base,

        "remaining_before_x_j":
            remaining_before_x,

        "x_energy_over_remaining_budget":
            (
                x_energy_min
                / remaining_before_x
                if remaining_before_x > 0.0
                else math.inf
            ),

        "base_plus_x_floor_j":
            total_floor,

        "passes_strict_energy_limit":
            (
                total_floor
                <
                limit
            ),

        "negative_mass_required":
            False,

        "broad_spectral_theorem":
            False,

        "source_reoptimization_included":
            False,
    }


def same_vertex_screening_scout(
    *,
    unscreened_g2_gev_m2: float,
    empirical_g2_limit_gev_m2: float,
) -> dict[str, float | bool]:
    """Return required matter-coupling amplitude suppression.

    Since g^2 scales as the square of the linear matter coupling, an empirical
    reduction

        g^2 -> S^2 g^2

    requires

        S <= sqrt(g_limit^2 / g_unscreened^2).

    For a cross operator C1 proportional to one power of the same matter
    coupling, ordinary same-state screening also suppresses C1 by S unless
    another interaction changes between the off and active states.
    """

    unscreened = float(
        unscreened_g2_gev_m2
    )

    limit = float(
        empirical_g2_limit_gev_m2
    )

    if (
        unscreened <= 0.0
        or limit <= 0.0
    ):
        raise ValueError(
            "screening strengths must be positive"
        )

    amplitude = min(
        1.0,
        math.sqrt(
            limit
            / unscreened
        ),
    )

    return {
        "required_matter_amplitude_retention_max":
            amplitude,

        "same_vertex_c1_retention_max":
            amplitude,

        "same_vertex_target_preserved_without_descreening":
            (
                amplitude
                >=
                0.95
            ),

        "active_x_dependent_descreening_required_for_rescue":
            (
                amplitude
                <
                0.95
            ),
    }


def z2_loop_generated_xt_scale(
    *,
    target_c1_ev_m4: float,
    loop_denominator: float = (
        32.0
        * math.pi**2
    ),
) -> dict[str, float | bool | str]:
    """Return equal-portal scale for a Z2-even one-loop XT scaffold.

    Uses only the dimensional scout

        C1
            ~
            1/(D F^4),

    where D defaults to 32 pi^2.

    This is not a prediction because XT is an allowed local counterterm.
    """

    c1 = float(
        target_c1_ev_m4
    )

    denominator = float(
        loop_denominator
    )

    if (
        c1 <= 0.0
        or denominator <= 0.0
    ):
        raise ValueError(
            "invalid loop scaffold input"
        )

    portal_scale = (
        1.0
        /
        (
            denominator
            * c1
        )
    )**0.25

    return {
        "equal_portal_scale_ev":
            portal_scale,

        "nominal_4pi_portal_scale_ev":
            FOUR_PI
            * portal_scale,

        "linear_offstate_single_mediator_yukawa":
            False,

        "z2_symmetry_available":
            True,

        "xt_counterterm_symmetry_allowed":
            True,

        "loop_matching_logarithmically_uv_sensitive":
            True,

        "finite_c1_sign_predicted_without_uv_boundary_condition":
            False,

        "complete_uv_origin":
            False,

        "classification":
            "YELLOW_MATCHING_SCAFFOLD",
    }


def atlas_records() -> list[dict[str, object]]:
    """Return the theorem-first UV family ranking after R3."""

    return [
        {
            "family":
                "SINGLE_LINEAR_UNIVERSAL_TRACE_SCALAR",

            "status":
                "CLOSED_R3",

            "reason":
                "OFFSTATE_YUKAWA_PLUS_RANKONE_COMPANIONS",
        },
        {
            "family":
                "NARROW_BAND_LINEAR_SCALAR_TOWER_CURRENT_SOURCE",

            "status":
                "TEST_WITH_R4_CAUCHY_BOUND",

            "reason":
                "SPECIES_SPLITTING_CANNOT_EVADE_CAUCHY_TRADEOFF",
        },
        {
            "family":
                "BROAD_SPECTRAL_LINEAR_SCALAR_TOWER",

            "status":
                "YELLOW",

            "reason":
                "MULTI_YUKAWA_EXPERIMENTAL_LIKELIHOOD_REQUIRED",
        },
        {
            "family":
                "DENSITY_ONLY_SCREENING_OF_SAME_TRACE_VERTEX",

            "status":
                "RED_AS_DIRECT_RESCUE",

            "reason":
                "SCREENS_ACTIVE_C1_WITH_OFFSTATE_FORCE",
        },
        {
            "family":
                "ACTIVE_X_DEPENDENT_SCREENING_DESCREENING",

            "status":
                "YELLOW_NEW_PHYSICS",

            "reason":
                "MUST_EXPLICITLY_SEPARATE_OFFSTATE_AND_ACTIVE_COUPLING",
        },
        {
            "family":
                "DIRECT_SHIFT_PROTECTED_GOLDSTONE_KINETIC_METRIC",

            "status":
                "YELLOW_HIGHEST_PRIORITY",

            "reason":
                "NO_DIRECT_YUKAWA_BUT_REQUIRED_OUTWARD_UV_SIGN_NOT_PROVED",
        },
        {
            "family":
                "Z2_LOOP_GENERATED_J0_PORTAL",

            "status":
                "YELLOW_SECOND_PRIORITY",

            "reason":
                "NO_LINEAR_YUKAWA_BUT_LOCAL_XT_COUNTERTERM_REQUIRES_UV_MATCH",
        },
        {
            "family":
                "TREE_SPIN2_POSITIVE_C1",

            "status":
                "CLOSED",

            "reason":
                "COMPANION_J2_AND_PRIOR_SPIN2_CLOSEOUT",
        },
        {
            "family":
                "PUBLISHED_MINIMAL_ASYMMETRON",

            "status":
                "CLOSED_FOR_EXTERNAL_TRUE_REPULSION",

            "reason":
                "WRONG_EXTERNAL_SIGN_AND_FREE_BUBBLE_INSTABILITY",
        },
    ]
