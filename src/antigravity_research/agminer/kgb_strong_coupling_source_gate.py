"""032V25B minimal-cubic KGB source-scale and strong-coupling preflight.

PURPOSE
-------
V25A established an explicit shift-symmetric cubic Horndeski / kinetic-gravity-
braiding action with:

1. one universal physical metric;
2. ordinary matter minimally coupled to that metric;
3. the historical hidden-axial derivative source operator;
4. tree-level active/off-state separation;
5. a nonzero active debraided matter response.

V25B asks a deliberately cheaper falsification question before attempting a
new coupled source PDE, RG resummation, finite-payload calculation, or energy
optimization:

    Can the historical V16 loop-0.30 hidden-axial source benchmark be
    transplanted unchanged into the minimal cubic KGB action while the
    canonically normalized cubic fluctuation operator remains above the
    source's own spatial variation momentum?

MINIMAL CUBIC RELATIONS
-----------------------
Absorb the dimensionless cubic coefficient into an effective scale Lambda_3,

    1 / Lambda_3^3
        =
        |beta| / Lambda^3.

For the static spacelike background used in V25A,

    y
        =
        |grad(phi)|^4
        /
        (2 Mpl^2 Lambda_3^6),

and

    Z_min
        =
        1-y.

The cubic fluctuation operator schematically contains

    (d pi)^2 Box(pi)
    /
    Lambda_3^3.

After canonical normalization

    pi_c
        =
        sqrt(Z_min) pi,

its local cubic suppression scale is

    Lambda_eff
        =
        Lambda_3 sqrt(Z_min).

Local cubic EFT control on a source scale L therefore minimally requires

    Lambda_eff
        >=
        n k_source,

where

    k_source
        =
        hbar c / L

and n is a chosen control margin.

For a requested Planck-normalized active coupling

    A
        =
        Mpl |g_c|,

V25A gave

    A^2
        =
        y
        /
        [2(1-y)].

Combining the relations gives an analytic source-gradient requirement,

    |grad(phi)|_required
        =
        [
            2 Mpl^2 y
            (n k_source)^6
            /
            (1-y)^3
        ]^(1/4).

HISTORICAL SOURCE BENCHMARK
---------------------------
The benchmark is the V16 selected loop-0.30 positive-band corridor:

    f_psi
        ~ 27.14469 eV

    b
        ~ 20.32104 eV

    mu
        ~ 66.61671 eV

    cutoff
        ~ 341.11024 eV

    hard margin
        ~ 5.12049.

The historical source convention is

    |grad(phi)|
        =
        b f_psi.

The shortest V15/V16 oblate source dimension is

    c
        ~ 0.0965912 m.

CLAIM BOUNDARY
--------------
Failure of this test closes only:

    UNCHANGED V16 LOOP-0.30 SOURCE
        +
    MINIMAL CUBIC KGB
        +
    LOCAL CANONICAL CUBIC EFT CONTROL
        ON THE HISTORICAL SOURCE SCALE.

It does NOT close:

- generalized K(X)+G3(X);
- weakly-broken-Galileon completions;
- multiscale KGB;
- large-Z or Vainshtein regimes with separately controlled interactions;
- alternative hidden-source microstates;
- higher-cutoff source sectors;
- the full tensor Horndeski theory;
- nonlinear metric response;
- the V25A action-existence result itself.

The two-field positive kinetic-block identity is also recorded:

    K =
        [[a,b],
         [b,c]]

with

    a>0,
    c>0,
    ac-b^2>0.

Writing

    rho
        =
        b / sqrt(ac),

the inverse propagator satisfies

    |G_12|
    /
    sqrt(G_11 G_22)
        =
        |rho|
        <
        1.

Thus normalized quadratic mixing alone cannot become arbitrarily large
without approaching a kinetic degeneracy. This identity is not a generalized
KGB no-go theorem.

No action oracle, candidate, survivor, energy optimization, or physical-device
claim is created.

CLAIM_CLASSIFICATION=
LOCAL_CANONICAL_CUBIC_EFT_AND_HISTORICAL_SOURCE_SCALE_FALSIFICATION
"""

from __future__ import annotations

import math
from typing import Any

