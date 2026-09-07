"""032V25F full KGB metric-numerator / radial-stability gate.

PURPOSE
-------
V25E derived the exact static spherical shift-current Jacobian

    D
        =
        dF/du

and showed that non-monotone K_XX/G3_XX can algebraically make D small.

That was intentionally NOT a full scalar-metric stability calculation.

V25F now incorporates the exact KGB debraiding / principal-symbol structure.

LITERATURE ORACLE
-----------------
For

    S
        =
        integral sqrt(-g) [
            Mpl^2 R / 2
            +
            K(X)
            +
            G(X) Box(phi)
        ],

Deffayet et al., arXiv:1008.0048, Eqs. 12-18 show that after using the
Einstein equation to eliminate second metric derivatives from the scalar
equation:

1. the principal matrix is lower triangular in scalar/metric variables;
2. the characteristic determinant factorizes into pure gravitational and
   pure scalar pieces;
3. the scalar characteristics are governed by the effective metric

       G_eff
         =
       L_tilde
         +
       2 Q . Hessian(phi);

4. gravitational backreaction contributes terms quadratic in G_X/Mpl.

STATIC SOURCE-ALIGNED VARIABLES
-------------------------------
Use

    u
        =
        d phi / dr
        >
        0,

    s
        =
        u^2 / 2
        =
        -X,

    A(s)
        =
        K_X,

    B(s)
        =
        -G_X.

The fixed-metric static source current used in V25E is

    F
        =
        u A
        +
        2 u^2 B / r,

with Jacobian

    D
        =
        A
        +
        u^2 A_s
        +
        4u B/r
        +
        2u^3 B_s/r.

Define

    q
        =
        B u^2 / Mpl.

For a local static spherical patch, reconstructing the debraided KGB
effective metric gives

    Z_t
        =
        A
        +
        2 B u'
        +
        B_s u^2 u'
        +
        4uB/r
        -
        q^2/2,

    Z_Omega
        =
        Z_t
        -
        2uB/r,

and, crucially,

    Z_r
        =
        D
        +
        3 q^2 / 2.

The cancellation of all u' terms from Z_r is exact.

The Planck-normalized nonrelativistic matter numerator induced by the
debraided KGB term is

    N
        =
        q / 2.

RADIAL CANONICAL BOUND
----------------------
On the regular source branch

    D >= 0,

we immediately obtain

    Z_r
        >=
        3 q^2 / 2,

hence

    N^2 / Z_r
        <=
        1/6

and therefore

    |N| / sqrt(Z_r)
        <=
        1/sqrt(6).

Thus making D small does NOT give unbounded canonically normalized radial
metric braiding.

If a two-vertex local transfer proxy scales as

    T
        =
        |N| / Z_r,

then

    T
        <=
        1 / sqrt(6 Z_r).

A requested enhancement T therefore requires

    Z_r
        <=
        1 / (6 T^2).

Large transfer can only be obtained by collapsing the full radial scalar
principal-symbol margin.

ABSOLUTE SOURCE-EFFICIENCY BOUND
--------------------------------
For source-aligned

    A > 0,
    B >= 0,

we also have

    F
        >=
        2u^2 B/r.

Therefore

    (|N|/F) (4 Mpl/r)
        <=
        1.

Non-monotone derivatives A_s and B_s can change susceptibility D, but they
cannot improve this absolute numerator-per-source-current bound.

CLAIM BOUNDARY
--------------
V25F closes only:

    SOURCE-ALIGNED G2+G3
        +
    NON-MONOTONE CURRENT-JACOBIAN TUNING
        +
    AS A FREE HEALTHY METRIC-GAIN MECHANISM.

It does NOT close:

- B<0 sign-reversed/cancellation branches;
- A<=0 branches that require an independent full stability proof;
- G4/G5 weakly-broken-Galileon structure;
- genuinely new hidden-source microphysics;
- oblate nonlinear source solutions;
- additional fields;
- background-dependent branches outside this local static reduction.

It also does not establish outward sign, finite payload response, source
charge per joule, or complete energy below 10 MJ.

CLAIM_CLASSIFICATION=
FULL_KGB_RADIAL_PRINCIPAL_SYMBOL_AND_METRIC_NUMERATOR_FALSIFICATION
"""

