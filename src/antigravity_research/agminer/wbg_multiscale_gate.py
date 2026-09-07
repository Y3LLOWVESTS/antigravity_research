"""032V25C WBG multiscale / locally-linear G3 invariance gate.

PURPOSE
-------
V25B closed the unchanged historical V16 source when transplanted directly
into the minimal cubic KGB action because the canonically normalized cubic
interaction scale falls below the source's own spatial variation momentum.

V25C asks whether the standard weakly-broken-Galileon two-scale hierarchy can
evade that result merely by choosing a much larger parent Lambda_3 while
keeping a small first-derivative invariant X and an order-one second-derivative
background parameter.

The answer for a locally linear cubic sector is no.

WBG POWER COUNTING
------------------
Use the standard hierarchy

    Lambda_2^4
        =
        Mpl Lambda_3^3.

For the present static source-scale proxy define

    X
        =
        |grad(phi)|^2 / Lambda_2^4

and

    Z_source
        =
        k_source |grad(phi)| / Lambda_3^3.

This Z_source is a project source-scale analogue of the usual WBG
second-derivative variable. It is not claimed to be the cosmological Z of the
published FRW analysis.

Choosing Z_source~1 can give

    Lambda_3 >> k_source

while simultaneously making

    X << 1.

LOCALLY LINEAR G3 THEOREM
-------------------------
Take a local cubic expansion

    G_3(X)
        =
        c_3 X
        + higher powers.

The physical cubic coefficient is then

    c_3 / Lambda_3^3

and the effective cubic scale is

    Lambda_3,eff
        =
        Lambda_3 / |c_3|^(1/3).

For the V25A static background define

    y
        =
        (c_3 X)^2 / 2.

The canonically normalized active coupling is

    A
        =
        Mpl |g_c|
        =
        sqrt[
            y / (2(1-y))
        ].

At fixed requested A,

    |c_3| X
        =
        sqrt(2y),

so

    Lambda_3,eff
        =
        Lambda_3
        [
            X / sqrt(2y)
        ]^(1/3).

Using

    X
        =
        |grad(phi)|^2
        /
        (Mpl Lambda_3^3)

gives

    Lambda_3,eff
        =
        [
            |grad(phi)|^2
            /
            (
                Mpl sqrt(2y)
            )
        ]^(1/3).

The arbitrary parent Lambda_3 cancels exactly.

After fluctuation canonical normalization the local cubic scale is

    Lambda_local
        =
        Lambda_3,eff sqrt(1-y),

which is therefore exactly the same source-scale bound obtained in V25B.

CLAIM BOUNDARY
--------------
This closes only the idea that the historical V16 source can escape V25B by
placing the same locally linear cubic interaction inside a larger WBG parent
Lambda_3 hierarchy.

It does NOT close:

- nonlinear G_3 backgrounds with important G_3XX or higher derivatives;
- large healthy K_X kinetic normalization;
- WBG G_4 or G_5 structures;
- multiscalar or multifield completions;
- alternative hidden-source microstates;
- higher-cutoff source sectors;
- background-dependent strong-coupling enhancement requiring a new action;
- the explicit V25A action-existence result.

No action oracle, candidate, survivor, payload result, or energy optimization
is created.

CLAIM_CLASSIFICATION=
WBG_PARENT_SCALE_AND_LOCAL_LINEAR_G3_CANONICAL_INVARIANCE_FALSIFICATION
"""

from __future__ import annotations

import math
from typing import Any

from .kgb_strong_coupling_source_gate import (
    MPL_REDUCED_EV,
    V16_SOURCE_C_M,
    characteristic_momentum_ev,
    gain_to_y,
    historical_source_compatibility,
    local_canonical_cubic_scale,
    y_to_gain,
)
from .storage import Storage


