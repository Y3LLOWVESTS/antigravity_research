"""032V26E1B1 — quadratic active-state conformal escape gate.

PURPOSE
-------
V26E1B0 established that the original V26D linear conformal factor

    A(x) = 1 + eta x

has the same leading pure-j0 physical matter operator as V17/V19:

    X T.

That exact canonical completion is therefore not reopened.

V26E1B1 tests the simplest genuinely different member of the SAME
invertible Class-Ia / Einstein-frame-equivalent V26D gravitational family:

    A_n(x)
        =
    1 + eta_n x^n

with

    n >= 2.

The primary candidate is n=2.

---------------------------------------------------------------------------
ACTIVE-STATE MATCHING
---------------------------------------------------------------------------

We preserve the representative V26D active response parameter

    beta_star = 1/21

at

    x_star = 0.1.

For

    A_n = 1 + eta x^n

define

    y = eta x_star^n.

Then

    beta_star
        =
    x A_x / A
        =
    n y /(1+y).

Solving gives

    y
        =
    beta_star /(n-beta_star).

For n=2 and beta_star=1/21:

    y = 1/41

    eta_2 = 100/41

    A_star = 42/41.

The conformal field-redefinition Jacobian is

    D_map
        =
    A - x A_x

so for n=2:

    D_map = 40/41.

This is comfortably nonsingular.

The tensor principal margin depends on the active beta_1:

    M_T,min
        =
    1 - 3 beta_1^2

and therefore remains

    146/147

when the same active beta_1 is preserved.

No principal-margin collapse is used.

---------------------------------------------------------------------------
OFF-STATE DIFFERENCE FROM V17/V19
---------------------------------------------------------------------------

For n=1:

    A^-1
        =
    1 - eta x + ...

and ordinary matter receives

    x T

at leading order.

That is the V17/V19 pure-j0 collision identified by V26E1B0.

For n=2:

    A^-1
        =
    1 - eta_2 x^2 + ...

so

    A_x(0) = 0

and there is NO O(x T) interaction at tree level.

The first universal matter interaction is instead

    x^2 T,

which contains four scalar legs.

Therefore the specific R5 two-scalar matter vertex is absent at tree level.

This is genuine active/off-state separation at the level of the leading
ordinary-matter operator.

It is NOT yet quantum silence.

---------------------------------------------------------------------------
WILSONIAN NDA DESCENDANT
---------------------------------------------------------------------------

Because x T is allowed by the same ordinary symmetries as x^2 T, scalar
contractions can regenerate a lower-order x T operator.

For a single x^n T vertex, contracting n-1 scalar pairs gives a Wilsonian
NDA descendant after n-1 loops.

At cutoff ratio

    Lambda_UV / Lambda = 1

use only the diagnostic estimate

    c1_desc
        ~
    eta_n
    [1/(16 pi^2)]^(n-1).

This is NOT:

    an exact beta function;
    a UV matching calculation;
    a naturalness certificate.

For comparison with the active response define

    s_NDA
        =
    |c1_desc|
    /
    |A_x/A|_active.

For the matched n=2 candidate this is approximately

    0.0324.

---------------------------------------------------------------------------
HISTORICAL V19R6 OVERLAP DIAGNOSTIC
---------------------------------------------------------------------------

The exact V19R6 tested implementation had

    empirical metric minimum
        =
    123456.884124... eV

and

    strict-energy metric maximum
        =
    122996.182444... eV.

For a pure-j0 force whose coefficient is reduced by relative factor s,
and whose old metric parameter scales as

    C1 ~ M^-4,

the old empirical bound would translate diagnostically to

    M_emp,new
        =
    M_emp,old s^(1/4).

The maximum relative off-state coupling that would merely reopen the old
overlap is

    s_required
        =
    (M_energy,max / M_emp,min)^4

        ~
    0.985.

Thus only a modest suppression was needed to eliminate the narrow historical
collision.

The n=2 Wilsonian NDA value

    s_NDA ~ 0.032

is far below that threshold.

This means:

    HISTORICAL EMPIRICAL/ENERGY HEADROOM WOULD REOPEN
    IF THE NDA DESCENDANT ESTIMATE AND OLD SOURCE SCALING APPLIED.

That statement is only a diagnostic.

The exact V19R6 energy boundary does NOT automatically transfer to this new
completion.

---------------------------------------------------------------------------
TECHNICAL NATURALNESS
---------------------------------------------------------------------------

The absence of x T at tree level is NOT protected by any symmetry already
declared in V26D.

All of the following allow x T:

    diffeomorphism invariance;
    shift symmetry phi -> phi + constant;
    Z2 phi -> -phi.

Both

    x T

and

    x^2 T

respect those symmetries.

Therefore setting the linear coefficient to zero does not currently
increase the symmetry of the action.

A UV threshold could consequently generate x T with a coefficient larger
than the low-energy NDA estimate.

Thus:

    TECHNICAL_NATURALNESS_CERTIFIED = NO.

But importantly:

    THE OLD EMPIRICAL COLLISION IS NO LONGER AN IMMEDIATE TREE-LEVEL
    THEOREM AGAINST THIS COMPLETION.

This is why the candidate is PROMISING CONDITIONAL rather than closed.

---------------------------------------------------------------------------
HIGHER POWERS
---------------------------------------------------------------------------

n=3 and n=4 are also tested at the same x_star and beta_star.

They:

    preserve the same active beta;
    have A_x(0)=0;
    remain well away from map singularity;
    remove the tree two-scalar vertex;
    push the first Wilsonian x T descendant to higher loop order.

However their required eta_n coefficients grow rapidly and no additional
symmetry is gained merely by increasing n.

Therefore n=2 is the preferred minimal representative.

---------------------------------------------------------------------------
WHAT THIS RUN DOES NOT ESTABLISH
---------------------------------------------------------------------------

It does NOT establish:

    a healthy lower-derivative scalar P/Q sector;
    the complete constrained scalar-metric symbol;
    physical hidden-source -> g00 response;
    outward sign;
    source reaction;
    finite payload;
    1g at 1m;
    microscopic source energy;
    UV matching;
    technical naturalness;
    complete energy.

The next scientific gate, if this run lands, is:

    explicit healthy n=2 scalar completion
    +
    frame-invariant physical g00 cross response
    +
    UV descendant bound.

---------------------------------------------------------------------------
PERFORMANCE POLICY
---------------------------------------------------------------------------

Minimum output floor:

    outward acceleration >= 9.80665 m/s^2

at

    true external stand-off >= 1.0 m.

Exceeding either floor is favorable.

---------------------------------------------------------------------------
ENERGY POLICY
---------------------------------------------------------------------------

No energy optimization.

The HOOK17 17.0676-J capacity reference does not transfer to V26D.

Complete V26D energy remains unknown.

CLAIM_CLASSIFICATION
--------------------
CLASSICAL_ACTIVE_OFFSTATE_SEPARATION_WITH_RADIATIVE_HEADROOM_DIAGNOSTIC
BUT_NO_TECHNICAL_NATURALNESS_CERTIFICATE
"""