from .storage import Storage


MPL_REDUCED_EV = 2.435e27
HBARC_EV_M = 1.973269804e-7


# ---------------------------------------------------------------------------
# Historical V16 selected loop-0.30 source benchmark.
# ---------------------------------------------------------------------------

V16_F_PSI_EV = 27.144690651647558
V16_B_AXIAL_EV = 20.32104381556904
V16_M_PSI_EV = 24.96671585947364
V16_MU_EV = 66.61670965827027
V16_CUTOFF_EV = 341.110242940734
V16_HARD_MARGIN = 5.120490710071961

V16_SOURCE_A_M = 0.25740088555864965
V16_SOURCE_C_M = 0.09659120999271102


def gain_to_y(
    gain_times_planck: float,
) -> float:
    """Convert A=Mpl|g_c| into the V25A dimensionless y."""

    gain = float(
        gain_times_planck
    )

    if (
        not math.isfinite(
            gain
        )
        or gain < 0.0
    ):
        raise ValueError(
            "gain must be finite and non-negative"
        )

    gain_squared = (
        gain
        *
        gain
    )

    return (
        2.0
        *
        gain_squared
        /
        (
            1.0
            +
            2.0
            *
            gain_squared
        )
    )


def y_to_gain(
    y: float,
) -> float:
    """Invert the V25A canonical gain relation."""

    value = float(
        y
    )

    if (
        not math.isfinite(
            value
        )
        or not (
            0.0
            <=
            value
            <
            1.0
        )
    ):
        raise ValueError(
            "y must satisfy 0 <= y < 1"
        )

    if value == 0.0:
        return 0.0

    return math.sqrt(
        value
        /
        (
            2.0
            *
            (
                1.0
                -
                value
            )
        )
    )


def characteristic_momentum_ev(
    length_m: float,
) -> float:
    """Return hbar*c/L in eV."""

    length = float(
        length_m
    )

    if (
        not math.isfinite(
            length
        )
        or length <= 0.0
    ):
        raise ValueError(
            "length_m must be positive and finite"
        )

    return (
        HBARC_EV_M
        /
        length
    )


def source_gradient_ev2(
    *,
    axial_b_ev: float,
    f_psi_ev: float,
) -> float:
    """Return the historical axial-source scalar-gradient convention.

    The V15-V19 convention is

        |grad(phi)|
            =
            b f_psi.
    """

    b_value = float(
        axial_b_ev
    )

    f_value = float(
        f_psi_ev
    )

    if (
        not math.isfinite(
            b_value
        )
        or
        not math.isfinite(
            f_value
        )
        or b_value < 0.0
        or f_value <= 0.0
    ):
        raise ValueError(
            "invalid source parameters"
        )

    return (
        b_value
        *
        f_value
    )


def cubic_scale_from_gradient_y(
    *,
    gradient_ev2: float,
    y: float,
) -> float:
    """Return Lambda_3 implied by gradient and V25A y."""

    gradient = float(
        gradient_ev2
    )

    value = float(
        y
    )

    if (
        not math.isfinite(
            gradient
        )
        or gradient <= 0.0
    ):
        raise ValueError(
            "gradient_ev2 must be positive and finite"
        )

    if (
        not math.isfinite(
            value
        )
        or not (
            0.0
            <
            value
            <
            1.0
        )
    ):
        raise ValueError(
            "y must satisfy 0 < y < 1"
        )

    return (
        gradient**4
        /
        (
            2.0
            *
            MPL_REDUCED_EV**2
            *
            value
        )
    )**(
        1.0
        /
        6.0
    )


def local_canonical_cubic_scale(
    *,
    gradient_ev2: float,
    y: float,
) -> float:
    """Return Lambda_eff=Lambda_3*sqrt(1-y)."""

    value = float(
        y
    )

    lambda_3 = (
        cubic_scale_from_gradient_y(
            gradient_ev2=
                gradient_ev2,

            y=
                value,
        )
    )

    return (
        lambda_3
        *
        math.sqrt(
            1.0
            -
            value
        )
    )