from __future__ import annotations

import math
from typing import Any

from .storage import Storage


INV_SQRT_6 = (
    1.0
    /
    math.sqrt(
        6.0
    )
)


def _positive(
    value: float,
    name: str,
) -> float:
    result = float(
        value
    )

    if (
        not math.isfinite(
            result
        )
        or result <= 0.0
    ):
        raise ValueError(
            f"{name} must be positive and finite"
        )

    return result


def local_kgb_components(
    *,
    u: float,
    radius: float,
    mpl: float,
    a_value: float,
    a_s: float,
    b_value: float,
    b_s: float,
    u_prime: float = 0.0,
) -> dict[str, Any]:
    """Return local static source-current and full scalar principal data."""

    gradient = _positive(
        u,
        "u",
    )

    r_value = _positive(
        radius,
        "radius",
    )

    mpl_value = _positive(
        mpl,
        "mpl",
    )

    values = tuple(
        float(
            item
        )
        for item
        in (
            a_value,
            a_s,
            b_value,
            b_s,
            u_prime,
        )
    )

    if not all(
        math.isfinite(
            item
        )
        for item
        in values
    ):
        raise ValueError(
            "all coefficients must be finite"
        )

    (
        a_coeff,
        a_derivative,
        b_coeff,
        b_derivative,
        curvature_gradient,
    ) = values

    current = (
        gradient
        *
        a_coeff
        +
        2.0
        *
        gradient**2
        *
        b_coeff
        /
        r_value
    )

    current_jacobian = (
        a_coeff
        +
        gradient**2
        *
        a_derivative
        +
        4.0
        *
        gradient
        *
        b_coeff
        /
        r_value
        +
        2.0
        *
        gradient**3
        *
        b_derivative
        /
        r_value
    )

    q_value = (
        b_coeff
        *
        gradient**2
        /
        mpl_value
    )

    w_value = (
        b_coeff
        *
        gradient
        /
        r_value
    )

    z_time = (
        a_coeff
        +
        2.0
        *
        b_coeff
        *
        curvature_gradient
        +
        b_derivative
        *
        gradient**2
        *
        curvature_gradient
        +
        4.0
        *
        w_value
        -
        0.5
        *
        q_value**2
    )

    z_angular = (
        z_time
        -
        2.0
        *
        w_value
    )

    z_radial = (
        current_jacobian
        +
        1.5
        *
        q_value**2
    )

    numerator = (
        q_value
        /
        2.0
    )

    scale = max(
        1.0,
        abs(
            a_coeff
        ),
        abs(
            current_jacobian
        ),
        abs(
            z_time
        ),
        abs(
            z_angular
        ),
        abs(
            z_radial
        ),
    )

    tolerance = (
        1.0e-14
        *
        scale
    )

    source_branch_regular = bool(
        current_jacobian
        >
        tolerance
    )

    scalar_principal_healthy = bool(
        z_time
        >
        tolerance
        and
        z_angular
        >
        tolerance
        and
        z_radial
        >
        tolerance
    )

    radial_canonical_braiding = None
    two_vertex_transfer_proxy = None

    if z_radial > tolerance:
        radial_canonical_braiding = (
            abs(
                numerator
            )
            /
            math.sqrt(
                z_radial
            )
        )

        two_vertex_transfer_proxy = (
            abs(
                numerator
            )
            /
            z_radial
        )

    temporal_canonical_braiding = None

    if z_time > tolerance:
        temporal_canonical_braiding = (
            abs(
                numerator
            )
            /
            math.sqrt(
                z_time
            )
        )

    geometry_normalized_source_efficiency = None

    if current != 0.0:
        geometry_normalized_source_efficiency = (
            abs(
                numerator
                /
                current
            )
            *
            4.0
            *
            mpl_value
            /
            r_value
        )

    return {
        "u":
            gradient,

        "radius":
            r_value,

        "mpl":
            mpl_value,

        "a_value":
            a_coeff,

        "a_s":
            a_derivative,

        "b_value":
            b_coeff,

        "b_s":
            b_derivative,

        "u_prime":
            curvature_gradient,

        "source_current":
            current,

        "source_current_jacobian":
            current_jacobian,

        "q_braiding":
            q_value,

        "w_curvature_braiding":
            w_value,

        "z_time":
            z_time,

        "z_angular":
            z_angular,

        "z_radial":
            z_radial,

        "radial_backreaction_increment":
            1.5
            *
            q_value**2,

        "metric_numerator_times_mpl":
            numerator,

        "source_branch_regular":
            source_branch_regular,

        "scalar_principal_healthy":
            scalar_principal_healthy,

        "radial_canonical_braiding":
            radial_canonical_braiding,

        "temporal_canonical_braiding":
            temporal_canonical_braiding,

        "two_vertex_transfer_proxy":
            two_vertex_transfer_proxy,

        "geometry_normalized_source_efficiency":
            geometry_normalized_source_efficiency,

        "full_finite_payload_metric_response_established":
            False,
    }


