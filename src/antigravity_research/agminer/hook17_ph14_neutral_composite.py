"""HOOK17-PH14: jointly on-shell, net-neutral two-species gauged Q-ball.

SCOPED MATHEMATICAL SOURCE COMPLETION, NOT AN ANTIGRAVITY ENGINE.

Same flat-space canonical source action (mostly-plus, natural units):
    S_X = int d4x [-F_X^2/4 - sum_{i=+,-}(|D_i psi_i|^2+U_i)]
    D_i = partial - i*q_i*A_X, q_+=+e, q_-=-e,
    U_i(s)=m_i^2*s - b*s^2 + c*s^3,
    psi_i = f_i(r)*exp(i*omega_i*t), A_X=A0(r)dt.

Solve SIX radial unknown functions (f+,f+',f-,f-',A0,A0') and
TWO unknown frequencies omega+/- simultaneously. Boundary conditions:
    f+(0)=fixed, f+'(0)=f-'(0)=A0'(0)=0;
    f_i'(R)+(sqrt(m_i^2-omega_i^2)+1/R)f_i(R)=0;
    A0(R)=A0'(R)=0.
The final A0'(R)=0 is the net-charge constraint; the other A0(R)=0
fixes the gauge. f-(0) is determined dynamically rather than prescribed.

Because scalar tails are exponentially small but not zero, the boundary
conditions approximate infinity; domain, mesh, charge-flux, and stress
checks are required. Both species have separately conserved global Noether
numbers; the only local U(1)_X gauge charge is e*(N+ - N-).

This is NOT a microscopic verified material, dynamic/spectral stability,
full two-carrier universal metric, true finite-source vacuum gap, B11-M6,
Earth-directed force or SI energy. A spherically symmetric on-shell pair
cannot generate the PH13 transverse trace-induced Y field: E_X and
nabla(lambda) are radial, so curl(lambda E_X)=0. Off-shell displaced
pairs can make a first-order Y response but do not certify an engine.

006D is the unreplaced conservative GR anchor, M5V remains FROZEN.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
from pathlib import Path
import math
import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp
from scipy.optimize import brentq
from scipy.linalg import solve_banded

BRANCH = '032H17A12D1R3X3B17-PH14'
ARCHIVES = {
    'ph13_module': ('src/antigravity_research/agminer/hook17_ph13_integrated_go_no_go.py',
                    '29b5575cc997a959eafc6ee808f65a1e45f2d00a0156830e013f8ee4b250d167'),
    'ph13_result': ('results/data/032h17_ph13_integrated_go_no_go_20261115T084131765629Z.json',
                    'd3ff81588bf5a2de259aa6601d3568129cc6e4713304dc35777b3dbe46e8dc1c'),
    'ph12_module': ('src/antigravity_research/agminer/hook17_ph12_gauged_qball_source.py',
                    '24afca0234910831c357f354db8eb6dcea08bba8814be5a21e091eb03e81b363'),
    'm5v_module': ('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py',
                    'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
}

@dataclass(frozen=True)
class Spec:
    m_plus: float=1.0
    m_minus: float=1.08
    quartic: float=2.0
    sextic: float=2.0
    e: float=0.05
    plus_center: float=0.7
    radius: float=40.0
    n: int=440
    tolerance: float=1.e-8


def validate(s:Spec):
    if s.n<180 or s.n%2 or s.radius<30 or not all(math.isfinite(v) for v in asdict(s).values()):
        raise ValueError('Requires even n>=180, R>=30, finite parameters')
    if min(s.m_plus,s.m_minus,s.quartic,s.sextic,s.e,s.plus_center,s.tolerance)<=0:
        raise ValueError('Strictly positive canonical parameters required')
    if min(s.m_plus**2,s.m_minus**2)<=s.quartic**2/(4*s.sextic):
        raise ValueError('Scalar potential not strictly positive for all s>=0')


def field_equations(s:Spec, r, y, omega):
    fp,gp,fm,gm,A,h=y
    op,om=omega
    wp=op-s.e*A
    wm=om+s.e*A
    b,c=s.quartic,s.sextic
    Fp=(s.m_plus**2-wp*wp)*fp-2*b*fp**3+3*c*fp**5
    Fm=(s.m_minus**2-wm*wm)*fm-2*b*fm**3+3*c*fm**5
    FA=-2*s.e*(wp*fp*fp-wm*fm*fm)
    gp_div=np.divide(gp,r,out=np.zeros_like(gp),where=r>0)
    gm_div=np.divide(gm,r,out=np.zeros_like(gm),where=r>0)
    h_div=np.divide(h,r,out=np.zeros_like(h),where=r>0)
    return np.array([gp,np.where(r>0,Fp-2*gp_div,Fp/3),
                     gm,np.where(r>0,Fm-2*gm_div,Fm/3),
                     h,np.where(r>0,FA-2*h_div,FA/3)])


def analytic_action_checks():
    f,g,om,q,A,m,b,c=sp.symbols('f g omega q A m b c',real=True)
    W=om-q*A
    L=W**2*f*f-g*g-m*m*f*f+b*f**4-c*f**6
    J=-sp.diff(L,A)
    assert sp.simplify(J-2*q*W*f*f)==0
    force=-sp.diff(L,f)/2
    expected=(m*m-W**2)*f-2*b*f**3+3*c*f**5
    assert sp.simplify(force-expected)==0
    k=sp.symbols('k',real=True)
    assert sp.simplify(W.subs({om:om+q*k,A:A+k})-W)==0
    assert sp.simplify((m*m*f*f-b*f**4+c*f**6)
                       -(m*m-b*b/(4*c))*f*f
                       -c*f*f*(f*f-b/(2*c))**2)==0
    # For spherical rho(r), E(r), lambda(r) radial:
    rr=sp.symbols('r',positive=True)
    E0,L0=sp.Function('E0'),sp.Function('L0')
    x,y,z=sp.symbols('x y z',real=True)
    radial=sp.sqrt(x*x+y*y+z*z)
    lam=L0(radial)
    E=sp.Matrix([E0(radial)*x/radial,E0(radial)*y/radial,E0(radial)*z/radial])
    curl=sp.Matrix([sp.diff(lam*E[2],y)-sp.diff(lam*E[1],z),
                    sp.diff(lam*E[0],z)-sp.diff(lam*E[2],x),
                    sp.diff(lam*E[1],x)-sp.diff(lam*E[0],y)])
    assert all(sp.simplify(t)==0 for t in curl)
    return {'canonical_two_scalar_current':'PASS_EXACT',
            'two_radial_Euler_Lagrange':'PASS_EXACT',
            'local_gauge_covariance':'PASS_EXACT',
            'positive_phi6_potential':'PASS_EXACT',
            'spherical_trace_induced_Y':'ZERO_BY_ROTATIONAL_SYMMETRY',
            'universal_metric_all_matter':'NOT_SOLVED'}


def solve_composite(s:Spec=Spec()):
    validate(s)
    r=np.linspace(0,s.radius,s.n)
    def bc(y0,yR,p):
        op,om=p
        kp=math.sqrt(max(1.e-12,s.m_plus*s.m_plus-op*op))
        km=math.sqrt(max(1.e-12,s.m_minus*s.m_minus-om*om))
        return np.array([y0[0]-s.plus_center,y0[1],y0[3],y0[5],
                         yR[1]+(kp+1/s.radius)*yR[0],
                         yR[3]+(km+1/s.radius)*yR[2],
                         yR[4],yR[5]])
    seedp=s.plus_center*np.exp(-(r/3.)**2)
    seedm=s.plus_center*math.sqrt(s.m_plus/s.m_minus)*np.exp(-(r/3.)**2)
    y0=np.array([seedp,-2*r*seedp/9,
                 seedm,-2*r*seedm/9,
                 np.zeros_like(r),np.zeros_like(r)])
    sol=solve_bvp(lambda x,y,p:field_equations(s,x,y,p),bc,r,y0,
                  p=np.array([.913*s.m_plus,.93*s.m_minus]),
                  tol=s.tolerance,max_nodes=18000)
    if sol.status!=0:raise RuntimeError('Joint neutral source BVP failed: '+sol.message)
    if not 0<sol.p[0]<s.m_plus or not 0<sol.p[1]<s.m_minus:
        raise RuntimeError('Ungapped scalar frequency, not localized')
    return sol


def summarize_composite(s:Spec=Spec()):
    sol=solve_composite(s)
    r=np.linspace(0,s.radius,6001)
    fp,gp,fm,gm,A,h=sol.sol(r)
    op,om=map(float,sol.p)
    wp=op-s.e*A;wm=om+s.e*A
    Uplus=s.m_plus*s.m_plus*fp*fp-s.quartic*fp**4+s.sextic*fp**6
    Uminus=s.m_minus*s.m_minus*fm*fm-s.quartic*fm**4+s.sextic*fm**6
    vol=4*np.pi*r*r
    npart=float(np.trapezoid(vol*2*wp*fp*fp,r))
    nminus=float(np.trapezoid(vol*2*wm*fm*fm,r))
    qnet=s.e*(npart-nminus)
    qflux=-4*np.pi*s.radius*s.radius*h[-1]
    terms={
        'matter_time':float(np.trapezoid(vol*(wp*wp*fp*fp+wm*wm*fm*fm),r)),
        'matter_gradient':float(np.trapezoid(vol*(gp*gp+gm*gm),r)),
        'positive_scalar_potential':float(np.trapezoid(vol*(Uplus+Uminus),r)),
        'electric_inside':float(np.trapezoid(vol*h*h/2,r)),
        'electric_outside_Coulomb':float(qflux*qflux/(8*np.pi*s.radius))
    }
    energy=sum(terms.values())
    free=s.m_plus*npart+s.m_minus*nminus
    Trr=(wp*wp*fp*fp+wm*wm*fm*fm)+gp*gp+gm*gm-Uplus-Uminus-h*h/2
    Ttheta=(wp*wp*fp*fp+wm*wm*fm*fm)-gp*gp-gm*gm-Uplus-Uminus+h*h/2
    d=field_equations(s,r,sol.sol(r),sol.p)
    dUp=2*s.m_plus*s.m_plus*fp*gp-4*s.quartic*fp**3*gp+6*s.sextic*fp**5*gp
    dUm=2*s.m_minus*s.m_minus*fm*gm-4*s.quartic*fm**3*gm+6*s.sextic*fm**5*gm
    dTrr=(-2*s.e*wp*h*fp*fp+2*wp*wp*fp*gp+2*gp*d[1]-dUp
          +2*s.e*wm*h*fm*fm+2*wm*wm*fm*gm+2*gm*d[3]-dUm-h*d[5])
    mask=r>r[5]
    div=float(np.max(abs(dTrr[mask]+2*(Trr[mask]-Ttheta[mask])/r[mask])))
    virial=float(np.trapezoid(vol*(3*(wp*wp*fp*fp+wm*wm*fm*fm)
                                -(gp*gp+gm*gm)-3*(Uplus+Uminus)+h*h/2),r))
    boundary=4*np.pi*s.radius**3*Trr[-1]
    relative_virial=abs(virial-boundary)/energy
    if min(np.min(fp),np.min(fm),np.min(wp),np.min(wm))<-1.e-8:
        raise RuntimeError('Invalid on-shell two-species solution')
    return {'spec':asdict(s),'BVP_status':'SOLVED',
            'BVP_nodes':len(sol.x),'BVP_collocation_rms':float(np.max(sol.rms_residuals)),
            'omega_plus':op,'omega_minus':om,
            'f_plus_center':float(fp[0]),'f_minus_center':float(fm[0]),
            'tail_plus_relative':float(fp[-1]/fp[0]),
            'tail_minus_relative':float(fm[-1]/fm[0]),
            'Noether_plus':npart,'Noether_minus':nminus,
            'integrated_net_gauge_charge':float(qnet),
            'boundary_Gauss_flux':float(qflux),
            'absolute_charge_vs_flux_error':float(abs(qnet-qflux)),
            'relative_charge_neutrality':abs(npart-nminus)/((npart+nminus)/2),
            'center_A0':float(A[0]),'max_abs_radial_E':float(np.max(abs(h))),
            'electric_field_energy':terms['electric_inside'],
            'canonical_energy_terms':terms,
            'total_field_plus_matter_energy':float(energy),
            'free_particle_mass_threshold':float(free),
            'binding_below_free_quanta':float(free-energy),
            'energy_over_free_mass':float(energy/free),
            'integrated_spatial_stress_trace':virial,
            'surface_stress_term':float(boundary),
            'stress_virial_relative_residual':float(relative_virial),
            'local_radial_stress_divergence_max':div,
            'source_support':'NONLINEAR_SCALAR_NO_PRESCRIBED_WELL',
            'neutral_composite_is_spherical':True,
            'induced_Y_on_shell':'ZERO_BY_ROTATIONAL_SYMMETRY',
            'full_linearized_stability':'NOT_CALCULATED',
            'material_UV':'NOT_VERIFIED',
            'SI_mass_energy':'NOT_CALIBRATED'}


def isolated_single(m:float, center:float, s:Spec):
    """Independent charged isolated one-species radial BVP."""
    r=np.linspace(0,s.radius,s.n)
    e=s.e;b=s.quartic;c=s.sextic
    def ode(x,y,pars):
        f,g,A,h=y;omega=pars[0];W=omega-e*A
        sf=(m*m-W*W)*f-2*b*f**3+3*c*f**5
        sa=-2*e*W*f*f
        ga=np.divide(g,x,out=np.zeros_like(g),where=x>0)
        ha=np.divide(h,x,out=np.zeros_like(h),where=x>0)
        return np.array([g,np.where(x>0,sf-2*ga,sf/3),h,np.where(x>0,sa-2*ha,sa/3)])
    def bc(o,t,pars):
        omega=pars[0]
        k=math.sqrt(max(1e-12,m*m-omega*omega))
        return [o[0]-center,o[1],o[3],t[1]+(k+1/s.radius)*t[0],
                t[3]+t[2]/s.radius]
    f=center*np.exp(-(r/3)**2)
    h0=.15*e*np.exp(-(r/8)**2)
    initial=np.array([f,-2*r*f/9,h0,-2*r*h0/64])
    sol=solve_bvp(ode,bc,r,initial,p=[.912*m],tol=s.tolerance,max_nodes=16000)
    if sol.status!=0:raise RuntimeError('Independent reference BVP did not converge')
    x=np.linspace(0,s.radius,6001)
    f,g,A,h=sol.sol(x);w=sol.p[0];W=w-e*A
    vol=4*np.pi*x*x
    N=float(np.trapezoid(vol*2*W*f*f,x))
    E=float(np.trapezoid(vol*(W*W*f*f+g*g+m*m*f*f-b*f**4+c*f**6+h*h/2),x)
            +(e*N)**2/(8*np.pi*s.radius))
    return {'N':N,'E':E,'omega':float(w),'center_amplitude':center,
            'tail':float(f[-1]),'rms':float(np.max(sol.rms_residuals))}


def compare_separated_solitons(s:Spec, pair:dict):
    """Each isolated lump is fitted to same individual conserved N."""
    output={};energy=0
    for label,m,target,low,high in (
        ('plus',s.m_plus,pair['Noether_plus'],.68,.71),
        ('minus',s.m_minus,pair['Noether_minus'],.65,.70),
    ):
        def residual(f0):return isolated_single(m,f0,s)['N']-target
        if residual(low)*residual(high)>=0:
            raise RuntimeError('Fixed charge solitary reference unbracketed')
        fstar=brentq(residual,low,high,xtol=1e-10)
        one=isolated_single(m,fstar,s)
        if abs(one['N']-target)>1e-5:
            raise RuntimeError('Isolated reference Noether number mismatch')
        output[label]=one;energy+=one['E']
    return {'isolated_by_species':output,'separated_energy':energy,
            'joint_composite_energy':pair['total_field_plus_matter_energy'],
            'joint_lower_than_separated':pair['total_field_plus_matter_energy']<energy,
            'binding_vs_two_isolated':energy-pair['total_field_plus_matter_energy'],
            'scope':'CLASSICAL_FIXED_INDIVIDUAL_NOETHER_NUMBERS_NOT_FULL_STABILITY'}


def frozen_translation_control(s=Spec(),pair=None,n=64,length=32.):
    """Only fixed-current spatial translation, not a sourced dynamical mode.

    The Fourier Coulomb energy is pair interaction only, omitting the
    profile/phase and other field responses. No periodic artifact may be
    called a whole-craft force or a stability eigenvalue.
    """
    if pair is None:pair=summarize_composite(s)
    sol=solve_composite(s)
    dx=length/n
    coords=(np.arange(n)-n//2)*dx
    x,y,z=np.meshgrid(coords,coords,coords,indexing='ij')
    rr=np.sqrt(x*x+y*y+z*z)
    fp,gp,fm,gm,A,h=sol.sol(np.minimum(rr,s.radius).ravel()).reshape(6,*rr.shape)
    wp=sol.p[0]-s.e*A;wm=sol.p[1]+s.e*A
    rhop=2*s.e*wp*fp*fp
    rhom=-2*s.e*wm*fm*fm
    jp=np.fft.fftn(rhop);jm=np.fft.fftn(rhom)
    kv=2*np.pi*np.fft.fftfreq(n,d=dx)
    kx,ky,kz=np.meshgrid(kv,kv,kv,indexing='ij')
    kk=kx*kx+ky*ky+kz*kz
    inv=np.divide(1.,kk,out=np.zeros_like(kk),where=kk>0)
    corr=jp*np.conj(jm)*inv
    def interaction(separation):
        return float(dx**3/n**3*np.real(np.sum(corr*np.exp(-1j*kz*separation))))
    ds=(0.,.25,.5,1.,2.)
    out={str(d):interaction(d) for d in ds}
    curvature=2*(interaction(.25)-interaction(0.))/.25**2
    return {'periodic_box_length':length,'n':n,
            'frozen_pair_Coulomb_interaction':out,
            'small_relative_translation_curvature':curvature,
            'classification':'FROZEN_CHARGE_TRANSLATION_ONLY_NOT_FULL_SPECTRAL_STABILITY'}


def reduced_energy_fixed_numbers(s:Spec, fplus, fminus, Nplus, Nminus):
    """Exact discrete Gauss reloading with both individual Noether numbers fixed.

    This finite-volume radial energy is a trial-subspace stability diagnostic.
    It does not include frequency-dependent phase dynamics, angular modes,
    metric variations or physical units.
    """
    fp=np.asarray(fplus,dtype=float)
    fm=np.asarray(fminus,dtype=float)
    n=len(fp)
    if n<80 or fm.shape!=(n,) or not all(np.isfinite(fp)) or not all(np.isfinite(fm)):
        raise ValueError('Invalid radial discrete scalar profiles')
    if np.min(fp)<0 or np.min(fm)<0 or min(Nplus,Nminus)<=0:
        raise ValueError('Invalid source amplitudes or conserved Noether numbers')
    dr=s.radius/n
    edges=np.arange(n+1)*dr
    centers=(np.arange(n)+.5)*dr
    vol=(edges[1:]**3-edges[:-1]**3)/3
    edgeweight=edges[1:-1]**2/dr
    diag=np.zeros(n)
    diag[:-1]+=edgeweight
    diag[1:]+=edgeweight
    boundary=2*s.radius**2/dr
    diag[-1]+=boundary
    diag+=2*s.e*s.e*(fp*fp+fm*fm)*vol
    bands=np.zeros((3,n))
    bands[0,1:]=-edgeweight
    bands[1]=diag
    bands[2,:-1]=-edgeweight
    plus=solve_banded((1,1),bands,2*s.e*fp*fp*vol)
    minus=solve_banded((1,1),bands,-2*s.e*fm*fm*vol)
    norm=np.array([
        [8*np.pi*np.dot(vol,fp*fp*(1-s.e*plus)),
         8*np.pi*np.dot(vol,fp*fp*(-s.e*minus))],
        [8*np.pi*np.dot(vol,fm*fm*(s.e*plus)),
         8*np.pi*np.dot(vol,fm*fm*(1+s.e*minus))],
    ])
    omega_plus,omega_minus=np.linalg.solve(norm,[Nplus,Nminus])
    A=omega_plus*plus+omega_minus*minus
    Wp=omega_plus-s.e*A
    Wm=omega_minus+s.e*A
    if min(np.min(Wp),np.min(Wm))<=0:raise ValueError('Nonpositive effective phase frequency')
    Np_num=8*np.pi*np.dot(vol,Wp*fp*fp)
    Nm_num=8*np.pi*np.dot(vol,Wm*fm*fm)
    if abs(Np_num-Nplus)>1e-8 or abs(Nm_num-Nminus)>1e-8:
        raise AssertionError('Noether constraint did not close')
    components={
        'matter_time':4*np.pi*np.dot(vol,Wp*Wp*fp*fp+Wm*Wm*fm*fm),
        'matter_gradient':4*np.pi*np.dot(edgeweight,np.diff(fp)**2+np.diff(fm)**2),
        'scalar_potential':4*np.pi*np.dot(vol,s.m_plus**2*fp**2-s.quartic*fp**4+s.sextic*fp**6+s.m_minus**2*fm**2-s.quartic*fm**4+s.sextic*fm**6),
        'electric_inside':2*np.pi*np.dot(edgeweight,np.diff(A)**2),
        'electric_last_to_boundary':2*np.pi*boundary*A[-1]**2,
    }
    rhs=2*s.e*(omega_plus*fp**2-omega_minus*fm**2)*vol
    residual=diag*A
    residual[:-1]-=edgeweight*A[1:]
    residual[1:]-=edgeweight*A[:-1]
    rel=float(np.linalg.norm(rhs-residual)/max(np.linalg.norm(rhs),1e-20))
    flux=4*np.pi*boundary*A[-1]
    return {'energy':float(sum(components.values())),'components':{k:float(v) for k,v in components.items()},
            'omega_plus':float(omega_plus),'omega_minus':float(omega_minus),
            'Noether_plus':float(Np_num),'Noether_minus':float(Nm_num),
            'Gauss_relative_residual':rel,'exterior_flux':float(flux),
            'neutrality_charge':float(s.e*(Np_num-Nm_num))}


def fixed_charge_radial_subspace(s:Spec=Spec(), n:int=440, step:float=.002):
    """Twelve static radial trial directions; not full gauge-scalar dynamics."""
    if n<120 or step<=0:raise ValueError('Invalid constrained screen')
    sol=solve_composite(s)
    rr=(np.arange(n)+.5)*s.radius/n
    fp,gp,fm,gm,A,h=sol.sol(rr)
    fine=np.linspace(0,s.radius,6001)
    ff,_,gg,_,AA,_=sol.sol(fine)
    Wp=sol.p[0]-s.e*AA;Wm=sol.p[1]+s.e*AA
    Np=float(np.trapezoid(8*np.pi*fine**2*Wp*ff**2,fine))
    Nm=float(np.trapezoid(8*np.pi*fine**2*Wm*gg**2,fine))
    ref=reduced_energy_fixed_numbers(s,fp,fm,Np,Nm)
    centers=[1.1,2.4,3.8,5.5,7.0]
    # Ten independently localized species perturbations and two
    # coherent-amplitude perturbations. No artificial optimizer.
    basis=[]
    for species,profile in ((0,fp),(1,fm)):
        for center in centers:
            bump=np.exp(-.5*((rr-center)/1.25)**2)*profile
            direction=np.zeros((2,n))
            direction[species]=bump
            basis.append(direction)
        direction=np.zeros((2,n))
        direction[species]=profile
        basis.append(direction)
    B=np.array(basis)
    d=len(B)
    def ene(c):
        trial=np.array([fp,fm])+np.einsum('i,ijk->jk',c,B)
        return reduced_energy_fixed_numbers(s,trial[0],trial[1],Np,Nm)['energy']
    zero=np.zeros(d);E0=ene(zero)
    grad=[];H=np.zeros((d,d))
    for i in range(d):
        u=np.zeros(d);u[i]=step
        plus=ene(u);minus=ene(-u)
        grad.append((plus-minus)/(2*step))
        H[i,i]=(plus+minus-2*E0)/step**2
        for j in range(i):
            v=np.zeros(d);v[j]=step
            H[i,j]=(ene(u+v)-ene(u-v)-ene(-u+v)+ene(-u-v))/(4*step*step)
            H[j,i]=H[i,j]
    eig=np.linalg.eigvalsh(H)
    return {'n':n,'step':step,'modes':d,'background_fv':ref,
            'max_gradient':float(max(abs(v) for v in grad)),
            'eigenvalues':[float(z) for z in eig],
            'negative_eigenvalues':int(np.sum(eig<-1.e-4)),
            'lowest_eigenvalue':float(eig[0]),
            'classification':'RESTRICTED_STATIC_RADIAL_FIXED_TWO_NOETHER_NUMBERS_NOT_DYNAMICAL_STABILITY'}


def provenance(root):
    result={}
    for name,(relative,expected) in ARCHIVES.items():
        p=Path(root)/relative
        if not p.is_file():result[name]={'status':'MISSING','expected_sha256':expected}
        else:
            actual=sha256(p.read_bytes()).hexdigest()
            result[name]={'status':'MATCH' if actual==expected else 'HASH_MISMATCH',
                          'actual_sha256':actual,'expected_sha256':expected}
    return result


def run(root):
    exact=analytic_action_checks()
    spec=Spec()
    central=summarize_composite(spec)
    finer=summarize_composite(replace(spec,n=880,tolerance=1e-9))
    larger=summarize_composite(replace(spec,radius=48.0,n=520))
    same_masses=summarize_composite(replace(spec,m_minus=1.0))
    nearby=summarize_composite(replace(spec,m_minus=1.05))
    reference=compare_separated_solitons(spec,central)
    translated=frozen_translation_control(spec,central)
    constrained=fixed_charge_radial_subspace(spec,n=440)
    constrained_alt=fixed_charge_radial_subspace(spec,n=660,step=.001)
    assert central['relative_charge_neutrality']<1.e-8
    assert central['absolute_charge_vs_flux_error']<1.e-6
    assert central['max_abs_radial_E']>1.e-5
    assert central['stress_virial_relative_residual']<1.e-7
    assert central['local_radial_stress_divergence_max']<2.e-5
    assert central['binding_below_free_quanta']>0
    assert reference['joint_lower_than_separated']
    assert reference['binding_vs_two_isolated']>0
    assert abs(finer['total_field_plus_matter_energy']-central['total_field_plus_matter_energy'])<.001
    assert abs(larger['total_field_plus_matter_energy']-central['total_field_plus_matter_energy'])<.001
    assert same_masses['max_abs_radial_E']<1.e-7
    assert nearby['max_abs_radial_E']>1.e-6
    assert translated['small_relative_translation_curvature']>0
    assert constrained['background_fv']['Gauss_relative_residual']<1.e-9
    assert constrained_alt['background_fv']['Gauss_relative_residual']<1.e-9
    assert abs(constrained['lowest_eigenvalue']-constrained_alt['lowest_eigenvalue'])<.02
    history=provenance(root)
    return {'branch':BRANCH,'exact_action':exact,'on_shell_neutral_source':central,
            'separated_lumps_same_N_comparison':reference,
            'high_resolution':{'n':finer['spec']['n'],'energy':finer['total_field_plus_matter_energy'],
                               'charge_err':finer['relative_charge_neutrality'],
                               'stress_err':finer['stress_virial_relative_residual']},
            'larger_radius':{'R':larger['spec']['radius'],'energy':larger['total_field_plus_matter_energy'],
                             'charge_err':larger['relative_charge_neutrality']},
            'symmetric_mass_null':{'m_minus':1.,'max_abs_E':same_masses['max_abs_radial_E']},
            'asymmetric_control':{'m_minus':1.05,'max_abs_E':nearby['max_abs_radial_E']},
            'frozen_translation_only':translated,
            'restricted_fixed_two_charge_radial':constrained,
            'restricted_radial_resolution':{'n':constrained_alt['n'],
                'lowest_eigenvalue':constrained_alt['lowest_eigenvalue'],
                'negative_eigenvalues':constrained_alt['negative_eigenvalues']},
            'provenance':history,
            'gates':{
                'P0_PROVENANCE':'PASS' if all(x['status']=='MATCH' for x in history.values()) else 'UNRESOLVED',
                'P1_TWO_SPECIES_NEUTRAL_ONSHELL':'PASS_SPHERICALLY_SYMMETRIC_BVP',
                'P1_FINITE_TRAP_FREE_SOURCE':'PASS_HYPOTHETICAL_PHI6_TWO_SCALAR_SECTOR',
                'P1_ELECTRIC_NEUTRALITY':'PASS_INTEGRAL_AND_GAUSS_BOUNDARY',
                'P1_POSITIVE_SOURCE_ENERGY':'PASS_CANONICAL_FLAT_CLASSICAL',
                'P1_BINDING_VS_SEPARATED_QBALLS':'PASS_SAME_INDIVIDUAL_NOETHER_NUMBERS',
                'P1_BINDING_VS_FREE_PARTICLES':'PASS_SAME_INDIVIDUAL_NOETHER_NUMBERS',
                'P1_RADIAL_STRESS_BALANCE':'PASS_SCOPED_STATIC',
                'P1_RESTRICTED_FIXED_TWO_CHARGE_HESSIAN':('NEGATIVE_DIRECTION_FOUND' if constrained['negative_eigenvalues'] else 'NONNEGATIVE_SAMPLED_SUBSPACE_ONLY'),
                'P1_FULL_RADIAL_AND_NONRADIAL_STABILITY':'NOT_CERTIFIED',
                'P1_REAL_PARTICLES_AND_QUANTUM_UV':'NOT_CERTIFIED',
                'P2_ONSHELL_SPHERICAL_TRACE_INDUCED_Y':'EXACT_ZERO_BY_SYMMETRY',
                'P2_NONSYMMETRIC_FULL_ONSHELL_Y':'NOT_DERIVED',
                'P2_UNIVERSAL_METRIC_FULL_CONSTITUTIVE':'NOT_SOLVED',
                'P3_EARTH_DOWN_CRAFT_UP':'NOT_DERIVED',
                'B11_M6_COMPLETE_CAUSAL_IMPULSE':'NOT_RUN',
                'P3_NEUTRAL_1G_1M':'NOT_CERTIFIED',
                'STRICT_COMPLETE_LT10MJ':'NOT_CERTIFIED',
                '006D_REPLACED':'NO'},
            'verdict':'YELLOW_ONSHELL_ELECTRIC_NEUTRAL_COMPOSITE_BUT_NO_MAGNETIC_Y_OR_METRIC_LIFT'}
