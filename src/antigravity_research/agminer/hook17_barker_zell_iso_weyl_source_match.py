"""032H17A7 — Barker-Zell iso-Weyl vector source-match gate.

PURPOSE
-------
Continue HOOK17 theorem-first physicalization after:

    H17A5
        direct clean V24 -> protected K3 1+ closed on Ward compatibility;

    H17A6
        direct J11 and declared minimal algebraic repairs closed;

    H17A6R1
        exact massless single-compensator class closed because the
        compensator returns to the same Ward identity;

    H17A6R2
        direct clean V24 -> Marzo-2022 protected massive 1- pole closed
        because the clean microscopic source has zero 1- support.

IMPORTANT PRIOR CLOSURE
-----------------------
V24B already tested the Barker-Zell 2024 EXTENDED-PROJECTIVE (EP)
pseudoscalar reduced action as a direct universal antigravity bridge.

That declared route is CLOSED.

The V24B implementation explicitly preserved:

    all_extended_projective_or_iso_weyl_models_closed = False.

Therefore this gate does NOT repeat the EP pseudoscalar calculation.

Instead it evaluates the distinct alternative double-vector symmetry
introduced in the same Barker-Zell paper:

    ISO-WEYL (IW).

LITERATURE FAMILY
-----------------
Will Barker and Sebastian Zell,

    "Consistent particle physics in metric-affine gravity
     from extended projective symmetry"

    arXiv:2402.14917.

The paper defines IW symmetry by

    T_mu     -> T_mu + B_mu
    Qhat_mu  -> Qhat_mu + 2 B_mu + C_mu

with

    Q_mu
    That_mu

inert.

The general IW vector block contains schematically

    M_P^2 [
        b1 Q_mu Q^mu
        +
        b2 That_mu That^mu
        +
        b3 That_mu Q^mu
    ]
    +
    alpha Rhat_mn Rhat^mn,

where

    Rhat_mn = partial_[m Q_n]

is the homothetic curvature.

Thus:

    Q_mu
        is the propagating vector;

    That_mu
        is nondynamical;

and, for finite b2,

    That_mu
        =
    -b3 Q_mu / (2 b2)

in vacuum.

The reduced vector theory is Einstein-Proca, or Einstein-Maxwell on the
special surface

    4 b1 b2 = b3^2.

SOURCE QUESTION
---------------
The clean HOOK17 V24 equal-rest particle/antiparticle configuration was
specifically chosen because:

    particle and antiparticle nonmetricity responses ADD;

    particle and antiparticle torsion responses CANCEL.

The V24 nonmetricity source is also exactly trace-free under

    Q^c
        ~
    eta^{ab} Delta^c_ab.

This is precisely the Weyl/dilation vector contraction needed for the
identified IW Q_mu channel.

Therefore the direct clean-pair IW vector block has two candidate source
entries:

    J_Q
        identified with the Weyl/dilation vector source channel;

    J_That
        identified with the axial-torsion source channel.

This gate asks whether either survives.

NONDYNAMICAL MIXING THEOREM
---------------------------
For a vector block with sources

    L
      =
    M_P^2 [
        b1 Q^2
        +
        b2 A^2
        +
        b3 A.Q
    ]
    +
    alpha F(Q)^2
    +
    Q.J_Q
    +
    A.J_A,

where A denotes the nondynamical That field, eliminating A gives an
effective Q source proportional to

    J_Q
      -
    (b3 / (2 b2)) J_A

for finite nonzero b2.

Consequently:

    J_Q = 0
    AND
    J_A = 0

implies

    J_Q_eff = 0

for every finite b3/(2b2).

Mixing cannot create a source from two zero source channels.

This is the central cheap falsifier.

CLAIM BOUNDARY
--------------
A RED result closes only:

    DIRECT CLEAN EQUAL-REST V24 SOURCE

        ->

    IDENTIFIED BARKER-ZELL IW
    Q_mu / That_mu VECTOR BLOCK.

It does NOT close:

- all Barker-Zell theories;
- the already-distinct EP matter sector beyond its existing V24B closure;
- a rederived full same-action V24 Dirac matter sector inside IW;
- generic Dirac states with nonzero axial torsion current;
- source-state engineering;
- a different protected 1+ or 2+ MAG action;
- full Noether-complete matter plus compensator actions;
- nonlinear vector-graviton completions;
- massive spin-3/nonmetricity families;
- V26D.

SAME-ACTION DISCIPLINE
----------------------
The Barker-Zell paper does not contain the complete Wheeler-V24 source plus
the V26B1 HOOK17 quadratic metric numerator in one action.

Therefore even a source representation match would not be a complete
HOOK17 theory.

Conversely, a zero in both identified native IW vector channels is a valid
cheap rejection of this direct source-identification attempt without
pretending to close all possible matter completions.

ENERGY POLICY
-------------
No energy optimization is performed.

The preserved value

    17.0676442196 J

remains only the R_P=1e12 HOOK17 canonical FIELD-CAPACITY reference.

Complete model/device operating energy remains unknown.

H17B remains unauthorized.

CLAIM_CLASSIFICATION
--------------------
THEOREM_FIRST_PUBLISHED_ACTION_VECTOR_SOURCE_PREFILTER
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    lorentz_trace,
    rest_spinup_special_case,
    wheeler_trace_altered_nonmetricity,
)

from .hook17_marzo2022_massive_source_match import (
    clean_v24_hook_parity_gate,
    h17a6r2_summary,
)

from .protected_dirac_metric_bridge import (
    extended_projective_bridge_gate,
)


TOL = 1.0e-12

HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def _clean_rest_spinors() -> tuple[np.ndarray, np.ndarray]:
    """Return the exact V24 equal-rest spin-up particle/antiparticle pair."""

    electron = np.array(
        [
            1.0 + 0j,
            0j,
            0j,
            0j,
        ]
    )

    positron = np.array(
        [
            0j,
            0j,
            0j,
            1.0 + 0j,
        ]
    )

    return (
        electron,
        positron,
    )


def a6r2_provenance_gate() -> dict[str, Any]:
    """Require the exact successful A6R2 starting state."""

    result = h17a6r2_summary()

    passed = bool(
        result[
            "r1_provenance_pass"
        ]
        and
        result[
            "direct_clean_v24_marzo2022_massive_1minus_closed"
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
        "a6r2_decision":
            result[
                "decision"
            ],

        "a6r2_provenance_pass":
            passed,

        "marzo2022_direct_clean_1minus_closed":
            result[
                "direct_clean_v24_marzo2022_massive_1minus_closed"
            ],

        "clean_1plus_survives":
            result[
                "productive_clean_v24_1plus_survives"
            ],

        "clean_2plus_survives":
            result[
                "productive_clean_v24_2plus_survives"
            ],

        "hook17_open":
            not result[
                "hook17_closed"
            ],
    }


def prior_barker_zell_ep_gate() -> dict[str, Any]:
    """Prevent accidental repetition of the completed V24B EP branch."""

    ep = extended_projective_bridge_gate()

    return {
        "prior_theory":
            ep[
                "theory"
            ],

        "ep_pseudoscalar_direct_bridge_already_closed":
            ep[
                "declared_ep_pseudoscalar_direct_antigravity_bridge_closed"
            ],

        "ep_direct_universal_metric_portal_identified":
            ep[
                "direct_universal_neutral_matter_metric_portal_identified"
            ],

        "all_ep_or_iw_models_closed_by_v24b":
            ep[
                "all_extended_projective_or_iso_weyl_models_closed"
            ],

        "iw_was_preserved_by_v24b":
            bool(
                ep[
                    "declared_ep_pseudoscalar_direct_antigravity_bridge_closed"
                ]
                and
                not ep[
                    "all_extended_projective_or_iso_weyl_models_closed"
                ]
            ),

        "repeat_ep_pseudoscalar_authorized":
            False,
    }


def barker_zell_iso_weyl_family_gate() -> dict[str, Any]:
    """Encode only the published IW facts required by this prefilter."""

    return {
        "family":
            "BARKER_ZELL_2024_ISO_WEYL_DOUBLE_VECTOR",

        "reference":
            (
                "W. Barker and S. Zell, "
                "arXiv:2402.14917"
            ),

        "distinct_from_extended_projective_branch":
            True,

        "double_vector_symmetry":
            True,

        "symmetry_name":
            "ISO_WEYL",

        "iw_inert_vectors":
            [
                "Q_MU",
                "T_HAT_MU",
            ],

        "propagating_vector":
            "Q_MU",

        "q_kinetic_operator":
            "HOMOTHETIC_CURVATURE_SQUARED",

        "homothetic_curvature":
            "R_HAT_MN=PARTIAL_[M Q_N]",

        "t_hat_is_nondynamical":
            True,

        "vector_mass_mixing":
            (
                "M_P^2*(b1*Q^2+b2*T_HAT^2+b3*T_HAT.Q)"
            ),

        "finite_b2_vacuum_elimination":
            "T_HAT=-b3*Q/(2*b2)",

        "reduced_vector_theory":
            "EINSTEIN_PROCA_OR_MAXWELL",

        "maxwell_surface":
            "4*b1*b2=b3^2",

        "pure_tensor_parts_propagate_in_iw_vector_block":
            False,

        "symmetry_protected_vector_family_published":
            True,

        "v24_wheeler_matter_source_derived_in_same_iw_action":
            False,

        "v26b1_hook_metric_numerator_derived_in_same_iw_action":
            False,

        "same_action_hook17_complete":
            False,

        "claim_scope":
            "PUBLISHED_IW_VECTOR_ACTION_PROVENANCE_ONLY",
    }


def clean_v24_pair_weyl_trace_gate() -> dict[str, Any]:
    """Compute the clean V24 pair's exact Weyl/dilation trace channel."""

    electron, positron = _clean_rest_spinors()

    q_e = np.asarray(
        wheeler_trace_altered_nonmetricity(
            electron
        ),
        dtype=float,
    )

    q_p = np.asarray(
        wheeler_trace_altered_nonmetricity(
            positron
        ),
        dtype=float,
    )

    q_pair = (
        q_e
        +
        q_p
    )

    trace_e = np.asarray(
        lorentz_trace(
            q_e
        ),
        dtype=float,
    )

    trace_p = np.asarray(
        lorentz_trace(
            q_p
        ),
        dtype=float,
    )

    trace_pair = np.asarray(
        lorentz_trace(
            q_pair
        ),
        dtype=float,
    )

    pair_norm = float(
        np.linalg.norm(
            q_pair
        )
    )

    pair_trace_norm = float(
        np.linalg.norm(
            trace_pair
        )
    )

    return {
        "pair_nonmetricity_tensor_nonzero":
            bool(
                pair_norm
                >
                TOL
            ),

        "pair_nonmetricity_component_norm":
            pair_norm,

        "electron_weyl_trace":
            trace_e.tolist(),

        "positron_weyl_trace":
            trace_p.tolist(),

        "pair_weyl_trace":
            trace_pair.tolist(),

        "electron_weyl_trace_norm":
            float(
                np.linalg.norm(
                    trace_e
                )
            ),

        "positron_weyl_trace_norm":
            float(
                np.linalg.norm(
                    trace_p
                )
            ),

        "pair_weyl_trace_norm":
            pair_trace_norm,

        "electron_weyl_trace_zero":
            bool(
                np.linalg.norm(
                    trace_e
                )
                <=
                TOL
            ),

        "positron_weyl_trace_zero":
            bool(
                np.linalg.norm(
                    trace_p
                )
                <=
                TOL
            ),

        "pair_weyl_trace_zero":
            bool(
                pair_trace_norm
                <=
                TOL
            ),

        "pair_nonmetricity_adds":
            bool(
                np.allclose(
                    q_e,
                    q_p,
                    atol=
                        TOL,
                    rtol=
                        0.0,
                )
                and
                np.allclose(
                    q_pair,
                    2.0
                    *
                    q_e,
                    atol=
                        TOL,
                    rtol=
                        0.0,
                )
            ),

        "identified_iw_q_vector_channel_zero":
            bool(
                pair_trace_norm
                <=
                TOL
            ),

        "trace_norm_is_physical_energy":
            False,
    }


