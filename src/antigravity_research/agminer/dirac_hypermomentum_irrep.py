"""032V24A Dirac-affine nonmetricity source/irrep preflight.

PURPOSE
-------
Reconstruct the explicit Wheeler (2026) GL(4)-Dirac trace-altered
nonmetricity response and perform theorem-level source/representation checks
before any propagating-mode scan.

SCIENTIFIC QUESTIONS
--------------------
- Is the Dirac nonmetricity response nonzero?
- Does it overlap the Weyl/dilation trace?
- Which algebraic rank-three carriers are nonzero?
- Can an equal-amplitude rest spin-up particle/antiparticle pair cancel the
  published torsion response while adding the nonmetricity response?
- Can a direct post-Riemannian force on structureless matter serve as the
  project's universal payload bridge?
- What does reciprocal two-sector quadratic mixing imply for cross response
  versus visible-visible off-state response?

IMPORTANT LIMITS
----------------
The total-symmetric/hook split below is an index-symmetry decomposition, not a
Barnes-Rivers spin projector. Component norms are diagnostics only; they are
not Lorentz invariants, energies, probabilities, or physical coupling
fractions. Wheeler's algebraic source-response is not itself a healthy
propagating nonmetricity realization.

Literature anchors: Wheeler, EPJC 86, 484 (2026), arXiv:2601.09013;
Iosifidis & Hehl, Phys. Lett. B 850, 138498 (2024), arXiv:2310.15595;
Barker, Marzo & Santoni, arXiv:2505.23894; Percacci & Sezgin, JHEP 01
(2026) 042, arXiv:2508.14211.

CLAIM_CLASSIFICATION=
LITERATURE_RECONSTRUCTION_PLUS_PROJECT_DERIVED_ALGEBRAIC_PREFLIGHT

This module does not establish a healthy propagating mode, canonical source
charge, universal physical metric, antigravity sign, finite-payload response,
energy efficiency, empirical viability, or a device.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .storage import Storage

ETA = np.diag([-1.0, 1.0, 1.0, 1.0])


def _as_spinor(
    spinor: np.ndarray | list[complex] | tuple[complex, ...],
) -> np.ndarray:
    """Return a finite four-component complex spinor."""
    psi = np.asarray(spinor, dtype=np.complex128)

    if psi.shape != (4,):
        raise ValueError(
            "spinor must contain exactly four complex components"
        )

    if (
        not np.all(np.isfinite(psi.real))
        or not np.all(np.isfinite(psi.imag))
    ):
        raise ValueError(
            "spinor components must be finite"
        )

    return psi


def dirac_component_bilinears(
    spinor: np.ndarray | list[complex] | tuple[complex, ...],
) -> dict[str, Any]:
    """Return Wheeler component bilinears D, R and I."""
    psi = _as_spinor(spinor)

    products = (
        np.conjugate(psi)[:, None]
        *
        psi[None, :]
    )

    return {
        "D":
            (
                np.abs(psi) ** 2
            ).astype(float),

        "R":
            np.real(
                products
            ).astype(float),

        "I":
            np.imag(
                products
            ).astype(float),
    }


def wheeler_trace_altered_nonmetricity(
    spinor: np.ndarray | list[complex] | tuple[complex, ...],
    *,
    alpha_over_kappa: float = 1.0,
) -> np.ndarray:
    """Reconstruct Wheeler Eq. (28), returned as q[c,a,b]."""
    s = float(
        alpha_over_kappa
    )

    if not np.isfinite(
        s
    ):
        raise ValueError(
            "alpha_over_kappa must be finite"
        )

    bil = (
        dirac_component_bilinears(
            spinor
        )
    )

    d = bil[
        "D"
    ]

    r = bil[
        "R"
    ]

    im = bil[
        "I"
    ]

    dm, dn, dr, ds = map(
        float,
        d,
    )

    i_mn = float(
        im[
            0,
            1,
        ]
    )

    i_mr = float(
        im[
            0,
            2,
        ]
    )

    i_ms = float(
        im[
            0,
            3,
        ]
    )

    i_nr = float(
        im[
            1,
            2,
        ]
    )

    i_ns = float(
        im[
            1,
            3,
        ]
    )

    i_rs = float(
        im[
            2,
            3,
        ]
    )

    r_mn = float(
        r[
            0,
            1,
        ]
    )

    r_mr = float(
        r[
            0,
            2,
        ]
    )

    r_ms = float(
        r[
            0,
            3,
        ]
    )

    r_nr = float(
        r[
            1,
            2,
        ]
    )

    r_ns = float(
        r[
            1,
            3,
        ]
    )

    r_rs = float(
        r[
            2,
            3,
        ]
    )

    q = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    q[
        0
    ] = (
        4.0
        *
        s
        *
        np.array(
            [
                [
                    0.0,
                    i_mn,
                    i_mr,
                    i_ms,
                ],
                [
                    i_mn,
                    0.0,
                    0.0,
                    0.0,
                ],
                [
                    i_mr,
                    0.0,
                    0.0,
                    0.0,
                ],
                [
                    i_ms,
                    0.0,
                    0.0,
                    0.0,
                ],
            ]
        )
    )

    q[
        1
    ] = (
        2.0
        *
        s
        *
        np.array(
            [
                [
                    2 * i_ms,
                    i_mr - i_ns,
                    i_mn - i_rs,
                    0.0,
                ],
                [
                    i_mr - i_ns,
                    -2 * i_nr,
                    0.0,
                    i_mn + i_rs,
                ],
                [
                    i_mn - i_rs,
                    0.0,
                    2 * i_nr,
                    i_mr + i_ns,
                ],
                [
                    0.0,
                    i_mn + i_rs,
                    i_mr + i_ns,
                    2 * i_ms,
                ],
            ]
        )
    )

    q[
        2
    ] = (
        2.0
        *
        s
        *
        np.array(
            [
                [
                    -2 * r_ms,
                    r_ns + r_mr,
                    r_rs - r_mn,
                    2 * (
                        dm
                        +
                        ds
                    ),
                ],
                [
                    r_ns + r_mr,
                    -2 * r_nr,
                    2 * (
                        dn
                        -
                        dr
                    ),
                    -r_mn - r_rs,
                ],
                [
                    r_rs - r_mn,
                    2 * (
                        dn
                        -
                        dr
                    ),
                    2 * r_nr,
                    r_ns - r_mr,
                ],
                [
                    2 * (
                        dm
                        +
                        ds
                    ),
                    -r_mn - r_rs,
                    r_ns - r_mr,
                    -2 * r_ms,
                ],
            ]
        )
    )

    q[
        3
    ] = (
        -2.0
        *
        s
        *
        np.array(
            [
                [
                    -2 * i_mr,
                    i_nr + i_ms,
                    0.0,
                    i_rs + i_mn,
                ],
                [
                    i_nr + i_ms,
                    -2 * i_ns,
                    i_rs - i_mn,
                    0.0,
                ],
                [
                    0.0,
                    i_rs - i_mn,
                    -2 * i_mr,
                    i_nr - i_ms,
                ],
                [
                    i_rs + i_mn,
                    0.0,
                    i_nr - i_ms,
                    2 * i_ns,
                ],
            ]
        )
    )

    return q


def lorentz_trace(
    q_up: np.ndarray,
) -> np.ndarray:
    """Return eta^{ab} q^c_ab."""
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
            "q must have shape (4,4,4)"
        )

    return np.einsum(
        "ab,cab->c",
        ETA,
        q,
    )


def lower_first_index(
    q_up: np.ndarray,
) -> np.ndarray:
    """Lower the first index with eta=(-,+,+,+)."""
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
            "q must have shape (4,4,4)"
        )

    return np.einsum(
        "cd,dab->cab",
        ETA,
        q,
    )


def symmetric_hook_decomposition(
    q_cov: np.ndarray,
) -> dict[
    str,
    np.ndarray,
]:
    """Split q_c(ab) into totally symmetric and hook index symmetries."""
    q = np.asarray(
        q_cov,
        dtype=float,
    )

    if q.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "q must have shape (4,4,4)"
        )

    if not np.allclose(
        q,
        np.swapaxes(
            q,
            1,
            2,
        ),
        rtol=0.0,
        atol=1e-12,
    ):
        raise ValueError(
            "q must be symmetric in its last two indices"
        )

    total = np.empty_like(
        q
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
                total[
                    a,
                    b,
                    c,
                ] = (
                    q[
                        a,
                        b,
                        c,
                    ]
                    +
                    q[
                        b,
                        a,
                        c,
                    ]
                    +
                    q[
                        c,
                        a,
                        b,
                    ]
                ) / 3.0

    return {
        "totally_symmetric":
            total,

        "hook_symmetric":
            q
            -
            total,
    }


def source_irrep_diagnostics(
    spinor: np.ndarray | list[complex] | tuple[complex, ...],
    *,
    alpha_over_kappa: float = 1.0,
) -> dict[
    str,
    Any,
]:
    """Return conservative V24A algebraic source diagnostics."""
    q_up = (
        wheeler_trace_altered_nonmetricity(
            spinor,
            alpha_over_kappa=
                alpha_over_kappa,
        )
    )

    q_cov = (
        lower_first_index(
            q_up
        )
    )

    parts = (
        symmetric_hook_decomposition(
            q_cov
        )
    )

    total = parts[
        "totally_symmetric"
    ]

    hook = parts[
        "hook_symmetric"
    ]

    nq = float(
        np.linalg.norm(
            q_cov
        )
    )

    nt = float(
        np.linalg.norm(
            total
        )
    )

    nh = float(
        np.linalg.norm(
            hook
        )
    )

    trace = (
        lorentz_trace(
            q_up
        )
    )

    if nq:
        tf = (
            nt
            /
            nq
        ) ** 2

        hf = (
            nh
            /
            nq
        ) ** 2

    else:
        tf = 0.0
        hf = 0.0

    reconstruction_error = float(
        np.linalg.norm(
            q_cov
            -
            total
            -
            hook
        )
        /
        max(
            nq,
            1.0,
        )
    )

    orthogonality = float(
        np.vdot(
            total,
            hook,
        ).real
        /
        max(
            nq
            *
            nq,
            1.0,
        )
    )

    return {
        "nonmetricity_response_nonzero":
            nq
            >
            1e-14,

        "last_pair_symmetric":
            bool(
                np.allclose(
                    q_up,
                    np.swapaxes(
                        q_up,
                        1,
                        2,
                    ),
                    atol=1e-12,
                    rtol=0.0,
                )
            ),

        "lorentz_trace":
            trace.tolist(),

        "lorentz_trace_norm":
            float(
                np.linalg.norm(
                    trace
                )
            ),

        "weyl_dilation_trace_overlap_zero":
            bool(
                np.linalg.norm(
                    trace
                )
                <
                1e-12
                *
                max(
                    nq,
                    1.0,
                )
            ),

        "totally_symmetric_carrier_nonzero":
            nt
            >
            1e-14,

        "hook_symmetric_carrier_nonzero":
            nh
            >
            1e-14,

        "component_tensor_norm":
            nq,

        "component_totally_symmetric_norm":
            nt,

        "component_hook_symmetric_norm":
            nh,

        "component_totally_symmetric_norm_fraction":
            tf,

        "component_hook_symmetric_norm_fraction":
            hf,

        "component_norm_is_lorentz_invariant":
            False,

        "component_norm_is_field_energy":
            False,

        "decomposition_reconstruction_relative_error":
            reconstruction_error,

        "decomposition_orthogonality_relative_inner_product":
            orthogonality,

        "exact_propagating_spin_projector_overlap_established":
            False,

        "canonical_normalization_established":
            False,

        "physical_metric_bridge_established":
            False,

        "source_charge_per_joule_established":
            False,

        "complete_energy_ledger":
            False,
    }


def _rest_spinup_torsion_matrix(
    *,
    particle: str,
    alpha_over_kappa: float = 1.0,
) -> np.ndarray:
    """Return Wheeler's unit-amplitude rest-spin-up torsion special case."""
    s = float(
        alpha_over_kappa
    )

    if not np.isfinite(
        s
    ):
        raise ValueError(
            "alpha_over_kappa must be finite"
        )

    if particle not in {
        "electron",
        "positron",
    }:
        raise ValueError(
            "particle must be 'electron' or 'positron'"
        )

    sign = (
        1.0
        if particle
        ==
        "electron"
        else
        -1.0
    )

    t = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    t[
        2,
        0,
        3,
    ] = (
        sign
        *
        0.5
        *
        s
    )

    t[
        2,
        3,
        0,
    ] = (
        -sign
        *
        0.5
        *
        s
    )

    return t


