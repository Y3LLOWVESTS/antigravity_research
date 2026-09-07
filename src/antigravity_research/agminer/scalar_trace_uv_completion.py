"""032V19R3 single-scalar universal-trace UV completion diagnostics.

PURPOSE
-------
Test a genuinely different UV origin for the positive-C1 kinetic-conformal
operator that does not invoke the already-rejected spin-2 realization.

Consider one healthy canonical real scalar mediator sigma with

    L_sigma
        =
        1/2 (partial sigma)^2
        -
        1/2 m_sigma^2 sigma^2
        +
        sigma
        (
            T/F_T
            -
            X/F_X
        )

where

    X = (partial phi)^2

and ordinary matter couples universally through

    S_m[
        exp(2 sigma/F_T) g_mu_nu,
        psi_m
    ].

At momenta well below m_sigma, integrating out sigma gives

    Delta L_eff
        =
        1/(2 m_sigma^2)
        (
            T/F_T
            -
            X/F_X
        )^2

and therefore

    Delta L_eff
        =
        - C1 X T
        + D_X X^2
        + D_T T^2

with

    C1
        =
        1/(m_sigma^2 F_X F_T)

    D_X
        =
        1/(2 m_sigma^2 F_X^2)

    D_T
        =
        1/(2 m_sigma^2 F_T^2).

For positive m_sigma^2 and real couplings,

    C1^2
        =
        4 D_X D_T.

Thus this single-mediator realization has a rank-one positive-semidefinite
companion-operator matrix.  The desired cross operator cannot be generated
without both scalar companions.

SIGN
----
The cross term is

    - C1 X T.

Expanding a universal physical metric

    A(X)
        =
        1
        -
        C1 X
        + ...

produces exactly this matter-trace term.

For a static scalar configuration,

    X
        =
        - |grad phi|^2,

so C1 > 0 gives

    A
        =
        1
        +
        C1 |grad phi|^2,

which is the outward V13-V19 target for a localized gradient decreasing away
from the source.

There are no tree-level j=2 / spin-2 companion operators in this template.

OFF-STATE FORCE
---------------
The same universal sigma T/F_T interaction gives nonrelativistic bodies scalar
charge

    Q_sigma
        =
        m/F_T.

Hence sigma mediates

    V_sigma(r)
        =
        - m1 m2
          /(4 pi F_T^2)
          exp(-m_sigma r)/r.

This maps directly to the mass-coupled Yukawa convention

    V_new(r)
        =
        - g^2 Q1 Q2
          /(4 pi)
          exp(-mu r)/r

through

    g^2
        =
        1/F_T^2

when F_T is expressed in GeV.

This is an off-state laboratory observable and does not rely on a cosmological
scalar background.

WEAK-MEDIATOR BEST CASE
-----------------------
The sigma-X interaction is dimension five.

Using the optimistic NDA condition

    m_sigma
        <=
        4 pi F_X,

the weakest possible ordinary-matter coupling at fixed m_sigma and C1 is
obtained on the boundary

    F_X
        =
        m_sigma/(4 pi).

Then

    F_T,max
        =
        4 pi
        /
        (C1 m_sigma^3).

Any positive safety factor above the NDA boundary makes F_X larger, F_T
smaller, and the fifth-force problem worse.

FINITE SPHERE FIELD ENERGY
--------------------------
For a uniform nonrelativistic trace source with

    (- Laplacian + m^2) sigma
        =
        J

inside a sphere of radius R, the exact positive mediator-field inventory is

    E_sigma
        =
        1/2 integral J sigma dV.

Relative to the local bulk result

    E_local
        =
        J^2 V/(2 m^2),

the exact finite-sphere factor is

    F(x)
        =
        1
        -
        3(x+1)/(2 x^3)
        [
            (x-1)
            +
            (x+1) exp(-2x)
        ],

where

    x
        =
        m R/(hbar c).

For the current 10-cm payload and eV-scale mediator, x is enormous and this
factor is extremely close to one.

CONSERVATIVE ENERGY POLICY
--------------------------
The routines below charge the POSITIVE mediator field inventory.

They do not use negative binding energy to reduce the device ledger.

The payload-only trace inventory is a LOWER BOUND on the universal mediator
cost because the source, support wall, controls, and other ordinary matter
also carry trace and are not included here.

EMPIRICAL PROVENANCE
--------------------
Kamiya et al., Phys. Rev. Lett. 114, 161101 (2015),
DOI 10.1103/PhysRevLett.114.161101:

- mass-coupled Yukawa interaction;
- 95 percent limit at 0.1 nm:
      g^2 < 1.4e-14 GeV^-2
- 95 percent limit at 1.0 nm:
      g^2 < 1.3e-16 GeV^-2
- reported improvement over interaction ranges 0.04 to 4 nm.

The constant

    1e-12 GeV^-2

used below is NOT a tabulated experimental point.

It is an intentionally very weak graphical envelope above the published
Fig. 5 exclusion curve over only the narrower 0.60 to 3.50 nm interval
needed by this run.

The exact 0.1-nm and 1.0-nm anchors are kept separately.

CLAIM LIMITS
------------
A red result closes only the:

    SINGLE
    CANONICAL
    LINEAR
    UNSCREENED
    UNIVERSAL-TRACE
    SCALAR-EXCHANGE

UV template.

It does not close:

- nonlinear screened scalar completions;
- loop-generated j=0 completions;
- collective/multi-mediator completions;
- more fundamental kinetic-metric UV structures;
- the kinetic-conformal class as a whole.

No negative-mass matter is used anywhere in this template.
"""

