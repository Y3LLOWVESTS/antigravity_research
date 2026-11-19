"""GAMMA1-00R10 restricted charged-source Lorentzian completion preflight.

Exact model: original PH16-04R2 stationary Routhian on immutable R3 data.
Hypothesis: minimally coupled charged complex scalars and isentropic fluid in
universal conformal metric, plus two Lorentzian U(1) Maxwell fields.
Only a STATIC REDUCTION and frozen-background instantaneous carrier blocks
are tested. NOT a full action reduction, constrained mode certificate,
Einstein solution, or Earth/support/whole-craft response.
"""
from __future__ import annotations
import hashlib
from pathlib import Path
import numpy as np
import sympy as sp

PH16_SHA='b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
R3_SHA='94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
R5_SHA='2b9217ef9b36758ef675eeb47796198adf1be2ff6b5764b316a2e312bc82c883'
R9_RESULT_SHA='eec38658fccbc6f7f7f5de392aa76d08052f2be91937c8e06da553d224b43a9a'
R9_VERIFY_SHA='7d56fca3931369ea68dc2e973f4e8b8ebbce72a8dd5d85e50532374d6cc2811a'
R9_ARCHIVE_SHA='5fb9a4966074e749cf697b50421cc7047c28cbae35a80f0d77942aac8721f8bd'


def sha(path):
    p=Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else 'MISSING'


def exact_lorentzian_necessary_identities():
    """Exact restricted algebra; formal action hypotheses, not GR EOM proof."""
    w,a,q,omega,F,G,U,s,ds,nlabel,m,k=sp.symbols(
        'w A q omega F G U sigma dSigma nlabel mass kappa',real=True
    )
    W=omega-q*a
    # Signature (-,+,+,+), minimally coupled charged complex scalar.
    L=sp.exp(2*s)*F**2*W**2-sp.exp(2*s)*G-sp.exp(4*s)*U
    N=2*sp.exp(2*s)*F**2*W
    fixedN=sp.symbols('fixedN',real=True)
    R=omega*fixedN-L
    fluid=m*nlabel*sp.exp(s)+sp.Rational(1,2)*k*nlabel**2*sp.exp(-2*s)
    n=nlabel*sp.exp(-3*s)
    mu=sp.exp(s)*(m+k*n)

    ex,ey,bx,by,chi,ell=sp.symbols('ex ey bx by chi ell',real=True)
    P=ex*by+ey*bx
    L_e=sp.Rational(1,2)*(ex**2+ey**2)+ell*P+chi*P**2/2
    H_b=sp.Rational(1,2)*(bx**2+by**2)-ell*P-chi*P**2/2
    HE=sp.hessian(L_e,(ex,ey))
    HB=sp.hessian(H_b,(by,bx))
    b_sq=by**2+bx**2
    e_sq=ex**2+ey**2

    z,p,alpha,beta,Ts=sp.symbols(
        'z p alpha beta Ttilde',real=True
    )
    sig=alpha*p-beta*p**2
    T_E=sp.exp(4*sig)*Ts*(1-4*(alpha-2*beta*p)*p)
    traces=sp.exp(4*sig)*Ts-4*sp.exp(4*sig)*Ts*(alpha-2*beta*p)*p

    checks={
       'Noether_time_derivative':
           sp.simplify(sp.diff(L,omega)-N)==0,

       'Routhian_fixed_charge_stationarity':
           sp.simplify(sp.diff(R,omega).subs(fixedN,N))==0,

       'time_gauge_shift_scalar_L':
           sp.simplify(
               L.subs({omega:omega+q*ds,a:a+ds},simultaneous=True)-L
           )==0,

       'fluid_energy_label_reduction':
           sp.simplify(fluid-sp.exp(4*s)*(m*n+k*n**2/2))==0,

       'fluid_redshifted_chemical_potential':
           sp.simplify(sp.diff(fluid,nlabel)-mu)==0,

       'electric_rank_one_Hessian':
           sp.simplify(
               HE-sp.eye(2)-chi*sp.Matrix([by,bx])*sp.Matrix([[by,bx]])
           )==sp.zeros(2),

       'electric_Hessian_determinant':
           sp.simplify(HE.det()-(1+chi*b_sq))==0,

       'magnetic_rank_one_Hessian':
           sp.simplify(
               HB-sp.eye(2)+chi*sp.Matrix([ex,ey])*sp.Matrix([[ex,ey]])
           )==sp.zeros(2),

       'magnetic_Hessian_determinant':
           sp.simplify(HB.det()-(1-chi*e_sq))==0,

       'constant_portal_does_not_change_quadratic_blocks':
           sp.simplify(
               sp.diff(HE[0,0],ell)+sp.diff(HB[0,0],ell)
           )==0,

       'Hodge_Weyl_weight_minus_four':
           sp.simplify(
               sp.diff(p*sp.exp(-4*z),z).subs(z,0)+4*p
           )==0,

       'metric_trace_portal_algebra':
           sp.simplify(T_E-traces)==0,

       'portal_coupling_off_zero':
           sp.simplify(
               (alpha-2*beta*p).subs({alpha:0,beta:0})
           )==0,
    }

    if not all(checks.values()):
        raise AssertionError(checks)
    return {name:bool(value) for name,value in checks.items()}


