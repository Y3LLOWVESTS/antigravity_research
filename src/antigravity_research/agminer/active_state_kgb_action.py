"""032V25A active-state kinetic-gravity-braiding action gate.

PURPOSE
-------
Construct the first explicit post-V25 A1 action which simultaneously has:

1. an intrinsic hidden source operator;
2. exact scalar shift symmetry;
3. one universal physical metric for ordinary neutral matter;
4. scalar-metric kinetic braiding that vanishes in the trivial off-state;
5. nonzero active-state matter/scalar response on a scalar-gradient
   background;
6. no direct V17/R5 kinetic-conformal matter operator at tree level.

The proposed action class is the cubic shift-symmetric Horndeski / kinetic
gravity braiding theory

    S =
      integral sqrt(-g) [
          Mpl^2 R / 2
          + X
          + beta X Box(phi) / Lambda^3
          + L_hidden
          + partial_mu(phi) J5_hidden^mu / f_psi
      ]
      + S_matter[g, matter],

with

    X = -1/2 g^{mu nu} partial_mu(phi) partial_nu(phi).

The hidden axial source term is the same exact-shift-compatible microscopic
operator used in V15-V19:

    J5_hidden^mu
      = bar(Psi) gamma^mu gamma^5 Psi.

IMPORTANT
---------
This run proves an ACTION-EXISTENCE / STRUCTURAL PORTAL result only.

It does NOT prove:

- a static self-consistent hidden source solution in the new KGB action;
- outward gravitational sign;
- finite-payload response;
- useful response per joule;
- nonlinear stability;
- radiative naturalness of the complete source-coupled theory;
- empirical viability;
- support/control feasibility;
- complete operating energy below 10 MJ.

No action oracle is created.

CLAIM_CLASSIFICATION=
EXPLICIT_ACTION_EXISTENCE_AND_ACTIVE_OFFSTATE_BRAIDING_PREFLIGHT
"""

from __future__ import annotations

from typing import Any

import math

from .storage import Storage


VERIFIED = "VERIFIED"
PARTIAL = "PARTIAL"
OPEN = "OPEN"
FAILED = "FAILED"


def action_specification() -> dict[str, Any]:
    """Return the explicit V25A action and its declared structural properties."""

    return {
        "family":
            "SHIFT_SYMMETRIC_CUBIC_KGB_HIDDEN_AXIAL_ACTIVE_STATE",

        "scalar_kinetic_definition":
            "X=-1/2*g^munu*d_mu(phi)*d_nu(phi)",

        "gravity_sector":
            "MPL^2*R/2",

        "scalar_sector":
            "X + beta*X*BOX(phi)/Lambda^3",

        "hidden_source_sector":
            (
                "L_hidden + "
                "d_mu(phi)*bar(Psi)*gamma^mu*gamma5*Psi/f_psi"
            ),

        "ordinary_matter_sector":
            "S_matter[g_munu,ordinary_matter]",

        "physical_metric":
            "g_munu",

        "ordinary_matter_minimally_coupled":
            True,

        "one_universal_physical_metric":
            True,

        "exact_constant_shift_symmetry":
            True,

        "source_operator_preserves_constant_shift":
            True,

        "horndeski_second_order_structure":
            True,

        "bulk_galileon_radiative_protection_context":
            True,

        "complete_source_coupled_naturalness_certified":
            False,

        "direct_v17_c1_matter_operator_present":
            False,

        "tree_level_r5_same_operator_present":
            False,

        "negative_mass_required":
            False,
    }


def off_state_tree_gate() -> dict[str, Any]:
    """Return the exact classical off-state limit.

    The off-state is

        hidden axial current = 0
        d_mu phi = 0
        X = 0.

    Therefore the cubic braiding and its debraided matter coupling vanish.

    This is a tree-level structural statement. It does not certify the
    quantum off-state ledger.
    """

    return {
        "hidden_source_on":
            False,

        "scalar_gradient_nonzero":
            False,

        "x_nonzero":
            False,

        "cubic_braiding_active":
            False,

        "debraided_scalar_matter_coupling_active":
            False,

        "direct_scalar_ordinary_matter_vertex":
            False,

        "ordinary_matter_metric":
            "g_munu",

        "tree_level_active_offstate_separation":
            True,

        "r5_same_tree_operator_absent":
            True,

        "gravitational_scalar_interactions_absent":
            False,

        "quantum_gravitational_descendants_certified":
            False,

        "offstate_empirical_closure":
            False,
    }


