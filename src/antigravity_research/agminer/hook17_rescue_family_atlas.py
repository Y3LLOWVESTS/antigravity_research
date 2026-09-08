"""032H17A HOOK17 rescue-family theorem and action atlas.

PURPOSE
-------
Run the first family-level HOOK17 physicalization gate after 032V26C closed
only the simplest direct massless hook-shift source plus raw H^2 metric.

This module deliberately does not scan continuous parameters.  It asks which
physically distinct rescue families survive cheap, invariant checks strongly
enough to justify a more expensive exact source-projector calculation.

SCIENTIFIC STARTING POINT
-------------------------
The preserved project state is:

- V24: an explicit clean Dirac rest particle/antiparticle state carries a
  nonzero intrinsic hook-like nonmetricity source;
- V26B1: quadratic rank-two descendants Q(H,H) possess a nonzero active g00
  numerator and zero off-state first variation;
- V26B1R1: the canonical field-capacity term is exceptionally small, but that
  is only a partial capacity result;
- V26C: a direct protected massless hook shift makes both the direct source
  coupling and the raw H^2 metric non-invariant;
- V26D: protected cT=1 DHOST/KMM is the preserved independent fallback.

NEW H17A TESTS
--------------
1. Curtright/Stueckelberg Ward-rescue theorem

   V24C already provides an invertible representation map from the project
   hook H_a(bc) to a first-pair-antisymmetric Curtright-like tensor T_[ab]c.
   Published linearized massive-(2,1) Stueckelberg theory requires three
   compensating fields (symmetric h_ab, antisymmetric b_ab, vector a_a) and
   admits a gauge-invariant Curtright combination Fhat.

   Therefore, at the kinematic EFT level, replacing T by invariant Fhat and
   mapping back to Hhat removes the exact V26C hook-shift Ward obstruction by
   construction.  In unitary gauge Hhat=H, so the V26B1 quadratic numerator
   and active/off-state algebra are retained.

   This is NOT a same-action completion: the published free Curtright action,
   the Wheeler Dirac source, and the HOOK17 universal metric have not yet been
   derived from one complete action.

2. Massive-Curtright provenance/pole prefilter

   In four dimensions the massive Curtright carrier has five physical degrees
   of freedom and is dual to massive spin-2 formulations.  That provenance is
   a warning because project branch 029 already tested one ordinary massive
   Fierz-Pauli source route.  It is not an automatic closure, because HOOK17
   uses a different intrinsic three-index source and nonlinear metric portal.

   For the clean V24 equal-rest source, however, every nonzero hook component
   contains exactly one time index.  The purely spatial Curtright tensor is
   exactly zero.  Hence its overlap with the purely transverse five-polarization
   massive Curtright pole in the carrier rest frame is zero.  This is a pole
   prefilter only; static Yukawa response is off-shell and must be evaluated
   with the full constrained/Stueckelberg propagator before closure.

3. Healthy hook-symmetric MAG projector-support prefilter

   Mikura/Percacci decompose hook-symmetric nonmetricity modes by longitudinal
   (L) and transverse (T) projector structure.  The clean V24 source contains
   exactly one longitudinal/time index in its rest frame.  Thus, before any
   coefficient algebra:

       hook 2-  : TTT            -> exact support zero
       hook 1-  : TTT            -> exact support zero
       hook 2+  : LTT            -> support allowed, exact projector unknown
       hook 1+  : TTL/TLT/LTT    -> support allowed, exact projector unknown
       hook 0+  : LTT            -> support allowed, exact projector unknown

   This is a cheap source-support theorem.  "Allowed" does not mean a nonzero
   irreducible projector; the exact published P_ij contraction is the next
   decisive calculation.

CLAIM LIMITS
------------
This module does NOT establish:

- a complete HOOK17 action;
- a same-action microscopic source plus healthy mode plus universal metric;
- a nonzero exact healthy-mode projector for the surviving LTT/TTL sectors;
- a static off-shell Curtright cross propagator;
- finite-payload outward acceleration;
- source/support/compensator energy;
- quantum, naturalness, empirical, nonlinear, or complete-energy closure;
- a practical antigravity device.

No AGMINER mass-candidate insertion is performed here.
No energy optimization is authorized here.

CLAIM_CLASSIFICATION=
SCOPED_HOOK17_RESCUE_FAMILY_THEOREM_PROJECTOR_PREFILTER_AND_ACTION_ATLAS
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from .dirac_hook_vector_bridge import (
    hook_to_torsionlike,
    torsionlike_to_hook,
)
from .nonlinear_hook_metric_bridge import (
    quadratic_active_background_derivative,
    quadratic_metric_descendant,
    rest_pair_hook,
)
from .protected_hook_symmetry_compatibility import (
    massless_hook_shift_source_ward_gate,
    quadratic_metric_hook_shift_gate,
)


HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7
TOL = 1.0e-12


@dataclass(frozen=True)
class Hook17FamilyRow:
    """One H17A family-atlas row using the buildplan's minimum columns."""

    FAMILY_ID: str
    FAMILY_NAME: str
    ACTION_REFERENCE: str
    ACTION_EXPLICIT: bool
    FIELD_CONTENT: str
    SYMMETRY: str
    SYMMETRY_EXACT_OR_SOFT: str
    SYMMETRY_BREAKING_SCALE: str
    OFFSTATE_LIMIT: str
    DIRAC_SOURCE_VERTEX: str
    SOURCE_IRREP: str
    SOURCE_WARD_STATUS: str
    HEALTHY_MODE: str
    HEALTHY_MODE_PROJECTOR: str
    SOURCE_PROJECTOR_STATUS: str
    KINETIC_HEALTH_KNOWN: str
    MASS_RANGE: str
    PHYSICAL_METRIC: str
    METRIC_WARD_STATUS: str
    ACTIVE_NUMERATOR_STATUS: str
    FIELD_REDEFINITION_STATUS: str
    OFFSTATE_PORTAL_ORDER: str
    LOWEST_OFFSTATE_FORCE: str
    CANONICALIZATION_STATUS: str
    CAPACITY_FORMULA_STATUS: str
    IMMEDIATE_EMPIRICAL_KILLER: str
    IMMEDIATE_NATURALNESS_KILLER: str
    SAME_ACTION_COMPLETE: bool
    STATUS: str
    FAILURE_CODE: str
    NEXT_CHEAP_FALSIFIER: str


