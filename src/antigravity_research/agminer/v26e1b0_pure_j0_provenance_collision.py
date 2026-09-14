"""032V26E1B0 — V26D Einstein-frame pure-j0 provenance collision gate.

PURPOSE
-------
V26E1A established an exact nonsingular field redefinition

    g_tilde_mn
        =
    A(X) g_phys_mn

with

    A(X)
        =
    1 + eta X/Lambda^4

for the normalized linear-F V26D scaffold.

The map has exact nonzero Jacobian margin:

    D_map = 1.

Therefore physical observables cannot be credited to a singular or
near-singular field redefinition.

Before building a large constrained scalar-metric cross propagator, V26E1B0
asks whether the transformed ordinary-matter interaction is actually a
previously tested low-energy operator class.

---------------------------------------------------------------------------
PHYSICAL METRIC EXPANSION
---------------------------------------------------------------------------

Ordinary matter is minimal to the physical Jordan/DHOST metric:

    g_phys.

Since

    g_tilde = A(X) g_phys,

we have

    g_phys
        =
    A(X)^(-1) g_tilde.

Write

    A(X)
        =
    1 + kappa X

where

    kappa = eta/Lambda^4.

Then near the off state:

    A^(-1)
        =
    1 - kappa X + kappa^2 X^2 + ...

and therefore

    delta g_phys_mn
        =
    -kappa X g_tilde_mn
        +
    O(X^2).

For a matter stress tensor:

    delta S_m
        =
    1/2 integral sqrt(-g) T^{mn} delta g_mn,

so the leading interaction is

    L_int
        =
    -(kappa/2) X T
        +
    O(X^2).

This is a UNIVERSAL KINETIC-CONFORMAL PURE-TRACE / j=0 operator.

There is no independent traceless j=2 matter tensor generated at O(X) by
a purely conformal metric transformation.

---------------------------------------------------------------------------
RELATION TO V17/V19
---------------------------------------------------------------------------

The V17 physical-metric class was

    g_phys
        =
    A_V17(X)^2 g_E

with

    A_V17
        =
    1 - C1 X + ...

so

    g_phys
        =
    (1 - 2 C1 X + ...) g_E.

After translating kinetic-sign conventions, equality of the physical metric
coefficient gives the magnitude relation

    |kappa|
        =
    2 |C1|.

Equivalently:

    |C1_equivalent|
        =
    |kappa|/2.

The exact sign translation depends on the branch's X/signature convention.
V26E1B0 therefore does NOT falsely identify the sign conventions.

The crucial off-state quantum observation is sign independent at leading
two-scalar order:

    V_2phi
        proportional to
    - C1^2 m1 m2 / r^7.

Therefore changing only the sign convention of C1 cannot remove the existence
of the two-scalar force.

---------------------------------------------------------------------------
HIDDEN SOURCE PROVENANCE
---------------------------------------------------------------------------

V26D declares

    (1/fPsi)
    nabla_mu(phi)
    bar(Psi) gamma^mu gamma5 Psi.

This is the same DERIVATIVE AXIAL-CURRENT SOURCE OPERATOR CLASS used by the
historical V14-V19 kinetic-conformal branch.

This statement concerns operator/source provenance.

It does NOT assert that V26D has already chosen the identical microscopic
source state, density, geometry, fPsi, scalar normalization, or support
architecture used by V17.

---------------------------------------------------------------------------
WHAT V19R5/R6 ACTUALLY CLOSED
---------------------------------------------------------------------------

Durable V19 failure memory:

    pure-j0 universal kinetic-conformal matter coupling
        ->
    nonzero off-state two-scalar/material force.

For the SPECIFIC tested V17 hidden-axial finite-payload implementation:

    empirical metric scale minimum
        ~123.456884 keV

while strict sub-10-MJ partial source energy required

    metric scale
        <~122.996182 keV.

Hence:

    empirical/strict-energy overlap
        =
    EMPTY.

At the empirical boundary the exact V17 partial source was approximately

    10.150225 MJ,

already above the strict target before omitted complete-device costs.

The tested positivity-compatible dimension-eight j=2 companion did not
cancel this material-force obstruction.

---------------------------------------------------------------------------
SCOPED TRANSFER RULE
---------------------------------------------------------------------------

The correct inference is NOT:

    ALL V26D COMPLETIONS ARE CLOSED.

The correct inference is:

1. V26D's exact Einstein-frame physical matter metric has the SAME LEADING
   PURE-j0 KINETIC-CONFORMAL OPERATOR CLASS.

2. Therefore a minimal canonical, unscreened scalar completion inherits the
   R5-type off-state two-scalar/material-force problem.

3. If one additionally chooses the same V17-equivalent hidden axial source
   normalization/architecture, the completed V19R6 empirical-energy
   non-overlap is provenance-duplicate failure memory and must not be
   recomputed as though it were new physics.

4. The exact V19R6 ENERGY boundary is NOT automatically transferred to an
   arbitrary new V26D P(X), Q(X), source state, source efficiency, or
   genuinely different protected scalar sector.

5. To remain scientifically new, a V26D continuation must introduce a
   mechanism that changes the physical low-energy problem, e.g.:

       active-state-only/descreened matter coupling;
       symmetry-protected suppression of off-state quantum descendants;
       genuinely non-j0 operator content;
       different healthy scalar dynamics changing source efficiency;
       another mechanism that demonstrably evades the R5 material force.

Simply recomputing the same canonical pure-j0 cross propagator in another
frame is NOT a new candidate.

---------------------------------------------------------------------------
CANONICAL NORMALIZATION
---------------------------------------------------------------------------

For

    L
      =
    -(Z/2)(d phi)^2
      +
    C1 (d phi)^2 T
      +
    (1/f) d phi J5,

with

    phi_c = sqrt(Z) phi,

one gets

    C1_c = C1/Z

and

    f_c = f sqrt(Z).

Therefore

    C1_c f_c^2
        =
    C1 f^2.

A simple wavefunction rescaling alone cannot erase the useful
metric/source invariant or evade the old failure memory.

---------------------------------------------------------------------------
PERFORMANCE POLICY
---------------------------------------------------------------------------

Any survivor must eventually achieve at least

    a_out >= 9.80665 m/s^2

at

    true external stand-off >= 1.0 m.

Exceeding either floor is favorable.

No energy optimization is performed in V26E1B0.

The HOOK17 17.0676-J capacity reference does not transfer to V26D.

CLAIM_CLASSIFICATION
--------------------
FRAME_PROVENANCE_COLLISION_AND_SCOPED_FAILURE_MEMORY_INHERITANCE
"""