def static_spacelike_state(
    y: float,
    *,
    beta_sign: int = 1,
) -> dict[str, Any]:
    """Return exact dimensionless minimal-cubic static-gradient diagnostics.

    Define

        y
          = beta^2 |grad(phi)|^4
            / (2 Mpl^2 Lambda^6).

    For a static spacelike gradient, the debraided cubic-Horndeski equation
    gives the principal kinetic coefficients

        Z_time = Z_perp = 1-y
        Z_parallel = 1+3y.

    The nonrelativistic matter coupling before canonical normalization obeys

        Mpl |g_m|
          = sqrt(y/2).

    Normalizing the scalar using Z_time gives

        Mpl |g_m,c|
          = sqrt[y / (2(1-y))].

    The latter exists only on the hyperbolic side y<1.
    """

    value = float(
        y
    )

    if not math.isfinite(
        value
    ) or value < 0.0:
        raise ValueError(
            "y must be finite and non-negative"
        )

    if beta_sign not in (
        -1,
        1,
    ):
        raise ValueError(
            "beta_sign must be -1 or +1"
        )

    z_time = (
        1.0
        -
        value
    )

    z_perp = (
        1.0
        -
        value
    )

    z_parallel = (
        1.0
        +
        3.0
        *
        value
    )

    uncanonical_mpl = (
        beta_sign
        *
        math.sqrt(
            value
            /
            2.0
        )
    )

    canonical_mpl = None

    if z_time > 0.0:
        canonical_mpl = (
            beta_sign
            *
            math.sqrt(
                value
                /
                (
                    2.0
                    *
                    z_time
                )
            )
        )

    return {
        "y":
            value,

        "z_time":
            z_time,

        "z_transverse":
            z_perp,

        "z_parallel":
            z_parallel,

        "hyperbolic_principal_part":
            bool(
                z_time > 0.0
                and
                z_perp > 0.0
                and
                z_parallel > 0.0
            ),

        "kinetic_degenerate":
            bool(
                abs(
                    z_time
                )
                <
                1.0e-14
            ),

        "uncanonical_matter_coupling_times_mpl":
            uncanonical_mpl,

        "canonical_matter_coupling_times_mpl":
            canonical_mpl,

        "active_debraided_matter_coupling_nonzero":
            bool(
                value > 0.0
            ),

        "outward_gravity_sign_established":
            False,
    }


def required_state_for_canonical_gain(
    gain_times_planck: float,
) -> dict[str, Any]:
    """Invert the minimal-cubic canonical gain relation exactly.

    If

        A = Mpl |g_c|,

    then

        A^2 = y/[2(1-y)]

    so

        y = 2 A^2 / (1+2 A^2)
        Z_time = 1/(1+2 A^2).

    Thus large gain forces the minimal cubic model toward kinetic degeneracy.
    """

    gain = float(
        gain_times_planck
    )

    if not math.isfinite(
        gain
    ) or gain < 0.0:
        raise ValueError(
            "gain_times_planck must be finite and non-negative"
        )

    gain_sq = (
        gain
        *
        gain
    )

    denominator = (
        1.0
        +
        2.0
        *
        gain_sq
    )

    y = (
        2.0
        *
        gain_sq
        /
        denominator
    )

    z_time = (
        1.0
        /
        denominator
    )

    state = static_spacelike_state(
        y
    )

    return {
        "requested_canonical_gain_times_planck":
            gain,

        "required_y":
            y,

        "required_z_time_margin":
            z_time,

        "reconstructed_canonical_gain_times_planck":
            (
                abs(
                    float(
                        state[
                            "canonical_matter_coupling_times_mpl"
                        ]
                    )
                )
                if state[
                    "canonical_matter_coupling_times_mpl"
                ]
                is not None
                else None
            ),

        "near_kinetic_degeneracy":
            bool(
                z_time
                <
                1.0e-3
            ),

        "strong_coupling_scale_certified":
            False,
    }