from __future__ import annotations

import math

from antigravity_research.agminer.kinetic_conformal import (
    EV_J,
    HBARC_EV_M,
)


C_LIGHT = 299792458.0
FOUR_PI = 4.0 * math.pi

KAMIYA_DOI = "10.1103/PhysRevLett.114.161101"

KAMIYA_RANGE_MIN_NM = 0.04
KAMIYA_RANGE_MAX_NM = 4.0

KAMIYA_LIMIT_0P1_NM_GEV_M2 = 1.4e-14
KAMIYA_LIMIT_1P0_NM_GEV_M2 = 1.3e-16

# Deliberately loose visual envelope above the published Fig. 5 curve over
# the ONLY interval required by this gate.
#
# This is not a digitized/tabulated experimental limit.
KAMIYA_GRAPHICAL_SCOUT_MIN_NM = 0.60
KAMIYA_GRAPHICAL_SCOUT_MAX_NM = 3.50
KAMIYA_ULTRACONSERVATIVE_GRAPHICAL_ENVELOPE_GEV_M2 = 1.0e-12


def scalar_trace_tree_match(
    *,
    mediator_mass_ev: float,
    f_x_ev: float,
    f_t_ev: float,
) -> dict[str, float | bool | str]:
    """Return tree-level Wilson coefficients from one canonical scalar."""

    mass = float(
        mediator_mass_ev
    )

    f_x = float(
        f_x_ev
    )

    f_t = float(
        f_t_ev
    )

    if (
        mass <= 0.0
        or f_x <= 0.0
        or f_t <= 0.0
    ):
        raise ValueError(
            "positive mediator mass and coupling scales required"
        )

    c1 = (
        1.0
        /
        (
            mass**2
            * f_x
            * f_t
        )
    )

    d_x = (
        1.0
        /
        (
            2.0
            * mass**2
            * f_x**2
        )
    )

    d_t = (
        1.0
        /
        (
            2.0
            * mass**2
            * f_t**2
        )
    )

    identity_left = (
        c1**2
    )

    identity_right = (
        4.0
        * d_x
        * d_t
    )

    identity_relative_error = (
        abs(
            identity_left
            - identity_right
        )
        /
        identity_left
    )

    return {
        "c1_ev_m4":
            c1,

        "cross_xt_coefficient_ev_m4":
            -c1,

        "d_x_ev_m4":
            d_x,

        "d_t_ev_m4":
            d_t,

        "rank_one_identity_relative_error":
            identity_relative_error,

        "rank_one_psd_companion_identity":
            (
                identity_relative_error
                <
                1.0e-12
            ),

        "positive_c1":
            (
                c1
                >
                0.0
            ),

        "target_metric":
            "A_EQUALS_1_MINUS_C1_X",

        "static_outward_sign_target":
            (
                c1
                >
                0.0
            ),

        "tree_spin2_companion":
            False,

        "tree_j2_companion":
            False,

        "canonical_positive_energy_mediator":
            True,

        "negative_mass_required":
            False,

        "universal_matter_metric":
            True,
    }