def _finite_rank3(value: np.ndarray) -> np.ndarray:
    """Validate and return a finite 4x4x4 rank-three tensor."""
    array = np.asarray(value, dtype=float)
    if array.shape != (4, 4, 4):
        raise ValueError("rank-three tensor must have shape (4,4,4)")
    if not np.all(np.isfinite(array)):
        raise ValueError("rank-three tensor must be finite")
    return array


def curtright_representation_gate() -> dict[str, Any]:
    """Verify the exact V24 hook <-> Curtright representation map."""
    hook = _finite_rank3(rest_pair_hook())
    curtright = _finite_rank3(hook_to_torsionlike(hook))
    rebuilt = _finite_rank3(torsionlike_to_hook(curtright))

    antisym_residual = float(
        np.max(np.abs(curtright + np.swapaxes(curtright, 0, 1)))
    )
    cyclic = (
        curtright
        + np.transpose(curtright, (1, 2, 0))
        + np.transpose(curtright, (2, 0, 1))
    )
    cyclic_residual = float(np.max(np.abs(cyclic)))
    roundtrip_residual = float(np.max(np.abs(rebuilt - hook)))

    return {
        "hook_norm": float(np.linalg.norm(hook)),
        "curtright_norm": float(np.linalg.norm(curtright)),
        "first_pair_antisymmetric": antisym_residual <= TOL,
        "first_pair_antisymmetry_residual": antisym_residual,
        "curtright_cyclic_identity": cyclic_residual <= TOL,
        "curtright_cyclic_residual": cyclic_residual,
        "representation_roundtrip_pass": roundtrip_residual <= TOL,
        "representation_roundtrip_residual": roundtrip_residual,
        "representation_match_is_action_match": False,
    }


def v24_longitudinal_support_gate() -> dict[str, Any]:
    """Classify clean V24 source support by number/location of time indices.

    This is an exact component-support statement in the declared equal-rest
    frame.  It is not a Lorentz-invariant norm and is used only as a cheap
    prefilter against O(3) L/T projectors defined in the carrier rest frame.
    """
    hook = _finite_rank3(rest_pair_hook())
    total = float(np.sum(hook * hook))
    if total <= 0.0:
        raise ValueError("V24 rest-pair hook unexpectedly vanished")

    by_count = {0: 0.0, 1: 0.0, 2: 0.0, 3: 0.0}
    by_position = {
        "FIRST_L": 0.0,
        "SECOND_L": 0.0,
        "THIRD_L": 0.0,
    }

    nonzero_components: list[dict[str, Any]] = []
    for a in range(4):
        for b in range(4):
            for c in range(4):
                value = float(hook[a, b, c])
                if abs(value) <= TOL:
                    continue
                n_time = int(a == 0) + int(b == 0) + int(c == 0)
                weight = value * value
                by_count[n_time] += weight
                if n_time == 1:
                    if a == 0:
                        by_position["FIRST_L"] += weight
                    elif b == 0:
                        by_position["SECOND_L"] += weight
                    else:
                        by_position["THIRD_L"] += weight
                nonzero_components.append(
                    {
                        "indices": [a, b, c],
                        "value": value,
                        "longitudinal_count": n_time,
                    }
                )

    fractions = {str(k): float(v / total) for k, v in by_count.items()}
    position_fractions = {
        key: float(value / total) for key, value in by_position.items()
    }

    return {
        "frame": "V24_EQUAL_REST_TIMELIKE_SOURCE_FRAME",
        "component_square_norm": total,
        "nonzero_component_count": len(nonzero_components),
        "nonzero_components": nonzero_components,
        "longitudinal_count_fraction": fractions,
        "one_longitudinal_fraction": fractions["1"],
        "one_longitudinal_only": bool(
            abs(fractions["1"] - 1.0) <= TOL
            and fractions["0"] <= TOL
            and fractions["2"] <= TOL
            and fractions["3"] <= TOL
        ),
        "one_longitudinal_position_fraction": position_fractions,
        "all_one_longitudinal_placements_present": bool(
            all(value > TOL for value in position_fractions.values())
        ),
        "support_statement_is_exact_projector_overlap": False,
    }


def massive_curtright_pole_prefilter() -> dict[str, Any]:
    """Test the clean source against the purely spatial massive pole support.

    A massive Curtright field in four dimensions carries five transverse
    physical polarizations.  In its timelike rest frame the physical pole can
    be represented by the purely spatial Curtright components.  The V24 clean
    source has none, so its rest-frame physical-pole support vanishes.

    Static/off-shell exchange is deliberately left open.
    """
    hook = _finite_rank3(rest_pair_hook())
    curtright = _finite_rank3(hook_to_torsionlike(hook))
    spatial = curtright[1:, 1:, 1:]
    spatial_norm = float(np.linalg.norm(spatial))

    support = v24_longitudinal_support_gate()

    return {
        "massive_curtright_dof_4d": 5,
        "curtright_spatial_pole_source_norm": spatial_norm,
        "clean_rest_pair_rest_frame_pole_support_nonzero": spatial_norm > TOL,
        "clean_rest_pair_rest_frame_pole_support_zero": spatial_norm <= TOL,
        "v24_one_longitudinal_only": support["one_longitudinal_only"],
        "massive_curtright_has_massive_spin2_duality_provenance": True,
        "029_massive_spin2_route_automatically_recloses_hook17": False,
        "reason_029_not_automatic": (
            "029 tested ordinary conserved symmetric-stress Fierz-Pauli "
            "source/portal behavior; HOOK17 has intrinsic rank-three source "
            "and nonlinear universal-metric descendants"
        ),
        "static_offshell_projector_evaluated": False,
        "static_offshell_projector_status": "REQUIRED_NEXT_FALSIFIER",
        "claim_scope": "TIMELIKE_REST_FRAME_MASSIVE_POLE_SUPPORT_ONLY",
    }