def control_ratio(
    *,
    gradient_ev2: float,
    length_m: float,
    gain_times_planck: float,
) -> float:
    """Return Lambda_eff/k_source for one background state."""

    gain = float(
        gain_times_planck
    )

    if gain == 0.0:
        return math.inf

    y = gain_to_y(
        gain
    )

    return (
        local_canonical_cubic_scale(
            gradient_ev2=
                gradient_ev2,

            y=
                y,
        )
        /
        characteristic_momentum_ev(
            length_m
        )
    )


def required_gradient_for_control(
    *,
    length_m: float,
    gain_times_planck: float,
    control_margin: float = 1.0,
) -> float:
    """Return minimum |grad(phi)| for Lambda_eff >= margin*k_source."""

    gain = float(
        gain_times_planck
    )

    margin = float(
        control_margin
    )

    if (
        not math.isfinite(
            margin
        )
        or margin <= 0.0
    ):
        raise ValueError(
            "control_margin must be positive and finite"
        )

    if gain == 0.0:
        return 0.0

    y = gain_to_y(
        gain
    )

    k_source = (
        characteristic_momentum_ev(
            length_m
        )
    )

    return (
        2.0
        *
        MPL_REDUCED_EV**2
        *
        y
        *
        (
            margin
            *
            k_source
        )**6
        /
        (
            1.0
            -
            y
        )**3
    )**0.25


def max_gain_for_gradient_cap(
    *,
    gradient_cap_ev2: float,
    length_m: float,
    control_margin: float = 1.0,
) -> dict[
    str,
    float,
]:
    """Return the largest A allowed by a gradient cap and local control.

    The control condition is

        y / (1-y)^3
            <=
        S

    where

        S
            =
        gradient^4
        /
        [2 Mpl^2 (margin*k)^6].

    The left side is monotonic for 0 <= y < 1, so bisection gives the unique
    limiting y.
    """

    gradient = float(
        gradient_cap_ev2
    )

    margin = float(
        control_margin
    )

    if (
        not math.isfinite(
            gradient
        )
        or gradient <= 0.0
    ):
        raise ValueError(
            "gradient cap must be positive and finite"
        )

    if (
        not math.isfinite(
            margin
        )
        or margin <= 0.0
    ):
        raise ValueError(
            "control_margin must be positive and finite"
        )

    k_source = (
        characteristic_momentum_ev(
            length_m
        )
    )

    s_parameter = (
        gradient**4
        /
        (
            2.0
            *
            MPL_REDUCED_EV**2
            *
            (
                margin
                *
                k_source
            )**6
        )
    )

    low = 0.0
    high = (
        1.0
        -
        1.0e-15
    )

    for _ in range(
        220
    ):
        middle = (
            0.5
            *
            (
                low
                +
                high
            )
        )

        left_side = (
            middle
            /
            (
                1.0
                -
                middle
            )**3
        )

        if (
            left_side
            <=
            s_parameter
        ):
            low = middle

        else:
            high = middle

    maximum_y = low

    return {
        "maximum_y":
            maximum_y,

        "maximum_gain_times_planck":
            y_to_gain(
                maximum_y
            ),

        "control_margin":
            margin,

        "source_scale_ev":
            k_source,

        "s_parameter":
            s_parameter,
    }


def historical_v16_source_benchmark() -> dict[
    str,
    Any,
]:
    """Return the historical source-scale benchmark used by V25B."""

    gradient = (
        source_gradient_ev2(
            axial_b_ev=
                V16_B_AXIAL_EV,

            f_psi_ev=
                V16_F_PSI_EV,
        )
    )

    source_momentum = (
        characteristic_momentum_ev(
            V16_SOURCE_C_M
        )
    )

    hard_margin_b_cap = (
        V16_CUTOFF_EV
        /
        V16_HARD_MARGIN
    )

    return {
        "f_psi_ev":
            V16_F_PSI_EV,

        "axial_b_ev":
            V16_B_AXIAL_EV,

        "m_psi_ev":
            V16_M_PSI_EV,

        "chemical_potential_ev":
            V16_MU_EV,

        "nda_cutoff_ev":
            V16_CUTOFF_EV,

        "hard_scale_margin":
            V16_HARD_MARGIN,

        "source_a_m":
            V16_SOURCE_A_M,

        "source_c_m":
            V16_SOURCE_C_M,

        "gradient_ev2":
            gradient,

        "source_variation_momentum_ev":
            source_momentum,

        "hard_margin_b_cap_ev":
            hard_margin_b_cap,

        "hard_margin_gradient_cap_ev2":
            (
                V16_F_PSI_EV
                *
                hard_margin_b_cap
            ),

        "relaxed_cutoff_gradient_cap_ev2":
            (
                V16_F_PSI_EV
                *
                V16_CUTOFF_EV
            ),

        "historical_source_is_current_physical_model":
            False,
    }


