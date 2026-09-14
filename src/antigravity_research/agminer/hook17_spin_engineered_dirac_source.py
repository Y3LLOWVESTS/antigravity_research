"""032H17A10A — spin-engineered intrinsic-Dirac rest-source gate.

PURPOSE
-------
Test the cheapest remaining HOOK17 source-state-engineering question after
the A9R3 technical-naturalness block and the V26E1B2 fallback closeout.

The historical V24 clean equal-rest particle/antiparticle source has zero
direct totally-symmetric Lorentz trace-vector support in the protected BMS
spin-one preflight.

That historical zero did not close the full Dirac rest-state manifold.

This module therefore enumerates the complete two-by-two particle /
antiparticle component basis at zero spatial momentum in the Wheeler source
convention and asks whether changing only the internal Dirac state can
produce a nonzero totally-symmetric trace carrier.

SCIENTIFIC QUESTION
-------------------
Does an exact rest-basis Dirac source state exist which:

1. uses the same Wheeler intrinsic nonmetricity source formula;
2. remains inside the particle/antiparticle rest component subspaces;
3. keeps the full Weyl/dilation trace zero;
4. but has nonzero totally-symmetric Lorentz trace-vector support?

If yes, the historical clean-rest BMS trace-vector source zero is a
source-state-specific zero rather than a theorem over the full rest basis.

THIS MODULE DOES NOT ESTABLISH
------------------------------
- the exact BMS tensor-gauge source Ward identity;
- that the new state sources the physical protected BMS pole;
- the published massive 1- pole projector;
- torsion cancellation for the engineered pair;
- a localized stationary many-body source;
- spin-texture stability;
- canonical source charge per joule;
- a universal physical metric;
- outward acceleration;
- finite-payload stand-off;
- source/support energy;
- complete operating energy;
- a practical antigravity model.

IMPORTANT REPRESENTATION DISTINCTION
------------------------------------
The full Wheeler nonmetricity trace

    eta^{ab} Q^c_ab

is distinct from the Lorentz trace of the totally-symmetric irrep

    t_a = eta^{bc} S_abc.

The former remains zero in the tested rest basis.

A nonzero latter quantity therefore does not reopen the already-closed
Weyl/dilation shortcut.

SOURCE PROVENANCE
-----------------
Every row is evaluated with the same

    wheeler_trace_altered_nonmetricity

source function already used by V24.

No arbitrary rank-three source is inserted by hand.

CLAIM CLASSIFICATION
--------------------
EXACT_REST_BASIS_DIRAC_SOURCE_STATE_REPRESENTATION_PREFLIGHT

NOVEL PHYSICS CLAIM
-------------------
NO
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    lower_first_index,
    symmetric_hook_decomposition,
    wheeler_trace_altered_nonmetricity,
)
from .dirac_hook_vector_bridge import (
    lorentz_trace_covector,
    trace_carrier_coupling_identity,
)
from .protected_dirac_metric_bridge import (
    totally_symmetric_so3_carriers,
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


PAIR_SPECS = (
    (
        "U1_V1",
        0,
        2,
    ),
    (
        "U1_V2",
        0,
        3,
    ),
    (
        "U2_V1",
        1,
        2,
    ),
    (
        "U2_V2",
        1,
        3,
    ),
)

HISTORICAL_CLEAN_PAIR_ID = "U1_V2"


def rest_component_basis() -> dict[
    str,
    np.ndarray,
]:
    """Return the four unit Dirac component-basis rest-state candidates.

    U1/U2 span the upper two-component particle subspace.

    V1/V2 span the lower two-component antiparticle subspace.

    We intentionally avoid assigning physical spin-up/spin-down names here.
    The source theorem depends only on the explicit component vectors.
    """

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    return {
        "U1":
            basis[
                0
            ].copy(),

        "U2":
            basis[
                1
            ].copy(),

        "V1":
            basis[
                2
            ].copy(),

        "V2":
            basis[
                3
            ].copy(),
    }


def _pair_source(
    particle_index: int,
    antiparticle_index: int,
) -> dict[
    str,
    np.ndarray,
]:
    """Return the exact Wheeler source decomposition for one rest pair."""

    basis = np.eye(
        4,
        dtype=np.complex128,
    )

    particle = basis[
        particle_index
    ]

    antiparticle = basis[
        antiparticle_index
    ]

    q_up = (
        wheeler_trace_altered_nonmetricity(
            particle
        )
        +
        wheeler_trace_altered_nonmetricity(
            antiparticle
        )
    )

    q_cov = lower_first_index(
        q_up
    )

    pieces = symmetric_hook_decomposition(
        q_cov
    )

    return {
        "q_up":
            np.asarray(
                q_up,
                dtype=float,
            ),

        "q_cov":
            np.asarray(
                q_cov,
                dtype=float,
            ),

        "totally_symmetric":
            np.asarray(
                pieces[
                    "totally_symmetric"
                ],
                dtype=float,
            ),

        "hook":
            np.asarray(
                pieces[
                    "hook_symmetric"
                ],
                dtype=float,
            ),
    }


def _full_weyl_dilation_trace(
    q_up: np.ndarray,
) -> np.ndarray:
    """Return eta^{ab} Q^c_ab for the full Wheeler source."""

    q = np.asarray(
        q_up,
        dtype=float,
    )

    if q.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "q_up must have shape (4,4,4)"
        )

    return np.einsum(
        "ab,cab->c",
        ETA,
        q,
    )


def _trace_carrier_basis_tests(
    source: np.ndarray,
) -> list[
    dict[
        str,
        Any,
    ]
]:
    """Test the exact pure-trace carrier identity against each basis vector."""

    rows = []

    for index in range(
        4
    ):
        vector = np.zeros(
            4,
            dtype=float,
        )

        vector[
            index
        ] = 1.0

        result = trace_carrier_coupling_identity(
            source,
            vector,
        )

        rows.append(
            {
                "basis_index":
                    index,

                "direct_contraction":
                    float(
                        result[
                            "direct_contraction"
                        ]
                    ),

                "predicted_contraction":
                    float(
                        result[
                            "predicted_contraction"
                        ]
                    ),

                "relative_error":
                    float(
                        result[
                            "relative_error"
                        ]
                    ),

                "identity_pass":
                    bool(
                        result[
                            "identity_pass"
                        ]
                    ),
            }
        )

    return rows


def rest_pair_state_record(
    pair_id: str,
    particle_index: int,
    antiparticle_index: int,
) -> dict[
    str,
    Any,
]:
    """Return exact representation diagnostics for one rest-basis pair."""

    pieces = _pair_source(
        particle_index,
        antiparticle_index,
    )

    q_up = pieces[
        "q_up"
    ]

    total = pieces[
        "totally_symmetric"
    ]

    hook = pieces[
        "hook"
    ]

    full_trace = _full_weyl_dilation_trace(
        q_up
    )

    total_trace = lorentz_trace_covector(
        total
    )

    q_norm = float(
        np.linalg.norm(
            q_up
        )
    )

    total_norm = float(
        np.linalg.norm(
            total
        )
    )

    hook_norm = float(
        np.linalg.norm(
            hook
        )
    )

    full_trace_norm = float(
        np.linalg.norm(
            full_trace
        )
    )

    total_trace_norm = float(
        np.linalg.norm(
            total_trace
        )
    )

    scale = max(
        q_norm,
        total_norm,
        hook_norm,
        1.0,
    )

    carrier_tests = (
        _trace_carrier_basis_tests(
            total
        )
    )

    maximum_direct_overlap = max(
        abs(
            float(
                row[
                    "direct_contraction"
                ]
            )
        )
        for row in carrier_tests
    )

    carriers = totally_symmetric_so3_carriers(
        total
    )

    combined_spin1_screen = float(
        np.hypot(
            carriers[
                "spin1_spatial_trace_norm"
            ],
            carriers[
                "spin1_zero_zero_i_norm"
            ],
        )
    )

    return {
        "pair_id":
            pair_id,

        "particle_component_index":
            int(
                particle_index
            ),

        "antiparticle_component_index":
            int(
                antiparticle_index
            ),

        "historical_clean_pair":
            bool(
                pair_id
                ==
                HISTORICAL_CLEAN_PAIR_ID
            ),

        "full_wheeler_source_component_norm":
            q_norm,

        "full_wheeler_source_zero":
            bool(
                q_norm
                <=
                TOL
            ),

        "full_weyl_dilation_trace":
            full_trace.tolist(),

        "full_weyl_dilation_trace_norm":
            full_trace_norm,

        "full_weyl_dilation_trace_zero":
            bool(
                full_trace_norm
                <=
                TOL
                *
                scale
            ),

        "totally_symmetric_source_component_norm":
            total_norm,

        "hook_source_component_norm":
            hook_norm,

        "totally_symmetric_lorentz_trace_covector":
            total_trace.tolist(),

        "totally_symmetric_lorentz_trace_norm":
            total_trace_norm,

        "totally_symmetric_trace_nonzero":
            bool(
                total_trace_norm
                >
                TOL
                *
                scale
            ),

        "trace_carrier_basis_tests":
            carrier_tests,

        "trace_carrier_identity_all_pass":
            bool(
                all(
                    row[
                        "identity_pass"
                    ]
                    for row
                    in carrier_tests
                )
            ),

        "maximum_direct_trace_carrier_overlap":
            maximum_direct_overlap,

        "direct_trace_carrier_overlap_nonzero":
            bool(
                maximum_direct_overlap
                >
                TOL
                *
                scale
            ),

        "so3_spin1_spatial_trace_norm":
            float(
                carriers[
                    "spin1_spatial_trace_norm"
                ]
            ),

        "so3_spin1_zero_zero_i_norm":
            float(
                carriers[
                    "spin1_zero_zero_i_norm"
                ]
            ),

        "so3_combined_spin1_screen_norm":
            combined_spin1_screen,

        "so3_spin2_zero_ij_stf_norm":
            float(
                carriers[
                    "spin2_zero_ij_stf_norm"
                ]
            ),

        "so3_spin3_spatial_stf_norm":
            float(
                carriers[
                    "spin3_spatial_stf_norm"
                ]
            ),

        "rest_frame_so3_screen_is_exact_pole_projector":
            False,

        "component_norm_is_lorentz_invariant":
            False,

        "component_norm_is_physical_energy":
            False,
    }


def rest_pair_state_atlas() -> list[
    dict[
        str,
        Any,
    ]
]:
    """Return all four particle/antiparticle component-basis pair rows."""

    return [
        rest_pair_state_record(
            pair_id,
            particle_index,
            antiparticle_index,
        )

        for (
            pair_id,
            particle_index,
            antiparticle_index,
        )
        in PAIR_SPECS
    ]


def h17a10a_summary() -> dict[
    str,
    Any,
]:
    """Return the theorem-first A10A source-state decision."""

    rows = rest_pair_state_atlas()

    row_map = {
        row[
            "pair_id"
        ]:
            row

        for row in rows
    }

    historical = row_map[
        HISTORICAL_CLEAN_PAIR_ID
    ]

    engineered = [
        row

        for row in rows

        if (
            row[
                "totally_symmetric_trace_nonzero"
            ]
            and
            not row[
                "historical_clean_pair"
            ]
        )
    ]

    engineered_ids = [
        row[
            "pair_id"
        ]

        for row in engineered
    ]

    expected_engineered_ids = {
        "U1_V1",
        "U2_V2",
    }

    exact_engineered_set = (
        set(
            engineered_ids
        )
        ==
        expected_engineered_ids
    )

    u1v1_trace = np.asarray(
        row_map[
            "U1_V1"
        ][
            "totally_symmetric_lorentz_trace_covector"
        ],
        dtype=float,
    )

    u2v2_trace = np.asarray(
        row_map[
            "U2_V2"
        ][
            "totally_symmetric_lorentz_trace_covector"
        ],
        dtype=float,
    )

    equal_opposite = bool(
        np.allclose(
            u1v1_trace,
            -u2v2_trace,
            rtol=0.0,
            atol=1.0e-12,
        )
        and
        np.linalg.norm(
            u1v1_trace
        )
        >
        TOL
    )

    expected_minus = np.array(
        [
            0.0,
            -8.0 / 3.0,
            0.0,
            0.0,
        ],
        dtype=float,
    )

    expected_plus = -expected_minus

    exact_trace_values = bool(
        np.allclose(
            u1v1_trace,
            expected_minus,
            rtol=0.0,
            atol=1.0e-12,
        )
        and
        np.allclose(
            u2v2_trace,
            expected_plus,
            rtol=0.0,
            atol=1.0e-12,
        )
    )

    all_full_weyl_trace_zero = bool(
        all(
            row[
                "full_weyl_dilation_trace_zero"
            ]
            for row
            in rows
        )
    )

    carrier_identities_pass = bool(
        all(
            row[
                "trace_carrier_identity_all_pass"
            ]
            for row
            in rows
        )
    )

    null_pair_zero = bool(
        row_map[
            "U2_V1"
        ][
            "full_wheeler_source_zero"
        ]
    )

    historical_trace_zero = bool(
        not historical[
            "totally_symmetric_trace_nonzero"
        ]
        and
        not historical[
            "direct_trace_carrier_overlap_nonzero"
        ]
    )

    source_state_escape = bool(
        historical_trace_zero
        and
        exact_engineered_set
        and
        exact_trace_values
        and
        equal_opposite
        and
        carrier_identities_pass
        and
        all_full_weyl_trace_zero
    )

    partial_green = bool(
        source_state_escape
        and
        null_pair_zero
    )

    decision = (
        "GREEN_A10A_REST_BASIS_TRACE_VECTOR_ESCAPE_SOURCE_LEVEL_ONLY"
        if partial_green
        else
        "RED_A10A_NO_EXACT_REST_BASIS_TRACE_VECTOR_ESCAPE"
    )

    next_gate = (
        "032H17A10B_BMS_PROTECTED_SPIN1_EXACT_WARD_"
        "TORSION_AND_POLE_PROJECTOR_GATE"
        if partial_green
        else
        "RETURN_TO_A9R3_NEW_PROTECTED_FAMILY_RERANK"
    )

    return {
        "branch":
            "032H17A10A",

        "subgate":
            (
                "SPIN_ENGINEERED_INTRINSIC_DIRAC_"
                "REST_SOURCE_STATE_PREFILTER"
            ),

        "decision":
            decision,

        "rest_component_basis_size":
            4,

        "particle_antiparticle_pair_count":
            len(
                rows
            ),

        "historical_clean_pair_id":
            HISTORICAL_CLEAN_PAIR_ID,

        "historical_clean_pair_trace_zero_reproduced":
            historical_trace_zero,

        "spin_engineered_rest_pair_trace_escape_exists":
            source_state_escape,

        "spin_engineered_nonzero_pair_ids":
            engineered_ids,

        "spin_engineered_nonzero_pair_count":
            len(
                engineered_ids
            ),

        "expected_engineered_pair_set_reproduced":
            exact_engineered_set,

        "engineered_trace_exact_values_reproduced":
            exact_trace_values,

        "engineered_trace_equal_and_opposite":
            equal_opposite,

        "engineered_trace_component_magnitude":
            float(
                8.0
                /
                3.0
            ),

        "engineered_maximum_direct_trace_carrier_overlap":
            max(
                float(
                    row[
                        "maximum_direct_trace_carrier_overlap"
                    ]
                )
                for row
                in engineered
            )
            if engineered
            else 0.0,

        "u2_v1_null_source_reproduced":
            null_pair_zero,

        "all_full_weyl_dilation_traces_zero":
            all_full_weyl_trace_zero,

        "trace_carrier_identity_all_pairs_pass":
            carrier_identities_pass,

        "microscopic_nonmetricity_source_formula":
            "WHEELER_V24_DIRAC_SOURCE",

        "microscopic_nonmetricity_source_provenance_preserved_under_state_change":
            True,

        "arbitrary_rank3_source_inserted":
            False,

        "historical_clean_source_zero_generalized_to_all_rest_states":
            False,

        "bms_totally_symmetric_trace_vector_candidate_reopened_by_state_engineering":
            partial_green,

        "exact_bms_tensor_gauge_source_ward_evaluated":
            False,

        "exact_bms_physical_pole_projector_evaluated_for_engineered_state":
            False,

        "exact_massive_1minus_projector_evaluated_for_engineered_state":
            False,

        "engineered_pair_full_torsion_source_reconstructed":
            False,

        "engineered_pair_torsion_cancellation_established":
            False,

        "localized_stationary_many_body_source_established":
            False,

        "source_texture_ward_compatible":
            False,

        "canonical_source_charge_per_joule_established":
            False,

        "universal_physical_metric_established":
            False,

        "finite_payload_outward_response_established":
            False,

        "true_standoff_established":
            False,

        "source_support_energy_established":
            False,

        "complete_energy_established":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_reference_capacity_transferred_to_new_carrier":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "exactly_target_passes":
            False,

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

        "next_scientific_question":
            (
                "Does the exact symmetry operator of the protected BMS "
                "totally-symmetric massless spin-one theory admit either "
                "spin-engineered Wheeler rest source after the full source "
                "Ward identity is imposed, while the complete Dirac torsion "
                "and nonmetricity source and physical pole projector remain "
                "nonzero and healthy?"
            ),
    }
