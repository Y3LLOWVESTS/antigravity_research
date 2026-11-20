"""DELTA1-00 action-first conditional energy and source-sign falsifiers."""
import math
import pytest
from pathlib import Path
from antigravity_research.delta1 import delta1_00_scalar_energy_gate as d
ROOT = Path(__file__).resolve().parents[2]


def test_01_immutable_parents():
    assert len(d.check_parents(ROOT)) == 4


def test_02_action_electric_source_sign():
    assert "OPPOSITE" in d.exact_variations()["electric_field_effective_charge"]


def test_03_action_reciprocal_earth_craft_proxy():
    assert d.exact_variations()["earth_craft_pair_recoil"].startswith("SYMBOLIC_EXACT")


def test_04_ppn_gamma_inversion():
    alpha = d.ppn_alpha_max()
    assert abs(2*alpha**2/(1+alpha**2)-d.PPN_GAMMA_TOLERANCE) < 1e-14


@pytest.mark.parametrize("rho", d.RHO_ASSUMED)
def test_05_to_07_target_field_energy_floor(rho):
    e=d.target_energy_floor(d.ppn_alpha_max(),rho)
    assert e["scalar_field_energy_in_target_J_LOWER_BOUND"] > d.BUDGET
    assert e["target_volume_m3_ASSUMED"] == d.TARGET_KG/rho


def test_08_high_density_strongest_case():
    e=d.target_energy_floor(d.ppn_alpha_max(),20000)
    assert 5e10 < e["scalar_field_energy_in_target_J_LOWER_BOUND"] < 6e10


def test_09_canonical_energy_scales_with_alpha_squared():
    a=d.ppn_alpha_max()
    v1=d.target_energy_floor(a,8000)["scalar_field_energy_in_target_J_LOWER_BOUND"]
    v2=d.target_energy_floor(2*a,8000)["scalar_field_energy_in_target_J_LOWER_BOUND"]
    assert math.isclose(v1/v2,4.,rel_tol=1e-13)


def test_10_source_gauge_coupling_threshold():
    s=d.source_leverage(d.ppn_alpha_max())
    assert s["alpha_times_eta_min_ignoring_matter"] > 1e20


def test_11_kinetic_linearization_exceeded():
    assert d.source_leverage(d.ppn_alpha_max())["eta_times_phi_at_standoff_threshold"] > 1e9


def test_12_scalar_negative_controls():
    assert all(d.negative_controls().values())


def test_13_no_empirical_promotion():
    x=d.science(ROOT)
    assert x["gates"]["METER_SCALE_EMPIRICAL_FIFTH_FORCE"] == "NOT_SCREENED"
    assert x["GAMMA1_01_authorized"] is False


def test_14_long_range_scoped_red():
    x=d.science(ROOT)
    assert x["classification"] == "SCOPED_RED_LONG_RANGE_UNSCREENED_SCALAR_F2"
    assert x["qualified_gravity_bridge_survivors"] == []