def clean_v24_pair_axial_torsion_gate() -> dict[str, Any]:
    """Use the exact V24 rest-pair torsion cancellation.

    If the full torsion response tensor cancels, every linear irreducible
    contraction of that tensor also cancels, including the axial pseudotrace
    T_hat_mu used in the Barker-Zell IW vector block.
    """

    rest = rest_spinup_special_case()

    full_torsion_zero = bool(
        rest[
            "pair_torsion_response_cancels"
        ]
    )

    opposite_sign = bool(
        rest[
            "equal_amplitude_particle_antiparticle_opposite_torsion_sign"
        ]
    )

    return {
        "particle_antiparticle_torsion_opposite_sign":
            opposite_sign,

        "full_pair_torsion_response_zero":
            full_torsion_zero,

        "axial_torsion_is_linear_irreducible_contraction":
            True,

        "identified_iw_t_hat_channel_zero":
            bool(
                full_torsion_zero
            ),

        "axial_torsion_channel_zero_by_linearity":
            bool(
                full_torsion_zero
            ),

        "generic_dirac_axial_torsion_forced_zero":
            False,

        "clean_pair_torsion_cancellation_is_source_state_specific":
            True,
    }


def iw_nondynamical_mixing_source_theorem() -> dict[str, Any]:
    """Test the complete native IW vector block for the clean V24 pair.

    With source terms

        Q.J_Q + A.J_A

    and finite b2, eliminating nondynamical A gives

        J_Q_eff
            =
        J_Q - (b3/(2b2))*J_A

    up to the common source normalization convention.

    Both source entries vanish for the clean pair, so no finite algebraic
    mixing coefficient can create a nonzero effective Q source.
    """

    family = barker_zell_iso_weyl_family_gate()
    q_gate = clean_v24_pair_weyl_trace_gate()
    a_gate = clean_v24_pair_axial_torsion_gate()

    j_q_zero = bool(
        q_gate[
            "identified_iw_q_vector_channel_zero"
        ]
    )

    j_a_zero = bool(
        a_gate[
            "identified_iw_t_hat_channel_zero"
        ]
    )

    effective_zero = bool(
        j_q_zero
        and
        j_a_zero
    )

    return {
        "propagating_iw_vector":
            family[
                "propagating_vector"
            ],

        "nondynamical_iw_vector":
            "T_HAT_MU",

        "identified_j_q_zero":
            j_q_zero,

        "identified_j_t_hat_zero":
            j_a_zero,

        "finite_b2_effective_source_formula":
            "J_Q_EFF=J_Q-(b3/(2*b2))*J_T_HAT",

        "mixing_can_create_nonzero_source_from_zero_zero":
            False,

        "effective_q_source_zero_for_all_finite_b3_over_b2":
            effective_zero,

        "singular_b2_zero_used_as_gain":
            False,

        "direct_clean_v24_iw_native_vector_block_source_zero":
            effective_zero,

        "algebraic_mixing_coefficients_scanned":
            False,

        "energy_optimization_performed":
            False,
    }


