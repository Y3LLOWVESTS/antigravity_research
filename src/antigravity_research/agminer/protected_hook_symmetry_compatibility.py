"""032V26C protected-hook same-action symmetry compatibility gate.

PURPOSE
-------
Test whether the algebraically promising V26B1 quadratic hook-metric
descendant can coexist with a symmetry-protected healthy metric-affine action
that also accepts the actual V24 intrinsic Dirac hook source.

V26B1 established:

    H_a(bc) != 0

for the clean Dirac rest particle/antiparticle source and found quadratic
rank-two metric descendants such as

    B_mn
        =
    H_a m b H^a_n{}^b

with:

    B_00 != 0.

V26B1 also established:

    dB/dH = 0 at H = 0

but:

    dB/dH != 0 around H_bar != 0.

This is an attractive active-state NUMERATOR and does not rely on a collapsing
principal eigenvalue.

V26B1R1 then showed that the corresponding unavoidable two-mediator off-state
force does not by itself close the architecture under the declared optimistic
capacity preflight.

The next question is more fundamental:

    CAN THE SOURCE AND THE QUADRATIC UNIVERSAL METRIC
    COEXIST WITH THE SYMMETRY THAT MAKES A HEALTHY
    PUBLISHED HOOK-CARRYING ACTION POSSIBLE?

PERCACCI-SEZGIN MASSLESS EXTENDED FRONSDAL SECTOR
-------------------------------------------------
Percacci and Sezgin, arXiv:2508.14211, consider a rank-three nonmetricity field

    Q_rho mu nu = Q_rho nu mu.

Their extended massless Fronsdal Lagrangian has both the usual higher-spin
gauge transformation and an independent hook shift

    delta_xi Q_rho mu nu
        =
    xi_rho mu nu

with

    xi_(rho mu nu)
        =
    0.

They state that all hook-symmetric degrees of freedom in this realization are
pure gauge.

This gives two immediate same-action tests.

1. SOURCE WARD TEST

A direct source coupling

    S_src
        =
    integral J^rho mu nu Q_rho mu nu

changes under the hook shift by

    delta S_src
        =
    integral J^rho mu nu xi_rho mu nu.

Gauge compatibility requires the source to annihilate every allowed hook
parameter.

The actual V24 source contains a nonzero hook component H.

Choosing the allowed gauge parameter

    xi = H

is therefore a decisive witness. If

    H_abc H^abc != 0,

the direct clean hook source is not compatible with the massless hook-shift
symmetry without an additional compensator or a deformation of the symmetry.

2. UNIVERSAL PHYSICAL-METRIC TEST

The V26B1 scaffold uses a quadratic descendant schematically

    g_phys
        =
    g
        +
    alpha Q(H,H)
        + ...

For an infinitesimal hook shift,

    H -> H + xi,

the first variation on a general active background is

    delta_xi Q(H,H)
        =
    2 Q(H,xi).

At the exact off state H=0 this first variation vanishes.

That is useful for suppressing linear off-state response.

However a gauge symmetry must hold on the full field configuration space, not
only at H=0.

Choosing

    xi = H

on an active background gives

    delta_xi Q(H,H)
        =
    2 Q(H,H),

which is nonzero whenever the desired active metric numerator is nonzero.

Therefore the simple zero-derivative H^2 universal metric is not invariant
under this published massless hook-shift symmetry.

This does NOT mean all quadratic active-state portals are impossible.

It means the current H^2 scaffold cannot simply be attached to the protected
massless extended-Fronsdal action while retaining its hook-shift protection.

PUBLISHED MASSIVE SPIN-3 SECTOR
-------------------------------
The same Percacci-Sezgin work also constructs healthy massive spin-3 sectors
at linearized level.

Those target models are explicitly chosen to have no gauge symmetries.

The hook components can act as auxiliary degrees of freedom.

That preserves a logical MAG possibility, but it is not yet the required
symmetry-protected same-action chain:

    intrinsic Dirac hook source
        ->
    healthy propagating geometric mode
        ->
    universal physical metric.

The paper itself discusses the difficulty of extending higher-spin gauge
symmetry to interactions and notes that coefficient-based suppression without
a protecting symmetry can be vulnerable to radiative corrections.

Therefore the massive sector remains:

    OPEN AT FREE / QUADRATIC LEVEL

but is not promoted as the V26 same-action survivor.

BARKER-MARZO-SANTONI TORSION-LIKE CATALOGUE
--------------------------------------------
arXiv:2507.05349 classifies linear pair-antisymmetric rank-three theories by
their underlying gauge symmetries and finds healthy vector torsion modes.

V24C established an exact representation map

    DIRAC HOOK
        <->
    PAIR-ANTISYMMETRIC TORSION-LIKE TENSOR.

But V24C also established that the clean rest-pair direct totally symmetric
trace-vector source is zero, and explicitly warned:

    REPRESENTATION MATCH
    IS NOT
    ACTION / PROJECTOR MATCH.

Other protected torsion-like vector channels are not closed here.

MARZO 2026 VECTOR-GRAVITON SYSTEM
--------------------------------
arXiv:2603.24008 contains quadratic vector-graviton mixing and consistent
cubic/quartic deformations.

V24D established for the tested linear source channel that the apparent
source-to-metric transfer is removable after Stueckelberg / Ward
reconstruction:

    NONREMOVABLE LINEAR VECTOR-METRIC CROSS SOURCE
    =
    FALSE.

Its nonlinear completion remains logically open.

However no same-action identification of the V24 Dirac hook with the Marzo
vector source has been derived.

SCOPE
-----
This gate can close:

    THE CURRENT ZERO-DERIVATIVE H^2 UNIVERSAL METRIC
    ATTACHED DIRECTLY TO THE MASSLESS
    HOOK-SHIFT-PROTECTED EXTENDED-FRONSDAL ACTION.

It does NOT close:

- all metric-affine gravity;
- massive nonmetricity theories;
- nonlinear gauge deformations;
- compensator constructions;
- derivative gauge-invariant hook curvatures;
- other torsion-like protected vector channels;
- the Marzo nonlinear completion;
- generic intrinsic Dirac hypermomentum.

PROMOTION LOGIC
---------------
If the current H^2 scaffold violates the exact hook-shift protection and no
already identified same-action alternative survives, do NOT start an expensive
MAG parameter search or energy optimization.

Park the nonlinear MAG architecture with a precise reopen condition:

    EXPLICIT NONLINEAR SYMMETRY-COMPATIBLE ACTION

that simultaneously supplies:

    DIRAC SOURCE
    +
    HEALTHY CARRIER
    +
    ONE UNIVERSAL METRIC
    +
    NONREMOVABLE RESPONSE.

Then promote the already preserved alternative V26 family:

    c_T = 1
    DHOST / BEYOND-HORNDESKI
    ACTIVE-STATE KINETIC-MATTER-MIXING

to the next explicit-action gate.

CLAIM LIMITS
------------
This module does not establish a practical antigravity model.

It does not establish finite-payload response, microscopic support, complete
energy, nonlinear stability, naturalness, or empirical viability.

No AGMINER candidate, rejection, action oracle, mechanism metric, survivor, or
region rule is created.

CLAIM_CLASSIFICATION=
SCOPED_SAME_ACTION_HOOK_GAUGE_SYMMETRY_COMPATIBILITY_NO_GO
"""