def planar_local_components(
    *,
    a_value: float,
    d_value: float,
    q_value: float,
) -> dict[str, Any]:
    """Return the local planar constant-gradient reduction.

    In this reduction curvature/Hessian terms vanish and

        Z_t = Z_perp = A-q^2/2
        Z_r = D+3q^2/2
        N = q/2.
    """

    a_coeff = float(
        a_value
    )

    d_coeff = float(
        d_value
    )

    q_coeff = float(
        q_value
    )

    if not all(
        math.isfinite(
            item
        )
        for item
        in (
            a_coeff,
            d_coeff,
            q_coeff,
        )
    ):
        raise ValueError(
            "finite inputs required"
        )

    z_time = (
        a_coeff
        -
        0.5
        *
        q_coeff**2
    )

    z_radial = (
        d_coeff
        +
        1.5
        *
        q_coeff**2
    )

    numerator = (
        q_coeff
        /
        2.0
    )

    radial_canonical = None
    transfer_proxy = None

    if z_radial > 0.0:
        radial_canonical = (
            abs(
                numerator
            )
            /
            math.sqrt(
                z_radial
            )
        )

        transfer_proxy = (
            abs(
                numerator
            )
            /
            z_radial
        )

    return {
        "a_value":
            a_coeff,

        "d_value":
            d_coeff,

        "q_value":
            q_coeff,

        "z_time":
            z_time,

        "z_angular":
            z_time,

        "z_radial":
            z_radial,

        "metric_numerator_times_mpl":
            numerator,

        "radial_canonical_braiding":
            radial_canonical,

        "two_vertex_transfer_proxy":
            transfer_proxy,

        "source_branch_regular":
            d_coeff > 0.0,

        "scalar_principal_healthy":
            bool(
                z_time > 0.0
                and
                z_radial > 0.0
            ),
    }


def minimal_cubic_from_y(
    y: float,
) -> dict[str, float]:
    """Reconstruct the V25A minimal-cubic local result."""

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

    q_value = math.sqrt(
        2.0
        *
        value
    )

    state = (
        planar_local_components(
            a_value=
                1.0,

            d_value=
                1.0,

            q_value=
                q_value,
        )
    )

    canonical_temporal = (
        state[
            "metric_numerator_times_mpl"
        ]
        /
        math.sqrt(
            state[
                "z_time"
            ]
        )
        if value > 0.0
        else 0.0
    )

    return {
        "y":
            value,

        "q":
            q_value,

        "z_time":
            state[
                "z_time"
            ],

        "z_radial":
            state[
                "z_radial"
            ],

        "canonical_matter_gain_times_mpl":
            canonical_temporal,
    }