def barker_zell_iw_clean_source_match_gate() -> dict[str, Any]:
    """Return the scoped source-match result."""

    provenance = a6r2_provenance_gate()
    prior_ep = prior_barker_zell_ep_gate()
    family = barker_zell_iso_weyl_family_gate()
    mixing = iw_nondynamical_mixing_source_theorem()

    direct_closed = bool(
        provenance[
            "a6r2_provenance_pass"
        ]
        and
        prior_ep[
            "iw_was_preserved_by_v24b"
        ]
        and
        family[
            "symmetry_protected_vector_family_published"
        ]
        and
        mixing[
            "direct_clean_v24_iw_native_vector_block_source_zero"
        ]
    )

    return {
        "prior_ep_pseudoscalar_repeated":
            False,

        "prior_ep_pseudoscalar_already_closed":
            prior_ep[
                "ep_pseudoscalar_direct_bridge_already_closed"
            ],

        "iw_is_distinct_open_branch_at_start":
            prior_ep[
                "iw_was_preserved_by_v24b"
            ],

        "iw_propagating_vector":
            family[
                "propagating_vector"
            ],

        "clean_pair_q_channel_zero":
            mixing[
                "identified_j_q_zero"
            ],

        "clean_pair_t_hat_channel_zero":
            mixing[
                "identified_j_t_hat_zero"
            ],

        "clean_pair_effective_q_source_after_t_hat_elimination_zero":
            mixing[
                "effective_q_source_zero_for_all_finite_b3_over_b2"
            ],

        "direct_clean_v24_barker_zell_iw_vector_route_closed":
            direct_closed,

        "full_barker_zell_iw_family_closed":
            False,

        "same_action_v24_dirac_iw_completion_closed":
            False,

        "generic_dirac_iw_source_closed":
            False,

        "source_state_engineering_closed":
            False,

        "static_offshell_iw_response_closed":
            False,

        "universal_hook17_metric_response_derived":
            False,

        "claim_scope":
            (
                "DIRECT CLEAN EQUAL-REST V24 SOURCE INTO IDENTIFIED "
                "BARKER-ZELL IW Q_MU/T_HAT_MU VECTOR CHANNELS"
            ),
    }


