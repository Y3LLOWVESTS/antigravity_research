"""PH16-03: PH15 finite-cell portal Y with exactly reclosed source Noether and hydrostatic neutral fluid.

Scope: Routhian variation of Y and both stationary charged-scalar frequencies at fixed F,X;
fluid material labels are updated to hydrostatic equilibrium at conserved total fluid number.
No scalar/X reoptimization, Einstein solution, finite 3D Earth, healthy full modes, or SI energy.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import sympy as sp
from scipy import sparse
from scipy.sparse.linalg import spsolve, eigsh
from antigravity_research.agminer.hook17_ph15_p10_free_space import CoulombSource, Spec
from antigravity_research.ph16.ph16_00_transfer_atlas import dR,dZ,source_traces
from antigravity_research.ph16.ph16_01_neutral_fluid_health import hydro_profile
from antigravity_research.ph16.ph16_02_reciprocal_principal import FrozenY

@dataclass(frozen=True)
class Settings:
    nr: int=12
    L: float=12.
    alpha: float=.05
    beta: float=40.
    n0: float=.15
    mass: float=1.
    kappa: float=.5

def exact_atlas():
    """Independent stationary action/charge/constitutive algebra."""
    P,a,b,W,F,K,U,n,m,k,q,A,omega,N=sp.symbols(
        'P alpha beta W F K U n m kappa q A omega N',real=True
    )
    sigma=a*P-b*P**2
    scalar=sp.exp(2*sigma)*(K-(omega-q*A)**2*F**2)+sp.exp(4*sigma)*U
    fluid=m*n*sp.exp(sigma)+k*n*n*sp.exp(-2*sigma)/2
    R=omega*N+scalar+fluid
    Wexpr=omega-q*A
    T=-(2*sp.exp(2*sigma)*(K-Wexpr**2*F**2)+4*sp.exp(4*sigma)*U
        +m*n*sp.exp(sigma)-k*n*n*sp.exp(-2*sigma))
    lam=sp.diff(sigma,P)*T
    charge=sp.diff(R,omega)
    q_current=2*sp.exp(2*sigma)*Wexpr*F**2
    nphys=n*sp.exp(-3*sigma)
    np_indep=sp.Symbol('n_phys',real=True)
    Tfluid=-(m*n*sp.exp(sigma)-k*n*n*sp.exp(-2*sigma))
    chis=sp.diff(lam,P)
    H_vw=-sp.symbols('c')
    H_ww=-2*sp.symbols('I',positive=True)
    Schur=sp.symbols('h')-H_vw**2/H_ww
    checks={
      'sigma_prime':sp.simplify(sp.diff(sigma,P)-(a-2*b*P))==0,
      'source_Noether_stationarity':sp.simplify(charge-(N-q_current))==0,
      'source_X_current_conjugate':sp.simplify(sp.diff(R,A)-q*q_current)==0,
      'matter_portal_lambda':sp.simplify(sp.diff(R,P)+lam)==0,
      'matter_portal_chi':sp.simplify(sp.diff(R,P,2)+chis)==0,
      'neutral_pullback_number_weight':sp.simplify(sp.exp(3*sigma)*nphys-n)==0,
      'hydrostatic_mu':sp.simplify(sp.exp(sigma)*(m+k*nphys)-sp.diff(sp.exp(4*sigma)*(m*np_indep+k*np_indep**2/2),np_indep).subs(np_indep,nphys)*sp.exp(-3*sigma))==0,
      'fluid_trace':sp.simplify(sp.diff(fluid,P)+Tfluid*sp.diff(sigma,P))==0,
      'schur_frequency_stiffening':sp.simplify(Schur-sp.symbols('h')-sp.symbols('c')**2/(2*sp.symbols('I',positive=True)))==0,
      'no_portal_alpha_beta_zero':sp.simplify(sp.diff(R,P).subs({a:0,b:0}))==0,
    }
    bad=[k for k,v in checks.items() if not v]
    if bad:raise AssertionError('Failed action identity: '+str(bad))
    return {k:bool(v) for k,v in checks.items()}


class NumberClosedY:
    """Stationary reduced Routhian and its exact analytic derivatives wrt Y.

    R = 1/2 v^T K_Y v + sum_i omega_i N_i
        + sum_cell w [e^(2sigma)(gradF^2 - W^2F^2)
                    +e^(4sigma) U +m n_l e^sigma
                    +k n_l^2 e^(-2sigma)/2].
    omega_i(v) enforces fixed Noether numbers; n_l held fixed for
    this inner Y variation. Outer iteration re-equilibrates n_l at
    fixed total neutral material number. X, F are frozen.
    """
    def __init__(self,m,fields,s:Settings,n_label):
        K0,U=source_traces(m,fields)
        self.base=FrozenY(m,fields,K0,U,s.alpha,s.beta,n_label.reshape(m.nr,m.nz))
        self.m=m;self.s=s
        self.F=fields['F'].reshape(2,m.cells)
        self.F2=self.F*self.F
        self.A=fields['A'].ravel()
        self.gradF2=K0.ravel()+np.sum((fields['W'].reshape(2,m.cells)*self.F)**2,axis=0)
        self.U=U.ravel()
        self.w=m.w
        self.nlabel=np.asarray(n_label).reshape(-1)
        self.N=np.full(2,float(m.s.N))
        self.q=m.q
        self.Kmat=self.base.Kmat
        self.Pmat=self.base.Pmat

    def fields_at(self,v):
        P=np.asarray(self.Pmat@v).ravel()
        sigma=self.s.alpha*P-self.s.beta*P**2
        ds=self.s.alpha-2*self.s.beta*P
        e2=np.exp(2*sigma)
        e4=e2*e2
        I=np.sum((self.w*e2)[None,:]*self.F2,axis=1)
        omega=(self.N/2+np.sum((self.w*e2*self.A)[None,:]*self.q[:,None]*self.F2,axis=1))/I
        W=omega[:,None]-self.q[:,None]*self.A[None,:]
        numbers=2*np.sum(self.w[None,:]*e2[None,:]*W*self.F2,axis=1)
        K=self.gradF2-np.sum((W*self.F)**2,axis=0)
        fluid1=self.s.mass*self.nlabel*np.exp(sigma)
        fluid2=self.s.kappa*self.nlabel**2*np.exp(-2*sigma)
        T=-2*e2*K-4*e4*self.U-fluid1+fluid2
        Ts=-4*e2*K-16*e4*self.U-fluid1-2*fluid2
        lam=ds*T
        chi=-2*self.s.beta*T+ds*ds*Ts
        return P,sigma,ds,e2,e4,omega,W,numbers,K,T,lam,chi

    def evaluate(self,v):
        P,sigma,ds,e2,e4,omega,W,numbers,K,T,lam,chi=self.fields_at(v)
        gradient=self.Kmat@v-self.Pmat.T@(self.w*lam)
        Hess=(self.Kmat-self.Pmat.T@(sparse.diags(self.w*chi)@self.Pmat)).tocsr()
        for i in range(2):
            b=4*self.w*e2*ds*W[i]*self.F2[i]
            u=np.asarray(self.Pmat.T@b).reshape(-1)
            I=np.sum(self.w*e2*self.F2[i])
            Hess=Hess+sparse.csr_matrix(np.outer(u,u)/(2*I))
        R=(.5*float(v@(self.Kmat@v))+omega@self.N +float(np.dot(self.w,e2*K+e4*self.U+self.s.mass*self.nlabel*np.exp(sigma)+.5*self.s.kappa*self.nlabel*self.nlabel*np.exp(-2*sigma))))
        return np.asarray(gradient).ravel(),Hess,float(R),numbers

    def solve(self,start,maxiter=12):
        v=start.copy(); history=[]
        for it in range(maxiter):
            g,H,R,_=self.evaluate(v)
            res=float(np.linalg.norm(g));history.append(res)
            if res<1e-9: break
            step=spsolve(H,-g)
            found=False
            for j in range(20):
                trial=v+(2.**(-j))*step
                tg,_,tR,_=self.evaluate(trial)
                if np.linalg.norm(tg)<res and tR<=R+1e-8:
                    v=trial;found=True;break
            if not found:break
        g,H,R,N=self.evaluate(v)
        eig=float(eigsh(H,k=1,which='SA',return_eigenvectors=False,tol=1e-7)[0])
        return v,{'residual_L2':float(np.linalg.norm(g)),'Hessian_min':eig,'Routhian_NOT_energy':R,'steps':len(history)-1,'history':history,'Noether':N.tolist()}

def one_case(s:Settings):
    m=CoulombSource(Spec(nr=s.nr,L=s.L),self_order=8)
    p10,fields=m.solve(350)
    if max(p10['scalar_equation_weighted_L2'])>5e-5:raise RuntimeError('P10 not converged')
    K,U=source_traces(m,fields)
    sh=(m.nr,m.nz);A=fields['A'].reshape(sh)
    n_label=np.full(m.cells,s.n0)
    f0=FrozenY(m,fields,K,U,s.alpha,s.beta,n_label.reshape(sh))
    y=f0.source_only_initial()
    trace=[]
    for outer in range(8):
        obj=NumberClosedY(m,fields,s,n_label)
        y,sol=obj.solve(y)
        if sol['residual_L2']>1e-8:raise RuntimeError('Y Routhian not converged')
        P,sigma,ds,e2,e4,omega,W,numbers,KK,T,lam,chi=obj.fields_at(y)
        n,C=hydro_profile(sigma.reshape(sh),m.w.reshape(sh),s.mass,s.kappa,s.n0)
        updated=(np.exp(3*sigma)*n.ravel())
        d=float(np.max(abs(updated-n_label)))
        trace.append(d)
        n_label=updated
        if d<1e-11:break
    obj=NumberClosedY(m,fields,s,n_label)
    y,sol=obj.solve(y)
    P,sigma,ds,e2,e4,omega,W,numbers,KK,T,lam,chi=obj.fields_at(y)
    nphys=n_label*np.exp(-3*sigma)
    eR=-dR(A,m.h);eZ=-dZ(A,m.h)
    # Diagnostic scalar EOM in mixed P10 finite-volume / FD discretization.
    ss=fields['F'].reshape(2,m.cells)**2
    omega0=np.mean(fields['W'].reshape(2,m.cells)+m.q[:,None]*fields['A'].ravel()[None,:],axis=1)
    initial_number_at_new_sigma=2*np.sum(m.w[None,:]*e2[None,:]*(omega0[:,None]-m.q[:,None]*fields['A'].ravel()[None,:])*ss,axis=1)
    num_unreclosed=float(np.max(abs(initial_number_at_new_sigma-m.s.N)))
    EOM=[]
    for i in range(2):
        fi=fields['F'][i]
        V=1.-4*ss[i]+6*ss[i]**2+m.s.g*ss[1-i]
        fs=fi.reshape(sh)
        offset=2*(dR(sigma.reshape(sh),m.h)*dR(fs,m.h)+dZ(sigma.reshape(sh),m.h)*dZ(fs,m.h)).ravel()
        resid=m.L@fi+(np.exp(2*sigma)*V-W[i]**2)*fi-offset
        EOM.append(float(np.sqrt(np.dot(m.w,resid**2))))
    # Approximate X response through PH15 free-space Green kernel and
    # FD constitutive source; this is mixed discretization, not the
    # exact X action gradient. Sign convention is held explicit.
    r=m.rho.reshape(sh)
    v=y.reshape(sh)
    BY_r=-dZ(v,m.h)
    BY_z=dR(v,m.h)+v/r
    lam2=lam.reshape(sh)
    divLB=dR(r*lam2*BY_r,m.h)/r+dZ(lam2*BY_z,m.h)
    charge=2*np.sum(m.q[:,None]*e2[None,:]*W*ss,axis=0)
    Xdef=fields['A']-m.wkernel@(charge-divLB.ravel())
    mu=(s.mass+s.kappa*nphys)*np.exp(sigma)
    ep2=eR*eR+eZ*eZ
    marg=1-chi.reshape(sh)*ep2
    grad,Hessian,R,Ncheck=obj.evaluate(y)
    direction=np.cos(np.arange(m.cells)*.13+.43)
    direction/=np.linalg.norm(direction)
    eps=1e-4
    gp,_,Rp,_=obj.evaluate(y+eps*direction)
    gm,_,Rm,_=obj.evaluate(y-eps*direction)
    grad_fd_error=float(abs((Rp-Rm)/(2*eps)-grad@direction))
    hess_fd_error=float(np.linalg.norm((gp-gm)/(2*eps)-Hessian@direction))
    return {
      'nr':s.nr,'L':s.L,'h':m.h,'beta':s.beta,
      'P10':{'EOM_initial_max':max(p10['scalar_equation_weighted_L2']),'N':p10['individual_Noether'],'source_energy_canonical':p10['canonical_energy_NOT_J']},
      'inner':sol,
      'frequency':[float(x) for x in omega],
      'source_N_residual_max':float(np.max(abs(numbers-m.s.N))),
      'frozen_P10_omega_Noether_defect_abs':num_unreclosed,
      'Routhian_directional_gradient_fd_abs':grad_fd_error,
      'Routhian_Hessian_vector_fd_L2':hess_fd_error,
      'neutral_number_residual':float(abs(np.dot(m.w,n_label)-s.n0*np.sum(m.w))),
      'neutral_mu_redshift_range':float(np.ptp(mu)),
      'neutral_outer_updates':trace,
      'neutral_labels_positive':bool(np.min(n_label)>0),
      'source_frozen_EOM_diagnostic_weighted_L2':EOM,
      'source_sigma_gradient_mixed_discretization':True,
      'X_mixed_discretization_kernel_defect_inf':float(np.max(abs(Xdef))),
      'X_mixed_discretization_kernel_defect_L2':float(np.sqrt(np.dot(m.w,Xdef**2))),
      'magnetic_margin_beta40_min':float(np.min(marg)),
      'magnetic_negative_cell_count':int(np.sum(marg<0)),
      'portal_P_max_abs':float(np.max(abs(P))),
      'portal_sigma_max_abs':float(np.max(abs(sigma))),
      'full_source_X_EOM':'NOT_SOLVED',
      'metric_Einstein_EOM':'NOT_SOLVED',
      'real_Earth_and_full_craft':'NOT_DERIVED',
      'SI_complete_energy':'NOT_CERTIFIED'
    }

def report():
    checks=exact_atlas()
    cases={f'{a}_L{b}':one_case(Settings(nr=a,L=float(b))) for a,b in [(12,12),(18,12),(12,16)]}
    cs=list(cases.values())
    gates={
      'three_P10_sources':len(cs)==3,
      'P10_source_initial_on_shell':all(c['P10']['EOM_initial_max']<5e-5 for c in cs),
      'Y_omega_stationary':all(c['inner']['residual_L2']<1e-8 for c in cs),
      'Y_omega_reduced_Hessian_positive':all(c['inner']['Hessian_min']>0 for c in cs),
      'source_individual_Noether_reclosed':all(c['source_N_residual_max']<1e-9 for c in cs),
      'old_P10_omega_fails_Noether':all(c['frozen_P10_omega_Noether_defect_abs']>1e-4 for c in cs),
      'Routhian_gradient_independent_FD':all(c['Routhian_directional_gradient_fd_abs']<2e-6 for c in cs),
      'Routhian_Hessian_independent_FD':all(c['Routhian_Hessian_vector_fd_L2']<2e-6 for c in cs),
      'neutral_material_number_preserved':all(c['neutral_number_residual']<1e-8 for c in cs),
      'neutral_chemical_hydrostatic':all(c['neutral_mu_redshift_range']<1e-9 for c in cs),
      'fluid_positive':all(c['neutral_labels_positive'] for c in cs),
      'outer_neutral_converged':all(c['neutral_outer_updates'][-1]<1e-9 for c in cs),
      'frozen_source_EOM_defect_reported':all(max(c['source_frozen_EOM_diagnostic_weighted_L2'])>1e-7 for c in cs),
      'X_mixed_grid_defect_reported':all(c['X_mixed_discretization_kernel_defect_inf']>1e-8 for c in cs),
      'frozen_gauge_beta40_positive':all(c['magnetic_margin_beta40_min']>0 for c in cs),
      'no_false_full_source_solve':all(c['full_source_X_EOM']=='NOT_SOLVED' for c in cs),
      'no_false_metric_solve':all(c['metric_Einstein_EOM']=='NOT_SOLVED' for c in cs),
      'no_false_earth_force':all(c['real_Earth_and_full_craft']=='NOT_DERIVED' for c in cs),
    }
    return {'exact':checks,'cases':cases,'gates':{k:bool(v) for k,v in gates.items()},'verdict':'YELLOW_PH16_03_FIXED_NOETHER_Y_FLUID_REDUCED_STATIONARY_FULL_SOURCE_X_METRIC_OPEN','scope':'Y+omega_i+hydrostatic n, fixed F/X. Mixed finite differences for source/X defect DIAGNOSTIC ONLY','full_joint_on_shell':'NOT_SOLVED','Earth_down_craft_up':'NOT_DERIVED','complete_SI_lt10MJ':'NOT_CERTIFIED'}
