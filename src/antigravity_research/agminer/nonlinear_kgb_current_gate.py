"""032V25E nonlinear KGB source-current / canonical-response gate.

PURPOSE
-------
V25D closed large locally constant positive K_X as a free rescue of the
unchanged historical V16 source when G3 is locally linear.

V25E now stops treating K_X and G3_X as constants.

Rather than scan arbitrary functions blindly, it derives the exact local
static spherical shift-current Jacobian for the shift-symmetric G2(X)+G3(X)
sector and asks what nonlinear K_XX/G3_XX can actually do to source response.

STANDARD SHIFT CURRENT
----------------------
For shift-symmetric Horndeski restricted to G2(X)+G3(X), the Noether current
contains

    J_(2)^a
        =
        -G2_X grad^a(phi)

and

    J_(3)^a
        =
        G3_X [
            grad^a(phi) Box(phi)
            -
            grad^a grad^b(phi) grad_b(phi)
        ].

For a flat static spherically symmetric field

    phi
        =
        phi(r),

    u
        =
        d phi / dr,

the cubic structure reduces exactly to

    grad^r(phi) Box(phi)
      -
    grad^r grad^b(phi) grad_b(phi)

        =
        2 u^2 / r.

Thus

    J^r
        =
        -G2_X u
        +
        2 G3_X u^2 / r.

SOURCE-ALIGNED CONVENTION
-------------------------
Define the positive-gradient variable

    s
        =
        u^2 / 2
        =
        -X

for the static spacelike branch, and define source-aligned coefficients

    A(s)
        =
        G2_X,

    B(s)
        =
        -G3_X.

Then

    F(u)
        =
        -J^r
        =
        u A(s)
        +
        2 u^2 B(s) / r.

For an integrated derivative source charge Q,

    Q
        =
        4 pi r^2 F(u)

outside the source.

The exact local source-current Jacobian is

    D
        =
        dF/du

        =
        A
        +
        u^2 A_s
        +
        4u B/r
        +
        2u^3 B_s/r.

Therefore

    du/dQ
        =
        1 / [4 pi r^2 D].

D is also the denominator of the static radial linearized current response:

    delta F
        =
        D delta u.

MONOTONE SOURCE-ALIGNED THEOREM
-------------------------------
If

    A > 0,
    A_s >= 0,
    B >= 0,
    B_s >= 0,

then

    D - F/u

        =
        u^2 A_s
        +
        2u B/r
        +
        2u^3 B_s/r

        >=
        0.

Hence

    epsilon_current
        =
        u D / F

        >=
        1.

The logarithmic source response is

    d ln u / d ln Q
        =
        1 / epsilon_current

        <=
        1.

Therefore this entire local monotone source-aligned nonlinear branch cannot
generate source-current anti-screening.

LARGE RESPONSE
--------------
For any branch, not only the monotone branch,

    source susceptibility
        ~
        1/D.

If a baseline has D0=1, an N-fold local source-response enhancement requires

    D
        =
        1/N.

The radial-static canonically normalized derivative-source coupling scales as

    g_source,c
        ~
        D^(-1/2).

Thus large susceptibility necessarily approaches D -> 0, the local static
current / branch degeneracy.

CLAIM BOUNDARY
--------------
This is NOT a full dynamical stability theorem.

D is the static radial current Jacobian. Full perturbative health still
requires the temporal, angular, scalar-metric, and constrained gravitational
kinetic structure.

The result closes only:

    STATIC SPHERICAL G2+G3
        +
    SOURCE-ALIGNED MONOTONE A(s),B(s)
        +
    SOURCE-CURRENT ANTISCREENING AS THE RESCUE MECHANISM.

It does NOT close:

- non-monotone A_s or B_s;
- important K_XX/G3_XX branches with changing metric numerator;
- full tensor braiding;
- G4/G5 WBG structure;
- oblate nonlinear source geometry;
- new hidden source sectors;
- stable branch transitions;
- nonlinear source solutions.

No action oracle, energy optimization, payload result, or antigravity model is
created.

CLAIM_CLASSIFICATION=
NONLINEAR_SHIFT_CURRENT_JACOBIAN_AND_STATIC_CANONICAL_RESPONSE_FALSIFICATION
"""

from __future__ import annotations

import math
from typing import Any

from .storage import Storage


