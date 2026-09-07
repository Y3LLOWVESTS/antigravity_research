"""032V24C Dirac hook / protected-vector bridge preflight.

PURPOSE
-------
Use the completed V24A/V24B source reconstruction to close the clean
rest-pair direct protected totally-symmetric spin-one shortcut, establish an
exact representation-level map from the surviving Dirac hook source into a
pair-antisymmetric torsion-like carrier, and rerank the most promising
vector-graviton bridge architectures.

SCIENTIFIC QUESTIONS
--------------------
1. Does the equal-amplitude rest particle/antiparticle source directly excite
   the trace vector which underlies the protected totally-symmetric spin-one
   homothetic-curvature model?

2. Is the hook source H_{a(bc)} exactly equivalent, at the representation
   level, to a pair-antisymmetric rank-three carrier?

3. Does the clean particle/antiparticle nonmetricity-addition witness survive
   that hook-to-torsion-like map?

4. Which open vector architecture now offers the best chance of supplying a
   universal physical-metric bridge?

LITERATURE CONTEXT
------------------
Barker, Marzo and Santoni (2025), arXiv:2505.23894:
    symmetry-protected totally symmetric MAG admits healthy massless spin-one
    and spin-three sectors. The spin-one nonlinear completion is associated
    with homothetic-curvature squared.

Barker, Marzo and Santoni (2025), arXiv:2507.05349:
    symmetry-first pair-antisymmetric/torsion-like rank-three theories contain
    healthy vector modes; scalar and pseudoscalar torsion are not the
    successful protected sectors of that catalogue.

Wheeler (2024), arXiv:2407.13867:
    mixed-symmetry nonmetricity can be traded into an altered torsion
    description at the geometric field-redefinition level.

Marzo (2026), arXiv:2603.24008:
    a vector and graviton can mix already at quadratic order under a common
    gauge symmetry while maintaining a healthy massless spin-two plus massive
    spin-one spectrum in an open parameter region. A consistent deformation
    survives through quartic order.

IMPORTANT LIMITS
----------------
The hook-to-torsion-like transformation implemented here is an exact linear
representation map. It is not by itself a proof that the Wheeler Dirac source
matches any particular healthy torsion action.

The Marzo vector-graviton model is used only as a bridge template. This module
does not identify its vector with the Dirac hook source, derive its external
matter coupling, prove an antigravity sign, or establish a complete energy
ledger.

No candidate, rejection, action oracle, or mechanism metric is created.

CLAIM_CLASSIFICATION=
THEOREM_LEVEL_SOURCE_OVERLAP_AND_REPRESENTATION_RERANK_PREFLIGHT
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    lower_first_index,
    symmetric_hook_decomposition,
    wheeler_trace_altered_nonmetricity,
)
from .protected_dirac_metric_bridge import (
    rest_pair_fronsdal_ward_scout,
)
from .storage import Storage


ETA = np.diag(
    [
        -1.0,
        1.0,
        1.0,
        1.0,
    ]
)


def _raise_all_indices(
    tensor_cov: np.ndarray,
) -> np.ndarray:
    """Raise all three indices with eta=(-,+,+,+)."""
    tensor = np.asarray(
        tensor_cov,
        dtype=float,
    )

    if tensor.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "tensor must have shape (4,4,4)"
        )

    return np.einsum(
        "am,bn,cp,mnp->abc",
        ETA,
        ETA,
        ETA,
        tensor,
    )


def lorentz_trace_covector(
    tensor_cov: np.ndarray,
) -> np.ndarray:
    """Return t_a = eta^{bc} T_abc."""
    tensor = np.asarray(
        tensor_cov,
        dtype=float,
    )

    if tensor.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "tensor must have shape (4,4,4)"
        )

    return np.einsum(
        "bc,abc->a",
        ETA,
        tensor,
    )


def pure_trace_symmetric_embedding(
    vector_cov: np.ndarray
    | list[float]
    | tuple[float, ...],
) -> np.ndarray:
    """Return eta_ab V_c + eta_ac V_b + eta_bc V_a.

    The overall normalization is intentionally irrelevant. This embedding
    represents the unique Lorentz trace-vector carrier inside a totally
    symmetric rank-three tensor.
    """
    vector = np.asarray(
        vector_cov,
        dtype=float,
    )

    if vector.shape != (
        4,
    ):
        raise ValueError(
            "vector must contain four components"
        )

    if not np.all(
        np.isfinite(
            vector
        )
    ):
        raise ValueError(
            "vector components must be finite"
        )

    result = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    for a in range(
        4
    ):
        for b in range(
            4
        ):
            for c in range(
                4
            ):
                result[
                    a,
                    b,
                    c,
                ] = (
                    ETA[
                        a,
                        b,
                    ]
                    *
                    vector[
                        c
                    ]
                    +
                    ETA[
                        a,
                        c,
                    ]
                    *
                    vector[
                        b
                    ]
                    +
                    ETA[
                        b,
                        c,
                    ]
                    *
                    vector[
                        a
                    ]
                )

    return result


def direct_source_carrier_contraction(
    source_cov: np.ndarray,
    carrier_cov: np.ndarray,
) -> float:
    """Return S^{abc} K_abc."""
    source_up = _raise_all_indices(
        source_cov
    )

    carrier = np.asarray(
        carrier_cov,
        dtype=float,
    )

    if carrier.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "carrier must have shape (4,4,4)"
        )

    return float(
        np.einsum(
            "abc,abc->",
            source_up,
            carrier,
        )
    )


def trace_carrier_coupling_identity(
    source_cov: np.ndarray,
    vector_cov: np.ndarray
    | list[float]
    | tuple[float, ...],
) -> dict[
    str,
    Any,
]:
    """Verify the exact trace-carrier source identity.

    For a totally symmetric source S and trace carrier

        K_abc = eta_ab V_c + eta_ac V_b + eta_bc V_a,

    one has exactly

        S^{abc} K_abc = 3 t^a V_a,

    where

        t_a = eta^{bc} S_abc.
    """
    source = np.asarray(
        source_cov,
        dtype=float,
    )

    vector = np.asarray(
        vector_cov,
        dtype=float,
    )

    trace_cov = lorentz_trace_covector(
        source
    )

    trace_up = ETA @ trace_cov

    direct = direct_source_carrier_contraction(
        source,
        pure_trace_symmetric_embedding(
            vector
        ),
    )

    predicted = float(
        3.0
        *
        np.dot(
            trace_up,
            vector,
        )
    )

    relative_error = (
        abs(
            direct
            -
            predicted
        )
        /
        max(
            abs(
                direct
            ),
            abs(
                predicted
            ),
            1.0,
        )
    )

    return {
        "trace_covector":
            trace_cov.tolist(),

        "trace_covector_norm":
            float(
                np.linalg.norm(
                    trace_cov
                )
            ),

        "direct_contraction":
            direct,

        "predicted_contraction":
            predicted,

        "relative_error":
            relative_error,

        "identity_pass":
            relative_error
            <
            1.0e-12,
    }


def _decompose_q_up(
    q_up: np.ndarray,
) -> dict[
    str,
    np.ndarray,
]:
    """Lower the first index and return total-symmetric and hook pieces."""
    q_cov = lower_first_index(
        q_up
    )

    parts = symmetric_hook_decomposition(
        q_cov
    )

    return {
        "q_cov":
            q_cov,

        "totally_symmetric":
            parts[
                "totally_symmetric"
            ],

        "hook":
            parts[
                "hook_symmetric"
            ],
    }


def _rest_electron_spinor() -> np.ndarray:
    return np.array(
        [
            1.0 + 0j,
            0j,
            0j,
            0j,
        ],
        dtype=np.complex128,
    )


def _rest_positron_spinor() -> np.ndarray:
    return np.array(
        [
            0j,
            0j,
            0j,
            1.0 + 0j,
        ],
        dtype=np.complex128,
    )


def _generic_spinor() -> np.ndarray:
    return np.array(
        [
            1.0 + 0.2j,
            0.3 - 0.4j,
            -0.2 + 0.9j,
            0.5 + 0.1j,
        ],
        dtype=np.complex128,
    )


def rest_pair_source_parts() -> dict[
    str,
    np.ndarray,
]:
    """Return decomposition of the equal-amplitude V24A rest pair."""
    q_pair = (
        wheeler_trace_altered_nonmetricity(
            _rest_electron_spinor()
        )
        +
        wheeler_trace_altered_nonmetricity(
            _rest_positron_spinor()
        )
    )

    return _decompose_q_up(
        q_pair
    )


def generic_source_parts() -> dict[
    str,
    np.ndarray,
]:
    """Return the V24A generic algebraic witness decomposition."""
    return _decompose_q_up(
        wheeler_trace_altered_nonmetricity(
            _generic_spinor()
        )
    )


def rest_pair_bms_spin1_trace_gate() -> dict[
    str,
    Any,
]:
    """Test direct overlap of the clean rest pair with the trace-vector mode."""
    source = rest_pair_source_parts()[
        "totally_symmetric"
    ]

    trace = lorentz_trace_covector(
        source
    )

    source_norm = float(
        np.linalg.norm(
            source
        )
    )

    trace_norm = float(
        np.linalg.norm(
            trace
        )
    )

    basis_results = []

    for index in range(
        4
    ):
        vector = np.zeros(
            4
        )

        vector[
            index
        ] = 1.0

        result = trace_carrier_coupling_identity(
            source,
            vector,
        )

        basis_results.append(
            {
                "basis_index":
                    index,

                "direct_contraction":
                    result[
                        "direct_contraction"
                    ],

                "predicted_contraction":
                    result[
                        "predicted_contraction"
                    ],

                "relative_error":
                    result[
                        "relative_error"
                    ],
            }
        )

    max_overlap = max(
        abs(
            float(
                row[
                    "direct_contraction"
                ]
            )
        )
        for row
        in basis_results
    )

    zero_trace = (
        trace_norm
        <
        1.0e-12
        *
        max(
            source_norm,
            1.0,
        )
    )

    zero_overlap = (
        max_overlap
        <
        1.0e-12
        *
        max(
            source_norm,
            1.0,
        )
    )

    return {
        "rest_pair_total_symmetric_source_nonzero":
            source_norm
            >
            1.0e-14,

        "rest_pair_total_symmetric_source_component_norm":
            source_norm,

        "lorentz_trace_covector":
            trace.tolist(),

        "lorentz_trace_covector_norm":
            trace_norm,

        "lorentz_trace_zero":
            zero_trace,

        "basis_trace_carrier_tests":
            basis_results,

        "maximum_direct_trace_carrier_overlap":
            max_overlap,

        "direct_trace_carrier_overlap_zero":
            zero_overlap,

        "bms_spin1_nonlinear_completion":
            "HOMOTHETIC_CURVATURE_SQUARED",

        "homothetic_curvature_trace_vector_sector":
            True,

        "rest_pair_direct_bms_protected_spin1_source_closed":
            bool(
                zero_trace
                and
                zero_overlap
            ),

        "generic_dirac_spin1_source_closed":
            False,

        "indirect_metric_mixing_source_closed":
            False,

        "component_norm_is_physical_energy":
            False,
    }


def generic_bms_spin1_trace_witness() -> dict[
    str,
    Any,
]:
    """Show why the full Dirac family is not closed by the rest-pair theorem."""
    source = generic_source_parts()[
        "totally_symmetric"
    ]

    trace = lorentz_trace_covector(
        source
    )

    return {
        "trace_covector":
            trace.tolist(),

        "trace_covector_norm":
            float(
                np.linalg.norm(
                    trace
                )
            ),

        "generic_algebraic_trace_carrier_nonzero":
            bool(
                np.linalg.norm(
                    trace
                )
                >
                1.0e-12
            ),

        "spinor_is_on_shell_localized_stationary_source":
            False,

        "source_ward_identity_established":
            False,

        "support_energy_established":
            False,

        "generic_dirac_protected_spin1_closed":
            False,
    }


def hook_to_torsionlike(
    hook: np.ndarray,
) -> np.ndarray:
    """Map H_{a(bc)} hook symmetry to T_[ab]c.

    Define

        T_abc = H_abc - H_bac.

    On the hook subspace with H_a(bc)=H_abc and H_(abc)=0, this map is
    invertible.
    """
    h = np.asarray(
        hook,
        dtype=float,
    )

    if h.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "hook must have shape (4,4,4)"
        )

    if not np.allclose(
        h,
        np.swapaxes(
            h,
            1,
            2,
        ),
        atol=1.0e-12,
        rtol=0.0,
    ):
        raise ValueError(
            "hook must be symmetric in its last two indices"
        )

    return (
        h
        -
        np.swapaxes(
            h,
            0,
            1,
        )
    )


def torsionlike_to_hook(
    torsionlike: np.ndarray,
) -> np.ndarray:
    """Invert T_abc = H_abc-H_bac on the declared hook representation."""
    t = np.asarray(
        torsionlike,
        dtype=float,
    )

    if t.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "torsionlike must have shape (4,4,4)"
        )

    if not np.allclose(
        t,
        -np.swapaxes(
            t,
            0,
            1,
        ),
        atol=1.0e-12,
        rtol=0.0,
    ):
        raise ValueError(
            "torsionlike must be antisymmetric in its first two indices"
        )

    result = np.empty_like(
        t
    )

    for a in range(
        4
    ):
        for b in range(
            4
        ):
            for c in range(
                4
            ):
                result[
                    a,
                    b,
                    c,
                ] = (
                    t[
                        a,
                        b,
                        c,
                    ]
                    +
                    t[
                        a,
                        c,
                        b,
                    ]
                ) / 3.0

    return result


def hook_torsionlike_map_diagnostics() -> dict[
    str,
    Any,
]:
    """Return exact map diagnostics and the rest-pair addition witness."""
    electron_parts = _decompose_q_up(
        wheeler_trace_altered_nonmetricity(
            _rest_electron_spinor()
        )
    )

    positron_parts = _decompose_q_up(
        wheeler_trace_altered_nonmetricity(
            _rest_positron_spinor()
        )
    )

    pair_parts = rest_pair_source_parts()
    generic_parts = generic_source_parts()

    h_e = electron_parts[
        "hook"
    ]

    h_p = positron_parts[
        "hook"
    ]

    h_pair = pair_parts[
        "hook"
    ]

    h_generic = generic_parts[
        "hook"
    ]

    t_e = hook_to_torsionlike(
        h_e
    )

    t_p = hook_to_torsionlike(
        h_p
    )

    t_pair = hook_to_torsionlike(
        h_pair
    )

    t_generic = hook_to_torsionlike(
        h_generic
    )

    reconstructed_pair = torsionlike_to_hook(
        t_pair
    )

    reconstructed_generic = torsionlike_to_hook(
        t_generic
    )

    pair_hook_norm = float(
        np.linalg.norm(
            h_pair
        )
    )

    electron_t_norm = float(
        np.linalg.norm(
            t_e
        )
    )

    pair_t_norm = float(
        np.linalg.norm(
            t_pair
        )
    )

    pair_reconstruction_error = float(
        np.linalg.norm(
            reconstructed_pair
            -
            h_pair
        )
        /
        max(
            pair_hook_norm,
            1.0,
        )
    )

    generic_reconstruction_error = float(
        np.linalg.norm(
            reconstructed_generic
            -
            h_generic
        )
        /
        max(
            float(
                np.linalg.norm(
                    h_generic
                )
            ),
            1.0,
        )
    )

    return {
        "rest_pair_hook_source_nonzero":
            pair_hook_norm
            >
            1.0e-14,

        "rest_pair_hook_component_norm":
            pair_hook_norm,

        "torsionlike_first_pair_antisymmetric":
            bool(
                np.allclose(
                    t_pair,
                    -np.swapaxes(
                        t_pair,
                        0,
                        1,
                    ),
                    atol=1.0e-12,
                    rtol=0.0,
                )
            ),

        "pair_hook_roundtrip_relative_error":
            pair_reconstruction_error,

        "generic_hook_roundtrip_relative_error":
            generic_reconstruction_error,

        "representation_map_invertible_on_declared_hook_space":
            bool(
                pair_reconstruction_error
                <
                1.0e-12
                and
                generic_reconstruction_error
                <
                1.0e-12
            ),

        "electron_positron_hook_same_sign":
            bool(
                np.allclose(
                    h_e,
                    h_p,
                    atol=1.0e-12,
                    rtol=0.0,
                )
            ),

        "electron_positron_torsionlike_same_sign":
            bool(
                np.allclose(
                    t_e,
                    t_p,
                    atol=1.0e-12,
                    rtol=0.0,
                )
            ),

        "pair_torsionlike_equals_two_single":
            bool(
                np.allclose(
                    t_pair,
                    2.0
                    *
                    t_e,
                    atol=1.0e-12,
                    rtol=0.0,
                )
            ),

        "electron_torsionlike_component_norm":
            electron_t_norm,

        "pair_torsionlike_component_norm":
            pair_t_norm,

        "pair_torsionlike_component_norm_over_single":
            pair_t_norm
            /
            electron_t_norm,

        "component_norm_is_lorentz_invariant":
            False,

        "component_norm_is_source_energy":
            False,

        "representation_map_is_physical_action_match":
            False,

        "healthy_propagating_vector_match_established":
            False,

        "universal_metric_bridge_established":
            False,
    }


def marzo_2026_vector_graviton_bridge_template() -> dict[
    str,
    Any,
]:
    """Encode only the published structural facts needed for AGMINER reranking."""
    return {
        "reference":
            "ARXIV_2603_24008",

        "quadratic_vector_graviton_mixing":
            True,

        "shared_linear_gauge_transformation":
            (
                "DELTA_H_ab=PARTIAL_(a_XI_b); "
                "DELTA_V_a=M^-1_PARTIAL_a(PARTIAL_DOT_XI)"
            ),

        "massless_spin2_propagates":
            True,

        "massive_spin1_propagates":
            True,

        "unitary_open_region_reported":
            True,

        "reported_unitary_sign_conditions":
            "v1<0 AND hv1>0 AND k1<0",

        "radiatively_unstable_fine_tuning_required_for_quadratic_health":
            False,

        "consistent_cubic_deformation_found":
            True,

        "consistent_quartic_order_noether_test_passed":
            True,

        "vector_transformation_lie_derivative_at_first_deformation":
            True,

        "gravitational_interaction_universality_recovered_in_bootstrap":
            True,

        "external_dirac_source_coupling_derived":
            False,

        "vector_identified_with_v24c_hook_torsionlike_mode":
            False,

        "affine_geometric_identification_completed":
            False,

        "universal_neutral_payload_metric_response_from_dirac_source_established":
            False,

        "canonical_source_charge_per_joule_established":
            False,

        "finite_payload_outward_sign_established":
            False,

        "complete_energy_ledger_established":
            False,

        "promotion_status":
            "BRIDGE_TEMPLATE_ONLY",
    }


def v24c_frontier_rerank() -> list[
    dict[
        str,
        Any,
    ]
]:
    """Return the post-V24C candidate-family ordering."""
    rest_spin1 = rest_pair_bms_spin1_trace_gate()
    generic_spin1 = generic_bms_spin1_trace_witness()
    hook = hook_torsionlike_map_diagnostics()
    ward = rest_pair_fronsdal_ward_scout()
    marzo = marzo_2026_vector_graviton_bridge_template()

    return [
        {
            "priority":
                1,

            "branch":
                "DIRAC_HOOK_TO_TORSIONLIKE_PROTECTED_VECTOR_ACTION_MATCH",

            "status":
                "HIGHEST_PRIORITY_OPEN_SOURCE_SIDE",

            "reason":
                (
                    "EXACT_NONZERO_DIRAC_HOOK_SOURCE_AND_EXACT_"
                    "PAIR_ANTISYMMETRIC_REPRESENTATION_MAP"
                ),

            "rest_pair_hook_nonzero":
                hook[
                    "rest_pair_hook_source_nonzero"
                ],

            "pair_source_purity_survives_map":
                hook[
                    "pair_torsionlike_equals_two_single"
                ],

            "healthy_vector_action_match":
                False,

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                1,

            "branch":
                "MARZO_2026_QUADRATIC_VECTOR_GRAVITON_MIXING",

            "status":
                "HIGHEST_PRIORITY_OPEN_BRIDGE_SIDE",

            "reason":
                (
                    "QUADRATIC_METRIC_VECTOR_MIXING_PLUS_HEALTHY_"
                    "MASSLESS_SPIN2_MASSIVE_SPIN1_AND_QUARTIC_"
                    "NOETHER_COMPLETION"
                ),

            "quadratic_vector_graviton_mixing":
                marzo[
                    "quadratic_vector_graviton_mixing"
                ],

            "dirac_hook_source_match":
                False,

            "complete_affine_identification":
                False,

            "complete_energy_ledger":
                False,
        },
        {
            "priority":
                2,

            "branch":
                "SYMMETRY_FIRST_TORSIONLIKE_VECTOR_CATALOGUE",

            "status":
                "OPEN_PROTECTED_VECTOR_ACTION_LIBRARY",

            "reason":
                (
                    "PAIR_ANTISYMMETRIC_REPRESENTATION_NOW_HAS_"
                    "EXPLICIT_DIRAC_HOOK_SOURCE_WITNESS"
                ),

            "exact_projector_source_match":
                False,

            "metric_bridge_established":
                False,
        },
        {
            "priority":
                0,

            "branch":
                "BMS_PROTECTED_TS_SPIN1_CLEAN_REST_PAIR_DIRECT",

            "status":
                "CLOSED_ZERO_TRACE_SOURCE_OVERLAP",

            "reason":
                "REST_PAIR_TOTALLY_SYMMETRIC_LORENTZ_TRACE_EXACTLY_ZERO",

            "direct_trace_carrier_overlap_zero":
                rest_spin1[
                    "direct_trace_carrier_overlap_zero"
                ],

            "generic_dirac_spin1_closed":
                False,
        },
        {
            "priority":
                0,

            "branch":
                "BMS_PROTECTED_TS_SPIN3_CLEAN_REST_PAIR_DIRECT_NO_COMPENSATOR",

            "status":
                "CLOSED_BY_V24B_WARD_GATE",

            "reason":
                "DIRECT_FACTORIZED_LOCALIZED_REST_PAIR_FAILS_FRONSDAL_WARD_IDENTITY",

            "maximum_normalized_ward_residual":
                ward[
                    "maximum_normalized_ward_residual"
                ],

            "compensating_current_closed":
                False,
        },
        {
            "priority":
                3,

            "branch":
                "GENERIC_ONSHELL_DIRAC_BMS_TS_SPIN1",

            "status":
                "OPEN_BUT_SOURCE_REALIZATION_NOT_ESTABLISHED",

            "reason":
                "GENERIC_ALGEBRAIC_DIRAC_WITNESS_HAS_NONZERO_TOTAL_SYMMETRIC_TRACE",

            "generic_trace_nonzero":
                generic_spin1[
                    "generic_algebraic_trace_carrier_nonzero"
                ],

            "on_shell_source":
                False,

            "support_energy":
                False,
        },
        {
            "priority":
                4,

            "branch":
                "COMPENSATED_OR_GENERAL_ONSHELL_DIRAC_SPIN3",

            "status":
                "OPEN_LOWER_PRIORITY",

            "reason":
                "V24B_CLOSED_ONLY_UNCOMPENSATED_REST_PAIR",

            "metric_bridge_established":
                False,
        },
    ]


def _insert_rule_once(
    storage: Storage,
    *,
    family: str,
    family_version: str,
    rule_type: str,
    rule: dict[
        str,
        Any,
    ],
    proof_reference: str,
) -> int:
    """Insert one region rule idempotently."""
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
            family,
            family_version,
            rule_type,
            proof_reference,
        ),
    ).fetchone()

    if (
        existing is not None
        and
        int(
            existing[
                "count"
            ]
        )
        >
        0
    ):
        return 0

    storage.add_region_rule(
        family=
            family,

        family_version=
            family_version,

        rule_type=
            rule_type,

        rule=
            rule,

        proof_reference=
            proof_reference,
    )

    return 1


def persist_v24c_region_rules(
    storage: Storage,
) -> int:
    """Persist only the exact rest-pair protected spin-one source closure."""
    gate = rest_pair_bms_spin1_trace_gate()

    return _insert_rule_once(
        storage,
        family=
            "032_DIRAC_INTRINSIC_HYPERMOMENTUM_NONMETRICITY",

        family_version=
            "V24C",

        rule_type=
            "REST_PAIR_BMS_HOMOTHETIC_SPIN1_ZERO_TRACE_OVERLAP",

        rule={
            "policy_specific":
                False,

            "scope":
                (
                    "WHEELER_EQUAL_AMPLITUDE_REST_PARTICLE_"
                    "ANTIPARTICLE_SOURCE_DIRECTLY_COUPLED_TO_"
                    "TOTALLY_SYMMETRIC_HOMOTHETIC_TRACE_VECTOR_MODE"
                ),

            "closed":
                True,

            "lorentz_trace_zero":
                gate[
                    "lorentz_trace_zero"
                ],

            "direct_trace_carrier_overlap_zero":
                gate[
                    "direct_trace_carrier_overlap_zero"
                ],

            "generic_dirac_spin1_closed":
                False,

            "indirect_metric_mixing_closed":
                False,

            "hook_sector_closed":
                False,

            "torsionlike_vector_sector_closed":
                False,

            "full_metric_affine_gravity_closed":
                False,
        },

        proof_reference=
            "032V24C_REST_PAIR_HOMOTHETIC_TRACE_SOURCE_GATE",
    )
