"""032V25 AGMINER global rerank around a non-removable metric bridge.

V24 established a new architecture-level falsification rule:

An apparent source-to-metric coupling is not useful evidence unless it survives

    canonical normalization,
    local invertible field redefinitions,
    and source Ward identities.

V25 applies that lesson globally without rewriting the historical V20 family
ranking.

This module is a research scheduler and failure-memory layer.

It does NOT assert that its highest-ranked design target exists as a physical
theory.

It creates no:

    candidate,
    action oracle,
    rejection,
    survivor,
    mechanism metric,
    or new region rule.

CLAIM_CLASSIFICATION=
CURRENT_FRONTIER_RERANK_AND_TIER0_ARCHITECTURE_UPDATE
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .storage import Storage


VERIFIED = "VERIFIED"
OPEN = "OPEN"
FAILED = "FAILED"
HISTORICAL = "HISTORICAL"
NOT_APPLICABLE = "NOT_APPLICABLE"


TIER_ORDER = {
    "A": 0,
    "B": 1,
    "C": 2,
    "CLOSED": 3,
}


TIER0_FIELDS = (
    "microscopic_source",
    "healthy_canonical_mode",
    "universal_physical_metric",
    "nonremovable_crosspropagator",
    "source_ward_compatibility",
    "protection_or_naturalness",
)


@dataclass(frozen=True)
class BridgeFrontierRow:
    family_id: str
    tier: str
    priority: int
    status: str
    role: str

    microscopic_source: str
    independent_productive_charge: str
    healthy_canonical_mode: str
    universal_physical_metric: str
    nonremovable_crosspropagator: str
    source_ward_compatibility: str
    protection_or_naturalness: str
    active_offstate_separation: str

    finite_payload_status: str
    energy_status: str

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

    @property
    def research_rank(self) -> str:
        if self.closed:
            return ""

        return (
            self.tier
            +
            str(
                self.priority
            )
        )

    def rank_key(
        self,
    ) -> tuple[
        int,
        int,
        str,
    ]:
        return (
            TIER_ORDER[
                self.tier
            ],
            self.priority,
            self.family_id,
        )

    def tier0_missing(
        self,
    ) -> tuple[
        str,
        ...,
    ]:
        missing = []

        for field in TIER0_FIELDS:
            if (
                getattr(
                    self,
                    field,
                )
                !=
                VERIFIED
            ):
                missing.append(
                    field
                )

        if (
            self.active_offstate_separation
            ==
            FAILED
        ):
            missing.append(
                "active_offstate_separation"
            )

        return tuple(
            missing
        )

    @property
    def action_oracle_authorized(
        self,
    ) -> bool:
        return (
            not self.closed
            and
            not self.tier0_missing()
            and
            self.active_offstate_separation
            in (
                VERIFIED,
                NOT_APPLICABLE,
            )
        )

    def as_row(
        self,
    ) -> dict[
        str,
        Any,
    ]:
        row = asdict(
            self
        )

        row[
            "closed"
        ] = self.closed

        row[
            "research_rank"
        ] = self.research_rank

        row[
            "tier0_missing"
        ] = list(
            self.tier0_missing()
        )

        row[
            "action_oracle_authorized"
        ] = self.action_oracle_authorized

        return row


def frontier_rows() -> list[
    BridgeFrontierRow
]:
    """Return the post-V24 current frontier without mutating V20 history."""

    rows = [

        # ============================================================
        # TIER A — CURRENT HIGHEST-VALUE DESIGN TARGETS
        # ============================================================

        BridgeFrontierRow(
            family_id=
                "INTRINSIC_SOURCE_ACTIVE_STATE_UNIVERSAL_METRIC_SYNTHESIS",

            tier=
                "A",

            priority=
                1,

            status=
                "DESIGN_TARGET_EXPLICIT_ACTION_REQUIRED",

            role=
                "SYNTHESIS_TARGET_NOT_YET_A_THEORY",

            microscopic_source=
                OPEN,

            independent_productive_charge=
                OPEN,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                OPEN,

            nonremovable_crosspropagator=
                OPEN,

            source_ward_compatibility=
                OPEN,

            protection_or_naturalness=
                OPEN,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "NOT_YET_DEFINED",

            energy_status=
                "NO_ENERGY_CLAIM_ACTION_REQUIRED_FIRST",

            inherited_blockers=
                (
                    "V24_TESTED_LINEAR_VECTOR_BRIDGES_CLOSED;"
                    "R5_R6_SAME_LOW_ENERGY_VERTEX_EMPIRICALLY_FATAL;"
                    "V22_UNPROTECTED_SINGLE_SCALE_LOCALIZATION_CLOSED"
                ),

            next_gate=
                (
                    "032V25A_EXPLICIT_SYMMETRY_PROTECTED_ACTIVE_STATE_"
                    "PHYSICAL_METRIC_ACTION_EXISTENCE_GATE"
                ),

            provenance=
                (
                    "V17_R5_R6_V24A_TO_V24D_"
                    "INTROSPECTIVE"
                ),

            reason=
                (
                    "COMBINES_THE_ONLY_DURABLE_HIGH_VALUE_LESSONS:"
                    "INDEPENDENT_SOURCE_CHARGE;"
                    "ACTIVE_OFFSTATE_SEPARATION;"
                    "ONE_UNIVERSAL_PHYSICAL_METRIC;"
                    "NONREMOVABLE_CROSSPROPAGATOR"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "ACTIVE_STATE_DEPENDENT_KINETIC_METRIC_DESCREENING",

            tier=
                "A",

            priority=
                2,

            status=
                "OPEN_EXPLICIT_ACTION_OR_THEOREM_REQUIRED",

            role=
                "PORTAL_SIDE_DESIGN_TARGET",

            microscopic_source=
                OPEN,

            independent_productive_charge=
                OPEN,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                OPEN,

            nonremovable_crosspropagator=
                OPEN,

            source_ward_compatibility=
                OPEN,

            protection_or_naturalness=
                OPEN,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "STRUCTURALLY_POSSIBLE_NOT_RECONSTRUCTED",

            energy_status=
                "NO_NEW_ENERGY_OPTIMIZATION_AUTHORIZED",

            inherited_blockers=
                (
                    "R4_DENSITY_ONLY_SAME_VERTEX_SCREENING_CLOSED;"
                    "R5_R6_OFFSTATE_MATERIAL_FORCE_NEAR_MISS;"
                    "MUST_DESCREEN_FROM_PHYSICAL_ACTIVE_STATE_"
                    "NOT_PARAMETER_TUNING"
                ),

            next_gate=
                (
                    "EXPLICIT_SYMMETRY_PROTECTED_ACTIVE_STATE_ACTION_"
                    "AND_OFFSTATE_LIMIT_THEOREM"
                ),

            provenance=
                (
                    "V20_ACTIVE_X_DESCREENING_PLUS_"
                    "R5_R6_PLUS_V24D"
                ),

            reason=
                (
                    "DIRECTLY_ATTACKS_THE_V17_R5_R6_NEAR_MISS_BY_"
                    "REQUIRING_ACTIVE_RESPONSE_AND_OFFSTATE_EMPIRICAL_"
                    "COUPLING_TO_SEPARATE_PHYSICALLY"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "SHIFT_PROTECTED_GOLDSTONE_KINETIC_METRIC_WITH_R5_EVASION",

            tier=
                "A",

            priority=
                3,

            status=
                "OPEN_ONLY_WITH_GENUINELY_NEW_NONPURE_J0_CONTENT",

            role=
                "PROTECTED_KINETIC_METRIC_REMAINDER",

            microscopic_source=
                HISTORICAL,

            independent_productive_charge=
                HISTORICAL,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                OPEN,

            nonremovable_crosspropagator=
                OPEN,

            source_ward_compatibility=
                OPEN,

            protection_or_naturalness=
                VERIFIED,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "V17_HISTORICAL_ONLY",

            energy_status=
                (
                    "V17_LOW_PARTIAL_HISTORICAL_"
                    "CURRENT_OPERATOR_CLOSED"
                ),

            inherited_blockers=
                (
                    "PURE_J0_LIMIT_CLOSED_R5_R6;"
                    "V21_STATIONARY_Q_CLOSED;"
                    "V22_UNPROTECTED_SINGLE_SCALE_LOCALIZATION_CLOSED"
                ),

            next_gate=
                (
                    "DERIVE_EXPLICIT_NONPURE_J0_MULTISCALE_OR_"
                    "ACTIVE_STATE_ACTION_BEFORE_ANY_SCAN"
                ),

            provenance=
                "V17_V19R6_V21_V22",

            reason=
                (
                    "SHIFT_PROTECTION_AND_V17_RESPONSE_PER_JOULE_"
                    "ARE_VALUABLE_BUT_THE_FAILED_LOW_ENERGY_OPERATOR_"
                    "MUST_NOT_BE_RELABELED_AND_REUSED"
                ),
        ),

        # ============================================================
        # TIER B — REAL SURVIVING SOURCE/PORTAL CLASSES,
        #          BUT MISSING ESSENTIAL ARROWS
        # ============================================================

        BridgeFrontierRow(
            family_id=
                "INTRINSIC_DIRAC_HYPERMOMENTUM_NONREMOVABLE_METRIC_BRIDGE",

            tier=
                "B",

            priority=
                1,

            status=
                "SOURCE_PROVENANCE_PRESERVED_BRIDGE_UNRESOLVED",

            role=
                "SOURCE_SIDE_KNOWLEDGE",

            microscopic_source=
                VERIFIED,

            independent_productive_charge=
                VERIFIED,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                OPEN,

            nonremovable_crosspropagator=
                OPEN,

            source_ward_compatibility=
                OPEN,

            protection_or_naturalness=
                OPEN,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "NOT_ESTABLISHED",

            energy_status=
                "SOURCE_CHARGE_PER_JOULE_NOT_ESTABLISHED",

            inherited_blockers=
                (
                    "V24A_WEYL_TRACE_ZERO;"
                    "V24B_DIRECT_UNCOMPENSATED_FRONSDAL_SPIN3_CLOSED;"
                    "V24C_CLEAN_REST_PAIR_TS_SPIN1_CLOSED;"
                    "V24D_TESTED_PROTECTED_LINEAR_VECTOR_BRIDGES_CLOSED"
                ),

            next_gate=
                (
                    "ONLY_REOPEN_WITH_AN_EXPLICIT_ACTION_CONTAINING_A_"
                    "NONREMOVABLE_UNIVERSAL_METRIC_CROSSPROPAGATOR"
                ),

            provenance=
                "V24A_V24B_V24C_V24D",

            reason=
                (
                    "EXPLICIT_INTRINSIC_DIRAC_SOURCE_IS_REAL_SOURCE_"
                    "KNOWLEDGE_BUT_NO_TESTED_HEALTHY_UNIVERSAL_"
                    "METRIC_BRIDGE_SURVIVED"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "PROTECTED_FIELD_VALUE_CONFORMAL_SCALAR_METRIC",

            tier=
                "B",

            priority=
                2,

            status=
                "OPEN_ONLY_WITH_GENUINELY_NEW_PROTECTION",

            role=
                "DIRECT_METRIC_CLASS_WITH_HISTORICAL_SOURCE",

            microscopic_source=
                HISTORICAL,

            independent_productive_charge=
                HISTORICAL,

            healthy_canonical_mode=
                HISTORICAL,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                VERIFIED,

            source_ward_compatibility=
                NOT_APPLICABLE,

            protection_or_naturalness=
                FAILED,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "031_HISTORICAL_CLASSICAL_RESPONSE",

            energy_status=
                "031_HISTORICAL_GJ_SCALE_NOT_CURRENT_TARGET",

            inherited_blockers=
                (
                    "031F0_UNPROTECTED_ULTRALIGHT_SCALAR_CLOSED;"
                    "DO_NOT_REOPEN_WITHOUT_NEW_RADIATIVE_PROTECTION"
                ),

            next_gate=
                (
                    "NEW_EXACT_PROTECTION_THEOREM_BEFORE_"
                    "SOURCE_OPTIMIZATION"
                ),

            provenance=
                "031_THROUGH_031F0",

            reason=
                (
                    "DIRECT_UNIVERSAL_METRIC_PORTAL_IS_STRUCTURALLY_"
                    "STRONG_BUT_TESTED_ULTRALIGHT_REALIZATION_FAILED_"
                    "NATURALNESS_EMPIRICAL_GATES"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "MATTER_TRIGGERED_PFORM_BROADER_DOMAIN",

            tier=
                "B",

            priority=
                3,

            status=
                "BROADER_CLASS_OPEN_TESTED_032R_DOMAIN_CLOSED",

            role=
                "TRIGGERED_GEOMETRIC_FIELD_CLASS",

            microscopic_source=
                OPEN,

            independent_productive_charge=
                OPEN,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                OPEN,

            nonremovable_crosspropagator=
                OPEN,

            source_ward_compatibility=
                OPEN,

            protection_or_naturalness=
                OPEN,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "UNRESOLVED",

            energy_status=
                "TESTED_TRIGGER_DOMAIN_FAILED",

            inherited_blockers=
                (
                    "032R_DECLARED_DOMAIN_CLOSED_"
                    "DO_NOT_RESCAN"
                ),

            next_gate=
                (
                    "NEW_TRIGGER_SCALING_OR_NONREMOVABLE_METRIC_"
                    "PORTAL_THEOREM_REQUIRED_BEFORE_REOPENING"
                ),

            provenance=
                "032R_BROADER_PFORM_REMAINDER",

            reason=
                (
                    "BROADER_PFORM_PHYSICS_NOT_FORMALLY_CLOSED_"
                    "BUT_NO_CURRENT_COMPLETE_SOURCE_TO_UNIVERSAL_"
                    "METRIC_CHAIN"
                ),
        ),

        # ============================================================
        # TIER C — NOT FORMALLY CLOSED, POOR EXPECTED VALUE
        # ============================================================

        BridgeFrontierRow(
            family_id=
                "BROAD_SPECTRAL_LINEAR_SCALAR_TOWER",

            tier=
                "C",

            priority=
                1,

            status=
                (
                    "LOW_PRIORITY_SEVERE_EMPIRICAL_AND_"
                    "SCAFFOLDING_PRESSURE"
                ),

            role=
                "MULTI_MEDIATOR_DIRECT_METRIC_CLASS",

            microscopic_source=
                OPEN,

            independent_productive_charge=
                OPEN,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                VERIFIED,

            source_ward_compatibility=
                NOT_APPLICABLE,

            protection_or_naturalness=
                OPEN,

            active_offstate_separation=
                FAILED,

            finite_payload_status=
                "STRUCTURALLY_POSSIBLE",

            energy_status=
                "NO_CURRENT_PRACTICAL_SURVIVOR",

            inherited_blockers=
                (
                    "R3_SINGLE_SCALAR_CLOSED;"
                    "R4_NARROW_BAND_TOWER_CLOSED;"
                    "SAME_LOW_ENERGY_TRACE_PORTALS_INHERIT_"
                    "FIFTH_FORCE_PRESSURE"
                ),

            next_gate=
                (
                    "ONLY_REVISIT_WITH_NEW_SPECTRAL_SUM_RULE_"
                    "AND_OFFSTATE_EVASION"
                ),

            provenance=
                "R3_R4",

            reason=
                (
                    "DIRECT_METRIC_RESPONSE_EXISTS_BUT_EMPIRICAL_"
                    "AND_SCAFFOLDING_TAX_DOMINATES"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "SECONDARY_TOPOLOGICAL_SHARED_SCAFFOLD",

            tier=
                "C",

            priority=
                2,

            status=
                "SOURCE_SIDE_INTERESTING_PORTAL_SIDE_UNSOLVED",

            role=
                "SOURCE_ONLY_ARCHITECTURE",

            microscopic_source=
                VERIFIED,

            independent_productive_charge=
                OPEN,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                FAILED,

            nonremovable_crosspropagator=
                FAILED,

            source_ward_compatibility=
                OPEN,

            protection_or_naturalness=
                VERIFIED,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "NO_METRIC_ACTIVE_PROMOTION",

            energy_status=
                "PORTAL_DOMINATED",

            inherited_blockers=
                "V9_V10_NO_FINITE_PAYLOAD_METRIC_ACTIVE_PROMOTION",

            next_gate=
                (
                    "NO_REOPEN_WITHOUT_DIRECT_LOCAL_NONREMOVABLE_"
                    "UNIVERSAL_METRIC_PORTAL"
                ),

            provenance=
                "V7_V8_V9_V10",

            reason=
                (
                    "COLLECTIVE_SOURCE_SCALING_ALONE_"
                    "IS_NOT_ANTIGRAVITY"
                ),
        ),

        # ============================================================
        # CLOSED — CURRENT FAILURE MEMORY
        # ============================================================

        BridgeFrontierRow(
            family_id=
                "V21_STATIONARY_Q_TIME_GRADIENT_DISFORMAL",

            tier=
                "CLOSED",

            priority=
                1,

            status=
                "CLOSED_STATIONARITY_INVERTIBILITY_COSMOLOGY",

            role=
                "CLOSED_DYNAMIC_DISFORMAL_REALIZATION",

            microscopic_source=
                FAILED,

            independent_productive_charge=
                OPEN,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                VERIFIED,

            source_ward_compatibility=
                NOT_APPLICABLE,

            protection_or_naturalness=
                VERIFIED,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "LOCAL_SIGN_MECHANISM_KNOWLEDGE_ONLY",

            energy_status=
                (
                    "REFERENCE_LOCAL_FIELD_INVENTORY_LOW_"
                    "BUT_ROUTE_CLOSED"
                ),

            inherited_blockers=
                (
                    "V21_STATIONARY_Q_INTEGRABILITY_PLUS_"
                    "INVERTIBILITY_COSMOLOGY"
                ),

            next_gate=
                "NONE_SAME_STATIONARY_Q_ARCHITECTURE",

            provenance=
                "032V21",

            reason=
                (
                    "LOCAL_OUTWARD_SIGN_DID_NOT_SUPPLY_A_"
                    "REALIZABLE_STATIONARY_RESERVOIR"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "V22_UNPROTECTED_SINGLE_SCALE_LOCALIZED_DISFORMAL",

            tier=
                "CLOSED",

            priority=
                2,

            status=
                "CLOSED_NATURALNESS_ENERGY_FLOOR",

            role=
                "CLOSED_LOCALIZED_DYNAMIC_DISFORMAL_REALIZATION",

            microscopic_source=
                OPEN,

            independent_productive_charge=
                OPEN,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                VERIFIED,

            source_ward_compatibility=
                NOT_APPLICABLE,

            protection_or_naturalness=
                FAILED,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "KINEMATICALLY_OPEN",

            energy_status=
                "OPTIMISTIC_LOWER_FLOOR_ABOUT_275_MJ",

            inherited_blockers=
                "V22_UNPROTECTED_SINGLE_SCALE_EFT",

            next_gate=
                "ONLY_EXPLICIT_PROTECTED_MULTISCALE_VARIANT",

            provenance=
                "032V22",

            reason=
                (
                    "LOCALIZATION_DID_NOT_SURVIVE_NATURALNESS_"
                    "PLUS_ABSOLUTE_ENERGY"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "V23_ORDINARY_STRESS_DERIVATIVE_HYPERMOMENTUM",

            tier=
                "CLOSED",

            priority=
                3,

            status=
                "CLOSED_FIXED_MOMENT_FINITE_PAYLOAD_EMPIRICAL",

            role=
                "CLOSED_ORDINARY_STRESS_SOURCE_ROUTE",

            microscopic_source=
                VERIFIED,

            independent_productive_charge=
                FAILED,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                OPEN,

            nonremovable_crosspropagator=
                OPEN,

            source_ward_compatibility=
                OPEN,

            protection_or_naturalness=
                OPEN,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "FAILED_REQUIRED_RESPONSE",

            energy_status=
                "OPTIMISTIC_FLOOR_ENORMOUS",

            inherited_blockers=
                "V23_FIXED_DIPOLE_MOMENT_THEOREM",

            next_gate=
                "NONE_ORDINARY_STRESS_ONE_DERIVATIVE_ROUTE",

            provenance=
                "032V23",

            reason=
                "NO_INDEPENDENT_CHARGE_PER_JOULE_LEVER",
        ),

        BridgeFrontierRow(
            family_id=
                "V24_MARZO_LINEAR_VECTOR_GRAVITON_PORTAL",

            tier=
                "CLOSED",

            priority=
                4,

            status=
                "CLOSED_LINEAR_STUECKELBERG_REMOVABLE",

            role=
                "CLOSED_LINEAR_BRIDGE",

            microscopic_source=
                OPEN,

            independent_productive_charge=
                OPEN,

            healthy_canonical_mode=
                VERIFIED,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                FAILED,

            source_ward_compatibility=
                FAILED,

            protection_or_naturalness=
                VERIFIED,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "NOT_REACHED",

            energy_status=
                "NOT_EVALUATED_CHEAP_THEOREM_KILL",

            inherited_blockers=
                (
                    "V24D_STUECKELBERG_FIELD_REDEFINITION_"
                    "AND_SOURCE_WARD_DIAGONALIZATION"
                ),

            next_gate=
                (
                    "NONLINEAR_COMPLETION_ONLY_IF_NEW_"
                    "NONREMOVABLE_RESPONSE_IS_DERIVED"
                ),

            provenance=
                "032V24D",

            reason=
                (
                    "APPARENT_LINEAR_VECTOR_METRIC_MIXING_IS_"
                    "NOT_A_PHYSICAL_CROSS_SOURCE"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                (
                    "V24_BMS_UNIVERSAL_IR_TORSIONLIKE_"
                    "VECTOR_METRIC_BRIDGE"
                ),

            tier=
                "CLOSED",

            priority=
                5,

            status=
                "CLOSED_DECLARED_IR_METRIC_ABSENT",

            role=
                "CLOSED_LINEAR_BRIDGE",

            microscopic_source=
                HISTORICAL,

            independent_productive_charge=
                HISTORICAL,

            healthy_canonical_mode=
                VERIFIED,

            universal_physical_metric=
                FAILED,

            nonremovable_crosspropagator=
                FAILED,

            source_ward_compatibility=
                OPEN,

            protection_or_naturalness=
                VERIFIED,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "NOT_REACHED",

            energy_status=
                "NOT_EVALUATED_CHEAP_THEOREM_KILL",

            inherited_blockers=
                (
                    "V24D_DECLARED_UNIVERSAL_IR_ACTION_"
                    "HAS_NO_DYNAMICAL_METRIC"
                ),

            next_gate=
                (
                    "NONLINEAR_MAG_COMPLETION_ONLY_IF_"
                    "PHYSICAL_METRIC_PORTAL_EXPLICIT"
                ),

            provenance=
                "032V24D",

            reason=
                (
                    "HEALTHY_VECTOR_MODE_WITHOUT_A_UNIVERSAL_"
                    "METRIC_BRIDGE_IS_NOT_ANTIGRAVITY"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "029_TESTED_MASSIVE_SPIN2_PORTAL",

            tier=
                "CLOSED",

            priority=
                6,

            status=
                "CLOSED_TESTED_MASS_GATED_SPIN2_ROUTE",

            role=
                "CLOSED_SPIN2_GAIN_PORTAL",

            microscopic_source=
                HISTORICAL,

            independent_productive_charge=
                FAILED,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                VERIFIED,

            source_ward_compatibility=
                NOT_APPLICABLE,

            protection_or_naturalness=
                OPEN,

            active_offstate_separation=
                OPEN,

            finite_payload_status=
                "TESTED",

            energy_status=
                (
                    "CONTROL_STRONG_COUPLING_REALIZATION_"
                    "FATAL_IN_TESTED_ROUTE"
                ),

            inherited_blockers=
                (
                    "029_MASS_GATING_STRONG_COUPLING_WALL_"
                    "AND_EMPIRICAL_COSTS"
                ),

            next_gate=
                "NONE_WITHOUT_GENUINELY_NEW_SPIN2_PHYSICS",

            provenance=
                "029",

            reason=
                (
                    "DO_NOT_REOPEN_GENERIC_MASSIVE_SPIN2_"
                    "OR_BIMETRIC_GAIN"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "031F0_UNPROTECTED_ULTRALIGHT_SCALAR",

            tier=
                "CLOSED",

            priority=
                7,

            status=
                "CLOSED_RADIATIVE_NATURALNESS_EMPIRICAL",

            role=
                "CLOSED_SCALAR_REALIZATION",

            microscopic_source=
                VERIFIED,

            independent_productive_charge=
                VERIFIED,

            healthy_canonical_mode=
                HISTORICAL,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                VERIFIED,

            source_ward_compatibility=
                NOT_APPLICABLE,

            protection_or_naturalness=
                FAILED,

            active_offstate_separation=
                FAILED,

            finite_payload_status=
                "HISTORICAL",

            energy_status=
                "BEST_REALIZED_HISTORICAL_ABOUT_96_GJ",

            inherited_blockers=
                "031F0_NO_RADIATIVE_PROTECTION",

            next_gate=
                "NONE_WITHOUT_GENUINELY_NEW_PROTECTION",

            provenance=
                "031_THROUGH_031F0",

            reason=
                (
                    "DIRECT_METRIC_RESPONSE_DOES_NOT_EXCUSE_"
                    "UNPROTECTED_ULTRALIGHT_EFT"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "CURRENT_HIDDEN_AXIAL_PURE_J0_KINETIC_CONFORMAL",

            tier=
                "CLOSED",

            priority=
                8,

            status=
                "CLOSED_R5_R6_EMPIRICAL_ENERGY_NONOVERLAP",

            role=
                "CLOSED_CURRENT_PHYSICAL_IMPLEMENTATION",

            microscopic_source=
                VERIFIED,

            independent_productive_charge=
                VERIFIED,

            healthy_canonical_mode=
                OPEN,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                VERIFIED,

            source_ward_compatibility=
                NOT_APPLICABLE,

            protection_or_naturalness=
                OPEN,

            active_offstate_separation=
                FAILED,

            finite_payload_status=
                "V17_HISTORICAL_GREEN_PARTIAL",

            energy_status=
                (
                    "59P4197_KJ_HISTORICAL_PARTIAL_"
                    "CURRENT_IMPLEMENTATION_CLOSED"
                ),

            inherited_blockers=
                (
                    "R5_CASIMIR_PLUS_R6_EMPTY_"
                    "EMPIRICAL_LT10MJ_OVERLAP"
                ),

            next_gate=
                "NONE_CURRENT_OPERATOR_IMPLEMENTATION",

            provenance=
                "V13_THROUGH_V19R6",

            reason=
                (
                    "PRESERVE_RESPONSE_PER_JOULE_LESSON_"
                    "DO_NOT_REPROMOTE_FAILED_OPERATOR"
                ),
        ),

        BridgeFrontierRow(
            family_id=
                "PURE_GR_PRACTICAL_LT10MJ",

            tier=
                "CLOSED",

            priority=
                9,

            status=
                "CLOSED_BY_1_OVER_G_BURDEN",

            role=
                "CONSERVATIVE_ANCHOR_NOT_PRACTICAL_ROUTE",

            microscopic_source=
                HISTORICAL,

            independent_productive_charge=
                FAILED,

            healthy_canonical_mode=
                VERIFIED,

            universal_physical_metric=
                VERIFIED,

            nonremovable_crosspropagator=
                VERIFIED,

            source_ward_compatibility=
                NOT_APPLICABLE,

            protection_or_naturalness=
                NOT_APPLICABLE,

            active_offstate_separation=
                NOT_APPLICABLE,

            finite_payload_status=
                "006D_TRUE_STANDOFF_ESTABLISHED",

            energy_status=
                "FUNDAMENTAL_1_OVER_G_SCALE_FATAL_FOR_LT10MJ",

            inherited_blockers=
                "006D_PLUS_024_TO_030_NO_TESTED_ESCAPE",

            next_gate=
                "NONE_WITHOUT_GENUINELY_NEW_GAIN_PHYSICS",

            provenance=
                "006D_024_030",

            reason=
                (
                    "TRUE_STANDOFF_EXISTS_BUT_"
                    "PRACTICAL_ENERGY_DOES_NOT"
                ),
        ),
    ]

    identifiers = [
        row.family_id
        for row
        in rows
    ]

    if (
        len(
            identifiers
        )
        !=
        len(
            set(
                identifiers
            )
        )
    ):
        raise RuntimeError(
            "duplicate family_id in V25 rerank"
        )

    return rows


def active_frontier_rows() -> list[
    BridgeFrontierRow
]:
    return sorted(
        (
            row
            for row
            in frontier_rows()
            if not row.closed
        ),
        key=
            lambda row:
                row.rank_key(),
    )


def closed_frontier_rows() -> list[
    BridgeFrontierRow
]:
    return sorted(
        (
            row
            for row
            in frontier_rows()
            if row.closed
        ),
        key=
            lambda row:
                row.rank_key(),
    )


def family_row(
    family_id: str,
) -> BridgeFrontierRow:
    for row in frontier_rows():
        if (
            row.family_id
            ==
            family_id
        ):
            return row

    raise KeyError(
        family_id
    )


def tier0_promotion_policy() -> dict[
    str,
    Any,
]:
    """Return the post-V24 theorem-first pre-scan policy."""

    return {
        "policy_version":
            "NONREMOVABLE_CROSSPROPAGATOR_V1",

        "required_fields":
            list(
                TIER0_FIELDS
            ),

        "active_offstate_separation_must_not_fail":
            True,

        "blind_parameter_scan_authorized":
            False,

        "energy_optimization_before_tier0":
            False,

        "action_oracle_before_tier0":
            False,

        "one_universal_physical_metric_required":
            True,

        "nonremovable_crosspropagator_required":
            True,

        "source_ward_compatibility_required":
            True,

        "canonical_normalization_required":
            True,

        "reject_if": [
            (
                "SOURCE_IS_ONLY_A_DERIVATIVE_OF_ORDINARY_STRESS_"
                "WITH_NO_INDEPENDENT_CHARGE_LEVER"
            ),
            (
                "MEDIATOR_IS_GHOST_TACHYON_OR_PURE_GAUGE"
            ),
            (
                "PAYLOAD_REQUIRES_SPECIAL_SPIN_POLARIZATION_"
                "OR_HIDDEN_CHARGE"
            ),
            (
                "APPARENT_METRIC_MIXING_IS_REMOVABLE_BY_"
                "LOCAL_INVERTIBLE_FIELD_REDEFINITION"
            ),
            (
                "SOURCE_WARD_IDENTITY_DIAGONALIZES_"
                "THE_APPARENT_CROSS_SOURCE"
            ),
            (
                "DECLARED_INFRARED_ACTION_HAS_NO_"
                "DYNAMICAL_PHYSICAL_METRIC"
            ),
            (
                "SAME_UNSUPPRESSED_VERTEX_PRODUCES_"
                "EMPIRICALLY_EXCLUDED_OFFSTATE_FORCE"
            ),
        ],

        "after_tier0": [
            "STATIC_OR_QUASISTATIC_OUTWARD_SIGN",
            "FINITE_PAYLOAD_KERNEL",
            "CANONICAL_RESPONSE_PER_JOULE",
            "POSITIVE_MEDIATOR_FIELD_INVENTORY",
            "SUPPORT_CONTROL_REACTION",
            "EMPIRICAL_AND_RG_UV",
            "COMPLETE_OPERATING_ENERGY_STRICT_LT10MJ",
        ],
    }


def hypothetical_fully_verified_row() -> BridgeFrontierRow:
    """Positive control proving the authorization logic can turn GREEN."""

    return BridgeFrontierRow(
        family_id=
            "V25_TEST_FULLY_VERIFIED_CONTROL",

        tier=
            "A",

        priority=
            99,

        status=
            "TEST_CONTROL",

        role=
            "TEST_CONTROL",

        microscopic_source=
            VERIFIED,

        independent_productive_charge=
            VERIFIED,

        healthy_canonical_mode=
            VERIFIED,

        universal_physical_metric=
            VERIFIED,

        nonremovable_crosspropagator=
            VERIFIED,

        source_ward_compatibility=
            VERIFIED,

        protection_or_naturalness=
            VERIFIED,

        active_offstate_separation=
            VERIFIED,

        finite_payload_status=
            "NOT_YET_RUN",

        energy_status=
            "NOT_YET_RUN",

        inherited_blockers=
            "NONE_TEST_CONTROL",

        next_gate=
            "FINITE_PAYLOAD_AND_ENERGY",

        provenance=
            "UNIT_TEST_ONLY",

        reason=
            "PROVES_GATE_IS_NOT_LOGICALLY_IMPOSSIBLE",
    )


def historical_reference_lessons() -> dict[
    str,
    Any,
]:
    """Carry only durable numerical lessons into the new scheduler."""

    return {
        "006d": {
            "coefficient_c":
                23.591586299249,

            "true_standoff":
                True,

            "practical_lt10mj":
                False,
        },

        "v17": {
            "partial_energy_j":
                5.94197e4,

            "finite_payload_partial":
                True,

            "current_physical_implementation_closed":
                True,

            "lesson":
                (
                    "NON_GR_METRIC_RESPONSE_CAN_ESCAPE_"
                    "1_OVER_G_AT_PARTIAL_LEVEL"
                ),
        },

        "v19r1": {
            "supported_static_preflight_j":
                3.681919e6,

            "certified_model":
                False,
        },

        "introspective": {
            "conserved_dec_headroom_min":
                12.8,

            "conserved_dec_headroom_max":
                17.9,

            "productive_participation_gap_b7_vs_relaxed":
                9.7,
        },

        "desired_future_early_partial_j": {
            "preferred_min":
                1.0e5,

            "preferred_max":
                1.0e6,

            "reason":
                (
                    "LEAVE_ROOM_FOR_SUPPORT_CONTROL_QUANTUM_"
                    "AND_BACKREACTION_BELOW_10MJ"
                ),
        },
    }


def persist_v25_metadata(
    storage: Storage,
) -> None:
    """Persist current scheduler state only; mutate no science tables."""

    metadata = {
        "032v25_ranking_version":
            "NONREMOVABLE_CROSSPROPAGATOR_V1",

        "032v25_top_design_target":
            (
                "INTRINSIC_SOURCE_ACTIVE_STATE_"
                "UNIVERSAL_METRIC_SYNTHESIS"
            ),

        "032v25_nonremovable_crosspropagator_required":
            "1",

        "032v25_source_ward_compatibility_required":
            "1",

        "032v25_one_universal_physical_metric_required":
            "1",

        "032v25_action_oracle_authorized":
            "0",

        "032v25_blind_parameter_scan_authorized":
            "0",

        "032v25_v24_tested_protected_linear_vector_bridges_closed":
            "1",

        "032v25_dirac_intrinsic_source_knowledge_preserved":
            "1",

        "agminer_next_family":
            (
                "ACTIVE_STATE_NONREMOVABLE_"
                "UNIVERSAL_METRIC_ACTION_EXISTENCE"
            ),
    }

    for key, value in metadata.items():
        storage.set_metadata(
            key,
            value,
        )