from __future__ import annotations

import itertools
import math
from typing import Any

import numpy as np

from .dirac_hook_vector_bridge import (
    generic_bms_spin1_trace_witness,
    hook_torsionlike_map_diagnostics,
    marzo_2026_vector_graviton_bridge_template,
    rest_pair_bms_spin1_trace_gate,
)
from .nonlinear_hook_metric_bridge import (
    quadratic_active_background_derivative,
    quadratic_metric_descendant,
    raise_all_indices,
    rest_pair_hook,
)


def _validate_rank3(
    tensor: np.ndarray,
    name: str,
) -> np.ndarray:
    """Return a finite real rank-three Lorentz tensor."""
    value = np.asarray(
        tensor,
        dtype=float,
    )

    if value.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            f"{name} must have shape (4,4,4)"
        )

    if not np.all(
        np.isfinite(
            value
        )
    ):
        raise ValueError(
            f"{name} must be finite"
        )

    return value


def fully_symmetric_rank3(
    tensor: np.ndarray,
) -> np.ndarray:
    """Return T_(abc) by averaging all six index permutations."""
    value = _validate_rank3(
        tensor,
        "tensor",
    )

    result = np.zeros_like(
        value
    )

    for permutation in itertools.permutations(
        (
            0,
            1,
            2,
        )
    ):
        result += np.transpose(
            value,
            permutation,
        )

    return (
        result
        /
        6.0
    )


