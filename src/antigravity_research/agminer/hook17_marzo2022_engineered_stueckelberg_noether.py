"""032H17A10C — engineered Marzo-2022 Stueckelberg source-Noether gate.

PURPOSE
-------
Test the cheapest same-symmetry source-completion question opened by A10B.

A10A established that two exact zero-momentum Dirac rest-pair states,

    U1 + V1
    U2 + V2

have nonzero totally-symmetric spin-one source support.

A10B established:

    direct BMS rest-density trace route = closed in tested class

while:

    Marzo-2022 protected massive 1- representation support
    = reopened for the engineered states.

The next question is not yet the exact physical pole residue.

The next cheaper question is:

Can the engineered Wheeler connection current be coupled to the published
Marzo-2022 Stueckelberg sector through one fixed local Abelian-invariant
interaction, rather than through state-by-state source repair?

PUBLISHED SYMMETRY
------------------
Marzo 2022 uses the extended Abelian transformation

    delta A_{mu nu}^rho
        =
    g_{mu nu} partial^rho Omega

    delta phi
        =
    f Omega.

Therefore the combination

    B_{mu nu}^rho
        =
    A_{mu nu}^rho
        -
    (1/f) g_{mu nu} partial^rho phi

is invariant for nonzero f.

A linearized source scaffold

    S_int
        ~
    integral J^{mu nu}_rho(psi) B_{mu nu}^rho

therefore generates the connection and compensating scalar source from one
fixed interaction.

SOURCE WARD IDENTITY
--------------------
For the source convention used here, Abelian invariance requires

    q^rho j_rho
        +
    f j_phi
        =
    0

where

    j_rho
        =
    eta^{mu nu} J_{mu nu rho}.

Without the scalar source:

    q^rho j_rho
        =
    0

would have to hold as an identity.

With the Stueckelberg completion:

    j_phi
        =
    -(q^rho j_rho)/f

and the identity is exact.

IMPORTANT INDEX CONVENTION
--------------------------
A9R1 already constructed a convention-matched Wheeler -> P&S source

    tau[c,a,b]

and projected it into the torsion-free space

    tau[c,a,b]
        =
    tau[b,a,c].

Marzo's torsion-free connection

    A_{mu nu}^rho

is symmetric in mu,nu.

The corresponding index relabeling used in this preflight is

    mu  = c
    nu  = b
    rho = a

so

    J[mu,nu,rho]
        =
    tau[mu,rho,nu].

This turns P&S first-third symmetry into Marzo first-second symmetry.

This is an index-convention relabeling of the existing A9R1
convention-matched source.

It is NOT an independent derivation of the full Wheeler matter variation
inside the Marzo action.

CLAIM LIMIT
-----------
A positive result establishes only:

    a local linearized Abelian-invariant source-interaction scaffold

    plus

    preservation of nonzero engineered 1- representation support.

It does NOT establish:

- a complete covariant Dirac matter action;
- the full engineered Wheeler torsion response;
- the exact constrained Marzo source basis S_i;
- the exact physical 1- pole projector;
- the exact pole residue;
- canonical source charge per joule;
- a universal physical metric;
- physical g00 response;
- outward sign;
- finite payload;
- true stand-off;
- source/support energy;
- complete operating energy;
- a practical device.

TORSION DISCIPLINE
------------------
The current repository implements Wheeler's torsion response only for the
published special rest-spin-up particle/antiparticle case.

The spin-engineered torsion source must not be guessed by analogy.

Its reconstruction is deferred until the general Wheeler torsion formula is
independently derived.

ENERGY POLICY
-------------
No energy optimization is authorized.

The historical ~17.07 J HOOK17 value remains field capacity only.

CLAIM CLASSIFICATION
--------------------
LINEARIZED_STUECKELBERG_NOETHER_SOURCE_COMPLETION_PREFLIGHT
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    lower_first_index,
    symmetric_hook_decomposition,
    wheeler_trace_altered_nonmetricity,
)
from .hook17_marzo2022_massive_source_match import (
    marzo2022_published_family_gate,
)
from .hook17_ps_wheeler_same_action_noether import (
    ps_torsion_free_source_for_spinor,
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

STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

HOOK17_REFERENCE_CAPACITY_RP1E12_J = (
    17.0676442196
)

PAIR_SPECS = {
    "U1_V1":
        (
            0,
            2,
        ),

    "U2_V2":
        (
            1,
            3,
        ),
}


def _basis() -> np.ndarray:
    """Return the four exact Dirac component basis vectors."""

    return np.eye(
        4,
        dtype=np.complex128,
    )


def engineered_pair_ps_tau(
    pair_id: str,
) -> np.ndarray:
    """Return the A9R1 convention-matched torsion-free tau[c,a,b]."""

    if pair_id not in PAIR_SPECS:
        raise ValueError(
            f"unknown engineered pair: {pair_id}"
        )

    (
        particle_index,
        antiparticle_index,
    ) = PAIR_SPECS[
        pair_id
    ]

    basis = _basis()

    tau = (
        ps_torsion_free_source_for_spinor(
            basis[
                particle_index
            ]
        )
        +
        ps_torsion_free_source_for_spinor(
            basis[
                antiparticle_index
            ]
        )
    )

    return np.asarray(
        tau,
        dtype=float,
    )


def ps_tau_to_marzo_torsionfree_source(
    tau_cab: np.ndarray,
) -> np.ndarray:
    """Relabel P&S tau[c,a,b] as Marzo J[mu,nu,rho].

    The existing P&S torsion-free source is symmetric in slots 0 and 2.

    Relabel:

        mu  = c
        nu  = b
        rho = a

    so:

        J[mu,nu,rho]
            =
        tau[mu,rho,nu].
    """

    tau = np.asarray(
        tau_cab,
        dtype=float,
    )

    if tau.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "tau_cab must have shape (4,4,4)"
        )

    if not np.allclose(
        tau,
        np.swapaxes(
            tau,
            0,
            2,
        ),
        atol=
            TOL,
        rtol=
            0.0,
    ):
        raise ValueError(
            "tau must be torsion-free first-third symmetric"
        )

    source = np.transpose(
        tau,
        (
            0,
            2,
            1,
        ),
    )

    if not np.allclose(
        source,
        np.swapaxes(
            source,
            0,
            1,
        ),
        atol=
            TOL,
        rtol=
            0.0,
    ):
        raise AssertionError(
            "Marzo source must be symmetric in mu,nu"
        )

    return np.asarray(
        source,
        dtype=float,
    )


def marzo_trace_covector(
    source_mnr: np.ndarray,
) -> np.ndarray:
    """Return j_rho = eta^(mu nu) J_(mu nu rho)."""

    source = np.asarray(
        source_mnr,
        dtype=float,
    )

    if source.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "source must have shape (4,4,4)"
        )

    return np.einsum(
        "mn,mnr->r",
        ETA,
        source,
    )


def all_rank3_pair_traces(
    tau_cab: np.ndarray,
) -> dict[
    str,
    np.ndarray,
]:
    """Return all Lorentz pair traces as a convention crosscheck."""

    tau = np.asarray(
        tau_cab,
        dtype=float,
    )

    return {
        "trace_01":
            np.einsum(
                "ij,ijk->k",
                ETA,
                tau,
            ),

        "trace_02":
            np.einsum(
                "ik,ijk->j",
                ETA,
                tau,
            ),

        "trace_12":
            np.einsum(
                "jk,ijk->i",
                ETA,
                tau,
            ),
    }


def direct_marzo_abelian_ward_residual(
    trace_cov: np.ndarray,
    q_up: np.ndarray,
) -> float:
    """Return q^rho j_rho for a pure-connection source."""

    trace = np.asarray(
        trace_cov,
        dtype=float,
    )

    q = np.asarray(
        q_up,
        dtype=float,
    )

    if trace.shape != (
        4,
    ):
        raise ValueError(
            "trace_cov must have shape (4,)"
        )

    if q.shape != (
        4,
    ):
        raise ValueError(
            "q_up must have shape (4,)"
        )

    return float(
        np.dot(
            q,
            trace,
        )
    )


def stueckelberg_scalar_source_for_ward(
    trace_cov: np.ndarray,
    q_up: np.ndarray,
    f: float,
) -> float:
    """Return the scalar source fixed by the Abelian Ward identity.

    Convention:

        q.j + f j_phi = 0.

    Hence:

        j_phi = -(q.j)/f.
    """

    f_value = float(
        f
    )

    if (
        not np.isfinite(
            f_value
        )
        or
        abs(
            f_value
        )
        <=
        1.0e-15
    ):
        raise ValueError(
            "f must be finite and nonzero"
        )

    return (
        -direct_marzo_abelian_ward_residual(
            trace_cov,
            q_up,
        )
        /
        f_value
    )


def completed_marzo_abelian_ward_residual(
    trace_cov: np.ndarray,
    q_up: np.ndarray,
    f: float,
) -> float:
    """Return the completed connection-plus-scalar Ward residual."""

    scalar_source = (
        stueckelberg_scalar_source_for_ward(
            trace_cov,
            q_up,
            f,
        )
    )

    return (
        direct_marzo_abelian_ward_residual(
            trace_cov,
            q_up,
        )
        +
        float(
            f
        )
        *
        scalar_source
    )


def stueckelberg_invariant_combination_gate() -> dict[
    str,
    Any,
]:
    """Verify delta[A - g dphi/f] = 0 exactly in the linearized algebra."""

    momentum_rows = {
        "TIME":
            np.array(
                [
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                ]
            ),

        "X":
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),

        "GENERIC":
            np.array(
                [
                    0.7,
                    -0.4,
                    0.2,
                    1.1,
                ]
            ),
    }

    rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for f in (
        1.0,
        -2.5,
        7.0,
    ):
        for (
            momentum_id,
            q_cov,
        ) in momentum_rows.items():
            delta_connection = np.einsum(
                "mn,r->mnr",
                ETA,
                q_cov,
            )

            delta_compensator = (
                (
                    1.0
                    /
                    f
                )
                *
                np.einsum(
                    "mn,r->mnr",
                    ETA,
                    f
                    *
                    q_cov,
                )
            )

            residual = (
                delta_connection
                -
                delta_compensator
            )

            residual_norm = float(
                np.linalg.norm(
                    residual
                )
            )

            rows.append(
                {
                    "f":
                        f,

                    "momentum_id":
                        momentum_id,

                    "residual_norm":
                        residual_norm,

                    "pass":
                        bool(
                            residual_norm
                            <=
                            TOL
                        ),
                }
            )

    return {
        "rows":
            rows,

        "all_pass":
            bool(
                all(
                    row[
                        "pass"
                    ]
                    for row
                    in rows
                )
            ),

        "fixed_relative_coefficient":
            "MINUS_1_OVER_F",

        "state_dependent_source_surgery":
            False,
    }


def engineered_totally_symmetric_1minus_trace(
    pair_id: str,
) -> np.ndarray:
    """Recompute the A10A/B spatial totally-symmetric spin-one trace."""

    if pair_id not in PAIR_SPECS:
        raise ValueError(
            f"unknown engineered pair: {pair_id}"
        )

    (
        particle_index,
        antiparticle_index,
    ) = PAIR_SPECS[
        pair_id
    ]

    basis = _basis()

    response_up = (
        wheeler_trace_altered_nonmetricity(
            basis[
                particle_index
            ]
        )
        +
        wheeler_trace_altered_nonmetricity(
            basis[
                antiparticle_index
            ]
        )
    )

    response_cov = lower_first_index(
        response_up
    )

    pieces = symmetric_hook_decomposition(
        response_cov
    )

    total = np.asarray(
        pieces[
            "totally_symmetric"
        ],
        dtype=float,
    )

    spatial = total[
        1:,
        1:,
        1:,
    ]

    return np.einsum(
        "ijj->i",
        spatial,
    )


def engineered_pair_noether_gate(
    pair_id: str,
) -> dict[
    str,
    Any,
]:
    """Evaluate direct Ward failure and symmetry-forced repair."""

    tau = engineered_pair_ps_tau(
        pair_id
    )

    source = (
        ps_tau_to_marzo_torsionfree_source(
            tau
        )
    )

    trace = marzo_trace_covector(
        source
    )

    traces = all_rank3_pair_traces(
        tau
    )

    one_minus = (
        engineered_totally_symmetric_1minus_trace(
            pair_id
        )
    )

    momenta = {
        "X":
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),

        "NULL_X":
            np.array(
                [
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                ]
            ),

        "GENERIC":
            np.array(
                [
                    0.7,
                    -0.4,
                    0.2,
                    1.1,
                ]
            ),
    }

    ward_rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for (
        momentum_id,
        q_up,
    ) in momenta.items():
        direct = (
            direct_marzo_abelian_ward_residual(
                trace,
                q_up,
            )
        )

        completion_rows = []

        for f in (
            1.0,
            -2.5,
            7.0,
        ):
            scalar_source = (
                stueckelberg_scalar_source_for_ward(
                    trace,
                    q_up,
                    f,
                )
            )

            completed = (
                completed_marzo_abelian_ward_residual(
                    trace,
                    q_up,
                    f,
                )
            )

            completion_rows.append(
                {
                    "f":
                        f,

                    "scalar_source":
                        scalar_source,

                    "completed_residual":
                        completed,

                    "pass":
                        bool(
                            abs(
                                completed
                            )
                            <=
                            TOL
                        ),
                }
            )

        ward_rows.append(
            {
                "momentum_id":
                    momentum_id,

                "direct_pure_connection_residual":
                    direct,

                "direct_pass":
                    bool(
                        abs(
                            direct
                        )
                        <=
                        TOL
                    ),

                "completions":
                    completion_rows,
            }
        )

    all_three_pair_traces_nonzero = bool(
        all(
            np.linalg.norm(
                value
            )
            >
            TOL
            for value
            in traces.values()
        )
    )

    direct_not_identity = bool(
        any(
            not row[
                "direct_pass"
            ]
            for row
            in ward_rows
        )
    )

    completed_all = bool(
        all(
            completion[
                "pass"
            ]
            for row
            in ward_rows
            for completion
            in row[
                "completions"
            ]
        )
    )

    return {
        "pair_id":
            pair_id,

        "ps_tau_norm":
            float(
                np.linalg.norm(
                    tau
                )
            ),

        "ps_tau_first_third_symmetric":
            bool(
                np.allclose(
                    tau,
                    np.swapaxes(
                        tau,
                        0,
                        2,
                    ),
                    atol=
                        TOL,
                    rtol=
                        0.0,
                )
            ),

        "marzo_source_first_second_symmetric":
            bool(
                np.allclose(
                    source,
                    np.swapaxes(
                        source,
                        0,
                        1,
                    ),
                    atol=
                        TOL,
                    rtol=
                        0.0,
                )
            ),

        "marzo_abelian_trace_covector":
            trace.tolist(),

        "marzo_abelian_trace_norm":
            float(
                np.linalg.norm(
                    trace
                )
            ),

        "marzo_abelian_trace_nonzero":
            bool(
                np.linalg.norm(
                    trace
                )
                >
                TOL
            ),

        "all_three_rank3_pair_traces":
            {
                key:
                    value.tolist()

                for (
                    key,
                    value,
                )
                in traces.items()
            },

        "all_three_rank3_pair_traces_nonzero":
            all_three_pair_traces_nonzero,

        "direct_pure_connection_ward_is_not_identity":
            direct_not_identity,

        "stueckelberg_completed_ward_all_samples_pass":
            completed_all,

        "ward_rows":
            ward_rows,

        "engineered_1minus_spatial_trace_vector":
            one_minus.tolist(),

        "engineered_1minus_spatial_trace_norm":
            float(
                np.linalg.norm(
                    one_minus
                )
            ),

        "engineered_1minus_representation_nonzero":
            bool(
                np.linalg.norm(
                    one_minus
                )
                >
                TOL
            ),

        "exact_1minus_pole_projector_evaluated":
            False,
    }


def h17a10c_summary() -> dict[
    str,
    Any,
]:
    """Return the scoped A10C decision."""

    family = (
        marzo2022_published_family_gate()
    )

    invariant = (
        stueckelberg_invariant_combination_gate()
    )

    rows = [
        engineered_pair_noether_gate(
            pair_id
        )
        for pair_id
        in (
            "U1_V1",
            "U2_V2",
        )
    ]

    family_ok = bool(
        family[
            "explicit_metric_affine_action_published"
        ]
        and
        family[
            "protecting_abelian_symmetry_published"
        ]
        and
        family[
            "stueckelberg_scalar_extension_published"
        ]
        and
        family[
            "massive_extension_preserves_abelian_protection"
        ]
        and
        family[
            "published_massive_physical_pole_sector"
        ]
        ==
        "1_MINUS"
    )

    source_completion = bool(
        invariant[
            "all_pass"
        ]
        and
        all(
            row[
                "marzo_abelian_trace_nonzero"
            ]
            for row
            in rows
        )
        and
        all(
            row[
                "direct_pure_connection_ward_is_not_identity"
            ]
            for row
            in rows
        )
        and
        all(
            row[
                "stueckelberg_completed_ward_all_samples_pass"
            ]
            for row
            in rows
        )
    )

    representation_survives = bool(
        all(
            row[
                "engineered_1minus_representation_nonzero"
            ]
            for row
            in rows
        )
    )

    partial_green = bool(
        family_ok
        and
        source_completion
        and
        representation_survives
    )

    decision = (
        "GREEN_A10C_LINEAR_STUECKELBERG_NOETHER_SOURCE_"
        "COMPLETION_PRESERVES_ENGINEERED_1MINUS_REPRESENTATION"
        if partial_green
        else
        "RED_A10C_ENGINEERED_MARZO_STUECKELBERG_SOURCE_COMPLETION_FAIL"
    )

    next_gate = (
        "032H17A10D_MARZO2022_EXACT_CONSTRAINED_1MINUS_"
        "SOURCE_PROJECTOR_RESIDUE_AND_CANONICAL_OVERLAP_GATE"
        if partial_green
        else
        "RETURN_TO_A9R3_NEW_PROTECTED_FAMILY_RERANK"
    )

    return {
        "branch":
            "032H17A10C",

        "decision":
            decision,

        "current_full_regression_before_a10c":
            927,

        "marzo2022_published_protected_stueckelberg_family":
            family_ok,

        "published_abelian_symmetry":
            (
                "delta_A_munu^rho=g_munu*d^rho_Omega; "
                "delta_phi=f*Omega"
            ),

        "published_stueckelberg_f_relation":
            "f=-d1-(5/2)d2",

        "published_massive_physical_pole_sector":
            family[
                "published_massive_physical_pole_sector"
            ],

        "stueckelberg_invariant_combination":
            (
                "B_munu^rho=A_munu^rho-"
                "(1/f)g_munu*d^rho_phi"
            ),

        "stueckelberg_invariant_combination_exact_linearized":
            invariant[
                "all_pass"
            ],

        "source_interaction_scaffold":
            "J_munu_rho(psi)*B^munu_rho",

        "relative_scalar_connection_source_coefficient_symmetry_fixed":
            True,

        "source_completion_is_state_by_state_surgery":
            False,

        "engineered_pair_rows":
            rows,

        "both_engineered_direct_pure_connection_ward_fail_generic":
            bool(
                all(
                    row[
                        "direct_pure_connection_ward_is_not_identity"
                    ]
                    for row
                    in rows
                )
            ),

        "both_engineered_stueckelberg_completed_ward_pass":
            bool(
                all(
                    row[
                        "stueckelberg_completed_ward_all_samples_pass"
                    ]
                    for row
                    in rows
                )
            ),

        "both_engineered_1minus_representation_preserved":
            representation_survives,

        "linearized_local_abelian_invariant_matter_interaction_scaffold_exists":
            source_completion,

        "full_covariant_dirac_matter_action_established":
            False,

        "independent_marzo_variational_index_map_rederived_from_original_action":
            False,

        "full_engineered_wheeler_torsion_source_reconstructed":
            False,

        "exact_marzo_constrained_source_projector_evaluated":
            False,

        "exact_physical_1minus_pole_overlap_established":
            False,

        "canonical_1minus_source_charge_per_joule_established":
            False,

        "universal_physical_metric_established":
            False,

        "finite_payload_outward_response_established":
            False,

        "true_standoff_established":
            False,

        "complete_energy_established":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_reference_capacity_transferred":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "energy_optimization_authorized":
            False,

        "geometry_optimization_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "hook17_closed":
            False,

        "partial_green":
            partial_green,

        "next":
            next_gate,

        "torsion_reconstruction_deferred_reason":
            (
                "CURRENT_REPOSITORY_IMPLEMENTATION_HAS_ONLY_THE_"
                "PUBLISHED_REST_SPINUP_TORSION_SPECIAL_CASE;_"
                "DO_NOT_GUESS_THE_SPIN_ENGINEERED_TORSION_SOURCE"
            ),
    }
