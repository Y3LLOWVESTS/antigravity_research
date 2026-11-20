"""Ten DELTA1-02 gates protecting R3B and the exact trace identity.

They do not prove an on-shell physical source or new gravitational model.
"""
import math
from pathlib import Path
import pytest
from antigravity_research.delta1 import delta1_02_r3b_portal_rank as d

ROOT=Path(__file__).resolve().parents[2]


def test_01_historical_lock():
    assert len(d.parents(ROOT)) == 6


def test_02_exact_arbitrary_function_trace_identity():
    assert d.theorem()["portal_only_reparametrization_escape_at_fixed_fields"].startswith("NO")


def test_03_original_R3B_reference_joules_not_device():
    p=d.parents(ROOT)["R3B_original_result"]
    assert math.isclose(
        p["historical_preloaded_capacity_j"],
        d.REFERENCE_J,rel_tol=0,abs_tol=1e-9
    )


def test_04_perfect_mirror_invariant_negative_control():
    c=d.perfect_mirror_control()
    assert c["P_over_Q"]==1.0
    assert c["independent_channel_rank"]==1


@pytest.mark.parametrize("h",d.GRID_M)
def test_05_and_06_authentic_r3b_field_geometry(h):
    m=d.native(h)
    assert m["torus_sample_cells"]>0
    assert abs(m["min_P_acceleration_m_s2"]-9.80665)<1e-9


def test_07_fine_grid_invariant_gram_is_hermitian_positive():
    m=d.native(.050)
    g=m["gradient_gram"]
    assert abs(g[0][1]-g[1][0])<1e-30
    assert g[0][0]>0 and g[1][1]>0
    assert abs(m["gradient_cosine_P_Q"])<=1+1e-12


def test_08_matter_interface_has_measured_finite_cells():
    for h in d.GRID_M:
        m=d.native(h)
        assert m["matter_interface_active_cells"]>0
        assert m["peak_original_beta"]>0
        assert 0<=m["matter_interface_mean_misalignment_sin"]<=1


def test_09_no_automatic_new_operator_promotion():
    x=d.science(ROOT)
    assert x["DELTA1_03_authorized"] is False
    assert x["qualified_gravity_bridge_survivors"]==[]


def test_10_historical_loaded_failure_preserved():
    x=d.science(ROOT)
    assert x["historical_loaded_fine_grid_min_acceleration_m_s2"]<0
    assert x["gates"]["FINITE_LOADED_1KG_TORUS"]=="HISTORICAL_FAIL_UNCHANGED"
