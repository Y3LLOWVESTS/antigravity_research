"""032V25D large-KX source-reaction / canonical-scale gate.

PURPOSE
-------
V25A established an explicit shift-symmetric KGB action.

V25B closed the unchanged historical V16 hidden-axial source when inserted
into the minimal cubic KGB action because the canonically normalized cubic
interaction scale fell below the source variation momentum.

V25C then proved that simply embedding the same locally linear G3 interaction
inside a larger WBG parent Lambda_3 hierarchy does not improve the physical
canonical source-scale bound.

V25D now tests the next apparent rescue:

    large healthy K_X.

The gate is deliberately local and theorem-first.

LOCAL MODEL
-----------
Take a local background patch with

    K_X
        =
        kappa
        >
        0

approximately constant, negligible K_XX in the local source-response
equation, and locally linear cubic braiding

    G_3
        ~
        c_3 X.

Canonical normalization gives

    phi_c
        =
        sqrt(kappa) phi.

Therefore the hidden derivative-source interaction

    d_mu(phi) J_hidden^mu / f

becomes

    d_mu(phi_c) J_hidden^mu
    /
    [f sqrt(kappa)].

So large kappa suppresses the canonically normalized microscopic source
coupling by

    kappa^(-1/2).

FIXED MICROSCOPIC SOURCE
------------------------
If the local scalar current is dominated by the K_X term, an unchanged
microscopic source produces

    |grad(phi)|
        ~
        |grad(phi)|_0 / kappa.

Hence

    |grad(phi_c)|
        ~
        |grad(phi)|_0 / sqrt(kappa).

At fixed requested physical canonical gain A, the required physical cubic
scale follows from the same V25A relation in canonical variables.

This gives

    Lambda_local(kappa)
        =
        Lambda_local(1)
        kappa^(-1/3).

Equivalently, for a fixed parent Lambda_3, the locally linear cubic
coefficient needed to maintain the same physical gain scales as

    |c_3|
        ~
        kappa^(5/2).

Thus large constant K_X does NOT rescue the unchanged-source locally-linear
G3 branch. It worsens the local cubic-control ratio.

FIXED BACKGROUND GRADIENT
-------------------------
One can instead demand that |grad(phi)| remain fixed while kappa increases.

Then the K_X-dominated source current requires the microscopic source drive to
increase by

    source_drive_multiplier
        =
        kappa.

At fixed physical gain the local canonical cubic scale then improves only as

    Lambda_local
        ~
        kappa^(1/3).

So improving the control ratio by a factor R requires

    kappa
        =
        R^3

and therefore also an R^3 source-drive multiplier.

This is a source-reaction statement, NOT an energy statement.

CLAIM BOUNDARY
--------------
This V25D result closes only:

    HISTORICAL V16 SOURCE
        +
    LOCALLY CONSTANT POSITIVE K_X
        +
    LOCALLY LINEAR G3
        +
    SOURCE-DOMINATED STATIC LOCAL RESPONSE
        +
    UNCHANGED MICROSCOPIC SOURCE DRIVE

as a rescue of the V25B/V25C source-scale problem.

It does NOT close:

- nonlinear K(X) with important K_XX;
- genuinely nonlinear G3(X) with important G3XX;
- Vainshtein or kinetic regimes requiring a new nonlinear source solution;
- G4 or G5 WBG structure;
- multifield or multisector realizations;
- new hidden-source states;
- source sectors with genuinely higher microscopic scale;
- background-dependent kinetic matrices not reducible to constant kappa;
- the V25A action-existence result.

No complete energy estimate is made.

No action oracle, candidate, survivor, or physical antigravity claim is
created.

CLAIM_CLASSIFICATION=
LOCAL_CONSTANT_KX_SOURCE_REACTION_AND_CANONICAL_NORMALIZATION_FALSIFICATION
"""

from __future__ import annotations

import math
from typing import Any

from .kgb_strong_coupling_source_gate import (
    historical_source_compatibility,
)
from .storage import Storage


def _validate_kappa(
    kappa: float,
) -> float:
    value = float(
        kappa
    )

    if (
        not math.isfinite(
            value
        )
        or value < 1.0
    ):
        raise ValueError(
            "kappa must be finite and >= 1"
        )

    return value