from __future__ import annotations

import math
from typing import Any

from .protected_ct1_dhost_kmm_action import (
    action_specification,
)

from .two_scalar_quantum_force import (
    trace_pair_force_coefficient,
)

from .v26e1a_exact_einstein_frame_map import (
    v26e1a_summary,
)


TOL = 1.0e-12

STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

MIN_OUTWARD_ACCELERATION_M_S2 = 9.80665
MIN_TRUE_STANDOFF_M = 1.0

V19R6_EMPIRICAL_METRIC_MIN_EV = 123456.884
V19R6_ENERGY_METRIC_MAX_EV = 122996.182
V19R6_EMPIRICAL_BOUNDARY_PARTIAL_J = 10.150225e6


def v26e1a_provenance_gate() -> dict[str, Any]:
    """Require the completed nonsingular E1A frame map."""

    result = v26e1a_summary()

    passed = bool(
        result[
            "v26e1a_partial_green"
        ]
        and
        result[
            "quadratic_dhost_gravity_sector_eh_equivalent"
        ]
        and
        result[
            "representative_map_invertible"
        ]
        and
        result[
            "linear_F_map_D_identically_one"
        ]
        and
        not result[
            "field_redefinition_near_singular"
        ]
        and
        result[
            "frame_invariant_cross_response_audit_required"
        ]
    )

    return {
        "v26e1a_provenance_pass":
            passed,

        "eh_equivalent":
            result[
                "quadratic_dhost_gravity_sector_eh_equivalent"
            ],

        "map_invertible":
            result[
                "representative_map_invertible"
            ],

        "map_jacobian_margin":
            result[
                "representative_D_map"
            ],

        "near_singular":
            result[
                "field_redefinition_near_singular"
            ],

        "physical_g00_still_open":
            not result[
                "physical_g00_cross_response_established"
            ],
    }