def historical_source_compatibility() -> dict[
    str,
    Any,
]:
    """Return the unchanged-V16/minimal-cubic compatibility bounds."""

    source = (
        historical_v16_source_benchmark()
    )

    gradient = float(
        source[
            "gradient_ev2"
        ]
    )

    length = float(
        source[
            "source_c_m"
        ]
    )

    actual = (
        max_gain_for_gradient_cap(
            gradient_cap_ev2=
                gradient,

            length_m=
                length,

            control_margin=
                1.0,
        )
    )

    hard_margin = (
        max_gain_for_gradient_cap(
            gradient_cap_ev2=
                float(
                    source[
                        "hard_margin_gradient_cap_ev2"
                    ]
                ),

            length_m=
                length,

            control_margin=
                1.0,
        )
    )

    relaxed_cutoff = (
        max_gain_for_gradient_cap(
            gradient_cap_ev2=
                float(
                    source[
                        "relaxed_cutoff_gradient_cap_ev2"
                    ]
                ),

            length_m=
                length,

            control_margin=
                1.0,
        )
    )

    hard_margin_5 = (
        max_gain_for_gradient_cap(
            gradient_cap_ev2=
                float(
                    source[
                        "hard_margin_gradient_cap_ev2"
                    ]
                ),

            length_m=
                length,

            control_margin=
                5.0,
        )
    )

    relaxed_cutoff_5 = (
        max_gain_for_gradient_cap(
            gradient_cap_ev2=
                float(
                    source[
                        "relaxed_cutoff_gradient_cap_ev2"
                    ]
                ),

            length_m=
                length,

            control_margin=
                5.0,
        )
    )

    ratio_at_1e3 = (
        control_ratio(
            gradient_ev2=
                gradient,

            length_m=
                length,

            gain_times_planck=
                1.0e-3,
        )
    )

    return {
        **source,

        "a1e3_lambda_eff_over_source_k":
            ratio_at_1e3,

        "actual_gradient_max_controlled_gain_times_planck":
            actual[
                "maximum_gain_times_planck"
            ],

        "hard_margin_proxy_max_controlled_gain_times_planck":
            hard_margin[
                "maximum_gain_times_planck"
            ],

        "relaxed_cutoff_max_controlled_gain_times_planck":
            relaxed_cutoff[
                "maximum_gain_times_planck"
            ],

        "hard_margin_proxy_margin5_max_gain_times_planck":
            hard_margin_5[
                "maximum_gain_times_planck"
            ],

        "relaxed_cutoff_margin5_max_gain_times_planck":
            relaxed_cutoff_5[
                "maximum_gain_times_planck"
            ],

        "unchanged_v16_to_minimal_cubic_kgb_transplant_closed":
            ratio_at_1e3
            <
            1.0,

        "closure_scope":
            (
                "UNCHANGED_V16_LOOP030_SOURCE_PLUS_MINIMAL_CUBIC_KGB_"
                "LOCAL_CANONICAL_CUBIC_EFT_CONTROL"
            ),

        "generalized_kgb_closed":
            False,

        "wbg_multiscale_kgb_closed":
            False,

        "new_hidden_source_closed":
            False,
    }