from __future__ import annotations

import math
from typing import Any

from .v26e1b0_pure_j0_provenance_collision import (
    V19R6_EMPIRICAL_METRIC_MIN_EV,
    V19R6_ENERGY_METRIC_MAX_EV,
    v26e1b0_summary,
)


TOL = 1.0e-12

BETA_TARGET = (
    1.0
    /
    21.0
)

X_STAR = 0.10

STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

MIN_OUTWARD_ACCELERATION_M_S2 = 9.80665
MIN_TRUE_STANDOFF_M = 1.0


def v26e1b0_provenance_gate() -> dict[str, Any]:
    """Require the exact scoped E1B0 collision."""

    result = v26e1b0_summary()

    passed = bool(
        result[
            "v17_v19_operator_class_collision"
        ]
        and
        result[
            "exact_v17_equivalent_completion_closed"
        ]
        and
        not result[
            "all_v26d_completions_globally_closed"
        ]
        and
        result[
            "genuinely_new_v26d_completion_rerank_authorized"
        ]
        and
        not result[
            "energy_optimization_authorized"
        ]
    )

    return {
        "v26e1b0_provenance_pass":
            passed,

        "linear_completion_closed":
            result[
                "exact_v17_equivalent_completion_closed"
            ],

        "all_v26d_closed":
            result[
                "all_v26d_completions_globally_closed"
            ],

        "new_completion_authorized":
            result[
                "genuinely_new_v26d_completion_rerank_authorized"
            ],

        "old_empirical_metric_min_ev":
            result[
                "v19r6_empirical_metric_min_ev"
            ],

        "old_energy_metric_max_ev":
            result[
                "v19r6_strict_energy_metric_max_ev"
            ],
    }