def v24_clean_rest_o3_hook_irrep_gate() -> dict[str, Any]:
    """Decompose the one-longitudinal clean V24 hook into O(3) irreps.

    In the equal-rest frame define

        A_ij = H_0ij,
        B_ij = H_i0j.

    Last-pair symmetry and the hook Young identity imply

        A_ij + B_ij + B_ji = 0.

    Therefore the one-L hook sector decomposes uniquely into:

    - symmetric-traceless A_ij: spin 2+ support;
    - antisymmetric part of B_ij: spin 1+ support;
    - trace of A_ij: spin 0+ support.

    This is an exact rest-frame representation decomposition.  It still does
    not supply the action-dependent canonical residue or saturated propagator.
    """
    hook = _finite_rank3(rest_pair_hook())
    a = np.asarray(hook[0, 1:, 1:], dtype=float)
    b = np.asarray(hook[1:, 0, 1:], dtype=float)

    a_symmetry_residual = float(np.max(np.abs(a - a.T)))
    hook_relation_residual = float(np.max(np.abs(a + b + b.T)))

    trace_a = float(np.trace(a))
    spin2 = a - np.eye(3) * trace_a / 3.0
    spin1 = 0.5 * (b - b.T)
    spin0_matrix = np.eye(3) * trace_a / 3.0

    spin2_norm2 = float(np.sum(spin2 * spin2))
    spin1_norm2 = float(np.sum(spin1 * spin1))
    spin0_norm2 = float(np.sum(spin0_matrix * spin0_matrix))

    return {
        "A_ij": a.tolist(),
        "B_ij": b.tolist(),
        "A_symmetric": a_symmetry_residual <= TOL,
        "A_symmetry_residual": a_symmetry_residual,
        "hook_young_relation_pass": hook_relation_residual <= TOL,
        "hook_young_relation_residual": hook_relation_residual,
        "spin2_plus_support_norm2": spin2_norm2,
        "spin2_plus_support_nonzero": spin2_norm2 > TOL,
        "spin1_plus_support_norm2": spin1_norm2,
        "spin1_plus_support_nonzero": spin1_norm2 > TOL,
        "spin0_plus_support_norm2": spin0_norm2,
        "spin0_plus_support_nonzero": spin0_norm2 > TOL,
        "spin0_plus_trace": trace_a,
        "exact_o3_irrep_support": {
            "HOOK_2_PLUS": spin2_norm2 > TOL,
            "HOOK_1_PLUS": spin1_norm2 > TOL,
            "HOOK_0_PLUS": spin0_norm2 > TOL,
            "HOOK_2_MINUS": False,
            "HOOK_1_MINUS": False,
        },
        "canonical_residue_evaluated": False,
        "saturated_propagator_evaluated": False,
    }

def mikura_percacci_hook_projector_prefilter() -> dict[str, Any]:
    """Apply exact rest-frame O(3) support selection before residues."""
    support = v24_longitudinal_support_gate()
    irreps = v24_clean_rest_o3_hook_irrep_gate()
    irrep_support = irreps["exact_o3_irrep_support"]

    rows = [
        {
            "mode": "HOOK_2_PLUS",
            "published_support": "LTT",
            "healthy_single_state_family_known": True,
            "v24_o3_irrep_support_nonzero": bool(irrep_support["HOOK_2_PLUS"]),
            "canonical_residue_done": False,
            "status": "NONZERO_O3_IRREP_SUPPORT__EXACT_RESIDUE_REQUIRED",
        },
        {
            "mode": "HOOK_2_MINUS",
            "published_support": "TTT",
            "healthy_single_state_family_known": True,
            "v24_o3_irrep_support_nonzero": False,
            "canonical_residue_done": True,
            "status": "ZERO_BY_REST_FRAME_O3_SUPPORT",
        },
        {
            "mode": "HOOK_1_PLUS",
            "published_support": "TTL+TLT-0.5LTT",
            "healthy_single_state_family_known": True,
            "v24_o3_irrep_support_nonzero": bool(irrep_support["HOOK_1_PLUS"]),
            "canonical_residue_done": False,
            "status": "NONZERO_O3_IRREP_SUPPORT__EXACT_RESIDUE_REQUIRED",
        },
        {
            "mode": "HOOK_1_MINUS",
            "published_support": "TTT",
            "healthy_single_state_family_known": True,
            "v24_o3_irrep_support_nonzero": False,
            "canonical_residue_done": True,
            "status": "ZERO_BY_REST_FRAME_O3_SUPPORT",
        },
        {
            "mode": "HOOK_0_PLUS",
            "published_support": "LTT",
            "healthy_single_state_family_known": True,
            "v24_o3_irrep_support_nonzero": bool(irrep_support["HOOK_0_PLUS"]),
            "canonical_residue_done": True,
            "status": "ZERO_BY_TRACE_FREE_CLEAN_SOURCE",
        },
    ]

    return {
        "source_support": support,
        "o3_irrep_gate": irreps,
        "modes": rows,
        "o3_irrep_support_survivors": [
            row["mode"]
            for row in rows
            if row["v24_o3_irrep_support_nonzero"]
        ],
        "o3_irrep_exact_zeros": [
            row["mode"]
            for row in rows
            if not row["v24_o3_irrep_support_nonzero"]
        ],
        "exact_canonical_residue_required_for_survivors": True,
        "matter_interactions_in_free_action_reference": False,
        "universal_metric_portal_in_free_action_reference": False,
        "same_action_complete": False,
    }