def quadratic_cross_response_invariance(
    *,
    metric_kinetic: float,
    scalar_kinetic: float,
    mixing: float,
) -> dict[str, Any]:
    """Show that diagonalizing kinetic mixing does not erase physical response.

    Consider one scalarized operator channel

        L2 =
          1/2 a h^2
          + b h pi
          + 1/2 c pi^2
          + h T
          + pi J.

    The original cross propagator is

        G_hpi = -b/(a c-b^2).

    Under the local invertible field redefinition

        h_prime = h + (b/a) pi,

    the kinetic matrix diagonalizes, but the physical metric variable becomes

        h = h_prime - (b/a) pi

    and the matter source therefore couples directly to pi with coefficient
    -b/a.

    The reconstructed J -> h response remains exactly

        -b/(a c-b^2).

    This is an algebraic response-invariance theorem, not a replacement for
    the full tensor Horndeski propagator.
    """

    a = float(
        metric_kinetic
    )

    c = float(
        scalar_kinetic
    )

    b = float(
        mixing
    )

    if not all(
        math.isfinite(
            value
        )
        for value
        in (
            a,
            b,
            c,
        )
    ):
        raise ValueError(
            "quadratic coefficients must be finite"
        )

    determinant = (
        a
        *
        c
        -
        b
        *
        b
    )

    healthy = bool(
        a > 0.0
        and
        c > 0.0
        and
        determinant > 0.0
    )

    if not healthy:
        return {
            "healthy_quadratic_channel":
                False,

            "determinant":
                determinant,

            "original_cross_response":
                None,

            "shifted_cross_response":
                None,

            "relative_error":
                None,
        }

    original = (
        -b
        /
        determinant
    )

    shifted_scalar_kinetic = (
        c
        -
        b
        *
        b
        /
        a
    )

    direct_metric_source_to_scalar = (
        -b
        /
        a
    )

    shifted = (
        direct_metric_source_to_scalar
        /
        shifted_scalar_kinetic
    )

    relative_error = (
        abs(
            original
            -
            shifted
        )
        /
        max(
            abs(
                original
            ),
            abs(
                shifted
            ),
            1.0,
        )
    )

    return {
        "healthy_quadratic_channel":
            True,

        "determinant":
            determinant,

        "original_cross_response":
            original,

        "shifted_scalar_kinetic":
            shifted_scalar_kinetic,

        "direct_metric_source_to_scalar_after_diagonalization":
            direct_metric_source_to_scalar,

        "shifted_cross_response":
            shifted,

        "relative_error":
            relative_error,

        "response_invariant_under_declared_field_redefinition":
            bool(
                relative_error
                <
                1.0e-12
            ),

        "full_tensor_horndeski_nonremovability_certified":
            False,
    }


def active_offstate_cross_response_demo() -> dict[str, Any]:
    """Return a controlled operator-level active/off-state comparison."""

    off = quadratic_cross_response_invariance(
        metric_kinetic=
            1.0,

        scalar_kinetic=
            1.0,

        mixing=
            0.0,
    )

    active = quadratic_cross_response_invariance(
        metric_kinetic=
            1.0,

        scalar_kinetic=
            1.0,

        mixing=
            0.25,
    )

    return {
        "offstate_cross_response":
            off[
                "original_cross_response"
            ],

        "active_cross_response":
            active[
                "original_cross_response"
            ],

        "offstate_zero":
            abs(
                float(
                    off[
                        "original_cross_response"
                    ]
                )
            )
            <
            1.0e-14,

        "active_nonzero":
            abs(
                float(
                    active[
                        "original_cross_response"
                    ]
                )
            )
            >
            1.0e-6,

        "active_response_field_redefinition_invariant":
            active[
                "response_invariant_under_declared_field_redefinition"
            ],

        "full_action_tensor_projection_completed":
            False,
    }


def protection_gate() -> dict[str, Any]:
    """Separate protected bulk structure from unproved full EFT naturalness."""

    return {
        "exact_constant_shift_symmetry":
            True,

        "flat_space_galileon_nonrenormalization_context":
            True,

        "weakly_broken_galileon_gravity_context":
            True,

        "hidden_axial_derivative_source_preserves_constant_shift":
            True,

        "hidden_source_preserves_full_galileon_symmetry":
            False,

        "full_source_coupled_rg_calculated":
            False,

        "full_source_coupled_naturalness_certified":
            False,

        "protection_status":
            PARTIAL,
    }