def rest_spinup_special_case() -> dict[
    str,
    Any,
]:
    """Return published equal-amplitude rest spin-up e-/e+ witnesses."""
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

    q_e = (
        wheeler_trace_altered_nonmetricity(
            electron
        )
    )

    q_p = (
        wheeler_trace_altered_nonmetricity(
            positron
        )
    )

    expected = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    expected[
        2,
        0,
        3,
    ] = 4.0

    expected[
        2,
        3,
        0,
    ] = 4.0

    t_e = (
        _rest_spinup_torsion_matrix(
            particle=
                "electron"
        )
    )

    t_p = (
        _rest_spinup_torsion_matrix(
            particle=
                "positron"
        )
    )

    q_pair = (
        q_e
        +
        q_p
    )

    t_pair = (
        t_e
        +
        t_p
    )

    return {
        "electron_nonmetricity_matches_published_special_case":
            bool(
                np.allclose(
                    q_e,
                    expected,
                    atol=1e-14,
                    rtol=0.0,
                )
            ),

        "positron_nonmetricity_matches_published_special_case":
            bool(
                np.allclose(
                    q_p,
                    expected,
                    atol=1e-14,
                    rtol=0.0,
                )
            ),

        "equal_amplitude_particle_antiparticle_same_nonmetricity_sign":
            bool(
                np.allclose(
                    q_e,
                    q_p,
                    atol=1e-14,
                    rtol=0.0,
                )
            ),

        "equal_amplitude_particle_antiparticle_opposite_torsion_sign":
            bool(
                np.allclose(
                    t_e,
                    -t_p,
                    atol=1e-14,
                    rtol=0.0,
                )
            ),

        "pair_torsion_response_cancels":
            bool(
                np.linalg.norm(
                    t_pair
                )
                <
                1e-14
            ),

        "pair_nonmetricity_response_adds":
            bool(
                np.allclose(
                    q_pair,
                    2
                    *
                    q_e,
                    atol=1e-14,
                    rtol=0.0,
                )
            ),

        "pair_nonmetricity_component_norm_over_single":
            float(
                np.linalg.norm(
                    q_pair
                )
                /
                np.linalg.norm(
                    q_e
                )
            ),

        "pair_hidden_vector_charge_cancellation_established":
            False,

        "pair_total_spin_cancellation_established":
            False,

        "pair_support_cost_established":
            False,

        "pair_source_energy_established":
            False,

        "electron_irrep":
            source_irrep_diagnostics(
                electron
            ),

        "positron_irrep":
            source_irrep_diagnostics(
                positron
            ),
    }