def radial_braiding_bound(
    *,
    d_value: float,
    q_value: float,
) -> dict[str, Any]:
    """Evaluate N^2/Z_r <= 1/6 for D>=0."""

    d_coeff = float(
        d_value
    )

    q_coeff = float(
        q_value
    )

    if (
        not math.isfinite(
            d_coeff
        )
        or
        not math.isfinite(
            q_coeff
        )
    ):
        raise ValueError(
            "finite inputs required"
        )

    z_radial = (
        d_coeff
        +
        1.5
        *
        q_coeff**2
    )

    numerator_squared = (
        q_coeff**2
        /
        4.0
    )

    ratio = None

    if z_radial > 0.0:
        ratio = (
            numerator_squared
            /
            z_radial
        )

    theorem_applies = bool(
        d_coeff
        >=
        0.0
        and
        z_radial > 0.0
    )

    return {
        "d_value":
            d_coeff,

        "q_value":
            q_coeff,

        "z_radial":
            z_radial,

        "numerator_squared":
            numerator_squared,

        "numerator_squared_over_z_radial":
            ratio,

        "theorem_applies":
            theorem_applies,

        "bound_one_sixth":
            (
                bool(
                    ratio
                    <=
                    (
                        1.0
                        /
                        6.0
                        +
                        1.0e-14
                    )
                )
                if theorem_applies
                else False
            ),

        "radial_canonical_braiding_bound":
            INV_SQRT_6,
    }


def required_radial_margin_for_transfer(
    transfer_gain: float,
) -> dict[str, float]:
    """Return the necessary Z_r ceiling for a requested two-vertex gain.

    From

        |N|/Z_r
            <=
        1/sqrt(6 Z_r)

    a transfer target T requires

        Z_r
            <=
        1/(6 T^2).
    """

    target = float(
        transfer_gain
    )

    if (
        not math.isfinite(
            target
        )
        or target <= 0.0
    ):
        raise ValueError(
            "transfer_gain must be positive and finite"
        )

    maximum_z_radial = (
        1.0
        /
        (
            6.0
            *
            target**2
        )
    )

    return {
        "transfer_gain":
            target,

        "necessary_maximum_z_radial":
            maximum_z_radial,

        "required_radial_collapse_factor_from_unit_margin":
            1.0
            /
            maximum_z_radial,
    }


def source_aligned_efficiency_theorem(
    *,
    u: float,
    radius: float,
    mpl: float,
    a_value: float,
    b_value: float,
) -> dict[str, Any]:
    """Evaluate the absolute numerator/source-current geometry bound."""

    gradient = _positive(
        u,
        "u",
    )

    r_value = _positive(
        radius,
        "radius",
    )

    mpl_value = _positive(
        mpl,
        "mpl",
    )

    a_coeff = float(
        a_value
    )

    b_coeff = float(
        b_value
    )

    if (
        not math.isfinite(
            a_coeff
        )
        or
        not math.isfinite(
            b_coeff
        )
    ):
        raise ValueError(
            "finite coefficients required"
        )

    assumptions = bool(
        a_coeff > 0.0
        and
        b_coeff >= 0.0
    )

    current = (
        gradient
        *
        a_coeff
        +
        2.0
        *
        gradient**2
        *
        b_coeff
        /
        r_value
    )

    q_value = (
        b_coeff
        *
        gradient**2
        /
        mpl_value
    )

    numerator = (
        abs(
            q_value
        )
        /
        2.0
    )

    normalized_efficiency = (
        numerator
        /
        current
        *
        4.0
        *
        mpl_value
        /
        r_value
    )

    return {
        "assumptions_pass":
            assumptions,

        "source_current":
            current,

        "metric_numerator_times_mpl":
            numerator,

        "geometry_normalized_efficiency":
            normalized_efficiency,

        "efficiency_bound_pass":
            bool(
                assumptions
                and
                normalized_efficiency
                <=
                1.0
                +
                1.0e-14
            ),
    }


