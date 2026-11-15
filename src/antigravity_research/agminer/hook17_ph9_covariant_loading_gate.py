"""HOOK17-PH9: fixed-amplitude gauge-covariant source loading and off-shell gate.

PH8's finite neutral 3D current ansatz is NOT a charged-scalar solution.
We perform a strictly scoped improvement: given its frozen scalar amplitudes,
solve BOTH static Maxwell equations including the gauge-dependent scalar
charge/current induced by the first source-generated potentials. The source
amplitudes are NOT varied and the universal metric portal is NOT loaded.

Use mostly-plus metric and canonical scalar L=-|D psi|²-m²|psi|²,
D=partial-i q A. On a static time-harmonic e^{i omega t} scalar,
  rho_X = sum_i 2 q_i (omega-q_i phi_X) |psi_i|²
  J_Y   = sum_i 2 q_i (grad(theta_i)-q_i A_Y)|psi_i|².
Y+ charge +1/winding +1, Y- charge -1/winding -1, so their
charge densities cancel but azimuthal currents reinforce. This is the
opposite winding-label assignment to PH8's descriptive comments, required
for its positive azimuthal-current convention under the common action.
The PH8 magnetic_species_charge is a species's INTEGRATED charge,
not its elementary gauge coupling (which is |q|=1 here).

The frozen-amplitude gauge field equations are
  (-laplacian + S_X) phi_X = rho_X0
  (-laplacian + S_Y) A_Y = J_Y0,    div A_Y=0 (toroidal symmetry)
where S_X=2 sum |psi_X|², S_Y=2 sum |psi_Y|².
These are elliptic, positive operators with periodic boundaries; we solve
by independent real FFT matrix-free conjugate gradients, and check Maxwell
residuals separately. No portal-dependent constitutive current is included.

Gauge-derived current closure is necessary but NOT sufficient: the scalars
must also satisfy their own covariant Euler-Lagrange equations and a finite
support/stress action. We calculate a nonzero KG matter-EOM residual and
preserve PH8's exact compact bounded-trap obstruction. The matter kinetic,
spatial-gradient, rest and field energy ledgers are included in ARBITRARY
canonical units. Earth coupling, gravity, SI calibration, and B11-M6 remain
open. 006D unreplaced; M5V frozen. No device/lift claim.
"""
from __future__ import annotations
from dataclasses import asdict, replace
from hashlib import sha256
from pathlib import Path
import math
import numpy as np
import sympy as sp
from scipy.sparse.linalg import LinearOperator, cg
from antigravity_research.agminer import hook17_ph8_finite_scalar_source_gate as ph8

