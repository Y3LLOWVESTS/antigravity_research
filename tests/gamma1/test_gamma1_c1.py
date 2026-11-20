"""14 decisive C1 L0 scientific gates; no device-level claims."""
from pathlib import Path

from antigravity_research.gamma1 import gamma1_c1_decision_atlas as c

ROOT = Path(__file__).resolve().parents[2]


def test_01_immutable_parents():
    assert len(c.check_parents(ROOT)) == 7


def test_02_dipole_and_current_bianchi():
    assert len(c.exact_bianchi()) == 3


def test_03_d0_differential_euler_from_4d_epsilon():
    assert c.d0_euler_amendment()["manufactured_Y_source_norm"] > 1e-5


def test_04_d0_const_lambda_null():
    assert c.d0_euler_amendment()["constant_lambda_bulk_source"] == "EXACT_ZERO_BY_BIANCHI"


def test_05_d0_lambda_A0_null():
    assert c.d0_euler_amendment()["lambda_equals_function_of_A0_source"] == "EXACT_ZERO_STATIC_ELECTRIC"


def test_06_d0_y_differential_convergence():
    e = c.d0_euler_amendment()["centered_difference_errors"]
    assert all(e[i] > e[i+1] for i in range(len(e)-1))
    assert 3.5 < e[0]/e[1] < 4.5


def test_07_x_polarity_reversal():
    assert c.d0_euler_amendment()["X_polarity_reversal"] == "ODD"


def test_08_m1_dec_geometric_bound():
    x = c.gr_dec_bound()
    assert 3e27 < x["min_source_gravitating_energy_J"] < 4e27
    assert x["max_accel_if_source_gravitating_energy_lt_10MJ_m_s2"] < 3e-20


def test_09_m1_dec_stress_extremizers():
    x = c.gr_dec_bound()["stress_extremizers"]
    assert x["all_positive"] == 4 and x["all_negative"] == -2


def test_10_m1_random_dec_negative_control():
    assert c.verify_dec_inequality()["max_abs_active_stress_ratio"] <= 4


def test_11_m2_healthy_universal_scalar_sign():
    x = c.scalar_exchange()
    assert x["universal_like_source_radial_force"] < 0
    assert x["canonical_kinetic_residue"] == "POSITIVE"


def test_12_m2_ghost_negative_control():
    assert c.scalar_exchange()["wrong_sign_kinetic_repulsion"] == "GHOST_DISALLOWED"


def test_13_m0_weak_metric_curvature_not_promotion():
    x = c.universal_metric_geometry()
    assert x["curvature_tidal_hessian_norm"] > 1e-18
    assert x["Einstein_response"] == "NOT_SOLVED"


def test_14_SI_degeneracy_and_no_automatic_promotion():
    d = c.si_portal_scaling()
    assert d["portal_sigma_equal_under_rescaling"] is True
    assert abs(d["canonical_quadratic_field_cost_ratio"]-5.8) < 1e-12