def matched_power_activation(
    *,
    power: int,
    x_star: float = X_STAR,
    beta_target: float = BETA_TARGET,
) -> dict[str, Any]:
    """Match A=1+eta*x^n to a prescribed active beta_1."""

    n = int(
        power
    )

    x = float(
        x_star
    )

    beta = float(
        beta_target
    )

    if n < 1:
        raise ValueError(
            "power must be >=1"
        )

    if x <= 0.0:
        raise ValueError(
            "x_star must be positive"
        )

    if beta <= 0.0:
        raise ValueError(
            "beta_target must be positive"
        )

    if n <= beta:
        raise ValueError(
            "power must exceed beta_target"
        )

    y = (
        beta
        /
        (
            float(
                n
            )
            -
            beta
        )
    )

    eta = (
        y
        /
        x**n
    )

    a = (
        1.0
        +
        y
    )

    a_x = (
        float(
            n
        )
        *
        eta
        *
        x**(
            n
            -
            1
        )
    )

    beta_reconstructed = (
        x
        *
        a_x
        /
        a
    )

    active_slope = (
        a_x
        /
        a
    )

    d_map = (
        a
        -
        x
        *
        a_x
    )

    tensor_margin = (
        1.0
        -
        3.0
        *
        beta_reconstructed**2
    )

    if n == 1:
        a_x_offstate = eta
    else:
        a_x_offstate = 0.0

    leading_scalar_legs = (
        2
        *
        n
    )

    return {
        "power":
            n,

        "x_star":
            x,

        "beta_target":
            beta,

        "eta":
            eta,

        "eta_xn_at_active":
            y,

        "A_active":
            a,

        "A_x_active":
            a_x,

        "active_log_slope_Ax_over_A":
            active_slope,

        "beta_reconstructed":
            beta_reconstructed,

        "beta_reconstruction_error":
            abs(
                beta_reconstructed
                -
                beta
            ),

        "D_map_active":
            d_map,

        "map_invertible_active":
            bool(
                a
                >
                0.0
                and
                d_map
                >
                0.0
            ),

        "field_redefinition_margin_collapse":
            False,

        "A_offstate":
            1.0,

        "A_x_offstate":
            a_x_offstate,

        "beta_offstate":
            0.0,

        "leading_matter_operator_power_x":
            n,

        "leading_matter_scalar_leg_count":
            leading_scalar_legs,

        "tree_two_scalar_matter_vertex_present":
            bool(
                n
                ==
                1
            ),

        "r5_tree_two_scalar_vertex_absent":
            bool(
                n
                >=
                2
            ),

        "active_offstate_separation":
            bool(
                beta_reconstructed
                >
                0.0
                and
                abs(
                    a_x_offstate
                )
                <=
                TOL
            )
            if n
            >=
            2
            else
            False,

        "tensor_worst_relative_margin":
            tensor_margin,

        "tensor_margin_positive":
            bool(
                tensor_margin
                >
                0.0
            ),

        "principal_margin_gain_used":
            False,
    }