def hook_projection_diagnostics(
    tensor: np.ndarray,
) -> dict[str, Any]:
    """Return total-symmetric versus hook content diagnostics."""
    value = _validate_rank3(
        tensor,
        "tensor",
    )

    symmetric = (
        fully_symmetric_rank3(
            value
        )
    )

    hook = (
        value
        -
        symmetric
    )

    value_norm = float(
        np.linalg.norm(
            value
        )
    )

    symmetric_norm = float(
        np.linalg.norm(
            symmetric
        )
    )

    hook_norm = float(
        np.linalg.norm(
            hook
        )
    )

    relative_symmetric_norm = (
        symmetric_norm
        /
        max(
            value_norm,
            1.0,
        )
    )

    reconstruction_error = float(
        np.linalg.norm(
            symmetric
            +
            hook
            -
            value
        )
        /
        max(
            value_norm,
            1.0,
        )
    )

    return {
        "tensor_norm":
            value_norm,

        "fully_symmetric_norm":
            symmetric_norm,

        "hook_norm":
            hook_norm,

        "relative_fully_symmetric_norm":
            relative_symmetric_norm,

        "hook_nonzero":
            bool(
                hook_norm
                >
                1.0e-12
            ),

        "fully_symmetric_part_zero":
            bool(
                relative_symmetric_norm
                <
                1.0e-12
            ),

        "reconstruction_relative_error":
            reconstruction_error,

        "pure_hook_within_tolerance":
            bool(
                hook_norm
                >
                1.0e-12
                and
                relative_symmetric_norm
                <
                1.0e-12
                and
                reconstruction_error
                <
                1.0e-12
            ),
    }


def lorentz_rank3_contraction(
    first_covariant: np.ndarray,
    second_covariant: np.ndarray,
) -> float:
    """Return A_abc B^abc using the project Minkowski convention."""
    first = _validate_rank3(
        first_covariant,
        "first_covariant",
    )

    second = _validate_rank3(
        second_covariant,
        "second_covariant",
    )

    second_raised = (
        raise_all_indices(
            second
        )
    )

    return float(
        np.einsum(
            "abc,abc->",
            first,
            second_raised,
        )
    )


def massless_hook_shift_source_ward_gate() -> dict[str, Any]:
    """Test the actual V24 hook against the massless hook-shift Ward identity.

    The published symmetry permits any hook-symmetric xi. Choosing xi equal to
    the actual source hook gives a sufficient incompatibility witness whenever

        J_abc xi^abc != 0.
    """
    hook = (
        rest_pair_hook()
    )

    decomposition = (
        hook_projection_diagnostics(
            hook
        )
    )

    source_shift_variation = (
        lorentz_rank3_contraction(
            hook,
            hook,
        )
    )

    variation_abs = abs(
        source_shift_variation
    )

    return {
        "published_massless_hook_shift":
            "delta_xi Q_rmn = xi_rmn",

        "published_hook_parameter_constraint":
            "xi_(rmn)=0",

        "actual_v24_source_hook_nonzero":
            decomposition[
                "hook_nonzero"
            ],

        "actual_v24_source_pure_hook_within_tolerance":
            decomposition[
                "pure_hook_within_tolerance"
            ],

        "actual_hook_tensor_norm":
            decomposition[
                "tensor_norm"
            ],

        "actual_hook_fully_symmetric_relative_norm":
            decomposition[
                "relative_fully_symmetric_norm"
            ],

        "chosen_ward_parameter":
            "xi=J_hook",

        "source_shift_variation":
            source_shift_variation,

        "source_shift_variation_abs":
            variation_abs,

        "source_shift_variation_nonzero":
            bool(
                variation_abs
                >
                1.0e-12
            ),

        "direct_hook_source_respects_published_massless_hook_shift":
            bool(
                variation_abs
                <=
                1.0e-12
            ),

        "compensator_included":
            False,

        "nonlinear_source_transformation_derived":
            False,
    }