def generic_dirac_iw_escape_gate() -> dict[str, Any]:
    """Preserve generic Dirac states after the clean-pair source theorem.

    The clean HOOK17 pair deliberately cancels its torsion response.

    Generic Dirac states need not share that particle/antiparticle
    cancellation, so a nonzero axial current feeding T_hat can in principle
    induce the Q vector through b3 mixing.

    No such state is promoted here because it must still be derived from one
    action and pass Ward, support, stability, metric-response and energy
    gates.
    """

    clean = clean_v24_pair_axial_torsion_gate()

    return {
        "clean_pair_torsion_cancellation":
            clean[
                "full_pair_torsion_response_zero"
            ],

        "clean_pair_cancellation_is_generic_dirac_identity":
            False,

        "generic_dirac_axial_source_proved_zero":
            False,

        "generic_dirac_iw_vector_route_closed":
            False,

        "generic_dirac_source_state_engineering_open":
            True,

        "generic_state_same_action_iw_source_derived":
            False,

        "generic_state_ward_compatible":
            False,

        "generic_state_support_energy_established":
            False,

        "generic_state_promoted_to_physical_model":
            False,
    }


def preserved_productive_source_gate() -> dict[str, Any]:
    """Verify that A7 does not erase the useful clean 1+ and 2+ sectors."""

    hook = clean_v24_hook_parity_gate()

    return {
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

        "clean_hook_1minus_support_zero":
            hook[
                "hook_1minus_support_zero"
            ],

        "source_norm_is_physical_energy":
            False,
    }