FOUR_PI = (
    4.0
    *
    math.pi
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


def source_aligned_current(
    *,
    u: float,
    radius: float,
    a_value: float,
    b_value: float,
) -> float:
    """Return F=-J^r in the source-aligned convention."""

    gradient = _positive(
        u,
        "u",
    )

    r_value = _positive(
        radius,
        "radius",
    )

    a_coeff = float(
        a_value
    )

    b_coeff = float(
        b_value
    )

    if not all(
        math.isfinite(
            item
        )
        for item
        in (
            a_coeff,
            b_coeff,
        )
    ):
        raise ValueError(
            "coefficients must be finite"
        )

    return (
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


def source_current_jacobian(
    *,
    u: float,
    radius: float,
    a_value: float,
    a_s: float,
    b_value: float,
    b_s: float,
) -> float:
    """Return D=dF/du for s=u^2/2."""

    gradient = _positive(
        u,
        "u",
    )

    r_value = _positive(
        radius,
        "radius",
    )

    coefficients = (
        float(
            a_value
        ),
        float(
            a_s
        ),
        float(
            b_value
        ),
        float(
            b_s
        ),
    )

    if not all(
        math.isfinite(
            item
        )
        for item
        in coefficients
    ):
        raise ValueError(
            "coefficients must be finite"
        )

    a_coeff, a_derivative, b_coeff, b_derivative = coefficients

    return (
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


def integrated_source_charge(
    *,
    u: float,
    radius: float,
    a_value: float,
    b_value: float,
) -> float:
    """Return Q=4*pi*r^2*F."""

    r_value = _positive(
        radius,
        "radius",
    )

    current = (
        source_aligned_current(
            u=
                u,

            radius=
                r_value,

            a_value=
                a_value,

            b_value=
                b_value,
        )
    )

    return (
        FOUR_PI
        *
        r_value**2
        *
        current
    )


def local_static_response(
    *,
    u: float,
    radius: float,
    a_value: float,
    a_s: float,
    b_value: float,
    b_s: float,
) -> dict[str, Any]:
    """Return current elasticity and local static susceptibility."""

    gradient = _positive(
        u,
        "u",
    )

    r_value = _positive(
        radius,
        "radius",
    )

    current = (
        source_aligned_current(
            u=
                gradient,

            radius=
                r_value,

            a_value=
                a_value,

            b_value=
                b_value,
        )
    )

    jacobian = (
        source_current_jacobian(
            u=
                gradient,

            radius=
                r_value,

            a_value=
                a_value,

            a_s=
                a_s,

            b_value=
                b_value,

            b_s=
                b_s,
        )
    )

    # Numerical branch classification must treat analytically degenerate
    # Jacobians as degenerate rather than allowing a positive roundoff residue
    # to promote them to a regular branch.
    jacobian_scale = max(
        1.0,
        abs(
            float(
                a_value
            )
        ),
        abs(
            gradient**2
            *
            float(
                a_s
            )
        ),
        abs(
            4.0
            *
            gradient
            *
            float(
                b_value
            )
            /
            r_value
        ),
        abs(
            2.0
            *
            gradient**3
            *
            float(
                b_s
            )
            /
            r_value
        ),
    )

    jacobian_tolerance = (
        1.0e-14
        *
        jacobian_scale
    )

    static_branch_regular = bool(
        jacobian
        >
        jacobian_tolerance
    )

    if not static_branch_regular:
        return {
            "current":
                current,

            "jacobian":
                jacobian,

            "static_branch_regular":
                False,

            "elasticity":
                None,

            "d_u_d_q":
                None,

            "radial_static_canonical_source_coupling_relative":
                None,

            "full_dynamic_stability_certified":
                False,
        }

    elasticity = (
        gradient
        *
        jacobian
        /
        current
        if current != 0.0
        else None
    )

    return {
        "current":
            current,

        "jacobian":
            jacobian,

        "static_branch_regular":
            True,

        "elasticity":
            elasticity,

        "d_u_d_q":
            1.0
            /
            (
                FOUR_PI
                *
                r_value**2
                *
                jacobian
            ),

        "radial_static_canonical_source_coupling_relative":
            1.0
            /
            math.sqrt(
                jacobian
            ),

        "full_dynamic_stability_certified":
            False,
    }


def monotone_source_aligned_theorem(
    *,
    u: float,
    radius: float,
    a_value: float,
    a_s: float,
    b_value: float,
    b_s: float,
) -> dict[str, Any]:
    """Evaluate the exact D-F/u theorem."""

    gradient = _positive(
        u,
        "u",
    )

    r_value = _positive(
        radius,
        "radius",
    )

    a_coeff = float(
        a_value
    )

    a_derivative = float(
        a_s
    )

    b_coeff = float(
        b_value
    )

    b_derivative = float(
        b_s
    )

    assumptions = bool(
        a_coeff > 0.0
        and
        a_derivative >= 0.0
        and
        b_coeff >= 0.0
        and
        b_derivative >= 0.0
    )

    current = (
        source_aligned_current(
            u=
                gradient,

            radius=
                r_value,

            a_value=
                a_coeff,

            b_value=
                b_coeff,
        )
    )

    jacobian = (
        source_current_jacobian(
            u=
                gradient,

            radius=
                r_value,

            a_value=
                a_coeff,

            a_s=
                a_derivative,

            b_value=
                b_coeff,

            b_s=
                b_derivative,
        )
    )

    exact_difference = (
        gradient**2
        *
        a_derivative
        +
        2.0
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

    reconstructed_difference = (
        jacobian
        -
        current
        /
        gradient
    )

    difference_error = abs(
        exact_difference
        -
        reconstructed_difference
    )

    elasticity = (
        gradient
        *
        jacobian
        /
        current
    )

    return {
        "assumptions_pass":
            assumptions,

        "current":
            current,

        "jacobian":
            jacobian,

        "exact_difference":
            exact_difference,

        "reconstructed_difference":
            reconstructed_difference,

        "difference_identity_error":
            difference_error,

        "elasticity":
            elasticity,

        "monotone_branch_cannot_antiscreen_source_current":
            bool(
                assumptions
                and
                exact_difference >= 0.0
                and
                elasticity >= 1.0
            ),
    }


def pure_k_linear_in_s(
    *,
    alpha: float,
    u: float = 1.0,
) -> dict[str, Any]:
    """Return a simple non-monotone K_X witness.

    Use

        A(s)
            =
            1 - alpha s,

        B
            =
            0.

    At u=1,

        s
            =
            1/2,

        F
            =
            1 - alpha/2,

        D
            =
            1 - 3 alpha/2.

    D -> 0 at alpha -> 2/3 from below.

    This witness proves non-monotone branches are not algebraically excluded.
    It is not promoted as a physical theory.
    """

    alpha_value = float(
        alpha
    )

    gradient = _positive(
        u,
        "u",
    )

    if (
        not math.isfinite(
            alpha_value
        )
        or alpha_value < 0.0
    ):
        raise ValueError(
            "alpha must be finite and non-negative"
        )

    s_value = (
        gradient**2
        /
        2.0
    )

    a_value = (
        1.0
        -
        alpha_value
        *
        s_value
    )

    a_s = (
        -alpha_value
    )

    result = (
        local_static_response(
            u=
                gradient,

            radius=
                1.0,

            a_value=
                a_value,

            a_s=
                a_s,

            b_value=
                0.0,

            b_s=
                0.0,
        )
    )

    baseline_response = (
        1.0
        /
        FOUR_PI
    )

    response_gain = None

    if (
        result[
            "d_u_d_q"
        ]
        is not None
    ):
        response_gain = (
            float(
                result[
                    "d_u_d_q"
                ]
            )
            /
            baseline_response
        )

    return {
        "alpha":
            alpha_value,

        "s":
            s_value,

        "a_value":
            a_value,

        "a_s":
            a_s,

        **result,

        "response_gain_over_canonical_baseline":
            response_gain,

        "physical_model":
            False,
    }


def required_static_margin_for_response_gain(
    response_gain: float,
) -> dict[str, float]:
    """Invert susceptibility enhancement relative to baseline D0=1."""

    gain = float(
        response_gain
    )

    if (
        not math.isfinite(
            gain
        )
        or gain < 1.0
    ):
        raise ValueError(
            "response_gain must be finite and >= 1"
        )

    jacobian = (
        1.0
        /
        gain
    )

    canonical_source = (
        1.0
        /
        math.sqrt(
            jacobian
        )
    )

    return {
        "response_gain":
            gain,

        "required_static_radial_jacobian":
            jacobian,

        "radial_static_canonical_source_coupling_relative":
            canonical_source,

        "distance_to_zero_jacobian":
            jacobian,

        "full_dynamic_stability_certified":
            False,
    }


def v25e_gate() -> dict[str, Any]:
    """Return the conservative V25E classification."""

    theorem = (
        monotone_source_aligned_theorem(
            u=
                1.0,

            radius=
                2.0,

            a_value=
                2.0,

            a_s=
                0.5,

            b_value=
                0.3,

            b_s=
                0.2,
        )
    )

    witness_100 = (
        pure_k_linear_in_s(
            alpha=
                0.66,
        )
    )

    gain_1000 = (
        required_static_margin_for_response_gain(
            1000.0
        )
    )

    return {
        "exact_static_spherical_g2_g3_current_used":
            True,

        "monotone_source_aligned_no_antiscreen_theorem":
            theorem[
                "monotone_branch_cannot_antiscreen_source_current"
            ],

        "nonmonotone_source_response_algebraically_possible":
            bool(
                witness_100[
                    "static_branch_regular"
                ]
                and
                float(
                    witness_100[
                        "response_gain_over_canonical_baseline"
                    ]
                )
                >
                1.0
            ),

        "large_response_requires_small_static_jacobian":
            True,

        "gain1000_required_radial_jacobian":
            gain_1000[
                "required_static_radial_jacobian"
            ],

        "gain1000_canonical_source_coupling_relative":
            gain_1000[
                "radial_static_canonical_source_coupling_relative"
            ],

        "nonmonotone_kxx_closed":
            False,

        "nonmonotone_g3xx_closed":
            False,

        "metric_braiding_numerator_analyzed":
            False,

        "full_tensor_stability_certified":
            False,

        "oblate_source_solution_solved":
            False,

        "full_source_rg_uv_certified":
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
                "RED_PARTIAL_032V25E_STATIC_SPHERICAL_SOURCE_ALIGNED_"
                "MONOTONE_NONLINEAR_KX_G3X_CANNOT_ANTISCREEN_SHIFT_"
                "CURRENT__LARGE_SOURCE_RESPONSE_REQUIRES_SMALL_CURRENT_"
                "JACOBIAN__NONMONOTONE_KXX_G3XX_METRIC_NUMERATOR_REMAINS_OPEN"
            ),

        "next":
            (
                "032V25F_NONMONOTONE_KX_G3XX_FULL_TENSOR_METRIC_"
                "NUMERATOR_AND_BRANCH_STABILITY_GATE"
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
    """Insert one narrow theorem-backed region rule idempotently."""

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


def persist_v25e_region_rule(
    storage: Storage,
) -> int:
    """Persist only the monotone source-current anti-screening closure."""

    return _insert_rule_once(
        storage,
        family=
            "032_ACTIVE_STATE_NONLINEAR_KGB",

        family_version=
            "V25E",

        rule_type=
            "MONOTONE_SOURCE_ALIGNED_NONLINEAR_CURRENT_NO_ANTISCREEN",

        rule={
            "policy_specific":
                False,

            "scope":
                (
                    "STATIC_FLAT_SPHERICAL_G2_G3_WITH_"
                    "A_GT0_AS_GE0_B_GE0_BS_GE0"
                ),

            "closed":
                True,

            "closed_mechanism":
                "SOURCE_CURRENT_ANTISCREENING",

            "exact_identity":
                (
                    "D_MINUS_F_OVER_U_EQUALS_"
                    "U2_AS_PLUS_2UB_OVER_R_PLUS_2U3_BS_OVER_R"
                ),

            "elasticity_lower_bound":
                1.0,

            "nonmonotone_kxx_closed":
                False,

            "nonmonotone_g3xx_closed":
                False,

            "metric_braiding_numerator_closed":
                False,

            "full_tensor_kgb_closed":
                False,

            "oblate_source_closed":
                False,

            "g4_g5_closed":
                False,
        },

        proof_reference=
            "032V25E_NONLINEAR_SHIFT_CURRENT_JACOBIAN_THEOREM",
    )


def persist_v25e_metadata(
    storage: Storage,
) -> None:
    """Persist current frontier metadata only."""

    metadata = {
        "032v25e_exact_static_spherical_current":
            "1",

        "032v25e_monotone_source_current_antiscreen_closed":
            "1",

        "032v25e_nonmonotone_kxx_closed":
            "0",

        "032v25e_nonmonotone_g3xx_closed":
            "0",

        "032v25e_metric_braiding_numerator_analyzed":
            "0",

        "032v25e_full_tensor_stability_certified":
            "0",

        "032v25e_action_oracle_authorized":
            "0",

        "032v25e_blind_parameter_scan_authorized":
            "0",

        "agminer_next_family":
            (
                "NONMONOTONE_KX_G3XX_FULL_TENSOR_"
                "METRIC_NUMERATOR_BRANCH_STABILITY"
            ),
    }

    for key, value in metadata.items():
        storage.set_metadata(
            key,
            value,
        )
