"""032H17A9 — Percacci-Sezgin projective 1+ exact source/pole gate.

This gate tests whether the clean V24 equal-rest Dirac source has nonzero
overlap with the healthy massive 1+ pole of the projective-invariant
torsion-free Percacci-Sezgin MAG action.

A8 already established:
- both projective source-trace constraints pass;
- clean V24 1+ support is nonzero;
- exact 1+ source matching is authorized.

A9 establishes only a partial result.

A GREEN result here means:
- healthy published Case-I 1+ pole;
- convention-matched V24 source;
- required torsion-free source projection;
- projective source traces remain zero;
- exact massive 1+ pole numerator is nonzero.

It does NOT establish:
- complete same-action Wheeler + Percacci-Sezgin matter;
- full diffeomorphism Ward consistency;
- the same-action HOOK17 metric numerator;
- complete operating energy;
- a practical antigravity model or device.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    lower_first_index,
    wheeler_trace_altered_nonmetricity,
)

from .hook17_native_protected_2plus_atlas import (
    h17a8_summary,
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


def a8_provenance_gate() -> dict[str, Any]:
    """Require the completed A8 state."""

    result = h17a8_summary()

    passed = bool(
        result[
            "a7_provenance_pass"
        ]
        and
        result[
            "current_declared_protected_2plus_atlas_closed"
        ]
        and
        result[
            "clean_v24_projective_source_trace_constraints_pass"
        ]
        and
        result[
            "clean_v24_projective_1plus_support_nonzero"
        ]
        and
        result[
            "projective_1plus_exact_source_match_authorized"
        ]
        and
        not result[
            "hook17_closed"
        ]
    )

    return {
        "a8_decision":
            result[
                "decision"
            ],

        "a8_provenance_pass":
            passed,

        "projective_trace_prefilter_pass":
            result[
                "clean_v24_projective_source_trace_constraints_pass"
            ],

        "clean_1plus_nonzero":
            result[
                "clean_v24_projective_1plus_support_nonzero"
            ],

        "clean_1plus_norm2":
            result[
                "clean_v24_1plus_norm2"
            ],

        "exact_1plus_source_match_authorized":
            result[
                "projective_1plus_exact_source_match_authorized"
            ],

        "hook17_open":
            not result[
                "hook17_closed"
            ],
    }


def percacci_sezgin_case_i_gate() -> dict[str, Any]:
    """Reconstruct a representative healthy Case-I parameter point."""

    a0 = 1.0
    big_a = 1.0
    b = 1.0
    h7 = -1.0

    c = (
        -16.0
        *
        b
        /
        25.0
    )

    h11 = (
        -10.0
        *
        h7
        /
        3.0
    )

    denominator = (
        17.0
        *
        h11
        +
        40.0
        *
        h7
    )

    mass2 = (
        3.0
        *
        b
        /
        denominator
    )

    residue = (
        6.0
        /
        denominator
    )

    expected_mass2 = (
        -9.0
        *
        b
        /
        (
            50.0
            *
            h7
        )
    )

    expected_residue = (
        -9.0
        /
        (
            25.0
            *
            h7
        )
    )

    healthy = bool(
        a0
        >
        0.0
        and
        abs(
            big_a
        )
        >
        TOL
        and
        b
        >
        0.0
        and
        h7
        <
        0.0
        and
        mass2
        >
        0.0
        and
        residue
        >
        0.0
        and
        np.isclose(
            mass2,
            expected_mass2,
            atol=
                TOL,
            rtol=
                0.0,
        )
        and
        np.isclose(
            residue,
            expected_residue,
            atol=
                TOL,
            rtol=
                0.0,
        )
    )

    return {
        "case":
            "PERCACCI_SEZGIN_CASE_I",

        "a0":
            a0,

        "A":
            big_a,

        "B":
            b,

        "C":
            c,

        "h7":
            h7,

        "h11":
            h11,

        "m_plus_squared":
            mass2,

        "m_plus":
            float(
                np.sqrt(
                    mass2
                )
            ),

        "r_plus":
            residue,

        "expected_case_i_m_plus_squared":
            expected_mass2,

        "expected_case_i_r_plus":
            expected_residue,

        "case_i_relations_pass":
            healthy,

        "massive_1plus_tachyon_free":
            bool(
                mass2
                >
                0.0
            ),

        "massive_1plus_residue_positive":
            bool(
                residue
                >
                0.0
            ),

        "published_protected_projective_family":
            True,

        "full_wheeler_matter_same_action":
            False,
    }


def _clean_rest_spinors() -> tuple[np.ndarray, np.ndarray]:
    """Return the established clean rest spin-up e-/e+ pair."""

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

    return (
        electron,
        positron,
    )


def clean_wheeler_response_cov() -> np.ndarray:
    """Return the fully covariant clean V24 nonmetricity response."""

    electron, positron = _clean_rest_spinors()

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
            "clean Wheeler source must be real"
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
            "clean Wheeler source must have shape (4,4,4)"
        )

    return result


def wheeler_to_ps_raw_source() -> np.ndarray:
    """Map Wheeler source convention to Percacci-Sezgin tau[c,a,b].

    The explicit pair of transpositions encodes the variational index map.

    For the clean source the final Wheeler pair is symmetric, so this mapped
    tensor numerically equals the clean fully covariant response.
    """

    response = clean_wheeler_response_cov()

    hypermomentum_abc = np.transpose(
        response,
        (
            2,
            1,
            0,
        ),
    )

    tau_raw = np.transpose(
        hypermomentum_abc,
        (
            2,
            0,
            1,
        ),
    )

    return np.asarray(
        tau_raw,
        dtype=float,
    )


def _nonzero_rows(
    tensor: np.ndarray,
) -> list[dict[str, Any]]:
    """Return sparse nonzero rank-three components."""

    rows: list[dict[str, Any]] = []

    for c in range(
        4
    ):
        for a in range(
            4
        ):
            for b in range(
                4
            ):
                value = float(
                    tensor[
                        c,
                        a,
                        b,
                    ]
                )

                if abs(
                    value
                ) <= TOL:
                    continue

                rows.append(
                    {
                        "c":
                            c,

                        "a":
                            a,

                        "b":
                            b,

                        "value":
                            value,
                    }
                )

    return rows


def wheeler_ps_source_map_gate() -> dict[str, Any]:
    """Diagnose the convention-matched raw source."""

    response = clean_wheeler_response_cov()
    raw = wheeler_to_ps_raw_source()

    symmetry_error = float(
        np.max(
            np.abs(
                response
                -
                np.swapaxes(
                    response,
                    1,
                    2,
                )
            )
        )
    )

    difference = float(
        np.linalg.norm(
            raw
            -
            response
        )
    )

    rows = _nonzero_rows(
        raw
    )

    expected = {
        (
            2,
            0,
            3,
        ):
            8.0,

        (
            2,
            3,
            0,
        ):
            8.0,
    }

    expected_pass = bool(
        len(
            rows
        )
        ==
        2
        and
        all(
            np.isclose(
                raw[
                    index
                ],
                value,
                atol=
                    TOL,
                rtol=
                    0.0,
            )
            for index, value in expected.items()
        )
    )

    return {
        "response_final_pair_symmetry_error":
            symmetry_error,

        "response_final_pair_symmetric":
            bool(
                symmetry_error
                <=
                TOL
            ),

        "raw_source_matches_clean_response_in_this_state":
            bool(
                difference
                <=
                TOL
            ),

        "raw_response_difference_norm":
            difference,

        "raw_source_norm":
            float(
                np.linalg.norm(
                    raw
                )
            ),

        "raw_nonzero_components":
            rows,

        "raw_expected_components_pass":
            expected_pass,

        "wheeler_to_ps_variational_source_map_convention_matched":
            bool(
                symmetry_error
                <=
                TOL
                and
                difference
                <=
                TOL
                and
                expected_pass
            ),

        "overall_wheeler_source_normalization_fixed_physically":
            False,

        "same_action_completion_established":
            False,
    }


def torsion_free_ps_source() -> np.ndarray:
    """Project tau onto the P&S torsion-free first-third symmetric space."""

    raw = wheeler_to_ps_raw_source()

    return (
        0.5
        *
        (
            raw
            +
            np.swapaxes(
                raw,
                0,
                2,
            )
        )
    )


def torsion_free_source_gate() -> dict[str, Any]:
    """Verify the exact torsion-free source projection."""

    source = torsion_free_ps_source()

    symmetry_error = float(
        np.max(
            np.abs(
                source
                -
                np.swapaxes(
                    source,
                    0,
                    2,
                )
            )
        )
    )

    rows = _nonzero_rows(
        source
    )

    expected = {
        (
            0,
            3,
            2,
        ):
            4.0,

        (
            2,
            0,
            3,
        ):
            4.0,

        (
            2,
            3,
            0,
        ):
            4.0,

        (
            3,
            0,
            2,
        ):
            4.0,
    }

    expected_pass = bool(
        len(
            rows
        )
        ==
        4
        and
        all(
            np.isclose(
                source[
                    index
                ],
                value,
                atol=
                    TOL,
                rtol=
                    0.0,
            )
            for index, value in expected.items()
        )
    )

    return {
        "torsion_free_first_third_symmetry_error":
            symmetry_error,

        "torsion_free_first_third_symmetric":
            bool(
                symmetry_error
                <=
                TOL
            ),

        "torsion_free_source_norm":
            float(
                np.linalg.norm(
                    source
                )
            ),

        "torsion_free_nonzero_components":
            rows,

        "torsion_free_expected_components_pass":
            expected_pass,

        "torsion_free_projection_reconstructed":
            bool(
                symmetry_error
                <=
                TOL
                and
                expected_pass
            ),

        "component_norm_is_physical_energy":
            False,
    }


def torsion_free_projection_identity_gate() -> dict[str, Any]:
    """Verify raw/projected sources couple identically to allowed fields."""

    raw = wheeler_to_ps_raw_source()
    projected = torsion_free_ps_source()

    carrier = np.arange(
        64,
        dtype=float,
    ).reshape(
        (
            4,
            4,
            4,
        )
    )

    carrier = (
        carrier
        /
        63.0
    )

    carrier_tf = (
        0.5
        *
        (
            carrier
            +
            np.swapaxes(
                carrier,
                0,
                2,
            )
        )
    )

    raw_contraction = float(
        np.sum(
            raw
            *
            carrier_tf
        )
    )

    projected_contraction = float(
        np.sum(
            projected
            *
            carrier_tf
        )
    )

    difference = abs(
        raw_contraction
        -
        projected_contraction
    )

    return {
        "test_field_first_third_symmetric":
            bool(
                np.allclose(
                    carrier_tf,
                    np.swapaxes(
                        carrier_tf,
                        0,
                        2,
                    ),
                    atol=
                        TOL,
                    rtol=
                        0.0,
                )
            ),

        "raw_source_contraction":
            raw_contraction,

        "projected_source_contraction":
            projected_contraction,

        "contraction_difference":
            difference,

        "torsion_free_source_projection_identity_pass":
            bool(
                difference
                <=
                TOL
            ),
    }


def projected_projective_trace_gate() -> dict[str, Any]:
    """Re-evaluate both projective source constraints after projection."""

    source = torsion_free_ps_source()

    trace_12 = np.einsum(
        "ij,ijk->k",
        ETA,
        source,
    )

    trace_23 = np.einsum(
        "jk,ijk->i",
        ETA,
        source,
    )

    norm_12 = float(
        np.linalg.norm(
            trace_12
        )
    )

    norm_23 = float(
        np.linalg.norm(
            trace_23
        )
    )

    source_norm = float(
        np.linalg.norm(
            source
        )
    )

    scale = max(
        source_norm,
        1.0,
    )

    pass_12 = bool(
        norm_12
        <=
        TOL
        *
        scale
    )

    pass_23 = bool(
        norm_23
        <=
        TOL
        *
        scale
    )

    return {
        "trace_first_second":
            trace_12.tolist(),

        "trace_first_second_norm":
            norm_12,

        "trace_second_third":
            trace_23.tolist(),

        "trace_second_third_norm":
            norm_23,

        "projective_constraint_tau_nu_nu_mu_pass":
            pass_12,

        "projective_constraint_tau_mu_nu_nu_pass":
            pass_23,

        "both_projective_source_trace_constraints_pass":
            bool(
                pass_12
                and
                pass_23
            ),

        "source_norm":
            source_norm,
    }


def div1_tau(
    source: np.ndarray,
    q_up: np.ndarray,
) -> np.ndarray:
    """Return div1(tau)_ab = q^c tau_cab."""

    q = np.asarray(
        q_up,
        dtype=float,
    )

    tau = np.asarray(
        source,
        dtype=float,
    )

    return np.einsum(
        "c,cab->ab",
        q,
        tau,
    )


def antisymmetric_part(
    tensor: np.ndarray,
) -> np.ndarray:
    """Return X_[ab]."""

    value = np.asarray(
        tensor,
        dtype=float,
    )

    return (
        0.5
        *
        (
            value
            -
            value.T
        )
    )


def exact_ps_1plus_pole_source_gate() -> dict[str, Any]:
    """Evaluate the exact P&S Case-I 1+ source numerator."""

    case = percacci_sezgin_case_i_gate()

    mass2 = float(
        case[
            "m_plus_squared"
        ]
    )

    mass = float(
        np.sqrt(
            mass2
        )
    )

    q_up = np.array(
        [
            mass,
            0.0,
            0.0,
            0.0,
        ],
        dtype=float,
    )

    q_cov = (
        ETA
        @
        q_up
    )

    raw = wheeler_to_ps_raw_source()
    projected = torsion_free_ps_source()

    raw_div1 = div1_tau(
        raw,
        q_up,
    )

    projected_div1 = div1_tau(
        projected,
        q_up,
    )

    raw_current = antisymmetric_part(
        raw_div1
    )

    projected_current = antisymmetric_part(
        projected_div1
    )

    raw_norm2 = float(
        np.sum(
            raw_current
            *
            raw_current
        )
    )

    projected_norm2 = float(
        np.sum(
            projected_current
            *
            projected_current
        )
    )

    transverse = (
        ETA
        +
        np.outer(
            q_up,
            q_up,
        )
        /
        mass2
    )

    transverse_q = (
        transverse
        @
        q_cov
    )

    current_after_projector = np.einsum(
        "ac,bd,cd->ab",
        transverse,
        transverse,
        projected_current,
    )

    numerator = float(
        np.einsum(
            "ab,ab->",
            projected_current,
            current_after_projector,
        )
    )

    expected_numerator = (
        8.0
        *
        mass2
    )

    b = float(
        case[
            "B"
        ]
    )

    coefficient_proxy = (
        numerator
        /
        (
            4.0
            *
            b
        )
    )

    return {
        "q_up":
            q_up.tolist(),

        "q_squared":
            float(
                q_up
                @
                ETA
                @
                q_up
            ),

        "m_plus_squared":
            mass2,

        "raw_div1":
            raw_div1.tolist(),

        "raw_antisymmetric_div1":
            raw_current.tolist(),

        "raw_antisymmetric_div1_norm2":
            raw_norm2,

        "naive_raw_rest_1plus_current_zero":
            bool(
                raw_norm2
                <=
                TOL
            ),

        "torsion_free_div1":
            projected_div1.tolist(),

        "torsion_free_antisymmetric_div1":
            projected_current.tolist(),

        "torsion_free_antisymmetric_div1_norm2":
            projected_norm2,

        "torsion_free_projected_rest_1plus_current_nonzero":
            bool(
                projected_norm2
                >
                TOL
            ),

        "expected_current_23":
            -2.0
            *
            mass,

        "expected_current_32":
            2.0
            *
            mass,

        "current_23_matches":
            bool(
                np.isclose(
                    projected_current[
                        2,
                        3,
                    ],
                    -2.0
                    *
                    mass,
                    atol=
                        TOL,
                    rtol=
                        0.0,
                )
            ),

        "current_32_matches":
            bool(
                np.isclose(
                    projected_current[
                        3,
                        2,
                    ],
                    2.0
                    *
                    mass,
                    atol=
                        TOL,
                    rtol=
                        0.0,
                )
            ),

        "transverse_projector_q_cov_norm":
            float(
                np.linalg.norm(
                    transverse_q
                )
            ),

        "on_shell_transverse_projector_pass":
            bool(
                np.linalg.norm(
                    transverse_q
                )
                <=
                TOL
            ),

        "exact_ps_1plus_pole_numerator":
            numerator,

        "expected_exact_numerator":
            expected_numerator,

        "exact_numerator_matches_8m2":
            bool(
                np.isclose(
                    numerator,
                    expected_numerator,
                    atol=
                        TOL,
                    rtol=
                        0.0,
                )
            ),

        "exact_ps_1plus_pole_numerator_nonzero":
            bool(
                numerator
                >
                TOL
            ),

        "full_propagator_pole_coefficient_proxy":
            coefficient_proxy,

        "full_propagator_pole_coefficient_proxy_positive":
            bool(
                coefficient_proxy
                >
                0.0
            ),

        "pole_coefficient_proxy_is_physical_coupling":
            False,

        "pole_coefficient_proxy_is_physical_energy":
            False,

        "overall_wheeler_source_normalization_omitted":
            True,

        "interpretation":
            (
                "NONZERO EXACT PERCACCI-SEZGIN CASE-I 1+ "
                "SOURCE NUMERATOR AFTER REQUIRED TORSION-FREE "
                "SOURCE PROJECTION"
            ),
    }


def diffeomorphism_connection_ward_term(
    source: np.ndarray,
    q_up: np.ndarray,
) -> np.ndarray:
    """Return q^a q^b tau_bca."""

    tau = np.asarray(
        source,
        dtype=float,
    )

    q = np.asarray(
        q_up,
        dtype=float,
    )

    return np.einsum(
        "a,b,bca->c",
        q,
        q,
        tau,
    )


def diffeomorphism_ward_gate() -> dict[str, Any]:
    """Evaluate connection-only part of the full diffeo source identity."""

    source = torsion_free_ps_source()

    case = percacci_sezgin_case_i_gate()

    mass = float(
        case[
            "m_plus"
        ]
    )

    rest_q = np.array(
        [
            mass,
            0.0,
            0.0,
            0.0,
        ]
    )

    mixed_q = np.array(
        [
            1.0,
            0.0,
            1.0,
            0.0,
        ]
    )

    rest_residual = (
        diffeomorphism_connection_ward_term(
            source,
            rest_q,
        )
    )

    mixed_residual = (
        diffeomorphism_connection_ward_term(
            source,
            mixed_q,
        )
    )

    rest_norm = float(
        np.linalg.norm(
            rest_residual
        )
    )

    mixed_norm = float(
        np.linalg.norm(
            mixed_residual
        )
    )

    return {
        "published_full_ward_identity":
            (
                "2*i*q^a*sigma_ac + q^a*q^b*tau_bca = 0"
            ),

        "massive_rest_connection_term":
            rest_residual.tolist(),

        "massive_rest_connection_term_norm":
            rest_norm,

        "massive_rest_connection_term_zero":
            bool(
                rest_norm
                <=
                TOL
            ),

        "generic_mixed_q":
            mixed_q.tolist(),

        "generic_mixed_connection_term":
            mixed_residual.tolist(),

        "generic_mixed_connection_term_norm":
            mixed_norm,

        "generic_connection_term_nonzero":
            bool(
                mixed_norm
                >
                TOL
            ),

        "metric_source_sigma_required_for_generic_ward":
            bool(
                mixed_norm
                >
                TOL
            ),

        "sigma_from_same_wheeler_projective_action_derived":
            False,

        "full_diffeomorphism_matter_ward_established":
            False,

        "localized_onshell_matter_source_established":
            False,
    }


def source_component_rows() -> list[dict[str, Any]]:
    """Return raw and projected source components."""

    rows: list[dict[str, Any]] = []

    for stage, tensor in (
        (
            "WHEELER_TO_PS_RAW",
            wheeler_to_ps_raw_source(),
        ),
        (
            "PERCACCI_SEZGIN_TORSION_FREE",
            torsion_free_ps_source(),
        ),
    ):
        for row in _nonzero_rows(
            tensor
        ):
            rows.append(
                {
                    "stage":
                        stage,

                    "c":
                        row[
                            "c"
                        ],

                    "a":
                        row[
                            "a"
                        ],

                    "b":
                        row[
                            "b"
                        ],

                    "value":
                        row[
                            "value"
                        ],
                }
            )

    return rows


def h17a9_summary() -> dict[str, Any]:
    """Return conservative A9 result."""

    provenance = a8_provenance_gate()
    case = percacci_sezgin_case_i_gate()
    mapping = wheeler_ps_source_map_gate()
    projection = torsion_free_source_gate()
    identity = torsion_free_projection_identity_gate()
    projective = projected_projective_trace_gate()
    pole = exact_ps_1plus_pole_source_gate()
    diffeo = diffeomorphism_ward_gate()

    partial_green = bool(
        provenance[
            "a8_provenance_pass"
        ]
        and
        case[
            "case_i_relations_pass"
        ]
        and
        mapping[
            "wheeler_to_ps_variational_source_map_convention_matched"
        ]
        and
        projection[
            "torsion_free_projection_reconstructed"
        ]
        and
        identity[
            "torsion_free_source_projection_identity_pass"
        ]
        and
        projective[
            "both_projective_source_trace_constraints_pass"
        ]
        and
        pole[
            "torsion_free_projected_rest_1plus_current_nonzero"
        ]
        and
        pole[
            "exact_numerator_matches_8m2"
        ]
        and
        pole[
            "exact_ps_1plus_pole_numerator_nonzero"
        ]
        and
        pole[
            "full_propagator_pole_coefficient_proxy_positive"
        ]
    )

    return {
        "branch":
            "032H17A9",

        "subgate":
            "PERCACCI_SEZGIN_PROJECTIVE_1PLUS_EXACT_SOURCE_PROJECTOR_WARD",

        "decision":
            (
                "GREEN_PARTIAL_A9_EXACT_PERCACCI_SEZGIN_1PLUS_"
                "POLE_OVERLAP_WITH_PROJECTIVE_TRACE_PASS__"
                "FULL_MATTER_NOETHER_AND_SAME_ACTION_REMAIN_OPEN"
            )
            if partial_green
            else
            "CHECK_A9_SOURCE_MAP_OR_EXACT_POLE_PROJECTOR",

        "a8_provenance_pass":
            provenance[
                "a8_provenance_pass"
            ],

        "percacci_sezgin_case_i_healthy":
            case[
                "case_i_relations_pass"
            ],

        "wheeler_to_ps_source_map_reconstructed":
            mapping[
                "wheeler_to_ps_variational_source_map_convention_matched"
            ],

        "source_map_status":
            (
                "CONVENTION_MATCHED_LINEAR_VARIATIONAL_MAP_"
                "NOT_FULL_SAME_ACTION_COMPLETION"
            ),

        "torsion_free_source_projection_reconstructed":
            projection[
                "torsion_free_projection_reconstructed"
            ],

        "torsion_free_source_projection_identity_pass":
            identity[
                "torsion_free_source_projection_identity_pass"
            ],

        "projective_source_trace_constraints_pass":
            projective[
                "both_projective_source_trace_constraints_pass"
            ],

        "naive_raw_rest_1plus_current_zero":
            pole[
                "naive_raw_rest_1plus_current_zero"
            ],

        "torsion_free_projected_rest_1plus_current_nonzero":
            pole[
                "torsion_free_projected_rest_1plus_current_nonzero"
            ],

        "exact_ps_1plus_pole_numerator":
            pole[
                "exact_ps_1plus_pole_numerator"
            ],

        "exact_ps_1plus_pole_numerator_nonzero":
            pole[
                "exact_ps_1plus_pole_numerator_nonzero"
            ],

        "exact_projective_1plus_pole_overlap_established":
            partial_green,

        "pole_overlap_normalization_complete":
            False,

        "full_diffeomorphism_matter_ward_established":
            diffeo[
                "full_diffeomorphism_matter_ward_established"
            ],

        "metric_source_sigma_required":
            diffeo[
                "metric_source_sigma_required_for_generic_ward"
            ],

        "metric_source_sigma_same_action_derived":
            False,

        "projective_symmetry_of_combined_wheeler_matter_action_established":
            False,

        "full_matter_noether_current_established":
            False,

        "localized_onshell_source_established":
            False,

        "v26b1_metric_numerator_same_action_derived":
            False,

        "same_action_hook17_complete":
            False,

        "universal_physical_metric_established":
            False,

        "finite_payload_antigravity_established":
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
                "032H17A9R1_PERCACCI_SEZGIN_WHEELER_"
                "SAME_ACTION_MATTER_NOETHER_GATE"
            ),

        "next_scientific_question":
            (
                "Does the Wheeler Dirac matter action preserve the "
                "Percacci-Sezgin projective symmetry and supply a metric "
                "source sigma_ab satisfying the full diffeomorphism "
                "Noether identity?"
            ),

        "partial_green":
            partial_green,

        "claim_scope":
            (
                "EXACT CASE-I 1+ POLE SOURCE NUMERATOR FOR THE "
                "CONVENTION-MATCHED CLEAN V24 SOURCE; FULL SAME-ACTION "
                "MATTER NOETHER CONSISTENCY REMAINS OPEN"
            ),
    }