def reconstruct_background(native,r5,beta=40.):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource,Spec,JointAction,Settings
    )

    m=CoulombSource(Spec(nr=12,L=12.),self_order=8)
    j=JointAction(m,Settings(nr=12,L=12.))

    F=np.stack([native['F_plus'],native['F_minus']])
    A=native['A_X']
    Y=native['A_Y']
    x=j.pack(F,A,Y)

    if abs(beta-40.)<1e-12:
        R,grad,d=j.evaluate(x,True)
        if abs(R-2401.472107471401)>1e-7 or np.linalg.norm(grad)>=1e-6:
            raise RuntimeError('ORIGINAL_ACTION_NOT_REPRODUCED')
        if np.max(abs(grad-native['joint_gradient']))>1e-10:
            raise RuntimeError('ORIGINAL_GRADIENT_NOT_REPRODUCED')

    w=j.w
    P=native['P']
    sig=.05*P-beta*P**2
    ds=.05-2*beta*P
    nlabel=native['neutral_n']*np.exp(3*native['sigma'])

    e2=np.exp(2*sig)
    f2=F**2
    I=f2@(w*e2)
    omega=(
        m.s.N/2
        +j.q*np.sum(f2*(w*e2*A)[None,:],axis=1)
    )/I

    W=omega[:,None]-j.q[:,None]*A[None,:]
    N=2*np.sum(f2*W*(w*e2)[None,:],axis=1)

    edge=F[:,j.edge_i]-F[:,j.edge_j]
    spatial=np.zeros(j.N)

    for i in range(2):
        t=.5*j.edge_c*edge[i]**2
        np.add.at(spatial,j.edge_i,t)
        np.add.at(spatial,j.edge_j,t)

    spatial+=j.boundary*np.sum(f2,axis=0)

    U=(
        np.sum(f2-2*f2**2+2*f2**3,axis=0)
        +m.s.g*f2[0]*f2[1]
    )

    Acoef=spatial-w*np.sum(f2*W*W,axis=0)
    Bcoef=w*U
    mm=j.s.mass*nlabel
    kk=j.s.kappa*nlabel*nlabel

    def rc(Pp):
        sp=.05*Pp-beta*Pp**2
        return (
            Acoef*np.exp(2*sp)
            +Bcoef*np.exp(4*sp)
            +w*(mm*np.exp(sp)+.5*kk*np.exp(-2*sp))
        )

    def derivatives(Pp):
        sp=.05*Pp-beta*Pp**2
        d=.05-2*beta*Pp
        e2p=np.exp(2*sp)
        e4p=e2p**2

        first=(
            2*Acoef*e2p
            +4*Bcoef*e4p
            +w*(mm*np.exp(sp)-kk*np.exp(-2*sp))
        )

        second=(
            4*Acoef*e2p
            +16*Bcoef*e4p
            +w*(mm*np.exp(sp)+2*kk*np.exp(-2*sp))
        )

        return (
            -first*d/w,
            (-second*d*d+2*beta*first)/w
        )

    lam,chi=derivatives(P)

    Er=-j.Dr@A
    Ez=-j.Dz@A
    Br=j.BR@Y
    Bz=j.BZ@Y

    E2=Er*Er+Ez*Ez
    B2=Br*Br+Bz*Bz

    if abs(beta-40.)<1e-12:
        if np.max(abs(lam-r5['lambda_Routhian']))>3e-12:
            raise RuntimeError('R5_MULTIPLIER_DRIFT')
        if np.max(abs(ds-r5['sigma_prime']))>3e-12:
            raise RuntimeError('R5_SIGMA_PRIME_DRIFT')
        if np.max(abs(P-(Er*Br+Ez*Bz)))>3e-12:
            raise RuntimeError('R3_HODGE_TRUNCATION_DRIFT')

    # Frozen background: NOT the full constrained principal symbol.
    electric=1+chi*B2
    magnetic=1-chi*E2

    return {
      'R':float(R) if beta==40. else None,
      'N':N,
      'omega':omega,
      'gauge_charge':float(j.q@N),
      'lambda':lam,
      'chi':chi,
      'electric':electric,
      'magnetic':magnetic,
      'E2':E2,
      'B2':B2,
      'ds':ds,
      'sigma':sig,
      'rc':rc,
      'derivatives':derivatives,
      'P':P,
      'fluid_redshifted_mu_spread':float(
          np.ptp(
              np.exp(sig)*(
                  j.s.mass+j.s.kappa*nlabel*np.exp(-3*sig)
              )
          )
      ),
    }


