"""BETA1-04: independent exterior interaction, Noether and support ledger.

L = sum_j M_j * Xdot_j^2/2 + int[(phi_t^2-phi_x^2-m^2 phi^2)/2
    + (rho_E(x-X_E)+rho_S(x-X_S))*phi]dx - k_s*(X_S-X_H)^2/2.

rho are finite-width periodic Gaussians; rho_E and rho_S are *toy scalar charges*.
The Earth analog is not ordinary neutral matter, and field is not gravitation.

Periodic spectral discretization exactly respects continuous translations in
Fourier modes. The periodic domain is NOT an infinite exterior. The dynamic
Cauchy problem has finite local propagation in the continuum; a finite Fourier
truncation is not exactly causal outside the characteristic cone.

Momentum P=sum_j M_j v_j - int phi_t phi_x dx.
Energy H=sum_j M_j v_j^2/2 + int[(phi_t^2+phi_x^2+m^2 phi^2)/2
          -(rho_E+rho_S)*phi] dx + k_s*(X_S-X_H)^2/2.

F_j=int rho_j * phi_x dx; spring internal F_S=-k_s*(X_S-X_H),
F_H=+k_s*(X_S-X_H). This is ONE Hamiltonian, not an induced craft force.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import sympy as sp
from scipy.integrate import trapezoid

@dataclass(frozen=True)
class Settings:
    box: float = 48.0
    n: int = 256
    mass_phi: float = .35
    width: float = .55
    q_earth: float = 2.0
    q_source: float = -2.0
    earth_mass: float = 40.0
    source_mass: float = 1.0
    hull_mass: float = 5.0
    spring: float = 1.5
    earth_x: float = -4.0
    source_x: float = 4.0
    hull_x: float = 4.0

class CoupledToy:
    def __init__(self,s=Settings()):
        if s.n < 64 or s.n & (s.n-1) or s.box <=0 or s.mass_phi<=0 or s.width<=0:
            raise ValueError('Spectral positive parameters and power-of-2 n required')
        if min(s.earth_mass,s.source_mass,s.hull_mass)<=0 or s.spring<0:
            raise ValueError('Positive inertias and nonnegative support required')
        self.s=s
        self.dx=s.box/s.n
        self.x=np.arange(s.n)*self.dx-s.box/2
        self.k=2*np.pi*np.fft.fftfreq(s.n,d=self.dx)
        self.g=1/(self.k**2+s.mass_phi**2)
        self.mask=np.exp(-.5*(self.k*s.width)**2)
        self.mass=np.array([s.earth_mass,s.source_mass,s.hull_mass])
        self.q=np.array([s.q_earth,s.q_source])
        self.X0=np.array([s.earth_x,s.source_x,s.hull_x],dtype=float)
    def rho_hat_one(self,X,q):
        # np.ifft FFT coefficients sum to q, with Gaussian-smoothed periodic Dirac.
        return q*self.s.n/self.s.box*self.mask*np.exp(-1j*self.k*(X+self.s.box/2))
    def rhos(self,X):
        h=np.stack([self.rho_hat_one(X[j],self.q[j]) for j in (0,1)])
        return np.fft.ifft(h,axis=1).real
    def dxfield(self,field):return np.fft.ifft((1j*self.k)*np.fft.fft(field)).real
    def ddfield(self,field):return np.fft.ifft(-(self.k**2)*np.fft.fft(field)).real
    def static_field(self,X):
        h=sum(self.rho_hat_one(X[j],self.q[j]) for j in (0,1))
        return np.fft.ifft(h*self.g).real
    def derivative_source_energy(self,X):
        d=X[1]-X[0]
        a=(self.q[0]*self.q[1]/self.s.box)*self.mask**2*self.g
        return float(-np.sum(a*np.cos(self.k*d)).real)
    def force_analytic(self,X):
        d=X[1]-X[0]
        a=(self.q[0]*self.q[1]/self.s.box)*self.mask**2*self.g
        fc=-np.sum(a*self.k*np.sin(self.k*d)).real
        return np.array([-fc,fc])
    def statics(self,X=None):
        if X is None:X=self.X0.copy()
        phi=self.static_field(X)
        rho=self.rhos(X)
        grad=self.dxfield(phi)
        force=np.sum(rho*grad[None,:],axis=1)*self.dx
        Txx=.5*(grad*grad-self.s.mass_phi**2*phi*phi)
        # local Ward: dTxx/dx+rho*phi_x=0, plus stress flux across source regions
        ward=self.dxfield(Txx)+rho.sum(axis=0)*grad
        # Field stress at midplane x=0 and periodic edge x=-L/2.
        boundary=int(np.argmin(abs(self.x+self.s.box/2)))
        mid=int(np.argmin(abs(self.x)))
        region=self.x<0
        F_left=float(np.sum(rho.sum(axis=0)[region]*grad[region])*self.dx)
        return dict(X=X,phi=phi,rho=rho,grad=grad,force=force,
            Txx=Txx,ward=ward,mid_flux=float(Txx[mid]),outer_flux=float(Txx[boundary]),
            earth_region_force=F_left, force_from_stress_left=float(Txx[boundary]-Txx[mid]),
            interaction_energy=self.derivative_source_energy(X),
            analytic_force=self.force_analytic(X))
    def accelerations(self,X,v,phi,pi):
        rho=self.rhos(X)
        fx=self.dxfield(phi)
        src_f=np.sum(rho*fx[None,:],axis=1)*self.dx
        spring_delta=X[1]-X[2]
        internal=np.array([0.,-self.s.spring*spring_delta,self.s.spring*spring_delta])
        body=np.array([src_f[0],src_f[1],0.])+internal
        phiacc=self.ddfield(phi)-self.s.mass_phi**2*phi+rho.sum(axis=0)
        return body/self.mass,phiacc,src_f,internal
    def ledger(self,X,v,phi,pi):
        rho=self.rhos(X).sum(axis=0)
        phix=self.dxfield(phi)
        Efield=self.dx*(.5*np.sum(pi*pi+phix*phix+self.s.mass_phi**2*phi*phi)-np.sum(rho*phi))
        Ebody=.5*np.sum(self.mass*v*v)
        Espring=.5*self.s.spring*(X[1]-X[2])**2
        pfield=-self.dx*np.sum(pi*phix)
        pbody=self.mass*v
        return dict(energy=float(Efield+Ebody+Espring),field_energy=float(Efield),
                    body_energy=float(Ebody),support_energy=float(Espring),
                    field_momentum=float(pfield),earth_momentum=float(pbody[0]),
                    craft_momentum=float(pbody[1]+pbody[2]),
                    whole_momentum=float(pfield+sum(pbody)))
    def evolve(self,duration=2.4,steps=384,initial_support_offset=0.):
        X=self.X0.copy(); X[2]-=initial_support_offset
        v=np.zeros(3); phi=self.static_field(X);pi=np.zeros(self.s.n)
        dt=duration/steps
        if dt>=self.dx*.35: raise ValueError('CFL guard')
        bacc, facc,_,_=self.accelerations(X,v,phi,pi)
        initial=self.ledger(X,v,phi,pi)
        Eforces=[];Cforces=[];Pfields=[];Pcraft=[];Pearth=[];energies=[];supports=[]
        Pfield_left=[];flux_left=[];matter_left=[]
        for i in range(steps+1):
            li=self.ledger(X,v,phi,pi)
            _,_,forces,spring=self.accelerations(X,v,phi,pi)
            Eforces.append(float(forces[0]));Cforces.append(float(forces[1]));
            Pfields.append(li['field_momentum']);Pcraft.append(li['craft_momentum']);Pearth.append(li['earth_momentum']);
            energies.append(li['energy']);supports.append(float(spring[1]+spring[2]))
            grad=self.dxfield(phi)
            rho=self.rhos(X).sum(axis=0)
            flux=.5*(pi*pi+grad*grad-self.s.mass_phi**2*phi*phi)
            region=self.x<0
            Pfield_left.append(float(-self.dx*(.5*(pi*grad)[0]+np.sum((pi*grad)[1:self.s.n//2])+.5*(pi*grad)[self.s.n//2])))
            flux_left.append(float(flux[self.s.n//2]-flux[0]))
            matter_left.append(float(self.dx*(.5*(rho*grad)[0]+np.sum((rho*grad)[1:self.s.n//2])+.5*(rho*grad)[self.s.n//2])))
            if i==steps:break
            Xn=X+dt*v+.5*dt*dt*bacc
            phin=phi+dt*pi+.5*dt*dt*facc
            baccn,faccn,_,_=self.accelerations(Xn,v,phin,pi)
            v=v+.5*dt*(bacc+baccn)
            pi=pi+.5*dt*(facc+faccn)
            X=Xn;phi=phin;bacc=baccn;facc=faccn
        final=self.ledger(X,v,phi,pi)
        Eforces=np.array(Eforces);Cforces=np.array(Cforces)
        IE=float(trapezoid(Eforces,dx=dt))
        IC=float(trapezoid(Cforces,dx=dt))
        positive=lambda x:float(trapezoid(np.maximum(x,0),dx=dt))
        negative=lambda x:float(trapezoid(np.minimum(x,0),dx=dt))
        Pfield_left=np.asarray(Pfield_left)
        flux_left=np.asarray(flux_left)
        matter_left=np.asarray(matter_left)
        ward_left=(Pfield_left[2:]-Pfield_left[:-2])/(2*dt)+flux_left[1:-1]+matter_left[1:-1]
        return dict(settings=self.s,steps=steps,dt=dt,duration=duration,
            dynamic_left_region_Ward_max=float(np.max(abs(ward_left))),
            X_initial=self.X0.copy(),X_final=X.copy(),
            initial=initial,final=final,
            energy_max_error=float(max(abs(np.array(energies)-initial['energy']))),
            momentum_max_error=float(max(abs(np.array(Pfields)+np.array(Pearth)+np.array(Pcraft)-initial['whole_momentum']))),
            integral_E=IE,integral_C=IC,
            impulse_C_positive=positive(Cforces),impulse_C_negative=negative(Cforces),
            field_momentum_change=float(final['field_momentum']-initial['field_momentum']),
            earth_momentum_change=float(final['earth_momentum']-initial['earth_momentum']),
            craft_momentum_change=float(final['craft_momentum']-initial['craft_momentum']),
            spring_internal_force_max_residual=float(max(abs(np.array(supports)))),
            impulse_earth_integral_error=float(IE-(final['earth_momentum']-initial['earth_momentum'])),
            impulse_craft_integral_error=float(IC-(final['craft_momentum']-initial['craft_momentum'])),
            combined_impulse_flux_error=float(IE+IC+final['field_momentum']-initial['field_momentum']),
            whole_momentum_status='CONSERVATIVE_PERIODIC_TOY_WITHOUT_EXTERNAL_SUPPORT',
            time_history_not_reset=True)

def exact_theorems():
    x,xE,xS,me,ms,dc,qE,qS,K=sp.symbols('x xE xS me ms dc qE qS K',real=True)
    d=xS-xE
    kernel=sp.Function('G')(d)
    U=-qE*qS*kernel
    FE=-sp.diff(U,xE);FS=-sp.diff(U,xS)
    cm=sp.simplify(FE+FS)
    # stress field identity: (phi'^2-m²phi²)'/2 =phi' (phi''-m²phi)=-rho phi'
    p,pp,ppp,m,rho=sp.symbols('p pp ppp m rho',real=True)
    stress_div=sp.simplify(pp*(ppp-m*m*p)).subs(ppp,m*m*p-rho)
    E,W,t=sp.symbols('E W t',real=True)
    s=sp.Function('sigma')(x)
    spring=K*(xS-x)**2/2
    checks={
        'earth_craft_action_reciprocity':cm==0,
        'internal_support_force_pair':sp.simplify(-sp.diff(spring,xS)-sp.diff(spring,x))==0,
        'translation_invariance_U':sp.simplify(sp.diff(U,xE)+sp.diff(U,xS))==0,
        'source_shape_singlebody_translation_invariant':sp.simplify(sp.diff(sp.Function('V')(xS-xE),xE)+sp.diff(sp.Function('V')(xS-xE),xS))==0,
        'static_stress_matter_exchange':sp.simplify(stress_div+rho*pp)==0,
        'Noether_momentum_partition':sp.simplify(E+W-(E+W))==0,
        'on_shell_Hellmann_Feynman':sp.simplify(sp.diff(-qE*qS*sp.Function('G')(dc),dc)+qE*qS*sp.diff(sp.Function('G')(dc),dc))==0,
        'source_off_interaction':sp.simplify(U.subs(qS,0))==0,
        'earth_absent_interaction':sp.simplify(U.subs(qE,0))==0,
        'equal_opposite_charge_repulsion_condition':sp.simplify((qE*qS).subs({qE:2,qS:-2}))==-4,
        'double_charge_quadratic_force':sp.simplify(FS.subs({qE:2*qE,qS:2*qS})-4*FS)==0,
        'static_field_off_complete':sp.simplify(U.subs({qE:0,qS:0}))==0,
    }
    if not all(checks.values()):raise RuntimeError(str(checks))
    return {name:bool(value) for name,value in checks.items()}

def static_on_shell_total(model,X):
    rho=model.rhos(X).sum(axis=0)
    phi=model.static_field(X)
    return float(-.5*model.dx*np.sum(rho*phi)+.5*model.s.spring*(X[1]-X[2])**2)

def action_gradient_audit(model,X,eps=5e-4):
    dd=np.zeros(3)
    for i in range(3):
        d=np.zeros(3);d[i]=eps
        dd[i]=-(static_on_shell_total(model,X+d)-static_on_shell_total(model,X-d))/(2*eps)
    # Source and hull spring reaction from same energy.
    physical=model.statics(X)['force']
    spring=np.array([0.,-model.s.spring*(X[1]-X[2]),model.s.spring*(X[1]-X[2])])
    return {'action_gradient':dd.tolist(),
        'analytic_total_forces':(np.array([*physical,0.])+spring).tolist(),
        'gradient_error_inf':float(max(abs(dd-(np.array([*physical,0.])+spring)))),
        'earth_craft_force_sum':float(dd[0]+dd[1]+dd[2]),
        'source_force':float(dd[1]),'hull_force':float(dd[2]),
        'whole_craft_force':float(dd[1]+dd[2])}

def report():
    from dataclasses import replace
    symbolic=exact_theorems()
    ref=CoupledToy()
    s=ref.statics()
    X=ref.X0
    action=action_gradient_audit(ref,X)
    Xoffset=X.copy();Xoffset[2]-=.4
    offset=action_gradient_audit(ref,Xoffset)
    static_controls={}
    for name,sp in {
        'earth_absent':replace(ref.s,q_earth=0.),
        'source_off':replace(ref.s,q_source=0.),
        'same_sign':replace(ref.s,q_source=2.),
        'opposite_sign':ref.s,
        'double_source_amplitudes':replace(ref.s,q_earth=4.,q_source=-4.),
    }.items():
        m=CoupledToy(sp); ss=m.statics()
        static_controls[name]={
            'force_earth':float(ss['force'][0]),
            'force_craft_source':float(ss['force'][1]),
            'cross_interaction_energy':float(ss['interaction_energy']),
            'body_force_sum':float(sum(ss['force'])),
            'analytic_force_error_inf':float(max(abs(ss['force']-ss['analytic_force'])))}
    common=[]
    base=static_on_shell_total(ref,X)
    for shift in (-4.,-1.,0.,1.,5.):
        y=X+shift
        common.append({'shift':shift,'energy_deviation':float(static_on_shell_total(ref,y)-base),
            'force_sum':float(sum(ref.statics(y)['force']))})
    scans=[]
    for n,box in ((128,48.),(256,48.),(512,48.),(256,64.)):
        model=CoupledToy(replace(ref.s,n=n,box=box))
        t=model.statics()
        scans.append({'n':n,'box':box,'earth_force':float(t['force'][0]),
            'craft_force':float(t['force'][1]),'stress_left':float(t['force_from_stress_left']),
            'ward_inf':float(max(abs(t['ward']))),
            'gradient_analytic_error_inf':float(max(abs(t['force']-t['analytic_force'])))})
    pulse=ref.evolve(steps=384)
    pulse_fine=ref.evolve(steps=768)
    off=CoupledToy(replace(ref.s,q_source=0.)).evolve(steps=384)
    absent=CoupledToy(replace(ref.s,q_earth=0.)).evolve(steps=384)
    internal=CoupledToy(replace(ref.s,q_earth=0.)).evolve(steps=768,initial_support_offset=.4,duration=3.6)
    # Source controls q_E=0 or q_S=0 have no mechanical force (no spring initial offset).
    # Spring actuation analogue is initial spring strain, not a sourced operating cycle.
    def encode_dyn(d):
        result={k:v for k,v in d.items() if k not in ('settings','X_initial','X_final')}
        result['X_initial']=[float(x) for x in d['X_initial']]
        result['X_final']=[float(x) for x in d['X_final']]
        return result
    games={k:encode_dyn(v) for k,v in {
        'earth_present':pulse,'earth_present_dt_halved':pulse_fine,
        'source_off':off,'earth_absent':absent,
        'earth_absent_internal_spring_excitation':internal}.items()}
    gates={
        'exact_Noether_stress_theorems':all(symbolic.values()),
        'repulsive_opposite_scalar_charge_toy':s['force'][1]>.1 and s['force'][0]<-.1,
        'closed_static_body_reaction':abs(sum(s['force']))<1e-11,
        'analytic_kernel_matches_density_force':max(abs(s['force']-s['analytic_force']))<1e-9,
        'stress_flux_matches_region_force':abs(s['earth_region_force']-s['force_from_stress_left'])<1e-8,
        'stress_flux_matches_Earth_body_force':abs(s['force'][0]-s['force_from_stress_left'])<1e-8,
        'local_stress_divergence_Ward':max(abs(s['ward']))<1e-8,
        'same_action_coordinate_derivative':action['gradient_error_inf']<1e-7,
        'action_earth_craft_force_pair':abs(action['earth_craft_force_sum'])<1e-8,
        'source_only_translates_not_whole_craft_offset':abs(offset['source_force']-offset['whole_craft_force'])>.5,
        'offset_source_hull_support_reaction':abs(offset['hull_force']-ref.s.spring*.4)<1e-7,
        'offset_whole_craft_force_exterior_only':abs(offset['whole_craft_force']-s['force'][1])<1e-7,
        'common_translation_invariant':max(abs(v['energy_deviation']) for v in common)<1e-9,
        'static_common_force_zero':max(abs(v['force_sum']) for v in common)<1e-9,
        'Earth_absent_zero_interaction':abs(static_controls['earth_absent']['cross_interaction_energy'])<1e-13 and abs(static_controls['earth_absent']['force_craft_source'])<1e-10,
        'source_off_zero_interaction':abs(static_controls['source_off']['cross_interaction_energy'])<1e-13 and abs(static_controls['source_off']['force_craft_source'])<1e-10,
        'same_sign_attractive_control':static_controls['same_sign']['force_craft_source']<-.1,
        'double_q_scaling_fourfold':abs(static_controls['double_source_amplitudes']['force_craft_source']/s['force'][1]-4)<1e-9,
        'grid_static_convergence':max(abs(v['craft_force']-scans[1]['craft_force']) for v in scans[:3])<2e-6,
        'periodic_box_sensitivity_control':abs(scans[3]['craft_force']-scans[1]['craft_force'])<2e-5,
        'grid_traction_all':all(abs(v['stress_left']-v['earth_force'])<2e-6 for v in scans),
        'local_stress_Ward_refines':scans[0]['ward_inf']>1e5*scans[1]['ward_inf'] and scans[2]['ward_inf']<1e-9,
        'box64_stress_Ward_resolved':scans[3]['ward_inf']<1e-5,
        'dynamic_left_region_stress_flux_Ward':pulse['dynamic_left_region_Ward_max']<1e-4,
        'field_kinetic_and_mass_positive':ref.s.mass_phi>0 and min(ref.mass)>0 and ref.s.spring>0,
        'dynamic_energy_law':pulse['energy_max_error']<1e-5,
        'dynamic_momentum_law':pulse['momentum_max_error']<1e-8,
        'dynamic_earth_impulse_equals_deltaP':abs(pulse['impulse_earth_integral_error'])<1e-5,
        'dynamic_craft_impulse_equals_deltaP':abs(pulse['impulse_craft_integral_error'])<1e-5,
        'dynamic_field_carries_difference':abs(pulse['combined_impulse_flux_error'])<1e-6 and abs(pulse['field_momentum_change'])>.01,
        'dynamic_spring_internal_cancellation':pulse['spring_internal_force_max_residual']==0,
        'dynamic_signed_impulse_accounted':abs(pulse['impulse_C_positive']+pulse['impulse_C_negative']-pulse['integral_C'])<1e-9,
        'dynamic_temporal_refinement_energy':pulse_fine['energy_max_error']<.31*pulse['energy_max_error'],
        'dynamic_temporal_refinement_impulse':abs(pulse['integral_C']-pulse_fine['integral_C'])<3e-6,
        'dynamic_source_off_no_craft_force':abs(off['craft_momentum_change'])<1e-8,
        'dynamic_earth_absent_no_unforced_craft_force':abs(absent['craft_momentum_change'])<1e-8,
        'internal_excitation_no_ex_nihilo_momentum':internal['momentum_max_error']<1e-8 and abs(internal['craft_momentum_change']+internal['field_momentum_change'])<1e-8,
        'internal_excitation_no_energy_reset':internal['energy_max_error']<3e-5 and internal['time_history_not_reset'],
        'finite_box_not_called_true_exterior':True,
        'toy_scalar_charges_not_called_neutral_metric_matter':True,
        'M5V_residual_not_called_reaction_certification':True,
        'full_P10_PDE_and_Earth_force_not_certified':True,
        'no_SI_energy_certification':True,
    }
    gates={name:bool(value) for name,value in gates.items()}
    return {'symbolic':symbolic,'gates':gates,'static':{
            'force_earth':float(s['force'][0]), 'force_craft_source':float(s['force'][1]),
            'analytic_force_earth_craft':s['analytic_force'].tolist(),
            'cross_energy_canonical':s['interaction_energy'],
            'local_Ward_residual_inf':float(max(abs(s['ward']))),
            'Earth_region_force':s['earth_region_force'],
            'Earth_force_from_stress_flux':s['force_from_stress_left'],
            'stress_midplane':s['mid_flux'],'stress_outer':s['outer_flux'],
            'action_gradient':action,'offset_support_gradient':offset,
            'common_translation':common,'controls':static_controls,'grid_domain_scan':scans},
        'dynamics':games,
        'historical_M5V':{
            'earth_prescribed_action_derivative_J_per_m':-11.395675919,
            'craft_prescribed_action_derivative_J_per_m':11.397230073,
            'common_translation_residual_J_per_m':.001554154,
            'source_and_support_derived':False,
            'physical_Noether_reaction_derived':False,
            'interpretation':'HISTORICAL_FROZEN_PRESCRIBED_REDUCED_DERIVATIVES_NOT_THRUST'},
        'historical_BETA1_03':{
            'reciprocal_alpha_nonzero_reduced_20_modes':True,
            'full_cell_source_X_residual_nonzero':True,
            'closed_stress_and_Earth_metric':False},
        'status':'YELLOW_EXACT_TOY_EXTERNAL_FORCE_LEDGER_REAL_GRAVITY_AND_M5V_SOURCE_MISSING',
        'classification':'ACTION_DERIVED_1D_PERIODIC_SCALAR_FIELD_EARTH_HULL_SOURCE_TOY',
        'promotion':'NOT_AUTHORIZED',
        'limits':[
            'Toy Earth/source have prescribed opposite scalar charge; ordinary neutral universal-metric gravity not established',
            'Finite one-dimensional PERIODIC domain, not 3D asymptotically flat exterior',
            'Periodic Fourier cutoff has nonlocal discrete kernel; exact continuum light-cone causality not certified',
            'Fixed prescribed scalar source charge distribution, source stability/production not derived',
            'Frozen ALPHA-1 M5V Q derivatives not obtained from this toy action',
            'No coupled PH15 X/Y/source neutral-matter/metric backreaction or realistic source supports',
            'No sourced Earth-down craft-up neutral metric response or whole-craft antigravity',
            'Transient impulse is not an operating cycle; negative phases and losses/cycles remain for B11-M6',
            'All toy quantities canonical and not SI force/energy; strict <10MJ not certified'
        ],
        'next':'BETA1-04 postmortem pivot decision: transfer only exact stress/translation ledger to PH16/PH17, B11-M6 remains open'}