BRANCH='032H17A12D1R3X3B17-PH9'
ARCHIVES={
 'ph8_source':('src/antigravity_research/agminer/hook17_ph8_finite_scalar_source_gate.py','e73f28a376a071602c38e95c3188a70d3b8dc553889fa8efa193c97f1368dc98'),
 'ph8_result':('results/data/032h17_ph8_finite_scalar_source_20261115T030602571597Z.json','ac12a7274bcb9753ad0635fe9f1776aa54da67ee16b7255e90a9228576bc1e80'),
 'ph7_source':('src/antigravity_research/agminer/hook17_ph7_noether_spectral_health.py','0a8464eae265da7d184c26a2823ce290bd9c5ea813ec4884b0f442209498d7c4'),
 'm5v_source':('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py','ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
}

def k_geometry(s):
    dx=s.length/s.n
    ks=2*np.pi*np.fft.fftfreq(s.n,d=dx)
    k=np.meshgrid(ks,ks,ks,indexing='ij')
    k2=sum(ki*ki for ki in k)
    return dx,k,k2

def screened_poisson(rhs,screen,k2,rtol=1e-10):
    """Solve (-Delta+screen)u=rhs using FFT preconditioned CG."""
    if rhs.shape!=screen.shape or not np.all(screen>=0) or not np.any(screen>0):
        raise ValueError('Positive nonzero scalar screening density required')
    shape=rhs.shape; count=[0]
    def op(v):
        u=v.reshape(shape)
        return (np.fft.ifftn(k2*np.fft.fftn(u)).real+screen*u).ravel()
    scale=float(np.mean(screen))
    inv=1/(k2+scale)
    def pre(v):
        return np.fft.ifftn(np.fft.fftn(v.reshape(shape))*inv).real.ravel()
    A=LinearOperator((rhs.size,rhs.size),matvec=op,dtype=float)
    M=LinearOperator((rhs.size,rhs.size),matvec=pre,dtype=float)
    def step(_): count[0]+=1
    sol,flag=cg(A,rhs.ravel(),M=M,rtol=rtol,atol=0.,maxiter=300,callback=step)
    if flag!=0 or not np.all(np.isfinite(sol)):
        raise RuntimeError(f'Frozen-amplitude Maxwell solver failed CG {flag=}, iterations={count[0]}')
    u=sol.reshape(shape)
    err=float(np.linalg.norm(op(sol)-rhs.ravel())/max(np.linalg.norm(rhs.ravel()),1e-15))
    return u,{'iterations':count[0],'relative_equation_residual':err}

def gradients(v,k):
    vk=np.fft.fftn(v)
    return [np.fft.ifftn(1j*ki*vk).real for ki in k]

def scalar_amplitudes(src,s):
    """Each Y species carries integrated |Q|=magnetic_species_charge, |q|=1."""
    xp=src['rho_x_plus']/(2*s.omega)
    xm=-src['rho_x_minus']/(2*s.omega)
    x,y,z=src['x'],src['y'],src['z']
    u=np.maximum(1-(x*x+y*y+z*z)/s.magnetic_radius**2,0.)**s.envelope_power
    yp=np.sqrt(src['vortex_amplitude_squared'])*(x+1j*y)*u/s.magnetic_radius
    ym=np.conj(yp)
    return xp,xm,yp,ym

def solve(s:ph8.Spec,orientation=1):
    """Self-consistent Maxwell at frozen scalar amplitude; not full source EOM."""
    ph8.validate(s)
    if orientation not in (1,-1): raise ValueError('Orientation must be +/-1')
    src=ph8.signed_sources(s); x,y,z=src['x'],src['y'],src['z']
    dx,k,k2=k_geometry(s)
    vol=dx**3
    xp,xm,yp,ym=scalar_amplitudes(src,s)
    sx=2*(xp+xm)
    sy=2*(np.abs(yp)**2+np.abs(ym)**2)
    # Winding n=+q for q=+1 and n=-q for q=-1.
    # This matches the current PH8 orientation, not its winding comment.
    j0=[orientation*v for v in src['j_y']]
    phi,phi_solver=screened_poisson(src['rho_x'],sx,k2)
    av=[];stats=[]
    for rhs in j0[:2]:
        a,st=screened_poisson(rhs,sy,k2)
        av.append(a); stats.append(st)
    av.append(np.zeros_like(phi))
    ex=[-u for u in gradients(phi,k)]
    Ak=[np.fft.fftn(u) for u in av]
    by=[np.fft.ifftn(1j*(k[(i+1)%3]*Ak[(i+2)%3]-k[(i+2)%3]*Ak[(i+1)%3])).real for i in range(3)]
    p=sum(e*b for e,b in zip(ex,by))
    rho=src['rho_x']-sx*phi
    j=[j0[i]-sy*av[i] for i in range(3)]
    divE=np.fft.ifftn(sum(1j*k[i]*np.fft.fftn(ex[i]) for i in range(3))).real
    divJ=np.fft.ifftn(sum(1j*k[i]*np.fft.fftn(j[i]) for i in range(3))).real
    divA=np.fft.ifftn(sum(1j*k[i]*Ak[i] for i in range(3))).real
    # Independent Maxwell residual against loaded physical matter sources.
    curlB=[np.fft.ifftn(1j*(k[(i+1)%3]*np.fft.fftn(by[(i+2)%3])-
                              k[(i+2)%3]*np.fft.fftn(by[(i+1)%3]))).real for i in range(3)]
    ee=.5*vol*sum(np.sum(v*v) for v in ex)
    bb=.5*vol*sum(np.sum(v*v) for v in by)
    em_energy=ee+bb
    # All four scalars' static candidate energy without support.
    time_en=vol*np.sum((s.omega-phi)**2*xp+(s.omega+phi)**2*xm+
                       s.omega**2*(np.abs(yp)**2+np.abs(ym)**2))
    rest_en=vol*s.mass**2*np.sum(xp+xm+np.abs(yp)**2+np.abs(ym)**2)
    # Fourier derivatives of complex scalar wave functions provide a
    # source-independent gradient energy, no divided-by-r singularity.
    xxp=np.sqrt(xp); xxm=np.sqrt(xm)
    gradx=vol*sum(float(np.sum(v*v)) for a in (xxp,xxm) for v in gradients(a,k))
    yk=np.fft.fftn(yp)
    gradyp=[np.fft.ifftn(1j*ki*yk) for ki in k]
    grad_y=2*vol*sum(float(np.sum(np.abs(gradyp[i]-1j*av[i]*yp)**2)) for i in range(3))
    grad_en=gradx+grad_y
    # Free scalar KG residual after solving self-loaded Maxwell.
    Lxp=np.fft.ifftn(-k2*np.fft.fftn(xxp)).real
    Lxm=np.fft.ifftn(-k2*np.fft.fftn(xxm)).real
    KGp=Lxp+((s.omega-phi)**2-s.mass**2)*xxp
    KGm=Lxm+((s.omega+phi)**2-s.mass**2)*xxm
    kg_rel=float(np.sqrt(np.sum(KGp*KGp+KGm*KGm)/np.sum(xxp*xxp+xxm*xxm)))
    # Independently recompute PH8's first-iteration unloaded fields.
    inv=np.divide(1.,k2,out=np.zeros_like(k2),where=k2>0)
    phi0=np.fft.ifftn(inv*np.fft.fftn(src['rho_x'])).real
    a0=[np.fft.ifftn(inv*np.fft.fftn(jt)).real for jt in j0]
    b0=[np.fft.ifftn(1j*(k[(i+1)%3]*np.fft.fftn(a0[(i+2)%3])-
                              k[(i+2)%3]*np.fft.fftn(a0[(i+1)%3]))).real for i in range(3)]
    e0=[-u for u in gradients(phi0,k)]
    p0=sum(e*b for e,b in zip(e0,b0))
    zi=s.n//2+int(round(s.probe_z/dx)); ci=s.n//2
    def probe(arr):
        val=float(arr[ci,ci,zi]); d=float((arr[ci,ci,zi+1]-arr[ci,ci,zi-1])/(2*dx))
        return val,d,-(s.alpha-2*s.beta*val)*d
    po,dpo,ao=probe(p0)
    pp,dpp,aa=probe(p)
    zj=s.n//2-int(round(s.probe_z/dx))
    pn=float(p[ci,ci,zj])
    dpn=float((p[ci,ci,zj+1]-p[ci,ci,zj-1])/(2*dx))
    earth_az=-(s.alpha-2*s.beta*pn)*dpn
    j0norm=float(np.sqrt(sum(np.sum(v*v) for v in j0)))
    drhonorm=float(np.linalg.norm((rho-src['rho_x']).ravel())/np.linalg.norm(src['rho_x'].ravel()))
    djnorm=float(np.sqrt(sum(np.sum((j[i]-j0[i])**2) for i in range(3)))/j0norm)
    support_fz=float(vol*np.sum((src['rho_x_plus']-2*xp*phi)*ex[2]))
    hoop=float(vol*np.sum(np.sqrt(sum(u*u for u in (
       j[1]*by[2]-j[2]*by[1],j[2]*by[0]-j[0]*by[2],j[0]*by[1]-j[1]*by[0])))))
    return {'spec':asdict(s),'orientation':orientation,'first_iteration_P_probe':po,
            'loaded_P_probe':pp,'earthward_axis_P':pn,
            'earthward_axis_accel_z_shape':earth_az,
            'first_iteration_metric_accel_shape':ao,
            'loaded_metric_accel_shape':aa,'loaded_P_z_derivative':dpp,
            'first_iteration_P_z_derivative':dpo,'probe_clearance':s.probe_z-src['support_extent'],
            'ratio_loaded_to_first_iteration_P':pp/po if po!=0 else None,
            'relative_gauge_rho_self_loading':drhonorm,'relative_gauge_J_self_loading':djnorm,
            'source_total_charge_loaded':float(vol*np.sum(rho)),
            'max_gauss_error':float(np.max(np.abs(divE-rho))),
            'relative_ampere_error':float(np.sqrt(sum(np.sum((curlB[i]-j[i])**2) for i in range(3)))/j0norm),
            'relative_current_divergence':float(np.linalg.norm(divJ.ravel())/j0norm),
            'relative_vector_potential_divergence':float(np.linalg.norm(divA.ravel())/j0norm),
            'phi_linear_solver':phi_solver,'vector_linear_solvers':stats,
            'canonical_energy':{'field_EB':float(em_energy),'electric_E':float(ee),
                                'magnetic_B':float(bb),'matter_time':float(time_en),
                                'matter_spatial':float(grad_en),'matter_rest':float(rest_en),
                                'field_plus_matter_excluding_support':float(em_energy+time_en+grad_en+rest_en)},
            'X_positive_cloud_support_Fz':support_fz,'Y_local_hoop_force_L1':hoop,
            'electric_scalar_KG_EOM_residual_L2_per_field_L2':kg_rel,
            'finite_source_support_action':'NOT_SOLVED','metric_portal_maxwell_loading':'NOT_SOLVED',
            'full_charged_scalar_on_shell':'NO','finite_3D_nonperiodic_exterior':'NOT_SOLVED',
            'full_Earth_and_craft_force':'NOT_DERIVED','SI_energy':'NOT_CALIBRATED'}

def exact_minimal_coupling_controls():
    """Independent variations of the common canonical scalar matter L."""
    phi,At,w,q,n,r,f,m=sp.symbols('phi At omega q n r f m', real=True)
    L=f*f*((w-q*phi)**2-(n/r-q*At)**2-m*m)
    rho=-sp.diff(L,phi)
    J=sp.diff(L,At)
    assert sp.simplify(rho-2*q*f*f*(w-q*phi))==0
    assert sp.simplify(J-2*q*f*f*(n/r-q*At))==0
    # Y+/Y-: q,n=(+1,+1),(-1,-1), equal |psi|².
    yplus=rho.subs(q,1);yminus=rho.subs(q,-1)
    assert sp.simplify((yplus+yminus).subs(phi,0))==0
    Jboth=sp.simplify(J.subs({q:1,n:1})+J.subs({q:-1,n:-1}))
    assert sp.simplify(Jboth-4*f*f*(1/r-At))==0
    assert sp.simplify(sp.diff(Jboth,At)+4*f*f)==0
    return {'electric_current_from_action':'PASS_EXACT',
            'azimuthal_current_from_action':'PASS_EXACT',
            'Y_charge_cancellation':'PASS_FOR_EQUAL_DENSITIES_AND_ZERO_A0',
            'Y_winding_label':'PLUS_CHARGE_PLUS_WINDING_PH8_COMMENT_SIGN_CORRECTION',
            'Ward_on_shell_source_identity':'NOT_CLOSED_MATTER_EOM_NONZERO'}

def archival(root):
    out={}
    for k,(rel,sha) in ARCHIVES.items():
        f=Path(root)/rel
        if not f.is_file(): out[k]={'status':'MISSING'}
        else:
            actual=sha256(f.read_bytes()).hexdigest()
            out[k]={'status':'MATCH' if actual==sha else 'HASH_MISMATCH','actual':actual,'expected':sha}
    return out

def run(root):
    base=ph8.Spec(n=96)
    primary=solve(base)
    independent=solve(replace(base,n=120,length=20.0))
    coarse=solve(replace(base,n=64))
    off=solve(replace(base,alpha=0.,beta=0.))
    reverse=solve(base,orientation=-1)
    assert abs(primary['source_total_charge_loaded'])<1e-8
    assert primary['max_gauss_error']<1e-4
    assert primary['max_gauss_error']<.1*coarse['max_gauss_error']
    assert primary['relative_ampere_error']<5e-5
    assert primary['relative_current_divergence']<5e-4
    assert primary['electric_scalar_KG_EOM_residual_L2_per_field_L2']>0.1
    assert primary['canonical_energy']['matter_spatial']>0
    assert primary['loaded_metric_accel_shape']>0
    assert primary['earthward_axis_accel_z_shape']<0
    assert off['loaded_metric_accel_shape']==0
    assert reverse['loaded_metric_accel_shape']<0
    assert abs(primary['loaded_metric_accel_shape']-independent['loaded_metric_accel_shape'])/abs(independent['loaded_metric_accel_shape'])<.1
    history=archival(root)
    return {'branch':BRANCH,'action_variations':exact_minimal_coupling_controls(),
            'primary':primary,'larger_domain_same_dx':independent,
            'coarse_grid_error_control':{'max_gauss_error':coarse['max_gauss_error'],
               'relative_current_divergence':coarse['relative_current_divergence']},
            'portal_off_control':{'metric_accel_shape':off['loaded_metric_accel_shape']},
            'chirality_reversal_control':{'metric_accel_shape':reverse['loaded_metric_accel_shape']},
            'provenance':history,
            'gates':{'P0_PROVENANCE':'PASS' if all(v['status']=='MATCH' for v in history.values()) else 'UNRESOLVED',
                     'P1_CANONICAL_CURRENT_COVARIANT_CORRECTION':'PASS_FROZEN_SCALAR_AMPLITUDES',
                     'P1_STATIC_MAXWELL_SELF_LOADING':'PASS_2_U1_FIXED_AMPLITUDE_PERIODIC',
                     'P1_CHARGED_SCALAR_ON_SHELL':'RED_NONZERO_KG_EOM_RESIDUAL',
                     'P1_COMPLETE_SOURCE_SUPPORT':'NOT_DERIVED',
                     'P2_PORTAL_BACKREACTION':'NOT_DERIVED',
                     'P2_FULL_UNIVERSAL_METRIC_FOR_ALL_MATTER':'NOT_DERIVED',
                     'P3_EARTH_DOWN_FULL_CRAFT_UP':'NOT_DERIVED',
                     'P3_B11_M6_SIGNED_CYCLE':'NOT_RUN',
                     'P3_REAL_NEUTRAL_1G_1M':'NOT_CERTIFIED',
                     'P3_STRICT_COMPLETE_LT10MJ':'NOT_CERTIFIED',
                     '006D_REPLACED':'NO'},
            'verdict':'YELLOW_LOADED_MAXWELL_FIXED_SCALARS_REMAIN_OFF_SHELL_NO_ENGINE'}