def numerical_evidence(native,r5):
    actual=reconstruct_background(native,r5,40.)
    stress=reconstruct_background(native,r5,60.)

    p=actual['P']
    step=3e-4
    rfun=actual['rc']

    finite_lam=-(
        rfun(p+step)-rfun(p-step)
    )/(2*step)/native['weights']

    finite_chi=-(
        rfun(p+step)-2*rfun(p)+rfun(p-step)
    )/(step**2)/native['weights']

    lam_err=float(np.max(abs(finite_lam-actual['lambda'])))
    chi_err=float(np.max(abs(finite_chi-actual['chi'])))

    if lam_err>1e-3 or chi_err>2e-2:
        raise RuntimeError(
            'INDEPENDENT_LOCAL_SECOND_VARIATION_MISMATCH: '
            +str((lam_err,chi_err))
        )

    if not (
        np.min(actual['electric'])>0
        and np.min(actual['magnetic'])>0
    ):
        raise RuntimeError('RESTRICTED_KINETIC_MARGIN_FAIL_BETA40')

    if np.sum(stress['magnetic']<0)!=4:
        raise RuntimeError('BETA60_FROZEN_WARNING_DRIFT')

    if not (
        np.max(abs(actual['N']-400))<1e-9
        and abs(actual['gauge_charge'])<1e-9
    ):
        raise RuntimeError('FIXED_NOETHER_OR_GAUGE_NEUTRALITY_FAILED')

    return {
      'beta40':{
        'charge_numbers':actual['N'].tolist(),
        'omega':actual['omega'].tolist(),
        'net_X_gauge_charge':actual['gauge_charge'],
        'lambda_range':[
            float(actual['lambda'].min()),
            float(actual['lambda'].max())
        ],
        'chi_range':[
            float(actual['chi'].min()),
            float(actual['chi'].max())
        ],
        'electric_rank_one_min':float(actual['electric'].min()),
        'magnetic_rank_one_min':float(actual['magnetic'].min()),
        'negative_electric_cells':int(np.sum(actual['electric']<0)),
        'negative_magnetic_cells':int(np.sum(actual['magnetic']<0)),
        'redshifted_fluid_mu_spread':
            actual['fluid_redshifted_mu_spread'],
        'lambda_finite_difference_max_abs':lam_err,
        'chi_finite_difference_max_abs':chi_err,
      },

      'beta60_OFFSHELL_FROZEN_PROFILE_CONTROL':{
        'negative_magnetic_cells':
            int(np.sum(stress['magnetic']<0)),
        'magnetic_rank_one_min':float(stress['magnetic'].min()),
        'electric_rank_one_min':float(stress['electric'].min()),
        'original_PH16_stationarity_beta60':'NOT_CLAIMED',
        'fixed_charge_frequency_recomputed':'YES',
        'neutral_material_label_frozen_from_beta40':'YES',
      },

      'single_monopole_SI_CONTROL_ONLY':{
        'G_m3_kg_s2':6.67430e-11,
        'c_m_s':299792458.,
        'equivalent_magnitude_mass_kg':9.80665/6.67430e-11,
        'rest_energy_J':
            (9.80665/6.67430e-11)*299792458.**2,
        'scope':'POINT_MONOPOLE_1M_ONLY_NOT_006D_OR_UNIVERSAL_NO_GO',
        'sign':
            'POSITIVE_MASS_ATTRACTIVE_NEGATIVE_MONOPOLE_REPULSIVE_UNDER_NEWTONIAN_ASSUMPTIONS',
      },

      'obstructions':{
        'Routhian_matter_static_ansatz':
            'CONDITIONAL_CHARGED_SCALARS_PLUS_ISENTROPIC_FLUID',
        'X_Y_spatial_quadratic':
            'FINITE_RING_GREEN_NOT_PROVEN_TO_EQUAL_LORENTZIAN_MAXWELL_REDUCTION',
        'full_offshell_fluid_current_Earth_hull_support':'UNSPECIFIED',
        'metric_P_Hodge_variation':
            'FORMAL_ALGEBRA_ONLY_NO_EINSTEIN_EOM',
        'full_constrained_Lorentzian_symbol':'NOT_COMPUTED',
        'actual_source_off_and_Earth_present':'NOT_SOLVED',
        'Earth_down_whole_craft_up':'NOT_DERIVED',
        'SI_normalization_for_portal':'UNKNOWN',
        'UV_empirical_consistency':'NOT_TESTED',
        'complete_energy_lt10MJ':'NOT_CERTIFIED',
      },
    }