def canonical_source_normalization(
    kappa: float,
) -> dict[str, float]:
    """Return canonical field/source normalization for constant K_X."""

    value = _validate_kappa(
        kappa
    )

    root = math.sqrt(
        value
    )

    return {
        "kappa":
            value,

        "canonical_field_multiplier":
            root,

        "canonical_hidden_source_coupling_relative":
            1.0
            /
            root,
    }


def fixed_source_gain_preserving_scaling(
    *,
    kappa: float,
    baseline_control_ratio: float,
) -> dict[str, Any]:
    """Return scaling with unchanged microscopic source drive.

    Assumptions:
        local constant K_X=kappa,
        locally linear G3,
        source-dominated current,
        same requested physical canonical gain.

    Then

        grad(phi) / grad(phi)_0
            =
            kappa^-1

        grad(phi_c) / grad(phi_c)_0
            =
            kappa^-1/2

        required c3 / c3_0
            =
            kappa^(5/2)

        Lambda_local / Lambda_local_0
            =
            kappa^-1/3.
    """

    value = _validate_kappa(
        kappa
    )

    baseline = float(
        baseline_control_ratio
    )

    if (
        not math.isfinite(
            baseline
        )
        or baseline <= 0.0
    ):
        raise ValueError(
            "baseline_control_ratio must be positive and finite"
        )

    scale_ratio = (
        value**(
            -1.0
            /
            3.0
        )
    )

    return {
        "kappa":
            value,

        "source_drive_multiplier":
            1.0,

        "background_gradient_relative":
            1.0
            /
            value,

        "canonical_background_gradient_relative":
            1.0
            /
            math.sqrt(
                value
            ),

        "canonical_hidden_source_coupling_relative":
            1.0
            /
            math.sqrt(
                value
            ),

        "required_linear_g3_coefficient_relative":
            value**2.5,

        "local_canonical_scale_relative":
            scale_ratio,

        "control_ratio":
            baseline
            *
            scale_ratio,

        "large_kx_improves_fixed_source_control":
            False,
    }


def fixed_gradient_gain_preserving_scaling(
    *,
    kappa: float,
    baseline_control_ratio: float,
) -> dict[str, Any]:
    """Return scaling when the background gradient is artificially held fixed.

    Holding grad(phi) fixed while K_X increases requires the source current to
    increase proportionally to kappa in the declared local source-dominated
    regime.

    At fixed physical gain:

        source drive
            ~ kappa

        canonical grad(phi)
            ~ sqrt(kappa)

        required c3
            ~ sqrt(kappa)

        local cubic scale
            ~ kappa^(1/3).
    """

    value = _validate_kappa(
        kappa
    )

    baseline = float(
        baseline_control_ratio
    )

    if (
        not math.isfinite(
            baseline
        )
        or baseline <= 0.0
    ):
        raise ValueError(
            "baseline_control_ratio must be positive and finite"
        )

    scale_ratio = (
        value**(
            1.0
            /
            3.0
        )
    )

    return {
        "kappa":
            value,

        "source_drive_multiplier":
            value,

        "background_gradient_relative":
            1.0,

        "canonical_background_gradient_relative":
            math.sqrt(
                value
            ),

        "canonical_hidden_source_coupling_relative":
            1.0
            /
            math.sqrt(
                value
            ),

        "required_linear_g3_coefficient_relative":
            math.sqrt(
                value
            ),

        "local_canonical_scale_relative":
            scale_ratio,

        "control_ratio":
            baseline
            *
            scale_ratio,

        "control_improvement_paid_by_source_reaction":
            True,
    }


def required_kappa_for_fixed_gradient_control(
    *,
    baseline_control_ratio: float,
    target_control_ratio: float,
) -> dict[str, float]:
    """Invert R = R0*kappa^(1/3)."""

    baseline = float(
        baseline_control_ratio
    )

    target = float(
        target_control_ratio
    )

    if (
        not math.isfinite(
            baseline
        )
        or baseline <= 0.0
    ):
        raise ValueError(
            "baseline control ratio must be positive and finite"
        )

    if (
        not math.isfinite(
            target
        )
        or target <= 0.0
    ):
        raise ValueError(
            "target control ratio must be positive and finite"
        )

    if target <= baseline:
        kappa = 1.0

    else:
        kappa = (
            target
            /
            baseline
        )**3

    state = (
        fixed_gradient_gain_preserving_scaling(
            kappa=
                kappa,

            baseline_control_ratio=
                baseline,
        )
    )

    return {
        "baseline_control_ratio":
            baseline,

        "target_control_ratio":
            target,

        "required_kappa":
            kappa,

        "required_source_drive_multiplier":
            state[
                "source_drive_multiplier"
            ],

        "canonical_source_coupling_relative":
            state[
                "canonical_hidden_source_coupling_relative"
            ],

        "reconstructed_control_ratio":
            state[
                "control_ratio"
            ],
    }