def quadratic_metric_hook_shift_gate() -> dict[str, Any]:
    """Test V26B1's B(H,H) metric descendant under the hook shift."""
    hook = (
        rest_pair_hook()
    )

    zero_hook = np.zeros_like(
        hook
    )

    metric_tensor = (
        quadratic_metric_descendant(
            hook,
            coefficient_a=
                0.0,
            coefficient_b=
                1.0,
            coefficient_c=
                0.0,
        )
    )

    offstate_first_variation = (
        quadratic_active_background_derivative(
            zero_hook,
            hook,
            coefficient_a=
                0.0,
            coefficient_b=
                1.0,
            coefficient_c=
                0.0,
        )
    )

    active_first_variation = (
        quadratic_active_background_derivative(
            hook,
            hook,
            coefficient_a=
                0.0,
            coefficient_b=
                1.0,
            coefficient_c=
                0.0,
        )
    )

    expected_active_variation = (
        2.0
        *
        metric_tensor
    )

    metric_norm = float(
        np.linalg.norm(
            metric_tensor
        )
    )

    offstate_norm = float(
        np.linalg.norm(
            offstate_first_variation
        )
    )

    active_norm = float(
        np.linalg.norm(
            active_first_variation
        )
    )

    identity_error = float(
        np.linalg.norm(
            active_first_variation
            -
            expected_active_variation
        )
        /
        max(
            np.linalg.norm(
                expected_active_variation
            ),
            1.0,
        )
    )

    return {
        "selected_quadratic_basis":
            "B_mn=H_a m b H^a_n{}^b",

        "quadratic_metric_tensor_norm":
            metric_norm,

        "quadratic_metric_g00":
            float(
                metric_tensor[
                    0,
                    0
                ]
            ),

        "quadratic_metric_g00_nonzero":
            bool(
                abs(
                    float(
                        metric_tensor[
                            0,
                            0
                        ]
                    )
                )
                >
                1.0e-12
            ),

        "offstate_first_variation_norm":
            offstate_norm,

        "offstate_first_variation_zero":
            bool(
                offstate_norm
                <
                1.0e-12
            ),

        "active_first_variation_norm":
            active_norm,

        "active_first_variation_g00":
            float(
                active_first_variation[
                    0,
                    0
                ]
            ),

        "active_first_variation_nonzero":
            bool(
                active_norm
                >
                1.0e-12
            ),

        "degree_two_identity_relative_error":
            identity_error,

        "degree_two_identity_pass":
            bool(
                identity_error
                <
                1.0e-12
            ),

        "quadratic_metric_respects_hook_shift_on_all_backgrounds":
            bool(
                active_norm
                <
                1.0e-12
            ),

        "offstate_linear_null_is_full_gauge_invariance":
            False,

        "compensating_metric_transformation_derived":
            False,

        "nonlinear_hook_shift_deformation_derived":
            False,
    }