def positive_2x2_mixing_diagnostics(
    *,
    metric_kinetic: float,
    scalar_kinetic: float,
    mixing: float,
) -> dict[
    str,
    Any,
]:
    """Return the exact normalized cross-response identity.

    For

        K =
            [[a,b],
             [b,c]],

    positive health requires

        a>0,
        c>0,
        ac-b^2>0.

    The inverse then obeys

        |G12| / sqrt(G11 G22)
            =
        |b| / sqrt(ac)
            =
        |rho|
            <
        1.
    """

    a_value = float(
        metric_kinetic
    )

    c_value = float(
        scalar_kinetic
    )

    b_value = float(
        mixing
    )

    if not all(
        math.isfinite(
            value
        )
        for value
        in (
            a_value,
            b_value,
            c_value,
        )
    ):
        raise ValueError(
            "finite coefficients required"
        )

    determinant = (
        a_value
        *
        c_value
        -
        b_value
        *
        b_value
    )

    healthy = bool(
        a_value > 0.0
        and
        c_value > 0.0
        and
        determinant > 0.0
    )

    if not healthy:
        return {
            "healthy":
                False,

            "determinant":
                determinant,

            "rho":
                None,

            "normalized_inverse_cross":
                None,

            "smallest_eigenvalue":
                None,
        }

    rho = (
        b_value
        /
        math.sqrt(
            a_value
            *
            c_value
        )
    )

    g11 = (
        c_value
        /
        determinant
    )

    g22 = (
        a_value
        /
        determinant
    )

    g12 = (
        -b_value
        /
        determinant
    )

    normalized = (
        abs(
            g12
        )
        /
        math.sqrt(
            g11
            *
            g22
        )
    )

    trace = (
        a_value
        +
        c_value
    )

    discriminant = math.sqrt(
        (
            a_value
            -
            c_value
        )**2
        +
        4.0
        *
        b_value
        *
        b_value
    )

    smallest = (
        0.5
        *
        (
            trace
            -
            discriminant
        )
    )

    return {
        "healthy":
            True,

        "determinant":
            determinant,

        "rho":
            rho,

        "absolute_rho":
            abs(
                rho
            ),

        "normalized_inverse_cross":
            normalized,

        "normalized_identity_error":
            abs(
                normalized
                -
                abs(
                    rho
                )
            ),

        "smallest_eigenvalue":
            smallest,

        "arbitrarily_large_normalized_cross_without_degeneracy":
            False,
    }


def protection_rg_scope() -> dict[
    str,
    Any,
]:
    """Separate bulk Galileon protection from full source-coupled RG closure."""

    return {
        "constant_shift_exact":
            True,

        "bulk_weakly_broken_galileon_protection_context":
            True,

        "hidden_axial_derivative_source_preserves_constant_shift":
            True,

        "hidden_axial_source_preserves_full_galileon_shift_phi_to_phi_plus_bx":
            False,

        "matter_or_source_loops_can_generate_additional_eft_operators":
            True,

        "full_source_coupled_rg_uv_calculated":
            False,

        "full_source_coupled_naturalness_certified":
            False,

        "status":
            "PARTIAL",
    }


def v25b_gate() -> dict[
    str,
    Any,
]:
    """Return the conservative V25B decision."""

    compatibility = (
        historical_source_compatibility()
    )

    protection = (
        protection_rg_scope()
    )

    return {
        "historical_v16_transplant":
            compatibility,

        "minimal_cubic_local_eft_control_pass_at_a1e3":
            (
                compatibility[
                    "a1e3_lambda_eff_over_source_k"
                ]
                >=
                1.0
            ),

        "unchanged_v16_minimal_cubic_transplant_closed":
            compatibility[
                "unchanged_v16_to_minimal_cubic_kgb_transplant_closed"
            ],

        "generalized_kx_g3_closed":
            False,

        "wbg_multiscale_kgb_closed":
            False,

        "alternative_hidden_source_closed":
            False,

        "full_tensor_nonremovable_crosspropagator_certified":
            False,

        "full_source_rg_uv_certified":
            protection[
                "full_source_coupled_rg_uv_calculated"
            ],

        "new_selfconsistent_kgb_hidden_source_solved":
            False,

        "outward_sign_established":
            False,

        "finite_payload_response_established":
            False,

        "source_charge_per_joule_established":
            False,

        "complete_operating_energy_established":
            False,

        "action_oracle_authorized":
            False,

        "blind_parameter_scan_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "decision":
            (
                "RED_PARTIAL_032V25B_UNCHANGED_V16_HIDDEN_AXIAL_SOURCE_"
                "TO_MINIMAL_CUBIC_KGB_FAILS_LOCAL_CANONICAL_CUBIC_EFT_"
                "CONTROL_ON_SOURCE_VARIATION_SCALE__V25A_ACTION_AND_"
                "GENERALIZED_WBG_MULTISCALE_KGB_REMAIN_OPEN"
            ),

        "next":
            (
                "032V25C_GENERALIZED_WBG_KGB_MULTISCALE_ACTION_"
                "AND_SOURCE_SCALE_GATE"
            ),
    }


