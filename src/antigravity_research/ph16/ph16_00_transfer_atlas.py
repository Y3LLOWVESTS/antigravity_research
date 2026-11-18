"""PH16-00: one-action transfer preflight for PH15-P10 + universal neutral matter.

CANDIDATE (signature -+++):
  S = S_EH[g] - 1/4 int sqrt(-g)(F_X^2 + F_Y^2)
      + S_source[psi_i,A_X,exp(2*sigma)g]
      + S_neutral[chi,exp(2*sigma)g]
      + S_support[hull,exp(2*sigma)g],
  P=(1/4) epsilon^{mu nu rho sigma} F_Xmu_nu F_Yrho_sigma,
  sigma(P)=alpha*P-beta*P^2.

This is a candidate effective-action *specification*, not a solution.
With matter varied under the conformal metric, lambda=delta L_m/delta P
= exp(4sigma) T_tilde (alpha-2beta P) (on matter EOM where needed).
The coupled carrier equations require
  nabla_mu(F_X^{mu nu}-lambda tilde(F_Y)^{mu nu})=J_X^nu,
  nabla_mu(F_Y^{mu nu}-lambda tilde(F_X)^{mu nu})=0,
with source charges from covariant derivatives, not prescribed.

A neutral particle S_p=-m int exp(sigma)ds_g gives
  a_g^mu=-(g^{mu nu}+u^mu u^nu)grad_nu sigma,
when treated as a test body on fixed g. Full gravitational response also
requires varying and SOLVING the Einstein equation including metric dependence
of epsilon and all sources; it is NOT solved here.

NUMERIC TEST: PH15-P10 free-Coulomb scalar/X source reconstructed.
At alpha small, calculate first-order Y current including a *prescribed*
smooth neutral trace as a sensitivity/control, WITHOUT solving neutral Earth
or applying the source/X/Y reciprocal correction. All quantities canonical.

No full on-shell source-X-Y-matter-metric, no real Earth, no external craft
reaction, no 1kg >=1g at >=1m, no SI <10MJ. BETA-1 stays frozen.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
import sympy as sp
from antigravity_research.agminer.hook17_ph15_p10_free_space import CoulombSource, Spec


@dataclass(frozen=True)
class Control:
    nr: int = 12
    L: float = 12.
    alpha: float = .05
    beta: float = 40.
    prescribed_neutral_amplitude: float = .15


def exact_atlas():
    a,b,P,K,U,n,m = sp.symbols('alpha beta P K U n m', real=True)
    s=a*P-b*P**2
    ds=sp.diff(s,P)

    # The -n exp(sigma) term is a rest-frame *test particle density*
    # and is NOT substituted for a generally covariant dust field action.
    Ls=-sp.exp(2*s)*K-sp.exp(4*s)*U
    Ln=-n*sp.exp(s)
    ls=sp.diff(Ls,P)
    ln=sp.diff(Ln,P)
    lt=ls+ln
    exp_l0=-a*(2*K+4*U+n)
    h=sp.symbols('h',real=True)
    small_beta=sp.diff(lt,P).subs(P,0)

    theta=sp.symbols('theta',real=True)
    P0=sp.symbols('P0',real=True)
    Pconformal=P0*sp.exp(-4*theta)
    Pdensity=sp.exp(4*theta)*Pconformal

    # One-dimensional conformal geodesic check at zero velocity.
    x=sp.symbols('x',real=True)
    sig=sp.Function('sigma')(x)
    accel=sp.simplify(-sp.diff(m*sp.exp(sig),x)/(m*sp.exp(sig)))

    # Independent Maxwell mixed-constitutive Hessian of same local L.
    EE,BB=sp.symbols('EE BB',real=True)
    Pi=EE*BB
    LL=sp.Rational(1,2)*(EE**2-BB**2)+(
        -sp.exp(2*(a*Pi-b*Pi**2))*K
        -sp.exp(4*(a*Pi-b*Pi**2))*U
        -n*sp.exp(a*Pi-b*Pi**2)
    )
    mixed1=sp.diff(sp.diff(LL,EE),BB)
    mixed2=sp.diff(sp.diff(LL,BB),EE)

    checks={
        'sigma_prime':sp.simplify(ds-(a-2*b*P))==0,
        'source_lambda_chain':sp.simplify(
            ls+(2*sp.exp(2*s)*K+4*sp.exp(4*s)*U)*ds
        )==0,
        'neutral_particle_lambda_chain':sp.simplify(
            ln+n*sp.exp(s)*ds
        )==0,
        'total_lambda_is_sum':sp.simplify(lt-ls-ln)==0,
        'lambda_at_P0_with_neutral':sp.simplify(
            lt.subs(P,0)-exp_l0
        )==0,
        'no_portal_alpha0_first_order':sp.simplify(
            lt.subs({P:0,a:0})
        )==0,
        'beta_changes_local_linear_Y_stiffness':sp.simplify(
            sp.diff(small_beta,b)-(4*K+8*U+2*n)
        )==0,
        'neutral_trace_changes_Y_drive_at_alpha':sp.simplify(
            sp.diff(lt.subs(P,0),n)+a
        )==0,
        'positive_rest_mass_conformal_particle':sp.simplify(
            -sp.diff(-m*sp.exp(s),P)-m*sp.exp(s)*ds
        )==0,
        'test_particle_conformal_accel':sp.simplify(
            accel+sp.diff(sig,x)
        )==0,
        'mixed_variation_reciprocal':sp.simplify(
            mixed1-mixed2
        )==0,
        'mixed_lambda_at_FY0':sp.simplify(
            mixed1.subs(BB,0)-exp_l0
        )==0,
        'Y0_induction_if_no_matter':sp.simplify(
            mixed1.subs({BB:0,K:0,U:0,n:0})
        )==0,
        'Y0_induction_if_alpha0':sp.simplify(
            mixed1.subs({BB:0,a:0})
        )==0,
        'P_is_even_under_simultaneous_F_reversal':sp.simplify(
            ((-EE)*(-BB))-Pi
        )==0,
        'P_is_odd_under_single_F_reversal':sp.simplify(
            ((-EE)*BB)+Pi
        )==0,
        'neutral_test_mass_must_not_be_negative':sp.simplify(
            sp.diff(-m*sp.exp(s),m)+sp.exp(s)
        )==0,
        'conformal_Weyl_trace_source':sp.simplify(
            sp.diff(-sp.exp(2*h)*K-sp.exp(4*h)*U,h).subs(h,0)
            +2*K+4*U
        )==0,
        'LeviCivita_P_is_metric_density_sensitive':sp.simplify(
            sp.diff(Pconformal,theta).subs(theta,0)+4*P0
        )==0,
        'Pontryagin_density_metric_independent':sp.simplify(
            sp.diff(Pdensity,theta)
        )==0,
    }

    if not all(checks.values()):
        raise AssertionError(
            'Exact single-action identity failed: '
            +str({k:v for k,v in checks.items() if not v})
        )

    return {
       'checks':{k:bool(v) for k,v in checks.items()},
       'lambda_source':str(ls),
       'lambda_neutral_rest_particle':str(ln),
       'lambda_total_at_P0':str(lt.subs(P,0)),
       'lambda_P_at_P0':str(small_beta),
       'neutral_test_acceleration_fixed_g':
           'a^mu=-(g^mu_nu+u^mu u_nu)grad^nu sigma; '
           'gravity metric perturbation NOT included',
       'metric_P_variation':
           'P=(epsilon density contraction)/(4 sqrt(-g)): '
           'delta P=(P/2)g_mu_nu delta g^mu_nu '
           '(holding FX,FY fixed)',
       'gauge_constitutive':
           'H_X=F_X-lambda*dual(F_Y); '
           'H_Y=F_Y-lambda*dual(F_X)',
       'Bianchi':
           'dF_X=dF_Y=0; '
           'nabla_mu dual(F_X)^mu_nu='
           'nabla_mu dual(F_Y)^mu_nu=0',
       'local_weyl_trace':
           'delta S_m / delta sigma = sqrt(-g_tilde) '
           'T_tilde; lambda_total=e^(4sigma) '
           'T_tilde sigma_prime',
       'total_stress_Ward':
           'total stress conservation is an on-shell '
           'obligation; NOT evaluated numerically',
       'diffeomorphism_and_Einstein':
           'FULL_VARIATION_AND_SOLVE_NOT_PERFORMED',
       'neutral_Earth_material':
           'PRESCRIBED_TRACE_SENSITIVITY_ONLY_NOT_COVARIANT_DUST_SOLVE',
    }


def dR(f,h):
    return np.gradient(f,h,axis=0,edge_order=2)


def dZ(f,h):
    return np.gradient(f,h,axis=1,edge_order=2)


def current_from_lambda(A,lam,h):
    """PH15-P1 cylindrical sign: j_phi=lambda_r A_z-lambda_z A_r."""
    return dR(lam,h)*dZ(A,h)-dZ(lam,h)*dR(A,h)


def neutral_trace_profile(m: CoulombSource, amplitude:float):
    r=m.rho.reshape(m.nr,m.nz)
    z=m.z.reshape(m.nr,m.nz)

    # Deliberately PRESCRIBED positive density; NOT physical Earth.
    return amplitude*np.exp(
        -((r-3.)/2.3)**2-((z+2.5)/3.2)**2
    )


def source_traces(m,fields):
    sh=(m.nr,m.nz)
    F=fields['F'].reshape(2,*sh)
    W=fields['W'].reshape(2,*sh)

    K=sum(
        dR(F[i],m.h)**2
        +dZ(F[i],m.h)**2
        -(W[i]*F[i])**2
        for i in range(2)
    )

    ss=F*F
    U=(
        np.sum(ss-2*ss**2+2*ss**3,axis=0)
        +m.s.g*ss[0]*ss[1]
    )

    return K,U


def numerical_case(c:Control):
    m=CoulombSource(Spec(nr=c.nr,L=c.L),self_order=8)
    info,fields=m.solve(350)

    if (
        max(info['scalar_equation_weighted_L2'])>5e-5
        or abs(info['net_X_charge'])>1e-8
    ):
       raise RuntimeError(
           'Protected P10 baseline source EOM or neutrality failed'
       )

    sh=(m.nr,m.nz)
    A=fields['A'].reshape(sh)
    K,U=source_traces(m,fields)

    lam_source=-2*c.alpha*(K+2*U)
    density=neutral_trace_profile(
        m,c.prescribed_neutral_amplitude
    )

    # Rest-frame particle lambda_n(P=0)=-alpha*rho_n.
    # This is NOT a physical on-shell Earth matter solution.
    lam_total=lam_source-c.alpha*density

    j0=current_from_lambda(A,lam_source,m.h)
    j=current_from_lambda(A,lam_total,m.h)
    jr=j-j0
    w=m.w.reshape(sh)

    norm=lambda a:float(np.sqrt(np.sum(w*a*a)))

    uniform_density=np.full_like(density,0.23)
    j_const=current_from_lambda(
        A,lam_source-c.alpha*uniform_density,m.h
    )
    j_aligned=current_from_lambda(
        A,lam_source-c.alpha*.24*A,m.h
    )
    j_off=current_from_lambda(
        np.zeros_like(A),lam_total,m.h
    )
    j_minus=current_from_lambda(A,-lam_total,m.h)
    j_double=current_from_lambda(
        A,lam_source-2*c.alpha*density,m.h
    )

    # First-order P10 kernel, WITHOUT Y backreaction.
    v0=(m.wmagkernel@j0.ravel()).reshape(sh)
    v=(m.wmagkernel@j.ravel()).reshape(sh)

    br=-dZ(v,m.h)
    bz=dR(v,m.h)+v/m.rho.reshape(sh)

    er=-dR(A,m.h)
    ez=-dZ(A,m.h)

    div_b=dR(br,m.h)+br/m.rho.reshape(sh)+dZ(bz,m.h)
    curl_e=dR(ez,m.h)-dZ(er,m.h)

    portal=er*br+ez*bz
    sigma=c.alpha*portal-c.beta*portal**2
    gz=-dZ(sigma,m.h)

    # gz is a fixed-background conformal test-body
    # acceleration diagnostic, NOT SI or whole-craft force.

    original_y=m.induced_Y_free_space(
        fields,alpha=c.alpha
    )

    return {
        'source':{
            'nr':c.nr,
            'L':c.L,
            'h':m.h,
            'P10_energy_canonical_not_J':
                info['canonical_energy_NOT_J'],
            'scalar_EOM_weighted_L2':
                info['scalar_equation_weighted_L2'],
            'free_X_Gauss_residual':
                info['free_coulomb_residual_inf'],
            'Noether':info['individual_Noether'],
            'net_X_charge':info['net_X_charge'],
            'first_order_existing_Y':original_y,
        },
        'prescribed_neutral_diagnostic':{
            'amplitude_arbitrary_canonical':
                c.prescribed_neutral_amplitude,
            'trace_density_integral_arbitrary':
                float(np.sum(w*density)),
            'source_Y_current_weighted_L2':norm(j0),
            'with_prescribed_neutral_Y_current_weighted_L2':
                norm(j),
            'neutral_increment_Y_current_weighted_L2':
                norm(jr),
            'neutral_increment_relative_to_source':
                norm(jr)/norm(j0),
            'neutral_increment_Biot_Savart_energy_canonical_not_J':
                float(.5*np.sum(w*jr*(v-v0))),
            'constant_neutral_trace_null_error':
                norm(j_const-j0),
            'A0_aligned_trace_null_error':
                norm(j_aligned-j0),
            'source_off_A0_zero_current':
                norm(j_off),
            'alpha_sign_reversal_error':
                norm(j+j_minus),
            'density_amplitude_double_error':
                norm((j_double-j0)-2*jr),
            'PH15_P10_first_order_current_reproduction_error':
                float(abs(norm(j0)-original_y['Y_current_L2'])),
            'Y_magnetic_Bianchi_inf':
                float(np.max(abs(div_b))),
            'X_electrostatic_Bianchi_inf':
                float(np.max(abs(curl_e))),
            'first_order_P_abs_integral_canonical':
                float(np.sum(w*abs(portal))),
            'prescribed_sigma_max_abs':
                float(np.max(abs(sigma))),
            'fixed_g_test_accel_z_max_abs_CANONICAL_NOT_SI':
                float(np.max(abs(gz))),
            'physical_Earth_density_EOM':'NOT_SOLVED',
            'physical_metric_Einstein_EOM':'NOT_SOLVED',
            'source_X_Y_reciprocal_EOM':'NOT_SOLVED',
            'physical_force_and_1kg_benchmark':'NOT_DERIVED',
        },
    }


def report():
    exact=exact_atlas()

    cfgs=(
        Control(nr=12,L=12),
        Control(nr=18,L=12),
        Control(nr=12,L=16),
    )

    cases={
        f'{c.nr}_L{int(c.L)}':numerical_case(c)
        for c in cfgs
    }

    s=[
        v['prescribed_neutral_diagnostic']
        for v in cases.values()
    ]
    p=[
        v['source']
        for v in cases.values()
    ]

    gates={
        'exact_20_action_relations':
            all(exact['checks'].values()),

        'P10_neutral_X_source_in_all_cases':
            all(abs(v['net_X_charge'])<1e-8 for v in p),

        'P10_individual_Noether_conserved':
            all(
                max(abs(q-400) for q in v['Noether'])<1e-5
                for v in p
            ),

        'P10_scalar_EOM_small':
            all(
                max(v['scalar_EOM_weighted_L2'])<5e-5
                for v in p
            ),

        'P10_X_Gauss_small':
            all(
                v['free_X_Gauss_residual']<1e-9
                for v in p
            ),

        'actual_P10_Y_first_order_nonzero':
            all(
                v['first_order_existing_Y']['Y_current_L2']>1e-6
                for v in p
            ),

        'P10_first_order_Y_current_exact_reproduction':
            all(
                v['PH15_P10_first_order_current_reproduction_error']<1e-11
                for v in s
            ),

        'static_Y_magnetic_Bianchi':
            all(v['Y_magnetic_Bianchi_inf']<1e-11 for v in s),

        'static_X_electrostatic_Bianchi':
            all(v['X_electrostatic_Bianchi_inf']<1e-11 for v in s),

        'neutral_load_changes_first_order_Y_current':
            all(
                v['neutral_increment_Y_current_weighted_L2']>1e-5
                for v in s
            ),

        'not_near_zero_relative_neutral_effect':
            all(
                v['neutral_increment_relative_to_source']>1e-3
                for v in s
            ),

        'neutral_variable_trace_distinguishable':
            all(
                abs(
                    v['with_prescribed_neutral_Y_current_weighted_L2']
                    -v['source_Y_current_weighted_L2']
                )>1e-6
                for v in s
            ),

        'constant_trace_bulk_null':
            all(
                v['constant_neutral_trace_null_error']<1e-11
                for v in s
            ),

        'aligned_trace_integrability_null':
            all(
                v['A0_aligned_trace_null_error']<1e-11
                for v in s
            ),

        'no_X_no_induced_Y':
            all(v['source_off_A0_zero_current']==0 for v in s),

        'reversal_alpha_antisymmetry':
            all(
                v['alpha_sign_reversal_error']<1e-11
                for v in s
            ),

        'linear_neutral_amplitude_at_fixed_background':
            all(
                v['density_amplitude_double_error']<1e-11
                for v in s
            ),

        'positive_first_order_Y_kernel_increment_energy':
            all(
                v['neutral_increment_Biot_Savart_energy_canonical_not_J']>0
                for v in s
            ),

        'conformal_particle_effect_not_claimed_SI':
            all(
                v['fixed_g_test_accel_z_max_abs_CANONICAL_NOT_SI']>0
                for v in s
            ),

        'positive_sensitivity_P_abs':
            all(
                v['first_order_P_abs_integral_canonical']>0
                for v in s
            ),

        'portal_sigma_reduced_small':
            all(
                v['prescribed_sigma_max_abs']<1
                for v in s
            ),

        'finite_source_energy_canonical':
            all(
                np.isfinite(v['P10_energy_canonical_not_J'])
                for v in p
            ),

        'mesh_energy_not_converged_certified':
            abs(
                p[0]['P10_energy_canonical_not_J']
                -p[1]['P10_energy_canonical_not_J']
            )>1e-3,

        'source_only_Y_not_universal_loaded':
            all(
                v['physical_Earth_density_EOM']=='NOT_SOLVED'
                for v in s
            ),

        'Einstein_metric_not_derived':
            all(
                v['physical_metric_Einstein_EOM']=='NOT_SOLVED'
                for v in s
            ),

        'full_reciprocal_EOM_not_derived':
            all(
                v['source_X_Y_reciprocal_EOM']=='NOT_SOLVED'
                for v in s
            ),

        'no_neutral_payload_force_claim':
            all(
                v['physical_force_and_1kg_benchmark']=='NOT_DERIVED'
                for v in s
            ),
    }

    gates={key:bool(value) for key,value in gates.items()}

    return {
        'action':{
            'candidate':
                'EH[g]+Maxwell_X+Maxwell_Y'
                '+S_source[psi,AX,g_tilde]'
                '+S_neutral[chi,g_tilde]'
                '+S_support[g_tilde]',
            'g_tilde':'exp(2sigma(P))*g',
            'sigma':'alpha P-beta P^2',
            'P':'epsilon FX FY / 4 with metric Levi-Civita tensor',
            'not_yet_one_physical_solution':True,
            'no_real_material_or_Einstein_equations_solved':True,
        },
        'exact':exact,
        'cases':cases,
        'gates':gates,
        'transfer_classification':
            'REQUIREMENTS_TRANSFER_ONLY_NOT_PHYSICAL_MECHANISM',
        'verdict':
            'YELLOW_PH16_00_UNIVERSAL_TRACE_LOADING_PREFLIGHT_PH15_SOURCE_ONLY_Y_INCOMPLETE',
        'exterior_metric_status':'NOT_SOLVED',
        'coupled_X_Y_source_status':'NOT_SOLVED',
        'physical_neutral_Earth_and_hull':'NOT_SOLVED',
        'complete_healthy_modes':'NOT_SOLVED',
        'physical_Earth_down_craft_up':'NOT_DERIVED',
        'physical_units_and_UV':'NOT_CERTIFIED',
        'recommendation':
            'PH16-01: one-action universal neutral fluid/support '
            'and both U1 variations with fixed-charge reciprocal '
            'PDE residual and principal kinetic symbol before any '
            'Earth-force claim',
        'limits':[
            'P10 discrete self-consistent electrostatics, '
            'first-order Y, not coupled X/Y',
            'Prescribed positive neutral trace is a sensitivity '
            'toy, NOT sourced Earth material',
            'The covariant neutral matter and hull/support '
            'action are declared but not implemented/varied '
            'in dynamical geometry',
            'Conformal test-particle acceleration is in '
            'canonical fixed-g background, NOT antigravity force',
            'Fully dynamical GR Einstein equations and stress '
            'Ward are formal obligations, not executed solutions',
            'No full-modes hyperbolicity, nonaxisymmetric '
            'spectrum, ghost/gradient/UV or SI scaling',
            'No 1kg neutral torus 1g at 1m, no Earth-down '
            'craft-up and no 10MJ certification',
        ],
    }
