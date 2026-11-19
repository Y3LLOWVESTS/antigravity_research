"""Independent R11 verifier, without imports of R11 science or runner.

Rebuilds PH16 fixed-Noether finite-difference mixed Hessian, recovers
rank-two Schur term, checks frozen two-U1 Gauss-projected plane-wave
symbol and strict provenance/negative limits. Not full Lorentzian health.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]


def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent_check(doc,arrays):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource,Spec,JointAction,Settings,
    )
    with np.load(ROOT/doc['parents']['R3_native']['path'],allow_pickle=False) as z:
        p={k:z[k].copy() for k in z.files}
    m=CoulombSource(Spec(nr=12,L=12.0),self_order=8)
    j=JointAction(m,Settings(nr=12,L=12.0))
    F=np.stack((p['F_plus'],p['F_minus'])); A=p['A_X']; Y=p['A_Y'];P=p['P'];w=j.w
    f2=F*F
    numbers=np.full(2,m.s.N,dtype=float)
    charges=j.q
    n_label=p['neutral_n']*np.exp(3*p['sigma'])
    source_edges=np.zeros(j.N)
    for i in range(2):
        d=F[i,j.edge_i]-F[i,j.edge_j]
        h=.5*j.edge_c*d**2
        np.add.at(source_edges,j.edge_i,h)
        np.add.at(source_edges,j.edge_j,h)
    source_edges+=j.boundary*np.sum(f2,axis=0)
    U=np.sum(f2-2*f2**2+2*f2**3,axis=0)+m.s.g*f2[0]*f2[1]
    def frequency(pp):
        e=np.exp(2*(.05*pp-40*pp**2))
        I=f2@(w*e)
        omega=(numbers/2+charges*np.sum(f2*(w*e*A)[None,:],axis=1))/I
        return omega,I
    om,I=frequency(P)
    W=om[:,None]-charges[:,None]*A[None,:]
    def R(pp,reclose=True):
        sig=.05*pp-40*pp**2;exp2=np.exp(2*sig)
        freq=frequency(pp)[0] if reclose else om
        Q=freq[:,None]-charges[:,None]*A[None,:]
        return float(np.dot(freq,numbers)+np.dot(source_edges,exp2)
           +np.dot(w*U,exp2**2)
           -np.dot(w*exp2,np.sum(f2*Q**2,axis=0))
           +np.dot(w,m.s.N*0+ j.s.mass*n_label*np.exp(sig)
                            +.5*j.s.kappa*n_label**2*np.exp(-2*sig)))
    sig=.05*P-40*P**2;ds=.05-80*P;exp2=np.exp(2*sig)
    C=-4*w[None,:]*exp2[None,:]*ds[None,:]*f2*W
    rank_two=C.T@(C/(2*I[:,None]))
    assert np.max(abs(rank_two-arrays['rank_two_Schur_correction']))<1e-10
    assert min(np.linalg.eigvalsh(rank_two))>-1e-9
    assert np.linalg.matrix_rank(rank_two,tol=1e-9)==2
    chi=arrays['local_chi']
    H0=np.diag(-w*chi)
    H=H0+rank_two
    assert np.max(abs(H-arrays['fixed_N_P_Hessian']))<1e-10
    eps=1e-4
    pairs=((11,12),(11,35),(35,36),(10,13))
    max_error=0.
    for a,b in pairs:
        x=np.zeros(288);y=x.copy();x[a]=eps;y[b]=eps
        fd=(R(P+x+y)-R(P+x-y)-R(P-x+y)+R(P-x-y))/(4*eps**2)
        ctrl=(R(P+x+y,False)-R(P+x-y,False)-R(P-x+y,False)+R(P-x-y,False))/(4*eps**2)
        if abs(ctrl)>2e-3:raise AssertionError('Fixed-frequency offdiag should vanish')
        max_error=max(max_error,abs(fd-H[a,b]))
        assert abs(fd-H[a,b])<2e-4
    assert max_error<2e-4
    drift=np.zeros(288);drift[11]=.002;drift[35]=-.003
    new_om,newI=frequency(P+drift)
    expo=np.exp(2*(.05*(P+drift)-40*(P+drift)**2))
    N_new=2*np.sum(f2*(new_om[:,None]-charges[:,None]*A[None,:])*(w*expo)[None,:],axis=1)
    N_fixed=2*np.sum(f2*(om[:,None]-charges[:,None]*A[None,:])*(w*expo)[None,:],axis=1)
    assert np.max(abs(N_new-numbers))<1e-9
    assert np.max(abs(N_fixed-numbers))>.001

    electric=np.stack((-j.Dr@A,-j.Dz@A,np.zeros(288)),axis=1)
    magnetic=np.stack((j.BR@Y,j.BZ@Y,np.zeros(288)),axis=1)
    assert np.max(abs(electric-arrays['E_X_3D']))<1e-11
    assert np.max(abs(magnetic-arrays['B_Y_3D']))<1e-11
    assert np.min(1-chi*np.sum(electric**2,axis=1))>.2

    # Constraint-adjusted frozen two-U1 local principal symbol:
    # n.D_X=0 fixes longitudinal e_X. The transverse 4x4 wave matrix is
    # (v^2-1) I + chi/(1+chi*(n.B)^2) u(v)u(v).T, where
    # u(v)=(v*B_transverse, (E cross n)_transverse).
    # At its predicted v, one eigenvalue must vanish; three other modes
    # remain luminal. This does not include dynamical scalar/fluid/metric.
    directions=((0,0,1),(1,0,0),(0,1,0),(1,1,0),(1,1,1),(1,2,3))
    errors=[];min_v2=1.
    for tup in directions:
        n=np.array(tup,dtype=float);n/=np.linalg.norm(n)
        trial=np.array([1.,0.,0.]) if abs(n[0])<.9 else np.array([0.,1.,0.])
        b1=np.cross(n,trial);b1/=np.linalg.norm(b1);b2=np.cross(n,b1)
        for cell in (0,11,35,59,106,211,287):
            B=magnetic[cell];E=electric[cell];z=chi[cell]
            bnorm=float(n@B);Bt=np.array([b1@B,b2@B]);Ecross=np.array([b1@np.cross(E,n),b2@np.cross(E,n)])
            v2=(1+z*bnorm**2-z*np.sum(Ecross**2))/(1+z*np.dot(B,B))
            assert 0<v2<=1+1e-12
            vv=np.sqrt(v2);denom=1+z*bnorm**2
            u=np.r_[vv*Bt,Ecross]
            M=(v2-1)*np.eye(4)+z/denom*np.outer(u,u)
            sv=np.linalg.svd(M,compute_uv=False)
            errors.append(float(min(sv)/max(sv)))
            assert errors[-1]<2e-10
            min_v2=min(min_v2,v2)
    report=doc['science']['hypothetical_frozen_two_U1_principal']
    assert report['analytic_all_directions_v2_lower_bound']>.18
    assert report['analytic_all_directions_v2_lower_bound']<=min_v2+1e-10
    assert doc['science']['topological_negative_controls']['constant_lambda_two_U1_plane_wave_null'] is True
    return {'global_mixed_schur_FD_max_abs':max_error,'charge_reclosure_max_abs':float(np.max(abs(N_new-numbers))),
            'conditional_plane_wave_4x4_null_rel_max':max(errors),
            'rank_two_eigen_nonzero':np.linalg.svd(rank_two,compute_uv=False)[:2].tolist(),
            'min_frozen_photon_v2_sample':min_v2}


def verify(path):
    p=Path(path).resolve()
    assert p.parent==ROOT/'results/data'
    assert re.fullmatch(r'gamma1_00r11_\d{8}T\d{12}Z\.json',p.name)
    assert p.with_name(p.name+'.sha256').read_text().strip()==sha(p)+'  '+p.name
    doc=json.loads(p.read_text())
    assert doc['classification']=='PASS_RANK_TWO_NONLOCAL_NOETHER_HESSIAN_AND_CONDITIONAL_FROZEN_U1_SYMBOL'
    assert len(doc['parents'])==6
    for v in doc['parents'].values():assert sha(ROOT/v['path'])==v['actual']==v['expected']
    for rel,h in doc['producing_sources'].items():assert sha(ROOT/rel)==h
    a=ROOT/doc['archive']['path']
    assert a.with_name(a.name+'.sha256').read_text().strip()==sha(a)+'  '+a.name
    assert sha(a)==doc['archive']['sha256']
    with np.load(a,allow_pickle=False) as npz:
        arrays={k:npz[k].copy() for k in npz.files}
    assert set(arrays)==set(doc['archive']['keys'])
    assert all(np.isfinite(x).all() for x in arrays.values())
    data=independent_check(doc,arrays)
    assert doc['science']['Noether_static_Schur']['constrained_Hessian_NOT_pointwise_local'] is True
    assert doc['science']['no_promotion']['exact_ell_doubleprime_equals_R10_chi']=='NOT_PROVEN'
    assert doc['full_Lorentzian_action']=='NOT_CLOSED'
    assert doc['Einstein_metric']=='NOT_SOLVED'
    assert doc['whole_craft_up']=='NOT_DERIVED'
    assert doc['complete_energy_lt10MJ']=='NOT_CERTIFIED'
    assert doc['GAMMA1_01_authorized'] is False
    assert doc['qualified_full_gravity_bridge_survivors']==[]
    assert doc['006D_replaced'] is False
    print('GAMMA1_00R11_INDEPENDENT_VERIFICATION=PASS')
    for k,v in data.items():print(k.upper()+'='+str(v))
    print('RESULT_SHA256='+sha(p))
    print('NOETHER_ARCHIVE_SHA256='+sha(a))
    return data


if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: verify_gamma1_00r11.py exact-R11-result.json')
    verify(sys.argv[1])
