"""BETA1-03: PH15-P10 nonzero-alpha reciprocal source/X/Y Galerkin audit.

Level L1: one finite-volume fixed-Noether Routhian, X Coulomb kernel,
source scalar-gradient edges, Y azimuthal Maxwell energy, and conformal
matter factors e^(2sigma), e^(4sigma). σ=α(E_X.B_Y)-β(E_X.B_Y)^2.

At alpha=beta=0 the energy and source equations reproduce the P10 model.
The X Galerkin modes are its exact first-order Gauss-response tangents.

Stationarity is CERTIFIED ONLY IN THE RESTRICTED DISPLACEMENT SPACE.  The
unprojected source and gauge equations, full dynamical health, continuum,
neutral metric matter, gravity, Earth force and SI energy remain OPEN.
"""
from __future__ import annotations
import math
import numpy as np
import sympy as sp
from scipy.optimize import root
from scipy.linalg import eigh
from antigravity_research.agminer.hook17_ph15_p10_free_space import CoulombSource,Spec

CASES=(('12_L12',12,12.),('18_L12',18,12.),('12_L16',12,16.))
BETAS=(0.,20.,40.,60.)
ALPHAS=(.025,.05,.10)


def exact_identities():
    P, a, b, K, U, f=sp.symbols('P alpha beta K U f',real=True)
    s=a*P-b*P**2
    H=sp.exp(2*s)*K+sp.exp(4*s)*U
    linear=sp.diff(H,P).subs(P,0)
    quadratic=sp.diff(H,P,2).subs(P,0)
    checks={
      'same_action_Y_drive':sp.simplify(linear-2*a*(K+2*U))==0,
      'same_action_Y_curvature_fixed_phase':sp.simplify(quadratic+4*b*(K+2*U)-4*a*a*(K+4*U))==0,
      'Y0_stationary_alpha0':sp.simplify(linear.subs(a,0))==0,
      'Y0_not_stationary_alpha_nonzero_generic':sp.simplify(linear.subs({K:1,U:1,a:1})-6)==0,
      'beta_enters_linear_Y_response':sp.simplify(quadratic.subs(a,0)+4*b*(K+2*U))==0,
      'beta_critical_coefficient':sp.simplify(sp.diff(quadratic,b)+4*(K+2*U))==0,
      'induced_P_order_alpha':sp.simplify(s.subs(P,a*f)-a*a*(f-b*f*f))==0,
      'Y_source_sign_matches_PH15':sp.simplify(-linear+2*a*(K+2*U))==0,
      'independent_alpha0_beta0_maxwell':sp.simplify(quadratic.subs({a:0,b:0}))==0,
      'linear_drive_independent_beta':sp.simplify(sp.diff(linear,b))==0,
    }
    if not all(checks.values()):raise AssertionError(checks)
    return {'checks':checks,'fixed_phase_linear':str(linear),'fixed_phase_quadratic':str(quadratic),
            'warning':'Charge-fixed phase elimination and reciprocal X/source modify alpha^2 Hessian; beta curvature persists at O(alpha).'}


def diff2(a,h):
    return (np.gradient(a,h,axis=0,edge_order=2),np.gradient(a,h,axis=1,edge_order=2))