def source_channel_rows() -> list[dict[str, Any]]:
    """Return the compact A7 source-channel atlas."""

    q_gate = clean_v24_pair_weyl_trace_gate()
    a_gate = clean_v24_pair_axial_torsion_gate()
    mixing = iw_nondynamical_mixing_source_theorem()
    productive = preserved_productive_source_gate()

    return [
        {
            "channel":
                "BARKER_ZELL_IW_Q_MU_WEYL_TRACE",

            "support_nonzero":
                not q_gate[
                    "identified_iw_q_vector_channel_zero"
                ],

            "support_measure":
                q_gate[
                    "pair_weyl_trace_norm"
                ],

            "status":
                "ZERO_CLEAN_PAIR_SOURCE_CHANNEL",
        },
        {
            "channel":
                "BARKER_ZELL_IW_T_HAT_MU_AXIAL_TORSION",

            "support_nonzero":
                not a_gate[
                    "identified_iw_t_hat_channel_zero"
                ],

            "support_measure":
                0.0,

            "status":
                "ZERO_BY_FULL_TORSION_CANCELLATION",
        },
        {
            "channel":
                "BARKER_ZELL_IW_EFFECTIVE_Q_AFTER_T_HAT_ELIMINATION",

            "support_nonzero":
                not mixing[
                    "effective_q_source_zero_for_all_finite_b3_over_b2"
                ],

            "support_measure":
                0.0,

            "status":
                "ZERO_FOR_ALL_FINITE_NATIVE_VECTOR_MIXING",
        },
        {
            "channel":
                "CLEAN_V24_HOOK_1_PLUS",

            "support_nonzero":
                productive[
                    "clean_hook_1plus_support_nonzero"
                ],

            "support_measure":
                productive[
                    "clean_hook_1plus_norm2"
                ],

            "status":
                "NONZERO_PRESERVED",
        },
        {
            "channel":
                "CLEAN_V24_HOOK_2_PLUS",

            "support_nonzero":
                productive[
                    "clean_hook_2plus_support_nonzero"
                ],

            "support_measure":
                productive[
                    "clean_hook_2plus_norm2"
                ],

            "status":
                "NONZERO_PRESERVED",
        },
    ]