def direct_structureless_payload_gate() -> dict[
    str,
    Any,
]:
    """Encode Iosifidis-Hehl zero-hypermomentum geodesic result narrowly."""
    return {
        "scope":
            "POINT_TEST_BODY_WITH_ZERO_INTRINSIC_HYPERMOMENTUM",

        "payload_intrinsic_hypermomentum":
            False,

        "direct_post_riemannian_microstructure_force_available":
            False,

        "usual_riemannian_geodesic_recovered":
            True,

        "universal_metric_backreaction_closed":
            False,

        "universal_physical_metric_bridge_established":
            False,

        "direct_connection_force_is_project_target":
            False,
    }


def quadratic_mixing_reciprocity(
    *,
    visible_inverse_propagator: float,
    hidden_inverse_propagator: float,
    mixing: float,
) -> dict[
    str,
    Any,
]:
    """Exact one-mode 2x2 reciprocal quadratic mixing identity.

    For K=[[a,b],[b,c]], health requires a>0, c>0, ac-b^2>0.

    With G=K^-1 and G_vv^0=1/a,

        G_vh^2 = (G_vv-G_vv^0) G_hh.

    At weak b, cross response is O(b), while the visible-visible correction
    is O(b^2). This is a structural portal fact, not a MAG action match.
    """
    a = float(
        visible_inverse_propagator
    )

    c = float(
        hidden_inverse_propagator
    )

    b = float(
        mixing
    )

    if not all(
        np.isfinite(
            x
        )
        for x in (
            a,
            b,
            c,
        )
    ):
        raise ValueError(
            "quadratic coefficients must be finite"
        )

    det = (
        a
        *
        c
        -
        b
        *
        b
    )

    healthy = (
        a
        >
        0.0
        and
        c
        >
        0.0
        and
        det
        >
        0.0
    )

    if not healthy:
        return {
            "healthy_positive_quadratic_block":
                False,

            "visible_inverse_propagator":
                a,

            "hidden_inverse_propagator":
                c,

            "mixing":
                b,

            "determinant":
                det,

            "cross_response":
                None,

            "visible_offstate_correction":
                None,

            "hidden_response":
                None,

            "reciprocity_identity_relative_error":
                None,
        }

    g_vv = (
        c
        /
        det
    )

    g_vh = (
        -b
        /
        det
    )

    g_hh = (
        a
        /
        det
    )

    g0 = (
        1.0
        /
        a
    )

    delta = (
        b
        *
        b
        /
        (
            a
            *
            det
        )
    )

    lhs = (
        g_vh
        *
        g_vh
    )

    rhs = (
        delta
        *
        g_hh
    )

    err = (
        abs(
            lhs
            -
            rhs
        )
        /
        max(
            abs(
                lhs
            ),
            abs(
                rhs
            ),
            1e-300,
        )
    )

    return {
        "healthy_positive_quadratic_block":
            True,

        "visible_inverse_propagator":
            a,

        "hidden_inverse_propagator":
            c,

        "mixing":
            b,

        "determinant":
            det,

        "visible_response_with_mixing":
            g_vv,

        "visible_response_without_mixing":
            g0,

        "visible_offstate_correction":
            delta,

        "cross_response":
            g_vh,

        "hidden_response":
            g_hh,

        "cross_response_squared":
            lhs,

        "visible_delta_times_hidden_response":
            rhs,

        "reciprocity_identity_relative_error":
            err,

        "weak_mixing_cross_order":
            1,

        "weak_mixing_visible_offstate_order":
            2,

        "physical_action_match_established":
            False,

        "canonical_metric_affine_normalization_established":
            False,

        "empirical_bound_mapped":
            False,
    }