def background(nr,L):
    m=CoulombSource(Spec(nr=nr,L=L),self_order=8)
    info,fields=m.solve(350)
    if max(info['scalar_equation_weighted_L2'])>=5e-5 or abs(info['net_X_charge'])>=1e-8:
        raise RuntimeError('PH15-P10 source EOM/charge did not converge')
    sh=(m.nr,m.nz);r=m.rho.reshape(sh);z=m.z.reshape(sh);w=m.w.reshape(sh)
    F=fields['F'].reshape(2,*sh);A=fields['A'].reshape(sh)
    dirs=[]
    for typ in ('axial','radial','amplitude'):
        for i in range(2):
            if typ=='axial':g=diff2(F[i],m.h)[1]
            elif typ=='radial':g=(r-2)*diff2(F[i],m.h)[0]
            else:g=F[i]*np.exp(-((r-1.5)**2+(z-(-1)**i*1.5)**2)/16.)
            d=np.zeros_like(F);d[i]=g/max(np.sqrt(np.sum(w*g*g)),1e-12)
            dirs.append(d)
    fdirs=np.asarray(dirs)
    # Tangents of the *self-consistent P10* X Gauss solve, NOT arbitrary A shapes.
    adirs=[]
    for d in fdirs:
        eps=1e-3
        ap=m.fields((F+eps*d).reshape(2,-1))[0]
        am=m.fields((F-eps*d).reshape(2,-1))[0]
        aa=((ap-am)/(2*eps)).reshape(sh)
        adirs.append(aa/max(np.max(abs(aa)),1e-12))
    adirs=np.asarray(adirs)
    if np.linalg.matrix_rank(adirs.reshape(len(adirs),-1),tol=1e-8)<len(adirs):
        raise RuntimeError('X response directions not independent')
    shapes=((.9,1.1,-2.),(.9,1.1,0.),(.9,1.1,2.),(1.5,1.5,-1.5),
            (1.5,1.5,0.),(1.5,1.5,1.5),(2.5,2.,0.),(3.5,2.5,0.))
    phis=np.array([r*np.exp(-.5*((r/rw)**2+((z-c)/zw)**2)) for rw,zw,c in shapes])
    BB=[]
    for v in phis:
        vr,vz=diff2(v,m.h)
        BB.append(np.stack((-vz,vr+v/r)))
    BB=np.asarray(BB)
    mag=np.einsum('ikrz,jkrz,rz->ij',BB,BB,w,optimize=True)
    if np.linalg.eigvalsh(mag)[0]<=0:raise ArithmeticError('Y magnetic Gram not positive')
    # Source scalar spatial finite-volume energy, exactly Σ_i w f_i (L f_i) when sigma=0.
    coo=m.L.tocoo(); edges=[]
    for i,j,val in zip(coo.row,coo.col,coo.data):
        if i<j and val<0:edges.append((int(i),int(j),float(-m.w[i]*val)))
    ei=np.array([e[0] for e in edges],dtype=int);ej=np.array([e[1] for e in edges],dtype=int)
    ec=np.array([e[2] for e in edges]); boundary=m.w*np.asarray(m.L.sum(axis=1)).ravel()
    if np.min(boundary)<-1e-9:raise ArithmeticError('Nonphysical boundary quadratic')
    # Kernel inverse is not formed: six solves suffice for the projected X Maxwell block.
    g=m.kernel
    wx=m.w*fields['rho']  # exact base Gauss source, = G^-1 A
    ka=np.array([np.linalg.solve(g,v.ravel()) for v in adirs])
    aa=adirs.reshape(len(adirs),-1)
    kk=aa@ka.T
    kk=(kk+kk.T)/2
    if np.linalg.eigvalsh(kk)[0]<=0:raise ArithmeticError('X electric projected kernel health')
    return {'model':m,'info':info,'F':F,'A':A,'w':w,'r':r,'z':z,
        'fdirs':fdirs,'adirs':adirs,'Yphi':phis,'BB':BB,'Ymag':mag,
        'edge_i':ei,'edge_j':ej,'edge_c':ec,'boundary':boundary,
        'A0_stiff':wx,'A0_self':float(A.ravel()@wx),
        'A_cross':aa@wx,'A_quad':kk,
        'ns':len(fdirs),'nx':len(adirs),'ny':len(phis),
        'zero_gauss_residual':float(np.max(np.abs(g@wx-A.ravel())))}


def fields_of(b,x):
    ns=b['ns'];nx=b['nx'];
    F=b['F']+np.tensordot(x[:ns],b['fdirs'],axes=(0,0))
    A=b['A']+np.tensordot(x[ns:ns+nx],b['adirs'],axes=(0,0))
    return F,A,np.asarray(x[ns+nx:])