def post_iso_weyl_rerank() -> list[dict[str, Any]]:
    """Return the rescue order after the Barker-Zell IW prefilter."""

    return [
        {
            "priority":
                1,

            "family":
                "NATIVE_PROTECTED_MAG_2PLUS",

            "status":
                "OPEN_HIGHEST_PRIORITY",

            "reason":
                (
                    "CLEAN V24 HAS EXACT NONZERO 2+ SUPPORT AND THE "
                    "PROTECTED 2+ ACTION/WARD INTERSECTION HAS NOT "
                    "BEEN GLOBALLY CLOSED"
                ),
        },
        {
            "priority":
                2,

            "family":
                "OTHER_NATIVE_PROTECTED_MAG_1PLUS",

            "status":
                "OPEN_EXCLUDING_CLOSED_K3_J11_DIRECT_ROUTES",

            "reason":
                (
                    "CLEAN V24 1+ SUPPORT IS NONZERO; K3/J11 DIRECT "
                    "WARD FAILURES DO NOT CLOSE ALL PROTECTED 1+ ACTIONS"
                ),
        },
        {
            "priority":
                3,

            "family":
                "FULL_NOETHER_COMPLETE_MATTER_PLUS_COMPENSATOR",

            "status":
                "OPEN_EXPLICIT_ACTION_REQUIRED",

            "reason":
                (
                    "R1 CLOSED THE SIMPLE MASSLESS COMPENSATOR CLASS, "
                    "NOT ADDITIONAL SAME-ACTION MATTER CURRENTS"
                ),
        },
        {
            "priority":
                4,

            "family":
                "MARZO2026_GENUINELY_NONLINEAR_VECTOR_GRAVITON",

            "status":
                "OPEN_NONLINEAR_ONLY",

            "reason":
                (
                    "THE TESTED LINEAR VECTOR-METRIC BRIDGE IS CLOSED; "
                    "ONLY A GENUINELY NONLINEAR COMPLETION MAY DIFFER"
                ),
        },
        {
            "priority":
                5,

            "family":
                "DIRAC_SOURCE_STATE_ENGINEERING",

            "status":
                "OPEN_AFTER_NATIVE_ACTION_MATCH",

            "reason":
                (
                    "GENERIC DIRAC AXIAL/TENSOR STATES ARE NOT CLOSED, "
                    "BUT SHOULD NOT BE OPTIMIZED BEFORE AN ACTION NEEDS THEM"
                ),
        },
        {
            "priority":
                6,

            "family":
                "MASSIVE_SPIN3_OR_NONMETRICITY",

            "status":
                "OPEN_LOWER_PRIORITY",

            "reason":
                (
                    "REQUIRES EXACT HEALTHY SOURCE PROJECTOR AND "
                    "STATIC OFFSHELL RESPONSE BEFORE ENERGY WORK"
                ),
        },
        {
            "priority":
                7,

            "family":
                "V26D_PROTECTED_CT1_DHOST_KMM",

            "status":
                "PRESERVED_INDEPENDENT_FALLBACK",

            "reason":
                (
                    "RESUME IF HOOK17 SAME-ACTION MAG RESCUE FAMILIES "
                    "FAIL THEIR PHYSICAL GATES"
                ),
        },
    ]