def inverse_conformal_series_gate(
    *,
    kappa: float = 0.5,
) -> dict[str, Any]:
    """Reconstruct A^-1 and the leading physical-metric coefficient."""

    value = float(
        kappa
    )

    # A = 1 + kappa X.
    #
    # A^-1 = 1 - kappa X + kappa^2 X^2 + ...
    first_order = -value
    second_order = value**2

    return {
        "A":
            "1+kappa*X",

        "physical_metric_factor":
            "A^-1",

        "linear_metric_coefficient":
            first_order,

        "quadratic_metric_coefficient":
            second_order,

        "leading_metric_deformation_pure_conformal":
            True,

        "leading_metric_deformation_contains_j2":
            False,

        "leading_matter_operator":
            "-(kappa/2)*X*T",

        "leading_matter_operator_pure_trace_j0":
            True,
    }


def v17_coefficient_match_gate(
    *,
    kappa: float = 0.5,
) -> dict[str, Any]:
    """Map V26D physical-metric coefficient magnitude to V17 convention."""

    value = float(
        kappa
    )

    c1_magnitude = (
        abs(
            value
        )
        /
        2.0
    )

    reconstructed_metric_magnitude = (
        2.0
        *
        c1_magnitude
    )

    return {
        "v26d_kappa":
            value,

        "v17_equivalent_abs_c1":
            c1_magnitude,

        "two_abs_c1":
            reconstructed_metric_magnitude,

        "abs_kappa":
            abs(
                value
            ),

        "metric_coefficient_magnitude_match":
            bool(
                abs(
                    reconstructed_metric_magnitude
                    -
                    abs(
                        value
                    )
                )
                <=
                TOL
            ),

        "x_sign_convention_identical_without_translation":
            False,

        "sign_translation_required":
            True,

        "offstate_force_depends_on_c1_squared":
            True,
    }


def pure_j0_operator_gate() -> dict[str, Any]:
    """Classify the Einstein-frame ordinary-matter operator."""

    series = inverse_conformal_series_gate()

    return {
        "ordinary_matter_universal":
            True,

        "metric_deformation_is_conformal":
            series[
                "leading_metric_deformation_pure_conformal"
            ],

        "leading_operator":
            series[
                "leading_matter_operator"
            ],

        "leading_operator_j0":
            series[
                "leading_matter_operator_pure_trace_j0"
            ],

        "independent_j2_generated_at_same_order":
            series[
                "leading_metric_deformation_contains_j2"
            ],

        "v17_v19_low_energy_operator_class_collision":
            bool(
                series[
                    "leading_matter_operator_pure_trace_j0"
                ]
                and
                not series[
                    "leading_metric_deformation_contains_j2"
                ]
            ),
    }


