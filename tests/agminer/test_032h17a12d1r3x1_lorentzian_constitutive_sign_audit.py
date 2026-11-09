"""R3X1 Lorentzian sign and independent loaded-solver regressions."""

from __future__ import annotations

import math
import numpy as np

from scipy.sparse import csr_matrix

from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    BRANCH,
    GRIDS_M,
    LAMBDA_VALUES,
    THETA_SIGNS,
    _solve_loaded,
    constitutive_action_gate,
    final_decision,
    provenance_gate,
    weighted_sign_certificate,
)


def test_branch_name():
    assert BRANCH == "032H17A12D1R3X1"


def test_actual_r3c1_r3x0_artifacts_required():
    assert provenance_gate()["pass"] is True


def test_lorentzian_constitutive_relations():
    gate = constitutive_action_gate()

    assert gate["constitutive_D_X"] == "E_X + theta B_Y"
    assert gate["constitutive_H_Y"] == "B_Y - theta E_X"

    assert gate["positive_K_gauss_offdiagonal_sign"] == 1
    assert gate["positive_K_ampere_offdiagonal_sign"] == -1


def test_lorentzian_hessian_diagonal_signs():
    gate = constitutive_action_gate()

    assert gate[
        "static_lorentzian_hessian_diagonal_signs"
    ] == [1, -1]

    assert gate[
        "canonical_kinetic_eigenvalues"
    ] == [1.0, 1.0]


def test_independent_u1_and_field_redefinition():
    gate = constitutive_action_gate()

    assert gate["independent_u1_gauge_bianchi_pass"] is True
    assert gate["field_redefinition_invariant"] is True

    assert gate[
        "polar_x_axial_y_parity_algebra_pass"
    ] is True


def test_parity_and_anomaly_remain_open():
    gate = constitutive_action_gate()

    assert gate[
        "physicalized_parity_odd_source_current"
    ] is False

    assert gate[
        "anomaly_cancellation_proven"
    ] is False


def _mini_prep():
    return {
        "operators": {
            "k_phi": csr_matrix([[2.0]]),
            "k_a": csr_matrix([[3.0]]),
            "nz_inner": 1,
            "nr_phi": 1,
            "nr_a": 1,
        },

        "coupling": {
            "active_phi": np.array([0]),
            "active_a": np.array([0]),
            "c": csr_matrix([[0.4]]),
            "d": csr_matrix([[0.4]]),
        },

        "phi0_vec": np.array([1.0]),
        "a0_vec": np.array([1.0]),

        "green_phi": np.array([[0.5]]),
        "green_a": np.array([[1.0 / 3.0]]),

        "c_green_a": np.array([[0.4 / 3.0]]),
        "d_green_phi": np.array([[0.4 / 2.0]]),

        "c_a0": np.array([0.4]),
        "d_phi0": np.array([0.4]),
    }


def test_weighted_lorentzian_reciprocity():
    prep = _mini_prep()

    field = {
        "h": 1.0,
        "rhos": np.array([0.0, 1.0, 2.0]),
        "zs": np.array([-1.0, 0.0, 1.0]),
    }

    # Scalar axis weight is 1/8, magnetic weight is 1.
    # C=8, D=1 therefore satisfy weighted adjointness.
    prep["operators"]["k_phi"] = csr_matrix(
        np.diag([2.0, 2.0])
    )

    prep["coupling"]["c"] = csr_matrix(
        [[8.0], [0.0]]
    )

    prep["coupling"]["d"] = csr_matrix(
        [[1.0, 0.0]]
    )

    certificate = weighted_sign_certificate(
        field,
        prep,
    )

    assert certificate[
        "lorentzian_static_action_pass"
    ] is True


def test_positive_k_cross_terms_are_skew():
    lam = 1.2

    positive_k = np.array([
        [2.0, lam * 0.4],
        [-lam * 0.4, 3.0],
    ])

    assert np.linalg.det(positive_k) > 0.0

    lorentzian_hessian = np.array([
        [2.0, lam * 0.4],
        [lam * 0.4, -3.0],
    ])

    assert np.max(
        np.abs(
            lorentzian_hessian - lorentzian_hessian.T
        )
    ) == 0.0


def test_physical_skew_block_finite_at_old_symmetric_pole():
    prep = _mini_prep()

    lam = math.sqrt(6.0) / 0.4

    for sign in THETA_SIGNS:
        solution = _solve_loaded(
            prep,
            lam,
            sign,
        )

        assert solution["success"] is True
        assert solution["relative_residual"] < 1.0e-12


def test_loaded_response_matches_direct_synthetic_system():
    prep = _mini_prep()

    for lam in (
        0.0,
        1.0e-5,
        1.0,
        10.0,
    ):
        for sign in THETA_SIGNS:
            solution = _solve_loaded(
                prep,
                lam,
                sign,
            )

            assert solution["success"]

            matrix = np.array([
                [2.0, lam * sign * 0.4],
                [-lam * sign * 0.4, 3.0],
            ])

            rhs = np.array([
                -lam * sign * 0.4,
                lam * sign * 0.4,
            ])

            direct = np.linalg.solve(
                matrix,
                rhs,
            )

            actual = np.array([
                solution["delta_phi_vec"][0],
                solution["delta_a_vec"][0],
            ])

            assert np.allclose(
                direct,
                actual,
                atol=1.0e-10,
                rtol=1.0e-10,
            )


def test_both_grids_and_full_loading_included():
    assert GRIDS_M == (0.075, 0.050)
    assert LAMBDA_VALUES[-1] == 1.0
    assert THETA_SIGNS == (1.0, -1.0)


def _mock_grid(success=True, minacc=0.0):
    return {
        "sign_certificate": {
            "lorentzian_static_action_pass": success,
        },

        "direct_checks": [
            {"pass": success},
        ],

        "rows": [
            {
                "lambda": 1.0,
                "theta_sign": 1.0,
                "solve_success": success,
                "relative_solve_residual": 0.0,
                "whole_payload_meets_one_g_floor":
                    minacc >= 9.80665,
                "weak_sigma_self_consistency": True,
                "canonical_field_energy_j": 2.0,
            },
        ],
    }


def _mock_action():
    return {
        "independent_u1_gauge_bianchi_pass": True,
        "field_redefinition_invariant": True,
        "polar_x_axial_y_parity_algebra_pass": True,
    }


def test_failed_provenance_never_promotes():
    result = final_decision(
        {"pass": False},
        _mock_action(),
        [_mock_grid()],
    )

    assert result["decision"].startswith("RED_HOLD")
    assert result["006d_replaced"] is False


def test_failed_one_g_is_not_rescue():
    result = final_decision(
        {"pass": True},
        _mock_action(),
        [_mock_grid(minacc=0.5)],
    )

    assert result["decision"].startswith(
        "GREEN_THEOREM_YELLOW"
    )

    assert result["physical_antigravity_model_found"] is False


def test_one_g_preflight_is_not_complete_model():
    result = final_decision(
        {"pass": True},
        _mock_action(),
        [_mock_grid(minacc=10.0)],
    )

    assert result["decision"].startswith("GREEN_SCOPED")

    assert result["complete_energy_established"] is False
    assert result["physical_antigravity_model_found"] is False
    assert result["006d_replaced"] is False