def source_and_conservation_gate() -> dict[str, Any]:
    """Return the source-provenance and conservation claim boundary."""

    return {
        "hidden_axial_derivative_source_operator_exists":
            True,

        "source_operator_historical_provenance":
            "032V15_TO_V19",

        "exact_scalar_constant_shift_preserved":
            True,

        "zero_net_derivative_source_topology_available":
            True,

        "new_kgb_static_selfconsistent_source_solved":
            False,

        "new_kgb_hidden_fermion_meanfield_reoptimized":
            False,

        "full_metric_scalar_hidden_source_conservation_solved":
            False,

        "source_ward_compatibility_status":
            OPEN,
    }


def v25a_action_existence_gate() -> dict[str, Any]:
    """Return the complete conservative V25A action-existence classification."""

    action = action_specification()
    offstate = off_state_tree_gate()
    source = source_and_conservation_gate()
    protection = protection_gate()

    active_reference = static_spacelike_state(
        0.10
    )

    response = active_offstate_cross_response_demo()

    return {
        "explicit_covariant_action_exists":
            True,

        "action_family":
            action[
                "family"
            ],

        "one_universal_physical_metric":
            action[
                "one_universal_physical_metric"
            ],

        "exact_constant_shift_symmetry":
            action[
                "exact_constant_shift_symmetry"
            ],

        "tree_level_active_offstate_separation":
            offstate[
                "tree_level_active_offstate_separation"
            ],

        "r5_same_tree_operator_absent":
            offstate[
                "r5_same_tree_operator_absent"
            ],

        "active_braiding_reference_hyperbolic":
            active_reference[
                "hyperbolic_principal_part"
            ],

        "active_debraided_matter_coupling_exists":
            active_reference[
                "active_debraided_matter_coupling_nonzero"
            ],

        "operator_cross_response_survives_diagonalization":
            response[
                "active_response_field_redefinition_invariant"
            ],

        "full_tensor_nonremovable_crosspropagator_certified":
            False,

        "microscopic_source_operator_exists":
            source[
                "hidden_axial_derivative_source_operator_exists"
            ],

        "new_action_source_solution_exists":
            source[
                "new_kgb_static_selfconsistent_source_solved"
            ],

        "full_source_ward_compatibility_certified":
            False,

        "bulk_protection_context_exists":
            True,

        "full_source_coupled_naturalness_certified":
            protection[
                "full_source_coupled_naturalness_certified"
            ],

        "outward_sign_established":
            False,

        "finite_payload_response_established":
            False,

        "source_charge_per_joule_established":
            False,

        "complete_operating_energy_established":
            False,

        "action_oracle_authorized":
            False,

        "blind_parameter_scan_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "decision":
            (
                "GREEN_PARTIAL_EXPLICIT_ACTIVE_STATE_KGB_ACTION_EXISTS_"
                "WITH_SINGLE_UNIVERSAL_METRIC_AND_TREE_OFFSTATE_SEPARATION_"
                "BUT_FULL_TENSOR_CROSSPROP_SOURCE_RG_SIGN_AND_ENERGY_OPEN"
            ),

        "next":
            (
                "032V25B_GENERALIZED_KGB_CANONICAL_GAIN_STRONG_COUPLING_"
                "RG_UV_AND_HIDDEN_SOURCE_SELFCONSISTENCY_GATE"
            ),
    }


def persist_v25a_metadata(
    storage: Storage,
) -> None:
    """Persist scheduler metadata only."""

    metadata = {
        "032v25a_action_family":
            "SHIFT_SYMMETRIC_CUBIC_KGB_HIDDEN_AXIAL_ACTIVE_STATE",

        "032v25a_explicit_covariant_action_exists":
            "1",

        "032v25a_one_universal_physical_metric":
            "1",

        "032v25a_tree_active_offstate_separation":
            "1",

        "032v25a_r5_same_tree_operator_absent":
            "1",

        "032v25a_full_tensor_nonremovable_crossprop_certified":
            "0",

        "032v25a_new_action_static_source_solution":
            "0",

        "032v25a_full_source_rg_uv_certified":
            "0",

        "032v25a_action_oracle_authorized":
            "0",

        "032v25a_blind_parameter_scan_authorized":
            "0",

        "agminer_next_family":
            (
                "GENERALIZED_KGB_CANONICAL_GAIN_STRONG_COUPLING_"
                "RG_UV_HIDDEN_SOURCE_SELFCONSISTENCY"
            ),
    }

    for key, value in metadata.items():
        storage.set_metadata(
            key,
            value,
        )
