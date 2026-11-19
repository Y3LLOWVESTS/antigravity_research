"""GAMMA1-00R7 focused physical weak-form gates and explicit controls."""
from pathlib import Path
import numpy as np
import pytest
from antigravity_research.gamma1.gamma1_00r7_green_fv import (
    PH16_SHA,P8_SHA,P10_SHA,R3_SHA,sha,bump,fit,mesh_audit,analyze,
)
ROOT=Path(__file__).resolve().parents[2]

@pytest.fixture(scope='module')
def survey():
    with np.load(ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',allow_pickle=False) as data:
        native={k:data[k].copy() for k in ('A_X','A_Y')}
    return analyze(native)

def test_parent_PH16_sha():assert sha(ROOT/'src/antigravity_research/ph16/ph16_04_joint_stationary.py')==PH16_SHA

def test_parent_P10_sha():assert sha(ROOT/'src/antigravity_research/agminer/hook17_ph15_p10_free_space.py')==P10_SHA

def test_parent_P8_sha():assert sha(ROOT/'src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py')==P8_SHA

def test_parent_R3_sha():assert sha(ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz')==R3_SHA

def test_compact_bump():
    x=np.array([-9.,-7.,0.,7.,9.]);y=bump(x,7.)
    assert y[0]==y[1]==y[3]==y[4]==0 and y[2]==pytest.approx(1.)

def test_exact_operator_self_control():
    L=np.array([[2.,-1.],[-1.,2.]])
    assert fit(7*L,L)['relative_frobenius_mismatch']<1e-14
    assert fit(7*L,L)['scale']==pytest.approx(7.)

@pytest.mark.parametrize('field',('X','Y'))
def test_reciprocal_green_inversion(survey,field):
    for mesh in survey['mesh_sweep']:
        assert mesh['Green_vs_weighted_FV'][field]['inverse_green_weight_identity_relative']<1e-10
        assert mesh['Green_vs_weighted_FV'][field]['reciprocity_inf']<1e-10

@pytest.mark.parametrize('field',('X','Y'))
def test_fv_is_closer_than_R6_nodal_interior(survey,field):
    mismatch=survey['mesh_sweep'][1]['Green_vs_weighted_FV'][field]['interior_fit']['relative_frobenius_mismatch']
    assert mismatch<.10

@pytest.mark.parametrize('field',('X','Y'))
def test_four_mesh_smooth_probes_monotone(survey,field):
    for probe in ('compact_center','compact_shifted','compact_wide'):
        v=survey['four_mesh_smooth_probe_trends'][field+'_'+probe]['abs_energy_ratio_minus_one']
        assert len(v)==4 and all(v[i+1]<v[i] for i in range(3))

@pytest.mark.parametrize('probe',('compact_center','compact_shifted','compact_wide'))
def test_Y_azimuthal_term_is_necessary(survey,probe):
    m=survey['mesh_sweep'][-1]
    assert m['Y_wrong_missing_azimuthal_term_K_over_L0'][probe] > m['compact_smooth_energy_K_over_FV']['Y'][probe]

def test_native_field_does_not_yet_match(survey):
    d=survey['mesh_sweep'][1]['native_R3_background']
    assert d['X']['on_field_best_scaled_gradient_mismatch']>.7
    assert d['Y']['on_field_best_scaled_gradient_mismatch']>.7


def test_cannot_promote_continuum(survey):
    assert survey['scope']['continuum_exterior']=='NOT_CERTIFIED'
    assert survey['scope']['Einstein_metric']=='NOT_SOLVED'
    assert survey['scope']['Earth_down_whole_craft_up']=='NOT_DERIVED'