def percacci_sezgin_massless_same_action_gate() -> dict[str, Any]:
    """Return the scoped massless extended-Fronsdal same-action decision."""
    source = (
        massless_hook_shift_source_ward_gate()
    )

    metric = (
        quadratic_metric_hook_shift_gate()
    )

    source_compatible = bool(
        source[
            "direct_hook_source_respects_published_massless_hook_shift"
        ]
    )

    metric_compatible = bool(
        metric[
            "quadratic_metric_respects_hook_shift_on_all_backgrounds"
        ]
    )

    same_action = bool(
        source_compatible
        and
        metric_compatible
    )

    return {
        "reference":
            "Percacci-Sezgin arXiv:2508.14211",

        "sector":
            "MASSLESS_EXTENDED_FRONSDAL_WITH_HOOK_SHIFT",

        "massless_spin3_propagates":
            True,

        "hook_degrees_pure_gauge_in_published_sector":
            True,

        "actual_v24_direct_hook_source_shift_compatible":
            source_compatible,

        "v26b1_quadratic_metric_shift_compatible":
            metric_compatible,

        "current_same_action_hook_source_plus_h2_metric":
            same_action,

        "current_h2_scaffold_closed_for_this_published_massless_sector":
            bool(
                not same_action
            ),

        "all_massless_metric_affine_theories_closed":
            False,

        "all_metric_affine_gravity_closed":
            False,

        "reopen_condition":
            (
                "EXPLICIT_COMPENSATOR_OR_NONLINEAR_GAUGE_DEFORMATION_"
                "MAKING_BOTH_SOURCE_AND_UNIVERSAL_METRIC_WARD_COMPATIBLE"
            ),
    }


def percacci_sezgin_massive_gate() -> dict[str, Any]:
    """Return conservative status of the published massive spin-three sector."""
    return {
        "reference":
            "Percacci-Sezgin arXiv:2508.14211",

        "sector":
            "MASSIVE_SPIN3_LINEARIZED",

        "healthy_massive_spin3_region_reported":
            True,

        "target_models_have_no_gauge_symmetries":
            True,

        "hook_can_act_as_auxiliary_component":
            True,

        "actual_v24_dirac_hook_to_propagating_spin3_source_match":
            False,

        "universal_h2_metric_same_action_derived":
            False,

        "nonlinear_interacting_completion_established":
            False,

        "radiative_protection_of_required_coefficient_relations_established":
            False,

        "current_same_action_survivor":
            False,

        "sector_globally_closed":
            False,

        "promotion_status":
            "OPEN_FREE_LEVEL_NOT_CURRENT_SYMMETRY_PROTECTED_SURVIVOR",
    }


def bms_torsionlike_same_action_gate() -> dict[str, Any]:
    """Return V24C plus symmetry-first torsion-like action compatibility."""
    trace_gate = (
        rest_pair_bms_spin1_trace_gate()
    )

    generic = (
        generic_bms_spin1_trace_witness()
    )

    hook_map = (
        hook_torsionlike_map_diagnostics()
    )

    return {
        "reference":
            "Barker-Marzo-Santoni arXiv:2507.05349",

        "healthy_pair_antisymmetric_vector_models_exist":
            True,

        "models_selected_by_gauge_symmetry":
            True,

        "actual_hook_to_torsionlike_representation_map":
            hook_map[
                "representation_map_invertible_on_declared_hook_space"
            ],

        "clean_pair_source_addition_survives_map":
            hook_map[
                "pair_torsionlike_equals_two_single"
            ],

        "clean_rest_pair_direct_protected_trace_vector_source_closed":
            trace_gate[
                "rest_pair_direct_bms_protected_spin1_source_closed"
            ],

        "generic_algebraic_trace_carrier_nonzero":
            generic[
                "generic_algebraic_trace_carrier_nonzero"
            ],

        "generic_witness_on_shell_localized_stationary":
            generic[
                "spinor_is_on_shell_localized_stationary_source"
            ],

        "generic_source_ward_identity_established":
            generic[
                "source_ward_identity_established"
            ],

        "other_protected_vector_channels_closed":
            False,

        "universal_physical_metric_bridge_same_action_established":
            False,

        "current_same_action_survivor":
            False,

        "promotion_status":
            "OPEN_SOURCE_ACTION_MATCH_UNRESOLVED",
    }


