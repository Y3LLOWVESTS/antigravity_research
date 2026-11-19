"""Independent R5 verifier: all-cell finite differences, hash locking, metric trace.

DOES NOT import R5 scientific module. Uses original immutable PH16 action
for its spatial grid and computes an independent frozen-envelope sigma action.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
EXPECTED_PH16='b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
EXPECTED_R3='94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def frozen_envelope_cell_differences(profile_path, derived_path, eps=1e-5):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
       CoulombSource,Spec,Settings,JointAction,hydro_profile,
    )
    with np.load(profile_path,allow_pickle=False) as native, np.load(derived_path,allow_pickle=False) as derived:
        F=np.stack([native['F_plus'],native['F_minus']]); A=native['A_X'];Y=native['A_Y'];P=native['P'];
        lam_saved=derived['lambda_Routhian'].copy(); ds_saved=derived['sigma_prime'].copy();
        portalX=derived['portal_X_gradient'].copy();portalY=derived['portal_Y_gradient'].copy()
        bareX=derived['bare_X_gradient'].copy();bareY=derived['bare_Y_gradient'].copy()
        totalX=derived['total_X_gradient'].copy();totalY=derived['total_Y_gradient'].copy()
        joint=native['joint_gradient'].copy(); saved_sig=native['sigma'].copy()
    m=CoulombSource(Spec(nr=12,L=12.0),self_order=8)
    s=Settings(nr=12,L=12.0);j=JointAction(m,s)
    x=j.pack(F,A,Y)
    R,g,details=j.evaluate(x,True)
    assert max(abs(g-joint))<1e-10 and np.linalg.norm(g)<1e-6
    assert abs(R-2401.472107471401)<1e-7
    sig=s.alpha*P-s.beta*P**2
    assert np.max(abs(sig-saved_sig))<1e-13
    ds=s.alpha-2*s.beta*P
    assert max(abs(ds-ds_saved))<1e-13
    w=j.w; e2=np.exp(2*sig); f2=F*F
    n,C=hydro_profile(sig.reshape(m.nr,m.nz),w.reshape(m.nr,m.nz),s.mass,s.kappa,s.n0)
    nlabel=n.ravel()*np.exp(3*sig)
    I=f2@(w*e2)
    omega=(m.s.N/2+j.q*np.sum(f2*(w*e2*A)[None,:],axis=1))/I
    W=omega[:,None]-j.q[:,None]*A[None,:]
    U=np.sum(f2-2*f2**2+2*f2**3,axis=0)+m.s.g*f2[0]*f2[1]
    ei=j.edge_i;ev=j.edge_j;c=j.edge_c
    differences=F[:,ei]-F[:,ev]
    edge_sq=np.sum(differences*differences,axis=0)
    cell_sq=np.sum(f2,axis=0)
    Wf_sq=np.sum(W*W*f2,axis=0)
    def frozen_action(sig_arg):
        exp2=np.exp(2*sig_arg);exp4=exp2*exp2
        return float(
          np.dot(c*(exp2[ei]+exp2[ev])/2,edge_sq)
          +np.dot(j.boundary*exp2,cell_sq)
          +np.dot(w*exp4,U)
          -np.dot(w*exp2,Wf_sq)
          +np.dot(w,s.mass*nlabel*np.exp(sig_arg)+.5*s.kappa*nlabel*nlabel*np.exp(-2*sig_arg))
        )
    fd=np.empty(288)
    for index in range(288):
        plus=sig.copy();minus=sig.copy()
        plus[index]+=eps;minus[index]-=eps
        fd[index]=(frozen_action(plus)-frozen_action(minus))/(2*eps)
    # Same-action envelope variation at fixed original omega and n_label.
    # Independent from analytic local_dsigma formula used by producer.
    lambda_fd=-fd*ds/w
    maxerr=float(np.max(abs(lam_saved-lambda_fd)))
    assert maxerr<3e-7, ('lambda_fd_mismatch',maxerr)
    assert np.all(lam_saved<0) and np.all(ds>0)
    assert np.allclose(bareX+portalX,totalX,rtol=0,atol=1e-10)
    assert np.allclose(bareY+portalY,totalY,rtol=0,atol=1e-10)
    assert np.max(abs(totalX-g[2*288:3*288]))<1e-10
    assert np.max(abs(totalY-g[3*288:4*288]))<1e-10
    return {'all_cell_auxiliary_sigma_derivative_max_abs':maxerr,
            'lattice_lambda_negative_cells':int(np.sum(lam_saved<0)),
            'sigma_prime_positive_cells':int(np.sum(ds>0)),
            'X_total_norm':float(np.linalg.norm(totalX)),
            'Y_total_norm':float(np.linalg.norm(totalY)),
            'Routhian_NOT_J':float(R)}


def independent_diagonal_metric_variation():
    """Independent numeric fixed-F metric trace check, generic scalar prototype."""
    sign=np.array([-1.,1.,1.,1.]);v=np.array([.9,.2,-.4,.15])
    alpha=.05;beta=40.;U=.3;p0=.003
    x=np.array([.02,-.03,.04,-.01])
    def density(x):
        volume=np.exp(np.sum(x))
        p=p0/volume
        sigma=alpha*p-beta*p*p
        Q=np.sum(sign*np.exp(-2*x)*v*v)
        return -volume*(.5*np.exp(2*sigma)*Q+np.exp(4*sigma)*U)
    volume=np.exp(np.sum(x));p=p0/volume
    sigma=alpha*p-beta*p*p
    Q=np.sum(sign*np.exp(-2*x)*v*v)
    trace_tilde=-np.exp(-2*sigma)*Q-4*U
    lam=np.exp(4*sigma)*trace_tilde*(alpha-2*beta*p)
    trace_E=np.exp(4*sigma)*trace_tilde-4*lam*p
    d=1e-6
    finite=0.
    for i in range(4):
        dx=np.zeros(4);dx[i]=d
        finite+=(density(x+dx)-density(x-dx))/(2*d)
    err=abs(finite-volume*trace_E)
    assert err<2e-8,err
    return float(err)


def verify(path):
    result=Path(path).resolve()
    assert result.parent==ROOT/'results/data'
    assert re.fullmatch(r'gamma1_00r5_\d{8}T\d{12}Z\.json',result.name)
    assert result.with_name(result.name+'.sha256').read_text().strip()==sha(result)+'  '+result.name
    d=json.loads(result.read_text())
    assert d['branch']=='GAMMA1-00R5'
    assert d['classification']=='PASS_ACTUAL_LATTICE_MULTIPLIER_AND_SCOPED_COVARIANT_IDENTITIES'
    assert len(d['parents'])==5
    for k,entry in d['parents'].items():
        assert sha(ROOT/entry['path'])==entry['expected']==entry['actual'],k
    for rel,expected in d['source_shas'].items():
        assert sha(ROOT/rel)==expected,rel
    archive=ROOT/d['derived_multiplier_archive']['path']
    assert sha(archive)==d['derived_multiplier_archive']['sha256']
    assert archive.with_name(archive.name+'.sha256').read_text().strip()==sha(archive)+'  '+archive.name
    assert len(d['exact_covariant_necessary_identities'])>=9
    assert len(d['exact_offshell_two_U1_Bianchi_and_topological_controls'])==16
    assert all(d['exact_covariant_necessary_identities'].values())
    assert all(d['exact_offshell_two_U1_Bianchi_and_topological_controls'].values())
    with np.load(archive,allow_pickle=False) as f:
        assert set(f.files)==set(d['derived_multiplier_archive']['keys'])
        assert len(f.files)==9
        for name in f.files:
            assert f[name].shape==(288,) and np.all(np.isfinite(f[name]))
    evidence=frozen_envelope_cell_differences(ROOT/d['parents']['R3_profile']['path'],archive)
    assert d['canonical_lattice_results']['lattice_multiplier_negative_cells']==288
    assert d['canonical_lattice_results']['sigma_prime_positive_cells']==288
    assert abs(evidence['X_total_norm']-d['canonical_lattice_results']['X_total_norm'])<1e-12
    assert abs(evidence['Y_total_norm']-d['canonical_lattice_results']['Y_total_norm'])<1e-12
    metric=independent_diagonal_metric_variation()
    assert d['complete_covariant_action']=='NOT_CLOSED'
    assert d['lattice_lambda_vs_covariant_lambda']=='NOT_IDENTIFIED_DIFFERENT_ACTION_LEVELS'
    assert d['physical_survivors']==[]
    assert d['GAMMA1_01_authorized'] is False and d['006D_replaced'] is False
    assert d['Earth_down']=='NOT_DERIVED' and d['whole_craft_up']=='NOT_DERIVED'
    assert d['complete_energy_lt10MJ']=='NOT_CERTIFIED'
    print('GAMMA1_00R5_INDEPENDENT_VERIFICATION=PASS')
    print('ORIGINAL_LATTICE_LAMBDA_ALL_CELL_FD_MAX_ABS='+str(evidence['all_cell_auxiliary_sigma_derivative_max_abs']))
    print('INDEPENDENT_COVARIANT_METRIC_TRACE_FD_MAX_ABS='+str(metric))
    print('RESULT_SHA256='+sha(result))
    print('MULTIPLIER_ARCHIVE_SHA256='+sha(archive))
    return evidence

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Supply exact R5 result JSON')
    verify(sys.argv[1])
