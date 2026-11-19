"""R5: recover actual PH16 fixed-Noether lattice multiplier; exact covariant metric algebra.

Proof scope: PH16 stationarity and a formal universal conformal metric ansatz.
Do NOT identify lattice lambda with physical covariant stress/energy, or
assert a complete Lorentzian theory, Einstein solution, or whole-craft force.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
import numpy as np
import sympy as sp
from scipy import sparse

PH16_SHA = 'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
R3_PROFILE_SHA = '94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'


def sha(path):
    path = Path(path)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else 'MISSING'


def exact_covariant_necessary_identities():
    """Restricted off-shell identities for generic physical-metric scalar matter.

    This proves algebraic metric/Hodge and carrier exchange terms, NOT the
    off-shell constrained fluid or solid Ward identities.
    """
    a,b,p,q,u,z,ex,bx,ey,by=sp.symbols('alpha beta P Q U z E_X B_X E_Y B_Y', real=True)
    sigma=a*p-b*p**2
    pz=p*sp.exp(-4*z)
    sigz=a*pz-b*pz**2
    density_z = -sp.exp(4*z)*(sp.exp(2*sigz)*q*sp.exp(-2*z)/2+sp.exp(4*sigz)*u)
    matter=-sp.exp(2*sigma)*q/2-sp.exp(4*sigma)*u
    trace_physical= -sp.exp(-2*sigma)*q-4*u
    lambda_cov=sp.exp(4*sigma)*trace_physical*sp.diff(sigma,p)
    # Einstein variation restricted to Weyl scaling at fixed F_cov.
    # delta (sqrt(-g)L) / delta z = sqrt(-g)(T^E)^mu_mu.
    TE_trace=sp.exp(4*sigma)*trace_physical-4*lambda_cov*p
    portal_ex=ex*by+ey*bx
    lam_portal=sp.diff(matter,p)
    checks={
      'Hodge_P_Weyl_weight_minus4':sp.simplify(sp.diff(pz,z).subs(z,0)+4*p)==0,
      'matter_trace_from_same_action':sp.simplify(sp.diff(density_z,z).subs(z,0)-TE_trace)==0,
      'physical_lambda_matches_P_variation':sp.simplify(lam_portal-lambda_cov)==0,
      'X_E_induced_constitutive':sp.simplify(sp.diff(portal_ex,ex)-by)==0,
      'Y_E_induced_constitutive':sp.simplify(sp.diff(portal_ex,ey)-bx)==0,
      'mixed_ward_reciprocity':sp.simplify(sp.diff(portal_ex,ex,by)-sp.diff(portal_ex,by,ex))==0,
      'coupling_off_null':sp.simplify(lambda_cov.subs({a:0,b:0}))==0,
      'P_zero_lambda_can_survive':sp.simplify(lambda_cov.subs(p,0)+a*(q+4*u))==0,
      'trace_free_matter_null':sp.simplify(lambda_cov.subs(q,-4*sp.exp(2*sigma)*u))==0,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    return {k:bool(v) for k,v in checks.items()}


def exact_topological_bianchi():
    """Both U(1) off-shell dF=0 and constant-portal bulk null identities."""
    coords=sp.symbols('t x y z', real=True)
    lam=sp.Function('lambda')(*coords)
    checks={}
    for species in ('X','Y'):
        A=[sp.Function('A'+species+str(i))(*coords) for i in range(4)]
        F=[[sp.diff(A[j],coords[i])-sp.diff(A[i],coords[j]) for j in range(4)] for i in range(4)]
        star=[[sp.Rational(1,2)*sum(sp.LeviCivita(i,j,k,l)*F[k][l] for k in range(4) for l in range(4)) for j in range(4)] for i in range(4)]
        for j in range(4):
            bianchi=sum(sp.diff(star[i][j],coords[i]) for i in range(4))
            variable_lam=sum(sp.diff(lam*star[i][j],coords[i])-sp.diff(lam,coords[i])*star[i][j] for i in range(4))
            checks['off_shell_dF_'+species+'_zero_'+str(j)]=sp.simplify(bianchi)==0
            checks['constant_lambda_bulk_null_'+species+'_'+str(j)]=sp.simplify(variable_lam)==0
    if not all(checks.values()):
        raise AssertionError(checks)
    return {k:bool(v) for k,v in checks.items()}


def load_profile(path):
    if sha(path)!=R3_PROFILE_SHA:
        raise RuntimeError('R3 immutable native archive missing or SHA mismatch')
    with np.load(path,allow_pickle=False) as f:
        required={'F_plus','F_minus','A_X','A_Y','joint_gradient','P','sigma','neutral_n','weights'}
        if not required <= set(f.files):
            raise RuntimeError('R3 native keys missing')
        result={k:np.array(f[k],copy=True) for k in f.files}
    if len(result['P'])!=288 or len(result['joint_gradient'])!=1152:
        raise RuntimeError('R3 native lattice shape mismatch')
    if any(not np.all(np.isfinite(v)) for v in result.values()):
        raise RuntimeError('nonfinite R3 native array')
    return result


def reconstruct_lattice_multiplier(profile):
    """No source solve. Reconstruct the EXACT original PH16 spatial Routhian.

    Exact origin is evaluate() in PH16-04R2 source (hash locked by caller).
    Returns a stationary *lattice* chain-rule multiplier, not T^GR_mu_nu.
    """
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource, Spec, Settings, JointAction, hydro_profile,
    )
    spec=Spec(nr=12,L=12.0)
    m=CoulombSource(spec,self_order=8)
    s=Settings(nr=12,L=12.0)
    obj=JointAction(m,s)
    x=np.concatenate([profile[k] for k in ('F_plus','F_minus','A_X','A_Y')])
    routhian,grad,d=obj.evaluate(x,True)
    F,A,Y=obj.unpack(x)
    N=obj.N;w=obj.w
    if N!=288 or np.max(abs(grad-profile['joint_gradient']))>1.e-10:
        raise RuntimeError('Reconstructed PH16 gradient differs from immutable R3')
    if abs(float(routhian)-2401.472107471401)>1.e-7 or np.linalg.norm(grad)>=1.e-6:
        raise RuntimeError('R3 native state not reproduced by exact PH16 action')
    Er=-obj.Dr@A; Ez=-obj.Dz@A
    Br=obj.BR@Y; Bz=obj.BZ@Y
    P=Er*Br+Ez*Bz
    sig=s.alpha*P-s.beta*P**2
    if np.max(abs(P-profile['P']))>2.e-12 or np.max(abs(sig-profile['sigma']))>2.e-12:
        raise RuntimeError('Native P or sigma failed exact action reconstruction')
    ds=s.alpha-2*s.beta*P
    e2=np.exp(2*sig);e4=e2*e2
    n,C=hydro_profile(sig.reshape(m.nr,m.nz),w.reshape(m.nr,m.nz),s.mass,s.kappa,s.n0)
    nlabel=n.ravel()*np.exp(3*sig)
    f2=F*F; I=f2@(w*e2)
    omega=(m.s.N/2+obj.q*np.sum(f2*(w*e2*A)[None,:],axis=1))/I
    W=omega[:,None]-obj.q[:,None]*A[None,:]
    edge_u=obj.edge_i;edge_v=obj.edge_j;c=obj.edge_c
    fc=F[:,edge_u]-F[:,edge_v]
    local=np.zeros(N)
    for i in range(2):
        half=c*fc[i]**2
        np.add.at(local,edge_u,e2[edge_u]*half)
        np.add.at(local,edge_v,e2[edge_v]*half)
        local+=2*obj.boundary*e2*f2[i]
    U=np.sum(f2-2*f2**2+2*f2**3,axis=0)+m.s.g*f2[0]*f2[1]
    local+=4*w*e4*U-2*w*e2*np.sum(W**2*f2,axis=0)
    local+=w*(s.mass*nlabel*np.exp(sig)-s.kappa*nlabel**2*np.exp(-2*sig))
    lam=-local*ds/w
    CA=(-sparse.diags(Br)@obj.Dr-sparse.diags(Bz)@obj.Dz)
    CY=(sparse.diags(Er)@obj.BR+sparse.diags(Ez)@obj.BZ)
    portal_A=np.asarray(CA.T@(-w*lam)).ravel()
    portal_Y=np.asarray(CY.T@(-w*lam)).ravel()
    bare_A=-obj.Kx@A +w*2*np.sum(obj.q[:,None]*e2[None,:]*W*f2,axis=0)
    bare_Y=obj.Ky@Y
    gx=bare_A+portal_A;gy=bare_Y+portal_Y
    if max(np.max(abs(gx-grad[2*N:3*N])),np.max(abs(gy-grad[3*N:4*N])))>1.e-10:
        raise RuntimeError('Original X/Y same-Routhian derivative decomposition failed')
    assert np.all(np.isfinite(lam))
    return {
      'arrays':{
       'lambda_Routhian':np.asarray(lam,dtype='<f8'),
       'sigma_prime':np.asarray(ds,dtype='<f8'),
       'local_dR_dsigma':np.asarray(local,dtype='<f8'),
       'portal_X_gradient':np.asarray(portal_A,dtype='<f8'),
       'portal_Y_gradient':np.asarray(portal_Y,dtype='<f8'),
       'bare_X_gradient':np.asarray(bare_A,dtype='<f8'),
       'bare_Y_gradient':np.asarray(bare_Y,dtype='<f8'),
       'total_X_gradient':np.asarray(gx,dtype='<f8'),
       'total_Y_gradient':np.asarray(gy,dtype='<f8'),
      },
      'summary':{
       'Routhian_NOT_J':float(routhian),
       'stationary_grad_L2':float(np.linalg.norm(grad)),
       'lattice_multiplier_min':float(lam.min()),
       'lattice_multiplier_max':float(lam.max()),
       'lattice_multiplier_negative_cells':int(np.sum(lam<0)),
       'lattice_multiplier_positive_cells':int(np.sum(lam>0)),
       'sigma_prime_min':float(ds.min()),
       'sigma_prime_max':float(ds.max()),
       'sigma_prime_positive_cells':int(np.sum(ds>0)),
       'X_portal_norm':float(np.linalg.norm(portal_A)),
       'Y_portal_norm':float(np.linalg.norm(portal_Y)),
       'X_bare_norm':float(np.linalg.norm(bare_A)),
       'Y_bare_norm':float(np.linalg.norm(bare_Y)),
       'X_total_norm':float(np.linalg.norm(gx)),
       'Y_total_norm':float(np.linalg.norm(gy)),
       'lambda_canonical_not_covariant_stress':True,
       'no_source_replay':True,
      }
    }