def marzo_nonlinear_same_action_gate() -> dict[str, Any]:
    """Return the post-V24D status of the Marzo nonlinear bridge family."""
    template = (
        marzo_2026_vector_graviton_bridge_template()
    )

    return {
        "reference":
            "Marzo arXiv:2603.24008",

        "quadratic_vector_graviton_mixing":
            template[
                "quadratic_vector_graviton_mixing"
            ],

        "massless_spin2_propagates":
            template[
                "massless_spin2_propagates"
            ],

        "massive_spin1_propagates":
            template[
                "massive_spin1_propagates"
            ],

        "unitary_open_region_reported":
            template[
                "unitary_open_region_reported"
            ],

        "consistent_cubic_deformation_found":
            template[
                "consistent_cubic_deformation_found"
            ],

        "consistent_quartic_noether_test":
            template[
                "consistent_quartic_order_noether_test_passed"
            ],

        "external_dirac_source_coupling_derived":
            template[
                "external_dirac_source_coupling_derived"
            ],

        "vector_identified_with_v24_hook":
            template[
                "vector_identified_with_v24c_hook_torsionlike_mode"
            ],

        "v24d_nonremovable_linear_vector_metric_cross_source":
            False,

        "v24d_linear_route_closed":
            True,

        "nonlinear_completion_globally_closed":
            False,

        "current_same_action_survivor":
            False,

        "promotion_status":
            "OPEN_NONLINEAR_ONLY_NO_DIRAC_HOOK_ACTION_MATCH",
    }


def v26c_action_compatibility_atlas() -> list[dict[str, Any]]:
    """Return current symmetry/action-level MAG compatibility ordering."""
    massless = (
        percacci_sezgin_massless_same_action_gate()
    )

    massive = (
        percacci_sezgin_massive_gate()
    )

    bms = (
        bms_torsionlike_same_action_gate()
    )

    marzo = (
        marzo_nonlinear_same_action_gate()
    )

    return [
        {
            "priority":
                1,

            "family":
                "PERCACCI_SEZGIN_MASSLESS_EXTENDED_FRONSDAL_HOOK",

            "status":
                "RED_CURRENT_H2_SCAFFOLD",

            "same_action_survivor":
                massless[
                    "current_same_action_hook_source_plus_h2_metric"
                ],

            "reason":
                (
                    "ACTUAL_V24_HOOK_SOURCE_AND_ACTIVE_H2_UNIVERSAL_METRIC_"
                    "BOTH_CONFLICT_WITH_EXACT_HOOK_SHIFT_PROTECTION"
                ),
        },
        {
            "priority":
                2,

            "family":
                "PERCACCI_SEZGIN_MASSIVE_SPIN3",

            "status":
                "OPEN_FREE_LEVEL_UNPROTECTED_FOR_CURRENT_PURPOSE",

            "same_action_survivor":
                massive[
                    "current_same_action_survivor"
                ],

            "reason":
                (
                    "HEALTHY_LINEAR_MASSIVE_SPIN3_EXISTS_BUT_CURRENT_DIRAC_"
                    "HOOK_SOURCE_METRIC_CHAIN_AND_RADIATIVE_PROTECTION_MISSING"
                ),
        },
        {
            "priority":
                2,

            "family":
                "BMS_TORSIONLIKE_PROTECTED_VECTOR",

            "status":
                "OPEN_SOURCE_ACTION_MATCH_UNRESOLVED",

            "same_action_survivor":
                bms[
                    "current_same_action_survivor"
                ],

            "reason":
                (
                    "REPRESENTATION_MAP_SURVIVES_BUT_CLEAN_TRACE_VECTOR_"
                    "SOURCE_IS_ZERO_AND_OTHER_ACTION_PROJECTOR_MATCHES_UNPROVEN"
                ),
        },
        {
            "priority":
                2,

            "family":
                "MARZO_2026_NONLINEAR_VECTOR_GRAVITON",

            "status":
                "OPEN_NONLINEAR_ONLY",

            "same_action_survivor":
                marzo[
                    "current_same_action_survivor"
                ],

            "reason":
                (
                    "LINEAR_PHYSICAL_CROSS_SOURCE_CLOSED_BY_V24D; "
                    "NONLINEAR_COMPLETION_OPEN_BUT_NO_DIRAC_HOOK_MATCH"
                ),
        },
        {
            "priority":
                3,

            "family":
                "CUSTOM_NONLINEAR_HOOK_H2_METRIC",

            "status":
                "NOT_ESTABLISHED_REQUIRES_NEW_GAUGE_DEFORMATION",

            "same_action_survivor":
                False,

            "reason":
                (
                    "ALGEBRAIC_NUMERATOR_SURVIVES_BUT_NO_EXPLICIT_SYMMETRY_"
                    "COMPATIBLE_ACTION_CURRENTLY_ESTABLISHED"
                ),
        },
    ]


