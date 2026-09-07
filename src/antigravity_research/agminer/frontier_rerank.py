"""032V20 AGMINER candidate-family rerank and failure-memory helpers.

PURPOSE
-------
032V19R6 closed the CURRENT hidden-axial pure-j0 kinetic-conformal
implementation.

It did NOT close AGMINER.

It did NOT close every possible kinetic-conformal theory.

V20 returns AGMINER from candidate-specific falsification to a
family-selection mode.

The goals are:

1. preserve R3-R6 failure anatomy in persistent AGMINER region rules;
2. prevent the closed current implementation from being rediscovered;
3. prevent pure-j0 Goldstone/Z2 variants from being promoted without
   genuinely new low-energy operator content;
4. preserve broader theory classes that were not actually closed;
5. rank the next research recipes transparently;
6. avoid inventing MechanismMetrics or action oracles for prefield ideas.

RANKING PHILOSOPHY
------------------
This module deliberately does NOT assign one opaque numerical score.

Families are grouped into explicit research tiers.

TIER A
    a literature-grounded theory class exists and a cheap theorem/sign/
    source/energy preflight can be written now.

TIER B
    structurally interesting, but requires genuinely new action-level
    physics before a parameter scan is justified.

TIER C
    not mathematically closed, but inherited empirical/source/scaffold
    burdens make it lower priority.

CLOSED
    do not spend additional search compute unless the stated assumptions
    are genuinely changed.

Within each tier, integer priority is only an ordering of the next
falsification experiments.

This is a research scheduler, not evidence that the highest-ranked family
will work.

FAILURE-MEMORY SCOPE
--------------------
A policy-independent physical failure must remain separate from a
policy-dependent strict-10-MJ failure.

Examples:

R5:
    the current pure-j0 coefficient fails the low-energy Casimir
    empirical gate.
    This is policy independent.

R6:
    the CURRENT hidden-axial implementation has no overlap between
    empirical coefficient viability and E_partial < 10 MJ.
    This is policy specific to the present energy objective and source.

The same theory family under genuinely new low-energy physics is not silently
closed by either statement.

NO NEGATIVE MASS
----------------
None of the active recipes below assumes negative inertial or gravitational
mass.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .storage import Storage


TIER_ORDER = {
    "A": 0,
    "B": 1,
    "C": 2,
    "CLOSED": 3,
}


@dataclass(frozen=True)
class FamilyRecipe:
    family_id: str
    tier: str
    priority: int
    status: str

    action_readiness: str
    universal_metric_response: str
    stand_off_status: str
    protection_status: str

    source_burden: str
    support_control_burden: str
    mechanism_prior_alignment: str

    inherited_blockers: str
    next_gate: str
    provenance: str
    reason: str

    negative_mass_required: bool = False

    def __post_init__(self) -> None:
        if self.tier not in TIER_ORDER:
            raise ValueError(
                "unknown research tier"
            )

        if self.priority < 1:
            raise ValueError(
                "priority must be positive"
            )

        if not self.family_id:
            raise ValueError(
                "family_id is required"
            )

    @property
    def closed(self) -> bool:
        return (
            self.tier
            ==
            "CLOSED"
        )

    def rank_key(
        self,
    ) -> tuple[int, int, str]:
        return (
            TIER_ORDER[
                self.tier
            ],
            self.priority,
            self.family_id,
        )

    def as_row(
        self,
    ) -> dict[str, Any]:
        row = asdict(
            self
        )

        row[
            "closed"
        ] = self.closed

        return row


def family_recipes() -> list[FamilyRecipe]:
    """Return the post-R6 transparent candidate-family frontier."""

    rows = [
        # ============================================================
        # TIER A — DIRECT NEXT PREFLIGHTS
        # ============================================================

        FamilyRecipe(
            family_id=
                "SHIFT_SYMMETRIC_TIME_GRADIENT_DISFORMAL_METRIC",

            tier=
                "A",

            priority=
                1,

            status=
                "PREFIELD_OPEN_HIGHEST_PRIORITY",

            action_readiness=
                "LITERATURE_THEORY_CLASS",

            universal_metric_response=
                "DIRECT_KINETIC_DEPENDENT_CONFORMAL_DISFORMAL_METRIC",

            stand_off_status=
                "STRUCTURALLY_POSSIBLE_SIGN_UNRESOLVED",

            protection_status=
                "EXACT_SHIFT_SYMMETRY_AVAILABLE",

            source_burden=
                "TIME_GRADIENT_RESERVOIR_PLUS_LOCAL_PROFILE",

            support_control_burden=
                "RESERVOIR_ACTIVATION_AND_CONTROL_OPEN",

            mechanism_prior_alignment=
                "HIGH_IF_BACKGROUND_RESOURCE_CAN_BE_SHARED_AND_LOW_TAX",

            inherited_blockers=
                (
                    "MUST_NOT_REDUCE_TO_R5_PURE_J0_STATIC_OPERATOR;"
                    "OFFSTATE_QUANTUM_FORCE_OPEN;"
                    "ABSOLUTE_BACKGROUND_ENERGY_OPEN"
                ),

            next_gate=
                (
                    "032V21_TIME_GRADIENT_DISFORMAL_SIGN_"
                    "RESERVOIR_ENERGY_AND_OFFSTATE_QUANTUM_PREFLIGHT"
                ),

            provenance=
                (
                    "V12_OPEN_SECONDARY_DYNAMIC_BACKGROUND;"
                    "IKEDA_IYONAGA_KOBAYASHI_PRD104_104009_2021"
                ),

            reason=
                (
                    "TIME_LINEAR_SHIFT_BACKGROUND_IS_A_REAL_THEORY_BRANCH;"
                    "DIRECT_PHYSICAL_METRIC_RESPONSE;"
                    "STRUCTURALLY_DISTINCT_FROM_CLOSED_STATIC_PURE_J0_SOURCE"
                ),
        ),

        FamilyRecipe(
            family_id=
                "PROPAGATING_NONMETRICITY_HEALTHY_SINGLE_MODE",

            tier=
                "A",

            priority=
                2,

            status=
                "PREFIELD_OPEN_NEW_EXTENSION",

            action_readiness=
                "LITERATURE_HEALTHY_FREE_PROPAGATOR_CLASS",

            universal_metric_response=
                "MATTER_PORTAL_UNRESOLVED",

            stand_off_status=
                "UNRESOLVED",

            protection_status=
                "HEALTHY_SINGLE_MODE_PARAMETER_CONDITIONS_EXIST",

            source_burden=
                "ORDINARY_MATTER_OR_HYPERMOMENTUM_SOURCE_UNRESOLVED",

            support_control_burden=
                "UNRESOLVED",

            mechanism_prior_alignment=
                "MEDIUM_HIGH_IF_DIRECT_UNIVERSAL_METRIC_MODE_EXISTS",

            inherited_blockers=
                (
                    "MINIMAL_MAG_Q_T_U_BRANCHES_REMAIN_CLOSED;"
                    "MUST_DEMONSTRATE_GENUINELY_PROPAGATING_EXTENSION;"
                    "NO_USEFUL_MATTER_PORTAL_YET"
                ),

            next_gate=
                (
                    "032V21B_PROPAGATING_NONMETRICITY_"
                    "MATTER_PORTAL_SIGN_AND_SOURCE_EXISTENCE_PREFLIGHT"
                ),

            provenance=
                (
                    "MIKURA_PERCACCI_EPJC85_377_2025;"
                    "DIMENSION_LE_4_SYMMETRIC_MAG_PROPAGATING_MODE"
                ),

            reason=
                (
                    "NEW_PROPAGATING_NONMETRICITY_KINETIC_TERMS_ARE_DISTINCT_"
                    "FROM_PREVIOUS_MINIMAL_ALGEBRAIC_MAG_CLOSEOUTS"
                ),
        ),

        # ============================================================
        # TIER B — REQUIRES GENUINELY NEW ACTION-LEVEL PHYSICS
        # ============================================================

        FamilyRecipe(
            family_id=
                "SHIFT_PROTECTED_GOLDSTONE_KINETIC_METRIC_WITH_R5_EVASION",

            tier=
                "B",

            priority=
                1,

            status=
                "OPEN_ONLY_WITH_NONPURE_J0_LOW_ENERGY_CONTENT",

            action_readiness=
                "MICROSCOPIC_PROVENANCE_EXISTS_BUT_REQUIRED_EVASION_NOT_BUILT",

            universal_metric_response=
                "KINETIC_METRIC",

            stand_off_status=
                "POSSIBLE_ONLY_AFTER_NEW_OPERATOR_SIGN_GATE",

            protection_status=
                "SHIFT_GOLDSTONE_PROTECTION_AVAILABLE",

            source_burden=
                "NEW_SOURCE_MATCHING_REQUIRED",

            support_control_burden=
                "OPEN",

            mechanism_prior_alignment=
                "HIGH_IF_R5_FORCE_CAN_BE_REMOVED_WITHOUT_STATIC_RESPONSE_LOSS",

            inherited_blockers=
                (
                    "PURE_J0_LIMIT_BLOCKED_BY_R5_R6;"
                    "ADDITIONAL_LOW_ENERGY_OPERATOR_CONTENT_REQUIRED"
                ),

            next_gate=
                (
                    "DERIVE_EXPLICIT_NONPURE_J0_ACTION_BEFORE_ANY_SCAN"
                ),

            provenance=
                "R4_GOLDSTONE_SURVIVOR_RECLASSIFIED_BY_R5_R6",

            reason=
                (
                    "GOLDSTONE_LABEL_ALONE_DOES_NOT_EVADE_R5;"
                    "ONLY_A_PHYSICAL_LOW_ENERGY_AMPLITUDE_CHANGE_COUNTS"
                ),
        ),

        FamilyRecipe(
            family_id=
                "ACTIVE_STATE_DEPENDENT_KINETIC_METRIC_DESCREENING",

            tier=
                "B",

            priority=
                2,

            status=
                "YELLOW_NEW_PHYSICS",

            action_readiness=
                "CONCEPT_REQUIRES_EXPLICIT_ACTION",

            universal_metric_response=
                "TARGET_DIRECT_METRIC_RESPONSE",

            stand_off_status=
                "STRUCTURALLY_POSSIBLE",

            protection_status=
                "MODEL_DEPENDENT",

            source_burden=
                "ENGINEERED_ACTIVE_STATE_REQUIRED",

            support_control_burden=
                "ACTIVATION_RESET_OFFSTATE_LEDGER_REQUIRED",

            mechanism_prior_alignment=
                "HIGH_IF_OFFSTATE_AND_ACTIVE_STATE_COUPLINGS_SEPARATE_PHYSICALLY",

            inherited_blockers=
                (
                    "DENSITY_ONLY_SAME_VERTEX_SCREENING_CLOSED_R4;"
                    "MUST_DESCREEN_FROM_ENGINEERED_STATE_NOT_PARAMETER_TUNING"
                ),

            next_gate=
                (
                    "EXPLICIT_ACTION_OR_THEOREM_BEFORE_PARAMETERIZATION"
                ),

            provenance=
                "R4_ACTIVE_X_DESCREENING_OPEN",

            reason=
                (
                    "ONLY_SCREENING_IDEA_THAT_CAN_IN_PRINCIPLE_SEPARATE_"
                    "OFFSTATE_EMPIRICAL_FORCE_FROM_ACTIVE_METRIC_RESPONSE"
                ),
        ),

        FamilyRecipe(
            family_id=
                "PROTECTED_FIELD_VALUE_CONFORMAL_SCALAR_METRIC",

            tier=
                "B",

            priority=
                3,

            status=
                "OPEN_ONLY_WITH_GENUINELY_NEW_PROTECTION",

            action_readiness=
                "CLASS_KNOWN_NEW_PROTECTION_ABSENT",

            universal_metric_response=
                "DIRECT_UNIVERSAL_CONFORMAL",

            stand_off_status=
                "CLASSICALLY_POSSIBLE",

            protection_status=
                "MUST_BE_NEW_RELATIVE_TO_031F0",

            source_burden=
                "MICROSCOPIC_SOURCE_KNOWN_IN_031_BUT_NOT_REUSABLE_AS_IS",

            support_control_burden=
                "OPEN",

            mechanism_prior_alignment=
                "MEDIUM",

            inherited_blockers=
                (
                    "031F0_UNPROTECTED_ULTRALIGHT_IMPLEMENTATION_CLOSED;"
                    "OFFSTATE_EMPIRICAL_GATE_REQUIRED_FIRST"
                ),

            next_gate=
                (
                    "PROTECTION_AND_EMPIRICAL_PREFLIGHT_BEFORE_SOURCE_ENERGY"
                ),

            provenance=
                "031_HISTORICAL_CLASSICAL_REALIZATION_031F0_CLOSEOUT",

            reason=
                (
                    "CLASSICALLY_POWERFUL_BUT_REOPENING_REQUIRES_"
                    "A_NEW_RADIATIVE_PROTECTION_MECHANISM"
                ),
        ),

        FamilyRecipe(
            family_id=
                "MATTER_TRIGGERED_PFORM_BROADER_DOMAIN",

            tier=
                "B",

            priority=
                4,

            status=
                "BROADER_CLASS_OPEN_TESTED_032R_DOMAIN_CLOSED",

            action_readiness=
                "LITERATURE_SPONTANEOUS_GROWTH_CLASS",

            universal_metric_response=
                "MODEL_DEPENDENT",

            stand_off_status=
                "UNRESOLVED",

            protection_status=
                "GAUGE_OR_FORM_SYMMETRY_MODEL_DEPENDENT",

            source_burden=
                "TRIGGER_AND_LOCALIZATION_OPEN",

            support_control_burden=
                "TRIGGER_ENERGY_AND_RESET_OPEN",

            mechanism_prior_alignment=
                "MEDIUM_LOW",

            inherited_blockers=
                (
                    "032R_DECLARED_10MJ_TRIGGER_DOMAIN_REMAINS_CLOSED;"
                    "DO_NOT_RESCAN_SAME_DOMAIN"
                ),

            next_gate=
                (
                    "NEW_TRIGGER_SCALING_THEOREM_REQUIRED_BEFORE_REOPENING"
                ),

            provenance=
                "RAMAZANOGLU_PFORM_SPONTANEOUS_GROWTH_CLASS",

            reason=
                (
                    "BROADER_PFORM_PHYSICS_EXISTS_BUT_EXISTING_PROJECT_"
                    "TRIGGER_DOMAIN_ALREADY_FAILED"
                ),
        ),

        # ============================================================
        # TIER C — OPEN BUT LOW PRIORITY
        # ============================================================

        FamilyRecipe(
            family_id=
                "BROAD_SPECTRAL_LINEAR_SCALAR_TOWER",

            tier=
                "C",

            priority=
                1,

            status=
                "MATHEMATICALLY_NOT_CLOSED_LOW_PRIORITY",

            action_readiness=
                "EXPLICIT_ACTION_CLASS",

            universal_metric_response=
                "DIRECT_TRACE_PORTAL",

            stand_off_status=
                "STRUCTURALLY_POSSIBLE",

            protection_status=
                "MODEL_DEPENDENT",

            source_burden=
                "MULTI_MEDIATOR",

            support_control_burden=
                "HIGH",

            mechanism_prior_alignment=
                "LOW_DUE_SCAFFOLD_AND_COMPANION_TAX",

            inherited_blockers=
                (
                    "R3_SINGLE_SCALAR_CLOSED;"
                    "R4_NARROW_BAND_TOWER_CLOSED;"
                    "FULL_MULTI_YUKAWA_LIKELIHOOD_NOT_RECONSTRUCTED"
                ),

            next_gate=
                (
                    "ONLY_REVISIT_IF_NEW_SPECTRAL_SUM_RULE_BEATS_R4_CAUCHY_BURDEN"
                ),

            provenance=
                "R4_BROAD_SPECTRAL_TOWER_YELLOW",

            reason=
                (
                    "NOT_FORMALLY_CLOSED_BUT_INHERITS_SEVERE_EMPIRICAL_"
                    "AND_COMPANION_OPERATOR_PRESSURE"
                ),
        ),

        FamilyRecipe(
            family_id=
                "DERIVATIVE_HYPERMOMENTUM_MULTIPOLE_PORTAL",

            tier=
                "C",

            priority=
                2,

            status=
                "BROADER_MAG_QUESTION_OPEN",

            action_readiness=
                "NO_DEVICE_ACTION_SELECTED",

            universal_metric_response=
                "UNRESOLVED",

            stand_off_status=
                "UNRESOLVED",

            protection_status=
                "GEOMETRIC_SYMMETRY_MODEL_DEPENDENT",

            source_burden=
                "NONSTANDARD_HYPERMOMENTUM_SOURCE_REQUIRED",

            support_control_burden=
                "HIGH_UNRESOLVED",

            mechanism_prior_alignment=
                "MEDIUM_IF_MULTIPOLE_KERNEL_LEVERAGE_EXISTS",

            inherited_blockers=
                (
                    "MINIMAL_TORSION_AND_MAG_BRANCHES_CLOSED;"
                    "MUST_NOT_REOPEN_Q_T_U_WITHOUT_PROPAGATING_NEW_SECTOR"
                ),

            next_gate=
                (
                    "SOURCE_EXISTENCE_AND_ORDINARY_MATTER_METRIC_RESPONSE_THEOREM"
                ),

            provenance=
                "032S_T_U_BROADER_DERIVATIVE_MULTIPOLE_REMAINDER",

            reason=
                (
                    "ONLY_BROADER_DERIVATIVE_MULTIPOLE_EXTENSION_REMAINS;"
                    "MINIMAL_CONNECTION_SOURCE_MECHANISMS_ALREADY_FAILED"
                ),
        ),

        FamilyRecipe(
            family_id=
                "SECONDARY_TOPOLOGICAL_SHARED_SCAFFOLD",

            tier=
                "C",

            priority=
                3,

            status=
                "DEMOTED",

            action_readiness=
                "SOURCE_ACTION_ORACLES_EXIST_METRIC_PORTAL_ABSENT",

            universal_metric_response=
                "SEPARATE_PORTAL_REQUIRED",

            stand_off_status=
                "SOURCE_ONLY_NOT_ESTABLISHED",

            protection_status=
                "TOPOLOGICAL",

            source_burden=
                "SHARED_SCAFFOLD_CAN_SCALE_FAVORABLY",

            support_control_burden=
                "METRIC_PORTAL_DOMINATES",

            mechanism_prior_alignment=
                "SOURCE_SIDE_INTERESTING_PORTAL_SIDE_BAD",

            inherited_blockers=
                (
                    "V9_V10_NO_FINITE_PAYLOAD_METRIC_ACTIVE_PROMOTION"
                ),

            next_gate=
                (
                    "NO_REOPEN_WITHOUT_DIRECT_LOCAL_UNIVERSAL_METRIC_PORTAL"
                ),

            provenance=
                "V7_V8_V9_V10_ACTION_ORACLE_HISTORY",

            reason=
                (
                    "COLLECTIVE_SOURCE_SCALING_ALONE_IS_NOT_ANTIGRAVITY"
                ),
        ),

        # ============================================================
        # CLOSED / PRESERVED MEMORY
        # ============================================================

        FamilyRecipe(
            family_id=
                "CURRENT_HIDDEN_AXIAL_PURE_J0_KINETIC_CONFORMAL",

            tier=
                "CLOSED",

            priority=
                1,

            status=
                "CLOSED_R6",

            action_readiness=
                "MICROSCOPIC_PARTIAL_REALIZATION_EXISTED",

            universal_metric_response=
                "PURE_J0_STATIC_KINETIC_CONFORMAL",

            stand_off_status=
                "FINITE_PAYLOAD_OUTWARD_CLASSICALLY_PRESENT",

            protection_status=
                "SHIFT_SYMMETRY",

            source_burden=
                "HIDDEN_AXIAL_SOURCE",

            support_control_burden=
                "V19_BAG_PREFLIGHT",

            mechanism_prior_alignment=
                "STRONG_BUT_EMPIRICALLY_INCOMPATIBLE",

            inherited_blockers=
                (
                    "R5_CASIMIR_EMPIRICAL_RED;"
                    "R6_POSITIVE_J2_CANCELLATION_CLOSED;"
                    "R6_EMPIRICAL_ENERGY_OVERLAP_EMPTY"
                ),

            next_gate=
                "NONE_CURRENT_IMPLEMENTATION_CLOSED",

            provenance=
                "032V13_THROUGH_032V19R6",

            reason=
                (
                    "EMPIRICAL_METRIC_MIN_123P456884_KEV_EXCEEDS_"
                    "STRICT_PARTIAL_ENERGY_MAX_122P996182_KEV"
                ),
        ),

        FamilyRecipe(
            family_id=
                "PURE_STATIC_DISFORMAL_DPHI_DPHI",

            tier=
                "CLOSED",

            priority=
                2,

            status=
                "CLOSED_STATIC_G00",

            action_readiness=
                "KNOWN_OPERATOR",

            universal_metric_response=
                "NO_STATIC_G00_RESPONSE",

            stand_off_status=
                "NO_DIRECT_STATIC_STANDOFF",

            protection_status=
                "SHIFT_SYMMETRY",

            source_burden=
                "NOT_RELEVANT",

            support_control_burden=
                "NOT_RELEVANT",

            mechanism_prior_alignment=
                "LOW",

            inherited_blockers=
                "032F_AND_014_015_STATIC_CLOSURE",

            next_gate=
                "NONE_WITHOUT_TIME_GRADIENT_OR_NEW_PHYSICS",

            provenance=
                "V12_PRESERVED_CLOSURE",

            reason=
                "D0PHI_ZERO_REMOVES_DIRECT_STATIC_DISFORMAL_G00_SHIFT",
        ),

        FamilyRecipe(
            family_id=
                "VECTOR_METRIC_PORTAL_PROTECTED_IMPLEMENTATIONS",

            tier=
                "CLOSED",

            priority=
                3,

            status=
                "CLOSED_THROUGH_022A",

            action_readiness=
                "TESTED",

            universal_metric_response=
                "MODEL_DEPENDENT",

            stand_off_status=
                "TESTED_IMPLEMENTATIONS_FAILED",

            protection_status=
                "TESTED_PROTECTIONS_FAILED",

            source_burden=
                "CLOSED",

            support_control_burden=
                "CLOSED",

            mechanism_prior_alignment=
                "DO_NOT_REOPEN",

            inherited_blockers=
                "018_022_FAILURE_MEMORY",

            next_gate=
                "ONLY_GENUINELY_NEW_PROTECTION",

            provenance=
                "018C_THROUGH_022A",

            reason=
                "PROTECTED_VECTOR_IMPLEMENTATIONS_ALREADY_EXHAUSTED",
        ),

        FamilyRecipe(
            family_id=
                "INDEPENDENT_MULTISCALAR_032G_032H",

            tier=
                "CLOSED",

            priority=
                4,

            status=
                "CLOSED_TESTED_ARCHITECTURE",

            action_readiness=
                "DEEPLY_SCANNED",

            universal_metric_response=
                "CORRECTED_SOURCE_AWARE",

            stand_off_status=
                "NO_PRACTICAL_SURVIVOR",

            protection_status=
                "NOT_SAVING",

            source_burden=
                "SCALES_WITH_CHANNEL_COUNT",

            support_control_burden=
                "HIGH",

            mechanism_prior_alignment=
                "COLLECTIVE_RESPONSE_NOT_FASTER_THAN_COST",

            inherited_blockers=
                "APPROX_51_MILLION_EVALUATIONS_NO_LT10MJ",

            next_gate=
                "NONE_SAME_ARCHITECTURE",

            provenance=
                "032G_032H",

            reason=
                "INDEPENDENT_CHANNEL_SCALING_DOES_NOT_IMPROVE_COMPLETE_EFFICIENCY",
        ),

        FamilyRecipe(
            family_id=
                "PURE_GR_PRACTICAL_LT10MJ",

            tier=
                "CLOSED",

            priority=
                5,

            status=
                "CLOSED_BY_1_OVER_G_BURDEN",

            action_readiness=
                "006D_TRUE_STANDOFF_EXISTS",

            universal_metric_response=
                "GR",

            stand_off_status=
                "PROVEN",

            protection_status=
                "NOT_APPLICABLE",

            source_burden=
                "FUNDAMENTAL_1_OVER_G_SCALE",

            support_control_burden=
                "ENORMOUS",

            mechanism_prior_alignment=
                "SIGN_GOOD_ENERGY_FATAL",

            inherited_blockers=
                "024_030_NO_TESTED_ESCAPE",

            next_gate=
                "NONE_WITHOUT_GENUINELY_NEW_GAIN_PHYSICS",

            provenance=
                "006D_AND_024_030",

            reason=
                "TRUE_STANDOFF_DOES_NOT_IMPLY_PRACTICAL_ENERGY",
        ),
    ]

    identifiers = [
        row.family_id
        for row in rows
    ]

    if len(
        identifiers
    ) != len(
        set(
            identifiers
        )
    ):
        raise RuntimeError(
            "duplicate family_id in V20 rerank"
        )

    return rows


def ranked_active_recipes() -> list[FamilyRecipe]:
    """Return active recipes in transparent tier order."""

    rows = [
        row
        for row in family_recipes()
        if not row.closed
    ]

    return sorted(
        rows,
        key=lambda row:
            row.rank_key(),
    )


def closed_recipes() -> list[FamilyRecipe]:
    """Return preserved closed families."""

    rows = [
        row
        for row in family_recipes()
        if row.closed
    ]

    return sorted(
        rows,
        key=lambda row:
            row.rank_key(),
    )


def family_recipe(
    family_id: str,
) -> FamilyRecipe:
    """Return one declared family recipe."""

    for row in family_recipes():
        if (
            row.family_id
            ==
            family_id
        ):
            return row

    raise KeyError(
        family_id
    )


def failure_memory_rules() -> list[dict[str, Any]]:
    """Return R3-R6 family-level failure rules for persistent AGMINER memory."""

    return [
        {
            "family":
                "032_KINETIC_CONFORMAL_PURE_J0_STATIC_COEFFICIENT",

            "family_version":
                "R5_R6",

            "rule_type":
                "EMPIRICAL_NO_GO_CURRENT_OPERATOR",

            "proof_reference":
                "032V19R5_TWO_SCALAR_CASIMIR_EMPIRICAL_GATE",

            "rule": {
                "policy_specific":
                    False,

                "scope":
                    "CURRENT_PURE_J0_LOW_ENERGY_OPERATOR_COEFFICIENT",

                "closed":
                    True,

                "current_c_ev_m4":
                    1.5142715050689224e-18,

                "empirical_c_cap_ev_m4":
                    2.152329494814525e-21,

                "current_over_cap":
                    703.5500413469051,

                "reason":
                    "OFFSTATE_TWO_SCALAR_FINITE_GOLD_FILM_CASIMIR_FORCE",

                "all_kinetic_conformal_theories_closed":
                    False,
            },
        },

        {
            "family":
                "032_DIM8_MATTER_J2_FIXED_STATIC_RESPONSE",

            "family_version":
                "R6",

            "rule_type":
                "POSITIVITY_CANCELLATION_NO_GO",

            "proof_reference":
                "032V19R6_J2_REFLECTION_POSITIVITY_GATE",

            "rule": {
                "policy_specific":
                    False,

                "scope":
                    "UNIVERSAL_DIM8_MATTER_J2_AT_FIXED_STATIC_CS",

                "closed":
                    True,

                "forward_positivity_condition":
                    "C2_GE_0",

                "reflection_reduction_requires":
                    "C2_LT_0",

                "positive_j2_never_reduces_reflection":
                    True,

                "general_companion_operator_cancellation_closed":
                    False,
            },
        },

        {
            "family":
                "032_HIDDEN_AXIAL_KINETIC_CONFORMAL_IMPLEMENTATION",

            "family_version":
                "V13_R6",

            "rule_type":
                "POLICY_SOURCE_IMPLEMENTATION_CLOSURE",

            "proof_reference":
                "032V19R6_EXACT_V17_EMPIRICAL_ENERGY_OVERLAP",

            "rule": {
                "policy_specific":
                    True,

                "policy":
                    "STRICT_COMPLETE_OPERATING_LT_10MJ",

                "scope":
                    "CURRENT_HIDDEN_AXIAL_SOURCE_AND_CURRENT_LOW_ENERGY_OPERATOR",

                "closed":
                    True,

                "empirical_metric_min_ev":
                    123456.8841240774,

                "strict_partial_energy_metric_max_ev":
                    122996.18244440094,

                "metric_gap_ev":
                    460.7016796764656,

                "empirical_energy_overlap_exists":
                    False,

                "all_possible_kinetic_conformal_theories_closed":
                    False,
            },
        },

        {
            "family":
                "032_SINGLE_LINEAR_UNIVERSAL_TRACE_SCALAR_UV",

            "family_version":
                "R3",

            "rule_type":
                "UV_TEMPLATE_PHYSICS_NO_GO",

            "proof_reference":
                "032V19R3_SCALAR_TRACE_UV_GATE",

            "rule": {
                "policy_specific":
                    False,

                "scope":
                    "SINGLE_CANONICAL_LINEAR_UNSCREENED_UNIVERSAL_TRACE_SCALAR",

                "closed":
                    True,

                "correct_outward_tree_sign":
                    True,

                "negative_mass_required":
                    False,

                "fatal_reason":
                    (
                        "UNAVOIDABLE_RANK_ONE_COMPANIONS_PLUS_"
                        "NANOMETER_OFFSTATE_FIFTH_FORCE"
                    ),
            },
        },

        {
            "family":
                "032_NARROW_BAND_LINEAR_SCALAR_TOWER_CURRENT_SOURCE",

            "family_version":
                "R4",

            "rule_type":
                "POLICY_SOURCE_FAMILY_CLOSURE",

            "proof_reference":
                "032V19R4_CAUCHY_EMPIRICAL_ENERGY_BOUND",

            "rule": {
                "policy_specific":
                    True,

                "scope":
                    "CURRENT_SOURCE_NARROW_BAND_HEALTHY_LINEAR_SCALAR_TOWER",

                "closed":
                    True,

                "cauchy_identity":
                    "C1_SQUARED_LE_4_DX_DT",

                "x_companion_energy_floor_j":
                    12128018.193629345,

                "base_plus_x_floor_j":
                    15809937.268980209,

                "broad_spectral_tower_closed":
                    False,
            },
        },

        {
            "family":
                "032_DENSITY_ONLY_SAME_TRACE_VERTEX_SCREENING",

            "family_version":
                "R4",

            "rule_type":
                "DIRECT_RESCUE_NO_GO",

            "proof_reference":
                "032V19R4_SAME_VERTEX_SCREENING_GATE",

            "rule": {
                "policy_specific":
                    False,

                "scope":
                    "SAME_LINEAR_MATTER_VERTEX_OFFSTATE_AND_ACTIVE_STATE",

                "closed_as_direct_rescue":
                    True,

                "required_amplitude_retention_max":
                    0.0044988226665448085,

                "reason":
                    "SCREENING_OFFSTATE_FORCE_ALSO_SCREENS_ACTIVE_C1",

                "active_state_dependent_descreening_closed":
                    False,
            },
        },

        {
            "family":
                "032_PURE_J0_GOLDSTONE_OR_Z2_PROMOTION",

            "family_version":
                "R5_R6",

            "rule_type":
                "INHERITED_PROMOTION_BLOCK",

            "proof_reference":
                "032V19R5_R6_LOW_ENERGY_OPERATOR_BLOCK",

            "rule": {
                "policy_specific":
                    False,

                "scope":
                    "PURE_J0_LOW_ENERGY_LIMIT_ONLY",

                "closed":
                    True,

                "promotion_without_new_low_energy_physics":
                    False,

                "goldstone_family_globally_closed":
                    False,

                "z2_loop_family_globally_closed":
                    False,

                "required_evasion":
                    (
                        "EXPLICIT_LOW_ENERGY_OPERATOR_CONTENT_OR_MATERIAL_"
                        "RESPONSE_THAT_CHANGES_R5_TWO_SCALAR_AMPLITUDE"
                    ),
            },
        },
    ]


def persist_failure_memory(
    storage: Storage,
) -> int:
    """Insert R3-R6 region rules idempotently.

    Region-rules currently have no database uniqueness constraint.
    Therefore idempotency is implemented here using the tuple

        family
        family_version
        rule_type
        proof_reference.

    Existing candidate, rejection, action-oracle, and mechanism rows are not
    modified.
    """

    inserted = 0

    for record in failure_memory_rules():
        existing = storage.connection.execute(
            """
            SELECT COUNT(*) AS count
            FROM region_rules
            WHERE family=?
              AND family_version=?
              AND rule_type=?
              AND proof_reference=?
            """,
            (
                record[
                    "family"
                ],

                record[
                    "family_version"
                ],

                record[
                    "rule_type"
                ],

                record[
                    "proof_reference"
                ],
            ),
        ).fetchone()

        if (
            existing is not None
            and int(
                existing[
                    "count"
                ]
            ) > 0
        ):
            continue

        storage.add_region_rule(
            family=
                record[
                    "family"
                ],

            family_version=
                record[
                    "family_version"
                ],

            rule_type=
                record[
                    "rule_type"
                ],

            rule=
                record[
                    "rule"
                ],

            proof_reference=
                record[
                    "proof_reference"
                ],
        )

        inserted += 1

    return inserted


def persist_frontier_metadata(
    storage: Storage,
) -> None:
    """Record current AGMINER research-state metadata."""

    storage.set_metadata(
        "agminer_research_mode",
        "GLOBAL_CANDIDATE_FAMILY_RERANK",
    )

    storage.set_metadata(
        "agminer_frontier_version",
        "032V20",
    )

    storage.set_metadata(
        "current_closed_implementation",
        "032_HIDDEN_AXIAL_PURE_J0_KINETIC_CONFORMAL_V13_R6",
    )

    storage.set_metadata(
        "agminer_itself_preserved",
        "1",
    )

    storage.set_metadata(
        "all_kinetic_conformal_theories_closed",
        "0",
    )

    storage.set_metadata(
        "physical_antigravity_model_found",
        "0",
    )

    storage.set_metadata(
        "certified_sub10mj_model_found",
        "0",
    )
