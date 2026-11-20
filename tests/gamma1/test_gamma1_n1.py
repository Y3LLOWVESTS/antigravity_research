"""N1 source fidelity, bulk Ward, and manufactured refinement gates."""
from pathlib import Path
import pytest

from antigravity_research.gamma1 import gamma1_n1_native_ward as n

ROOT = Path(__file__).resolve().parents[2]


def test_01_native_source_and_R5_hashes():
    assert len(n.lock(ROOT)) == 8


def test_02_native_stationarity_multiplier_and_ward():
    x = n.native(ROOT)
    assert x["joint_gradient_l2"] < 1e-6
    assert x["R5_portal_Y_replication_inf"] < 1e-10
    assert x["constant_lambda_X_bulk_inf"] < 1e-9
    assert x["constant_lambda_Y_bulk_inf"] < 1e-9


def test_03_native_Y_eom_closed():
    assert n.native(ROOT)["native_Y_EOM_l2"] < 1e-6


def test_04_native_integrability_decomposition():
    q = n.native(ROOT)["integrability_projection"]
    assert q["exact_linear_decomposition_error"] < 1e-9
    assert q["Y_aligned_artifact_over_total"] is not None


def test_05_restricted_full_variational_obligation():
    assert n.science(ROOT)["gates"][
        "NATIVE_CONTINUUM_AND_EXTERIOR_MATCH"
    ] == "NOT_ESTABLISHED"


@pytest.mark.parametrize("nr", [24, 36, 48, 72])
def test_06_to_09_compact_topological_control(nr):
    assert n.smooth_control(nr)[
        "constant_topological_abs_max"
    ] < 1e-10


def test_10_convergence_of_artifact_and_weak_current():
    result = n.convergence()
    assert result["aligned_null_artifact_decreases"]
    assert result["weak_jacobian_error_decreases"]


def test_11_constant_multiplier_exact_but_f_of_A_not_exact_on_grid():
    r = n.smooth_control(48)
    assert r["constant_topological_abs_max"] < 1e-10
    assert r[
        "aligned_function_of_A_spurious_weighted_l2"
    ] > 1e-5