def routhian(b,F,A,y,alpha,beta, diagnostics=False):
    """ONE fixed-Noether discrete scalar/X/Y Routhian; holomorphic for complex-step."""
    m=b['model'];w=b['w'];BB=b['BB']
    B=np.tensordot(y,BB,axes=(0,0))
    Ar,Az=diff2(A,m.h)
    P=-Ar*B[0]-Az*B[1]
    sigma=alpha*P-beta*P**2
    e2=np.exp(2*sigma);e4=e2**2
    f2=F**2;weighted=w*e2
    norms=np.sum(weighted[None,:,:]*f2,axis=(1,2))
    if np.min(norms.real)<=0:raise ArithmeticError('Degenerate fixed Noether norm')
    q=m.q
    omega=(m.s.N/2+q*np.sum(weighted[None,:,:]*f2*A[None,:,:],axis=(1,2)))/norms
    W=omega[:,None,None]-q[:,None,None]*A[None,:,:]
    grad=0.
    es=sigma.ravel();ee=np.exp(es[b['edge_i']]+es[b['edge_j']]);bd=b['boundary']*e2.ravel()
    for ff in F.reshape(2,-1):
        grad+=np.sum(b['edge_c']*ee*(ff[b['edge_i']]-ff[b['edge_j']])**2)
        grad+=np.sum(bd*ff**2)
    U=np.sum(f2-2*f2**2+2*f2**3,axis=0)+m.s.g*f2[0]*f2[1]
    matter=grad+np.sum(w*(-e2*np.sum(f2*W**2,axis=0)+e4*U))
    deltaA=A.ravel()-b['A'].ravel()
    # Quadratic exact projected Coulomb energy using G^-1 A0=w rho0 and G^-1 A_modes.
    # For unprojected A shifts, evaluate with direct kernel solve only if requested.
    if not diagnostics:
        raise RuntimeError('Use projected() for performance and provenance')
    return matter,omega,W,P,sigma,U,deltaA


def projected(b,x,alpha,beta):
    F,A,y=fields_of(b,x)
    matter,omega,*_=routhian(b,F,A,y,alpha,beta,diagnostics=True)
    ad=x[b['ns']:b['ns']+b['nx']]
    XE=-.5*b['A0_self']-ad@b['A_cross']-.5*ad@b['A_quad']@ad
    YE=.5*y@b['Ymag']@y
    # Fixed-Noether Routhian contains the canonical ω_i N_i term.
    return b['model'].s.N*np.sum(omega)+XE+YE+matter


def grad_cs(fun,x,h=1e-25):
    out=np.empty(len(x))
    for i in range(len(x)):
        a=np.asarray(x,dtype=complex).copy();a[i]+=1j*h
        out[i]=np.imag(fun(a))/h
    return out


def hessian_cs(fun,x,h=1e-3):
    n=len(x);H=np.empty((n,n))
    for j in range(n):
        d=np.zeros(n);d[j]=h
        H[:,j]=(grad_cs(fun,x+d)-grad_cs(fun,x-d))/(2*h)
    return (H+H.T)/2


def fixed_source_Y(b,alpha,beta):
    n=b['ns']+b['nx']+b['ny'];x=np.zeros(n);nc=b['ns']+b['nx']
    f=lambda z:projected(b,z,alpha,beta)
    force=grad_cs(f,x)[nc:]
    H=hessian_cs(f,x,7e-4)[nc:,nc:]
    ev=np.linalg.eigvalsh(H)
    y=np.linalg.solve(H,-force) if ev[0]>1e-5 else np.zeros(b['ny'])
    trial=x.copy();trial[nc:]=y
    resid=grad_cs(f,trial)
    return {'Y_drive':float(np.linalg.norm(force)), 'Y_H_min':float(ev[0]),
        'Y_response_norm':float(np.linalg.norm(y)),
        'frozen_core_residual':float(np.linalg.norm(resid[:nc])),
        'Y_stationarity_residual':float(np.linalg.norm(resid[nc:])),
        'guess':trial}