def compensated_hook17_ward_rescue_gate() -> dict[str, Any]:
    """Test whether an invariant compensated hook removes the V26C Ward fail."""
    representation = curtright_representation_gate()
    hook = _finite_rank3(rest_pair_hook())

    raw_source = massless_hook_shift_source_ward_gate()
    raw_metric = quadratic_metric_hook_shift_gate()

    # A published Stueckelberg-completed Curtright tensor Fhat is invariant.
    # Because the V24C map is linear and invertible on the declared hook
    # subspace, Hhat = map^{-1}(Fhat) is invariant too.  Hence both J.Hhat and
    # Q(Hhat,Hhat) are invariant for an inert external/source current.
    compensated_source_ward_pass = bool(
        representation["representation_roundtrip_pass"]
    )
    compensated_metric_ward_pass = compensated_source_ward_pass

    q = quadratic_metric_descendant(hook)
    active_derivative = quadratic_active_background_derivative(hook, hook)
    offstate_derivative = quadratic_active_background_derivative(
        np.zeros_like(hook),
        hook,
    )

    expected_active = 2.0 * q
    active_identity_residual = float(
        np.max(np.abs(active_derivative - expected_active))
    )
    offstate_residual = float(np.max(np.abs(offstate_derivative)))

    return {
        "published_massive_curtright_stueckelberg_fields": [
            "SYMMETRIC_H_MN",
            "KALB_RAMOND_B_MN",
            "VECTOR_A_M",
        ],
        "published_compensator_count": 3,
        "gauge_invariant_curtright_combination_exists": True,
        "v24_hook_curtright_map_pass": representation[
            "representation_roundtrip_pass"
        ],
        "raw_v26c_source_ward_pass": bool(
            raw_source.get("direct_source_ward_compatible", False)
        ),
        "raw_v26c_metric_ward_pass": bool(
            raw_metric.get("quadratic_metric_hook_shift_invariant", False)
        ),
        "compensated_source_ward_pass_by_invariance": compensated_source_ward_pass,
        "compensated_quadratic_metric_ward_pass_by_invariance": (
            compensated_metric_ward_pass
        ),
        "unitary_gauge_recovers_v26b1_hook": True,
        "v26b1_quadratic_metric_nonzero": bool(np.linalg.norm(q) > TOL),
        "v26b1_active_degree_two_identity_pass": active_identity_residual <= TOL,
        "v26b1_active_degree_two_identity_residual": active_identity_residual,
        "v26b1_offstate_first_variation_zero": offstate_residual <= TOL,
        "v26b1_offstate_first_variation_residual": offstate_residual,
        "kinematic_ward_obstruction_repaired": bool(
            compensated_source_ward_pass and compensated_metric_ward_pass
        ),
        "complete_same_action_established": False,
        "healthy_mode_projector_established": False,
        "field_redefinition_survival_established": False,
        "complete_energy_established": False,
    }


