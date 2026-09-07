"""032V24B protected Dirac source and universal-metric bridge kill gates.

PURPOSE
-------
Use the successful V24A explicit Dirac nonmetricity reconstruction to test the
cheapest remaining protected metric-affine routes before any PDE or parameter
scan.

SCIENTIFIC QUESTIONS
--------------------
1. What rotational carriers occur in the totally symmetric part of the clean
   torsion-cancelled rest particle/antiparticle source witness?
2. Does that same simple localized source satisfy the standard massless
   Fronsdal spin-3 source Ward identity without compensating currents?
3. How suppressed is the first metric-distortion quadratic mixing in the
   symmetry-first totally symmetric EFT when it first appears at dimension
   five and three derivatives?
4. Does the published extended-projective pseudoscalar theory provide a new
   universal neutral-matter metric bridge, or only ordinary Einstein
   stress-energy backreaction after the affine auxiliaries are eliminated?

IMPORTANT CLAIM LIMITS
----------------------
The SO(3) decomposition is a rest-frame screening diagnostic. It is NOT an
exact Lorentz-covariant pole/helicity projection and therefore is not used as
an AGMINER exclusion rule.

The Fronsdal Ward test is exact only for the declared direct coupling of a
factorized localized source

    J^{abc}(x) = S^{abc} f(x)

to the standard massless Fronsdal spin-3 field, with no added compensating
current. Failure closes only that narrow realization.

The dimension-five mixing estimate is EFT power counting, not a matched
Wilson coefficient and not a no-go theorem.

The Einstein stress-only bound applies to a static linearized type-I DEC
source when every productive source element remains at least the declared
stand-off gap from the payload point. It does not constrain a genuinely new
nonminimal universal physical-metric portal.

No candidate, rejection, action oracle, or mechanism metric is created here.

CLAIM_CLASSIFICATION=
THEOREM_LEVEL_SOURCE_COMPATIBILITY_AND_UNIVERSAL_BRIDGE_PREFLIGHT
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hypermomentum_irrep import (
    lower_first_index,
    symmetric_hook_decomposition,
    wheeler_trace_altered_nonmetricity,
)
from .storage import Storage


ETA = np.diag([-1.0, 1.0, 1.0, 1.0])

G_NEWTON = 6.67430e-11
C_LIGHT = 299792458.0
HBARC_EV_M = 1.973269804e-7
MPL_REDUCED_EV = 2.435e27
STANDARD_GRAVITY_M_S2 = 9.80665


def _totally_symmetric_source(
    spinor: np.ndarray,
) -> np.ndarray:
    """Return the fully covariant totally symmetric V24A source component."""
    q_up = wheeler_trace_altered_nonmetricity(
        spinor
    )

    q_cov = lower_first_index(
        q_up
    )

    return symmetric_hook_decomposition(
        q_cov
    )[
        "totally_symmetric"
    ]


def rest_pair_totally_symmetric_source() -> np.ndarray:
    """Return the equal-amplitude rest e-/e+ totally symmetric source witness."""
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
        _totally_symmetric_source(
            electron
        )
        +
        _totally_symmetric_source(
            positron
        )
    )


def totally_symmetric_so3_carriers(
    tensor: np.ndarray,
) -> dict[
    str,
    Any,
]:
    """Decompose a fully symmetric rank-three source into rest-frame SO(3).

    For S_abc=S_(abc):

    - S_ijk -> spin-3 STF plus a spatial spin-1 trace vector;
    - S_0ij -> spin-2 STF plus a scalar trace;
    - S_00i -> a second spin-1 vector;
    - S_000 -> a scalar.

    These Euclidean component norms are diagnostics only. They are not
    Lorentz invariants, pole residues, probabilities, couplings, or energies.
    """
    s = np.asarray(
        tensor,
        dtype=float,
    )

    if s.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "tensor must have shape (4,4,4)"
        )

    permutations = (
        s,
        np.transpose(
            s,
            (
                0,
                2,
                1,
            ),
        ),
        np.transpose(
            s,
            (
                1,
                0,
                2,
            ),
        ),
        np.transpose(
            s,
            (
                1,
                2,
                0,
            ),
        ),
        np.transpose(
            s,
            (
                2,
                0,
                1,
            ),
        ),
        np.transpose(
            s,
            (
                2,
                1,
                0,
            ),
        ),
    )

    if not all(
        np.allclose(
            s,
            permuted,
            rtol=0.0,
            atol=1.0e-12,
        )
        for permuted
        in permutations
    ):
        raise ValueError(
            "tensor must be totally symmetric"
        )

    delta = np.eye(
        3
    )

    spatial = s[
        1:,
        1:,
        1:,
    ]

    spatial_trace = np.einsum(
        "iik->k",
        spatial,
    )

    spin3 = np.empty_like(
        spatial
    )

    for i in range(
        3
    ):
        for j in range(
            3
        ):
            for k in range(
                3
            ):
                spin3[
                    i,
                    j,
                    k,
                ] = (
                    spatial[
                        i,
                        j,
                        k,
                    ]
                    -
                    (
                        delta[
                            i,
                            j,
                        ]
                        *
                        spatial_trace[
                            k
                        ]
                        +
                        delta[
                            i,
                            k,
                        ]
                        *
                        spatial_trace[
                            j
                        ]
                        +
                        delta[
                            j,
                            k,
                        ]
                        *
                        spatial_trace[
                            i
                        ]
                    )
                    /
                    5.0
                )

    zero_ij = s[
        0,
        1:,
        1:,
    ]

    zero_ij_trace = float(
        np.trace(
            zero_ij
        )
    )

    spin2 = (
        zero_ij
        -
        delta
        *
        zero_ij_trace
        /
        3.0
    )

    zero_zero_i = s[
        0,
        0,
        1:,
    ].copy()

    zero_zero_zero = float(
        s[
            0,
            0,
            0,
        ]
    )

    return {
        "spin3_spatial_stf_norm":
            float(
                np.linalg.norm(
                    spin3
                )
            ),

        "spin1_spatial_trace_norm":
            float(
                np.linalg.norm(
                    spatial_trace
                )
            ),

        "spin2_zero_ij_stf_norm":
            float(
                np.linalg.norm(
                    spin2
                )
            ),

        "spin0_zero_ij_trace":
            zero_ij_trace,

        "spin1_zero_zero_i_norm":
            float(
                np.linalg.norm(
                    zero_zero_i
                )
            ),

        "spin0_zero_zero_zero":
            zero_zero_zero,

        "source_component_norm":
            float(
                np.linalg.norm(
                    s
                )
            ),

        "component_norm_is_lorentz_invariant":
            False,

        "exact_massless_helicity_projection_established":
            False,

        "agminer_exclusion_rule_from_so3_screen":
            False,
    }


def rest_pair_so3_screen() -> dict[
    str,
    Any,
]:
    """Return a non-promotional rotational carrier screen for the rest pair."""
    carriers = totally_symmetric_so3_carriers(
        rest_pair_totally_symmetric_source()
    )

    scale = max(
        float(
            carriers[
                "source_component_norm"
            ]
        ),
        1.0,
    )

    tolerance = (
        1.0e-12
        *
        scale
    )

    spin1_norm = float(
        np.hypot(
            carriers[
                "spin1_spatial_trace_norm"
            ],
            carriers[
                "spin1_zero_zero_i_norm"
            ],
        )
    )

    spin3_norm = float(
        carriers[
            "spin3_spatial_stf_norm"
        ]
    )

    spin2_norm = float(
        carriers[
            "spin2_zero_ij_stf_norm"
        ]
    )

    return {
        **carriers,

        "combined_spin1_carrier_norm":
            spin1_norm,

        "rest_frame_spin1_screen_zero":
            spin1_norm
            <
            tolerance,

        "rest_frame_spin3_screen_zero":
            spin3_norm
            <
            tolerance,

        "rest_frame_spin2_carrier_nonzero":
            spin2_norm
            >
            tolerance,

        "rest_frame_so3_screen_is_exact_pole_projection":
            False,

        "rest_frame_so3_screen_closes_protected_spin1_spin3":
            False,

        "full_dirac_source_family_closed":
            False,
    }


def generic_dirac_algebraic_carrier_witness() -> dict[
    str,
    Any,
]:
    """Show that generic algebraic Dirac data can carry spin-1/spin-3 pieces."""
    spinor = np.array(
        [
            1.0 + 0.2j,
            0.3 - 0.4j,
            -0.2 + 0.9j,
            0.5 + 0.1j,
        ],
        dtype=np.complex128,
    )

    carriers = totally_symmetric_so3_carriers(
        _totally_symmetric_source(
            spinor
        )
    )

    scale = max(
        float(
            carriers[
                "source_component_norm"
            ]
        ),
        1.0,
    )

    tolerance = (
        1.0e-12
        *
        scale
    )

    spin1_norm = float(
        np.hypot(
            carriers[
                "spin1_spatial_trace_norm"
            ],
            carriers[
                "spin1_zero_zero_i_norm"
            ],
        )
    )

    spin3_norm = float(
        carriers[
            "spin3_spatial_stf_norm"
        ]
    )

    return {
        **carriers,

        "combined_spin1_carrier_norm":
            spin1_norm,

        "algebraic_spin1_carrier_nonzero":
            spin1_norm
            >
            tolerance,

        "algebraic_spin3_carrier_nonzero":
            spin3_norm
            >
            tolerance,

        "spinor_is_claimed_on_shell_stationary_source":
            False,

        "localized_source_equations_solved":
            False,

        "protecting_gauge_ward_identity_established":
            False,

        "full_dirac_source_family_closed":
            False,
    }


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


def fronsdal_spin3_ward_residual(
    tensor_cov: np.ndarray,
    spatial_wavevector: tuple[
        float,
        float,
        float,
    ],
) -> dict[
    str,
    Any,
]:
    """Evaluate the standard massless spin-3 source Ward condition.

    For the Fronsdal gauge transformation with traceless rank-two gauge
    parameter, a direct source J^{abc} must satisfy that

        D^{bc} = k_a J^{abc}

    has vanishing traceless part. Equivalently D^{bc} must be proportional to
    eta^{bc}. This routine checks that condition for a static Fourier mode

        k_a = (0,kx,ky,kz).

    The test is appropriate for a factorized source tensor multiplied by one
    localized scalar envelope. It does not claim that compensating currents or
    a more general on-shell source cannot restore the Ward identity.
    """
    k_spatial = np.asarray(
        spatial_wavevector,
        dtype=float,
    )

    if k_spatial.shape != (
        3,
    ):
        raise ValueError(
            "spatial_wavevector must contain three components"
        )

    if not np.all(
        np.isfinite(
            k_spatial
        )
    ):
        raise ValueError(
            "spatial_wavevector components must be finite"
        )

    k_norm = float(
        np.linalg.norm(
            k_spatial
        )
    )

    if k_norm <= 0.0:
        raise ValueError(
            "spatial_wavevector must be nonzero"
        )

    source_up = _raise_all_indices(
        tensor_cov
    )

    k_cov = np.array(
        [
            0.0,
            float(
                k_spatial[
                    0
                ]
            ),
            float(
                k_spatial[
                    1
                ]
            ),
            float(
                k_spatial[
                    2
                ]
            ),
        ]
    )

    divergence = np.einsum(
        "a,abc->bc",
        k_cov,
        source_up,
    )

    divergence_trace = float(
        np.einsum(
            "bc,bc->",
            ETA,
            divergence,
        )
    )

    traceless = (
        divergence
        -
        ETA
        *
        divergence_trace
        /
        4.0
    )

    residual_norm = float(
        np.linalg.norm(
            traceless
        )
    )

    source_norm = float(
        np.linalg.norm(
            source_up
        )
    )

    normalized = (
        residual_norm
        /
        max(
            k_norm
            *
            source_norm,
            1.0e-300,
        )
    )

    tolerance = (
        1.0e-12
        *
        max(
            k_norm
            *
            source_norm,
            1.0,
        )
    )

    return {
        "spatial_wavevector":
            k_spatial.tolist(),

        "wavevector_norm":
            k_norm,

        "source_component_norm":
            source_norm,

        "divergence_trace":
            divergence_trace,

        "traceless_divergence_norm":
            residual_norm,

        "normalized_ward_residual":
            normalized,

        "standard_fronsdal_source_ward_pass":
            residual_norm
            <=
            tolerance,

        "compensating_current_included":
            False,

        "source_envelope_factorization_assumed":
            True,
    }


def rest_pair_fronsdal_ward_scout() -> dict[
    str,
    Any,
]:
    """Test the direct rest-pair source against representative spatial modes."""
    source = rest_pair_totally_symmetric_source()

    directions = {
        "x":
            (
                1.0,
                0.0,
                0.0,
            ),

        "y":
            (
                0.0,
                1.0,
                0.0,
            ),

        "z":
            (
                0.0,
                0.0,
                1.0,
            ),

        "xyz":
            (
                1.0,
                1.0,
                1.0,
            ),
    }

    rows = {
        name:
            fronsdal_spin3_ward_residual(
                source,
                direction,
            )
        for name, direction
        in directions.items()
    }

    maximum = max(
        float(
            row[
                "normalized_ward_residual"
            ]
        )
        for row
        in rows.values()
    )

    all_pass = all(
        bool(
            row[
                "standard_fronsdal_source_ward_pass"
            ]
        )
        for row
        in rows.values()
    )

    return {
        "direction_results":
            rows,

        "maximum_normalized_ward_residual":
            maximum,

        "all_tested_spatial_directions_pass":
            all_pass,

        "direct_factorized_localized_rest_pair_without_compensator_closed":
            not all_pass,

        "compensating_current_or_more_general_source_closed":
            False,

        "all_massless_spin3_dirac_sources_closed":
            False,

        "all_metric_affine_gravity_closed":
            False,
    }


def bms_dimension5_metric_mixing_scout(
    *,
    length_m: float = 0.10,
    dimensionless_wilson: float = 1.0,
    reference_scale_ev: float = MPL_REDUCED_EV,
) -> dict[
    str,
    Any,
]:
    """Return the dimension-five three-derivative metric-mixing EFT scout.

    If the leading distortion kinetic term scales as k^2 while the first
    metric-distortion quadratic mixing scales schematically as

        kappa_5 k^3 / Lambda,

    the dimensionless mixing relative to the distortion kinetic term scales as

        epsilon_mix ~ |kappa_5| k / Lambda.

    This is power counting only.
    """
    length = float(
        length_m
    )

    kappa = float(
        dimensionless_wilson
    )

    scale = float(
        reference_scale_ev
    )

    if not np.isfinite(
        length
    ) or length <= 0.0:
        raise ValueError(
            "length_m must be positive and finite"
        )

    if not np.isfinite(
        kappa
    ):
        raise ValueError(
            "dimensionless_wilson must be finite"
        )

    if not np.isfinite(
        scale
    ) or scale <= 0.0:
        raise ValueError(
            "reference_scale_ev must be positive and finite"
        )

    k_ev = (
        HBARC_EV_M
        /
        length
    )

    epsilon = (
        abs(
            kappa
        )
        *
        k_ev
        /
        scale
    )

    target_rows = []

    for target in (
        1.0e-3,
        1.0e-1,
    ):
        required_kappa = (
            target
            *
            scale
            /
            k_ev
        )

        effective_suppression_ev = (
            scale
            /
            required_kappa
        )

        effective_length_m = (
            HBARC_EV_M
            /
            effective_suppression_ev
        )

        target_rows.append(
            {
                "target_mixing":
                    target,

                "required_dimensionless_wilson":
                    required_kappa,

                "effective_suppression_scale_ev":
                    effective_suppression_ev,

                "effective_suppression_length_m":
                    effective_length_m,
            }
        )

    return {
        "length_m":
            length,

        "wavenumber_ev":
            k_ev,

        "reference_scale_ev":
            scale,

        "dimensionless_wilson":
            kappa,

        "natural_dimension5_mixing_ratio":
            epsilon,

        "metric_distortion_mixing_first_dimension":
            5,

        "metric_distortion_mixing_derivative_order":
            3,

        "dominant_distortion_kinetic_dimension":
            4,

        "mixing_subleading_in_declared_eft":
            True,

        "target_rows":
            target_rows,

        "matched_bms_wilson_coefficient_established":
            False,

        "source_to_metric_response_established":
            False,

        "naturalness_no_go_established":
            False,
    }


def einstein_stress_bridge_bound(
    *,
    energy_j: float = 1.0e7,
    stand_off_gap_m: float = 0.10,
    target_acceleration_m_s2: float = STANDARD_GRAVITY_M_S2,
    active_source_factor: float = 4.0,
) -> dict[
    str,
    Any,
]:
    """Return a deliberately generous stress-only Einstein bridge bound.

    For static linearized gravity and a type-I DEC source,

        |epsilon + p1 + p2 + p3| <= 4 epsilon.

    If every productive source element is at least d from the payload point,

        |a| <= 4 G E / (c^2 d^2).

    The factor four is deliberately generous for repulsion. Under diagonal
    DEC the negative active-source magnitude itself has a tighter factor-two
    pointwise bound, but this routine does not rely on that improvement.
    """
    energy = float(
        energy_j
    )

    gap = float(
        stand_off_gap_m
    )

    target = float(
        target_acceleration_m_s2
    )

    factor = float(
        active_source_factor
    )

    if not np.isfinite(
        energy
    ) or energy <= 0.0:
        raise ValueError(
            "energy_j must be positive and finite"
        )

    if not np.isfinite(
        gap
    ) or gap <= 0.0:
        raise ValueError(
            "stand_off_gap_m must be positive and finite"
        )

    if not np.isfinite(
        target
    ) or target <= 0.0:
        raise ValueError(
            "target_acceleration_m_s2 must be positive and finite"
        )

    if not np.isfinite(
        factor
    ) or factor <= 0.0:
        raise ValueError(
            "active_source_factor must be positive and finite"
        )

    acceleration = (
        factor
        *
        G_NEWTON
        *
        energy
        /
        (
            C_LIGHT
            **
            2
            *
            gap
            **
            2
        )
    )

    required_energy = (
        target
        *
        C_LIGHT
        **
        2
        *
        gap
        **
        2
        /
        (
            factor
            *
            G_NEWTON
        )
    )

    return {
        "energy_j":
            energy,

        "stand_off_gap_m":
            gap,

        "active_source_factor":
            factor,

        "acceleration_upper_bound_m_s2":
            acceleration,

        "target_acceleration_m_s2":
            target,

        "target_to_upper_bound_ratio":
            target
            /
            acceleration,

        "energy_required_at_same_bound_j":
            required_energy,

        "required_energy_over_supplied":
            required_energy
            /
            energy,

        "uses_exact_10mj_fail_boundary_as_optimistic_supremum":
            abs(
                energy
                -
                1.0e7
            )
            <
            1.0e-9,

        "complete_device_energy_claim":
            False,

        "nonminimal_metric_portal_closed_by_this_bound":
            False,
    }


def extended_projective_bridge_gate() -> dict[
    str,
    Any,
]:
    """Classify the published EP pseudoscalar as a direct AG metric bridge."""
    bound = einstein_stress_bridge_bound()

    return {
        "theory":
            "BARKER_ZELL_2024_EXTENDED_PROJECTIVE_PSEUDOSCALAR",

        "dirac_motivated_protecting_symmetry":
            True,

        "published_spectrum":
            "MASSLESS_GRAVITON_PLUS_ONE_PSEUDOSCALAR",

        "published_reduced_metric_form":
            "EINSTEIN_HILBERT_PLUS_CANONICAL_PSEUDOSCALAR",

        "published_scalar_fermion_vertex":
            True,

        "published_four_fermion_vertex":
            True,

        "direct_universal_neutral_matter_metric_portal_identified":
            False,

        "universal_bridge_in_declared_reduced_action":
            "EINSTEIN_STRESS_ENERGY_ONLY",

        "direct_fermion_vertex_is_universal_unpolarized_payload_metric_force":
            False,

        "stress_only_bridge_bound":
            bound,

        "strict_sub10mj_reference_gap_reaches_1g":
            bool(
                bound[
                    "acceleration_upper_bound_m_s2"
                ]
                >=
                STANDARD_GRAVITY_M_S2
            ),

        "declared_ep_pseudoscalar_direct_antigravity_bridge_closed":
            True,

        "all_extended_projective_or_iso_weyl_models_closed":
            False,

        "new_added_universal_metric_portal_closed":
            False,
    }


def protected_mode_rerank() -> list[
    dict[
        str,
        Any,
    ]
]:
    """Return the conservative post-V24A/V24B theory-space ranking."""
    rest = rest_pair_so3_screen()
    ward = rest_pair_fronsdal_ward_scout()
    generic = generic_dirac_algebraic_carrier_witness()
    ep = extended_projective_bridge_gate()
    mixing = bms_dimension5_metric_mixing_scout()

    return [
        {
            "priority":
                1,

            "branch":
                "BMS_TOTALLY_SYMMETRIC_PROTECTED_SPIN1_REST_PAIR",

            "status":
                "OPEN_EXACT_SPIN1_SOURCE_CONSTRAINT_REQUIRED",

            "reason":
                "SO3_REST_SCREEN_ZERO_IS_NOT_AN_EXACT_POLE_PROJECTION",

            "rest_frame_so3_spin1_screen_zero":
                rest[
                    "rest_frame_spin1_screen_zero"
                ],

            "hard_exclusion_from_so3_screen":
                False,

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                0,

            "branch":
                "STANDARD_FRONSDAL_F4_SPIN3_DIRECT_REST_PAIR",

            "status":
                "CLOSED_WITHOUT_COMPENSATING_CURRENT",

            "reason":
                "DIRECT_LOCALIZED_FACTORISED_REST_PAIR_FAILS_FRONSDAL_SOURCE_WARD_IDENTITY",

            "maximum_normalized_ward_residual":
                ward[
                    "maximum_normalized_ward_residual"
                ],

            "compensating_current_closed":
                False,

            "all_spin3_dirac_sources_closed":
                False,
        },
        {
            "priority":
                1,

            "branch":
                "BMS_PROTECTED_TOTALLY_SYMMETRIC_SPIN1_ONSHELL_DIRAC",

            "status":
                "HIGHEST_PRIORITY_OPEN_PROTECTED_TS_ROUTE",

            "reason":
                "LOWER_SPIN_PROTECTED_MODE_REQUIRES_EXACT_SOURCE_CONSTRAINT_AND_METRIC_BRIDGE",

            "generic_algebraic_spin1_carrier_exists":
                generic[
                    "algebraic_spin1_carrier_nonzero"
                ],

            "generic_witness_on_shell":
                False,

            "metric_mixing_dimension":
                mixing[
                    "metric_distortion_mixing_first_dimension"
                ],

            "natural_dimension5_mixing_ratio_at_10cm":
                mixing[
                    "natural_dimension5_mixing_ratio"
                ],

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                2,

            "branch":
                "BMS_OR_CATALOGUE_SPIN3_WITH_COMPENSATED_ONSHELL_DIRAC_SOURCE",

            "status":
                "OPEN_ONLY_WITH_WARD_COMPATIBLE_SOURCE_AND_METRIC_BRIDGE",

            "reason":
                "REST_PAIR_DIRECT_SOURCE_FAILS_BUT_COMPENSATED_OR_MORE_GENERAL_ONSHELL_SOURCE_NOT_CLOSED",

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                0,

            "branch":
                "BARKER_ZELL_EXTENDED_PROJECTIVE_PSEUDOSCALAR",

            "status":
                "CLOSED_AS_DECLARED_DIRECT_SUB10MJ_UNIVERSAL_BRIDGE",

            "reason":
                "PUBLISHED_REDUCED_ACTION_HAS_EINSTEIN_METRIC_PLUS_CANONICAL_PSEUDOSCALAR_WITH_FERMION_VERTICES_BUT_NO_NEW_UNIVERSAL_PHYSICAL_METRIC_PORTAL",

            "stress_only_target_gap":
                ep[
                    "stress_only_bridge_bound"
                ][
                    "target_to_upper_bound_ratio"
                ],

            "all_ep_extensions_closed":
                False,
        },
        {
            "priority":
                4,

            "branch":
                "BARKER_ZELL_ISO_WEYL_VECTOR",

            "status":
                "LOW_PRIORITY_OPEN_ONLY_WITH_GENUINELY_NEW_UNIVERSAL_METRIC_PORTAL",

            "reason":
                "HEALTHY_VECTOR_DOES_NOT_BY_ITSELF_SUPPLY_PROJECT_UNIVERSAL_NEUTRAL_MATTER_METRIC_RESPONSE",

            "protected_vector_history_reopened":
                False,
        },
        {
            "priority":
                3,

            "branch":
                "PERCACCI_SEZGIN_SPIN3_OR_SPIN3_PLUS_SPIN0",

            "status":
                "TREE_LEVEL_HEALTHY_NOT_PROMOTED_WITHOUT_PROTECTION_AND_SOURCE_MATCH",

            "reason":
                "LINEAR_HEALTH_DOES_NOT_ESTABLISH_RADIATIVE_PROTECTION_OR_DIRAC_SOURCE_METRIC_BRIDGE",

            "radiative_protection_established":
                False,

            "universal_metric_bridge_established":
                False,
        },
        {
            "priority":
                2,

            "branch":
                "BROADER_HOOK_OR_MIXED_SYMMETRY_MAG_WITH_PROTECTED_LOWER_SPIN_METRIC_ACTIVE_MODE",

            "status":
                "OPEN_NEW_ACTION_REQUIRED",

            "reason":
                "V24A_HOOK_CARRIER_NONZERO_AND_CURRENT_PROTECTED_TS_EP_DIRECT_ROUTES_DO_NOT_COMPLETE_THE_CHAIN",

            "explicit_protecting_action_identified":
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


def persist_v24b_region_rules(
    storage: Storage,
    *,
    energy_policy_id: str,
) -> int:
    """Persist two narrow V24B exclusions without creating candidates."""
    ward = rest_pair_fronsdal_ward_scout()

    inserted = _insert_rule_once(
        storage,
        family=
            "032_DIRAC_INTRINSIC_HYPERMOMENTUM_NONMETRICITY",

        family_version=
            "V24B",

        rule_type=
            "REST_PAIR_DIRECT_FRONSDAL_SPIN3_WARD_FAILURE",

        rule={
            "policy_specific":
                False,

            "scope":
                "WHEELER_EQUAL_AMPLITUDE_REST_PAIR_TIMES_SINGLE_LOCALIZED_SCALAR_ENVELOPE_DIRECTLY_COUPLED_TO_STANDARD_MASSLESS_FRONSDAL_SPIN3_WITHOUT_COMPENSATING_CURRENT",

            "closed":
                True,

            "maximum_normalized_ward_residual":
                ward[
                    "maximum_normalized_ward_residual"
                ],

            "all_tested_spatial_directions_pass":
                ward[
                    "all_tested_spatial_directions_pass"
                ],

            "compensating_current_closed":
                False,

            "more_general_on_shell_dirac_source_closed":
                False,

            "massless_spin1_closed":
                False,

            "hook_sector_closed":
                False,

            "full_metric_affine_gravity_closed":
                False,
        },
        proof_reference=
            "032V24B_FRONSDAL_REST_PAIR_SOURCE_WARD_GATE",
    )

    ep = extended_projective_bridge_gate()

    inserted += _insert_rule_once(
        storage,
        family=
            "032_EXTENDED_PROJECTIVE_PSEUDOSCALAR",

        family_version=
            "BARKER_ZELL_2024_V24B",

        rule_type=
            "STRESS_ONLY_UNIVERSAL_BRIDGE_FAILS_SUB10MJ_10CM_STANDOFF",

        rule={
            "policy_specific":
                True,

            "energy_policy_id":
                str(
                    energy_policy_id
                ),

            "scope":
                "PUBLISHED_EP_PSEUDOSCALAR_REDUCED_ACTION_WITHOUT_ADDED_NONMINIMAL_UNIVERSAL_PHYSICAL_METRIC_PORTAL",

            "closed":
                True,

            "reference_standoff_gap_m":
                0.10,

            "optimistic_energy_boundary_j":
                1.0e7,

            "active_source_factor":
                4.0,

            "acceleration_upper_bound_m_s2":
                ep[
                    "stress_only_bridge_bound"
                ][
                    "acceleration_upper_bound_m_s2"
                ],

            "target_to_upper_bound_ratio":
                ep[
                    "stress_only_bridge_bound"
                ][
                    "target_to_upper_bound_ratio"
                ],

            "all_extended_projective_models_closed":
                False,

            "added_universal_metric_portal_closed":
                False,

            "iso_weyl_vector_closed":
                False,
        },
        proof_reference=
            "032V24B_EP_PSEUDOSCALAR_EINSTEIN_STRESS_BRIDGE_BOUND",
    )

    return inserted