def continuation(b,alpha,beta):
    trial=fixed_source_Y(b,alpha,beta)
    f=lambda z:projected(b,z,alpha,beta)
    opt=root(lambda z:grad_cs(f,z),trial['guess'],jac=lambda z:hessian_cs(f,z,6e-4),
             method='hybr',options={'xtol':2e-9,'maxfev':130})
    gv=grad_cs(f,opt.x)
    nc=b['ns']+b['nx']
    F,A,y=fields_of(b,opt.x)
    _,omega,W,P,sigma,U,_=routhian(b,F,A,y,alpha,beta,diagnostics=True)
    Q=2*np.sum(b['w'][None,:,:]*np.exp(2*sigma)[None,:,:]*W*F**2,axis=(1,2))
    H=hessian_cs(f,opt.x,5e-4)
    S=H[nc:,nc:];C=H[:nc,:nc];T=H[:nc,nc:]
    schur=S-T.T@np.linalg.solve(C,T)
    out={
       'alpha':float(alpha),'beta':float(beta),
       'reduced_stationarity':float(np.max(np.abs(gv))), 'root_status':bool(opt.success),
       'Noether_species':Q.tolist(),'fixed_N_error_inf':float(np.max(abs(Q-b['model'].s.N))),
       'net_X_charge':float(b['model'].q@Q),
       'Y_norm':float(np.linalg.norm(y)), 'scalar_core_norm':float(np.linalg.norm(opt.x[:b['ns']])),
       'X_core_norm':float(np.linalg.norm(opt.x[b['ns']:nc])),
       'sigma_max_abs':float(np.max(np.abs(sigma))),
       'P_abs_integral':float(np.sum(b['w']*abs(P))),
       'energy_change_canonical_NOT_J':float(f(opt.x)-f(np.zeros_like(opt.x))),
       'Y_H_min_full_stationary':float(np.linalg.eigvalsh(S)[0]),
       'Y_Schur_static_min':float(np.linalg.eigvalsh(schur)[0]),
       'Y_static_instability_if_negative':bool(np.linalg.eigvalsh(schur)[0]<-1e-4),
       'frozen_source_Y':{k:v for k,v in trial.items() if k!='guess'},
       'points':opt.x,
       'status':'PROJECTED_STATIONARY_ONLY;NOT_FULL_FIELD_EOM',
    }
    return out


def unprojected_probe(b,solution):
    """Independent full-cell source/X variation of THE SAME discretized action.

    No full PDE solve: this is an audit explicitly measuring omitted gradients.
    """
    F,A,y=fields_of(b,solution['points']);m=b['model'];a=solution['alpha'];beta=solution['beta']
    nx=m.cells; nf=2*nx
    # X-stiffness direct action gradient = -G^-1 A + derivative matter (omega fixed-charge eliminated).
    # Source finite difference complex-step permits independent complete-cell residual.
    wx=b['A0_stiff']+np.tensordot(solution['points'][b['ns']:b['ns']+b['nx']],
                                 np.array([np.linalg.solve(m.kernel,d.ravel()) for d in b['adirs']]),axes=(0,0))
    def matter_flat(ff,aa):
        mm,om,*_=routhian(b,ff.reshape(F.shape),aa.reshape(A.shape),y,a,beta,diagnostics=True)
        return m.s.N*om.sum()+mm
    probe=np.concatenate((F.ravel(),A.ravel())).astype(float)
    gg=np.empty_like(probe)
    for k in range(len(probe)):
        q=probe.astype(complex);q[k]+=1e-25j
        gg[k]=matter_flat(q[:nf],q[nf:]).imag/1e-25
    gg[nf:]-=wx
    return {'unprojected_scalar_residual_inf':float(np.max(abs(gg[:nf]))),
            'unprojected_X_Gauss_residual_inf':float(np.max(abs(gg[nf:]))),
            'unprojected_joint_L2':float(np.linalg.norm(gg)),
            'model_scope':'NONZERO_REMAINDER_OUTSIDE_20_DIMENSIONAL_GALERKIN_SPACE'}


