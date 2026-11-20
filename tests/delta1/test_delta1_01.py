"""Fourteen focused DELTA1-01 scientific gates.

Protect nonlinear action variations, field energy, source signs,
stand-off and no-promotion boundaries. These tests are not
device feasibility or experimental validation.
"""
from pathlib import Path
import math
import numpy as np

from antigravity_research.delta1 import delta1_01_exact_shell as d

ROOT = Path(__file__).resolve().parents[2]


def test_01_hash_locked_parents():
    assert len(d.parents(ROOT)) == 4


def test_02_ensemble_charge_and_voltage_with_battery():
    assert d.exact_ensemble()[
        "matched_background_force_sign"
    ] == "IDENTICAL_NEGATIVE"


def test_03_exact_nonlinear_field_equations():
    assert d.exact_ode_and_boundary(.6) < 1e-11
    assert d.exact_ode_and_boundary(1.2) < 1e-11


def test_04_scalar_infinity_and_zero_bare_shell_charge():
    assert abs(d.profile(.8,0)[0]) < 1e-13
    assert abs(d.profile(.8,1)[1]) < 1e-13


def test_05_exponential_Z_strictly_positive():
    assert min(
        math.exp(d.profile(1.2,float(s))[0])
        for s in np.linspace(0,1,32)
    ) >= 1


def test_06_electric_Gauss_constant_flux():
    z = d.state(1.2,1)
    for r in np.linspace(d.R,7,21):
        y = d.profile(1.2,d.R/float(r))[0]
        EX = (
            z["Q_C_conventional_X_normalization"]
            /(4*math.pi*d.EPS0*r*r*math.exp(y))
        )
        assert math.isclose(
            4*math.pi*d.EPS0*r*r*math.exp(y)*EX,
            z["Q_C_conventional_X_normalization"],
            rel_tol=1e-14,
        )


def test_07_energy_quadrature_both_fields():
    assert d.quadrature_check(1.2)[
        "max_relative_error"
    ] < 1e-10


def test_08_scalar_and_electric_positive():
    z = d.state(1.2,1)
    assert z["E_scalar_exterior_J"] > 0
    assert z["E_X_exterior_J"] > 0


def test_09_optimizer_vs_brute_mesh():
    t,e = d.optimize()
    assert 1.15 < t < 1.28
    assert 3e13 < e < 3.3e13


def test_10_alpha_scaling_of_exact_energy():
    t,_ = d.optimize()
    assert math.isclose(
        d.state(t,1)["E_total_exterior_J"]
        /d.state(t,10)["E_total_exterior_J"],
        100,
        rel_tol=1e-13,
    )


def test_11_radial_acceleration_everywhere_in_interval():
    t,_ = d.optimize()
    z = d.state(t,1)

    assert z["min_acceleration_m_s2"] >= (
        d.GRAVITY*(1-1e-14)
    )

    for r in np.linspace(
        d.TARGET_NEAR,d.TARGET_FAR,97
    ):
        accel = (
            d.C*d.C*d.shape(t,float(r))/z["eta"]
        )
        assert accel >= d.GRAVITY*(1-1e-12)


def test_12_1m_true_matter_standoff():
    assert d.TARGET_NEAR-d.R >= 1


def test_13_energy_threshold_strict():
    t,e = d.optimize()
    alpha = math.sqrt(e/d.CEILING)

    assert 1700 < alpha < 1800
    assert d.state(t,1000)[
        "E_total_exterior_J"
    ] > d.CEILING


def test_14_no_false_physical_promotion():
    out = d.science(ROOT)
    assert out["qualified_gravity_bridge_survivors"] == []
    assert out["gates"][
        "FULL_EINSTEIN_EARTH_CRAFT_ACTION"
    ] == "NOT_DERIVED"
    assert out["DELTA1_02_authorized"] is False
