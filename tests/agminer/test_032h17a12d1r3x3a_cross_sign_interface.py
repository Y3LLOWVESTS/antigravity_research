"""Targeted tests of opposite-sign cross U(1) source gate."""
import numpy as np

from antigravity_research.agminer.hook17_fdual_f_r3x3a_cross_sign_interface import (
    BRANCH, GRIDS, TARGET_G, BUDGET_J, algebra_gate, old_witness,
    whiten, verify_dual,
)
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    geometric_standoff_m,
)
from antigravity_research.agminer.hook17_fdual_f_r3x2_source_cone import (
    source_ward_gate,
)


def test_branch():
    assert BRANCH == "032H17A12D1R3X3A"


def test_two_grids_and_strict_budget():
    assert GRIDS == (0.075, 0.05)
    assert BUDGET_J == 10_000_000.0
    assert TARGET_G == 9.80665


def test_exact_canonical_cross_invariant_identity():
    gate = algebra_gate()
    assert gate["pass"]
    assert gate["cross_identity_residual"] < 1e-12
    assert gate["canonical_energy_residual"] < 1e-12
    assert gate["same_action_signs"] == [1, -1]


def test_parity_completion_not_falsely_promoted():
    assert algebra_gate()["microscopic_parity_anomaly_complete"] is False


def test_source_ward_neutrality():
    assert source_ward_gate()["net_charge_zero_pass"]


def test_exact_geometric_standoff():
    assert abs(geometric_standoff_m() - 1.0) < 1e-12


def test_whitening_preserves_full_rank():
    a = np.array([np.diag([8.0, 18.0])])
    h = np.diag([4.0, 9.0])

    b, w, error, condition = whiten(a, h)

    assert error < 1e-12
    assert abs(condition - 2.25) < 1e-12
    assert np.allclose(b[0], 2.0 * np.eye(2))


def test_true_opposite_sector_can_escape_same_sign_dual():
    bp = np.array([-np.eye(2)])
    bm = np.array([np.eye(2)])
    witness = verify_dual(bp, bm, np.array([1.0]), 1.0)

    assert witness["gamma_plus"] == -1.0
    assert witness["gamma_minus"] == 1.0
    assert witness["gamma_max"] == 1.0


def test_same_negative_witness_for_both_excludes():
    bp = np.array([-np.eye(2)])
    bm = np.array([-2.0 * np.eye(2)])
    witness = verify_dual(bp, bm, np.array([1.0]), 1.0)

    assert witness["energy_bound"][2]["one_g_excluded_below_10mj"]


def test_artifact_witness_provenance_exists():
    for h in GRIDS:
        rows = old_witness(h)
        assert len(rows) > 0
        assert all(row["weight"] >= 0 for row in rows)