def source_operator_provenance_gate() -> dict[str, Any]:
    """Compare V26D hidden-source operator class with V14-V19."""

    action = action_specification()

    coupling = str(
        action[
            "hidden_source_coupling"
        ]
    )

    axial = bool(
        "gamma5"
        in coupling
        and
        "nabla_mu(phi)"
        in coupling
    )

    return {
        "v26d_hidden_source_sector":
            action[
                "hidden_source_sector"
            ],

        "v26d_hidden_source_coupling":
            coupling,

        "v26d_derivative_axial_current_operator":
            axial,

        "v17_v19_hidden_source_operator_class":
            "DERIVATIVE_AXIAL_CURRENT",

        "same_hidden_source_operator_class":
            axial,

        "same_microscopic_source_state_established":
            False,

        "same_source_geometry_established":
            False,

        "same_fpsi_established":
            False,

        "same_source_energy_functional_established":
            False,
    }


def offstate_two_scalar_force_gate() -> dict[str, Any]:
    """Preserve the R5 pure-j0 off-state quantum descendant."""

    coefficient = float(
        trace_pair_force_coefficient()
    )

    expected = (
        15.0
        /
        (
            8.0
            *
            math.pi**3
        )
    )

    return {
        "trace_pair_force_coefficient":
            coefficient,

        "expected_trace_pair_force_coefficient":
            expected,

        "coefficient_reconstruction_error":
            abs(
                coefficient
                -
                expected
            ),

        "coefficient_reconstructed":
            bool(
                abs(
                    coefficient
                    -
                    expected
                )
                <=
                TOL
            ),

        "potential_form":
            "-K*C1^2*m1*m2/r^7",

        "force_exists_at_classical_offstate":
            True,

        "force_requires_classical_background_X":
            False,

        "force_is_even_under_c1_sign_flip":
            True,

        "canonical_unscreened_pure_j0_has_r5_type_quantum_descendant":
            True,
    }


def canonical_rescaling_gate(
    *,
    c1: float = 2.0,
    f: float = 3.0,
    z: float = 5.0,
) -> dict[str, Any]:
    """Reconstruct the durable C1*f^2 normalization invariant."""

    c1_value = float(
        c1
    )

    f_value = float(
        f
    )

    z_value = float(
        z
    )

    if z_value <= 0.0:
        raise ValueError(
            "Z must be positive"
        )

    c1_canonical = (
        c1_value
        /
        z_value
    )

    f_canonical = (
        f_value
        *
        math.sqrt(
            z_value
        )
    )

    before = (
        c1_value
        *
        f_value**2
    )

    after = (
        c1_canonical
        *
        f_canonical**2
    )

    return {
        "C1":
            c1_value,

        "f":
            f_value,

        "Z":
            z_value,

        "C1_canonical":
            c1_canonical,

        "f_canonical":
            f_canonical,

        "invariant_before":
            before,

        "invariant_after":
            after,

        "relative_error":
            abs(
                before
                -
                after
            )
            /
            max(
                abs(
                    before
                ),
                1.0e-300,
            ),

        "c1_f2_invariant":
            bool(
                abs(
                    before
                    -
                    after
                )
                <=
                TOL
                *
                max(
                    abs(
                        before
                    ),
                    1.0,
                )
            ),

        "wavefunction_rescaling_alone_evades_failure_memory":
            False,
    }


def inherited_v19r6_failure_memory() -> dict[str, Any]:
    """Return durable scoped V19R6 closeout numbers."""

    gap = (
        V19R6_EMPIRICAL_METRIC_MIN_EV
        -
        V19R6_ENERGY_METRIC_MAX_EV
    )

    gap_fraction = (
        gap
        /
        V19R6_ENERGY_METRIC_MAX_EV
    )

    return {
        "empirical_metric_min_ev":
            V19R6_EMPIRICAL_METRIC_MIN_EV,

        "strict_energy_metric_max_ev":
            V19R6_ENERGY_METRIC_MAX_EV,

        "metric_gap_ev":
            gap,

        "metric_gap_fraction":
            gap_fraction,

        "empirical_boundary_partial_j":
            V19R6_EMPIRICAL_BOUNDARY_PARTIAL_J,

        "strict_energy_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "empirical_energy_overlap_exists":
            False,

        "tested_v17_hidden_axial_pure_j0_implementation_closed":
            True,

        "all_kinetic_conformal_theories_closed":
            False,

        "exact_r6_energy_boundary_transfers_to_arbitrary_v26d_source":
            False,
    }