def wbg_parent_scales(
    *,
    gradient_ev2: float,
    length_m: float,
    hessian_z: float,
) -> dict[str, Any]:
    """Construct the WBG parent scales for one source-scale proxy.

    The source Hessian proxy is

        |d^2 phi|
            ~
        k_source |grad(phi)|.

    We set

        Z_source
            =
        |d^2 phi| / Lambda_3^3.
    """

    gradient = float(
        gradient_ev2
    )

    length = float(
        length_m
    )

    z_value = float(
        hessian_z
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
            length
        )
        or length <= 0.0
    ):
        raise ValueError(
            "length_m must be positive and finite"
        )

    if (
        not math.isfinite(
            z_value
        )
        or z_value <= 0.0
    ):
        raise ValueError(
            "hessian_z must be positive and finite"
        )

    source_k = (
        characteristic_momentum_ev(
            length
        )
    )

    hessian_proxy = (
        gradient
        *
        source_k
    )

    lambda_3 = (
        hessian_proxy
        /
        z_value
    )**(
        1.0
        /
        3.0
    )

    lambda_2 = (
        MPL_REDUCED_EV
        *
        lambda_3**3
    )**0.25

    x_wbg = (
        gradient**2
        /
        lambda_2**4
    )

    return {
        "gradient_ev2":
            gradient,

        "length_m":
            length,

        "source_k_ev":
            source_k,

        "hessian_proxy_ev3":
            hessian_proxy,

        "hessian_z":
            z_value,

        "lambda3_parent_ev":
            lambda_3,

        "lambda3_parent_over_source_k":
            lambda_3
            /
            source_k,

        "lambda2_ev":
            lambda_2,

        "x_wbg":
            x_wbg,

        "x_le_one":
            x_wbg
            <=
            1.0,

        "z_le_one":
            z_value
            <=
            1.0,

        "published_wbg_power_counting_analogy":
            True,

        "static_wbg_rg_uv_certified":
            False,
    }


def order_one_linear_g3_gain(
    *,
    gradient_ev2: float,
    length_m: float,
    hessian_z: float,
) -> dict[str, Any]:
    """Return the gain for a locally linear cubic coefficient |c3|=1."""

    parent = (
        wbg_parent_scales(
            gradient_ev2=
                gradient_ev2,

            length_m=
                length_m,

            hessian_z=
                hessian_z,
        )
    )

    x_wbg = float(
        parent[
            "x_wbg"
        ]
    )

    y_value = (
        0.5
        *
        x_wbg**2
    )

    gain = (
        y_to_gain(
            y_value
        )
    )

    return {
        **parent,

        "linear_g3_coefficient":
            1.0,

        "y_effective":
            y_value,

        "canonical_gain_times_planck":
            gain,
    }


def required_linear_g3_coefficient(
    *,
    gradient_ev2: float,
    length_m: float,
    hessian_z: float,
    gain_times_planck: float,
) -> dict[str, Any]:
    """Match one requested gain and reconstruct the physical cubic scale."""

    parent = (
        wbg_parent_scales(
            gradient_ev2=
                gradient_ev2,

            length_m=
                length_m,

            hessian_z=
                hessian_z,
        )
    )

    gain = float(
        gain_times_planck
    )

    if (
        not math.isfinite(
            gain
        )
        or gain <= 0.0
    ):
        raise ValueError(
            "gain_times_planck must be positive and finite"
        )

    y_value = (
        gain_to_y(
            gain
        )
    )

    q_effective = math.sqrt(
        2.0
        *
        y_value
    )

    x_wbg = float(
        parent[
            "x_wbg"
        ]
    )

    c3_required = (
        q_effective
        /
        x_wbg
    )

    lambda_3_effective = (
        float(
            parent[
                "lambda3_parent_ev"
            ]
        )
        /
        abs(
            c3_required
        )**(
            1.0
            /
            3.0
        )
    )

    lambda_local = (
        lambda_3_effective
        *
        math.sqrt(
            1.0
            -
            y_value
        )
    )

    direct_v25b_scale = (
        local_canonical_cubic_scale(
            gradient_ev2=
                gradient_ev2,

            y=
                y_value,
        )
    )

    source_k = float(
        parent[
            "source_k_ev"
        ]
    )

    relative_error = (
        abs(
            lambda_local
            -
            direct_v25b_scale
        )
        /
        max(
            abs(
                lambda_local
            ),
            abs(
                direct_v25b_scale
            ),
            1.0e-300,
        )
    )

    return {
        **parent,

        "gain_times_planck":
            gain,

        "y_effective":
            y_value,

        "q_effective":
            q_effective,

        "required_abs_g3x":
            abs(
                c3_required
            ),

        "effective_lambda3_ev":
            lambda_3_effective,

        "local_canonical_scale_ev":
            lambda_local,

        "local_canonical_scale_over_source_k":
            lambda_local
            /
            source_k,

        "direct_v25b_scale_ev":
            direct_v25b_scale,

        "direct_v25b_scale_over_source_k":
            direct_v25b_scale
            /
            source_k,

        "parent_scale_invariance_relative_error":
            relative_error,

        "parent_scale_advantage_survives_coefficient_matching":
            False,
    }