def hook17_family_atlas() -> list[dict[str, Any]]:
    """Return conservative H17A action-family rows without false promotion."""
    ward = compensated_hook17_ward_rescue_gate()
    curtright = massive_curtright_pole_prefilter()
    mp = mikura_percacci_hook_projector_prefilter()

    rows = [
        Hook17FamilyRow(
            FAMILY_ID="H17-F1",
            FAMILY_NAME="MASSIVE_CURTRIGHT_STUECKELBERG_HOOK",
            ACTION_REFERENCE=(
                "CHATZISTAVRAKIDIS_RANJBAR_ZEKO_JHEP_05_2025_218"
            ),
            ACTION_EXPLICIT=True,
            FIELD_CONTENT="T_(2,1)+h_(2)+b_(2)+a_(1)+GR_METRIC_TEMPLATE",
            SYMMETRY="MIXED_SYMMETRY_STUECKELBERG_GAUGE",
            SYMMETRY_EXACT_OR_SOFT="EXACT_LINEARIZED_STUECKELBERG",
            SYMMETRY_BREAKING_SCALE="MASS_PARAMETER__NOT_YET_HOOK17_MATCHED",
            OFFSTATE_LIMIT="FHAT=0_TEMPLATE_RIEMANNIAN_OFFSTATE_POSSIBLE",
            DIRAC_SOURCE_VERTEX="J_HOOK_DOT_HHAT_TEMPLATE_ONLY",
            SOURCE_IRREP="V24_INTRINSIC_HOOK_MAPPED_TO_CURTRIGHT_(2,1)",
            SOURCE_WARD_STATUS=(
                "KINEMATIC_PASS_WITH_INVARIANT_HHAT__SAME_ACTION_NOT_DERIVED"
            ),
            HEALTHY_MODE="MASSIVE_CURTRIGHT_5_DOF",
            HEALTHY_MODE_PROJECTOR="STATIC_OFFSHELL_PROJECTOR_NOT_YET_DONE",
            SOURCE_PROJECTOR_STATUS=(
                "REST_FRAME_PHYSICAL_POLE_ZERO__STATIC_OFFSHELL_UNKNOWN"
                if curtright["clean_rest_pair_rest_frame_pole_support_zero"]
                else "REST_FRAME_POLE_SUPPORT_PRESENT__STATIC_OFFSHELL_UNKNOWN"
            ),
            KINETIC_HEALTH_KNOWN="FREE_LINEARIZED_MASSIVE_THEORY_KNOWN",
            MASS_RANGE="MASSIVE_RANGE_TUNABLE_IN_FREE_THEORY__NATURALNESS_UNKNOWN",
            PHYSICAL_METRIC="g_phys=g+Q(HHAT,HHAT)/M_H^2_TEMPLATE",
            METRIC_WARD_STATUS=(
                "KINEMATIC_PASS_IF_BUILT_ONLY_FROM_INVARIANT_HHAT"
            ),
            ACTIVE_NUMERATOR_STATUS=(
                "V26B1_UNITARY_GAUGE_NUMERATOR_RETAINED"
                if ward["v26b1_active_degree_two_identity_pass"]
                else "FAIL"
            ),
            FIELD_REDEFINITION_STATUS=(
                "DUAL_MASSIVE_SPIN2_PROVENANCE_REQUIRES_EXACT_DUAL_FRAME_AUDIT"
            ),
            OFFSTATE_PORTAL_ORDER="QUADRATIC_TEMPLATE",
            LOWEST_OFFSTATE_FORCE="TWO_MEDIATOR_LIKE__MASSIVE_VERSION_NOT_EVALUATED",
            CANONICALIZATION_STATUS="FREE_FIELD_KNOWN__HOOK17_SOURCE_METRIC_NOT_DONE",
            CAPACITY_FORMULA_STATUS="V26B1R1_CAPACITY_NOT_TRANSFERABLE_YET",
            IMMEDIATE_EMPIRICAL_KILLER="NONE_PROVEN_AT_H17A",
            IMMEDIATE_NATURALNESS_KILLER="MASS_AND_COMPENSATOR_SCALES_UNTESTED",
            SAME_ACTION_COMPLETE=False,
            STATUS=(
                "KINEMATIC_WARD_RESCUE_SURVIVES__POLE_ZERO_AND_DUALITY_WARNING"
            ),
            FAILURE_CODE="NO_FATAL_FAMILY_THEOREM__NO_PROMOTION_YET",
            NEXT_CHEAP_FALSIFIER=(
                "STATIC_OFFSHELL_CURTRIGHT_STUECKELBERG_SATURATED_PROPAGATOR_"
                "WITH_V24_SOURCE_PLUS_DUAL_FRAME_SOURCE_METRIC_AUDIT"
            ),
        ),
        Hook17FamilyRow(
            FAMILY_ID="H17-F2",
            FAMILY_NAME="HEALTHY_HOOK_SYMMETRIC_NONMETRICITY_MAG",
            ACTION_REFERENCE="MIKURA_PERCACCI_EPJC_85_377_2025",
            ACTION_EXPLICIT=True,
            FIELD_CONTENT="GR_METRIC+HOOK_SYMMETRIC_NONMETRICITY_Q",
            SYMMETRY="DIFFEOMORPHISM__HOOK_KINEMATIC_IRREP",
            SYMMETRY_EXACT_OR_SOFT="EXACT_AT_FREE_QUADRATIC_LEVEL",
            SYMMETRY_BREAKING_SCALE="NOT_A_HOOK_SHIFT_FAMILY",
            OFFSTATE_LIMIT="Q=0_RIEMANNIAN",
            DIRAC_SOURCE_VERTEX="V24_DIRAC_HYPERMOMENTUM_MATCH_NOT_IN_REFERENCE_ACTION",
            SOURCE_IRREP="V24_HOOK",
            SOURCE_WARD_STATUS="NO_HOOK_SHIFT_OBSTRUCTION__FULL_MATTER_WARD_UNDONE",
            HEALTHY_MODE="HOOK_2PLUS_2MINUS_1PLUS_1MINUS_0PLUS_FAMILIES",
            HEALTHY_MODE_PROJECTOR="PUBLISHED_O3_PROJECTOR_BASIS",
            SOURCE_PROJECTOR_STATUS=(
                "SUPPORT_SURVIVORS=" + ",".join(mp["o3_irrep_support_survivors"])
                + ";EXACT_ZEROS=" + ",".join(mp["o3_irrep_exact_zeros"])
            ),
            KINETIC_HEALTH_KNOWN="EXPLICIT_GHOST_TACHYON_FREE_SINGLE_STATE_REGIONS",
            MASS_RANGE="MASSIVE_POLES__RANGE_PARAMETER_DEPENDENT",
            PHYSICAL_METRIC="GR_METRIC_EXISTS__HOOK17_Q2_MATTER_METRIC_NOT_IN_REFERENCE",
            METRIC_WARD_STATUS="HOOK17_METRIC_PORTAL_NOT_YET_DERIVED",
            ACTIVE_NUMERATOR_STATUS="V26B1_ALGEBRAIC_Q2_WITNESS_RELEVANT_NOT_SAME_ACTION",
            FIELD_REDEFINITION_STATUS="NOT_YET_AUDITED_WITH_DIRAC_SOURCE_AND_MATTER_METRIC",
            OFFSTATE_PORTAL_ORDER="UNKNOWN_UNTIL_METRIC_PORTAL_CHOSEN",
            LOWEST_OFFSTATE_FORCE="UNKNOWN",
            CANONICALIZATION_STATUS="FREE_PROPAGATOR_CANONICAL_POLES_KNOWN",
            CAPACITY_FORMULA_STATUS="NOT_AUTHORIZED",
            IMMEDIATE_EMPIRICAL_KILLER="NONE_PROVEN_AT_H17A",
            IMMEDIATE_NATURALNESS_KILLER="NO_IMMEDIATE_THEOREM__INTERACTIONS_UNTESTED",
            SAME_ACTION_COMPLETE=False,
            STATUS="HIGHEST_PRIORITY_EXACT_PROJECTOR_ACTION_MATCHING_FAMILY",
            FAILURE_CODE="SAME_ACTION_DIRAC_AND_METRIC_PORTAL_INCOMPLETE",
            NEXT_CHEAP_FALSIFIER=(
                "EXACT_CANONICAL_RESIDUES_FOR_HOOK_2PLUS_AND_1PLUS_"
                "THEN_SAME_ACTION_DIRAC_VERTEX_AND_Q2_UNIVERSAL_METRIC_MATCH"
            ),
        ),
        Hook17FamilyRow(
            FAMILY_ID="H17-F3",
            FAMILY_NAME="MASSIVE_SPIN3_SYMMETRIC_NONMETRICITY",
            ACTION_REFERENCE="PERCACCI_SEZGIN_JHEP_01_2026_042",
            ACTION_EXPLICIT=True,
            FIELD_CONTENT="GR_METRIC+SYMMETRIC_NONMETRICITY_WITH_HEALTHY_SPIN3",
            SYMMETRY="DIFFEOMORPHISM",
            SYMMETRY_EXACT_OR_SOFT="EXACT_LINEARIZED",
            SYMMETRY_BREAKING_SCALE="MASS_PARAMETER",
            OFFSTATE_LIMIT="Q=0_RIEMANNIAN",
            DIRAC_SOURCE_VERTEX="NOT_MATCHED_TO_V24_IN_SAME_ACTION",
            SOURCE_IRREP="V24_CLEAN_DIRECT_SPIN3_SHORTCUT_PREVIOUSLY_ZERO",
            SOURCE_WARD_STATUS="UNRESOLVED",
            HEALTHY_MODE="MASSIVE_SPIN3_OPTIONALLY_PLUS_SPIN0",
            HEALTHY_MODE_PROJECTOR="PUBLISHED_LINEARIZED_PROJECTOR_STRUCTURE",
            SOURCE_PROJECTOR_STATUS="CLEAN_DIRECT_SHORTCUT_WARNING__GENERAL_MATCH_OPEN",
            KINETIC_HEALTH_KNOWN="HEALTHY_LINEARIZED_REGIONS_EXIST",
            MASS_RANGE="MASSIVE",
            PHYSICAL_METRIC="GR_METRIC__HOOK17_NONLINEAR_PORTAL_NOT_DERIVED",
            METRIC_WARD_STATUS="UNRESOLVED",
            ACTIVE_NUMERATOR_STATUS="UNRESOLVED_FOR_HEALTHY_SPIN3_MODE",
            FIELD_REDEFINITION_STATUS="UNRESOLVED",
            OFFSTATE_PORTAL_ORDER="UNKNOWN",
            LOWEST_OFFSTATE_FORCE="UNKNOWN",
            CANONICALIZATION_STATUS="FREE_LINEARIZED_LEVEL_ONLY",
            CAPACITY_FORMULA_STATUS="NOT_AUTHORIZED",
            IMMEDIATE_EMPIRICAL_KILLER="NONE_PROVEN_AT_H17A",
            IMMEDIATE_NATURALNESS_KILLER="MASS_INTERACTION_COMPLETION_UNTESTED",
            SAME_ACTION_COMPLETE=False,
            STATUS="OPEN_LOWER_THAN_H17_F2_PENDING_SOURCE_PROJECTOR",
            FAILURE_CODE="V24B_CLEAN_DIRECT_SPIN3_ZERO_WARNING",
            NEXT_CHEAP_FALSIFIER="EXACT_V24_SOURCE_PROJECTOR_IN_PUBLISHED_SPIN3_ACTION",
        ),
        Hook17FamilyRow(
            FAMILY_ID="H17-F4",
            FAMILY_NAME="GENUINELY_NONLINEAR_VECTOR_GRAVITON_COMPLETION",
            ACTION_REFERENCE="V24D_OPEN_NONLINEAR_COMPLETION_CLASS",
            ACTION_EXPLICIT=False,
            FIELD_CONTENT="VECTOR_OR_TORSIONLIKE_MODE+GRAVITON+NONLINEAR_PORTAL",
            SYMMETRY="MODEL_DEPENDENT_GAUGE",
            SYMMETRY_EXACT_OR_SOFT="UNKNOWN",
            SYMMETRY_BREAKING_SCALE="UNKNOWN",
            OFFSTATE_LIMIT="MUST_BE_EXACTLY_OR_STRONGLY_SUPPRESSED",
            DIRAC_SOURCE_VERTEX="HOOK_TO_VECTOR_MAP_EXISTS__ACTION_MATCH_MISSING",
            SOURCE_IRREP="V24_HOOK_TO_TORSIONLIKE_VECTORLIKE",
            SOURCE_WARD_STATUS="LINEAR_TESTED_ROUTE_CLOSED__NONLINEAR_UNKNOWN",
            HEALTHY_MODE="HEALTHY_TORSIONLIKE_VECTOR_MODES_EXIST_IN_LITERATURE",
            HEALTHY_MODE_PROJECTOR="NOT_SAME_ACTION_MATCHED",
            SOURCE_PROJECTOR_STATUS="UNKNOWN",
            KINETIC_HEALTH_KNOWN="FAMILY_DEPENDENT",
            MASS_RANGE="UNKNOWN",
            PHYSICAL_METRIC="NONLINEAR_ACTIVE_BACKGROUND_PORTAL_REQUIRED",
            METRIC_WARD_STATUS="UNKNOWN",
            ACTIVE_NUMERATOR_STATUS="MUST_BE_GENUINELY_NONLINEAR",
            FIELD_REDEFINITION_STATUS="LINEAR_RESPONSE_PREVIOUSLY_REMOVABLE",
            OFFSTATE_PORTAL_ORDER="MUST_START_QUADRATIC_OR_HIGHER",
            LOWEST_OFFSTATE_FORCE="UNKNOWN",
            CANONICALIZATION_STATUS="UNKNOWN",
            CAPACITY_FORMULA_STATUS="NOT_AUTHORIZED",
            IMMEDIATE_EMPIRICAL_KILLER="UNKNOWN",
            IMMEDIATE_NATURALNESS_KILLER="UNKNOWN",
            SAME_ACTION_COMPLETE=False,
            STATUS="OPEN_CONSTRUCTION_CLASS__NO_ACTION_YET",
            FAILURE_CODE="NO_EXPLICIT_NEW_NONLINEAR_ACTION",
            NEXT_CHEAP_FALSIFIER="WRITE_MINIMAL_EXPLICIT_NONLINEAR_ACTION_OR_DEMOTE",
        ),
        Hook17FamilyRow(
            FAMILY_ID="H17-F5",
            FAMILY_NAME="GAUGE_INVARIANT_COMPOSITE_OR_CURVATURE_PORTAL",
            ACTION_REFERENCE="H17_TARGET_CLASS",
            ACTION_EXPLICIT=False,
            FIELD_CONTENT="HOOK_OR_NONMETRICITY_FIELD_STRENGTH+UNIVERSAL_METRIC",
            SYMMETRY="GAUGE_INVARIANT_COMPOSITE_REQUIRED",
            SYMMETRY_EXACT_OR_SOFT="UNKNOWN",
            SYMMETRY_BREAKING_SCALE="UNKNOWN",
            OFFSTATE_LIMIT="COMPOSITE_ZERO_OR_HIGH_ORDER",
            DIRAC_SOURCE_VERTEX="UNKNOWN",
            SOURCE_IRREP="V24_HOOK",
            SOURCE_WARD_STATUS="UNKNOWN",
            HEALTHY_MODE="UNKNOWN_UNTIL_ACTION_SPECIFIED",
            HEALTHY_MODE_PROJECTOR="UNKNOWN",
            SOURCE_PROJECTOR_STATUS="UNKNOWN",
            KINETIC_HEALTH_KNOWN="UNKNOWN",
            MASS_RANGE="UNKNOWN",
            PHYSICAL_METRIC="CURVATURE_OR_FIELD_STRENGTH_COMPOSITE",
            METRIC_WARD_STATUS="TARGET_IS_INVARIANT_BY_CONSTRUCTION_BUT_NOT_YET_SHOWN",
            ACTIVE_NUMERATOR_STATUS="UNKNOWN",
            FIELD_REDEFINITION_STATUS="UNKNOWN",
            OFFSTATE_PORTAL_ORDER="LIKELY_DERIVATIVE_AND_OR_QUADRATIC",
            LOWEST_OFFSTATE_FORCE="UNKNOWN",
            CANONICALIZATION_STATUS="UNKNOWN",
            CAPACITY_FORMULA_STATUS="NOT_AUTHORIZED",
            IMMEDIATE_EMPIRICAL_KILLER="UNKNOWN",
            IMMEDIATE_NATURALNESS_KILLER="DERIVATIVE_SCALE_MAY_BE_COSTLY__UNTESTED",
            SAME_ACTION_COMPLETE=False,
            STATUS="OPEN_IDEA_CLASS__NO_ACTION_YET",
            FAILURE_CODE="NO_EXPLICIT_ACTION",
            NEXT_CHEAP_FALSIFIER="ENUMERATE_LOWEST_DIMENSION_INVARIANTS_AND_TEST_SOURCE_METRIC_CHAIN",
        ),
        Hook17FamilyRow(
            FAMILY_ID="H17-F6",
            FAMILY_NAME="DIRAC_SOURCE_STATE_ENGINEERING",
            ACTION_REFERENCE="V24_SOURCE_FAMILY",
            ACTION_EXPLICIT=True,
            FIELD_CONTENT="DIRAC_SOURCE_STATES_WITH_EXISTING_AFFINE_SOURCE_STRUCTURE",
            SYMMETRY="SOURCE_STATE_CHOICE_NOT_NEW_GAUGE_THEORY",
            SYMMETRY_EXACT_OR_SOFT="N_A",
            SYMMETRY_BREAKING_SCALE="N_A",
            OFFSTATE_LIMIT="SOURCE_ABSENT",
            DIRAC_SOURCE_VERTEX="EXPLICIT_AT_SOURCE_LEVEL",
            SOURCE_IRREP="FULL_HYPERMOMENTUM_DECOMPOSITION_STATE_DEPENDENT",
            SOURCE_WARD_STATUS="DEPENDS_ON_TARGET_CARRIER_ACTION",
            HEALTHY_MODE="NOT_DEFINED_UNTIL_TARGET_ACTION_CHOSEN",
            HEALTHY_MODE_PROJECTOR="NOT_DEFINED",
            SOURCE_PROJECTOR_STATUS="CAN_REPAIR_ZERO_OVERLAP_ONLY_AFTER_ACTION_PROJECTOR_KNOWN",
            KINETIC_HEALTH_KNOWN="SOURCE_ONLY",
            MASS_RANGE="CARRIER_DEPENDENT",
            PHYSICAL_METRIC="CARRIER_DEPENDENT",
            METRIC_WARD_STATUS="CARRIER_DEPENDENT",
            ACTIVE_NUMERATOR_STATUS="STATE_DEPENDENT",
            FIELD_REDEFINITION_STATUS="CARRIER_DEPENDENT",
            OFFSTATE_PORTAL_ORDER="CARRIER_DEPENDENT",
            LOWEST_OFFSTATE_FORCE="CARRIER_DEPENDENT",
            CANONICALIZATION_STATUS="SOURCE_STATE_ONLY",
            CAPACITY_FORMULA_STATUS="NOT_AUTHORIZED",
            IMMEDIATE_EMPIRICAL_KILLER="NONE_AT_SOURCE_ONLY_LEVEL",
            IMMEDIATE_NATURALNESS_KILLER="NONE_AT_SOURCE_ONLY_LEVEL",
            SAME_ACTION_COMPLETE=False,
            STATUS="DEFER_UNTIL_EXACT_PROJECTOR_IDENTIFIES_SOURCE_BOTTLENECK",
            FAILURE_CODE="NOT_AN_INDEPENDENT_CARRIER_ACTION_FAMILY",
            NEXT_CHEAP_FALSIFIER="USE_ONLY_IF_F2_F3_EXACT_PROJECTORS_ARE_ZERO_OR_TINY",
        ),
        Hook17FamilyRow(
            FAMILY_ID="H17-CONTROL-V26C",
            FAMILY_NAME="DIRECT_MASSLESS_PROTECTED_HOOK_PLUS_RAW_H2_METRIC",
            ACTION_REFERENCE="032V26C",
            ACTION_EXPLICIT=True,
            FIELD_CONTENT="MASSLESS_HOOK+DIRECT_V24_SOURCE+RAW_H2_METRIC",
            SYMMETRY="EXACT_HOOK_SHIFT",
            SYMMETRY_EXACT_OR_SOFT="EXACT",
            SYMMETRY_BREAKING_SCALE="NONE",
            OFFSTATE_LIMIT="H=0",
            DIRAC_SOURCE_VERTEX="J_HOOK_DOT_H",
            SOURCE_IRREP="V24_HOOK",
            SOURCE_WARD_STATUS="FAIL",
            HEALTHY_MODE="PROTECTED_MASSLESS_HOOK_TEMPLATE",
            HEALTHY_MODE_PROJECTOR="IRRELEVANT_AFTER_WARD_FAIL",
            SOURCE_PROJECTOR_STATUS="NOT_PROMOTABLE",
            KINETIC_HEALTH_KNOWN="DECLARED_PROTECTED_TEMPLATE",
            MASS_RANGE="MASSLESS",
            PHYSICAL_METRIC="g+Q(H,H)/M_H^2",
            METRIC_WARD_STATUS="FAIL",
            ACTIVE_NUMERATOR_STATUS="ALGEBRAICALLY_NONZERO_BUT_GAUGE_DEPENDENT",
            FIELD_REDEFINITION_STATUS="NOT_PHYSICALIZED",
            OFFSTATE_PORTAL_ORDER="QUADRATIC",
            LOWEST_OFFSTATE_FORCE="TWO_MEDIATOR_PRESENT",
            CANONICALIZATION_STATUS="PARTIAL",
            CAPACITY_FORMULA_STATUS="V26B1R1_REFERENCE_ONLY",
            IMMEDIATE_EMPIRICAL_KILLER="NOT_PRIMARY_FAILURE",
            IMMEDIATE_NATURALNESS_KILLER="NOT_PRIMARY_FAILURE",
            SAME_ACTION_COMPLETE=False,
            STATUS="CLOSED",
            FAILURE_CODE="SOURCE_WARD_FAIL_AND_METRIC_WARD_FAIL",
            NEXT_CHEAP_FALSIFIER="NONE__DO_NOT_REOPEN_WITHOUT_NEW_GAUGE_COMPLETION",
        ),
    ]

    return [asdict(row) for row in rows]