def quadratic_activation_gate() -> dict[str, Any]:
    """Return exact n=2 candidate diagnostics."""

    result = matched_power_activation(
        power=
            2
    )

    expected_eta = (
        100.0
        /
        41.0
    )

    expected_a = (
        42.0
        /
        41.0
    )

    expected_d = (
        40.0
        /
        41.0
    )

    expected_slope = (
        10.0
        /
        21.0
    )

    expected_tensor_margin = (
        146.0
        /
        147.0
    )

    exact_match = bool(
        abs(
            result[
                "eta"
            ]
            -
            expected_eta
        )
        <=
        TOL
        and
        abs(
            result[
                "A_active"
            ]
            -
            expected_a
        )
        <=
        TOL
        and
        abs(
            result[
                "D_map_active"
            ]
            -
            expected_d
        )
        <=
        TOL
        and
        abs(
            result[
                "active_log_slope_Ax_over_A"
            ]
            -
            expected_slope
        )
        <=
        TOL
        and
        abs(
            result[
                "tensor_worst_relative_margin"
            ]
            -
            expected_tensor_margin
        )
        <=
        TOL
    )

    return {
        **result,

        "expected_eta":
            expected_eta,

        "expected_A_active":
            expected_a,

        "expected_D_map_active":
            expected_d,

        "expected_active_log_slope":
            expected_slope,

        "expected_tensor_margin":
            expected_tensor_margin,

        "exact_quadratic_active_match":
            exact_match,

        "preferred_minimal_power_candidate":
            True,
    }


def power_family_rows() -> list[dict[str, Any]]:
    """Return n=2,3,4 active-state family diagnostics."""

    rows: list[
        dict[str, Any]
    ] = []

    for power in (
        2,
        3,
        4,
    ):
        rows.append(
            matched_power_activation(
                power=
                    power
            )
        )

    return rows


def power_family_gate() -> dict[str, Any]:
    """Require all tested powers to preserve active beta without singular maps."""

    rows = power_family_rows()

    all_beta = all(
        row[
            "beta_reconstruction_error"
        ]
        <=
        TOL
        for row in rows
    )

    all_map = all(
        row[
            "map_invertible_active"
        ]
        for row in rows
    )

    all_offstate = all(
        row[
            "r5_tree_two_scalar_vertex_absent"
        ]
        for row in rows
    )

    all_tensor = all(
        row[
            "tensor_margin_positive"
        ]
        for row in rows
    )

    minimum_map_margin = min(
        row[
            "D_map_active"
        ]
        for row in rows
    )

    maximum_eta = max(
        row[
            "eta"
        ]
        for row in rows
    )

    return {
        "power_count":
            len(
                rows
            ),

        "powers":
            [
                row[
                    "power"
                ]
                for row in rows
            ],

        "all_match_active_beta":
            all_beta,

        "all_active_maps_invertible":
            all_map,

        "all_remove_tree_r5_two_scalar_vertex":
            all_offstate,

        "all_tensor_margins_positive":
            all_tensor,

        "minimum_active_map_margin":
            minimum_map_margin,

        "maximum_eta":
            maximum_eta,

        "higher_power_eta_grows_rapidly":
            True,

        "higher_power_adds_new_symmetry":
            False,

        "family_classical_escape_pass":
            bool(
                all_beta
                and
                all_map
                and
                all_offstate
                and
                all_tensor
            ),
    }


def historical_overlap_suppression_gate() -> dict[str, Any]:
    """Return relative off-state suppression needed to reopen old R6 overlap."""

    empirical = float(
        V19R6_EMPIRICAL_METRIC_MIN_EV
    )

    energy_max = float(
        V19R6_ENERGY_METRIC_MAX_EV
    )

    required_relative_c1 = (
        energy_max
        /
        empirical
    )**4

    return {
        "old_empirical_metric_min_ev":
            empirical,

        "old_energy_metric_max_ev":
            energy_max,

        "old_metric_gap_ev":
            (
                empirical
                -
                energy_max
            ),

        "maximum_relative_offstate_c1_to_reopen_old_overlap":
            required_relative_c1,

        "suppression_fraction_required":
            (
                1.0
                -
                required_relative_c1
            ),

        "old_overlap_was_narrow":
            bool(
                required_relative_c1
                >
                0.90
            ),

        "diagnostic_only":
            True,

        "exact_old_energy_boundary_transfers_to_new_completion":
            False,
    }