def local_constant_kx_theorem() -> dict[str, Any]:
    """Return the exact declared power-law theorem."""

    return {
        "local_model":
            "CONSTANT_POSITIVE_KX_PLUS_LOCALLY_LINEAR_G3",

        "fixed_source_gradient_exponent":
            -1.0,

        "fixed_source_canonical_gradient_exponent":
            -0.5,

        "fixed_source_required_g3_coefficient_exponent":
            2.5,

        "fixed_source_local_scale_exponent":
            -1.0
            /
            3.0,

        "fixed_gradient_source_drive_exponent":
            1.0,

        "fixed_gradient_required_g3_coefficient_exponent":
            0.5,

        "fixed_gradient_local_scale_exponent":
            1.0
            /
            3.0,

        "nonlinear_kxx_closed":
            False,

        "nonlinear_g3xx_closed":
            False,

        "full_wbg_g4_g5_closed":
            False,

        "source_energy_scaling_established":
            False,
    }


def historical_v16_kx_gate() -> dict[str, Any]:
    """Apply the theorem to the verified V25B historical-source ratio."""

    historical = (
        historical_source_compatibility()
    )

    baseline = float(
        historical[
            "a1e3_lambda_eff_over_source_k"
        ]
    )

    fixed_source_10 = (
        fixed_source_gain_preserving_scaling(
            kappa=
                10.0,

            baseline_control_ratio=
                baseline,
        )
    )

    fixed_source_1000 = (
        fixed_source_gain_preserving_scaling(
            kappa=
                1000.0,

            baseline_control_ratio=
                baseline,
        )
    )

    unit_control = (
        required_kappa_for_fixed_gradient_control(
            baseline_control_ratio=
                baseline,

            target_control_ratio=
                1.0,
        )
    )

    margin5 = (
        required_kappa_for_fixed_gradient_control(
            baseline_control_ratio=
                baseline,

            target_control_ratio=
                5.0,
        )
    )

    return {
        "historical_gradient_ev2":
            historical[
                "gradient_ev2"
            ],

        "historical_source_k_ev":
            historical[
                "source_variation_momentum_ev"
            ],

        "baseline_gain_times_planck":
            1.0e-3,

        "baseline_control_ratio":
            baseline,

        "fixed_source_kappa10_control_ratio":
            fixed_source_10[
                "control_ratio"
            ],

        "fixed_source_kappa1000_control_ratio":
            fixed_source_1000[
                "control_ratio"
            ],

        "fixed_source_kappa1000_required_g3_multiplier":
            fixed_source_1000[
                "required_linear_g3_coefficient_relative"
            ],

        "fixed_gradient_unit_control_required_kappa":
            unit_control[
                "required_kappa"
            ],

        "fixed_gradient_unit_control_source_drive_multiplier":
            unit_control[
                "required_source_drive_multiplier"
            ],

        "fixed_gradient_unit_control_canonical_source_coupling_relative":
            unit_control[
                "canonical_source_coupling_relative"
            ],

        "fixed_gradient_margin5_required_kappa":
            margin5[
                "required_kappa"
            ],

        "fixed_gradient_margin5_source_drive_multiplier":
            margin5[
                "required_source_drive_multiplier"
            ],

        "fixed_gradient_margin5_canonical_source_coupling_relative":
            margin5[
                "canonical_source_coupling_relative"
            ],

        "unchanged_source_large_constant_kx_rescue_closed":
            True,

        "fixed_gradient_large_kx_is_free_rescue":
            False,

        "source_reaction_must_be_included":
            True,

        "source_energy_multiplier_established":
            False,

        "nonlinear_kxx_closed":
            False,

        "nonlinear_g3xx_closed":
            False,

        "full_wbg_g4_g5_closed":
            False,

        "alternative_hidden_source_closed":
            False,
    }