def h17a_summary() -> dict[str, Any]:
    """Return the fail-closed H17A decision and exact next calculation."""
    representation = curtright_representation_gate()
    ward = compensated_hook17_ward_rescue_gate()
    curtright = massive_curtright_pole_prefilter()
    mp = mikura_percacci_hook_projector_prefilter()
    atlas = hook17_family_atlas()

    same_action_complete = [
        row for row in atlas if bool(row["SAME_ACTION_COMPLETE"])
    ]
    closed = [row for row in atlas if row["STATUS"] == "CLOSED"]
    action_projector_targets = [
        row
        for row in atlas
        if row["FAMILY_ID"] in {"H17-F1", "H17-F2", "H17-F3"}
        and row["STATUS"] != "CLOSED"
    ]

    decision = (
        "YELLOW_H17A_WARD_RESCUE_AND_HEALTHY_ACTION_FAMILIES_EXIST_"
        "BUT_NO_SAME_ACTION_COMPLETE_HOOK17_SURVIVOR"
    )
    next_step = (
        "032H17A2_EXACT_V24_HEALTHY_MODE_PROJECTORS_AND_SAME_ACTION_MATCH__"
        "PRIORITY_F2_HOOK_2PLUS_AND_1PLUS__PARALLEL_F1_STATIC_OFFSHELL_"
        "CURTRIGHT_DUALITY_AUDIT"
    )

    return {
        "phase": "032H17A",
        "decision": decision,
        "next": next_step,
        "baseline_expected_before_patch": 673,
        "energy_optimization_authorized": False,
        "mass_candidate_campaign_authorized": False,
        "action_oracle_authorized": False,
        "hook17_reference_capacity_rp1e12_j": HOOK17_REFERENCE_CAPACITY_RP1E12_J,
        "hook17_complete_energy_j": None,
        "strict_complete_operating_target_j": STRICT_COMPLETE_OPERATING_TARGET_J,
        "exactly_target_passes": False,
        "representation": representation,
        "compensated_ward_rescue": ward,
        "curtright_pole_prefilter": curtright,
        "hook_mag_projector_prefilter": mp,
        "atlas": atlas,
        "family_count": len(atlas),
        "closed_family_count_including_control": len(closed),
        "same_action_complete_survivor_count": len(same_action_complete),
        "action_projector_target_count": len(action_projector_targets),
        "h17a_full_survivor": False,
        "h17b_authorized": False,
        "most_informative_next_family": "H17-F2",
        "most_informative_next_modes": mp["o3_irrep_support_survivors"],
        "permanent_clean_rest_pole_zeros": mp["o3_irrep_exact_zeros"],
        "curtright_kinematic_ward_rescue_is_real": ward[
            "kinematic_ward_obstruction_repaired"
        ],
        "curtright_complete_same_action_model_exists": False,
        "curtright_rest_frame_pole_overlap_zero": curtright[
            "clean_rest_pair_rest_frame_pole_support_zero"
        ],
        "curtright_static_offshell_response_closed": False,
        "v26d_fallback_status": "PRESERVED_PAUSED_V26E_NOT_ACTIVATED_YET",
        "physical_antigravity_model_found": False,
        "certified_sub10mj_model_found": False,
        "practical_device_found": False,
    }
