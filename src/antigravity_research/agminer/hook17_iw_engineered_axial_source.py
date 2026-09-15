"""032H17A12A — engineered Dirac source into Barker-Zell iso-Weyl vector.

PURPOSE
-------
Revisit the A7 Barker-Zell iso-Weyl (IW) vector family only because later
A10/A11 work supplied the missing ingredient that A7 explicitly left open:
a general Wheeler torsion source for spin-engineered Dirac rest states.

This is a theorem-first source/protection gate.

It does not:
- build a universal metric;
- solve a finite-payload PDE;
- optimize field capacity;
- calculate complete operating energy;
- promote a physical antigravity model.

SCIENTIFIC LOGIC
----------------
A7 established a published IW vector family with:

    propagating Q_mu
    nondynamical T_hat_mu

and source reduction:

    J_Q_eff = J_Q - (b3/(2*b2))*J_T_hat.

The historical clean U1_V2 pair had both source channels zero.

A7 explicitly left generic Dirac source-state engineering open.

A10A later found engineered rest pairs that escaped the historical source
cancellations.

A11B subsequently reconstructed Wheeler's full general-spinor torsion
response.

This module therefore tests whether those exact later source states reopen
A7's previously unavailable axial T_hat channel.

PROTECTION TEST
---------------
The IW action reduces generically to a Proca vector and to Maxwell on:

    4*b1*b2 = b3^2.

For the Maxwell branch, the effective vector source must satisfy its Ward
identity.

For an unmodified massive Dirac field:

    partial_mu j5^mu
        =
    2*i*m*psi_bar*gamma5*psi

already classically, with possible additional anomaly terms quantum
mechanically.

Therefore an effective source proportional to the ordinary massive-Dirac
axial current is not an exact conserved Maxwell current as an operator
identity.

A state-specific static cancellation is not promoted into a same-action Ward
identity.

For the Proca branch a nonconserved source is algebraically allowed, but IW
symmetry itself permits the vector mass/mixing terms.  Therefore IW alone
does not protect a meter-range ultralight Proca mass.

The large m_e/m_V hierarchy is reported, but the numerical A10F2 loop
coefficient is NOT transferred to this distinct action.

SAME-ACTION DISCIPLINE
----------------------
A nonzero result here establishes an exact algebraic source-channel reopening
for the Wheeler GL(4) source evaluated on the A10 engineered states.

It does NOT establish that Wheeler's matter source has been obtained by
variation of one IW-invariant matter action.

The earlier A7 provenance record explicitly left that unestablished.

CLAIM LIMITS
------------
This gate does not close:

- all Barker-Zell IW matter completions;
- a genuinely new exact conserved source;
- full Noether-compensated IW matter;
- higher-spin torsion sources;
- derivative/composite source completions;
- other protected vector/torsion families;
- HOOK17 globally.

CLAIM CLASSIFICATION
--------------------
THEOREM_FIRST_SOURCE_REOPENING_AND_PROTECTION_PREFLIGHT
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    lorentz_trace,
    wheeler_trace_altered_nonmetricity,
)
from .hook17_barker_zell_iso_weyl_source_match import (
    barker_zell_iso_weyl_family_gate,
    generic_dirac_iw_escape_gate,
)
from .hook17_k2_wheeler_torsion_ward import (
    wheeler_full_torsion_response,
)
from .hook17_spin_engineered_dirac_source import (
    HISTORICAL_CLEAN_PAIR_ID,
    PAIR_SPECS,
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

ELECTRON_MASS_EV = 510_998.95

METER_RANGE_VECTOR_MASS_EV = (
    1.973269804e-7
)


def _levi_civita4(
    a: int,
    b: int,
    c: int,
    d: int,
) -> int:
    """Return epsilon^{abcd} with epsilon^{0123}=+1."""

    values = (
        a,
        b,
        c,
        d,
    )

    if len(
        set(
            values
        )
    ) != 4:
        return 0

    inversions = sum(
        values[
            i
        ]
        >
        values[
            j
        ]
        for i in range(
            4
        )
        for j in range(
            i + 1,
            4,
        )
    )

    return (
        -1
        if inversions % 2
        else 1
    )


def axial_torsion_pseudotrace(
    torsion_up: np.ndarray,
) -> np.ndarray:
    """Return an unnormalised axial pseudotrace of Wheeler T^a_bc.

    Only zero/nonzero structure and relative signs are used.

    The conventional overall normalization is omitted because A7's mixing
    coefficient carries convention-dependent normalization.
    """

    torsion = np.asarray(
        torsion_up,
        dtype=float,
    )

    if torsion.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "torsion_up must have shape (4,4,4)"
        )

    torsion_lower = np.einsum(
        "ad,dbc->abc",
        ETA,
        torsion,
    )

    axial = np.zeros(
        4,
        dtype=float,
    )

    for mu in range(
        4
    ):
        axial[
            mu
        ] = sum(
            _levi_civita4(
                mu,
                a,
                b,
                c,
            )
            *
            torsion_lower[
                a,
                b,
                c,
            ]
            for a in range(
                4
            )
            for b in range(
                4
            )
            for c in range(
                4
            )
        )

    return axial


def engineered_iw_source_atlas() -> list[
    dict[
        str,
        Any,
    ]
]:
    """Return exact A10 rest-pair sources for the A7 IW vector block."""

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    rows = []

    for (
        pair_id,
        particle_index,
        antiparticle_index,
    ) in PAIR_SPECS:
        particle = basis[
            particle_index
        ]

        antiparticle = basis[
            antiparticle_index
        ]

        torsion = (
            wheeler_full_torsion_response(
                particle
            )
            +
            wheeler_full_torsion_response(
                antiparticle
            )
        )

        axial = (
            axial_torsion_pseudotrace(
                torsion
            )
        )

        nonmetricity = (
            wheeler_trace_altered_nonmetricity(
                particle
            )
            +
            wheeler_trace_altered_nonmetricity(
                antiparticle
            )
        )

        q_trace = np.asarray(
            lorentz_trace(
                nonmetricity
            ),
            dtype=float,
        )

        axial_norm = float(
            np.linalg.norm(
                axial
            )
        )

        q_trace_norm = float(
            np.linalg.norm(
                q_trace
            )
        )

        rows.append(
            {
                "pair_id":
                    pair_id,

                "historical_clean_pair":
                    pair_id
                    ==
                    HISTORICAL_CLEAN_PAIR_ID,

                "full_torsion_norm":
                    float(
                        np.linalg.norm(
                            torsion
                        )
                    ),

                "j_t_hat_axial":
                    axial.tolist(),

                "j_t_hat_norm":
                    axial_norm,

                "j_t_hat_nonzero":
                    axial_norm
                    >
                    TOL,

                "j_q_weyl_trace":
                    q_trace.tolist(),

                "j_q_norm":
                    q_trace_norm,

                "j_q_zero":
                    q_trace_norm
                    <=
                    TOL,

                "finite_nonzero_b3_over_2b2_induces_q_source":
                    bool(
                        axial_norm
                        >
                        TOL
                        and
                        q_trace_norm
                        <=
                        TOL
                    ),

                "source_norm_is_physical_energy":
                    False,
            }
        )

    return rows


def engineered_iw_reopening_theorem() -> dict[
    str,
    Any,
]:
    """Test whether later A10 states reopen the exact A7 IW source channel."""

    prior = (
        generic_dirac_iw_escape_gate()
    )

    rows = (
        engineered_iw_source_atlas()
    )

    reopened = [
        row
        for row in rows
        if row[
            "j_t_hat_nonzero"
        ]
    ]

    clean = next(
        row
        for row in rows
        if row[
            "historical_clean_pair"
        ]
    )

    u1v1 = next(
        row
        for row in rows
        if row[
            "pair_id"
        ]
        ==
        "U1_V1"
    )

    u2v2 = next(
        row
        for row in rows
        if row[
            "pair_id"
        ]
        ==
        "U2_V2"
    )

    opposite = bool(
        np.allclose(
            np.asarray(
                u1v1[
                    "j_t_hat_axial"
                ],
                dtype=float,
            ),
            -np.asarray(
                u2v2[
                    "j_t_hat_axial"
                ],
                dtype=float,
            ),
            atol=
                TOL,
            rtol=
                0.0,
        )
    )

    return {
        "a7_generic_dirac_source_state_engineering_was_open":
            prior[
                "generic_dirac_source_state_engineering_open"
            ],

        "historical_clean_pair_id":
            HISTORICAL_CLEAN_PAIR_ID,

        "historical_clean_pair_axial_source_zero":
            not clean[
                "j_t_hat_nonzero"
            ],

        "engineered_nonzero_axial_pair_ids":
            [
                row[
                    "pair_id"
                ]
                for row in reopened
            ],

        "engineered_nonzero_axial_pair_count":
            len(
                reopened
            ),

        "u1_v1_u2_v2_axial_sources_equal_and_opposite":
            opposite,

        "engineered_dirac_reopens_a7_t_hat_channel":
            bool(
                prior[
                    "generic_dirac_source_state_engineering_open"
                ]
                and
                len(
                    reopened
                )
                >=
                2
                and
                opposite
            ),

        "all_tested_weyl_q_direct_traces_zero":
            all(
                row[
                    "j_q_zero"
                ]
                for row in rows
            ),

        "iw_mixing_source_formula":
            "J_Q_EFF=J_Q-(b3/(2*b2))*J_T_HAT",

        "finite_nonzero_mixing_reopens_effective_q_source":
            any(
                row[
                    "finite_nonzero_b3_over_2b2_induces_q_source"
                ]
                for row in rows
            ),

        "same_action_iw_matter_completion_established":
            False,

        "rows":
            rows,
    }


def iw_maxwell_source_ward_gate() -> dict[
    str,
    Any,
]:
    """Apply the operator-level source Ward test on the IW Maxwell surface."""

    family = (
        barker_zell_iso_weyl_family_gate()
    )

    source = (
        engineered_iw_reopening_theorem()
    )

    return {
        "iw_maxwell_surface":
            family[
                "maxwell_surface"
            ],

        "effective_q_source_reopened":
            source[
                "finite_nonzero_mixing_reopens_effective_q_source"
            ],

        "ordinary_massive_dirac_axial_current_divergence":
            (
                "partial_mu_j5^mu="
                "2*i*m*psi_bar*gamma5*psi"
                "+quantum_anomaly_terms"
            ),

        "mass_term_breaks_axial_current_conservation":
            True,

        "quantum_anomaly_can_further_break_axial_current_conservation":
            True,

        "state_specific_static_divergence_zero_is_operator_ward_identity":
            False,

        "unmodified_massive_dirac_axial_source_is_exact_conserved_current":
            False,

        "direct_maxwell_source_ward_pass":
            False,

        "direct_engineered_dirac_iw_maxwell_branch_closed":
            True,

        "full_noether_completed_iw_maxwell_source_closed":
            False,

        "exact_new_conserved_source_closed":
            False,
    }


def iw_proca_protection_gate() -> dict[
    str,
    Any,
]:
    """Test whether generic IW Proca solves the meter-range protection issue."""

    family = (
        barker_zell_iso_weyl_family_gate()
    )

    hierarchy = (
        ELECTRON_MASS_EV
        /
        METER_RANGE_VECTOR_MASS_EV
    )

    return {
        "generic_iw_reduced_vector_theory":
            family[
                "reduced_vector_theory"
            ],

        "iw_action_contains_vector_mass_mixing_terms":
            True,

        "iw_vector_mass_mixing":
            family[
                "vector_mass_mixing"
            ],

        "iw_symmetry_forbids_vector_mass_terms":
            False,

        "meter_range_target_mass_ev":
            METER_RANGE_VECTOR_MASS_EV,

        "electron_mass_ev":
            ELECTRON_MASS_EV,

        "electron_mass_over_meter_vector_mass":
            hierarchy,

        "nonconserved_axial_source_has_longitudinal_hierarchy":
            True,

        "a10f2_loop_coefficient_transferred_to_iw":
            False,

        "meter_scale_proca_mass_technically_protected_by_iw_alone":
            False,

        "unmodified_iw_proca_branch_promoted":
            False,

        "genuinely_new_higgs_noether_or_symmetry_protection_closed":
            False,
    }


def a12a_rerank() -> list[
    dict[
        str,
        Any,
    ]
]:
    """Return the post-gate protected-source priority order."""

    return [
        {
            "priority":
                1,

            "family":
                "FULL_SAME_ACTION_IW_NOETHER_OR_EXACT_CONSERVED_CURRENT",

            "status":
                "OPEN_HIGHEST_PRIORITY_IF_NEW_ACTION_EXISTS",

            "reason":
                (
                    "ENGINEERED DIRAC STATES REOPEN THE NATIVE IW AXIAL "
                    "SOURCE CHANNEL, BUT THE UNMODIFIED MASSIVE-DIRAC "
                    "MAXWELL CURRENT FAILS THE WARD IDENTITY AND IW "
                    "ALONE DOES NOT PROTECT THE METER-SCALE PROCA MASS"
                ),
        },
        {
            "priority":
                2,

            "family":
                "CONFORMAL_VECTOR_TORSION_WITH_GENUINELY_NEW_MICROSCOPIC_SOURCE",

            "status":
                "OPEN_SOURCE_PROVENANCE_REQUIRED",

            "reason":
                (
                    "SCALE-INVARIANT PGT PROVIDES A SYMMETRY-MOTIVATED "
                    "VECTOR-TORSION KINETIC ROUTE, BUT A NEW SAME-ACTION "
                    "MICROSCOPIC SOURCE IS REQUIRED"
                ),
        },
        {
            "priority":
                3,

            "family":
                "GENUINELY_NONLINEAR_VECTOR_GRAVITON_OR_CURVATURE_PORTAL",

            "status":
                "OPEN_NONLINEAR_ONLY",

            "reason":
                (
                    "TESTED LINEAR VECTOR-METRIC BRIDGES ARE CLOSED; "
                    "ONLY A GENUINELY NEW GAUGE-INVARIANT NONLINEAR "
                    "COMPLETION CAN DIFFER"
                ),
        },
    ]


def h17a12a_summary() -> dict[
    str,
    Any,
]:
    """Return the conservative A12A decision."""

    source = (
        engineered_iw_reopening_theorem()
    )

    maxwell = (
        iw_maxwell_source_ward_gate()
    )

    proca = (
        iw_proca_protection_gate()
    )

    source_reopened = (
        source[
            "engineered_dirac_reopens_a7_t_hat_channel"
        ]
    )

    direct_current_blocked = bool(
        maxwell[
            "direct_engineered_dirac_iw_maxwell_branch_closed"
        ]
        and
        not proca[
            "meter_scale_proca_mass_technically_protected_by_iw_alone"
        ]
    )

    if (
        source_reopened
        and
        direct_current_blocked
    ):
        decision = (
            "YELLOW_A12A_ENGINEERED_DIRAC_REOPENS_BARKER_ZELL_IW_AXIAL_SOURCE__"
            "DIRECT_UNMODIFIED_MAXWELL_BRANCH_CLOSED_ON_AXIAL_CURRENT_WARD__"
            "METER_RANGE_PROCA_NOT_PROTECTED_BY_IW_ALONE__"
            "PROMOTE_ONLY_NEW_SAME_ACTION_SOURCE_PROTECTION"
        )
    else:
        decision = (
            "CHECK_A12A_IW_SOURCE_OR_PROTECTION_ASSUMPTIONS"
        )

    return {
        "branch":
            "032H17A12A",

        "decision":
            decision,

        "source_reopening":
            source,

        "maxwell_source_ward":
            maxwell,

        "proca_protection":
            proca,

        "engineered_iw_source_channel_reopened":
            source_reopened,

        "unmodified_ordinary_dirac_iw_route_promoted":
            False,

        "full_barker_zell_iw_family_closed":
            False,

        "full_same_action_iw_noether_completion_closed":
            False,

        "higher_spin_or_new_microscopic_source_closed":
            False,

        "metric_gate_authorized":
            False,

        "payload_gate_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "hook17_closed":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "rerank":
            a12a_rerank(),

        "next":
            "032H17A12B_FULL_SAME_ACTION_IW_EXACT_SOURCE_PROTECTION_GATE",

        "stop_rule":
            (
                "DO_NOT_BUILD_IW_METRIC_PAYLOAD_OR_ENERGY_LEDGER_UNTIL_"
                "A_NEW_SAME_ACTION_EXACT_CONSERVED_SOURCE_OR_TECHNICALLY_"
                "NATURAL_MASS_PROTECTION_IS_EXHIBITED"
            ),
    }
