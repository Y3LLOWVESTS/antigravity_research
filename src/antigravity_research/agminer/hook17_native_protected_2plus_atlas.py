"""032H17A8 — native protected 2+ action / projective rerank atlas.

PURPOSE
-------
Continue the HOOK17 theorem-first rescue sequence after A7.

A7 closed the direct clean V24 source into the identified Barker-Zell
iso-Weyl vector block because:

    J_Q = 0
    J_T_HAT = 0

for the clean equal-rest particle/antiparticle source.

However, A7 preserved exact nonzero microscopic support in:

    hook 1+
    hook 2+.

The next question proposed by A7 was whether a symmetry-protected MAG action
with a genuine healthy 2+ carrier exists and accepts the V24 source.

LITERATURE RESULT 1
-------------------
Barker, Marzo and Santoni,
arXiv:2507.05349,

perform a symmetry-first classification of the general linear,
parity-conserving, pair-antisymmetric rank-three field on Minkowski space.

They identify:

    206 symmetry-defined candidate IR foundations

and fully establish unitarity for:

    22 models.

For that assessed unitary set they state that they find no symmetry which
supports the tuning required for propagating spin-zero or spin-two torsion.

The successful protected particles are vectors.

Therefore:

    BMS PAIR-ANTISYMMETRIC PROTECTED 2+
    =
    CLOSED WITHIN THE DECLARED CATALOGUE SCOPE.

This does not imply that all protected 2+ MAG theories are impossible.

LITERATURE RESULT 2
-------------------
Mikura and Percacci,
"Some simple theories of gravity with propagating nonmetricity",
arXiv:2401.10097,
EPJC 85, 377 (2025),

construct healthy symmetric-MAG single-state theories.

In the hook-symmetric sector a healthy massive 2+ state exists.

The published 2+ branch has, among its conditions,

    m1_QQ < 0
    b6_QQ < 0,

and the single-state parameter relations are fixed so that the unwanted
states do not propagate.

Critically, the analysis explicitly assumes that diffeomorphism is the only
gauge symmetry.

Thus:

    HEALTHY 2+
    =
    YES

but:

    ADDITIONAL GAUGE PROTECTION OF THE REQUIRED TUNING
    =
    NOT ESTABLISHED.

Under the HOOK17 protection rule this is not yet an acceptable protected
carrier.

LITERATURE RESULT 3
-------------------
Percacci and Sezgin,
"A New Class of Ghost and Tachyon Free Metric Affine Gravities",
arXiv:1912.01023,
Phys. Rev. D 101, 084040,

derive a projective-invariant torsion-free MAG class.

Projective invariance imposes source constraints of the form

    tau^nu_{ nu mu} = 0
    tau_{mu nu}^nu = 0.

Their six-parameter ghost/tachyon-free subclass is deliberately chosen so
that:

    spin 3 does not propagate

and:

    in 2+ only the massless graviton propagates.

The additional massive physical sectors include:

    2-
    1+
    1-.

Hence this family is not a protected extra 2+ rescue.

But it IS a concrete symmetry-protected 1+ family.

A8 therefore also tests whether the actual clean V24 source satisfies the
two projective source-trace constraints.

If it does, the projective 1+ family becomes a high-value A9 source-projector
target.

CLAIM BOUNDARY
--------------
A8 may close:

- protected 2+ inside the assessed BMS pair-antisymmetric symmetry catalogue;
- Mikura-Percacci 2+ as a currently UNPROTECTED HOOK17 realization;
- direct clean V24 use of the Percacci-Sezgin additional 2- pole if the
  existing V24 2- projector remains exactly zero.

A8 does NOT close:

- all possible protected 2+ theories;
- parity-violating theories;
- unknown nonlinear completions;
- projective protected 1+;
- other protected vector families;
- massive spin-3/nonmetricity;
- nonlinear vector-graviton models;
- full Noether-complete matter sectors;
- V26D.

ENERGY POLICY
-------------
No capacity optimization is performed.

17.0676442196 J remains only the preserved HOOK17 canonical field-capacity
reference at R_P=1e12.

Complete operating energy remains unknown.

H17B remains unauthorized.

CLAIM_CLASSIFICATION
--------------------
THEOREM_FIRST_LITERATURE_PROTECTION_AND_SOURCE_WARD_ATLAS
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    lower_first_index,
    wheeler_trace_altered_nonmetricity,
)

from .hook17_barker_zell_iso_weyl_source_match import (
    h17a7_summary,
)

from .hook17_marzo2022_massive_source_match import (
    clean_v24_hook_parity_gate,
)


ETA = np.diag(
    [
        -1.0,
        1.0,
        1.0,
        1.0,
    ]
)

TOL = 1.0e-12

HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def a7_provenance_gate() -> dict[str, Any]:
    """Require the exact successful A7 starting state."""

    result = h17a7_summary()

    passed = bool(
        result[
            "a6r2_provenance_pass"
        ]
        and
        result[
            "direct_clean_v24_barker_zell_iw_vector_route_closed"
        ]
        and
        result[
            "productive_clean_v24_1plus_survives"
        ]
        and
        result[
            "productive_clean_v24_2plus_survives"
        ]
        and
        not result[
            "hook17_closed"
        ]
    )

    return {
        "a7_decision":
            result[
                "decision"
            ],

        "a7_provenance_pass":
            passed,

        "iw_direct_clean_route_closed":
            result[
                "direct_clean_v24_barker_zell_iw_vector_route_closed"
            ],

        "clean_1plus_survives":
            result[
                "productive_clean_v24_1plus_survives"
            ],

        "clean_1plus_norm2":
            result[
                "productive_clean_v24_1plus_norm2"
            ],

        "clean_2plus_survives":
            result[
                "productive_clean_v24_2plus_survives"
            ],

        "clean_2plus_norm2":
            result[
                "productive_clean_v24_2plus_norm2"
            ],

        "hook17_open":
            not result[
                "hook17_closed"
            ],
    }


def bms_pair_antisymmetric_spin2_protection_gate() -> dict[str, Any]:
    """Encode the scoped BMS symmetry-first spin-two result."""

    return {
        "family":
            "BMS_2025_PAIR_ANTISYMMETRIC_SYMMETRY_CATALOGUE",

        "reference":
            (
                "Barker, Marzo, Santoni, "
                "arXiv:2507.05349"
            ),

        "field":
            "K_ALPHA_BETA_CHI_PAIR_ANTISYMMETRIC",

        "linear":
            True,

        "parity_conserving":
            True,

        "minkowski_background":
            True,

        "symmetry_first":
            True,

        "candidate_symmetric_ir_foundations":
            206,

        "confirmed_unitary_models":
            22,

        "confirmed_unitary_modes_vector_only":
            True,

        "symmetry_supporting_spin_zero_found":
            False,

        "symmetry_supporting_spin_two_found":
            False,

        "protected_2plus_survivor_in_assessed_catalogue":
            False,

        "protected_2minus_survivor_in_assessed_catalogue":
            False,

        "all_possible_protected_spin2_globally_closed":
            False,

        "parity_violating_extensions_closed":
            False,

        "nonlinear_completions_closed":
            False,

        "claim_scope":
            (
                "ASSESSED UNITARY SYMMETRY-DEFINED LINEAR "
                "PARITY-CONSERVING PAIR-ANTISYMMETRIC CATALOGUE"
            ),
    }


def mikura_percacci_hook_2plus_gate() -> dict[str, Any]:
    """Classify the healthy but not symmetry-protected hook 2+ branch."""

    return {
        "family":
            "MIKURA_PERCACCI_2025_HOOK_SYMMETRIC_NONMETRICITY_2PLUS",

        "reference":
            (
                "Mikura and Percacci, "
                "arXiv:2401.10097"
            ),

        "explicit_symmetric_mag_action":
            True,

        "hook_symmetric_nonmetricity":
            True,

        "healthy_massive_2plus_exists":
            True,

        "single_state_2plus_parameter_relations_required":
            True,

        "published_ghost_free_condition_m1qq_negative":
            True,

        "published_ghost_free_condition_b6qq_negative":
            True,

        "analysis_assumes_only_diffeomorphism_gauge_symmetry":
            True,

        "additional_gauge_symmetry_protects_2plus_tuning":
            False,

        "radiative_protection_of_single_state_tuning_established":
            False,

        "hook17_protection_gate_pass":
            False,

        "exact_v24_projector_needed_before_protection":
            False,

        "energy_scan_authorized":
            False,

        "status":
            "HEALTHY_BUT_UNPROTECTED",

        "claim_scope":
            (
                "PUBLISHED SINGLE-STATE HOOK-SYMMETRIC "
                "NONMETRICITY 2PLUS BRANCH"
            ),
    }


def percacci_sezgin_projective_family_gate() -> dict[str, Any]:
    """Encode the projective-invariant torsion-free MAG branch."""

    return {
        "family":
            "PERCACCI_SEZGIN_PROJECTIVE_TORSION_FREE_MAG",

        "reference":
            (
                "Percacci and Sezgin, "
                "arXiv:1912.01023"
            ),

        "torsion_free":
            True,

        "projective_invariance":
            True,

        "source_trace_constraints_published":
            True,

        "source_constraint_1":
            "TAU^NU_{NU MU}=0",

        "source_constraint_2":
            "TAU_{MU NU}^NU=0",

        "ghost_tachyon_free_subclass_exists":
            True,

        "spin3_propagates_in_selected_subclass":
            False,

        "massive_2plus_propagates":
            False,

        "massless_graviton_2plus_propagates":
            True,

        "massive_2minus_propagates":
            True,

        "massive_1plus_propagates":
            True,

        "massive_1minus_propagates":
            True,

        "protected_extra_2plus_candidate":
            False,

        "protected_1plus_candidate":
            True,

        "same_action_v24_source_derived":
            False,

        "hook17_metric_numerator_derived":
            False,

        "claim_scope":
            (
                "PROJECTIVE-INVARIANT TORSION-FREE "
                "GHOST/TACHYON-FREE SUBCLASS"
            ),
    }


def _clean_rest_pair_nonmetricity_cov() -> np.ndarray:
    """Return the fully covariant clean V24 rest-pair nonmetricity source."""

    electron = np.array(
        [
            1.0 + 0j,
            0j,
            0j,
            0j,
        ],
        dtype=np.complex128,
    )

    positron = np.array(
        [
            0j,
            0j,
            0j,
            1.0 + 0j,
        ],
        dtype=np.complex128,
    )

    q_up = (
        wheeler_trace_altered_nonmetricity(
            electron
        )
        +
        wheeler_trace_altered_nonmetricity(
            positron
        )
    )

    q_cov = lower_first_index(
        q_up
    )

    value = np.real_if_close(
        q_cov
    )

    if np.iscomplexobj(
        value
    ):
        raise ValueError(
            "clean V24 source did not reduce to a real tensor"
        )

    result = np.asarray(
        value,
        dtype=float,
    )

    if result.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "clean V24 source must be rank three"
        )

    return result


def clean_v24_projective_trace_gate() -> dict[str, Any]:
    """Test the two published projective source-trace constraints.

    With all source indices lowered, the two constraints correspond to the
    Lorentz contractions over:

        first-second indices

    and:

        second-third indices.

    Zero is insensitive to the conventional placement of the remaining
    free index.
    """

    source = _clean_rest_pair_nonmetricity_cov()

    trace_12 = np.einsum(
        "ab,abc->c",
        ETA,
        source,
    )

    trace_23 = np.einsum(
        "bc,abc->a",
        ETA,
        source,
    )

    trace_12_norm = float(
        np.linalg.norm(
            trace_12
        )
    )

    trace_23_norm = float(
        np.linalg.norm(
            trace_23
        )
    )

    source_norm = float(
        np.linalg.norm(
            source
        )
    )

    constraint_1 = bool(
        trace_12_norm
        <=
        TOL
        *
        max(
            source_norm,
            1.0,
        )
    )

    constraint_2 = bool(
        trace_23_norm
        <=
        TOL
        *
        max(
            source_norm,
            1.0,
        )
    )

    return {
        "source_component_norm":
            source_norm,

        "source_nonzero":
            bool(
                source_norm
                >
                TOL
            ),

        "trace_first_second":
            trace_12.tolist(),

        "trace_first_second_norm":
            trace_12_norm,

        "trace_second_third":
            trace_23.tolist(),

        "trace_second_third_norm":
            trace_23_norm,

        "projective_constraint_tau_nu_nu_mu_pass":
            constraint_1,

        "projective_constraint_tau_mu_nu_nu_pass":
            constraint_2,

        "both_projective_source_trace_constraints_pass":
            bool(
                constraint_1
                and
                constraint_2
            ),

        "exact_projective_1plus_pole_projector_evaluated":
            False,

        "projective_1plus_source_nonzero_established":
            False,

        "same_action_matter_completion_established":
            False,

        "component_norm_is_physical_energy":
            False,
    }


def clean_v24_projective_spin_rerank_gate() -> dict[str, Any]:
    """Combine projective Ward prefilter with existing exact V24 irreps."""

    projective = (
        clean_v24_projective_trace_gate()
    )

    hook = (
        clean_v24_hook_parity_gate()
    )

    return {
        "projective_source_trace_constraints_pass":
            projective[
                "both_projective_source_trace_constraints_pass"
            ],

        "clean_hook_2minus_support_zero":
            hook[
                "hook_2minus_support_zero"
            ],

        "clean_hook_1minus_support_zero":
            hook[
                "hook_1minus_support_zero"
            ],

        "clean_hook_1plus_support_nonzero":
            hook[
                "hook_1plus_support_nonzero"
            ],

        "clean_hook_1plus_norm2":
            hook[
                "hook_1plus_norm2"
            ],

        "clean_hook_2plus_support_nonzero":
            hook[
                "hook_2plus_support_nonzero"
            ],

        "clean_hook_2plus_norm2":
            hook[
                "hook_2plus_norm2"
            ],

        "direct_clean_v24_projective_2minus_route_supported":
            bool(
                not hook[
                    "hook_2minus_support_zero"
                ]
            ),

        "projective_1plus_exact_source_match_authorized":
            bool(
                projective[
                    "both_projective_source_trace_constraints_pass"
                ]
                and
                hook[
                    "hook_1plus_support_nonzero"
                ]
            ),

        "projective_1plus_already_certified":
            False,
    }


def protected_2plus_atlas_rows() -> list[dict[str, Any]]:
    """Return the current protected 2+ action-family atlas."""

    bms = (
        bms_pair_antisymmetric_spin2_protection_gate()
    )

    mp = (
        mikura_percacci_hook_2plus_gate()
    )

    ps = (
        percacci_sezgin_projective_family_gate()
    )

    rerank = (
        clean_v24_projective_spin_rerank_gate()
    )

    return [
        {
            "family":
                "BMS_PAIR_ANTISYMMETRIC",

            "healthy_2plus":
                False,

            "symmetry_protected":
                True,

            "clean_v24_2plus_available":
                True,

            "protected_2plus_survivor":
                False,

            "status":
                "RED_SCOPED_NO_SYMMETRY_SUPPORTED_SPIN2",
        },
        {
            "family":
                "MIKURA_PERCACCI_HOOK_NONMETRICITY",

            "healthy_2plus":
                mp[
                    "healthy_massive_2plus_exists"
                ],

            "symmetry_protected":
                mp[
                    "additional_gauge_symmetry_protects_2plus_tuning"
                ],

            "clean_v24_2plus_available":
                True,

            "protected_2plus_survivor":
                False,

            "status":
                "BLOCKED_UNPROTECTED_TUNING",
        },
        {
            "family":
                "PERCACCI_SEZGIN_PROJECTIVE_MAG",

            "healthy_2plus":
                ps[
                    "massless_graviton_2plus_propagates"
                ],

            "symmetry_protected":
                ps[
                    "projective_invariance"
                ],

            "clean_v24_2plus_available":
                True,

            "protected_2plus_survivor":
                False,

            "status":
                "NO_EXTRA_MASSIVE_2PLUS_IN_SELECTED_HEALTHY_CLASS",
        },
        {
            "family":
                "PERCACCI_SEZGIN_PROJECTIVE_1PLUS_RERANK",

            "healthy_2plus":
                False,

            "symmetry_protected":
                True,

            "clean_v24_2plus_available":
                False,

            "protected_2plus_survivor":
                False,

            "status":
                (
                    "PROMOTE_1PLUS_EXACT_SOURCE_GATE"
                    if rerank[
                        "projective_1plus_exact_source_match_authorized"
                    ]
                    else
                    "PROJECTIVE_SOURCE_PREFILTER_FAILED"
                ),
        },
    ]


def h17a8_summary() -> dict[str, Any]:
    """Return the conservative A8 decision."""

    provenance = (
        a7_provenance_gate()
    )

    bms = (
        bms_pair_antisymmetric_spin2_protection_gate()
    )

    mp = (
        mikura_percacci_hook_2plus_gate()
    )

    ps = (
        percacci_sezgin_projective_family_gate()
    )

    projective = (
        clean_v24_projective_spin_rerank_gate()
    )

    rows = protected_2plus_atlas_rows()

    protected_2plus_survivors = [
        row
        for row in rows
        if row[
            "protected_2plus_survivor"
        ]
    ]

    current_atlas_closed = bool(
        provenance[
            "a7_provenance_pass"
        ]
        and
        not bms[
            "protected_2plus_survivor_in_assessed_catalogue"
        ]
        and
        not mp[
            "hook17_protection_gate_pass"
        ]
        and
        not ps[
            "protected_extra_2plus_candidate"
        ]
        and
        len(
            protected_2plus_survivors
        )
        ==
        0
    )

    projective_1plus_promoted = bool(
        ps[
            "protected_1plus_candidate"
        ]
        and
        projective[
            "projective_1plus_exact_source_match_authorized"
        ]
    )

    return {
        "branch":
            "032H17A8",

        "subgate":
            "NATIVE_PROTECTED_2PLUS_ACTION_SOURCE_WARD_ATLAS",

        "decision":
            (
                "RED_SCOPED_A8_CURRENT_PROTECTED_2PLUS_ATLAS_"
                "HAS_ZERO_ACCEPTABLE_SURVIVORS__"
                "PERCACCI_SEZGIN_PROJECTIVE_1PLUS_PROMOTED"
            )
            if (
                current_atlas_closed
                and
                projective_1plus_promoted
            )
            else
            "CHECK_A8_PROTECTION_OR_PROJECTIVE_SOURCE_PREFILTER",

        "a7_provenance_pass":
            provenance[
                "a7_provenance_pass"
            ],

        "clean_v24_2plus_source_survives":
            provenance[
                "clean_2plus_survives"
            ],

        "clean_v24_2plus_norm2":
            provenance[
                "clean_2plus_norm2"
            ],

        "clean_v24_1plus_source_survives":
            provenance[
                "clean_1plus_survives"
            ],

        "clean_v24_1plus_norm2":
            provenance[
                "clean_1plus_norm2"
            ],

        "bms_assessed_protected_spin2_survivor":
            bms[
                "protected_2plus_survivor_in_assessed_catalogue"
            ],

        "mikura_percacci_healthy_2plus_exists":
            mp[
                "healthy_massive_2plus_exists"
            ],

        "mikura_percacci_2plus_protection_established":
            mp[
                "hook17_protection_gate_pass"
            ],

        "percacci_sezgin_projective_family_exists":
            ps[
                "projective_invariance"
            ],

        "percacci_sezgin_extra_massive_2plus_exists":
            ps[
                "massive_2plus_propagates"
            ],

        "percacci_sezgin_protected_1plus_exists":
            ps[
                "protected_1plus_candidate"
            ],

        "clean_v24_projective_source_trace_constraints_pass":
            projective[
                "projective_source_trace_constraints_pass"
            ],

        "clean_v24_projective_2minus_support_zero":
            projective[
                "clean_hook_2minus_support_zero"
            ],

        "clean_v24_projective_1plus_support_nonzero":
            projective[
                "clean_hook_1plus_support_nonzero"
            ],

        "projective_1plus_exact_source_match_authorized":
            projective[
                "projective_1plus_exact_source_match_authorized"
            ],

        "projective_1plus_exact_pole_overlap_established":
            False,

        "current_declared_protected_2plus_atlas_survivor_count":
            len(
                protected_2plus_survivors
            ),

        "current_declared_protected_2plus_atlas_closed":
            current_atlas_closed,

        "all_possible_protected_2plus_globally_closed":
            False,

        "healthy_unprotected_2plus_exists":
            mp[
                "healthy_massive_2plus_exists"
            ],

        "protection_is_current_2plus_bottleneck":
            True,

        "other_protected_1plus_closed":
            False,

        "full_noether_complete_matter_compensator_closed":
            False,

        "massive_spin3_nonmetricity_closed":
            False,

        "marzo2026_nonlinear_vector_graviton_closed":
            False,

        "hook17_closed":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_complete_energy_j":
            None,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "capacity_recalculation_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "sub100j_capacity_tuning_authorized":
            False,

        "h17b_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "v26d_fallback_status":
            "PRESERVED",

        "v26e_status":
            "PAUSED_NOT_CLOSED",

        "next":
            (
                "032H17A9_PERCACCI_SEZGIN_PROJECTIVE_"
                "1PLUS_EXACT_SOURCE_PROJECTOR_WARD_GATE"
            ),

        "next_scientific_question":
            (
                "Given that the clean V24 source satisfies both published "
                "projective source-trace constraints and has nonzero 1+ "
                "support, does it have nonzero residue on the actual "
                "healthy projective 1+ pole of the Percacci-Sezgin action?"
            ),

        "atlas":
            rows,

        "claim_scope":
            (
                "CURRENT DECLARED PROTECTED 2PLUS LITERATURE ATLAS; "
                "NOT A GLOBAL NO-GO FOR ALL MAG"
            ),
    }