def wilsonian_nda_descendant(
    *,
    power: int,
    cutoff_ratio: float = 1.0,
) -> dict[str, Any]:
    """Estimate lower-order xT descendant using Wilsonian NDA only."""

    row = matched_power_activation(
        power=
            power
    )

    n = int(
        power
    )

    ratio = float(
        cutoff_ratio
    )

    if ratio <= 0.0:
        raise ValueError(
            "cutoff_ratio must be positive"
        )

    loops = (
        n
        -
        1
    )

    one_loop = (
        1.0
        /
        (
            16.0
            *
            math.pi**2
        )
    )

    loop_factor = (
        one_loop**loops
    )

    cutoff_factor = (
        ratio**(
            4
            *
            loops
        )
    )

    c1_descendant = (
        row[
            "eta"
        ]
        *
        loop_factor
        *
        cutoff_factor
    )

    active_slope = abs(
        row[
            "active_log_slope_Ax_over_A"
        ]
    )

    relative_to_active = (
        abs(
            c1_descendant
        )
        /
        active_slope
    )

    overlap = historical_overlap_suppression_gate()

    required = overlap[
        "maximum_relative_offstate_c1_to_reopen_old_overlap"
    ]

    adjusted_empirical_min = (
        overlap[
            "old_empirical_metric_min_ev"
        ]
        *
        relative_to_active**0.25
    )

    combinatoric_headroom = (
        required
        /
        relative_to_active
    )

    return {
        "power":
            n,

        "assumed_cutoff_ratio_LambdaUV_over_Lambda":
            ratio,

        "wilsonian_loop_order_to_xT":
            loops,

        "one_loop_factor":
            one_loop,

        "loop_factor":
            loop_factor,

        "cutoff_power_factor":
            cutoff_factor,

        "nda_generated_xT_coefficient":
            c1_descendant,

        "active_log_slope":
            active_slope,

        "nda_relative_offstate_to_active_coupling":
            relative_to_active,

        "maximum_relative_offstate_coupling_for_old_overlap":
            required,

        "nda_below_old_overlap_threshold":
            bool(
                relative_to_active
                <
                required
            ),

        "diagnostic_adjusted_old_empirical_min_ev":
            adjusted_empirical_min,

        "old_energy_metric_max_ev":
            overlap[
                "old_energy_metric_max_ev"
            ],

        "historical_overlap_reopens_under_nda_assumptions":
            bool(
                adjusted_empirical_min
                <
                overlap[
                    "old_energy_metric_max_ev"
                ]
            ),

        "multiplicative_nda_uncertainty_headroom_before_old_overlap_closes":
            combinatoric_headroom,

        "exact_beta_function":
            False,

        "uv_matching_computed":
            False,

        "combinatoric_factors_computed":
            False,

        "nda_only":
            True,
    }


def nda_family_gate() -> dict[str, Any]:
    """Evaluate low-energy NDA descendants for n=2,3,4."""

    rows = [
        wilsonian_nda_descendant(
            power=
                power
        )
        for power in (
            2,
            3,
            4,
        )
    ]

    all_reopen = all(
        row[
            "historical_overlap_reopens_under_nda_assumptions"
        ]
        for row in rows
    )

    return {
        "row_count":
            len(
                rows
            ),

        "all_tested_powers_reopen_old_overlap_under_nda_assumptions":
            all_reopen,

        "n2_relative_offstate_to_active":
            rows[
                0
            ][
                "nda_relative_offstate_to_active_coupling"
            ],

        "n2_adjusted_old_empirical_min_ev":
            rows[
                0
            ][
                "diagnostic_adjusted_old_empirical_min_ev"
            ],

        "n2_multiplicative_uncertainty_headroom":
            rows[
                0
            ][
                "multiplicative_nda_uncertainty_headroom_before_old_overlap_closes"
            ],

        "nda_is_quantum_certification":
            False,

        "rows":
            rows,
    }


def technical_naturalness_gate() -> dict[str, Any]:
    """Audit whether A_x(0)=0 is protected by the declared V26D symmetries."""

    return {
        "diffeomorphism_symmetry_allows_xT":
            True,

        "shift_symmetry_allows_xT":
            True,

        "phi_Z2_allows_xT":
            True,

        "diffeomorphism_symmetry_allows_x2T":
            True,

        "shift_symmetry_allows_x2T":
            True,

        "phi_Z2_allows_x2T":
            True,

        "setting_xT_coefficient_zero_increases_declared_symmetry":
            False,

        "declared_symmetry_forbids_xT_but_allows_x2T":
            False,

        "fake_X_to_minus_X_parity_is_declared_field_symmetry":
            False,

        "low_energy_loops_can_generate_xT":
            True,

        "uv_threshold_can_generate_xT":
            True,

        "actual_beta_function_computed":
            False,

        "uv_matching_computed":
            False,

        "technical_naturalness_certified":
            False,

        "current_status":
            "RADIATIVE_HEADROOM_PRESENT_BUT_UV_PROTECTION_NOT_CERTIFIED",
    }


