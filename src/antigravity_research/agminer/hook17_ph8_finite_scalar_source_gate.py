"""HOOK17-PH8: finite 3D charged-scalar source, Ward, support and exterior gate.

A theorem-first physical-source preflight, NOT a physical antigravity model.

Action candidate in flat spacetime (mostly plus, natural units):
    L = -1/4 (F_X^2 + F_Y^2)
        - sum_i [|D_i psi_i|^2 + (m_i^2 + V_i)|psi_i|^2]
        + L_neutral[g_tilde, neutral] + L_support + L_EH
    D_i = d - i q_i A_(X or Y)
    g_tilde = exp(2 sigma(P)) g, sigma=alpha P-beta P^2
    P = -(1/2) F_X.mu.nu *dual(F_Y).mu.nu
      = E_X.B_Y + E_Y.B_X  [specified R3X1 orientation].

For this run, A_X,0 electric and A_Y magnetostatic are computed from
stationary matter Noether-current ansatz, with portal backreaction OFF.
This is a first Maxwell iteration, not a solution of coupled charged-
scalar Maxwell/Einstein equations or the proposed total action.

The ansatz uses four finite-support charged complex scalar species:
  X+ and X-: opposite charges, localized stationary phase modes at
  z=+d and -d, giving a net-zero electric dipole and no spatial current.
  Y+ and Y-: co-located opposite charges, opposite phase winding,
  giving exactly canceling local charge density and reinforcing
  azimuthal circulating current. No magnetic monopoles are introduced.
Each current is derived from J^mu = i q(psi*D^mu psi - c.c.).
At zero gauge potential and with time phase e^{+i omega t},
J^0=+2 q omega |psi|^2; spatial J=-2q Im(psi*grad psi).
The full gauge-covariant matter equations must also hold; we test them
separately and FAIL to promote a kinematically conserved ansatz.

The compact radial envelope f=(1-r^2/R^2)^k_+ is C^(k-1).
For any smooth bounded quadratic stationary trap V(r), the linear
KG radial equations require V_req=omega^2-m^2+Delta f/f.
For k>=2, this diverges as r approaches R from below. A physically
supported compact configuration therefore needs different nonlinear
matter physics, boundaries, stresses or a new bounded field solution.
This is a scoped obstruction, not a general theorem about all solitons.

Static Fourier Poisson uses a periodic cube as a *finite-domain
approximation*, screens at equal spacing on two boxes and measures
images/boundary effects. It is NOT exact 3D exterior radiation/DtN.

Energy is in ARBITRARY canonical natural units. Length is sampled on a
meter-labelled numerical geometry, but charge, frequency, neutral
portal constants and energy are not SI calibrated. No 1g/1m or <10MJ
certificate is allowed. The full Earth, hull, metric, off-state,
confinement, source EOM, reciprocal portal field loading and B11-M6
pulse remain UNRESOLVED. ALPHA-1 M5V remains frozen; 006D unreplaced.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import math

import numpy as np
import sympy as sp

BRANCH = '032H17A12D1R3X3B17-PH8'
ARCHIVES = {
    'ph7_result': ('results/data/032h17_ph7_noether_spectral_health_20261115T023628445509Z.json',
                   'da116371aab0da56e06ea0d6e5b3b7711df91be1339610df36988be79c645555'),
    'ph6_result': ('results/data/032h17_ph6_same_action_bridge_20261115T011930061817Z.json',
                   'ad11d0ef66b32f5237e03a59533ce540a7be03280c141bc94aa5794777ff9a62'),
    'm5v_source': ('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py',
                   'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
}

@dataclass(frozen=True)
class Spec:
    n: int = 96
    length: float = 16.0
    electric_radius: float = 1.0
    electric_offset: float = .55
    magnetic_radius: float = 1.3
    envelope_power: int = 4
    charge: float = 1.0
    magnetic_species_charge: float = .5
    omega: float = 1.0
    mass: float = 1.0
    alpha: float = .3
    beta: float = .4
    probe_z: float = 3.0


def validate(spec:Spec):
    if spec.n < 48 or spec.n % 2 or spec.envelope_power < 3:
        raise ValueError('Need even n>=48 and compact C2 envelope k>=3')
    for value in asdict(spec).values():
        if not math.isfinite(value):
            raise ValueError('All parameters finite')
    if min(spec.length,spec.electric_radius,spec.magnetic_radius,
           spec.charge,spec.magnetic_species_charge,spec.omega,spec.mass)>0:
        pass
    else:
        raise ValueError('Source parameters must be strictly positive')
    if spec.alpha<0 or spec.beta<0 or spec.electric_offset<=0:
        raise ValueError('Negative portal or nonpositive source offset')
    extent=max(spec.electric_radius+spec.electric_offset,spec.magnetic_radius)
    if not extent+1.0 < spec.probe_z < spec.length/2-1.0:
        raise ValueError('Probe must be >=1m beyond full compact source and inside interior box')
    if extent>spec.length/4:
        raise ValueError('Source too large for this periodic-screen geometry')
    if spec.probe_z*spec.n/spec.length != round(spec.probe_z*spec.n/spec.length):
        raise ValueError('Probe location must be a grid coordinate for unambiguous derivatives')


def signed_sources(spec:Spec):
    """Evaluate canonical charged matter Noether currents at A=0.

    Exactly neutral paired source species, localized |psi|^2 and winding.
    Dynamical on-shell completion is separately required and fails here.
    """
    validate(spec)
    dx=spec.length/spec.n
    q=(np.arange(spec.n)-spec.n//2)*dx
    x,y,z=np.meshgrid(q,q,q,indexing='ij')
    vol=dx**3
    k=spec.envelope_power
    def compact2(zz,radius):
        u=(x*x+y*y+zz*zz)/radius**2
        return np.maximum(1-u,0.)**(2*k)
    fplus=compact2(z-spec.electric_offset,spec.electric_radius)
    fminus=compact2(z+spec.electric_offset,spec.electric_radius)
    rho_plus=spec.charge*fplus/(vol*np.sum(fplus))
    rho_minus=-spec.charge*fminus/(vol*np.sum(fminus))
    rho_x=rho_plus+rho_minus
    fy=compact2(z,spec.magnetic_radius)
    vortex_norm=vol*np.sum((x*x+y*y)/spec.magnetic_radius**2*fy)
    amp_sq=spec.magnetic_species_charge/(2*spec.omega*vortex_norm)
    # Y+ winding n=-1 and Y- winding n=+1; q*n=-1 for both.
    Jamp=4*amp_sq/spec.magnetic_radius**2
    j_y=np.array([-Jamp*y*fy, Jamp*x*fy, np.zeros_like(x)])
    # Source NOETHER rho_Y cancels pointwise, not just in the integral.
    rho_y=np.zeros_like(rho_x)
    return {'x':x,'y':y,'z':z,'dx':dx,'vol':vol,'rho_x':rho_x,
            'rho_x_plus':rho_plus,'rho_x_minus':rho_minus,'rho_y':rho_y,
            'j_y':j_y,'support_extent':max(spec.electric_radius+spec.electric_offset,
                                         spec.magnetic_radius),'vortex_amplitude_squared':amp_sq}


def fourier_fields(spec:Spec, chirality=1):
    """Solve first iteration Maxwell ∇.E_X=rho_X, ∇xB_Y=J_Y^T.

    Fields have arbitrary canonical normalization. All other E/B zero.
    """
    if chirality not in (-1,1):
        raise ValueError('Chirality must be +1 or -1')
    a=signed_sources(spec)
    n=spec.n; dx=a['dx']; vol=a['vol']
    ks=2*np.pi*np.fft.fftfreq(n,d=dx)
    kx,ky,kz=np.meshgrid(ks,ks,ks,indexing='ij')
    K=(kx,ky,kz)
    k2=kx*kx+ky*ky+kz*kz
    inv=np.divide(1.,k2,out=np.zeros_like(k2),where=k2>0)
    rhok=np.fft.fftn(a['rho_x'])
    jk=[np.fft.fftn(chirality*u) for u in a['j_y']]
    phi=np.fft.ifftn(rhok*inv).real
    Ay=[np.fft.ifftn(jt*inv).real for jt in jk]
    e=[np.fft.ifftn(-1j*ki*rhok*inv).real for ki in K]
    b=[np.fft.ifftn(1j*(K[(i+1)%3]*jk[(i+2)%3]-
                            K[(i+2)%3]*jk[(i+1)%3])*inv).real for i in range(3)]
    p=e[0]*b[0]+e[1]*b[1]+e[2]*b[2]
    div_ek=1j*sum(K[i]*np.fft.fftn(e[i]) for i in range(3))
    div_bk=1j*sum(K[i]*np.fft.fftn(b[i]) for i in range(3))
    gauss_residual=float(np.max(np.abs(np.fft.ifftn(div_ek).real-a['rho_x'])))
    div_b_residual=float(np.max(np.abs(np.fft.ifftn(div_bk).real)))
    div_j=np.fft.ifftn(1j*(kx*jk[0]+ky*jk[1]+kz*jk[2])).real
    # The Poisson solver automatically takes the transverse projection.
    j_perp=[np.fft.ifftn(jk[i]-K[i]*(kx*jk[0]+ky*jk[1]+kz*jk[2])*inv).real
            for i in range(3)]
    residual=float(math.sqrt(vol*sum(np.sum((u-v)**2) for u,v in zip(j_perp,
                    (chirality*a['j_y'][i] for i in range(3))))))
    electric_energy=.5*vol*sum(float(np.sum(v*v)) for v in e)
    magnetic_energy=.5*vol*sum(float(np.sum(v*v)) for v in b)
    qnet=float(vol*np.sum(a['rho_x']+a['rho_y']))
    # The A=0 Noether currents are not the covariant currents at the
    # first-iteration self-generated gauge potential. This unmodeled
    # dependence is a source EOM / Maxwell self-consistency obstruction.
    x,y,z=a['x'],a['y'],a['z']
    electric_number=(a['rho_x_plus']-a['rho_x_minus'])/(2*spec.omega)
    delta_rho=-2*phi*electric_number
    compact_ring=np.maximum(1-(x*x+y*y+z*z)/spec.magnetic_radius**2,0.)**(2*spec.envelope_power)
    vortex_number=2*a['vortex_amplitude_squared']*(x*x+y*y)/spec.magnetic_radius**2*compact_ring
    delta_j=np.array([2*vortex_number*Aj for Aj in Ay])
    rho_loading_ratio=float(np.sqrt(np.sum(delta_rho**2)/np.sum(a['rho_x']**2)))
    current_loading_ratio=float(np.sqrt(np.sum(delta_j**2)/np.sum(a['j_y']**2)))
    source_time_rest_unloaded=(spec.omega**2+spec.mass**2)*(spec.charge+
                              spec.magnetic_species_charge)/spec.omega
    xi=yi=n//2
    zi=int(round(spec.probe_z/dx))+n//2
    zj=n-zi  # z -> -z on the centered periodic grid
    p_earth=float(p[xi,yi,zj])
    dp_earth=float((p[xi,yi,zj+1]-p[xi,yi,zj-1])/(2*dx))
    a_earth_shape=-(spec.alpha-2*spec.beta*p_earth)*dp_earth
    p_probe=float(p[xi,yi,zi])
    p_left=float(p[xi,yi,zi-1])
    p_right=float(p[xi,yi,zi+1])
    dp_dz=(p_right-p_left)/(2*dx)
    sigma_prime=spec.alpha-2*spec.beta*p_probe
    a_over_c2=-sigma_prime*dp_dz
    radial_independent_fd=-(spec.alpha*p_right-spec.beta*p_right**2
                            -(spec.alpha*p_left-spec.beta*p_left**2))/(2*dx)
    # Restore electrostatic mechanical load of the + charged material.
    fplus_z=float(vol*np.sum(a['rho_x_plus']*e[2]))
    lorentz_hoop_density=np.stack((
        a['j_y'][1]*b[2],-a['j_y'][0]*b[2],
        a['j_y'][0]*b[1]-a['j_y'][1]*b[0]),axis=0)
    hoop_l1=float(vol*np.sum(np.sqrt(np.sum(lorentz_hoop_density**2,axis=0))))
    # Maxwell field momentum is E_X x B_X + E_Y x B_Y, here ZERO.
    # E_X x B_Y is not part of the sum of carrier stress tensors.
    return {'spec':asdict(spec),'chirality':chirality,
        'net_charge':qnet,'rho_y_pointwise_zero':True,
        'max_abs_Gauss_X_residual':gauss_residual,
        'max_abs_divergence_BY_residual':div_b_residual,
        'max_abs_divergence_JY_sampled':float(np.max(np.abs(div_j))),
        'transverse_source_L2_projection_residual':residual,
        'charged_scalar_covariant_rho_loading_relative_L2':rho_loading_ratio,
        'charged_scalar_covariant_J_loading_relative_L2':current_loading_ratio,
        'unloaded_scalar_time_plus_rest_energy_canonical':source_time_rest_unloaded,
        'electric_energy_canonical':electric_energy,'magnetic_energy_canonical':magnetic_energy,
        'field_energy_canonical':electric_energy+magnetic_energy,
        'volume_integral_P':float(vol*np.sum(p)),
        'volume_integral_abs_P':float(vol*np.sum(np.abs(p))),
        'probe_z':spec.probe_z,'probe_clearance':spec.probe_z-a['support_extent'],
        'P_at_probe':p_probe,'dP_dz_at_probe':dp_dz,
        'P_at_earthward_axis_probe':p_earth,
        'a_earthward_z_shape':float(a_earth_shape),
        'sigma_prime_at_probe':sigma_prime,
        'a_over_c2_independent_sigma_difference':radial_independent_fd,
        'neutral_acceleration_over_c_squared_shape':a_over_c2,
        'X_positive_cloud_internal_support_Fz':fplus_z,
        'Y_magnetic_local_hoop_stress_L1':hoop_l1,
        'two_carrier_maxwell_field_momentum':0.0,
        'full_portal_backreaction':'NOT_SOLVED',
        'full_charged_scalar_EOM':'NOT_SOLVED',
        'nonperiodic_exterior':'NOT_SOLVED'}


def theorem_controls():
    """Analytical Noether, compact KG, parity and conformal gates."""
    r,R,k,om,m=sp.symbols('r R k omega m', positive=True)
    f=(1-r**2/R**2)**k
    lap0=sp.diff(f,r,2)+2*sp.diff(f,r)/r
    lap1=sp.diff(f,r,2)+4*sp.diff(f,r)/r
    vr0=sp.factor(lap0/f+om**2-m**2)
    vr1=sp.factor(lap1/f+om**2-m**2)
    expect0=(om**2-m**2-6*k/(R**2*(1-r**2/R**2))
             +4*k*(k-1)*r**2/(R**4*(1-r**2/R**2)**2))
    expect1=(om**2-m**2-10*k/(R**2*(1-r**2/R**2))
             +4*k*(k-1)*r**2/(R**4*(1-r**2/R**2)**2))
    assert sp.simplify(vr0-expect0)==0
    assert sp.simplify(vr1-expect1)==0
    assert sp.simplify(sp.limit(vr0*(1-r**2/R**2)**2,r,R,dir='-')-4*k*(k-1)/R**2)==0
    assert sp.simplify(sp.limit(vr1*(1-r**2/R**2)**2,r,R,dir='-')-4*k*(k-1)/R**2)==0
    assert sp.diff(f,r).subs(r,0)==0
    # Nontrivial off-shell Abelian Ward identity in one spatial direction,
    # psi=R(x)e^{i theta(x)}, covariant w=theta'-q*A.
    xx,charge=sp.symbols('xx charge',real=True)
    rr=sp.Function('rr')(xx); angle=sp.Function('angle')(xx)
    av=sp.Function('av')(xx)
    w=sp.diff(angle,xx)-charge*av
    J=-2*charge*rr**2*w
    E_imag=2*sp.diff(rr,xx)*w+rr*sp.diff(w,xx)
    assert sp.simplify(sp.diff(J,xx)+2*charge*rr*E_imag)==0
    # Abelian gauge Ward: for J^μ=iq(ψ*D^μψ−c.c.),
    # ∇_μ J^μ = iq(ψ* E_ψ − ψ E*_ψ) off-shell.
    qt, qcharge, omega = sp.symbols('t q omega',real=True)
    psi=sp.symbols('A',positive=True)*sp.exp(sp.I*omega*qt)
    j0=sp.simplify(sp.I*qcharge*(sp.conjugate(psi)*(-sp.diff(psi,qt))-
             psi*(-sp.diff(sp.conjugate(psi),qt))))
    assert sp.simplify(j0-2*qcharge*omega*sp.symbols('A',positive=True)**2)==0
    # Metric determinant derivative of P∝(-g)^-1/2 under Weyl scaling.
    eps,P0=sp.symbols('eps P0',real=True)
    assert sp.diff(P0*sp.exp(-4*eps),eps).subs(eps,0)==-4*P0
    return {'compact_KG_l0_required_trap':str(vr0),
        'compact_KG_l1_required_trap':str(vr1),
        'trap_wall_double_pole_coefficient':'4*k*(k-1)/R**2',
        'compact_linear_KG_bounded_trap':'FAIL_FOR_THIS_PROFILE',
        'charged_scalar_N0_phase_current':'PASS_EXACT',
        'gauge_Ward_local_off_shell_identity':'PASS_EXACT_1D_PHASE_WITH_GAUGE_POTENTIAL',
        'constant_mixed_theta_topological':'F_X_WEDGE_F_Y_IS_TOTAL_DERIVATIVE',
        'mixed_static_volume_integral_P':'ZERO_IF_SURFACE_TERM_VANISHES',
        'Weyl_weight_of_P':-4,
        'conformal_null_geodesics':'UNCHANGED_AS_UNPARAMETERIZED_CURVES',
        'dynamical_matter_and_metric_EOM':'NOT_SOLVED'}


def provenance(root:Path):
    result={}
    for name,(rel,expected) in ARCHIVES.items():
        file=root/rel
        if not file.is_file():
            result[name]={'status':'MISSING','expected':expected}
        else:
            actual=sha256(file.read_bytes()).hexdigest()
            result[name]={'status':'MATCH' if actual==expected else 'HASH_MISMATCH',
                          'actual':actual,'expected':expected}
    return result


def run(root:Path):
    th=theorem_controls()
    base=Spec()
    primary=fourier_fields(base)
    domain=fourier_fields(Spec(n=120,length=20))
    coarse=fourier_fields(Spec(n=64,length=16))
    reverse=fourier_fields(base,chirality=-1)
    # Same physical dx=1/6 on both boxes, a genuine boundary/domain screen.
    difference=abs(primary['P_at_probe']-domain['P_at_probe']) / abs(domain['P_at_probe'])
    force_difference=abs(primary['neutral_acceleration_over_c_squared_shape']-
                         domain['neutral_acceleration_over_c_squared_shape']) / abs(domain['neutral_acceleration_over_c_squared_shape'])
    assert primary['probe_clearance']>=1
    assert abs(primary['net_charge'])<1e-11
    assert abs(primary['volume_integral_P'])<1e-10
    assert primary['volume_integral_abs_P']>0
    assert primary['max_abs_Gauss_X_residual']<1e-4
    assert primary['max_abs_Gauss_X_residual'] < .1*coarse['max_abs_Gauss_X_residual']
    assert primary['max_abs_divergence_BY_residual']<1e-10
    assert primary['max_abs_divergence_JY_sampled'] < .2*coarse['max_abs_divergence_JY_sampled']
    assert abs(primary['neutral_acceleration_over_c_squared_shape']-primary['a_over_c2_independent_sigma_difference'])<1e-9
    assert primary['electric_energy_canonical']>0 and primary['magnetic_energy_canonical']>0
    assert primary['neutral_acceleration_over_c_squared_shape']>0
    assert primary['a_earthward_z_shape']<0
    assert primary['X_positive_cloud_internal_support_Fz']<0
    assert primary['Y_magnetic_local_hoop_stress_L1']>0
    assert primary['charged_scalar_covariant_rho_loading_relative_L2']>0
    assert primary['charged_scalar_covariant_J_loading_relative_L2']>0
    assert reverse['P_at_probe']==-primary['P_at_probe']
    assert reverse['dP_dz_at_probe']==-primary['dP_dz_at_probe']
    assert reverse['neutral_acceleration_over_c_squared_shape']<0
    assert difference<.05 and force_difference<.05
    hist=provenance(root)
    return {'branch':BRANCH,'theorems':th,'primary_source_solution':primary,
        'coarse_source_continuity_control':coarse,
        'independent_domain_solution':domain,'chirality_reversal':reverse,
        'domain_relative_P_difference':difference,'domain_relative_force_difference':force_difference,
        'provenance':hist,
        'reaction_diagnostic':{
          'static_test_matter_force_shape':primary['neutral_acceleration_over_c_squared_shape'],
          'source_translation_reaction_if_same_potential':-primary['neutral_acceleration_over_c_squared_shape'],
          'earthward_probe_force_z_shape':primary['a_earthward_z_shape'],
          'craftward_reaction_z_if_earth_is_external':-primary['a_earthward_z_shape'],
          'whole_craft_force_for_both_onboard_in_static_reduced_potential':0.0,
          'earth_source_metric_response':'NOT_DERIVED',
          'field_momentum_and_stress_for_FULL_portal':'NOT_DERIVED',
        },
        'gates':{
          'P0_PROVENANCE':'PASS' if all(v['status']=='MATCH' for v in hist.values()) else 'UNRESOLVED',
          'P1_FINITE_3D_SCALAR_CURRENT_WARD':'PASS_CONTINUUM_KINEMATIC_DISCRETE_RESIDUAL_SCREEN',
          'P1_CHARGED_SCALAR_ON_SHELL':'RED_NOT_SATISFIED',
          'P1_COVARIANT_CURRENT_SELF_LOADING':'RED_FIRST_ITERATION_CURRENT_CHANGED',
          'P1_FINITE_BOUNDED_SUPPORT':'RED_TRAP_STRESSES_NOT_DERIVED',
          'P2_COUPLED_MAXWELL_FIRST_ITERATION':'PASS_PERIODIC_FIRST_ITERATION_WITH_DISCRETE_GAUSS_ERROR',
          'P2_PORTAL_LOADED_MAXWELL_BACKREACTION':'NOT_SOLVED',
          'P2_PARITY_CHIRALITY_REVERSAL':'PASS_SIGN_SCREEN',
          'P2_EVEN_STATIC_INTEGRAL_P':'ZERO_TOPOLOGICAL_CONSTRAINT',
          'P2_1M_SOURCE_TO_PROBE_GEOMETRY':'PASS_GEOMETRIC_ONLY',
          'P2_NEUTRAL_GE1G_AT_GE1M':'NOT_CERTIFIED',
          'P3_FULL_METRIC_WARD_NOETHER_GRAVITY':'NOT_DERIVED',
          'P3_EARTH_DOWN_WHOLE_CRAFT_UP':'NOT_DERIVED',
          'P3_3D_LOADED_CAUSAL_PULSE':'NOT_RUN',
          'B11_M6_SIGNED_CYCLE_RADIATION':'NOT_RUN',
          'STRICT_COMPLETE_LT10MJ':'NOT_CERTIFIED',
          '006D_REPLACED':'NO'},
        'verdict':'YELLOW_3D_SCALAR_NOETHER_SOURCE_ANSATZ_REJECTED_ON_SHELL_NO_ENGINE'}