def weak_single_scalar_best_case(
    *,
    mediator_mass_ev: float,
    target_c1_ev_m4: float,
    nda_margin: float = 1.0,
) -> dict[str, float | bool]:
    """Return least-coupled matter portal on the sigma-X NDA boundary.

    Require

        Lambda_X
            =
            4 pi F_X
            >=
            nda_margin * m_sigma.

    For fixed C1 and m_sigma, ordinary-matter coupling is weakest when F_X
    takes its smallest allowed value.

    Therefore

        F_X,min
            =
            nda_margin m_sigma/(4 pi)

    and

        F_T,max
            =
            1/(C1 m_sigma^2 F_X,min).

    nda_margin=1 is deliberately maximally optimistic.
    """

    mass = float(
        mediator_mass_ev
    )

    c1 = float(
        target_c1_ev_m4
    )

    margin = float(
        nda_margin
    )

    if (
        mass <= 0.0
        or c1 <= 0.0
        or margin < 1.0
    ):
        raise ValueError(
            "invalid weak-mediator input"
        )

    f_x = (
        margin
        * mass
        / FOUR_PI
    )

    f_t = (
        1.0
        /
        (
            c1
            * mass**2
            * f_x
        )
    )

    f_t_gev = (
        f_t
        * 1.0e-9
    )

    g2 = (
        1.0
        / f_t_gev**2
    )

    interaction_range_nm = (
        HBARC_EV_M
        / mass
        * 1.0e9
    )

    matching = (
        scalar_trace_tree_match(
            mediator_mass_ev=
                mass,

            f_x_ev=
                f_x,

            f_t_ev=
                f_t,
        )
    )

    return {
        "mediator_mass_ev":
            mass,

        "nda_margin":
            margin,

        "f_x_ev":
            f_x,

        "x_portal_nda_cutoff_ev":
            FOUR_PI
            * f_x,

        "f_t_ev":
            f_t,

        "f_t_gev":
            f_t_gev,

        "mass_force_g2_gev_m2":
            g2,

        "interaction_range_nm":
            interaction_range_nm,

        "c1_ev_m4":
            float(
                matching[
                    "c1_ev_m4"
                ]
            ),

        "d_x_ev_m4":
            float(
                matching[
                    "d_x_ev_m4"
                ]
            ),

        "d_t_ev_m4":
            float(
                matching[
                    "d_t_ev_m4"
                ]
            ),

        "rank_one_psd_companion_identity":
            bool(
                matching[
                    "rank_one_psd_companion_identity"
                ]
            ),

        "tree_spin2_companion":
            False,

        "negative_mass_required":
            False,
    }


