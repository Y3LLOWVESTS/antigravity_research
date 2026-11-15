"""HOOK17-PH10: bounded finite-well eigenmodes and gauge-loading obstruction.

Purpose
-------
Check whether PH8-PH9's off-shell charged scalar amplitudes can be replaced
by *actual stationary eigenfunctions* of a bounded linear KG matter action.
Use four species; X+/- opposite electric charge at separated locations and
Y+/- opposite charge with opposite azimuthal winding at same location.

The prescribed finite spherical square wells are explicitly NOT dynamical
support matter; their wall pressure, source work, energy and universal metric
variations are unmodeled. Modes have exponential tails and so are not strictly
compact. Gravity, source-on SI energy, full Ward/Noether/Earth reaction, stable
cycling and 1g at 1m are NOT certified. Frozen M5V untouched, 006D unreplaced.

Physics
-------
Mostly-plus signature, psi(t)=e^(+i omega t) psi(x), D=partial-iqA.
For A=0, radial mode R_l solves
  R''+2 R'/r-l(l+1)R/r² + (omega²-m²+U0*1_{r<R})R=0.
With 0<omega<m, kappa=sqrt(m²-omega²), k=sqrt(U0-kappa²),
  R_in=j_l(kr), R_out=C*k_l(kappa*r),
  k j_l'(kR)/j_l(kR) = kappa k_l'(kappa R)/k_l(kappa R).
Modes are C1 at the finite step and are exactly on-shell at zero gauge fields,
except the spherical well interface, which satisfies the weak matching law.
The chosen well is locally non-tachyonic m²-U0>0. Finite trap depth is NOT
an onboard realization of the necessary support potential.

At fixed on-shell wavefunctions, we solve their gauge-dependent electrostatic
and magnetostatic Maxwell equations and then compute the newly induced charged
scalar EOM residual. It MUST remain nonzero; a fully coupled stationary solution
requires iterating the matter wavefunctions and deriving their trap supports.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from hashlib import sha256
from pathlib import Path
import math
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad
from scipy.special import spherical_jn, spherical_kn
from antigravity_research.agminer import hook17_ph9_covariant_loading_gate as ph9

BRANCH = '032H17A12D1R3X3B17-PH10'
ARCHIVES = {
  'ph9_source':('src/antigravity_research/agminer/hook17_ph9_covariant_loading_gate.py','6778d91755c6669625e363ae568f7887b1a28327817f005dc0ba858774982858'),
  'ph9_result':('results/data/032h17_ph9_covariant_loading_20261115T034906847682Z.json','cc71fed5e758a3d78b93783a8446ccc79a02336ce81e998b79628958679f55ff'),
  'ph8_source':('src/antigravity_research/agminer/hook17_ph8_finite_scalar_source_gate.py','e73f28a376a071602c38e95c3188a70d3b8dc553889fa8efa193c97f1368dc98'),
  'm5v_source':('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py','ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
}

@dataclass(frozen=True)
class Spec:
    n:int=64
    length:float=16.0
    mass:float=5.0
    omega:float=4.0
    electric_radius:float=1.0
    magnetic_radius:float=1.0
    offset:float=.55
    positive_charge:float=1.0
    vortex_charge:float=.5
    alpha:float=.3
    beta:float=.4
    probe_z:float=3.0

def validate(s):
    if s.n<48 or s.n%2: raise ValueError('n even >=48 required')
    if any(not math.isfinite(v) for v in asdict(s).values()):raise ValueError('All inputs finite')
    if not (0<s.omega<s.mass and 0<s.electric_radius and 0<s.magnetic_radius and 0<s.offset and s.positive_charge>0 and s.vortex_charge>0 and s.length>0):
        raise ValueError('Positive bound-state physical parameters required')
    if min(s.alpha,s.beta)<0:raise ValueError('Invalid portal control')
    if not max(s.electric_radius+s.offset,s.magnetic_radius)+1.0 < s.probe_z < s.length/2-1.:
        raise ValueError('Exterior geometric probe requires >=1m radius clearance')
    if abs(s.probe_z*s.n/s.length-round(s.probe_z*s.n/s.length))>1e-9:
        raise ValueError('Probe must align with grid')

def radial_mode(l,R,m,omega):
    """Exact l=0 or l=1 C1 bound state of a finite-depth sphere."""
    if l not in (0,1) or not 0<omega<m or R<=0:raise ValueError('Bad bound-mode input')
    kapp=math.sqrt(m*m-omega*omega)
    def mismatch(k):
        return (k*spherical_jn(l,k*R,derivative=True)/spherical_jn(l,k*R)
                -kapp*spherical_kn(l,kapp*R,derivative=True)/spherical_kn(l,kapp*R))
    # Ground mode below its first radial zero, without pole crossings.
    # j0 first zero at pi, j1 first at approximately 4.493409.
    upper=(math.pi if l==0 else 4.493409457909064)/R
    grid=np.linspace(.05/R, upper*(1-1e-5), 250)
    choices=[]
    for lo,hi in zip(grid[:-1],grid[1:]):
        if mismatch(lo)*mismatch(hi)<0:
            choices.append(brentq(mismatch,lo,hi,xtol=1e-13))
    if len(choices)!=1:raise ValueError('No unique ground radial mode')
    k=choices[0]; u0=k*k+kapp*kapp
    if u0 >= m*m:
        raise ValueError('Negative local quadratic mass in finite well')
    scale=spherical_jn(l,k*R)/spherical_kn(l,kapp*R)
    def radial(r):
        r=np.asarray(r, dtype=float)
        return np.where(r<=R,spherical_jn(l,k*r),scale*spherical_kn(l,kapp*np.maximum(r,1e-10)))
    # independent C1 boundary residual, not a finite-difference test
    inside_d=k*spherical_jn(l,k*R,derivative=True)
    outside_d=scale*kapp*spherical_kn(l,kapp*R,derivative=True)
    return {'l':l,'R':R,'m':m,'omega':omega,'k':k,'kappa':kapp,'depth':u0,
            'minimum_quadratic_mass_squared':m*m-u0,
            'boundary_value':float(spherical_jn(l,k*R)),
            'boundary_slope_jump':float(inside_d-outside_d),
            'match_residual':float(mismatch(k)),'radial':radial}

def mode_radial_residual(mode, r):
    """Independent finite-difference radial KG residual away from the wall."""
    r=np.asarray(r,dtype=float)
    h=1e-4*mode['R'];f=mode['radial']
    a=f(r);fp=(f(r+h)-f(r-h))/(2*h);fpp=(f(r+h)-2*a+f(r-h))/h**2
    well=np.where(r<mode['R'],mode['k']**2,-mode['kappa']**2)
    return fpp+2*fp/r-mode['l']*(mode['l']+1)*a/(r*r)+well*a

def normalized_fields(s):
    """Finite-energy charged scalar wavefunctions and first loaded currents."""
    validate(s)
    dx=s.length/s.n
    q=(np.arange(s.n)-s.n//2)*dx
    x,y,z=np.meshgrid(q,q,q,indexing='ij')
    rplus=np.sqrt(x*x+y*y+(z-s.offset)**2)
    rminus=np.sqrt(x*x+y*y+(z+s.offset)**2)
    rad=np.sqrt(x*x+y*y+z*z)
    m0=radial_mode(0,s.electric_radius,s.mass,s.omega)
    m1=radial_mode(1,s.magnetic_radius,s.mass,s.omega)
    fplus=m0['radial'](rplus)
    fminus=m0['radial'](rminus)
    r1=m1['radial'](rad)
    # Spherical harmonic Y_1^1 proportional to (x+i*y)/r.
    # Regular j1(r)/r at r=0; assign zero exactly at origin.
    factor=np.divide(r1,rad,out=np.full_like(rad,m1['k']/3),where=rad>1e-12)
    vortex=(x+1j*y)*factor
    vol=dx**3
    ampplus=math.sqrt(s.positive_charge/(2*s.omega*vol*np.sum(fplus*fplus)))
    ampminus=math.sqrt(s.positive_charge/(2*s.omega*vol*np.sum(fminus*fminus)))
    ampy=math.sqrt(s.vortex_charge/(2*s.omega*vol*np.sum(abs(vortex)**2)))
    p=ampplus*fplus
    n=ampminus*fminus
    yp=ampy*vortex
    ym=np.conj(yp)
    xp=p*p;xm=n*n;wy=np.abs(yp)**2
    rho0=2*s.omega*(xp-xm)
    sx=2*(xp+xm)
    sy=4*wy
    rsq=x*x+y*y
    # Y charge +/-1 and winding +/-1, angular spin current q*n=+1.
    # Avoid coordinate singularity by using u(r)^2 analytically.
    jpref=4*ampy**2*factor**2
    j0=[-jpref*y,jpref*x,np.zeros_like(x)]
    return {'s':s,'x':x,'y':y,'z':z,'dx':dx,'vol':vol,'xp':xp,'xm':xm,'yp':yp,'ym':ym,
            'rho0':rho0,'sx':sx,'sy':sy,'j0':j0,'m0':m0,'m1':m1,
            'charge_x':float(vol*np.sum(rho0)),
            'charge_y':float(vol*np.sum(2*s.omega*(wy-wy)))}

def solve(s=Spec(), orientation=1):
    """Frozen exact *ungauged* eigenfunctions with gauge-loaded Maxwell fields."""
    if orientation not in (-1,1):raise ValueError('Orientation must be +/-1')
    d=normalized_fields(s)
    vol=d['vol'];dx=d['dx'];x,y,z=d['x'],d['y'],d['z']
    _,ks,k2=ph9.k_geometry(s)
    j0=[orientation*j for j in d['j0']]
    phi,st=ph9.screened_poisson(d['rho0'],d['sx'],k2)
    av=[];ast=[]
    for j in j0[:2]:
        a,sa=ph9.screened_poisson(j,d['sy'],k2)
        av.append(a);ast.append(sa)
    av.append(np.zeros_like(phi))
    e=[-g for g in ph9.gradients(phi,ks)]
    ak=[np.fft.fftn(a) for a in av]
    b=[np.fft.ifftn(1j*(ks[(i+1)%3]*ak[(i+2)%3]-ks[(i+2)%3]*ak[(i+1)%3])).real
       for i in range(3)]
    P=sum(e[i]*b[i] for i in range(3))
    rho=d['rho0']-d['sx']*phi
    j=[j0[i]-d['sy']*av[i] for i in range(3)]
    divj=np.fft.ifftn(1j*sum(ks[i]*np.fft.fftn(j[i]) for i in range(3))).real
    dive=np.fft.ifftn(1j*sum(ks[i]*np.fft.fftn(e[i]) for i in range(3))).real
    # Scalar equations after gauge loading: F0 solves free spherical well exactly.
    # For X species at fixed amplitude, EOM adds [(omega-q phi)^2-omega²]psi.
    rp=((s.omega-phi)**2-s.omega**2)*np.sqrt(d['xp'])
    rm=((s.omega+phi)**2-s.omega**2)*np.sqrt(d['xm'])
    rel_kg_x=float(np.sqrt(vol*np.sum(rp*rp+rm*rm)/
                           (vol*np.sum(d['xp']+d['xm']))))
    # Fourier Coulomb-gauge divergence enters the charged Y EOM exactly.
    a_sq = av[0]**2 + av[1]**2
    div_a = np.fft.ifftn(1j*sum(ks[i]*ak[i] for i in range(3))).real
    # Y charge densities cancel when the two populations are equal.
    qnet=float(vol*np.sum(rho))
    # Fields are static: no same-sector E x B field momentum in these sectors.
    eb_energy=float(.5*vol*sum(np.sum(v*v) for v in e+b))
    # Stationary KG energy, with exact well potential included, but excluding
    # trap-generating matter/support and any gravitational/portal loading.
    psi=(np.sqrt(d['xp']),np.sqrt(d['xm']),
         d['yp'] if orientation==1 else d['ym'],
         d['ym'] if orientation==1 else d['yp'])
    # spatial covariant derivatives: X ∇ψ, Y ∇ψ -iq A ψ.
    grad_energy=0.
    time_energy=0.
    rest_and_trap=0.
    # represent precisely each finite-square-well V_i
    for idx,wave in enumerate(psi):
        charge=(1.,-1.,1.,-1.)[idx]
        center=(s.offset,-s.offset,0.,0.)[idx]
        radius=(s.electric_radius,s.electric_radius,s.magnetic_radius,s.magnetic_radius)[idx]
        depth=(d['m0']['depth'],d['m0']['depth'],d['m1']['depth'],d['m1']['depth'])[idx]
        rr2=x*x+y*y+(z-center)**2
        V=np.where(rr2<radius*radius,-depth,0.)
        time_energy+=float(vol*np.sum((s.omega-charge*phi)**2*abs(wave)**2)) if idx<2 else float(vol*np.sum(s.omega*s.omega*abs(wave)**2))
        rest_and_trap+=float(vol*np.sum((s.mass*s.mass+V)*abs(wave)**2))
        gk=[np.fft.ifftn(1j*ks[i]*np.fft.fftn(wave)) for i in range(3)]
        if idx>=2:
            gk=[gk[i]-1j*charge*av[i]*wave for i in range(3)]
        grad_energy+=float(vol*sum(np.sum(abs(u)**2) for u in gk))
    # Exact Y gauge correction on the continuous A=0 eigenmode.  The
    # spectral derivatives of the complex modes compute the additional
    # -2*i*q*A.grad(psi)-i*q*(div A)*psi-q² A² psi operator.
    yKG_norm=0.;y_norm=0.
    for charge,wave in ((1.,psi[2]),(-1.,psi[3])):
        gradpsi=[np.fft.ifftn(1j*ks[i]*np.fft.fftn(wave)) for i in range(3)]
        ag=sum(av[i]*gradpsi[i] for i in range(3))
        new_E=-2j*charge*ag-1j*charge*div_a*wave-a_sq*wave
        yKG_norm+=float(vol*np.sum(abs(new_E)**2))
        y_norm+=float(vol*np.sum(abs(wave)**2))
    rel_kg_y_exact=math.sqrt(yKG_norm/y_norm)
    # Independent continuum radial integration, with the finite well
    # potential included, must close gradient+rest+trap=omega²*norm.
    radial_data=[]
    for mode in (d['m0'],d['m1']):
        R=mode['R'];k=mode['k'];kappa=mode['kappa'];l=mode['l']
        coef=spherical_jn(l,k*R)/spherical_kn(l,kappa*R)
        fin=lambda r:spherical_jn(l,k*r)
        fout=lambda r:coef*spherical_kn(l,kappa*r)
        din=lambda r:k*spherical_jn(l,k*r,derivative=True)
        dout=lambda r:coef*kappa*spherical_kn(l,kappa*r,derivative=True)
        norm=quad(lambda r:r*r*fin(r)**2,0,R)[0]+quad(lambda r:r*r*fout(r)**2,R,np.inf)[0]
        spatial=quad(lambda r:r*r*din(r)**2+l*(l+1)*fin(r)**2,0,R)[0]+quad(lambda r:r*r*dout(r)**2+l*(l+1)*fout(r)**2,R,np.inf)[0]
        potential=quad(lambda r:r*r*(s.mass*s.mass-mode['depth'])*fin(r)**2,0,R)[0]+quad(lambda r:r*r*s.mass*s.mass*fout(r)**2,R,np.inf)[0]
        tail=quad(lambda r:r*r*fout(r)**2,R,np.inf)[0]/norm
        tail_at_probe=quad(lambda r:r*r*fout(r)**2,s.probe_z,np.inf)[0]/norm
        radial_data.append({'l':l,'normalization':norm,'spatial':spatial,'rest_plus_trap':potential,
                            'time':s.omega*s.omega*norm,'relative_variational_residual':abs(spatial+potential-s.omega*s.omega*norm)/(s.omega*s.omega*norm),
                            'fraction_outside_well':tail,'fraction_beyond_probe_from_its_center':tail_at_probe})
    ci=s.n//2;zi=ci+int(round(s.probe_z/dx));zneg=ci-int(round(s.probe_z/dx))
    def probe(at):
        p=float(P[ci,ci,at]);deriv=float((P[ci,ci,at+1]-P[ci,ci,at-1])/(2*dx))
        return {'P':p,'P_prime':deriv,'acceleration_shape':-(s.alpha-2*s.beta*p)*deriv}
    upper=probe(zi);lower=probe(zneg)
    return {'spec':asdict(s), 'orientation':orientation,
            'eigenstates':[{k:v for k,v in d[key].items() if k!='radial'} for key in ('m0','m1')],
            'net_charge_unloaded':d['charge_x'],'net_charge_loaded':qnet,
            'charge_y_exact_cancel':d['charge_y'],
            'max_gauss_residual':float(np.max(np.abs(dive-rho))),
            'relative_current_divergence':float(np.linalg.norm(divj.ravel())/
                                     np.sqrt(sum(np.sum(u*u) for u in j0))),
            'max_divergence_A':float(np.max(abs(div_a))),
            'CG_phi':st,'CG_vector':ast,
            'upper_probe':upper,'lower_probe':lower,
            'probe_geometric_clearance':s.probe_z-max(s.electric_radius+s.offset,s.magnetic_radius),
            'scalar_KG_residual_from_loaded_X':rel_kg_x,
            'scalar_KG_residual_from_loaded_Y_exact_gauge_correction':rel_kg_y_exact,
            'independent_continuum_radial_virial':radial_data,
            'partial_energy':{'field':eb_energy,'matter_gradient':grad_energy,
                              'matter_time':time_energy,'matter_rest_plus_prescribed_trap':rest_and_trap,
                              'sum_excluding_trap_hardware':eb_energy+grad_energy+time_energy+rest_and_trap},
            'trap_boundary_pressure':'UNRESOLVED_EXTERNAL_TRAP_ACTION',
            'nonperiodic_exterior':'NOT_SOLVED',
            'complete_portal_backreaction':'NOT_SOLVED',
            'full_charged_scalar_on_shell':'NO_AFTER_GAUGE_LOADING',
            'universal_metric_all_matter':'NOT_DERIVED',
            'whole_spacecraft_reaction':'NOT_DERIVED',
            'complete_SI_energy':'NOT_CERTIFIED'}

def provenance(root):
    result={}
    for key,(rel,expected) in ARCHIVES.items():
        path=Path(root)/rel
        if not path.is_file():result[key]={'status':'MISSING'}
        else:
            sha=sha256(path.read_bytes()).hexdigest()
            result[key]={'status':'MATCH' if sha==expected else 'HASH_MISMATCH',
                         'actual':sha,'expected':expected}
    return result

def run(root):
    s=Spec()
    primary=solve(s)
    domain=solve(replace(s,n=80,length=20.0))
    refined=solve(replace(s,n=96))
    flip=solve(s,orientation=-1)
    off=solve(replace(s,alpha=0,beta=0))
    p=primary['upper_probe'];q=domain['upper_probe']
    rel=abs(p['P']-q['P'])/abs(q['P']) if abs(q['P'])>1e-15 else math.inf
    history=provenance(root)
    assert all(m['minimum_quadratic_mass_squared']>0 for m in primary['eigenstates'])
    assert all(abs(m['boundary_slope_jump'])<1e-10 for m in primary['eigenstates'])
    assert abs(primary['net_charge_loaded'])<1e-8
    assert primary['scalar_KG_residual_from_loaded_X']>1e-5
    assert primary['scalar_KG_residual_from_loaded_Y_exact_gauge_correction']>1e-5
    assert all(r['relative_variational_residual']<1e-10 for r in primary['independent_continuum_radial_virial'])
    assert primary['partial_energy']['matter_gradient']>0
    assert primary['probe_geometric_clearance']>=1
    assert off['upper_probe']['acceleration_shape']==0
    assert flip['upper_probe']['P']==-p['P']
    assert rel<.15
    assert refined['max_gauss_residual']<.5*primary['max_gauss_residual']
    assert refined['relative_current_divergence']<.7*primary['relative_current_divergence']
    assert abs(refined['upper_probe']['P']-p['P'])<.01*abs(p['P'])
    return {'branch':BRANCH,'primary':primary,'larger_domain':domain,
            'finer_resolution':{'n':refined['spec']['n'],
               'upper_probe':refined['upper_probe'],
               'max_gauss_residual':refined['max_gauss_residual'],
               'relative_current_divergence':refined['relative_current_divergence']},
            'chirality_reversal':{'upper_probe':flip['upper_probe']},
            'portal_off':{'upper_probe':off['upper_probe']},
            'domain_P_relative_difference':rel,
            'provenance':history,
            'gates':{
                'P0_PROVENANCE':'PASS' if all(v['status']=='MATCH' for v in history.values()) else 'UNRESOLVED',
                'P1_BOUNDED_KG_ZERO_GAUGE_EIGENMODES':'PASS_EXACT_RADIAL_AND_WEAK_INTERFACE',
                'P1_SOURCE_WELL_SELF_CONSISTENT':'NO_TRAP_MATTER_ON_SHELL',
                'P1_GAUGE_LOADED_CHARGED_SCALAR_EOM':'RED_RESIDUAL_NONZERO',
                'P1_BOUNDED_TRAP_STRESS_ENERGY':'NOT_DERIVED',
                'P2_FIXED_MODE_GAUGE_LOADED_MAXWELL':'PASS_SCOPED_PERIODIC_RESIDUAL_REFINEMENT',
                'P2_REAL_3D_SOURCE_COMPACT':'NO_EXPONENTIAL_TAILS',
                'P2_PORTAL_LOADED_EOM':'NOT_DERIVED',
                'P3_UNIVERSAL_METRIC_AND_GRAVITY':'NOT_DERIVED',
                'P3_EARTH_DOWN_CRAFT_UP':'NOT_DERIVED',
                'B11_M6_COMPLETE_SIGNED_PULSE':'NOT_RUN',
                'P3_NEUTRAL_GE1G_GE1M':'NOT_CERTIFIED',
                'STRICT_FULL_ENERGY_LT10MJ':'NOT_CERTIFIED',
                '006D_REPLACED':'NO'},
            'verdict':'YELLOW_BOUNDED_WELL_ZERO_GAUGE_ON_SHELL_BUT_LOADED_SOURCE_NOT_CLOSED'}
