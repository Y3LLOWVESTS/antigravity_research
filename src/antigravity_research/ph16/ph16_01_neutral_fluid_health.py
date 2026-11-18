"""PH16-01: covariant pullback neutral fluid, solid support and frozen-mode atlas.

Hypothetical common action (signature -+++):
  S= EH[g] -1/4∫sqrt(-g)(F_X²+F_Y²)
     + S_charged[psi_i,D_X,gtilde] + S_fluid[Phi^I,gtilde]
     + S_solid[Xi^I,gtilde]
  gtilde=exp(2sigma(P))g, sigma=alpha P-beta P²,
  P=epsilon^{munurhosigma}F_X_munu F_Y_rhosigma/4.

S_fluid=-∫sqrt(-gtilde) rho(n), rho(n)=m n+kappa n²/2;
  n=sqrt(det(gtilde^{munu}∂_mu Phi^I ∂_nu Phi^J)).
  J^mu=(1/3! sqrt(-gtilde)) epsilon^{mu nu rho sigma} epsilon_IJK
       ∂_nu Phi^I ∂_rho Phi^J ∂_sigma Phi^K, identically conserved.
S_solid has three material labels and a positive shear response, explicitly
specified in exact_atlas(); not solved with Earth/hull boundary conditions.

This run derives formal action identities, a hydrostatic *one-way* neutral
fluid response to PH15-P10's first-order Y field, and a local frozen-background
necessary magnetic-gradient health condition. A negative local principal
coefficient is a UV/high-wave-number warning in this EFT, NOT a complete
coupled dynamical eigenmode computation. The 20-mode BETA1-03 Hessian cannot
certify the omitted continuum modes.

No simultaneous source/X/Y/fluid/solid/Einstein solution and no SI units.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import sympy as sp
from antigravity_research.agminer.hook17_ph15_p10_free_space import CoulombSource, Spec
from antigravity_research.ph16.ph16_00_transfer_atlas import (
    dR, dZ, current_from_lambda, source_traces, neutral_trace_profile,
)


@dataclass(frozen=True)
class Parameters:
    nr: int = 12
    L: float = 12.0
    alpha: float = 0.05
    beta: float = 40.0
    rest_mass: float = 1.0
    compressibility: float = 0.5
    reference_density: float = 0.15
    gaussian_perturbation: float = 0.15


def exact_atlas():
    a,b,P,m,k,n,K,U,C,x = sp.symbols('alpha beta P m kappa n K U C x',real=True)
    sig=a*P-b*P**2
    nphys=n*sp.exp(-3*sig)
    rho=lambda v:m*v+k*v*v/2
    pres=sp.simplify(n*sp.diff(rho(n),n)-rho(n))
    trace=sp.simplify(-rho(n)+3*pres)
    Lf=-sp.exp(4*sig)*rho(nphys)
    Ls=-K*sp.exp(2*sig)-U*sp.exp(4*sig)
    Ltot=Ls+Lf
    sig0={P:0}
    chis=sp.diff(Ls,P,2).subs(sig0)
    chif=sp.diff(Lf,P,2).subs(sig0)
    chi=sp.expand(chis+chif)
    intended=((-4*K-16*U-m*n-2*k*n*n)*a*a
              +(4*K+8*U+2*m*n-2*k*n*n)*b)
    lam=sp.diff(Ltot,P)
    lam0=sp.expand(lam.subs(sig0))
    # Hydrostatic isentropic redshift relation mu(n(x))*exp(sigma(x))=C
    sx=sp.Function('s')(x)
    nx=(C*sp.exp(-sx)-m)/k
    mu=m+k*nx
    rho_x=rho(nx)
    p_x=k*nx*nx/2
    hydro=sp.simplify(sp.diff(p_x,x)+(rho_x+p_x)*sp.diff(sx,x))
    # Matter label identically conserved, here a 1+1 reduction.
    label=sp.Function('phi')(x,sp.Symbol('t'))
    t=label.args[1]
    Jt=sp.diff(label,x);Jx=-sp.diff(label,t)
    # Positive shear strain about unimodular identity, using B^(IJ).
    q=sp.symbols('q',real=True)
    eigs=[sp.exp(q),sp.exp(-q),sp.Integer(1)]
    shear=sum(e*e for e in eigs)-sum(eigs)**2/3
    ns,nref,ks,ms=sp.symbols('ns nref ks ms',real=True)
    solid_energy=ms*ns+ks*(ns-nref)**2/2
    solid_pressure=sp.expand(ns*sp.diff(solid_energy,ns)-solid_energy)
    # Metric P transforms under a Weyl rescaling and has a nontrivial metric variation.
    theta,P0=sp.symbols('theta P0',real=True)
    P_weyl=P0*sp.exp(-4*theta)
    # Mixed two-U1 constitutive variations (formal consistency).
    EX,EY,BY=sp.symbols('EX EY BY',real=True)
    kinetic=sp.Rational(1,2)*(EX**2+EY**2-BY**2)
    Llocal=kinetic+Ltot.subs(P,EX*BY)
    mixedA=sp.diff(sp.diff(Llocal,EX),BY)
    mixedB=sp.diff(sp.diff(Llocal,BY),EX)
    checks={
      'barotropic_rho':sp.simplify(rho(n)-m*n-k*n*n/2)==0,
      'fluid_pressure':sp.simplify(pres-k*n*n/2)==0,
      'fluid_trace':sp.simplify(trace+m*n-k*n*n)==0,
      'fluid_rho_minus_pressure':sp.simplify(rho(n)-pres-m*n)==0,
      'fluid_positive_enthalpy_formula':sp.simplify(rho(n)+pres-m*n-k*n*n)==0,
      'fluid_sound_speed_formula':sp.simplify(n*sp.diff(rho(n),n,2)/sp.diff(rho(n),n)-k*n/(m+k*n))==0,
      'pullback_density_conformal_weight_minus3':sp.simplify(nphys-n*sp.exp(-3*sig))==0,
      'fluid_conformal_action_reduction':sp.simplify(Lf+m*n*sp.exp(sig)+k*n*n*sp.exp(-2*sig)/2)==0,
      'fluid_conformal_trace_variation':sp.simplify(sp.diff((-m*n*sp.exp(sp.Symbol('z'))-k*n*n*sp.exp(-2*sp.Symbol('z'))/2),sp.Symbol('z')).subs(sp.Symbol('z'),0)-trace)==0,
      'source_lambda_chain':sp.simplify(sp.diff(Ls,P)+(2*K*sp.exp(2*sig)+4*U*sp.exp(4*sig))*(a-2*b*P))==0,
      'fluid_lambda_chain':sp.simplify(sp.diff(Lf,P)-(-m*n*sp.exp(sig)+k*n*n*sp.exp(-2*sig))*(a-2*b*P))==0,
      'total_lambda_additive':sp.simplify(lam-sp.diff(Ls,P)-sp.diff(Lf,P))==0,
      'lambda_P0_total':sp.simplify(lam0+a*(2*K+4*U+m*n-k*n*n))==0,
      'fluid_second_P_variation':sp.simplify(chif-((-m*n-2*k*n*n)*a*a+(2*m*n-2*k*n*n)*b))==0,
      'source_second_P_variation':sp.simplify(chis-((-4*K-16*U)*a*a+(4*K+8*U)*b))==0,
      'full_second_P_variation':sp.simplify(chi-intended)==0,
      'hydrostatic_mu_redshift_constant':sp.simplify(mu*sp.exp(sx)-C)==0,
      'hydrostatic_Euler_pressure_balance':hydro==0,
      'one_plus_one_baryon_current_identically_conserved':sp.simplify(sp.diff(Jt,t)+sp.diff(Jx,x))==0,
      'uniform_unconfined_fluid_requires_zero_gradient':sp.simplify(sp.diff(nx,x).subs(sp.diff(sx,x),0))==0,
      'solid_stress_free_reference':sp.simplify(solid_pressure.subs(ns,nref))==0,
      'solid_bulk_curvature':sp.simplify(sp.diff(solid_energy,ns,2)-ks)==0,
      'solid_shear_quadratic_positive_coefficient':sp.simplify(sp.diff(shear,q,2).subs(q,0)-4)==0,
      'solid_shear_no_linear_stress':sp.simplify(sp.diff(shear,q).subs(q,0))==0,
      'mixed_U1_variations_symmetric':sp.simplify(mixedA-mixedB)==0,
      'neutral_density_changes_Y_constitutive_beta':sp.simplify(sp.diff(chi,b)- (4*K+8*U+2*m*n-2*k*n*n))==0,
      'P_metric_conformal_weight_minus4':sp.simplify(sp.diff(P_weyl,theta).subs(theta,0)+4*P0)==0,
      'Pontryagin_4form_metric_invariant':sp.simplify(sp.diff(sp.exp(4*theta)*P_weyl,theta))==0,
      'Y_kinetic_sign_at_electrostatic_X':sp.simplify(sp.diff(Llocal,EY,2)-1)==0,
      'Y_magnetic_principal_Hessian':sp.simplify(sp.diff(Llocal,BY,2).subs(BY,0)+1-chi*EX**2)==0,
      'constant_lambda_topological_bulk_null':sp.simplify(sp.diff(sp.Symbol('lambda0'),x))==0,
    }
    failed=[name for name,ok in checks.items() if not ok]
    if failed:raise AssertionError('Exact action checks failed: '+str(failed))
    return {'checks':{k:bool(v) for k,v in checks.items()},
       'covariant_fluid_action':'S_n=-int sqrt(-gtilde) rho(n), n=sqrt(det(Btilde^IJ)), Btilde^IJ=gtilde^munu partial_mu Phi^I partial_nu Phi^J',
       'baryon_current':'identically conserved Hodge dual of dPhi1 wedge dPhi2 wedge dPhi3',
       'covariant_solid_action':'S_s=-int sqrt(-gtilde)[ms*n+ks/2*(n-nref)^2+mus/4*(tr(C^2)-(tr C)^2/3)], C=B/(det B)^(1/3)',
       'solid_stability_scope':'positive restricted bulk/shear strain curvature; NO full solid dynamic modes or interface solution',
       'charged_source':'two opposite-charge complex scalars D_X=partial+i q X; scalar and current EOM NOT resolved in this run',
       'gauge_equations':'nabla_mu(FX^munu-lambda *FY^munu)=J_X^nu, nabla_mu(FY^munu-lambda *FX^munu)=0; metric Hodge dual',
       'lambda_total_at_zero':str(lam0), 'chi_total_at_zero':str(chi),
       'neutral_hydrostatic_first_integral':'(m+kappa*n) exp(sigma)=constant; only conditional on fixed static geometry and absence of body/traction forces',
       'metric_P_variation':'at fixed F, delta P = (P/2) g_munu delta g^munu; Pontryagin density sqrt(-g) P metric independent',
       'matter_metric_tensor':'T_eff_munu=e^(2sigma) Ttilde_munu - lambda P g_munu; requires simultaneous metric/matter variations',
       'diffeomorphism_and_Bianchi':'total on-shell stress divergence zero required; full metric field equation NOT solved',
       'principal_caveat':'frozen matter/X electrostatic background; magnetic alignment trial not a full gauge/constrained/dynamical spectrum',
       'physical_state':'NO full source/X/Y/neutral/solid/metric joint stationary solution'}


def hydro_profile(sigma,weights,m,k,n0):
    """One-way ideal fluid equilibrium preserving integrated material-label number."""
    es=np.exp(-sigma)
    # Conserve N=int sqrt(gamma_tilde)*n = int w*exp(3sigma)*n.
    C=(k*n0*np.sum(weights)+m*np.sum(weights*np.exp(3*sigma)))/np.sum(weights*np.exp(2*sigma))
    n=(C*es-m)/k
    if np.min(n)<=0:raise ArithmeticError('Vacuum interface requires free-boundary/traction solver')
    return n,C


def trace(n,m,k):return -m*n+k*n*n


def principal_coefficients(K,U,E2,n,m,k,alpha,beta):
    # Local Lagrangian second P derivative at P=0 and fixed comoving labels.
    alpha2=(-4*K-16*U-m*n-2*k*n*n)*alpha**2
    beta1=(4*K+8*U+2*m*n-2*k*n*n)
    chi=alpha2+beta*beta1
    return chi,1-chi*E2,alpha2,beta1


def finite_difference_principal(K,U,n,E,a,b,m,k,step=3e-5):
    def loc(B):
        P=E*B;s=a*P-b*P**2
        return (-B**2/2-K*np.exp(2*s)-U*np.exp(4*s)
                -m*n*np.exp(s)-k*n*n*np.exp(-2*s)/2)
    return (loc(step)-2*loc(0.)+loc(-step))/step**2


def numerical_case(params:Parameters):
    p=params
    m=CoulombSource(Spec(nr=p.nr,L=p.L),self_order=8)
    info,f=m.solve(350)
    if max(info['scalar_equation_weighted_L2'])>5e-5 or abs(info['net_X_charge'])>1e-8:
        raise RuntimeError('Protected PH15-P10 source not on shell in base electrostatic sector')
    sh=(p.nr,2*p.nr);w=m.w.reshape(sh)
    A=f['A'].reshape(sh);K,U=source_traces(m,f)
    E_r=-dR(A,m.h);E_z=-dZ(A,m.h);E2=E_r**2+E_z**2
    lam_source=-p.alpha*(2*K+4*U)
    jsrc=current_from_lambda(A,lam_source,m.h)
    phi=(m.wmagkernel@jsrc.ravel()).reshape(sh)
    B_r=-dZ(phi,m.h);B_z=dR(phi,m.h)+phi/m.rho.reshape(sh)
    P=E_r*B_r+E_z*B_z
    sigma=p.alpha*P-p.beta*P**2
    n,C=hydro_profile(sigma,w,p.rest_mass,p.compressibility,p.reference_density)
    rho=p.rest_mass*n+.5*p.compressibility*n*n
    press=.5*p.compressibility*n*n
    mu=p.rest_mass+p.compressibility*n
    chem=mu*np.exp(sigma)
    Euler_r=dR(press,m.h)+(rho+press)*dR(sigma,m.h)
    Euler_z=dZ(press,m.h)+(rho+press)*dZ(sigma,m.h)
    chem_res=max(np.max(abs(chem-C)),np.max(abs(dR(chem,m.h))),np.max(abs(dZ(chem,m.h))))
    euler_res=max(np.max(abs(Euler_r)),np.max(abs(Euler_z)))
    norm=lambda v:float(np.sqrt(np.sum(w*v*v)))
    trace0=trace(p.reference_density,p.rest_mass,p.compressibility)
    # Hydrostatic *density rearrangement* contribution only.  Even constant
    # fluid trace affects chi and the Y operator; NOT counted as zero loading.
    jhyd=current_from_lambda(A,p.alpha*(trace(n,p.rest_mass,p.compressibility)-trace0),m.h)
    # Prescribed control: same integrated number, nonuniform profile violating
    # hydrostatic Euler unless physical supports are supplied.
    gaussian=neutral_trace_profile(m,1.)
    physical_weight=w*np.exp(3*sigma)
    gaussian-=float(np.sum(physical_weight*gaussian)/np.sum(physical_weight))
    n_unstructured_constant=p.reference_density*np.sum(w)/np.sum(physical_weight)
    arbitrary_n=n_unstructured_constant+p.gaussian_perturbation*gaussian
    if np.min(arbitrary_n)<=0:raise ArithmeticError('Gaussian control density nonpositive')
    jgauss=current_from_lambda(A,p.alpha*(trace(arbitrary_n,p.rest_mass,p.compressibility)-trace0),m.h)
    gauss_mu=(p.rest_mass+p.compressibility*arbitrary_n)*np.exp(sigma)
    # Principal frozen Y-sector: a magnetic plane-wave perturbation can align
    # B_Y with E_X while its wavevector is perpendicular to E_X.
    beta_scans={}
    for beta in (0.,20.,40.,60.,80.):
        chi,margin,alpha2,beta1=principal_coefficients(
            K,U,E2,p.reference_density,p.rest_mass,p.compressibility,p.alpha,beta)
        i,j=np.unravel_index(np.argmin(margin),sh)
        beta_scans[str(int(beta))]={
            'minimum_frozen_magnetic_margin':float(np.min(margin)),
            'negative_cells':int(np.count_nonzero(margin<-1e-9)),
            'total_cells':int(margin.size),
            'minimum_at_rz_indices':[int(i),int(j)],
            'maximum_electric_field_squared':float(np.max(E2)),
            'kinetic_Y_electric_frozen':1.0,
            'full_coupled_health':'NOT_CERTIFIED',
        }
    # beta_crit local with exact fixed-background P=0 χ(β); only if positive slope.
    chi40,margin40,alpha2,beta1=principal_coefficients(
        K,U,E2,p.reference_density,p.rest_mass,p.compressibility,p.alpha,p.beta)
    positive=beta1*E2>1e-13
    critical=np.min((1-alpha2[positive]*E2[positive])/(beta1[positive]*E2[positive]))
    imin,jmin=np.unravel_index(np.argmin(margin40),sh)
    E=float(np.sqrt(E2[imin,jmin]));stiff=-1+chi40[imin,jmin]*E*E
    fd=finite_difference_principal(K[imin,jmin],U[imin,jmin],p.reference_density,
                                   E,p.alpha,p.beta,p.rest_mass,p.compressibility)
    cs2=p.compressibility*n/(p.rest_mass+p.compressibility*n)
    # A single P10 regularized axisymmetric source is not a real 3D Earth solution.
    return {
      'source':{'nr':p.nr,'L':p.L,'h_canonical':m.h,
          'canonical_source_energy_NOT_J':float(info['canonical_energy_NOT_J']),
          'Noether':list(map(float,info['individual_Noether'])),
          'net_X_charge':float(info['net_X_charge']),
          'base_P10_EOM_max':float(max(info['scalar_equation_weighted_L2'])),
          'base_free_X_Gauss_residual':float(info['free_coulomb_residual_inf']),
          'Y_approximation':'SOURCE_ONLY_FIRST_ORDER_NO_BETA_OR_NEUTRAL_Y_BACKREACTION'},
      'neutral_hydrostatic_ONE_WAY':{
          'rest_mass':p.rest_mass,'kappa':p.compressibility,
          'reference_density':p.reference_density,
          'integrated_number_reference':float(p.reference_density*np.sum(w)),
          'integrated_number_actual':float(np.sum(w*np.exp(3*sigma)*n)),
          'number_preservation_abs_error':float(abs(np.sum(w*np.exp(3*sigma)*n)-p.reference_density*np.sum(w))),
          'positive_min_density':float(np.min(n)),
          'max_density_readjustment':float(np.max(abs(n-p.reference_density))),
          'redshifted_mu_const':float(C),
          'redshifted_mu_max_residual':float(chem_res),
          'static_Euler_finite_difference_inf':float(euler_res),
          'minimum_sound_speed_squared':float(np.min(cs2)),
          'maximum_sound_speed_squared':float(np.max(cs2)),
          'minimum_density_energy':float(np.min(rho)),
          'minimum_energy_minus_abs_pressure':float(np.min(rho-abs(press))),
          'portal_sigma_max':float(np.max(abs(sigma))),
          'density_response_Y_current_L2':norm(jhyd),
          'arbitrary_same_number_gaussian_Y_current_L2':norm(jgauss),
          'ratio_hydro_over_arbitrary':float(norm(jhyd)/norm(jgauss)),
          'gaussian_number_error':float(abs(np.sum(w*np.exp(3*sigma)*arbitrary_n)-p.reference_density*np.sum(w))),
          'arbitrary_Gaussian_redshifted_mu_range':float(np.ptp(gauss_mu)),
          'constant_fluid_trace_Y_driving_current_L2':norm(current_from_lambda(A,p.alpha*np.full(sh,trace0),m.h)),
          'constant_fluid_trace_changes_Y_stiffness':True,
          'status':'ONE_WAY_HYDROSTATIC_FLUID_NOT_EARTH_OR_COUPLED_SOURCE'},
      'principal_Y_frozen_background':{
          'scans':beta_scans,
          'beta_first_local_zero_stiffness':float(critical),
          'beta40_local_second_B_derivative_FD':float(fd),
          'beta40_local_second_B_derivative_exact':float(stiff),
          'beta40_FD_difference_abs':float(abs(fd-stiff)),
          'pointwise_negative_mode_trial':'local short-wavelength divergence-free BY parallel EX, k perpendicular EX, not full PDE eigenmode',
          'complete_X_Y_fluid_solid_kinetic_matrix':'NOT_SOLVED',
          'continuum_and_UV_validity':'NOT_CERTIFIED'},
      'missing':{
          'full_X_Y_source_EOM':'NOT_SOLVED',
          'Einstein_EOM':'NOT_SOLVED',
          'material_support_boundaries':'NOT_SOLVED',
          'onboard_whole_craft':'NOT_DERIVED',
          'physical_Earth_down_craft_up':'NOT_DERIVED',
          'neutral_torus_1kg_1g_1m':'NOT_CERTIFIED',
          'complete_SI_energy_lt10MJ':'NOT_CERTIFIED',
      },
    }


def report():
    symbolic=exact_atlas()
    cases={f'{nr}_L{L}':numerical_case(Parameters(nr=nr,L=float(L)))
           for nr,L in ((12,12),(18,12),(12,16))}
    sources=[c['source'] for c in cases.values()]
    fluids=[c['neutral_hydrostatic_ONE_WAY'] for c in cases.values()]
    healthy=[c['principal_Y_frozen_background'] for c in cases.values()]
    gates={
       'symbolic_all_exact':all(symbolic['checks'].values()),
       'real_P10_3_reconstructions':len(cases)==3,
       'source_P10_charge_neutral':all(abs(s['net_X_charge'])<1e-8 for s in sources),
       'source_fixed_noether_each_species':all(max(abs(x-400) for x in s['Noether'])<1e-5 for s in sources),
       'source_base_EOM_converged':all(s['base_P10_EOM_max']<5e-5 for s in sources),
       'source_base_X_gauss_converged':all(s['base_free_X_Gauss_residual']<1e-9 for s in sources),
       'fluid_density_positive':all(f['positive_min_density']>0 for f in fluids),
       'fluid_number_preservation':all(f['number_preservation_abs_error']<1e-8 for f in fluids),
       'fluid_hydrostatic_mu_first_integral':all(f['redshifted_mu_max_residual']<1e-11 for f in fluids),
       'fluid_hydrostatic_Euler_local':all(f['static_Euler_finite_difference_inf']<1e-8 for f in fluids),
       'fluid_WEC_positive':all(f['minimum_density_energy']>0 for f in fluids),
       'fluid_DEC_positive':all(f['minimum_energy_minus_abs_pressure']>0 for f in fluids),
       'fluid_sound_speed_sub_luminal':all(0<f['minimum_sound_speed_squared']<=f['maximum_sound_speed_squared']<1 for f in fluids),
       'fluid_sigma_weak_oneway':all(f['portal_sigma_max']<1e-3 for f in fluids),
       'fluid_density_readjusts':all(f['max_density_readjustment']>1e-7 for f in fluids),
       'hydrostatic_density_induction_nonzero':all(f['density_response_Y_current_L2']>1e-9 for f in fluids),
       'arbitrary_Gaussian_same_number':all(f['gaussian_number_error']<1e-8 for f in fluids),
       'arbitrary_Gaussian_is_not_hydrostatic':all(f['arbitrary_Gaussian_redshifted_mu_range']>1e-3 for f in fluids),
       'hydrostatic_source_smaller_than_imposed_profile':all(f['ratio_hydro_over_arbitrary']<.01 for f in fluids),
       'constant_trace_no_local_Y_drive':all(f['constant_fluid_trace_Y_driving_current_L2']<1e-11 for f in fluids),
       'constant_trace_still_modifies_Y_stiffness':all(f['constant_fluid_trace_changes_Y_stiffness'] for f in fluids),
       'beta0_frozen_magnetic_positive':all(h['scans']['0']['minimum_frozen_magnetic_margin']>0 for h in healthy),
       'beta40_frozen_magnetic_positive':all(h['scans']['40']['minimum_frozen_magnetic_margin']>0 for h in healthy),
       'beta60_frozen_magnetic_negative':all(h['scans']['60']['minimum_frozen_magnetic_margin']<0 for h in healthy),
       'beta80_frozen_magnetic_negative':all(h['scans']['80']['minimum_frozen_magnetic_margin']<0 for h in healthy),
       'critical_beta_between_40_and60':all(40<h['beta_first_local_zero_stiffness']<60 for h in healthy),
       'beta40_second_variation_independent_FD':all(h['beta40_FD_difference_abs']<3e-5 for h in healthy),
       'some_negative_cells_at_beta60':all(h['scans']['60']['negative_cells']>0 for h in healthy),
       'Y_electric_frozen_kinetic_positive':all(h['scans']['40']['kinetic_Y_electric_frozen']==1 for h in healthy),
       'full_coupled_modes_not_claimed_healthy':all(h['complete_X_Y_fluid_solid_kinetic_matrix']=='NOT_SOLVED' for h in healthy),
       'fluid_not_claimed_real_Earth':all(f['status'].startswith('ONE_WAY_') for f in fluids),
       'missing_source_recognition':all(c['missing']['full_X_Y_source_EOM']=='NOT_SOLVED' for c in cases.values()),
       'missing_Einstein_recognition':all(c['missing']['Einstein_EOM']=='NOT_SOLVED' for c in cases.values()),
       'missing_support_boundaries':all(c['missing']['material_support_boundaries']=='NOT_SOLVED' for c in cases.values()),
       'missing_full_craft_reaction':all(c['missing']['physical_Earth_down_craft_up']=='NOT_DERIVED' for c in cases.values()),
       'missing_SI_and_complete_energy':all(c['missing']['complete_SI_energy_lt10MJ']=='NOT_CERTIFIED' for c in cases.values()),
    }
    gates={k:bool(v) for k,v in gates.items()}
    return {'symbolic':symbolic,'cases':cases,'gates':gates,
       'verdict':'YELLOW_PH16_01_COVARIANT_FLUID_EQUILIBRIUM_AND_FROZEN_PRINCIPAL_OBSTRUCTION_FULL_RECIPROCITY_OPEN',
       'classification':'COVARIANT_FLUID_AND_SOLID_ACTION_IDENTITIES_ONE_WAY_HYDROSTATIC_PLUS_FROZEN_PRINCIPAL_TEST',
       'physical_transfer':'SCOPED_FLUID_IDENTITY_AND_NECESSARY_PRINCIPAL_HEALTH_ONLY',
       'limits':[
           'Covariant pullback perfect-fluid and elastic solid actions are explicitly defined, but Earth/solid dynamical equations and support boundaries are not solved.',
           'Hydrostatic density responds to a prescribed sigma computed from source-only PH15-P10 first-order Y; not jointly on-shell.',
           'Homogeneous neutral fluid gives zero bulk first-order Y *drive*, NOT zero beta-dependent constitutive stiffness or zero gravity.',
           'Frozen magnetic principal margin negative at beta60 and beta80 in this EFT; a full dynamical constrained X/Y/fluid/metric spectrum remains uncomputed.',
           'This diagnostic fluid occupies a finite numerical box with no physical Earth, surface tension or torus; its density number is canonical, not 1kg.',
           'No general 3D Einstein solution, no whole-craft Earth interaction, no SI matching, UV cutoff or strict 10MJ energy certificate.',
       ],
       'next':'PH16-02: coupled full-cell X/Y/source/fluid residual and complete constrained magnetic/kinetic/UV audit before any PH17 transfer',
    }