def uniform_sphere_yukawa_factor(
    x: float,
) -> float:
    """Return exact finite-sphere factor for a uniform Yukawa source."""

    value = float(
        x
    )

    if value <= 0.0:
        raise ValueError(
            "x must be positive"
        )

    if value < 1.0e-3:
        # Stable small-x expansion.
        return (
            2.0
            * value**2
            / 5.0
            -
            value**3
            / 3.0
            +
            6.0
            * value**4
            / 35.0
            -
            value**5
            / 15.0
            +
            4.0
            * value**6
            / 189.0
        )

    exponential = (
        math.exp(
            -2.0
            * value
        )
        if value
        <
        350.0
        else 0.0
    )

    factor = (
        1.0
        -
        (
            3.0
            * (
                value
                + 1.0
            )
            /
            (
                2.0
                * value**3
            )
        )
        * (
            (
                value
                - 1.0
            )
            +
            (
                value
                + 1.0
            )
            * exponential
        )
    )

    if (
        factor <= 0.0
        or factor > 1.0
    ):
        raise RuntimeError(
            "invalid uniform-sphere Yukawa factor"
        )

    return factor


def nonrelativistic_trace_density_ev4(
    *,
    mass_kg: float,
    radius_m: float,
    trace_fraction: float = 1.0,
) -> dict[str, float]:
    """Return uniform nonrelativistic matter-trace density."""

    mass = float(
        mass_kg
    )

    radius = float(
        radius_m
    )

    fraction = float(
        trace_fraction
    )

    if (
        mass <= 0.0
        or radius <= 0.0
        or not (
            0.0
            <
            fraction
            <=
            1.0
        )
    ):
        raise ValueError(
            "invalid trace source"
        )

    volume_m3 = (
        4.0
        * math.pi
        * radius**3
        / 3.0
    )

    trace_density_j_m3 = (
        fraction
        * mass
        * C_LIGHT**2
        / volume_m3
    )

    trace_density_ev4 = (
        trace_density_j_m3
        * HBARC_EV_M**3
        / EV_J
    )

    volume_ev_m3 = (
        volume_m3
        / HBARC_EV_M**3
    )

    return {
        "volume_m3":
            volume_m3,

        "volume_ev_m3":
            volume_ev_m3,

        "trace_density_j_m3":
            trace_density_j_m3,

        "trace_density_ev4":
            trace_density_ev4,
    }


def uniform_sphere_trace_field_energy_j(
    *,
    mediator_mass_ev: float,
    f_t_ev: float,
    source_mass_kg: float,
    source_radius_m: float,
    trace_fraction: float = 1.0,
) -> dict[str, float | str | bool]:
    """Return positive mediator field inventory from a uniform trace source."""

    mediator_mass = float(
        mediator_mass_ev
    )

    f_t = float(
        f_t_ev
    )

    if (
        mediator_mass <= 0.0
        or f_t <= 0.0
    ):
        raise ValueError(
            "positive mediator parameters required"
        )

    source = (
        nonrelativistic_trace_density_ev4(
            mass_kg=
                source_mass_kg,

            radius_m=
                source_radius_m,

            trace_fraction=
                trace_fraction,
        )
    )

    d_t = (
        1.0
        /
        (
            2.0
            * mediator_mass**2
            * f_t**2
        )
    )

    local_energy_j = (
        d_t
        * float(
            source[
                "trace_density_ev4"
            ]
        )**2
        * float(
            source[
                "volume_ev_m3"
            ]
        )
        * EV_J
    )

    x = (
        mediator_mass
        * float(
            source_radius_m
        )
        / HBARC_EV_M
    )

    finite_factor = (
        uniform_sphere_yukawa_factor(
            x
        )
    )

    exact_energy_j = (
        local_energy_j
        * finite_factor
    )

    return {
        "m_r_over_hbarc":
            x,

        "finite_sphere_factor":
            finite_factor,

        "local_bulk_positive_field_inventory_j":
            local_energy_j,

        "exact_positive_field_inventory_j":
            exact_energy_j,

        "conservative_ledger_charge_j":
            exact_energy_j,

        "negative_binding_credit_applied":
            False,

        "source_and_support_trace_included":
            False,

        "interpretation":
            "PAYLOAD_ONLY_UNIVERSAL_TRACE_MEDIATOR_LOWER_BOUND",
    }