def h17a7_summary() -> dict[str, Any]:
    """Return the conservative H17A7 decision."""

    provenance = a6r2_provenance_gate()
    prior_ep = prior_barker_zell_ep_gate()
    family = barker_zell_iso_weyl_family_gate()
    source_match = barker_zell_iw_clean_source_match_gate()
    generic = generic_dirac_iw_escape_gate()
    productive = preserved_productive_source_gate()

    direct_closed = bool(
        provenance[
            "a6r2_provenance_pass"
        ]
        and
        prior_ep[
            "iw_was_preserved_by_v24b"
        ]
        and
        source_match[
            "direct_clean_v24_barker_zell_iw_vector_route_closed"
        ]
    )

    return {
        "branch":
            "032H17A7",

        "subgate":
            "BARKER_ZELL_ISO_WEYL_VECTOR_SOURCE_MATCH",

        "decision":
            (
                "RED_SCOPED_A7_DIRECT_CLEAN_V24_IDENTIFIED_"
                "Q_AND_T_HAT_CHANNELS_ZERO_FOR_BARKER_ZELL_IW__"
                "FULL_SAME_ACTION_IW_AND_NATIVE_1PLUS_2PLUS_REMAIN_OPEN"
            )
            if direct_closed
            else
            "CHECK_A7_SOURCE_MAPPING_OR_PROVENANCE",

        "a6r2_provenance_pass":
            provenance[
                "a6r2_provenance_pass"
            ],

        "prior_ep_pseudoscalar_already_closed":
            prior_ep[
                "ep_pseudoscalar_direct_bridge_already_closed"
            ],

        "prior_ep_not_repeated":
            True,

        "iw_distinct_branch_preserved_by_v24b":
            prior_ep[
                "iw_was_preserved_by_v24b"
            ],

        "barker_zell_iw_published_vector_family_exists":
            family[
                "symmetry_protected_vector_family_published"
            ],

        "iw_propagating_vector":
            family[
                "propagating_vector"
            ],

        "iw_reduced_vector_theory":
            family[
                "reduced_vector_theory"
            ],

        "clean_pair_iw_q_channel_zero":
            source_match[
                "clean_pair_q_channel_zero"
            ],

        "clean_pair_iw_t_hat_channel_zero":
            source_match[
                "clean_pair_t_hat_channel_zero"
            ],

        "clean_pair_iw_effective_q_source_zero":
            source_match[
                "clean_pair_effective_q_source_after_t_hat_elimination_zero"
            ],

        "direct_clean_v24_barker_zell_iw_vector_route_closed":
            direct_closed,

        "full_barker_zell_iw_family_closed":
            False,

        "same_action_v24_dirac_iw_completion_closed":
            False,

        "generic_dirac_iw_route_closed":
            generic[
                "generic_dirac_iw_vector_route_closed"
            ],

        "generic_dirac_source_state_engineering_open":
            generic[
                "generic_dirac_source_state_engineering_open"
            ],

        "productive_clean_v24_1plus_survives":
            productive[
                "clean_hook_1plus_support_nonzero"
            ],

        "productive_clean_v24_1plus_norm2":
            productive[
                "clean_hook_1plus_norm2"
            ],

        "productive_clean_v24_2plus_survives":
            productive[
                "clean_hook_2plus_support_nonzero"
            ],

        "productive_clean_v24_2plus_norm2":
            productive[
                "clean_hook_2plus_norm2"
            ],

        "full_noether_complete_matter_compensator_closed":
            False,

        "other_protected_1plus_closed":
            False,

        "protected_2plus_closed":
            False,

        "marzo2026_nonlinear_vector_graviton_closed":
            False,

        "massive_spin3_nonmetricity_closed":
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
            "032H17A8_NATIVE_PROTECTED_2PLUS_ACTION_SOURCE_WARD_ATLAS",

        "next_scientific_question":
            (
                "Which symmetry-protected MAG action with a genuine healthy "
                "2+ carrier has a nonzero exact V24 source projector, a "
                "compatible source Ward identity, and a nonremovable path "
                "to one universal physical metric?"
            ),

        "rerank":
            post_iso_weyl_rerank(),

        "claim_scope":
            (
                "DIRECT CLEAN EQUAL-REST V24 SOURCE INTO THE IDENTIFIED "
                "BARKER-ZELL ISO-WEYL Q_MU/T_HAT_MU VECTOR BLOCK ONLY"
            ),
    }