def quadratic_candidate_classification() -> dict[str, Any]:
    """Classify n=2 without overclaiming."""

    provenance = v26e1b0_provenance_gate()
    candidate = quadratic_activation_gate()
    overlap = historical_overlap_suppression_gate()
    nda = wilsonian_nda_descendant(
        power=
            2
    )
    naturalness = technical_naturalness_gate()

    classical_escape = bool(
        provenance[
            "v26e1b0_provenance_pass"
        ]
        and
        candidate[
            "exact_quadratic_active_match"
        ]
        and
        candidate[
            "active_offstate_separation"
        ]
        and
        candidate[
            "r5_tree_two_scalar_vertex_absent"
        ]
        and
        candidate[
            "map_invertible_active"
        ]
        and
        candidate[
            "tensor_margin_positive"
        ]
    )

    nda_headroom = bool(
        nda[
            "historical_overlap_reopens_under_nda_assumptions"
        ]
        and
        nda[
            "nda_relative_offstate_to_active_coupling"
        ]
        <
        overlap[
            "maximum_relative_offstate_c1_to_reopen_old_overlap"
        ]
    )

    return {
        "classical_escape_from_exact_e1b0_r5_collision":
            classical_escape,

        "same_active_beta_1_as_representative_v26d":
            bool(
                candidate[
                    "beta_reconstruction_error"
                ]
                <=
                TOL
            ),

        "active_beta_1":
            candidate[
                "beta_reconstructed"
            ],

        "offstate_beta_1":
            candidate[
                "beta_offstate"
            ],

        "tree_r5_two_scalar_vertex_absent":
            candidate[
                "r5_tree_two_scalar_vertex_absent"
            ],

        "active_map_margin":
            candidate[
                "D_map_active"
            ],

        "tensor_margin":
            candidate[
                "tensor_worst_relative_margin"
            ],

        "nda_radiative_headroom_present":
            nda_headroom,

        "nda_relative_offstate_to_active":
            nda[
                "nda_relative_offstate_to_active_coupling"
            ],

        "nda_adjusted_old_empirical_min_ev":
            nda[
                "diagnostic_adjusted_old_empirical_min_ev"
            ],

        "old_energy_metric_max_ev":
            nda[
                "old_energy_metric_max_ev"
            ],

        "technical_naturalness_certified":
            naturalness[
                "technical_naturalness_certified"
            ],

        "uv_protection_required":
            True,

        "full_scalar_health_established":
            False,

        "physical_g00_cross_response_established":
            False,

        "candidate_status":
            (
                "PROMISING_CONDITIONAL_ACTIVE_STATE_COMPLETION"
                if (
                    classical_escape
                    and
                    nda_headroom
                )
                else
                "CHECK_QUADRATIC_ACTIVE_STATE_ESCAPE"
            ),

        "physical_model":
            False,
    }