def _insert_rule_once(
    storage: Storage,
    *,
    family: str,
    family_version: str,
    rule_type: str,
    rule: dict[
        str,
        Any,
    ],
    proof_reference: str,
) -> int:
    """Insert one region rule idempotently."""

    row = storage.connection.execute(
        """
        SELECT COUNT(*) AS count
        FROM region_rules
        WHERE family=?
          AND family_version=?
          AND rule_type=?
          AND proof_reference=?
        """,
        (
            family,
            family_version,
            rule_type,
            proof_reference,
        ),
    ).fetchone()

    if (
        row is not None
        and
        int(
            row[
                "count"
            ]
        )
        >
        0
    ):
        return 0

    storage.add_region_rule(
        family=
            family,

        family_version=
            family_version,

        rule_type=
            rule_type,

        rule=
            rule,

        proof_reference=
            proof_reference,
    )

    return 1


def persist_v25b_region_rule(
    storage: Storage,
) -> int:
    """Persist the narrow historical-source transplant closure."""

    compatibility = (
        historical_source_compatibility()
    )

    return _insert_rule_once(
        storage,
        family=
            "032_ACTIVE_STATE_KGB_HIDDEN_AXIAL",

        family_version=
            "V25B",

        rule_type=
            "V16_SOURCE_MINIMAL_CUBIC_LOCAL_EFT_CONTROL_FAILURE",

        rule={
            "policy_specific":
                False,

            "scope":
                compatibility[
                    "closure_scope"
                ],

            "closed":
                True,

            "source_variation_momentum_ev":
                compatibility[
                    "source_variation_momentum_ev"
                ],

            "historical_gradient_ev2":
                compatibility[
                    "gradient_ev2"
                ],

            "a1e3_lambda_eff_over_source_k":
                compatibility[
                    "a1e3_lambda_eff_over_source_k"
                ],

            "actual_gradient_max_controlled_gain_times_planck":
                compatibility[
                    "actual_gradient_max_controlled_gain_times_planck"
                ],

            "hard_margin_proxy_max_controlled_gain_times_planck":
                compatibility[
                    "hard_margin_proxy_max_controlled_gain_times_planck"
                ],

            "relaxed_cutoff_max_controlled_gain_times_planck":
                compatibility[
                    "relaxed_cutoff_max_controlled_gain_times_planck"
                ],

            "generalized_kgb_closed":
                False,

            "wbg_multiscale_kgb_closed":
                False,

            "new_hidden_source_closed":
                False,

            "full_tensor_horndeski_closed":
                False,
        },

        proof_reference=
            "032V25B_MINIMAL_CUBIC_HISTORICAL_SOURCE_CONTROL_GATE",
    )


def persist_v25b_metadata(
    storage: Storage,
) -> None:
    """Persist current scheduler metadata only."""

    metadata = {
        "032v25b_v16_minimal_cubic_transplant_closed":
            "1",

        "032v25b_generalized_kgb_closed":
            "0",

        "032v25b_wbg_multiscale_kgb_closed":
            "0",

        "032v25b_full_tensor_crossprop_certified":
            "0",

        "032v25b_full_source_rg_uv_certified":
            "0",

        "032v25b_action_oracle_authorized":
            "0",

        "032v25b_blind_parameter_scan_authorized":
            "0",

        "agminer_next_family":
            (
                "GENERALIZED_WBG_KGB_MULTISCALE_"
                "ACTION_AND_SOURCE_SCALE"
            ),
    }

    for key, value in metadata.items():
        storage.set_metadata(
            key,
            value,
        )