def uniform_source_x_field_energy_j(
    *,
    mediator_mass_ev: float,
    f_x_ev: float,
    axial_b_ev: float,
    f_psi_ev: float,
    source_radius_m: float,
) -> dict[str, float]:
    """Return the positive X-companion field inventory for a uniform source.

    For the axial source convention,

        |grad phi|
            =
            b f_psi.

    Hence

        |X|
            =
            (b f_psi)^2.

    Only the X-source contribution is included here.
    """

    mass = float(
        mediator_mass_ev
    )

    f_x = float(
        f_x_ev
    )

    b_value = float(
        axial_b_ev
    )

    f_psi = float(
        f_psi_ev
    )

    radius = float(
        source_radius_m
    )

    if (
        mass <= 0.0
        or f_x <= 0.0
        or b_value <= 0.0
        or f_psi <= 0.0
        or radius <= 0.0
    ):
        raise ValueError(
            "invalid X-source input"
        )

    x_magnitude_ev4 = (
        b_value
        * f_psi
    )**2

    d_x = (
        1.0
        /
        (
            2.0
            * mass**2
            * f_x**2
        )
    )

    volume_m3 = (
        4.0
        * math.pi
        * radius**3
        / 3.0
    )

    volume_ev_m3 = (
        volume_m3
        / HBARC_EV_M**3
    )

    local_energy_j = (
        d_x
        * x_magnitude_ev4**2
        * volume_ev_m3
        * EV_J
    )

    x_geometry = (
        mass
        * radius
        / HBARC_EV_M
    )

    finite_factor = (
        uniform_sphere_yukawa_factor(
            x_geometry
        )
    )

    return {
        "x_magnitude_ev4":
            x_magnitude_ev4,

        "d_x_ev_m4":
            d_x,

        "finite_sphere_factor":
            finite_factor,

        "positive_x_field_inventory_j":
            local_energy_j
            * finite_factor,
    }


def practical_mediator_mass_ceiling_ev(
    *,
    minimum_mass_ev: float,
    target_c1_ev_m4: float,
    base_static_energy_j: float,
    energy_limit_j: float,
    payload_mass_kg: float,
    payload_radius_m: float,
    nda_margin: float = 1.0,
) -> dict[str, float | bool]:
    """Find the optimistic mediator mass where payload field + base = limit.

    Only the payload trace mediator field is added.

    Therefore the resulting mass ceiling is optimistic: omitted universal
    source/support trace can only tighten it.
    """

    minimum_mass = float(
        minimum_mass_ev
    )

    c1 = float(
        target_c1_ev_m4
    )

    base = float(
        base_static_energy_j
    )

    limit = float(
        energy_limit_j
    )

    if (
        minimum_mass <= 0.0
        or c1 <= 0.0
        or base < 0.0
        or limit <= base
    ):
        raise ValueError(
            "invalid practical mass ceiling input"
        )

    def total_energy(
        mediator_mass: float,
    ) -> float:
        weak = (
            weak_single_scalar_best_case(
                mediator_mass_ev=
                    mediator_mass,

                target_c1_ev_m4=
                    c1,

                nda_margin=
                    nda_margin,
            )
        )

        field = (
            uniform_sphere_trace_field_energy_j(
                mediator_mass_ev=
                    mediator_mass,

                f_t_ev=
                    float(
                        weak[
                            "f_t_ev"
                        ]
                    ),

                source_mass_kg=
                    payload_mass_kg,

                source_radius_m=
                    payload_radius_m,
            )
        )

        return (
            base
            +
            float(
                field[
                    "conservative_ledger_charge_j"
                ]
            )
        )

    minimum_total = (
        total_energy(
            minimum_mass
        )
    )

    if minimum_total >= limit:
        return {
            "window_exists":
                False,

            "minimum_mass_ev":
                minimum_mass,

            "minimum_total_j":
                minimum_total,

            "mass_ceiling_ev":
                minimum_mass,

            "mass_ceiling_range_nm":
                HBARC_EV_M
                / minimum_mass
                * 1.0e9,

            "energy_at_ceiling_j":
                minimum_total,
        }

    low = minimum_mass
    high = 2.0 * minimum_mass

    while (
        total_energy(
            high
        )
        <
        limit
    ):
        high *= 2.0

        if high > 1.0e7:
            raise RuntimeError(
                "failed to bracket practical mediator mass ceiling"
            )

    for _ in range(
        100
    ):
        middle = (
            0.5
            * (
                low
                + high
            )
        )

        if (
            total_energy(
                middle
            )
            <
            limit
        ):
            low = middle
        else:
            high = middle

    ceiling = (
        0.5
        * (
            low
            + high
        )
    )

    ceiling_total = (
        total_energy(
            ceiling
        )
    )

    return {
        "window_exists":
            True,

        "minimum_mass_ev":
            minimum_mass,

        "minimum_total_j":
            minimum_total,

        "mass_ceiling_ev":
            ceiling,

        "mass_ceiling_range_nm":
            HBARC_EV_M
            / ceiling
            * 1.0e9,

        "energy_at_ceiling_j":
            ceiling_total,

        "strictly_allowed_requires_mass_below_ceiling":
            True,

        "payload_trace_only_lower_bound":
            True,
    }


