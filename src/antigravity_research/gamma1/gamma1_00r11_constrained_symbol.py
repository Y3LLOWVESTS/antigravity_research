"""R11: exact PH16 fixed-Noether Schur variation plus conditional frozen U(1) principal symbol.

No full Lorentzian action is claimed: the local ell''=chi_R10 identification is
an unproved hypothesis, and all scalar/fluid/metric/support modes are omitted.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import numpy as np

PH16_SHA='b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
R3_SHA='94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
R5_SHA='2b9217ef9b36758ef675eeb47796198adf1be2ff6b5764b316a2e312bc82c883'
R10_SHA='0e7b85cf62d1541667f76022885c9b04de58245a760124115d97d84f83df7cfd'
R10_VERIFY_SHA='5473718c84c509e17bcbe00451793365c5bdc7e2962fdb441849b8261ce2b028'
R9_SHA='eec38658fccbc6f7f7f5de392aa76d08052f2be91937c8e06da553d224b43a9a'
DIRECTIONS=((1.,0.,0.),(0.,1.,0.),(0.,0.,1.),(1.,1.,0.),(1.,-1.,0.),(1.,1.,1.),(1.,-1.,1.),(1.,2.,3.),(3.,1.,2.),(-2.,1.,1.))


def sha(path):
    p=Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'


def background(native,beta=40.):
    from antigravity_research.ph16.ph16_04_joint_stationary import CoulombSource,Spec,JointAction,Settings
    m=CoulombSource(Spec(nr=12,L=12.),self_order=8)
    j=JointAction(m,Settings(nr=12,L=12.))
    F=np.stack((native['F_plus'],native['F_minus']))
    f2=F*F;A=native['A_X'];Y=native['A_Y'];P=native['P'];w=j.w
    nlabel=native['neutral_n']*np.exp(3*native['sigma'])
    spatial=np.zeros(j.N)
    for s in range(2):
        half=.5*j.edge_c*(F[s,j.edge_i]-F[s,j.edge_j])**2
        np.add.at(spatial,j.edge_i,half)
        np.add.at(spatial,j.edge_j,half)
    spatial+=j.boundary*np.sum(f2,axis=0)
    U=np.sum(f2-2*f2**2+2*f2**3,axis=0)+m.s.g*f2[0]*f2[1]
    numbers=np.full(2,m.s.N,dtype=float)
    def sigma(p):return .05*p-beta*p*p
    def omega(p):
        e2=np.exp(2*sigma(p));I=f2@(w*e2)
        om=(numbers/2+j.q*np.sum(f2*(w*e2*A)[None,:],axis=1))/I
        return om,I
    om,I=omega(P)
    W=om[:,None]-j.q[:,None]*A[None,:]
    def reduced_R(p,reclose=True):
        ss=sigma(p);e2=np.exp(2*ss)
        freq=omega(p)[0] if reclose else om
        Wp=freq[:,None]-j.q[:,None]*A[None,:]
        return float(np.dot(freq,numbers)+np.dot(spatial,e2)
            +np.dot(w*U,e2**2)-np.dot(w*e2,np.sum(f2*Wp**2,axis=0))
            +np.dot(w,j.s.mass*nlabel*np.exp(ss)
                   +.5*j.s.kappa*nlabel**2*np.exp(-2*ss)))
    ss=sigma(P);e2=np.exp(2*ss);sp=.05-2*beta*P
    Af=spatial-w*np.sum(f2*W*W,axis=0)
    first=2*Af*e2+4*w*U*e2**2+w*(j.s.mass*nlabel*np.exp(ss)-j.s.kappa*nlabel**2*np.exp(-2*ss))
    second=4*Af*e2+16*w*U*e2**2+w*(j.s.mass*nlabel*np.exp(ss)+2*j.s.kappa*nlabel**2*np.exp(-2*ss))
    lam=-first*sp/w
    chi=(-second*sp**2+2*beta*first)/w
    C=-4*(f2*W)*(w*e2*sp)[None,:]
    dH=C.T@(C/(2*I[:,None]))
    H=np.diag(-w*chi)+dH
    E=np.stack((-j.Dr@A,-j.Dz@A,np.zeros(j.N)),axis=1)
    B=np.stack((j.BR@Y,j.BZ@Y,np.zeros(j.N)),axis=1)
    if np.max(abs(P-np.sum(E*B,axis=1)))>2e-12:raise RuntimeError('P_HODGE_DRIFT')
    return dict(j=j,P=P,w=w,I=I,om=om,N=numbers,lam=lam,chi=chi,C=C,dH=dH,H=H,E=E,B=B,R=reduced_R,native=native,beta=beta)


def charge_checks(s):
    P=s['P'];R=s['R'];H=s['H'];w=s['w'];h=1e-4
    pairs=((11,12),(11,35),(35,36),(10,13))
    off=[];diag=[];frozen=[];base=R(P)
    for i,j in pairs:
        a=np.zeros_like(P);b=a.copy();a[i]=h;b[j]=h
        derivative=(R(P+a+b)-R(P+a-b)-R(P-a+b)+R(P-a-b))/(4*h*h)
        off.append(abs(derivative-H[i,j]))
        frozen.append(abs((R(P+a+b,False)-R(P+a-b,False)-R(P-a+b,False)+R(P-a-b,False))/(4*h*h)))
        diag.append(abs((R(P+a)-2*base+R(P-a))/(h*h)-H[i,i]))
    if max(off)>2e-4 or max(diag)>2e-3 or max(frozen)>2e-3:
        raise RuntimeError('NOETHER_SCHUR_FINITE_DIFFERENCE_FAIL '+str((max(off),max(diag),max(frozen))))
    dH=s['dH'];v=np.linalg.svd(dH,compute_uv=False)
    eigen=np.linalg.eigvalsh(-H/np.sqrt(w[:,None]*w[None,:]))
    offmatrix=dH-np.diag(np.diag(dH))
    offmax=float(np.max(abs(offmatrix)))
    if offmax<.05:
        raise RuntimeError('FIXED_NOETHER_NONLOCAL_OFFDIAGONAL_MISSING')
    if min(np.linalg.eigvalsh((dH+dH.T)/2))<-1e-10:
        raise RuntimeError('FIXED_NOETHER_SCHUR_NOT_PSD')
    if np.sum(v>1e-9)!=2 or min(eigen)<=0 or v[0]<.05:
        raise RuntimeError('RANK_TWO_OR_CONSTRAINED_CURVATURE_FAIL')
    # Exact 2 Noether constraints after independently perturbed P field.
    q=s['j'].q;f2=np.stack((s['native']['F_plus'],s['native']['F_minus']))**2
    A=s['native']['A_X'];shift=np.zeros_like(P);shift[11]=.002;shift[35]=-.003
    e2=np.exp(2*(.05*(P+shift)-s['beta']*(P+shift)**2))
    inertia=f2@(w*e2)
    newomega=(s['N']/2+q*np.sum(f2*(w*e2*A)[None,:],axis=1))/inertia
    actual=2*np.sum(f2*(newomega[:,None]-q[:,None]*A[None,:])*(w*e2)[None,:],axis=1)
    frozenN=2*np.sum(f2*(s['om'][:,None]-q[:,None]*A[None,:])*(w*e2)[None,:],axis=1)
    if np.max(abs(actual-s['N']))>1e-9:raise RuntimeError('NOETHER_RECLOSURE_FAILED')
    return dict(mixed_hessian_FD_max_abs=float(max(off)),diagonal_hessian_FD_max_abs=float(max(diag)),
        frozen_frequency_mixed_null_max_abs=float(max(frozen)),
        constrained_N_max_abs=float(np.max(abs(actual-s['N']))),
        frozen_frequency_N_drift=float(np.max(abs(frozenN-s['N']))),
        correction_rank=int(np.sum(v>1e-9)),correction_singular_values=v[:2].tolist(),
        corrected_chi_spectrum_min=float(min(eigen)),corrected_chi_spectrum_max=float(max(eigen)),
        correction_norm=float(np.linalg.norm(dH)),
        nonlocal_off_diagonal_max_abs=offmax,
        correction_psd=True,
        constrained_Hessian_NOT_pointwise_local=True,
        tested_cell_pairs=[list(t) for t in pairs])


def topology_controls():
    """Plane-wave constant lambda topological term and one-action Hessian facts."""
    import sympy as sp
    ax,ay,cx,cy,k,omega=sp.symbols('ax ay cx cy k omega',real=True,nonzero=True)
    # n=e_z; Faraday imposes b=k/omega * (e_z cross e).
    b_x=sp.Matrix([-k*ay/omega,k*ax/omega,0])
    b_y=sp.Matrix([-k*cy/omega,k*cx/omega,0])
    e_x=sp.Matrix([ax,ay,0]);e_y=sp.Matrix([cx,cy,0])
    topological=sp.simplify(e_x.dot(b_y)+e_y.dot(b_x))
    if topological!=0:raise RuntimeError('CONSTANT_P_BIANCHI_CONTROL_FAIL')
    return {'constant_lambda_two_U1_plane_wave_null':True,
            'two_U1_Bianchi':'F=dA_AS_A_HYPOTHESIS_NOT_FULL_SOURCE_WARD',
            'scalar_fluid_metric_Ward':'NOT_DERIVED'}


def principal(s):
    chi=s['chi'];E=s['E'];B=s['B'];e2=np.sum(E**2,axis=1);b2=np.sum(B**2,axis=1)
    if min(chi)<=0:raise RuntimeError('CHI_SIGN_DRIFT')
    lower=(1-chi*e2)/(1+chi*b2)
    direction={}
    for n0 in DIRECTIONS:
        n=np.array(n0)/np.linalg.norm(n0)
        bn=B@n;et2=e2-(E@n)**2
        velocity=(1+chi*bn**2-chi*et2)/(1+chi*b2)
        direction[','.join(map(str,n0))]=dict(min_v2=float(min(velocity)),max_v2=float(max(velocity)),
            nonpositive_cells=int(np.sum(velocity<=0)),superluminal_cells=int(np.sum(velocity>1+1e-12)))
    if min(lower)<=0 or any(d['nonpositive_cells'] or d['superluminal_cells'] for d in direction.values()):
        raise RuntimeError('FROZEN_PHOTON_SYMBOL_INVALID')
    return dict(directions=direction,analytic_all_directions_v2_lower_bound=float(min(lower)),
        analytic_all_directions_v2_upper_bound=1.,
        azimuthal_min_v2=direction['0.0,0.0,1.0']['min_v2'],
        gauss_denominator_all_directions_lower_bound=1.0,
        electric_rank_one_nontrivial_eigen_min=float(min(1+chi*b2)),
        modified_branch='(1+chi(B.n)^2-chi|E_cross_n|^2)/(1+chi|B|^2)',
        other_three_branches='LUMINAL_IN_FROZEN_TWO_U1_MODEL')


def analyze(native,r5):
    required=('F_plus','F_minus','A_X','A_Y','P','sigma','neutral_n','weights')
    if any(native[k].shape!=(288,) or not np.all(np.isfinite(native[k])) for k in required):
        raise RuntimeError('NATIVE_ARCHIVE_SHAPE_OR_NONFINITE')
    s=background(native,40.)
    if np.max(abs(s['lam']-r5['lambda_Routhian']))>3e-12:
        raise RuntimeError('ORIGINAL_R5_FIRST_VARIATION_DRIFT')
    finite=charge_checks(s)
    c40=principal(s)
    s60=background(native,60.)
    phi=(1-s60['chi']*np.sum(s60['E']**2,axis=1))/(1+s60['chi']*np.sum(s60['B']**2,axis=1))
    if np.sum(phi<=0)!=4:raise RuntimeError('BETA60_CONTROL_DRIFT')
    return {'Noether_static_Schur':{
      'formula':'H_PP|N=diag(H_PP|omega)+C.T diag(1/(2I_plus),1/(2I_minus)) C',
      'H_omegaomega':'diag(-2I_plus,-2I_minus)',
      'I_plus_minus':s['I'].tolist(),'R5_lambda_max_abs_error':float(np.max(abs(s['lam']-r5['lambda_Routhian']))),
      'local_chi_range':[float(min(s['chi'])),float(max(s['chi']))],**finite},
      'hypothetical_frozen_two_U1_principal':c40,
      'topological_negative_controls':topology_controls(),
      'beta60_frozen_control':{'negative_phi_direction_cells':int(np.sum(phi<=0)),
                                'phi_min_v2':float(min(phi)),'beta60_stationary':'NOT_CLAIMED'},
      'no_promotion':{'full_Lorentzian_action':'NOT_CLOSED',
         'exact_ell_doubleprime_equals_R10_chi':'NOT_PROVEN',
         'PH16_Green_to_local_Maxwell':'NOT_PROVEN',
         'scalar_fluid_kinetic_mixing':'NOT_INCLUDED',
         'gravity_metric_Hodge_variation':'NOT_DERIVED',
         'Earth_support_hull_variations':'NOT_DERIVED',
         'whole_craft_force':'NOT_DERIVED',
         'SI_energy_lt10MJ':'NOT_CERTIFIED',
         'full_mode_stability':'NOT_CERTIFIED',
         'nonlocal_fixed_N_kernel_rejects_pointwise_local_chi':'YES_WITHIN_PH16_REDUCTION'},
      'arrays':{
         'fixed_N_P_Hessian':np.asarray(s['H'],dtype='<f8'),
         'rank_two_Schur_correction':np.asarray(s['dH'],dtype='<f8'),
         'local_chi':np.asarray(s['chi'],dtype='<f8'),
         'E_X_3D':np.asarray(s['E'],dtype='<f8'),
         'B_Y_3D':np.asarray(s['B'],dtype='<f8'),
      }}