def v25f_gate() -> dict[str, Any]:
    """Return the conservative V25F classification."""

    witness = (
        planar_local_components(
            a_value=
                2.0,

            d_value=
                0.01,

            q_value=
                0.5,
        )
    )

    bound = (
        radial_braiding_bound(
            d_value=
                0.01,

            q_value=
                0.5,
        )
    )

    gain1000 = (
        required_radial_margin_for_transfer(
            1000.0
        )
    )

    return {
        "kgb_characteristic_factorization_used":
            True,

        "exact_metric_braiding_numerator_analyzed":
            True,

        "full_radial_principal_backreaction_analyzed":
            True,

        "v25e_small_d_can_be_radially_regularized":
            witness[
                "scalar_principal_healthy"
            ],

        "source_aligned_radial_canonical_braiding_bound":
            bound[
                "bound_one_sixth"
            ],

        "radial_canonical_bound_value":
            INV_SQRT_6,

        "gain1000_required_maximum_z_radial":
            gain1000[
                "necessary_maximum_z_radial"
            ],

        "source_aligned_nonmonotone_current_tuning_free_metric_gain_closed":
            True,

        "sign_reversed_b_branch_closed":
            False,

        "cancellation_branch_closed":
            False,

        "g4_g5_wbg_closed":
            False,

        "alternative_hidden_source_closed":
            False,

        "oblate_nonlinear_source_closed":
            False,

        "full_finite_payload_crosspropagator_certified":
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

        "kgb_g2_g3_source_aligned_core_rerank_recommended":
            True,

        "decision":
            (
                "RED_PARTIAL_032V25F_SOURCE_ALIGNED_NONMONOTONE_G2_G3_"
                "CURRENT_JACOBIAN_TUNING_DOES_NOT_PRODUCE_UNBOUNDED_"
                "HEALTHY_METRIC_GAIN__FULL_RADIAL_BRAIDING_BACKREACTION_"
                "BOUNDS_CANONICAL_NUMERATOR__SIGN_REVERSED_G4_G5_AND_"
                "NEW_SOURCE_REMAIN_OPEN"
            ),

        "next":
            (
                "032V26_AGMINER_GLOBAL_RERANK_AFTER_KGB_G2_G3_"
                "SOURCE_ALIGNED_CORE_CLOSEOUT"
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
    """Insert one theorem-backed rule idempotently."""

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


def persist_v25f_region_rule(
    storage: Storage,
) -> int:
    """Persist only the source-aligned G2+G3 free-gain closure."""

    gain1000 = (
        required_radial_margin_for_transfer(
            1000.0
        )
    )

    return _insert_rule_once(
        storage,
        family=
            "032_ACTIVE_STATE_NONLINEAR_KGB",

        family_version=
            "V25F",

        rule_type=
            "SOURCE_ALIGNED_NONMONOTONE_CURRENT_TUNING_NO_FREE_METRIC_GAIN",

        rule={
            "policy_specific":
                False,

            "scope":
                (
                    "LOCAL_STATIC_SOURCE_ALIGNED_G2_G3_WITH_D_GE0_"
                    "AND_NONMONOTONE_CURRENT_JACOBIAN_TUNING"
                ),

            "closed":
                True,

            "exact_radial_identity":
                "Z_R_EQUALS_D_PLUS_3_Q2_OVER_2",

            "metric_numerator":
                "N_EQUALS_Q_OVER_2",

            "canonical_bound":
                "N2_OVER_ZR_LE_1_OVER_6",

            "gain1000_required_maximum_z_radial":
                gain1000[
                    "necessary_maximum_z_radial"
                ],

            "sign_reversed_b_closed":
                False,

            "cancellation_branch_closed":
                False,

            "g4_g5_closed":
                False,

            "alternative_hidden_source_closed":
                False,

            "full_kgb_closed":
                False,
        },

        proof_reference=
            "032V25F_FULL_KGB_RADIAL_PRINCIPAL_METRIC_NUMERATOR_GATE",
    )


def persist_v25f_metadata(
    storage: Storage,
) -> None:
    """Persist current frontier metadata only."""

    metadata = {
        "032v25f_metric_braiding_numerator_analyzed":
            "1",

        "032v25f_full_radial_principal_backreaction_analyzed":
            "1",

        "032v25f_source_aligned_nonmonotone_free_metric_gain_closed":
            "1",

        "032v25f_sign_reversed_b_closed":
            "0",

        "032v25f_g4_g5_closed":
            "0",

        "032v25f_alternative_hidden_source_closed":
            "0",

        "032v25f_action_oracle_authorized":
            "0",

        "032v25f_blind_parameter_scan_authorized":
            "0",

        "032v25f_global_rerank_recommended":
            "1",

        "agminer_next_family":
            (
                "GLOBAL_RERANK_AFTER_KGB_G2_G3_"
                "SOURCE_ALIGNED_CORE_CLOSEOUT"
            ),
    }

    for key, value in metadata.items():
        storage.set_metadata(
            key,
            value,
        )