def kamiya_exact_anchor(
    range_nm: float,
) -> dict[str, float | str]:
    """Return one exact published Kamiya 95-percent anchor."""

    value = float(
        range_nm
    )

    if math.isclose(
        value,
        1.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ):
        limit = (
            KAMIYA_LIMIT_1P0_NM_GEV_M2
        )

    elif math.isclose(
        value,
        0.1,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    ):
        limit = (
            KAMIYA_LIMIT_0P1_NM_GEV_M2
        )

    else:
        raise ValueError(
            "only exact 0.1-nm and 1.0-nm anchors are tabulated here"
        )

    return {
        "range_nm":
            value,

        "mediator_mass_ev":
            HBARC_EV_M
            / (
                value
                * 1.0e-9
            ),

        "limit_g2_gev_m2":
            limit,

        "confidence":
            "95_PERCENT",

        "provenance":
            KAMIYA_DOI,
    }


def graphical_empirical_scout(
    *,
    interaction_range_nm: float,
    predicted_g2_gev_m2: float,
) -> dict[str, float | bool | str]:
    """Compare with deliberately weakened published-curve envelope."""

    range_nm = float(
        interaction_range_nm
    )

    g2 = float(
        predicted_g2_gev_m2
    )

    if (
        range_nm <= 0.0
        or g2 <= 0.0
    ):
        raise ValueError(
            "invalid empirical scout input"
        )

    in_scope = (
        KAMIYA_GRAPHICAL_SCOUT_MIN_NM
        <= range_nm
        <= KAMIYA_GRAPHICAL_SCOUT_MAX_NM
    )

    ratio = (
        g2
        /
        KAMIYA_ULTRACONSERVATIVE_GRAPHICAL_ENVELOPE_GEV_M2
    )

    return {
        "range_nm":
            range_nm,

        "predicted_g2_gev_m2":
            g2,

        "graphical_envelope_g2_gev_m2":
            KAMIYA_ULTRACONSERVATIVE_GRAPHICAL_ENVELOPE_GEV_M2,

        "predicted_over_graphical_envelope":
            ratio,

        "within_graphical_scout_scope":
            in_scope,

        "excluded_by_graphical_envelope_scout":
            (
                in_scope
                and ratio > 1.0
            ),

        "envelope_is_tabulated_limit":
            False,

        "source":
            "KAMIYA_2015_FIGURE_5_INTENTIONALLY_LOOSE_ENVELOPE",
    }
