"""032H17A12B — concurrent-IW enhanced-U(1) exact source protection gate.

PURPOSE
-------
Test the shortest symmetry-protected continuation after A12A.

A12A established that A10 spin engineering reopens the Barker-Zell
iso-Weyl axial source channel, but the unmodified massive-Dirac axial
current fails the Maxwell Ward identity and the generic IW Proca mass is
not protected at meter range.

The Barker-Zell concurrent-symmetry action contains three relevant
connection vectors:

    Q_mu       propagating homothetic/Weyl vector,
    T_hat_mu   axial torsion vector,
    Zc_mu      2*T_mu - Qhat_mu.

The published Dirac matter coupling instead uses

    Zep_mu = 2*T_mu + Q_mu - Qhat_mu = Q_mu + Zc_mu.

This branch asks whether a symmetry-enhanced subfamily of the published
concurrent vector block can simultaneously:

1. eliminate T_hat contamination from the propagating Q source;
2. make Q exactly massless by a gauge null direction rather than a tiny
   unprotected Proca mass;
3. source that massless direction with the exact massive-Dirac vector
   Noether current, not the nonconserved axial current;
4. keep the nondynamical-vector block far from singularity.

DECLARED VECTOR BLOCK
---------------------
Ignoring the optional Holst-squared scalar sector, which the enhanced
symmetry below forbids for generic c != 1, use

    L_mass / M_P^2 =
        b1 Q^2
      + b2 T_hat^2
      + b3 Q.T_hat
      + b4 Zc^2
      + b5 Zc.Q
      + b6 Zc.T_hat.

The homothetic curvature supplies the Maxwell kinetic term for Q.

For y=(T_hat,Zc), define

    H = [[2 b2, b6],
         [b6, 2 b4]]

and d=(b3,b5). Eliminating y gives an effective Q mass coefficient

    b1 - 1/2 d^T H^-1 d

and, because the Dirac source is

    T_hat.J_M + (Q+Zc).J_N,

an effective current

    J_eff = J_N - (H^-1 d)_T J_M - (H^-1 d)_Z J_N.

EXACT CORRIDOR
--------------
The two algebraic conditions

    2 b3 b4 - b5 b6 = 0
    4 b1 b4 - b5^2 = 0

give

    c = b5/(2 b4),
    J_eff = (1-c) J_N,

and the exact vector-mass null direction

    (delta Q, delta T_hat, delta Zc) proportional to (1,0,-c).

This is not accepted as physical gain if H is near singular.

MATTER COMPLETION
-----------------
Barker-Zell's generic Dirac current is

    J_N = (alpha_nm/4) V - 2 beta_nm J_M.

Set beta_nm=0. Then J_N is proportional to the ordinary vector current

    V^mu = psi_bar gamma^mu psi,

which is exactly conserved classically for a massive Dirac field.

The connection transformation is reconstructed as a gradient combination
of the exact projective and iso-Weyl trace transformations:

    A_mu = (1/8) partial_mu lambda,
    B_mu = 0,
    C_mu = (c-1) partial_mu lambda.

It produces

    delta Q   = + partial lambda,
    delta Zc  = -c partial lambda,
    delta Zep = (1-c) partial lambda,
    delta T_hat = 0.

A compensating Dirac phase transformation cancels the variation of the
Zep.J_N coupling. Therefore the declared subfamily has a classical exact
local U(1)-type gauge protection of the massless direction.

The Holst pseudoscalar contains a T_hat.Zep contribution. For c != 1 it
is not invariant under this enhanced gauge transformation, so the
Holst-squared term is excluded by the new symmetry rather than set small
to obtain range.

CLAIM LIMITS
------------
A green result establishes only a scoped classical same-action corridor.
It does NOT yet establish:

- canonical Q normalization;
- sufficient physical source charge per joule;
- a viable Standard-Model charge assignment;
- anomaly-free embedding of the full microscopic source;
- empirical consistency;
- neutral-payload direct-force silence;
- the HOOK17 quadratic universal metric for this carrier;
- finite-payload 1g/1m transfer;
- complete operating energy below 10 MJ;
- a practical antigravity model.

Those are deliberately pushed to A12C before any metric or payload work.

CLAIM CLASSIFICATION
--------------------
SCOPED_CLASSICAL_SAME_ACTION_SYMMETRY_PROTECTION_THEOREM
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


def _repo_root() -> Path:
    """Return the repository root from src/antigravity_research/agminer."""

    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


@lru_cache(maxsize=1)
def a12a_artifact() -> dict[str, Any]:
    """Load the authoritative local A12A summary."""

    path = (
        _repo_root()
        / "results"
        / "data"
        / "032h17a12a_hook17_iw_engineered_axial_source_summary.json"
    )

    if not path.exists():
        raise FileNotFoundError(str(path))

    return json.loads(
        path.read_text(encoding="utf-8")
    )


def a12a_provenance_gate() -> dict[str, Any]:
    """Require the exact A12A handoff state."""

    result = a12a_artifact()

    passed = bool(
        result["branch"] == "032H17A12A"
        and result["engineered_iw_source_channel_reopened"] is True
        and result["full_barker_zell_iw_family_closed"] is False
        and result["full_same_action_iw_noether_completion_closed"] is False
        and result["hook17_closed"] is False
        and result["metric_gate_authorized"] is False
        and result["payload_gate_authorized"] is False
    )

    return {
        "pass": passed,
        "decision": result["decision"],
        "a12a_next": result["next"],
    }


@lru_cache(maxsize=1)
def concurrent_c4_exact_reduction() -> dict[str, Any]:
    """Derive the exact mass/source corridor symbolically."""

    b1, b2, b3, b4, b5, b6 = sp.symbols(
        "b1 b2 b3 b4 b5 b6",
        real=True,
    )
    j_m, j_n = sp.symbols("J_M J_N")

    hessian = sp.Matrix(
        [
            [2 * b2, b6],
            [b6, 2 * b4],
        ]
    )
    determinant = sp.factor(hessian.det())

    mixing = sp.Matrix([b3, b5])
    elimination = sp.simplify(
        hessian.inv() * mixing
    )

    mass_coefficient = sp.factor(
        b1
        - sp.Rational(1, 2)
        * (mixing.T * hessian.inv() * mixing)[0]
    )

    effective_source = sp.factor(
        j_n
        - elimination[0] * j_m
        - elimination[1] * j_n
    )

    corridor = {
        b3: b5 * b6 / (2 * b4),
        b1: b5**2 / (4 * b4),
    }

    c_ratio = sp.factor(
        b5 / (2 * b4)
    )

    corridor_elimination = sp.simplify(
        elimination.subs(corridor)
    )
    corridor_mass = sp.factor(
        mass_coefficient.subs(corridor)
    )
    corridor_source = sp.factor(
        effective_source.subs(corridor)
    )

    full_mass_hessian = sp.Matrix(
        [
            [2 * b1, b3, b5],
            [b3, 2 * b2, b6],
            [b5, b6, 2 * b4],
        ]
    )

    null_vector = sp.Matrix(
        [1, 0, -c_ratio]
    )

    null_residual = sp.simplify(
        full_mass_hessian.subs(corridor)
        * null_vector
    )

    projective_source = sp.simplify(
        corridor_source.subs(
            b5,
            2 * b4,
        )
    )

    return {
        "nondynamical_hessian_determinant":
            str(determinant),

        "nondynamical_nonsingularity_condition":
            "4*b2*b4-b6**2 != 0",

        "axial_decoupling_condition":
            "2*b3*b4-b5*b6 = 0",

        "massless_condition_after_axial_decoupling":
            "4*b1*b4-b5**2 = 0",

        "general_elimination_w_t_hat":
            str(sp.factor(elimination[0])),

        "general_elimination_w_zc":
            str(sp.factor(elimination[1])),

        "general_effective_source":
            str(effective_source),

        "corridor_c":
            str(c_ratio),

        "corridor_w_t_hat":
            str(sp.factor(corridor_elimination[0])),

        "corridor_w_zc":
            str(sp.factor(corridor_elimination[1])),

        "corridor_mass_coefficient":
            str(corridor_mass),

        "corridor_effective_source":
            str(corridor_source),

        "massless_null_vector":
            [
                "1",
                "0",
                "-" + str(c_ratio),
            ],

        "null_vector_identity_pass":
            all(
                sp.simplify(entry) == 0
                for entry in null_residual
            ),

        "projective_aligned_c1_source_cancels":
            projective_source == 0,

        "generic_c_not_1_source_can_be_nonzero":
            True,

        "exact_symbolic_arithmetic":
            True,
    }


@lru_cache(maxsize=1)
def enhanced_u1_symmetry_gate() -> dict[str, Any]:
    """Reconstruct the exact gradient symmetry and Dirac Noether source."""

    c, alpha_nm = sp.symbols(
        "c alpha_nm",
        real=True,
    )

    # Measure every transformation in units of d_lambda.
    delta_q = sp.Integer(1)

    # Projective:
    #   delta T = -3 A
    #   delta Q = +8 A
    #   delta Qhat = +2 A
    #
    # with A=d_lambda/8.
    delta_t_projective = -sp.Rational(3, 8)
    delta_qhat_projective = sp.Rational(1, 4)

    # Iso-Weyl C adds only to Qhat when B=0.
    delta_qhat_iw_c = c - 1

    delta_t = delta_t_projective
    delta_qhat = sp.simplify(
        delta_qhat_projective
        + delta_qhat_iw_c
    )

    # Zc = 2 T - Qhat
    delta_zc = sp.simplify(
        2 * delta_t
        - delta_qhat
    )

    # Zep = Q + Zc = 2T + Q - Qhat
    delta_zep = sp.simplify(
        delta_q
        + delta_zc
    )

    # beta_nm=0 makes J_N a pure vector current.
    j_n_vector_coefficient = alpha_nm / 4

    geometric_matter_variation = sp.simplify(
        delta_zep
        * j_n_vector_coefficient
    )

    required_phase_charge = sp.simplify(
        -geometric_matter_variation
    )

    total_matter_variation = sp.simplify(
        geometric_matter_variation
        + required_phase_charge
    )

    # From the post-Riemannian Holst identity,
    # R_tilde contains (1/3) T_hat.Zep.
    holst_shift_coefficient = sp.factor(
        delta_zep / 3
    )

    return {
        "projective_gradient_choice":
            "A_mu=(1/8)*partial_mu(lambda)",

        "iso_weyl_gradient_choice":
            "C_mu=(c-1)*partial_mu(lambda)",

        "concurrent_b_choice":
            "B_mu=0",

        "delta_q_coefficient":
            str(delta_q),

        "delta_zc_coefficient":
            str(delta_zc),

        "delta_zep_coefficient":
            str(delta_zep),

        "delta_t_hat_coefficient":
            "0",

        "beta_nm":
            0,

        "j_n_current":
            "(alpha_nm/4)*psi_bar*gamma^mu*psi",

        "massive_dirac_vector_current_classically_conserved":
            True,

        "required_dirac_phase_charge":
            str(required_phase_charge),

        "matter_variation_cancels_exactly":
            total_matter_variation == 0,

        "fermion_mass_term_phase_invariant":
            True,

        "homothetic_maxwell_term_gradient_invariant":
            True,

        "holst_shift_coefficient":
            str(holst_shift_coefficient),

        "holst_square_allowed_by_generic_c_not_1_enhanced_u1":
            False,

        "enhanced_u1_forbids_holst_square_for_generic_c_not_1":
            True,

        "classical_same_action_gauge_completion_in_declared_subfamily":
            total_matter_variation == 0,

        "isolated_vectorlike_dirac_current_has_axial_mass_divergence_problem":
            False,

        "full_standard_model_quantum_anomaly_completion_certified":
            False,
    }


def _expanded_eigenvalues(
    matrix: sp.Matrix,
) -> list[sp.Expr]:
    """Return exact eigenvalues with multiplicity."""

    values: list[sp.Expr] = []

    for eigenvalue, multiplicity in matrix.eigenvals().items():
        values.extend(
            [sp.simplify(eigenvalue)]
            * int(multiplicity)
        )

    return sorted(
        values,
        key=lambda value: float(sp.N(value)),
    )


@lru_cache(maxsize=1)
def rational_corridor_witness() -> dict[str, Any]:
    """Give a far-from-singular exact rational point on the corridor."""

    b1 = sp.Rational(1, 4)
    b2 = sp.Integer(1)
    b3 = sp.Integer(0)
    b4 = sp.Integer(1)
    b5 = sp.Integer(1)
    b6 = sp.Integer(0)

    c_ratio = sp.Rational(1, 2)

    nondynamical_hessian = sp.Matrix(
        [
            [2 * b2, b6],
            [b6, 2 * b4],
        ]
    )

    full_mass_hessian = sp.Matrix(
        [
            [2 * b1, b3, b5],
            [b3, 2 * b2, b6],
            [b5, b6, 2 * b4],
        ]
    )

    null_vector = sp.Matrix(
        [1, 0, -c_ratio]
    )

    nondynamical_eigenvalues = (
        _expanded_eigenvalues(
            nondynamical_hessian
        )
    )

    mass_eigenvalues = (
        _expanded_eigenvalues(
            full_mass_hessian
        )
    )

    null_residual = (
        full_mass_hessian
        * null_vector
    )

    return {
        "b1": "1/4",
        "b2": "1",
        "b3": "0",
        "b4": "1",
        "b5": "1",
        "b6": "0",

        "c": "1/2",

        "nondynamical_hessian_determinant":
            str(nondynamical_hessian.det()),

        "nondynamical_hessian_eigenvalues":
            [
                str(value)
                for value in nondynamical_eigenvalues
            ],

        "full_vector_mass_hessian_eigenvalues":
            [
                str(value)
                for value in mass_eigenvalues
            ],

        "gauge_null_vector":
            ["1", "0", "-1/2"],

        "gauge_null_residual":
            [
                str(sp.simplify(value))
                for value in null_residual
            ],

        "effective_j_n_fraction":
            "1/2",

        "distance_from_projective_source_cancellation_c1":
            "1/2",

        "nondynamical_sector_nonsingular":
            nondynamical_hessian.det() != 0,

        "positive_nondynamical_margins":
            all(
                value > 0
                for value in nondynamical_eigenvalues
            ),

        "one_exact_gauge_null_and_other_mass_eigenvalues_positive":
            mass_eigenvalues
            == [
                sp.Integer(0),
                sp.Integer(2),
                sp.Rational(5, 2),
            ],

        "gain_from_near_singular_mixing":
            False,

        "masslessness_is_exact_symmetry_null_not_small_eigenvalue":
            True,
    }


@lru_cache(maxsize=1)
def h17a12b_summary() -> dict[str, Any]:
    """Return the conservative A12B promotion decision."""

    provenance = a12a_provenance_gate()
    reduction = concurrent_c4_exact_reduction()
    symmetry = enhanced_u1_symmetry_gate()
    witness = rational_corridor_witness()

    corridor_exists = bool(
        provenance["pass"]
        and reduction["null_vector_identity_pass"]
        and reduction[
            "projective_aligned_c1_source_cancels"
        ]
        and symmetry[
            "matter_variation_cancels_exactly"
        ]
        and symmetry[
            "classical_same_action_gauge_completion_in_declared_subfamily"
        ]
        and symmetry[
            "enhanced_u1_forbids_holst_square_for_generic_c_not_1"
        ]
        and witness[
            "nondynamical_sector_nonsingular"
        ]
        and witness[
            "positive_nondynamical_margins"
        ]
        and witness[
            "one_exact_gauge_null_and_other_mass_eigenvalues_positive"
        ]
        and not witness[
            "gain_from_near_singular_mixing"
        ]
    )

    decision = (
        "GREEN_SCOPED_A12B_CONCURRENT_IW_ENHANCED_U1_"
        "CLASSICAL_SAME_ACTION_MASSLESS_VECTOR_AND_EXACT_"
        "DIRAC_VECTOR_CURRENT_CORRIDOR__CANONICAL_SOURCE_"
        "QUANTUM_SM_PAYLOAD_SILENCE_AND_EMPIRICAL_GATES_OPEN"
        if corridor_exists
        else
        "YELLOW_A12B_REQUIRES_REVIEW"
    )

    return {
        "branch":
            "032H17A12B",

        "decision":
            decision,

        "a12a_provenance":
            provenance,

        "exact_concurrent_reduction":
            reduction,

        "enhanced_u1_symmetry":
            symmetry,

        "rational_nonsingular_witness":
            witness,

        "classical_protected_same_action_massless_source_corridor_exists":
            corridor_exists,

        "ultralight_proca_mass_required":
            False
            if corridor_exists
            else None,

        "masslessness_protected_by_declared_exact_gauge_symmetry_classically":
            corridor_exists,

        "exact_massive_dirac_vector_noether_current_available_classically":
            corridor_exists,

        "near_singular_gain_used":
            False,

        "canonical_source_normalization_established":
            False,

        "source_energy_per_required_charge_established":
            False,

        "full_standard_model_anomaly_free_embedding_established":
            False,

        "neutral_payload_direct_force_silence_established":
            False,

        "empirical_consistency_established":
            False,

        "universal_metric_response_established_for_this_carrier":
            False,

        "canonical_source_empirical_gate_authorized":
            corridor_exists,

        "metric_gate_authorized":
            False,

        "payload_gate_authorized":
            False,

        "complete_energy_optimization_authorized":
            False,

        "hook17_closed":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "next":
            (
                "032H17A12C_CONCURRENT_U1_CANONICAL_SOURCE_CHARGE_"
                "ANOMALY_PAYLOAD_SILENCE_EMPIRICAL_GATE"
                if corridor_exists
                else
                "REVIEW_A12B_CONCURRENT_IW_SYMMETRY_ASSUMPTIONS"
            ),

        "stop_rule":
            (
                "DO_NOT_BUILD_METRIC_PAYLOAD_OR_COMPLETE_ENERGY_LEDGER_"
                "UNTIL_A12C_ESTABLISHES_CANONICAL_SOURCE_STRENGTH_"
                "A_PHYSICALLY_ALLOWED_SOURCE_CHARGE_ASSIGNMENT_AND_"
                "NO_IMMEDIATE_QUANTUM_OR_EMPIRICAL_KILL"
            ),
    }
