"""R3X0 theorem-first canonical/finite-payload regressions."""

from __future__ import annotations

import math
import numpy as np

from scipy.sparse import csr_matrix

from antigravity_research.agminer.hook17_fdual_f_r3x0_cross_topological_gate import (
    BRANCH,
    _split_operator_relative_residual,
    algebra_ward_gate,
    canonical_kinetic_gate,
    decision,
    dual_euclidean,
    f_of_potential,
    field_capacity_inequality_gate,
    loaded_block_rotation_gate,
    provenance_gate,
)


def test_branch_frozen():
    assert BRANCH == "032H17A12D1R3X0"


def test_provenance_from_actual_r3c1_and_r3d0():
    assert provenance_gate()["pass"] is True


def test_independent_u1_gauge_and_bianchi_ward():
    assert algebra_ward_gate()["independent_u1_ward_pass"] is True


def test_cross_to_plus_minus_exact_field_redefinition():
    assert algebra_ward_gate()["full_redefinition_pass"] is True


def test_vector_axial_parity_algebra_not_microscopic_completion():
    gate = algebra_ward_gate()

    assert gate["vector_axial_parity_algebra_pass"] is True
    assert gate["axial_gauge_anomaly_canceled"] is False
    assert gate["source_ward_realization_proven"] is False


def test_dual_contracts_antisymmetric_tensor():
    tensor = f_of_potential(
        np.array([1.0, 2.0, 3.0, 4.0]),
        np.array([2.0, 0.0, -1.0, 1.0]),
    )

    dual = dual_euclidean(tensor)

    assert np.max(np.abs(dual + dual.T)) < 1.0e-14


def test_healthy_canonical_kinetics_preserve_opposite_portal_signature():
    rows = canonical_kinetic_gate()["rows"]

    assert all(
        row["healthy_kinetic"]
        and row["one_positive_one_negative"]
        for row in rows
    )


def test_parity_forbids_kinetic_mixing_in_vector_axial_assignment():
    rows = canonical_kinetic_gate()["rows"]

    assert rows[0]["parity_allowed_when_x_polar_y_axial"] is True

    assert all(
        not row["parity_allowed_when_x_polar_y_axial"]
        for row in rows[1:]
    )


def test_negative_topological_eigenvalue_is_not_ghost():
    assert (
        canonical_kinetic_gate()[
            "negative_portal_eigenvalue_is_a_ghost"
        ]
        is False
    )


def test_four_field_loaded_block_exact_rotation():
    assert (
        loaded_block_rotation_gate()[
            "two_equal_cross_blocks_to_opposite_self_blocks_pass"
        ]
        is True
    )


def test_mixed_portal_bound_no_free_capacity_gain():
    result = field_capacity_inequality_gate()

    assert result["inequality_pass"] is True
    assert result["capacity_improvement_from_relabeling"] is False


def test_mixed_portal_bound_is_sharp():
    assert math.isclose(
        field_capacity_inequality_gate()["saturating_ratio"],
        1.0,
    )


def test_two_source_lane_weighted_operator_residual():
    # Direct synthetic SPD same-action coupled block.
    lam = 0.13

    kphi = csr_matrix([[2.0]])
    ka = csr_matrix([[3.0]])
    c = csr_matrix([[0.4]])
    d = csr_matrix([[0.4]])

    phi0 = 1.3
    a0 = -0.7

    coupled = np.array([
        [2.0, lam * 0.4],
        [lam * 0.4, 3.0],
    ])

    delta = np.linalg.solve(
        coupled,
        -lam * np.array([
            0.4 * a0,
            0.4 * phi0,
        ]),
    )

    prep = {
        "operators": {
            "k_phi": kphi,
            "k_a": ka,
        },
        "coupling": {
            "c": c,
            "d": d,
        },
        "phi0_vec": np.array([phi0]),
        "a0_vec": np.array([a0]),
    }

    solution = {
        "delta_phi_vec": np.array([delta[0]]),
        "delta_a_vec": np.array([delta[1]]),
    }

    for fraction in (0.0, 0.2, 0.5, 0.8, 1.0):
        residual = _split_operator_relative_residual(
            prep,
            solution,
            lam,
            fraction,
        )

        assert residual < 1.0e-13


def _mock_grids(
    *,
    symmetry=True,
    matching=True,
    sign_loss=True,
):
    grids = []

    for h in (0.075, 0.050):
        grids.append({
            "h_m": h,
            "full_weighted_action_certificate": symmetry,
            "rows": [{
                "lambda": 3.0e-5,
                "split_fraction": 0.5,
                "cross_min_acceleration_m_s2":
                    -2.0 if sign_loss else 2.0,
                "mathematical_relabeling_identity_pass": matching,
            }],
        })

    return grids


def test_scoped_no_free_lunch_is_not_global_cross_topological_closure():
    result = decision(
        _mock_grids(),
        algebra_ward_gate(),
        canonical_kinetic_gate(),
        field_capacity_inequality_gate(),
    )

    assert result["decision"].startswith(
        "GREEN_THEOREM_RED_NAIVE_CROSS"
    )
    assert result["all_independent_two_field_sources_closed"] is False
    assert result["physical_antigravity_model_found"] is False
    assert result["006d_replaced"] is False


def test_action_or_observable_failure_requires_hold():
    for bad in (
        _mock_grids(symmetry=False),
        _mock_grids(matching=False),
    ):
        result = decision(
            bad,
            algebra_ward_gate(),
            canonical_kinetic_gate(),
            field_capacity_inequality_gate(),
        )

        assert result["decision"].startswith("RED_HOLD")


def test_unexpected_sign_requires_audit_not_false_closure():
    result = decision(
        _mock_grids(sign_loss=False),
        algebra_ward_gate(),
        canonical_kinetic_gate(),
        field_capacity_inequality_gate(),
    )

    assert result["decision"].startswith("YELLOW_R3X0")