def weak_mixing_scaling_scout(
    mixing_values: tuple[
        float,
        ...,
    ] = (
        1e-1,
        3e-2,
        1e-2,
        3e-3,
        1e-3,
    ),
) -> list[
    dict[
        str,
        Any,
    ]
]:
    """Dimensionless scout of the exact weak-mixing scaling."""
    rows = []

    for b in mixing_values:
        result = (
            quadratic_mixing_reciprocity(
                visible_inverse_propagator=
                    1.0,

                hidden_inverse_propagator=
                    1.0,

                mixing=
                    float(
                        b
                    ),
            )
        )

        if not result[
            "healthy_positive_quadratic_block"
        ]:
            raise RuntimeError(
                "default weak-mixing scout left healthy domain"
            )

        rows.append(
            {
                "mixing":
                    float(
                        b
                    ),

                "abs_cross_response":
                    abs(
                        float(
                            result[
                                "cross_response"
                            ]
                        )
                    ),

                "visible_offstate_correction":
                    float(
                        result[
                            "visible_offstate_correction"
                        ]
                    ),

                "hidden_response":
                    float(
                        result[
                            "hidden_response"
                        ]
                    ),

                "reciprocity_identity_relative_error":
                    float(
                        result[
                            "reciprocity_identity_relative_error"
                        ]
                    ),

                "physical_units_assigned":
                    False,

                "empirical_bound_assigned":
                    False,
            }
        )

    return rows