def v26c_gate() -> dict[str, Any]:
    """Return the conservative V26C frontier decision."""
    source = (
        massless_hook_shift_source_ward_gate()
    )

    metric = (
        quadratic_metric_hook_shift_gate()
    )

    massless = (
        percacci_sezgin_massless_same_action_gate()
    )

    atlas = (
        v26c_action_compatibility_atlas()
    )

    survivor_count = sum(
        1
        for row
        in atlas
        if row[
            "same_action_survivor"
        ]
    )

    algebraic_numerator_preserved = bool(
        metric[
            "quadratic_metric_g00_nonzero"
        ]
        and
        metric[
            "offstate_first_variation_zero"
        ]
        and
        metric[
            "active_first_variation_nonzero"
        ]
    )

    return {
        "phase":
            "032V26C",

        "claim_classification":
            (
                "SCOPED_SAME_ACTION_HOOK_GAUGE_"
                "SYMMETRY_COMPATIBILITY_NO_GO"
            ),

        "v24_intrinsic_dirac_hook_source_preserved":
            source[
                "actual_v24_source_hook_nonzero"
            ],

        "v26b1_quadratic_algebraic_numerator_preserved":
            algebraic_numerator_preserved,

        "v26b1r1_quantum_force_preflight_preserved":
            True,

        "massless_extended_fronsdal_hook_is_pure_gauge":
            massless[
                "hook_degrees_pure_gauge_in_published_sector"
            ],

        "massless_extended_fronsdal_direct_v24_source_ward_compatible":
            massless[
                "actual_v24_direct_hook_source_shift_compatible"
            ],

        "massless_extended_fronsdal_h2_metric_ward_compatible":
            massless[
                "v26b1_quadratic_metric_shift_compatible"
            ],

        "protected_massless_hook_h2_same_action_survives":
            massless[
                "current_same_action_hook_source_plus_h2_metric"
            ],

        "current_mag_same_action_survivor_count":
            survivor_count,

        "current_mag_explicit_same_action_survivor":
            bool(
                survivor_count
                >
                0
            ),

        "all_metric_affine_gravity_closed":
            False,

        "intrinsic_dirac_hypermomentum_closed":
            False,

        "marzo_nonlinear_completion_closed":
            False,

        "bms_other_vector_channels_closed":
            False,

        "massive_spin3_closed":
            False,

        "current_zero_derivative_h2_massless_protected_route_closed":
            True,

        "expensive_mag_noether_completion_authorized":
            False,

        "mag_energy_optimization_authorized":
            False,

        "action_oracle_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "mag_frontier_status":
            "PARKED_PENDING_GENUINELY_NEW_SYMMETRY_COMPATIBLE_ACTION",

        "mag_reopen_condition":
            (
                "EXPLICIT_SAME_ACTION_NONLINEAR_GAUGE_DEFORMATION_OR_"
                "COMPENSATOR_WITH_DIRAC_SOURCE_PLUS_HEALTHY_MODE_PLUS_"
                "ONE_UNIVERSAL_METRIC_PLUS_NONREMOVABLE_RESPONSE"
            ),

        "protected_ct1_dhost_kmm_explicit_action_gate_authorized":
            True,

        "next":
            (
                "032V26D_PROTECTED_CT1_DHOST_KMM_"
                "EXPLICIT_ACTION_AND_ACTIVE_NUMERATOR_GATE"
            ),
    }
