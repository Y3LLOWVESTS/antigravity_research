"""B17-M0 regression: action-conditional confinement, real R3B multipoles,
craft geometry, directional sign, numerical derivative convergence and
no promotion of an unloaded Earth tracer to a whole-craft force."""

import importlib.util
import math
from pathlib import Path
import sys

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
    OnboardGeometry, local_confined_portal_gate,
    fitted_b_field, frozen_earth_tracer_accel, normalized_r3b_fit,
)

spec = importlib.util.spec_from_file_location(
    "b17_m0", Path(__file__).resolve().parents[2] / "simulations" /
    "032h17a12d1r3x3b17_m0_exterior_earth_facing_preflight.py"
)
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


def test_exact_confined_local_portal_no_go():
    shut = local_confined_portal_gate(exterior_fx_zero=True, exterior_fy_zero=True)
    assert shut["direct_local_P_and_gradient_zero_proven"] is True
    assert shut["direct_local_portal_transmits"] is False
    partial = local_confined_portal_gate(exterior_fx_zero=False, exterior_fy_zero=True)
    assert partial["direct_local_portal_transmits"] is None
    assert not partial["actual_exterior_carrier_source_realized"]


def test_craft_geometry_no_earth_penetration():
    base = OnboardGeometry()
    assert base.source_center_z_m == 3
    assert base.source_support_to_earth_gap_m == 1
    assert OnboardGeometry(hull_bottom_above_ground_m=5).source_center_z_m == 8
    with pytest.raises(ValueError):
        OnboardGeometry(hull_bottom_above_ground_m=-0.1)
    with pytest.raises(ValueError):
        OnboardGeometry(source_bottom_above_hull_bottom_m=-0.1)


def test_multipole_dipole_field_parity_and_inverse_seventh_power():
    # Pure ell=1: B^2 on the negative symmetry axis goes as r^-6,
    # hence -c^2 partial_z sigma is Earth-down and scales r^-7.
    a = np.array([1.0])
    g = OnboardGeometry()
    v1 = frozen_earth_tracer_accel(a, g, 0, 0, 1.0)
    v2 = frozen_earth_tracer_accel(a, g, 0, 3, 1.0)
    assert v1 < 0 and v2 < 0
    assert math.isclose(v1/v2, 128.0, rel_tol=3e-5)
    br, bz = fitted_b_field(a, 0, -3)
    assert br == 0 and bz > 0
    with pytest.raises(ValueError):
        fitted_b_field(a, 0, -1.5)


def test_sign_redefinition_and_zero_field_control():
    g = OnboardGeometry()
    a = np.array([1.0, 0.25, -0.10])
    pos = frozen_earth_tracer_accel(a, g, 0.5, 0, 1)
    neg = frozen_earth_tracer_accel(-a, g, 0.5, 0, 1)
    assert math.isclose(pos, neg, rel_tol=1e-12)
    assert frozen_earth_tracer_accel(np.zeros(3), g, 0.5, 0, 1) == 0


@pytest.fixture(scope="module")
def real_result():
    return m.run(0.05)


def test_real_r3b_reference_and_earth_facing_control(real_result):
    assert math.isclose(real_result["r3b_reconstructed_preloaded_energy_j"],
                        1.5429162116460216, rel_tol=0, abs_tol=5e-8)
    assert real_result["r3b_fitted_exterior_rms"] < 0.05
    axis = [x for x in real_result["tracer_rows"] if x["earth_radial_m"] == 0]
    assert len(axis) == 7
    assert all(x["earth_surface_preloaded_az_m_s2"] < 0 for x in axis)
    assert all(x["source_to_earth_gap_m"] >= 1 for x in real_result["tracer_rows"])
    assert max(x["finite_difference_relative_change"] for x in real_result["tracer_rows"]) < 5e-4


def test_reaction_and_source_are_explicitly_uncertified(real_result):
    assert real_result["matter_backreaction_solved"] is False
    assert real_result["whole_craft_force_n"] is None
    assert real_result["earth_reaction_impulse_ns"] is None
    assert real_result["complete_operating_energy_j"] is None
    assert real_result["006d_replaced"] is False
