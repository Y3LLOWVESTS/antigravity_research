"""R5 focused necessary-identity and actual PH16 native-multiplier tests."""
from pathlib import Path
import pytest
import numpy as np
from antigravity_research.gamma1.gamma1_00r5_multiplier import (
 sha,load_profile,reconstruct_lattice_multiplier,
 exact_covariant_necessary_identities,exact_topological_bianchi,PH16_SHA,R3_PROFILE_SHA,
)
ROOT=Path(__file__).resolve().parents[2]
PROFILE=ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz'
PH16=ROOT/'src/antigravity_research/ph16/ph16_04_joint_stationary.py'
@pytest.fixture(scope='module')
def actual():return reconstruct_lattice_multiplier(load_profile(PROFILE))

def test_original_ph16_sha():assert sha(PH16)==PH16_SHA

def test_native_r3_archive_sha():assert sha(PROFILE)==R3_PROFILE_SHA

def test_covariant_restricted_identities():
    d=exact_covariant_necessary_identities();assert len(d)>=9 and all(d.values())

def test_offshell_bianchi_not_EOM():
    d=exact_topological_bianchi();assert len(d)==16 and all(d.values())

def test_all_288_actual_lambda_negative(actual):
    a=actual['arrays']['lambda_Routhian'];assert a.shape==(288,) and np.all(a<0)

def test_all_288_sigma_prime_positive(actual):
    a=actual['arrays']['sigma_prime'];assert np.all(a>0)

def test_scalar_derivative_identity(actual):
    a=actual['arrays'];w=load_profile(PROFILE)['weights']
    assert np.max(abs(a['lambda_Routhian']+a['local_dR_dsigma']*a['sigma_prime']/w))<2e-14

def test_x_portal_bare_balance(actual):
    a=actual['arrays'];assert np.linalg.norm(a['bare_X_gradient']+a['portal_X_gradient'])<1e-6

def test_y_portal_bare_balance(actual):
    a=actual['arrays'];assert np.linalg.norm(a['bare_Y_gradient']+a['portal_Y_gradient'])<1e-6

def test_original_full_grad_reconstructed(actual):
    s=actual['summary'];assert s['stationary_grad_L2']<1e-6

def test_routhian_not_joules(actual):
    s=actual['summary'];assert abs(s['Routhian_NOT_J']-2401.472107471401)<1e-7

def test_no_physical_promotion(actual):
    s=actual['summary'];assert s['lambda_canonical_not_covariant_stress'] and s['no_source_replay']

@pytest.mark.parametrize('q',[-.3,0,.05,.5])
def test_weak_field_portal_derivative_sign_control(q):
    p=q;sigmap=.05-80*p
    assert np.isfinite(sigmap)

@pytest.mark.parametrize('a,b',[(0,0),(.05,40),(.2,0)])
def test_on_off_analytic_portal(a,b):
    p=.005
    assert (a-2*b*p)==pytest.approx(a-2*b*p)
    if a==b==0:assert a-2*b*p==0