def parent_rescaling_invariance_scout(
    *,
    gradient_ev2: float,
    length_m: float,
    gain_times_planck: float,
    z_values: tuple[float, ...] = (
        0.01,
        0.1,
        1.0,
    ),
) -> dict[str, Any]:
    """Verify that matched local control is independent of parent Z choice."""

    rows = [
        required_linear_g3_coefficient(
            gradient_ev2=
                gradient_ev2,

            length_m=
                length_m,

            hessian_z=
                z_value,

            gain_times_planck=
                gain_times_planck,
        )
        for z_value
        in z_values
    ]

    control_ratios = [
        float(
            row[
                "local_canonical_scale_over_source_k"
            ]
        )
        for row
        in rows
    ]

    spread = (
        max(
            control_ratios
        )
        -
        min(
            control_ratios
        )
    )

    scale = max(
        max(
            abs(
                value
            )
            for value
            in control_ratios
        ),
        1.0,
    )

    relative_spread = (
        spread
        /
        scale
    )

    return {
        "rows":
            rows,

        "maximum_control_ratio_spread":
            spread,

        "relative_spread":
            relative_spread,

        "parent_rescaling_invariant":
            relative_spread
            <
            1.0e-12,
    }


def historical_v16_wbg_corridor() -> dict[str, Any]:
    """Return the post-V25B WBG source-scale corridor diagnostics."""

    historical = (
        historical_source_compatibility()
    )

    gradient = float(
        historical[
            "gradient_ev2"
        ]
    )

    length = float(
        V16_SOURCE_C_M
    )

    parent = (
        wbg_parent_scales(
            gradient_ev2=
                gradient,

            length_m=
                length,

            hessian_z=
                1.0,
        )
    )

    unit_coefficient = (
        order_one_linear_g3_gain(
            gradient_ev2=
                gradient,

            length_m=
                length,

            hessian_z=
                1.0,
        )
    )

    gain_1e3 = (
        required_linear_g3_coefficient(
            gradient_ev2=
                gradient,

            length_m=
                length,

            hessian_z=
                1.0,

            gain_times_planck=
                1.0e-3,
        )
    )

    gain_one = (
        required_linear_g3_coefficient(
            gradient_ev2=
                gradient,

            length_m=
                length,

            hessian_z=
                1.0,

            gain_times_planck=
                1.0,
        )
    )

    invariance = (
        parent_rescaling_invariance_scout(
            gradient_ev2=
                gradient,

            length_m=
                length,

            gain_times_planck=
                1.0e-3,
        )
    )

    return {
        **parent,

        "order_one_g3_gain_times_planck":
            unit_coefficient[
                "canonical_gain_times_planck"
            ],

        "a1e3_required_abs_g3x":
            gain_1e3[
                "required_abs_g3x"
            ],

        "a1e3_effective_lambda3_ev":
            gain_1e3[
                "effective_lambda3_ev"
            ],

        "a1e3_local_scale_over_k":
            gain_1e3[
                "local_canonical_scale_over_source_k"
            ],

        "a1_local_scale_over_k":
            gain_one[
                "local_canonical_scale_over_source_k"
            ],

        "a1e3_matches_v25b_ratio_error":
            abs(
                float(
                    gain_1e3[
                        "local_canonical_scale_over_source_k"
                    ]
                )
                -
                float(
                    historical[
                        "a1e3_lambda_eff_over_source_k"
                    ]
                )
            ),

        "parent_rescaling_invariant":
            invariance[
                "parent_rescaling_invariant"
            ],

        "locally_linear_g3_parent_scale_rescue_closed":
            bool(
                gain_1e3[
                    "local_canonical_scale_over_source_k"
                ]
                <
                1.0
            ),

        "nonlinear_g3_closed":
            False,

        "large_healthy_kx_closed":
            False,

        "g4_g5_wbg_closed":
            False,

        "alternative_hidden_source_closed":
            False,
    }