def literature_intersection_atlas() -> list[
    dict[
        str,
        Any,
    ]
]:
    """Return non-promotional V24A theory intersections."""
    return [
        {
            "priority":
                0,

            "sector":
                "WEYL_DILATION_TRACE",

            "wheeler_dirac_algebraic_overlap":
                False,

            "status":
                "CLOSED_FOR_EXPLICIT_WHEELER_DIRAC_SOURCE",

            "reason":
                "EXACT_VANISHING_LORENTZ_TRACE",

            "exact_dilation_trace_projection_established":
                True,

            "exact_spin_projector_overlap_established":
                False,

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                1,

            "sector":
                "TOTALLY_SYMMETRIC_TRACEFREE",

            "wheeler_dirac_algebraic_overlap":
                True,

            "status":
                "OPEN_FOR_EXACT_PROJECTOR_AND_METRIC_BRIDGE_TEST",

            "reason":
                "NONZERO_ALGEBRAIC_CARRIER_ONLY",

            "published_health_context":
                (
                    "SYMMETRY_FIRST_MASSLESS_SPIN1_OR_SPIN3_"
                    "POSSIBLE_UNDER_BMS_ASSUMPTIONS"
                ),

            "radiative_protection_priority":
                "HIGHEST",

            "exact_spin_projector_overlap_established":
                False,

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                2,

            "sector":
                "HOOK_SYMMETRIC_TRACEFREE",

            "wheeler_dirac_algebraic_overlap":
                True,

            "status":
                "OPEN_FOR_EXACT_PROJECTOR_AND_METRIC_BRIDGE_TEST",

            "reason":
                "NONZERO_ALGEBRAIC_CARRIER_ONLY",

            "published_health_context":
                (
                    "TREE_LEVEL_MASSIVE_SPIN3_OR_SPIN3_PLUS_SPIN0_"
                    "POSSIBLE_IN_PERCACCI_SEZGIN_CLASS"
                ),

            "radiative_protection_established_for_that_class":
                False,

            "exact_spin_projector_overlap_established":
                False,

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                0,

            "sector":
                "DIRECT_STRUCTURELESS_CONNECTION_FORCE",

            "wheeler_dirac_algebraic_overlap":
                None,

            "status":
                "NOT_A_UNIVERSAL_PAYLOAD_BRIDGE",

            "reason":
                "ZERO_PAYLOAD_HYPERMOMENTUM_RECOVERS_GEODESIC",

            "exact_spin_projector_overlap_established":
                None,

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                1,

            "sector":
                "TORSION_CANCELLED_PARTICLE_ANTIPARTICLE_PAIR_SOURCE",

            "wheeler_dirac_algebraic_overlap":
                True,

            "status":
                "OPEN_MICROSCOPIC_SOURCE_WITNESS",

            "reason":
                (
                    "PUBLISHED_SPECIAL_CASE_TORSION_OPPOSITE_"
                    "NONMETRICITY_SAME_SIGN"
                ),

            "hidden_charge_neutrality_established":
                False,

            "support_cost_established":
                False,

            "exact_spin_projector_overlap_established":
                False,

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                1,

            "sector":
                "WEAK_UNIVERSAL_METRIC_MIXING_PLUS_LARGE_HIDDEN_CHARGE",

            "wheeler_dirac_algebraic_overlap":
                True,

            "status":
                "OPEN_STRUCTURAL_PORTAL_STRATEGY",

            "reason":
                (
                    "CROSS_RESPONSE_LINEAR_IN_MIXING_"
                    "VISIBLE_OFFSTATE_CORRECTION_QUADRATIC_IN_MIXING"
                ),

            "physical_action_match_established":
                False,

            "source_charge_per_joule_established":
                False,

            "empirical_bound_mapped":
                False,

            "universal_metric_bridge_established":
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
    existing = (
        storage.connection.execute(
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
    )

    if (
        existing is not None
        and int(
            existing[
                "count"
            ]
        ) > 0
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


def persist_v24a_region_rules(
    storage: Storage,
) -> int:
    """Persist only two narrow policy-independent closures."""
    family = (
        "032_DIRAC_INTRINSIC_HYPERMOMENTUM_NONMETRICITY"
    )

    inserted = (
        _insert_rule_once(
            storage,

            family=
                family,

            family_version=
                "V24A",

            rule_type=
                "ZERO_WEYL_DILATION_OVERLAP",

            rule={
                "policy_specific":
                    False,

                "scope":
                    "EXPLICIT_WHEELER_2026_GL4_DIRAC_SOURCE",

                "closed":
                    True,

                "weyl_dilation_trace_overlap":
                    False,

                "tracefree_nonmetricity_source_response":
                    True,

                "totally_symmetric_tracefree_closed":
                    False,

                "hook_symmetric_tracefree_closed":
                    False,

                "full_dirac_hypermomentum_closed":
                    False,

                "full_metric_affine_gravity_closed":
                    False,

                "universal_metric_bridge_established":
                    False,
            },

            proof_reference=
                "032V24A_DIRAC_NONMETRICITY_IRREP_PREFLIGHT",
        )
    )

    inserted += (
        _insert_rule_once(
            storage,

            family=
                family,

            family_version=
                "V24A",

            rule_type=
                "DIRECT_STRUCTURELESS_CONNECTION_FORCE_NOT_UNIVERSAL",

            rule={
                "policy_specific":
                    False,

                "scope":
                    (
                        "DIRECT_POST_RIEMANNIAN_TEST_BODY_FORCE_WITH_"
                        "ZERO_PAYLOAD_INTRINSIC_HYPERMOMENTUM"
                    ),

                "closed":
                    True,

                "usual_riemannian_geodesic_recovered":
                    True,

                "metric_backreaction_closed":
                    False,

                "universal_physical_metric_bridge_closed":
                    False,

                "microstructured_payload_force_closed":
                    False,

                "full_metric_affine_gravity_closed":
                    False,
            },

            proof_reference=
                "032V24A_STRUCTURELESS_PAYLOAD_BRIDGE_PREFLIGHT",
        )
    )

    return inserted