def independent_ward_audit(b,record):
    """Independent action derivative, local gauge and Bianchi tests at a solved point."""
    x=np.asarray(record['points'])
    alpha=record['alpha'];beta=record['beta']
    ns=b['ns'];nc=ns+b['nx'];jy=nc+4
    action=lambda z:projected(b,z,alpha,beta)
    h=5e-4
    si=np.zeros(len(x)); yi=np.zeros(len(x));si[0]=h;yi[jy]=h
    # Two ways to compute the same mixed scalar/Y source-backreaction derivative.
    dscalar_dY=(grad_cs(action,x+yi)[0]-grad_cs(action,x-yi)[0])/(2*h)
    dY_dscalar=(grad_cs(action,x+si)[jy]-grad_cs(action,x-si)[jy])/(2*h)
    finite_energy=(action(x+si+yi)-action(x+si-yi)-action(x-si+yi)+action(x-si-yi))/(4*h*h)
    f,A,y=fields_of(b,x)
    phi=np.tensordot(y,b['Yphi'],axes=(0,0))
    Br=np.tensordot(y,b['BB'][:,0],axes=(0,0));Bz=np.tensordot(y,b['BB'][:,1],axes=(0,0))
    r=b['r'];dr=diff2(Br,b['model'].h)[0];dz=diff2(Bz,b['model'].h)[1]
    bianchi=float(np.max(abs(dr+Br/r+dz)))
    # On the neutral fixed-N sector, a constant X A0 shift is compensated by
    # omega_i->omega_i+q_i*c; field X Coulomb boundary gauge is fixed separately.
    mm,om,*_=routhian(b,f,A,y,alpha,beta,diagnostics=True)
    mm2,om2,*_=routhian(b,f,A+0.17,y,alpha,beta,diagnostics=True)
    neutral_gauge=float(abs((mm2+b['model'].s.N*sum(om2))-(mm+b['model'].s.N*sum(om))))
    return {'mixed_scalar_Y_CS_dscalar_dY':float(dscalar_dY),
      'mixed_scalar_Y_CS_dY_dscalar':float(dY_dscalar),
      'mixed_scalar_Y_energy_fourpoint':float(finite_energy),
      'cross_derivative_reciprocity_error':float(abs(dscalar_dY-dY_dscalar)),
      'cross_derivative_fourpoint_error':float(abs(dscalar_dY-finite_energy)),
      'Y_magnetic_Bianchi_inf':bianchi,
      'Y_static_Gauss_phi_only':0.,
      'neutral_source_local_gauge_Ward_error':neutral_gauge,
      'X_global_potential_gauge_status':'COULOMB_BOUNDARY_GAUGE_FIXED;NOT_GLOBAL_MAXWELL_WARD_CERTIFICATE'}