def v25d_gate() -> dict[str, Any]:
    """Return the conservative V25D decision."""

    result = (
        historical_v16_kx_gate()
    )

    theorem = (
        local_constant_kx_theorem()
    )

    return {
        "large_constant_kx_fixed_source_rescue_closed":
            result[
                "unchanged_source_large_constant_kx_rescue_closed"
            ],

        "fixed_gradient_rescue_requires_source_reaction":
            result[
                "source_reaction_must_be_included"
            ],

        "source_energy_cost_established":
            theorem[
                "source_energy_scaling_established"
            ],

        "nonlinear_kxx_closed":
            False,

        "nonlinear_g3xx_closed":
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
                "RED_PARTIAL_032V25D_LARGE_CONSTANT_KX_DOES_NOT_"
                "RESCUE_UNCHANGED_V16_SOURCE_WITH_LOCALLY_LINEAR_G3__"
                "FIXED_GRADIENT_CONTROL_IMPROVEMENT_REQUIRES_KAPPA_"
                "PROPORTIONAL_SOURCE_REACTION__NONLINEAR_KXX_G3XX_"
                "AND_NEW_SOURCE_REMAIN_OPEN"
            ),

        "next":
            (
                "032V25E_NONLINEAR_KX_G3_SOURCE_CURRENT_"
                "AND_CANONICAL_RESPONSE_GATE"
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


def persist_v25d_region_rule(
    storage: Storage,
) -> int:
    """Persist only the fixed-source constant-KX locally-linear-G3 closure."""

    result = (
        historical_v16_kx_gate()
    )

    return _insert_rule_once(
        storage,
        family=
            "032_ACTIVE_STATE_WBG_KGB",

        family_version=
            "V25D",

        rule_type=
            "LARGE_CONSTANT_KX_FIXED_SOURCE_LOCALLY_LINEAR_G3_NO_RESCUE",

        rule={
            "policy_specific":
                False,

            "scope":
                (
                    "HISTORICAL_V16_SOURCE_PLUS_LOCAL_CONSTANT_POSITIVE_KX_"
                    "PLUS_LOCALLY_LINEAR_G3_PLUS_UNCHANGED_SOURCE_DRIVE"
                ),

            "closed":
                True,

            "baseline_control_ratio":
                result[
                    "baseline_control_ratio"
                ],

            "fixed_source_kappa10_control_ratio":
                result[
                    "fixed_source_kappa10_control_ratio"
                ],

            "fixed_source_kappa1000_control_ratio":
                result[
                    "fixed_source_kappa1000_control_ratio"
                ],

            "fixed_gradient_unit_control_required_kappa":
                result[
                    "fixed_gradient_unit_control_required_kappa"
                ],

            "fixed_gradient_margin5_required_kappa":
                result[
                    "fixed_gradient_margin5_required_kappa"
                ],

            "source_energy_multiplier_established":
                False,

            "nonlinear_kxx_closed":
                False,

            "nonlinear_g3xx_closed":
                False,

            "g4_g5_closed":
                False,

            "alternative_hidden_source_closed":
                False,

            "full_kgb_closed":
                False,
        },

        proof_reference=
            "032V25D_CONSTANT_KX_SOURCE_REACTION_CANONICAL_GATE",
    )


def persist_v25d_metadata(
    storage: Storage,
) -> None:
    """Persist frontier metadata only."""

    metadata = {
        "032v25d_large_constant_kx_fixed_source_rescue_closed":
            "1",

        "032v25d_fixed_gradient_requires_source_reaction":
            "1",

        "032v25d_source_energy_multiplier_established":
            "0",

        "032v25d_nonlinear_kxx_closed":
            "0",

        "032v25d_nonlinear_g3xx_closed":
            "0",

        "032v25d_full_wbg_g4_g5_closed":
            "0",

        "032v25d_full_tensor_crossprop_certified":
            "0",

        "032v25d_action_oracle_authorized":
            "0",

        "032v25d_blind_parameter_scan_authorized":
            "0",

        "agminer_next_family":
            (
                "NONLINEAR_KX_G3_SOURCE_CURRENT_"
                "CANONICAL_RESPONSE"
            ),
    }

    for key, value in metadata.items():
        storage.set_metadata(
            key,
            value,
        )