def v26e1b1_summary() -> dict[str, Any]:
    """Return conservative E1B1 result."""

    provenance = v26e1b0_provenance_gate()
    quadratic = quadratic_candidate_classification()
    family = power_family_gate()
    nda = nda_family_gate()
    naturalness = technical_naturalness_gate()

    promising = bool(
        provenance[
            "v26e1b0_provenance_pass"
        ]
        and
        quadratic[
            "classical_escape_from_exact_e1b0_r5_collision"
        ]
        and
        quadratic[
            "nda_radiative_headroom_present"
        ]
        and
        family[
            "family_classical_escape_pass"
        ]
    )

    return {
        "branch":
            "032V26E1B1",

        "subgate":
            "QUADRATIC_ACTIVE_STATE_CONFORMAL_ESCAPE_AND_RADIATIVE_HEADROOM",

        "decision":
            (
                "YELLOW_PROMISING_V26E1B1_QUADRATIC_ACTIVE_STATE_"
                "COMPLETION_REMOVES_TREE_R5_TWO_SCALAR_VERTEX_WHILE_"
                "PRESERVING_ACTIVE_BETA_AND_HEALTHY_MAP__LOW_ENERGY_NDA_"
                "DESCENDANT_HAS_HISTORICAL_EMPIRICAL_HEADROOM__UV_"
                "NATURALNESS_AND_FULL_CROSSPROP_REMAIN_OPEN"
            )
            if promising
            else
            "CHECK_V26E1B1_ACTIVE_STATE_ESCAPE",

        "v26e1b0_provenance_pass":
            provenance[
                "v26e1b0_provenance_pass"
            ],

        "quadratic_active_state_classical_escape":
            quadratic[
                "classical_escape_from_exact_e1b0_r5_collision"
            ],

        "quadratic_candidate_status":
            quadratic[
                "candidate_status"
            ],

        "quadratic_eta":
            quadratic_activation_gate()[
                "eta"
            ],

        "quadratic_active_beta_1":
            quadratic[
                "active_beta_1"
            ],

        "quadratic_offstate_beta_1":
            quadratic[
                "offstate_beta_1"
            ],

        "quadratic_active_map_margin":
            quadratic[
                "active_map_margin"
            ],

        "quadratic_tensor_margin":
            quadratic[
                "tensor_margin"
            ],

        "quadratic_tree_r5_two_scalar_vertex_absent":
            quadratic[
                "tree_r5_two_scalar_vertex_absent"
            ],

        "power_family_classical_escape_pass":
            family[
                "family_classical_escape_pass"
            ],

        "old_overlap_required_relative_offstate_c1":
            historical_overlap_suppression_gate()[
                "maximum_relative_offstate_c1_to_reopen_old_overlap"
            ],

        "quadratic_nda_relative_offstate_to_active":
            quadratic[
                "nda_relative_offstate_to_active"
            ],

        "quadratic_nda_adjusted_old_empirical_min_ev":
            quadratic[
                "nda_adjusted_old_empirical_min_ev"
            ],

        "old_energy_metric_max_ev":
            quadratic[
                "old_energy_metric_max_ev"
            ],

        "quadratic_nda_radiative_headroom_present":
            quadratic[
                "nda_radiative_headroom_present"
            ],

        "quadratic_nda_uncertainty_headroom_factor":
            nda[
                "n2_multiplicative_uncertainty_headroom"
            ],

        "nda_is_quantum_certification":
            nda[
                "nda_is_quantum_certification"
            ],

        "technical_naturalness_certified":
            naturalness[
                "technical_naturalness_certified"
            ],

        "uv_matching_computed":
            naturalness[
                "uv_matching_computed"
            ],

        "current_naturalness_status":
            naturalness[
                "current_status"
            ],

        "full_static_spacelike_scalar_health_established":
            False,

        "physical_g00_cross_response_established":
            False,

        "frame_invariant_response_established":
            False,

        "outward_sign_established":
            False,

        "finite_payload_established":
            False,

        "minimum_required_outward_acceleration_m_s2":
            MIN_OUTWARD_ACCELERATION_M_S2,

        "minimum_required_true_standoff_m":
            MIN_TRUE_STANDOFF_M,

        "performance_above_floor_is_favorable":
            True,

        "v26d_field_capacity_j":
            None,

        "v26d_complete_energy_j":
            None,

        "hook17_capacity_reference_transfers_to_v26d":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "energy_optimization_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "quadratic_candidate_promoted_to_next_physical_gate":
            promising,

        "next":
            (
                "032V26E1B2_QUADRATIC_ACTIVE_STATE_HEALTHY_SCALAR_"
                "PHYSICAL_G00_CROSSPROP_AND_UV_DESCENDANT_GATE"
            ),

        "claim_scope":
            (
                "CLASSICAL ACTIVE/OFFSTATE OPERATOR SEPARATION PLUS "
                "LOW-ENERGY WILSONIAN NDA HEADROOM; NOT TECHNICAL-"
                "NATURALNESS OR PHYSICAL ANTIGRAVITY CERTIFICATION"
            ),
    }