def identical_v17_completion_gate() -> dict[str, Any]:
    """Classify the exact provenance-duplicate completion."""

    operator = pure_j0_operator_gate()
    source = source_operator_provenance_gate()
    force = offstate_two_scalar_force_gate()
    memory = inherited_v19r6_failure_memory()

    identical_completion_closed = bool(
        operator[
            "v17_v19_low_energy_operator_class_collision"
        ]
        and
        source[
            "same_hidden_source_operator_class"
        ]
        and
        force[
            "canonical_unscreened_pure_j0_has_r5_type_quantum_descendant"
        ]
        and
        memory[
            "tested_v17_hidden_axial_pure_j0_implementation_closed"
        ]
    )

    return {
        "leading_matter_operator_class_matches_v17_v19":
            operator[
                "v17_v19_low_energy_operator_class_collision"
            ],

        "hidden_source_operator_class_matches_v17_v19":
            source[
                "same_hidden_source_operator_class"
            ],

        "r5_quantum_descendant_present_for_canonical_unscreened_completion":
            force[
                "canonical_unscreened_pure_j0_has_r5_type_quantum_descendant"
            ],

        "v17_identical_source_state_and_scalar_completion_assumption":
            "REQUIRED_FOR_EXACT_R6_ENERGY_TRANSFER",

        "exact_v17_equivalent_completion_closed":
            identical_completion_closed,

        "arbitrary_v26d_source_closed":
            False,

        "arbitrary_v26d_lower_derivative_scalar_sector_closed":
            False,
    }


def novelty_requirements_gate() -> dict[str, Any]:
    """Specify what a continued V26D completion must genuinely change."""

    return {
        "plain_canonical_pure_j0_recomputation_counts_as_new_physics":
            False,

        "acceptable_novelty_routes":
            [
                "ACTIVE_STATE_ONLY_OR_DESCREENED_MATTER_RESPONSE",
                "SYMMETRY_PROTECTED_OFFSTATE_QUANTUM_SUPPRESSION",
                "GENUINELY_NON_J0_OPERATOR_CONTENT",
                "HEALTHY_NONCANONICAL_SCALAR_DYNAMICS_WITH_NEW_EMPIRICAL_AUDIT",
                "DIFFERENT_MICROSCOPIC_SOURCE_EFFICIENCY_WITH_NEW_ENERGY_LEDGER",
            ],

        "new_route_must_recheck_r5_material_force":
            True,

        "new_route_must_recheck_source_joule":
            True,

        "new_route_must_recheck_canonical_health":
            True,

        "new_route_must_recheck_field_redefinition_invariance":
            True,

        "new_route_must_preserve_one_universal_physical_metric":
            True,

        "new_route_must_hit_at_least_1g_at_1m":
            True,
    }


