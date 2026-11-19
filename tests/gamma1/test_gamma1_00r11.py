"""R11 focused exact fixed-Noether Schur and hypothetical two-U1 mode tests."""
from pathlib import Path
import numpy as np
import pytest
from antigravity_research.gamma1.gamma1_00r11_constrained_symbol import (
  PH16_SHA,R3_SHA,R5_SHA,R10_SHA,R10_VERIFY_SHA,R9_SHA,
  sha,background,charge_checks,principal,topology_controls,analyze,DIRECTIONS,
)
ROOT=Path(__file__).resolve().parents[2]

@pytest.fixture(scope='module')
def native():
    with np.load(ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',allow_pickle=False) as f:
        return {k:f[k].copy() for k in f.files}

@pytest.fixture(scope='module')
def r5():
    with np.load(ROOT/'results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz',allow_pickle=False) as f:
        return {k:f[k].copy() for k in f.files}

@pytest.fixture(scope='module')
def report(native,r5):return analyze(native,r5)

@pytest.mark.parametrize('rel,digest',[
 ('src/antigravity_research/ph16/ph16_04_joint_stationary.py',PH16_SHA),
 ('results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',R3_SHA),
 ('results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz',R5_SHA),
 ('results/data/gamma1_00r9_20261119T050922694396Z.json',R9_SHA),
 ('results/data/gamma1_00r10_20261119T065042059747Z.json',R10_SHA),
 ('results/data/gamma1_00r10_verification_20261119T070450958407Z.json',R10_VERIFY_SHA),
])
def test_parent_hash(rel,digest):assert sha(ROOT/rel)==digest

def test_constant_portal_topological_null(report):
    assert report['topological_negative_controls']['constant_lambda_two_U1_plane_wave_null'] is True

def test_reproduces_R5_first_derivative(report):
    assert report['Noether_static_Schur']['R5_lambda_max_abs_error']<3e-12

def test_exact_two_source_inertia_positive(report):
    assert min(report['Noether_static_Schur']['I_plus_minus'])>0

def test_FD_global_mixed_hessian(report):
    assert report['Noether_static_Schur']['mixed_hessian_FD_max_abs']<2e-4

def test_FD_diagonal_hessian(report):
    assert report['Noether_static_Schur']['diagonal_hessian_FD_max_abs']<2e-3

def test_fixed_frequency_offdiagonal_null_control(report):
    assert report['Noether_static_Schur']['frozen_frequency_mixed_null_max_abs']<2e-3

def test_exact_fixed_charge_reclosure(report):
    assert report['Noether_static_Schur']['constrained_N_max_abs']<1e-9
    assert report['Noether_static_Schur']['frozen_frequency_N_drift']>.001

def test_schur_PSD_and_rank_two(report):
    d=report['Noether_static_Schur']
    assert d['correction_rank']==2 and d['correction_psd']
    assert d['nonlocal_off_diagonal_max_abs']>.05

def test_constrained_chi_spectrum_still_positive(report):
    assert report['Noether_static_Schur']['corrected_chi_spectrum_min']>0

def test_static_hessian_not_pointwise_local(report):
    assert report['Noether_static_Schur']['constrained_Hessian_NOT_pointwise_local']

@pytest.mark.parametrize('direction',DIRECTIONS)
def test_frozen_two_U1_directions_not_unhealthy(report,direction):
    key=','.join(map(str,direction))
    row=report['hypothetical_frozen_two_U1_principal']['directions'][key]
    assert row['nonpositive_cells']==0
    assert row['superluminal_cells']==0
    assert row['min_v2']>0 and row['max_v2']<=1+1e-12

def test_analytic_all_direction_frozen_lower_bound(report):
    x=report['hypothetical_frozen_two_U1_principal']['analytic_all_directions_v2_lower_bound']
    assert .18<x<.20

def test_beta60_negative_control(report):
    assert report['beta60_frozen_control']['negative_phi_direction_cells']==4
    assert report['beta60_frozen_control']['phi_min_v2']<0

def test_archive_shapes(report):
    a=report['arrays']
    assert a['fixed_N_P_Hessian'].shape==(288,288)
    assert a['rank_two_Schur_correction'].shape==(288,288)
    assert a['local_chi'].shape==(288,)
    assert a['E_X_3D'].shape==(288,3) and a['B_Y_3D'].shape==(288,3)
    assert all(np.isfinite(x).all() for x in a.values())

def test_no_gravity_or_Lorentzian_certificate(report):
    d=report['no_promotion']
    assert d['full_Lorentzian_action']=='NOT_CLOSED'
    assert d['full_mode_stability']=='NOT_CERTIFIED'
    assert d['whole_craft_force']=='NOT_DERIVED'
    assert d['exact_ell_doubleprime_equals_R10_chi']=='NOT_PROVEN'
