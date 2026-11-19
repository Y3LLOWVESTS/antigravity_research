"""R6 independent full-data verifier: no import of R6 scientific module."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np

ROOT=Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent_evidence(doc):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource,Spec,Settings,JointAction,
    )
    from scipy import sparse
    r3=ROOT/doc['parents']['R3_native']['path']
    r5=ROOT/doc['parents']['R5_multiplier']['path']
    with np.load(r3,allow_pickle=False) as f:
        F=np.stack((f['F_plus'],f['F_minus']))
        A=f['A_X'].copy();Y=f['A_Y'].copy()
        sig=f['sigma'].copy();P=f['P'].copy();n=f['neutral_n'].copy()
    with np.load(r5,allow_pickle=False) as f:
        saved=f['lambda_Routhian'].copy()
        ds=f['sigma_prime'].copy()

    m=CoulombSource(Spec(nr=12,L=12.),self_order=8)
    obj=JointAction(m,Settings(nr=12,L=12.))
    w=obj.w
    f2=F*F
    e2=np.exp(2*sig)
    omega=(m.s.N/2+obj.q*np.sum(f2*(w*e2*A)[None,:],axis=1))/(f2@(w*e2))
    W=omega[:,None]-obj.q[:,None]*A[None,:]
    local_mass=n*np.exp(3*sig)
    pot=np.sum(f2-2*f2**2+2*f2**3,axis=0)+m.s.g*f2[0]*f2[1]
    diff=F[:,obj.edge_i]-F[:,obj.edge_j]
    edges=np.sum(diff*diff,axis=0)
    scalar_sq=np.sum(f2,axis=0)
    tem=np.sum(W*W*f2,axis=0)
    # Differentiation with respect to local physical-metric Weyl factor
    # while holding the candidate charges and scalar profiles fixed.
    def candidate_action(sigma):
        e2loc=np.exp(2*sigma)
        return float(
          np.dot(obj.edge_c*.5*(e2loc[obj.edge_i]+e2loc[obj.edge_j]),edges)
          +np.dot(obj.boundary*e2loc,scalar_sq)
          +np.dot(w*np.exp(4*sigma),pot)
          -np.dot(w*e2loc,tem)
          +np.dot(w,obj.s.mass*local_mass*np.exp(sigma)
                 +obj.s.kappa*.5*local_mass**2*np.exp(-2*sigma))
        )
    epsilon=1e-5
    finite=np.empty(obj.N)
    for i in range(obj.N):
        up=sig.copy(); down=sig.copy()
        up[i]+=epsilon;down[i]-=epsilon
        finite[i]=(candidate_action(up)-candidate_action(down))/(2*epsilon)
    independent_lam=-finite*ds/w
    fd_error=float(np.max(abs(independent_lam-saved)))
    assert fd_error<3e-7,fd_error

    Dr=obj.Dr.toarray();Dz=obj.Dz.toarray()
    BR=obj.BR.toarray();BZ=obj.BZ.toarray()
    Lx=Dr.T@(w[:,None]*Dr)+Dz.T@(w[:,None]*Dz)
    Ly=BR.T@(w[:,None]*BR)+BZ.T@(w[:,None]*BZ)
    interior=np.arange(288).reshape(12,24)[1:-1,1:-1].ravel()
    results={}
    for label,K,L,v in (
        ('X_electric',obj.Kx,Lx,A),
        ('Y_magnetic',obj.Ky,Ly,Y),
    ):
        def calc(a,b):
            scale=float(np.einsum('ij,ij->',a,b)/np.einsum('ij,ij->',b,b))
            return scale,float(np.linalg.norm(a-scale*b)/np.linalg.norm(a))
        full=calc(K,L)
        sub=calc(K[np.ix_(interior,interior)],L[np.ix_(interior,interior)])
        Lv=L@v; Kv=K@v
        c=float(np.dot(Kv,Lv)/np.dot(Lv,Lv))
        err=float(np.linalg.norm(Kv-c*Lv)/np.linalg.norm(Kv))
        existing=doc['kernel_comparison'][label]
        assert np.allclose(full,[existing['whole_grid']['best_scale'],existing['whole_grid']['relative_frobenius_mismatch']],rtol=1e-10,atol=1e-12)
        assert np.allclose(sub,[existing['interior_220x220']['best_scale'],existing['interior_220x220']['relative_frobenius_mismatch']],rtol=1e-10,atol=1e-12)
        assert np.isclose(err,existing['on_archived_field_relative_gradient_mismatch'],rtol=1e-10,atol=1e-12)
        assert full[1]>.60 and sub[1]>.60
        results[label]={'whole':float(full[1]),'interior':float(sub[1]),'on_field':err}
    return fd_error,results


def verify(path):
    path=Path(path).resolve()
    assert path.parent==ROOT/'results/data'
    assert re.fullmatch(r'gamma1_00r6_\d{8}T\d{12}Z\.json',path.name)
    assert path.with_name(path.name+'.sha256').read_text().strip()==sha(path)+'  '+path.name
    d=json.loads(path.read_text())
    assert d['classification']=='PASS_RESTRICTED_STATIC_TRACE_AND_FAIL_NODAL_MAXWELL_MATCH'
    assert len(d['parents'])==6
    for entry in d['parents'].values():
        assert entry['actual']==entry['expected']==sha(ROOT/entry['path'])
    for rel,digest in d['producing_sources'].items():
        assert sha(ROOT/rel)==digest
    out=ROOT/d['restricted_trace_archive']['path']
    assert sha(out)==d['restricted_trace_archive']['sha256']
    assert out.with_name(out.name+'.sha256').read_text().strip()==sha(out)+'  '+out.name
    with np.load(out,allow_pickle=False) as f:
        assert set(f.files)==set(d['restricted_trace_archive']['keys'])
        assert all(f[k].shape==(288,) and np.isfinite(f[k]).all() for k in f.files)
        assert max(abs(f['trace_minus_R5_lambda']))<3e-12
    err,kernels=independent_evidence(d)
    assert d['complete_covariant_action']=='NOT_CLOSED'
    assert d['Einstein_metric']=='NOT_SOLVED'
    assert d['whole_craft_up']=='NOT_DERIVED'
    assert d['complete_SI_energy_lt10MJ']=='NOT_CERTIFIED'
    assert d['qualified_physical_survivors']==[]
    assert d['GAMMA1_01_authorized'] is False
    assert d['006D_replaced'] is False
    print('GAMMA1_00R6_INDEPENDENT_VERIFICATION=PASS')
    print('WEYL_TRACE_ALL_CELL_FD_MAX_ABS='+str(err))
    for label,v in kernels.items():
        print(label+'_WHOLE_FROB_REL='+str(v['whole']))
        print(label+'_INTERIOR_FROB_REL='+str(v['interior']))
        print(label+'_ON_FIELD_REL='+str(v['on_field']))
    print('RESULT_SHA256='+sha(path))
    print('TRACE_ARCHIVE_SHA256='+sha(out))

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('Usage: verify_gamma1_00r6.py result.json')
    verify(sys.argv[1])