def v26e1b0_summary() -> dict[str, Any]:
    """Return conservative provenance-collision classification."""

    provenance = v26e1a_provenance_gate()
    operator = pure_j0_operator_gate()
    coefficient = v17_coefficient_match_gate()
    source = source_operator_provenance_gate()
    force = offstate_two_scalar_force_gate()
    canonical = canonical_rescaling_gate()
    memory = inherited_v19r6_failure_memory()
    identical = identical_v17_completion_gate()
    novelty = novelty_requirements_gate()

    collision = bool(
        provenance[
            "v26e1a_provenance_pass"
        ]
        and
        operator[
            "v17_v19_low_energy_operator_class_collision"
        ]
        and
        coefficient[
            "metric_coefficient_magnitude_match"
        ]
        and
        source[
            "same_hidden_source_operator_class"
        ]
        and
        force[
            "coefficient_reconstructed"
        ]
        and
        canonical[
            "c1_f2_invariant"
        ]
    )

    return {
        "branch":
            "032V26E1B0",

        "subgate":
            "FRAME_PROVENANCE_PURE_J0_COLLISION_AND_FAILURE_MEMORY",

        "decision":
            (
                "RED_SCOPED_V26E1B0_V26D_EINSTEIN_FRAME_"
                "LEADING_MATTER_OPERATOR_IS_PURE_J0_PROVENANCE_"
                "COLLISION_WITH_V17_V19__IDENTICAL_CANONICAL_"
                "COMPLETION_NOT_REOPENED__GENUINELY_NEW_PROTECTED_"
                "COMPLETIONS_REMAIN_OPEN"
            )
            if collision
            else
            "CHECK_V26E1B0_FRAME_OPERATOR_MAPPING",

        "v26e1a_provenance_pass":
            provenance[
                "v26e1a_provenance_pass"
            ],

        "leading_einstein_frame_matter_operator_pure_j0":
            operator[
                "leading_operator_j0"
            ],

        "leading_independent_j2_generated":
            operator[
                "independent_j2_generated_at_same_order"
            ],

        "v17_v19_operator_class_collision":
            operator[
                "v17_v19_low_energy_operator_class_collision"
            ],

        "v17_equivalent_abs_c1_over_abs_kappa":
            0.5,

        "sign_convention_translation_required":
            coefficient[
                "sign_translation_required"
            ],

        "offstate_force_sign_flip_escape":
            False,

        "same_hidden_axial_source_operator_class":
            source[
                "same_hidden_source_operator_class"
            ],

        "same_hidden_axial_source_state_established":
            source[
                "same_microscopic_source_state_established"
            ],

        "r5_type_two_scalar_force_present_for_canonical_unscreened_completion":
            force[
                "canonical_unscreened_pure_j0_has_r5_type_quantum_descendant"
            ],

        "c1_f2_canonical_rescaling_invariant":
            canonical[
                "c1_f2_invariant"
            ],

        "v19r6_identical_implementation_empirical_energy_overlap_exists":
            memory[
                "empirical_energy_overlap_exists"
            ],

        "v19r6_empirical_metric_min_ev":
            memory[
                "empirical_metric_min_ev"
            ],

        "v19r6_strict_energy_metric_max_ev":
            memory[
                "strict_energy_metric_max_ev"
            ],

        "v19r6_empirical_boundary_partial_j":
            memory[
                "empirical_boundary_partial_j"
            ],

        "exact_v19r6_energy_boundary_transfers_to_arbitrary_v26d_source":
            memory[
                "exact_r6_energy_boundary_transfers_to_arbitrary_v26d_source"
            ],

        "exact_v17_equivalent_completion_closed":
            identical[
                "exact_v17_equivalent_completion_closed"
            ],

        "all_v26d_completions_globally_closed":
            False,

        "plain_canonical_e1b_crossprop_recomputation_as_new_candidate_authorized":
            False,

        "genuinely_new_v26d_completion_rerank_authorized":
            collision,

        "acceptable_novelty_routes":
            novelty[
                "acceptable_novelty_routes"
            ],

        "full_static_spacelike_scalar_health_established":
            False,

        "physical_g00_cross_response_established":
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

        "energy_optimization_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "next":
            (
                "032V26E1B1_PROTECTED_ACTIVE_STATE_SCALAR_"
                "COMPLETION_RERANK_GATE"
            ),

        "claim_scope":
            (
                "LEADING EINSTEIN-FRAME MATTER OPERATOR AND SOURCE-"
                "OPERATOR PROVENANCE; EXACT V19R6 ENERGY CLOSEOUT "
                "TRANSFERRED ONLY TO THE IDENTICAL V17-EQUIVALENT "
                "COMPLETION, NOT TO ARBITRARY NEW V26D COMPLETIONS"
            ),
    }