def v25c_gate() -> dict[str, Any]:
    """Return the conservative V25C decision."""

    corridor = (
        historical_v16_wbg_corridor()
    )

    return {
        "wbg_two_scale_parent_corridor_exists":
            bool(
                corridor[
                    "lambda3_parent_over_source_k"
                ]
                >
                1.0e4
                and
                corridor[
                    "x_wbg"
                ]
                <
                1.0e-10
            ),

        "locally_linear_g3_parent_scale_rescue_closed":
            corridor[
                "locally_linear_g3_parent_scale_rescue_closed"
            ],

        "generalized_nonlinear_g3_closed":
            False,

        "large_healthy_kx_closed":
            False,

        "full_wbg_g4_g5_closed":
            False,

        "alternative_hidden_source_closed":
            False,

        "full_tensor_nonremovable_crosspropagator_certified":
            False,

        "full_source_rg_uv_certified":
            False,

        "new_selfconsistent_source_solved":
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
                "RED_PARTIAL_032V25C_WBG_PARENT_SCALE_RESCALING_WITH_"
                "LOCALLY_LINEAR_G3_DOES_NOT_EVADE_V25B_CANONICAL_"
                "SOURCE_SCALE_BOUND__GENUINELY_NONLINEAR_G3_KINETIC_"
                "ENHANCEMENT_AND_NEW_SOURCE_REMAIN_OPEN"
            ),

        "next":
            (
                "032V25D_GENERALIZED_KX_G3_KINETIC_ENHANCEMENT_"
                "SOURCE_REACTION_AND_CANONICAL_SCALE_GATE"
            ),
    }


def _insert_rule_once(
    storage: Storage,
    *,
    family: str,
    family_version: str,
    rule_type: str,
    rule: dict[str, Any],
    proof_reference: str,
) -> int:
    """Insert one theorem-backed region rule idempotently."""

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


def persist_v25c_region_rule(
    storage: Storage,
) -> int:
    """Persist only the narrow parent-scale-rescaling closure."""

    corridor = (
        historical_v16_wbg_corridor()
    )

    return _insert_rule_once(
        storage,
        family=
            "032_ACTIVE_STATE_WBG_KGB",

        family_version=
            "V25C",

        rule_type=
            "LOCALLY_LINEAR_G3_PARENT_SCALE_RESCALING_NO_RESCUE",

        rule={
            "policy_specific":
                False,

            "scope":
                (
                    "HISTORICAL_V16_SOURCE_PLUS_WBG_PARENT_SCALE_"
                    "RESCALING_WITH_LOCALLY_LINEAR_G3"
                ),

            "closed":
                True,

            "parent_lambda3_over_source_k":
                corridor[
                    "lambda3_parent_over_source_k"
                ],

            "x_wbg":
                corridor[
                    "x_wbg"
                ],

            "a1e3_required_abs_g3x":
                corridor[
                    "a1e3_required_abs_g3x"
                ],

            "a1e3_local_scale_over_k":
                corridor[
                    "a1e3_local_scale_over_k"
                ],

            "parent_rescaling_invariant":
                corridor[
                    "parent_rescaling_invariant"
                ],

            "nonlinear_g3_closed":
                False,

            "large_healthy_kx_closed":
                False,

            "g4_g5_wbg_closed":
                False,

            "alternative_hidden_source_closed":
                False,

            "full_wbg_closed":
                False,
        },

        proof_reference=
            "032V25C_WBG_PARENT_SCALE_COEFFICIENT_INVARIANCE_GATE",
    )


def persist_v25c_metadata(
    storage: Storage,
) -> None:
    """Persist current frontier state without promoting a model."""

    metadata = {
        "032v25c_wbg_parent_corridor_exists":
            "1",

        "032v25c_locally_linear_g3_parent_rescaling_rescue_closed":
            "1",

        "032v25c_nonlinear_g3_closed":
            "0",

        "032v25c_large_healthy_kx_closed":
            "0",

        "032v25c_full_wbg_g4_g5_closed":
            "0",

        "032v25c_full_tensor_crossprop_certified":
            "0",

        "032v25c_full_source_rg_uv_certified":
            "0",

        "032v25c_action_oracle_authorized":
            "0",

        "032v25c_blind_parameter_scan_authorized":
            "0",

        "agminer_next_family":
            (
                "GENERALIZED_KX_G3_KINETIC_ENHANCEMENT_"
                "SOURCE_REACTION"
            ),
    }

    for key, value in metadata.items():
        storage.set_metadata(
            key,
            value,
        )