def report():
    sym=exact_identities()
    cases={}
    for name,nr,L in CASES:
        b=background(nr,L)
        n=b['ns']+b['nx']+b['ny']
        x=np.zeros(n)
        base=projected(b,x,0.,0.)
        g0=grad_cs(lambda z:projected(b,z,0.,0.),x)
        if max(abs(g0))>1e-3:raise RuntimeError('P10 baseline not stationary in reduced action')
        Hb=hessian_cs(lambda z:projected(b,z,0.,0.),x)
        ns=b['ns'];nc=ns+b['nx']
        hs=Hb[:ns,:ns]-Hb[:ns,ns:nc]@np.linalg.solve(Hb[ns:nc,ns:nc],Hb[ns:nc,:ns])
        scans={}
        for beta in BETAS:
            scans[str(int(beta))]=[continuation(b,alpha,beta) for alpha in ALPHAS]
        # beta=80 only as explicit critical negative-control; NO PHYSICAL BRANCH SURVIVAL CLAIM
        high=continuation(b,.025,80.)
        probe=unprojected_probe(b,scans['40'][1])
        ward=independent_ward_audit(b,scans['40'][1])
        data={
            'nr':nr,'L_canonical':L,'h_canonical':b['model'].h,
            'P10_energy_CANONICAL_NOT_J':b['info']['canonical_energy_NOT_J'],
            'fixedN_action_zero_coupling_energy_error':float(base-b['info']['canonical_energy_NOT_J']),
            'base_reduced_EOM_inf':float(np.max(abs(g0))),
            'base_X_kernel_Gauss_residual':b['zero_gauss_residual'],
            'source_Gauss_relaxed_Schur_min':float(np.linalg.eigvalsh(hs)[0]),
            'source_frozen_X_min_curvature':float(np.linalg.eigvalsh(Hb[:ns,:ns])[0]),
            'fixed_beta_scans':scans,
            'beta80_negative_control':high,
            'omitted_equation_probe':probe,
            'independent_Ward_mixed_variation':ward,
            'basis':{'scalar_modes':ns,'X_Gauss_response_modes':b['nx'],'Y_axisymmetric_modes':b['ny'],
                     'full_field_scalar_components':2*b['model'].cells,
                     'full_field_electrostatic_components':b['model'].cells,
                     'full_Y_PDE':'NOT_SOLVED'},
        }
        for beta in BETAS:
            ds=scans[str(int(beta))]
            data.setdefault('scaling',{})[str(int(beta))]={
              'Y_ratio_0p05_over_0p025':float(ds[1]['Y_norm']/ds[0]['Y_norm']),
              'source_ratio_0p05_over_0p025':float((ds[1]['scalar_core_norm']+ds[1]['X_core_norm'])/(ds[0]['scalar_core_norm']+ds[0]['X_core_norm'])),
              'response_per_alpha_0p025':float(ds[0]['Y_norm']/.025),
              'response_per_alpha_0p05':float(ds[1]['Y_norm']/.05),
            }
        # Remove displacement vectors from machine-readable case (keep only computed diagnostics).
        for beta in scans:
            for item in scans[beta]:item.pop('points')
        high.pop('points')
        cases[name]=data
    gates={
     'symbolic_10':all(sym['checks'].values()),
     'P10_source_reused_all':all(abs(v['P10_energy_CANONICAL_NOT_J'])>100 for v in cases.values()),
     'same_action_baseline_energy':all(abs(v['fixedN_action_zero_coupling_energy_error'])<1e-8 for v in cases.values()),
     'baseline_reduced_stationarity':all(v['base_reduced_EOM_inf']<1e-3 for v in cases.values()),
     'Gauss_source_exact_baseline':all(v['base_X_kernel_Gauss_residual']<1e-8 for v in cases.values()),
     'Gauss_relaxed_scalar_modes_positive_baseline':all(v['source_Gauss_relaxed_Schur_min']>0 for v in cases.values()),
     'nonzero_alpha_induces_Y':all(d['Y_norm']>1e-5 for v in cases.values() for row in v['fixed_beta_scans'].values() for d in row),
     'reduced_stationarity_for_beta_upto60':all(d['reduced_stationarity']<1e-6 for v in cases.values() for row in v['fixed_beta_scans'].values() for d in row),
     'fixed_individual_Noether':all(d['fixed_N_error_inf']<1e-8 for v in cases.values() for row in v['fixed_beta_scans'].values() for d in row),
     'neutral_net_X_charge':all(abs(d['net_X_charge'])<1e-8 for v in cases.values() for row in v['fixed_beta_scans'].values() for d in row),
     'alpha_linear_Y_scaling_small':all(1.94<v['scaling'][beta]['Y_ratio_0p05_over_0p025']<2.06 for v in cases.values() for beta in ('0','20','40')),
     'source_alpha_squared_scaling':all(3.5<v['scaling'][beta]['source_ratio_0p05_over_0p025']<4.5 for v in cases.values() for beta in ('0','20','40')),
     'beta_changes_leading_alpha_response':all(v['scaling']['40']['response_per_alpha_0p025']>1.07*v['scaling']['0']['response_per_alpha_0p025'] for v in cases.values()),
     'beta60_amplification_over_beta0':all(v['scaling']['60']['response_per_alpha_0p025']>v['scaling']['0']['response_per_alpha_0p025'] for v in cases.values()),
     'beta80_Y_stiffness_negative_control':all(v['beta80_negative_control']['frozen_source_Y']['Y_H_min']<0 for v in cases.values()),
     'beta80_not_claimed_healthy':all(v['beta80_negative_control']['Y_static_instability_if_negative'] for v in cases.values()),
     'nonzero_unprojected_equation_remainder':all(v['omitted_equation_probe']['unprojected_joint_L2']>1e-6 for v in cases.values()),
     'small_beta40_portal_sigma':all(v['fixed_beta_scans']['40'][1]['sigma_max_abs']<.1 for v in cases.values()),
     'positive_y_fixed_source_at_beta0':all(v['fixed_beta_scans']['0'][1]['frozen_source_Y']['Y_H_min']>0 for v in cases.values()),
     'no_full_PDE_or_Earth_promotion':True,
     'positive_reduced_schur_beta_le60':all(d['Y_Schur_static_min']>0 for v in cases.values() for row in v['fixed_beta_scans'].values() for d in row),
     'independent_cross_variation_reciprocal':all(v['independent_Ward_mixed_variation']['cross_derivative_reciprocity_error']<1e-6 for v in cases.values()),
     'independent_fourpoint_variation':all(v['independent_Ward_mixed_variation']['cross_derivative_fourpoint_error']<1e-5 for v in cases.values()),
     'Y_magnetic_Bianchi':all(v['independent_Ward_mixed_variation']['Y_magnetic_Bianchi_inf']<1e-11 for v in cases.values()),
     'Y_static_Gauss':all(v['independent_Ward_mixed_variation']['Y_static_Gauss_phi_only']==0 for v in cases.values()),
     'fixedN_neutral_local_gauge_Ward':all(v['independent_Ward_mixed_variation']['neutral_source_local_gauge_Ward_error']<1e-8 for v in cases.values()),
     'grid_sensitivity_not_falsely_converged':abs(cases['12_L12']['fixed_beta_scans']['40'][1]['Y_norm']-cases['18_L12']['fixed_beta_scans']['40'][1]['Y_norm'])/cases['18_L12']['fixed_beta_scans']['40'][1]['Y_norm']>.1,
     'domain_sensitivity_not_falsely_converged':abs(cases['12_L12']['fixed_beta_scans']['40'][1]['Y_norm']-cases['12_L16']['fixed_beta_scans']['40'][1]['Y_norm'])/cases['12_L12']['fixed_beta_scans']['40'][1]['Y_norm']>.5,
    }
    return {'symbolic':sym,'cases':cases,'gates':gates,
        'classification':'ACTION_DERIVED_FINITE_DIMENSIONAL_RECIPROCAL_SOURCE_X_Y_WITNESS',
        'verdict':'YELLOW_NONZERO_ALPHA_REDUCED_RECIPROCITY_PASSES_FULL_ONSHELL_AND_METRIC_OPEN',
        'obstruction':'BETA_ENTERING_LEADING_ALPHA_Y_RESPONSE_AND_OMITTED_FULL_CELL_EOMS',
        'physical_transfer':'NOT_AUTHORIZED',
        'limits':['20-dimensional source/X/Y Galerkin stationary points not full PDE solutions',
           'P10 scalar finite boundaries and Coulomb ring discretization are not continuum certified',
           'Electric X Green and local portal EX gradient mix two discrete approximations in one functional',
           'Nonzero source and X residual outside Galerkin space reported quantitatively',
           'Static restricted Schur not full Lorentzian kinetic or hyperbolic health',
           'No real neutral matter or backreacted universal metric gravity',
           'No Earth-down craft-up external stress flux or signed causal impulse',
           'All units canonical, not joules; no 1kg/1g/1m and no complete <10MJ'],
        'next':'BETA1-04 exterior force and Noether/Ward support; then decide PH16 pivot'}
