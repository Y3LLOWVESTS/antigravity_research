"""HOOK17-PH13-MEGA: coupled-source, portal and propulsion feasibility.

Strictly diagnostic: NO antigravity engine or physical lift established.
All numerical fields use arbitrary canonical natural units.
ALPHA-1 B17-M5V frozen. Conservative GR anchor 006D unreplaced.

PH12's radial gauged scalar is independently reconstructed. Its profile
is varied at FIXED Noether number with Gauss's law re-solved for each
perturbation. The finite-dimensional constrained energy Hessian tests
only sampled static radial directions, NOT dynamical spectral stability.

Full universal candidate:
    g_tilde = exp(2 sigma(P))*g
    sigma(P)=alpha*P-beta*P**2
    P=E_X dot B_Y + E_Y dot B_X

Matter:
    L_m=-exp(2sigma)*K-exp(4sigma)*U

K is the scalar covariant kinetic contraction in background g.
The carrier principal Hessian is rank-one at fixed matter velocities;
the full joint scalar-carrier Hessian requires an additional Schur test.

The universal matter-trace response lambda=dL_m/dP can induce a
secondary Y magnetic field through curl(lambda*E_X). We calculate
this in first-order perturbation theory for two separated,
charge-conjugated PH12 lumps.

CRITICAL: each isolated lump is on shell, but their two-center
superposition IS NOT. The periodic 3D induced-field calculation is
a mechanism probe, not an on-shell neutral composite, exterior gravity,
complete energy, or thrust.

Whole-craft momentum requires external Earth/environment coupling or
momentum flux. Internal impulses cancel in a closed system.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import json
import math

import numpy as np
import sympy as sp
from scipy.integrate import solve_bvp
from scipy.linalg import solve_banded

BRANCH = '032H17A12D1R3X3B17-PH13'

ARCHIVES = {
    'ph7_result': (
        'results/data/032h17_ph7_noether_spectral_health_20261115T023628445509Z.json',
        'da116371aab0da56e06ea0d6e5b3b7711df91be1339610df36988be79c645555'
    ),
    'ph12_module': (
        'src/antigravity_research/agminer/hook17_ph12_gauged_qball_source.py',
        '24afca0234910831c357f354db8eb6dcea08bba8814be5a21e091eb03e81b363'
    ),
    'ph12_result': (
        'results/data/032h17_ph12_gauged_qball_20261115T072909800847Z.json',
        '0f895a4c512d29d12617edbcf2ab8b3a87fd451427e24d9c59bf405fcf1d15ee'
    ),
    'ph11_module': (
        'src/antigravity_research/agminer/hook17_ph11_universal_metric_support_gate.py',
        '03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba'
    ),
    'm5v_module': (
        'src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py',
        'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'
    ),
}


@dataclass(frozen=True)
class Parameters:
    m: float = 1.
    b: float = 2.
    c: float = 2.
    e: float = .05
    f0: float = .7
    R: float = 40.
    collocation: int = 440
    finite_volume: int = 480
    tolerance: float = 1.e-9


def validate(p: Parameters):
    if p.collocation < 180 or p.finite_volume < 120:
        raise ValueError('Insufficient resolution')
    if not all(math.isfinite(v) for v in asdict(p).values()):
        raise ValueError('Nonfinite source parameter')
    if not (
        p.m > 0 and p.b > 0 and p.c > 0
        and p.e >= 0 and p.f0 > 0
        and p.R >= 25 and p.tolerance > 0
    ):
        raise ValueError('Invalid source parameters')
    if p.m*p.m <= p.b*p.b/(4*p.c):
        raise ValueError('Potential not positive in this gate')


def bvp(p: Parameters):
    """Independently reconstruct PH12 radial scalar-Maxwell equations."""
    validate(p)
    r = np.linspace(0, p.R, p.collocation)
    e, m, b, c = p.e, p.m, p.b, p.c

    def fun(x, y, pars):
        omega = pars[0]
        f, df, A, dA = y
        W = omega-e*A

        scalar_source = (
            (m*m-W*W)*f
            -2*b*f**3
            +3*c*f**5
        )
        maxwell_source = -2*e*W*f*f

        df_r = np.divide(
            df, x, out=np.zeros_like(df), where=x>0
        )
        dA_r = np.divide(
            dA, x, out=np.zeros_like(dA), where=x>0
        )

        return np.array([
            df,
            np.where(
                x>0,
                scalar_source-2*df_r,
                scalar_source/3
            ),
            dA,
            np.where(
                x>0,
                maxwell_source-2*dA_r,
                maxwell_source/3
            )
        ])

    def bc(origin, edge, pars):
        kappa = math.sqrt(
            max(1.e-12, p.m*p.m-pars[0]**2)
        )
        return [
            origin[0]-p.f0,
            origin[1],
            origin[3],
            edge[1]+(kappa+1/p.R)*edge[0],
            edge[3]+edge[2]/p.R
        ]

    f = p.f0*np.exp(-(r/3.)**2)
    A = .15*e*np.exp(-(r/8.)**2)

    initial = np.array([
        f,
        -2*r/9*f,
        A,
        -2*r/64*A
    ])

    solution = solve_bvp(
        fun, bc, r, initial,
        p=np.array([.92*p.m]),
        tol=p.tolerance,
        max_nodes=20000
    )

    if solution.status or not 0 < solution.p[0] < p.m:
        raise RuntimeError(
            'PH12 BVP reconstruction rejected: '
            + solution.message
        )

    return solution


def finite_volume_reduced_energy(
    f: np.ndarray,
    N: float,
    p: Parameters
):
    """Solve Gauss and energy at fixed Noether number in radial FV.

    Cell centers r_i=(i+1/2)dr, exact radial cell-volume weights.
    A0=omega*a, where
        (-Delta+2 e^2 f^2)a=2 e f^2

    Includes a Coulomb exterior condition. No trapping well.
    This is a reduced finite-volume energy, not a continuum proof.
    """
    f = np.asarray(f, dtype=float)
    n = p.finite_volume

    if (
        f.shape != (n,)
        or N <= 0
        or not np.all(np.isfinite(f))
    ):
        raise ValueError('Invalid amplitude or conserved number')

    if np.min(f) < -1.e-12:
        raise ValueError('Negative amplitude outside test scope')

    dr = p.R/n
    edges = np.arange(n+1)*dr
    centers = (np.arange(n)+.5)*dr

    volume = (
        edges[1:]**3-edges[:-1]**3
    )/3

    gradient_weights = edges[1:-1]**2/dr

    diagonal = np.zeros(n)
    diagonal[:-1] += gradient_weights
    diagonal[1:] += gradient_weights

    # Exterior Coulomb condition.
    diagonal[-1] += centers[-1]
    diagonal += 2*p.e*p.e*f*f*volume

    band = np.zeros((3,n))
    band[0,1:] = -gradient_weights
    band[1] = diagonal
    band[2,:-1] = -gradient_weights

    rhs = 2*p.e*f*f*volume

    a = solve_banded(
        (1,1), band, rhs,
        check_finite=True
    )

    check = diagonal*a
    check[:-1] -= gradient_weights*a[1:]
    check[1:] -= gradient_weights*a[:-1]

    gauss_residual = float(
        np.linalg.norm(check-rhs)/
        max(np.linalg.norm(rhs),1.e-20)
    )

    W_factor = 1-p.e*a

    if np.min(W_factor) <= 0:
        raise ValueError('Invalid effective frequency')

    norm = float(
        np.dot(volume,f*f*W_factor)
    )

    omega = N/(8*np.pi*norm)
    charge = p.e*N

    matter_time = (
        4*np.pi*omega**2*
        np.dot(volume,f*f*W_factor**2)
    )

    matter_gradient = (
        4*np.pi*
        np.dot(gradient_weights,np.diff(f)**2)
    )

    scalar_potential = (
        p.m*p.m*f*f
        -p.b*f**4
        +p.c*f**6
    )

    matter_potential = (
        4*np.pi*
        np.dot(volume,scalar_potential)
    )

    electric_inside = (
        2*np.pi*omega**2*
        np.dot(gradient_weights,np.diff(a)**2)
    )

    electric_outside = (
        2*np.pi*omega**2*
        centers[-1]*a[-1]**2
    )

    total = (
        matter_time
        +matter_gradient
        +matter_potential
        +electric_inside
        +electric_outside
    )

    flux = (
        4*np.pi*omega*centers[-1]*a[-1]
    )

    flux_error = (
        abs(flux-charge)/max(abs(charge),1.e-15)
        if p.e else 0.
    )

    return {
        'energy': float(total),
        'omega': float(omega),
        'charge': float(charge),
        'Noether_number': float(N),
        'gauss_residual': gauss_residual,
        'Gauss_exterior_flux': float(flux),
        'Gauss_flux_relative_error': float(flux_error),
        'components': {
            'matter_time': float(matter_time),
            'matter_gradient': float(matter_gradient),
            'matter_potential': float(matter_potential),
            'electric_radial': float(electric_inside),
            'electric_tail': float(electric_outside)
        },
        'max_a': float(np.max(a)),
        'max_weight_correction': float(
            np.max(abs(p.e*a))
        )
    }


def evaluate_fixed_N(
    p=Parameters(),
    modes=8,
    h=2.e-3
):
    """Eight-mode constrained static Hessian with Gauss reloading.

    Six smooth localized modes plus coherent-amplitude and
    radial-dilation directions. This is NOT a complete spectrum.
    """
    solution = bvp(p)

    n = p.finite_volume
    radius = (
        np.arange(n)+.5
    )*p.R/n

    f,fp = solution.sol(radius)[:2]

    dense = np.linspace(0,p.R,12001)
    fs,gs,As,Hs = solution.sol(dense)

    W = solution.p[0]-p.e*As

    N = float(
        8*np.pi*np.trapezoid(
            dense*dense*W*fs*fs,
            dense
        )
    )

    U = (
        p.m*p.m*fs*fs
        -p.b*fs**4
        +p.c*fs**6
    )

    continuous_energy = float(
        4*np.pi*np.trapezoid(
            dense*dense*(
                W*W*fs*fs
                +gs*gs
                +U
                +Hs*Hs/2
            ),
            dense
        )
        +(p.e*N)**2/(8*np.pi*p.R)
    )

    reference = finite_volume_reduced_energy(
        f,N,p
    )

    widths = [1.2,2.2,3.4,4.8,6.0,7.5]

    if modes < 1 or modes > 8:
        raise ValueError('Fixed basis supports 1 to 8 modes')

    basis = []

    for j in range(min(modes,len(widths))):
        bump = np.exp(
            -.5*((radius-widths[j])/1.3)**2
        )
        basis.append(f*bump)

    if modes > len(widths):
        basis.append(f.copy())

    if modes > len(widths)+1:
        basis.append(f+radius*fp)

    B = np.array(basis)

    def energy_for(coefficients):
        perturbed = (
            f+np.einsum(
                'i,ij->j',
                coefficients,B
            )
        )
        return finite_volume_reduced_energy(
            perturbed,N,p
        )['energy']

    zero = np.zeros(modes)
    E0 = energy_for(zero)

    gradient = []
    Hessian = np.zeros((modes,modes))

    for i in range(modes):
        ei = np.zeros(modes)
        ei[i] = h

        gradient.append(
            (
                energy_for(ei)
                -energy_for(-ei)
            )/(2*h)
        )

        Hessian[i,i] = (
            energy_for(ei)
            +energy_for(-ei)
            -2*E0
        )/h**2

        for j in range(i):
            ej = np.zeros(modes)
            ej[j] = h

            entry = (
                energy_for(ei+ej)
                -energy_for(ei-ej)
                -energy_for(-ei+ej)
                +energy_for(-ei-ej)
            )/(4*h*h)

            Hessian[i,j] = entry
            Hessian[j,i] = entry

    eigenvalues = np.linalg.eigvalsh(Hessian)

    return {
        'bvp_omega': float(solution.p[0]),
        'bvp_rms_max': float(
            np.max(solution.rms_residuals)
        ),
        'bvp_Noether_number': N,
        'bvp_energy_with_Coulomb_tail':
            continuous_energy,
        'finite_volume': reference,
        'relative_discrete_energy_error': float(
            abs(reference['energy']-continuous_energy)
            /continuous_energy
        ),
        'relative_discrete_omega_error': float(
            abs(reference['omega']-solution.p[0])
            /solution.p[0]
        ),
        'finite_modes': modes,
        'finite_h': h,
        'gradient': list(map(float,gradient)),
        'hessian_eigenvalues':
            list(map(float,eigenvalues)),
        'negative_eigenvalues': int(
            np.sum(eigenvalues < -1.e-5)
        ),
        'hessian_min': float(eigenvalues[0]),
        'hessian_max': float(eigenvalues[-1]),
        'classification':
            'RESTRICTED_RADIAL_FIXED_CHARGE_ENERGY_SCREEN_ONLY',
        'full_radial_dynamical_spectrum':
            'NOT_CALCULATED',
        'all_angular_perturbations':
            'NOT_CALCULATED',
        'verified_quantum_stability': 'NO'
    }


def exact_portal_principal(ph12=None):
    """Symbolic matter-trace and rank-one carrier principal Hessian."""
    p,alpha,beta,K,U,bb = sp.symbols(
        'p alpha beta K U bb',real=True
    )

    sigma = alpha*p-beta*p*p
    L = -sp.exp(2*sigma)*K-sp.exp(4*sigma)*U

    d1 = sp.factor(sp.diff(L,p))
    d2 = sp.factor(sp.diff(L,p,2))

    predicted = (
        -(2*sp.exp(2*sigma)*K
          +4*sp.exp(4*sigma)*U)
        *sp.diff(sigma,p,2)
        -(4*sp.exp(2*sigma)*K
          +16*sp.exp(4*sigma)*U)
        *sp.diff(sigma,p)**2
    )

    assert sp.simplify(d2-predicted)==0

    at_zero = (
        4*(beta-alpha**2)*K
        +8*(beta-2*alpha**2)*U
    )

    assert sp.simplify(
        d2.subs(p,0)-at_zero
    )==0

    ex,by,ey,bx = sp.symbols(
        'ex by ey bx',real=True
    )

    P = ex*by+ey*bx

    Llocal = (
        (ex**2+ey**2)/2
        +L.subs(p,P)
    )

    DX = sp.diff(Llocal,ex)
    DY = sp.diff(Llocal,ey)

    assert sp.simplify(
        DX-ex-sp.diff(L,p).subs(p,P)*by
    )==0

    assert sp.simplify(
        DY-ey-sp.diff(L,p).subs(p,P)*bx
    )==0

    ev = sp.symbols('ev',real=True)

    hessian = sp.diff(
        ev**2/2+L.subs(p,ev*bb),
        ev,2
    ).subs(ev,0)

    assert sp.simplify(
        hessian-(1+bb**2*at_zero)
    )==0

    bad = {
        alpha:.3,
        beta:.4,
        K:-4.,
        U:.15,
        bb:4.
    }

    counterexample = float(
        (1+bb**2*at_zero).subs(bad)
    )

    good = {
        alpha:.3,
        beta:.4,
        K:-.3,
        U:.2,
        bb:.1
    }

    small_field = float(
        (1+bb**2*at_zero).subs(good)
    )

    assert counterexample<0
    assert small_field>0

    source_center = {}

    if ph12 is not None:
        source = ph12['primary_gauged_equilibrium']

        f0 = float(source['center_f'])
        omega = float(source['omega'])
        coupling = float(
            source['spec']['gauge_coupling']
        )
        A0 = float(source['A0_at_center'])

        K0 = -((omega-coupling*A0)*f0)**2

        U0 = (
            f0*f0
            -2*f0**4
            +2*f0**6
        )

        lpp = float(
            at_zero.subs({
                alpha:.3,
                beta:.4,
                K:K0,
                U:U0
            })
        )

        source_center = {
            'PH12_scalar_K_center': K0,
            'PH12_scalar_U_center': U0,
            'rank_one_Lpp_at_P0': lpp,
            'frozen_matter_magnetic_norm_critical':
                math.sqrt(-1/lpp) if lpp<0 else None,
            'interpretation':
                'CONDITIONAL_HYPOTHETICAL_Y_MAGNETIC_BACKGROUND_NOT_AN_ON_SHELL_TWO_CARRIER_RESULT'
        }

    lambda_zero = sp.simplify(
        d1.subs(p,0)
    )

    assert sp.simplify(
        lambda_zero+(2*K+4*U)*alpha
    )==0

    return {
        'lambda_at_P0': str(lambda_zero),
        'same_action_electric_displacements':
            'DX=EX+lambda_BY_AND_DY=EY+lambda_BX',
        'variable_lambda_nonradial_bulk':
            'GRAD_LAMBDA_CROSSED_WITH_OTHER_ELECTRIC_OR_MAGNETIC_REQUIRED',
        'L_m_second_derivative_at_P0':
            str(at_zero),
        'principal_eigenvalues':
            'FIVE_TRANSVERSE_EQUAL_1_AND_ONE_LONGITUDINAL_1_PLUS_LPP_B2',
        'longitudinal_counterexample':
            counterexample,
        'longitudinal_small_field_control':
            small_field,
        'counterexample_background': {
            'alpha':.3,
            'beta':.4,
            'K':-4.,
            'U':.15,
            'Bnorm':4.
        },
        'source_center_conditional_threshold':
            source_center,
        'same_action_matter_trace_loading':
            'REQUIRED_NONCONSTANT_LAMBDA',
        'full_Dirac_Bergmann_constraint_health':
            'NOT_CERTIFIED',
        'full_metric_Einstein_UV_causality':
            'NOT_CERTIFIED',
        'Y_field_source_and_exterior_mixed_P':
            'NOT_PRESENT_IN_PH12'
    }


def exact_joint_scalar_carrier_hessian(ph12=None):
    """Joint scalar/carrier Hessian in one polarization.

    A necessary local principal condition; not a complete
    constrained gravity, gauge or quantum-mode spectrum.
    """
    eps,B,v,grad2,U,a,b = sp.symbols(
        'eps B v grad2 U alpha beta',
        real=True
    )

    P = eps*B
    sigma = a*P-b*P**2
    omega = sp.exp(sigma)

    L = (
        eps**2/2
        +omega**2*(v**2-grad2)
        -omega**4*U
    )

    H = sp.hessian(
        L,(v,eps)
    ).subs(eps,0)

    frozen = sp.factor(H[1,1])
    schur = sp.factor(
        H[1,1]-H[0,1]**2/H[0,0]
    )

    predicted_frozen = (
        1+B**2*(
            4*(b-a*a)*(grad2-v*v)
            +8*(b-2*a*a)*U
        )
    )

    predicted_joint = (
        1+B**2*(
            4*(b-a*a)*grad2
            -4*(b+a*a)*v*v
            +8*(b-2*a*a)*U
        )
    )

    assert sp.simplify(
        frozen-predicted_frozen
    )==0

    assert sp.simplify(
        schur-predicted_joint
    )==0

    assert sp.simplify(H[0,0]-2)==0
    assert sp.simplify(sp.det(H)-2*schur)==0

    numeric = sp.lambdify(
        (v,eps,B,grad2,U,a,b),
        L,'numpy'
    )

    h = 1.e-4
    vv = .6344175224

    def fun(vv_,ee_):
        return float(
            numeric(
                vv_,ee_,2.,0.,.245098,.3,.4
            )
        )

    finite_difference = (
        fun(vv+h,h)
        -fun(vv+h,-h)
        -fun(vv-h,h)
        +fun(vv-h,-h)
    )/(4*h*h)

    mixed = float(
        H[0,1].subs({
            v:vv,B:2.,grad2:0.,
            U:.245098,a:.3,b:.4
        })
    )

    assert abs(finite_difference-mixed)<3.e-7

    sample = {
        a:.3,b:.4,grad2:0.,
        U:.245098,v:vv,B:2.
    }

    frozen_sample = float(
        frozen.subs(sample)
    )

    joint_sample = float(
        schur.subs(sample)
    )

    assert frozen_sample>0
    assert joint_sample<0

    source_center = {}

    if ph12 is not None:
        q = ph12['primary_gauged_equilibrium']

        f0 = float(q['center_f'])

        W = (
            float(q['omega'])
            -float(q['spec']['gauge_coupling'])
            *float(q['A0_at_center'])
        )

        v2 = (W*f0)**2

        potential = (
            f0*f0
            -2*f0**4
            +2*f0**6
        )

        common = {
            a:.3,b:.4,
            v:math.sqrt(v2),
            grad2:0.,
            U:potential
        }

        cf = float(
            sp.diff(frozen,B,2).subs({
                **common,B:0
            })/2
        )

        cj = float(
            sp.diff(schur,B,2).subs({
                **common,B:0
            })/2
        )

        assert cj<cf<0

        source_center = {
            'PH12_f0': f0,
            'PH12_covariant_time_velocity_squared':
                v2,
            'PH12_scalar_potential':
                potential,
            'frozen_carrier_B_squared_coefficient':
                cf,
            'joint_scalar_carrier_B_squared_coefficient':
                cj,
            'frozen_carrier_threshold_B':
                math.sqrt(-1/cf),
            'joint_scalar_carrier_threshold_B':
                math.sqrt(-1/cj),
            'B2_test_frozen_eigenvalue':
                float(frozen.subs({
                    **common,B:2.
                })),
            'B2_test_joint_Schur':
                float(schur.subs({
                    **common,B:2.
                })),
            'source_note':
                'REQUIRES_HYPOTHETICAL_ON_SHELL_MAGNETIC_Y_BACKGROUND_NOT_IN_PH12'
        }

        assert (
            source_center['B2_test_frozen_eigenvalue']>0
        )
        assert (
            source_center['B2_test_joint_Schur']<0
        )

    return {
        'source_center_conditional_joint_hessian':
            source_center,
        'joint_vv_kinetic_coefficient': 2.0,
        'closed_form_frozen':
            str(predicted_frozen),
        'closed_form_schur':
            str(predicted_joint),
        'independent_mixed_second_derivative_fd':
            finite_difference,
        'independent_mixed_second_derivative_exact':
            mixed,
        'constructed_frozen_positive_joint_negative': {
            'frozen': frozen_sample,
            'Schur': joint_sample
        },
        'classification':
            'NECESSARY_LOCAL_PRINCIPAL_MATRIX_NOT_FULL_GAUGE_GRAVITY_PROOF'
    }


def noether_craft_theorem(ph7=None):
    """Separate internal momentum transfer from external craft impulse."""
    fn,fs,ff = sp.symbols(
        'fn fs ff',real=True
    )

    assert sp.simplify(
        (fn+fs+ff).subs(ff,-fn-fs)
    )==0

    if ph7 is None:
        q = .0135056116872862
        field = -.013505464288151511
        src = -1.4056781776116325e-7
    else:
        ledger = ph7['fine_momentum_ledger']
        q = float(ledger['neutral_momentum'])
        field = float(ledger['field_momentum'])
        src = float(
            ledger['source_center_momentum']
        )

    residual = q+field+src

    assert abs(residual)<1.e-8

    return {
        'internal_transfers_cancel':
            'PASS_EXACT_NOETHER_CONTROL',
        'PH7_neutral_impulse': q,
        'PH7_carrier_impulse': field,
        'PH7_source_impulse': src,
        'PH7_total_discrete_momentum_residual':
            residual,
        'PH12_pure_X_electric_mixed_P': 0.0,
        'PH12_native_neutral_metric_repulsion':
            'NOT_DERIVED',
        'whole_craft_external_impulse':
            'NOT_DERIVED',
        'Earth_and_atmosphere_contact_field_boundary':
            'NOT_COUPLED',
        'B11_M6_complete_signed_cycle':
            'NOT_RUN',
        'interpretation':
            'CLOSED_INTERNAL_SYSTEM_CANNOT_PRODUCE_NET_LIFT_WITHOUT_EXTERNAL_MOMENTUM_FLUX_OR_EARTH_FORCE'
    }


def provenance(root):
    """Verify historical artifacts without modifying them."""
    result = {}

    for name,(relative,expected) in ARCHIVES.items():
        path = Path(root)/relative

        if not path.is_file():
            result[name] = {
                'status':'MISSING',
                'expected_sha256':expected
            }
        else:
            actual = sha256(
                path.read_bytes()
            ).hexdigest()

            result[name] = {
                'status': (
                    'MATCH' if actual==expected
                    else 'HASH_MISMATCH'
                ),
                'actual_sha256':actual,
                'expected_sha256':expected
            }

    return result


def trace_induced_second_carrier(
    p: Parameters = Parameters(),
    n: int = 65,
    length: float = 64.,
    separation: float = 16.,
    alpha: float = .3,
    same_center: bool = False,
    only_one: bool = False
):
    """First-order induced Y from two separated PH12 X lumps.

    The individual radial configurations are on-shell.
    Their combined two-center superposition is NOT on-shell.

    Project E into the periodic longitudinal subspace, then solve
        curl B_Y = curl(lambda E_X)
    using the transverse Helmholtz projector.
    """
    if (
        n<33 or n%2!=1
        or length<=0
        or separation<=0
        or not math.isfinite(alpha)
    ):
        raise ValueError(
            'Odd n>=33 and valid finite geometry required'
        )

    if (
        separation/2>length/4
        or p.R<length/2
    ):
        raise ValueError(
            'Invalid source and periodic domain geometry'
        )

    solution = bvp(p)

    dx = length/n
    coords = (
        np.arange(n)-n//2
    )*dx

    x,y,z = np.meshgrid(
        coords,coords,coords,
        indexing='ij'
    )

    E = np.zeros(
        (3,n,n,n),dtype=float
    )

    lam = np.zeros(
        (n,n,n),dtype=float
    )

    centers = (
        (separation/2,1),
        (-separation/2,-1)
    )

    if same_center:
        centers = (
            (0.,1),(0.,-1)
        )

    if only_one:
        centers = ((0.,1),)

    radial_points = np.linspace(
        0,p.R,8001
    )

    fr,_,Ar,_ = solution.sol(
        radial_points
    )

    Noether = float(
        8*np.pi*np.trapezoid(
            radial_points**2
            *(solution.p[0]-p.e*Ar)
            *fr*fr,
            radial_points
        )
    )

    Qsource = p.e*Noether

    for center_z,sign in centers:
        xyz = (
            x,y,z-center_z
        )

        rr = np.sqrt(
            sum(u*u for u in xyz)
        )

        clipped = np.minimum(
            rr,p.R
        )

        f,df,A,dA = solution.sol(
            clipped.ravel()
        ).reshape(4,*rr.shape)

        W = solution.p[0]-p.e*A

        K = -(W*f)**2+df*df

        U = (
            p.m*p.m*f*f
            -p.b*f**4
            +p.c*f**6
        )

        local_lambda = -alpha*(
            2*K+4*U
        )

        local_lambda[rr>p.R] = 0.

        lam += local_lambda

        exterior_field = (
            Qsource/
            (
                4*np.pi
                *np.maximum(rr,1.e-12)**2
            )
        )

        electric_radial = np.where(
            rr>p.R,
            exterior_field,
            -dA
        )

        for i,u in enumerate(xyz):
            E[i] += (
                sign*electric_radial
                *u/np.maximum(rr,1.e-12)
            )

    # A periodic longitudinal projection prevents a fake
    # nonzero volume-integrated mixed topological term.
    ks = 2*np.pi*np.fft.fftfreq(
        n,d=dx
    )

    k = np.stack(
        np.meshgrid(
            ks,ks,ks,
            indexing='ij'
        )
    )

    k2 = np.sum(
        k*k,axis=0
    )

    inverse = np.divide(
        1.,k2,
        out=np.zeros_like(k2),
        where=k2>0
    )

    raw_hat = np.stack([
        np.fft.fftn(u)
        for u in E
    ])

    k_dot_E = np.sum(
        k*raw_hat,axis=0
    )

    E_hat = k*(
        k_dot_E*inverse
    )[None]

    E = np.fft.ifftn(
        E_hat,
        axes=(1,2,3)
    ).real

    V = E*lam[None]

    Vhat = np.stack([
        np.fft.fftn(u)
        for u in V
    ])

    k_dot_V = np.sum(
        k*Vhat,axis=0
    )

    Bhat = (
        Vhat
        -k*(k_dot_V*inverse)[None]
    )

    B = np.fft.ifftn(
        Bhat,
        axes=(1,2,3)
    ).real

    mixed = np.sum(
        E*B,axis=0
    )

    volume = dx**3

    Jhat = 1j*np.stack([
        k[1]*Vhat[2]-k[2]*Vhat[1],
        k[2]*Vhat[0]-k[0]*Vhat[2],
        k[0]*Vhat[1]-k[1]*Vhat[0]
    ])

    curlBhat = 1j*np.stack([
        k[1]*Bhat[2]-k[2]*Bhat[1],
        k[2]*Bhat[0]-k[0]*Bhat[2],
        k[0]*Bhat[1]-k[1]*Bhat[0]
    ])

    Jnorm = np.linalg.norm(Jhat)

    ampere_residual = float(
        np.linalg.norm(
            curlBhat-Jhat
        )/max(Jnorm,1.e-25)
    )

    divB_residual = float(
        np.linalg.norm(
            np.sum(k*Bhat,axis=0)
        )/max(np.linalg.norm(Bhat),1.e-25)
    )

    return {
        'n': n,
        'length': length,
        'separation': separation,
        'alpha': alpha,
        'single_isolated_source_gauge_charge':
            Qsource,
        'charge_conjugated_pair':
            not same_center and not only_one,
        'same_center_control': same_center,
        'single_lump_control': only_one,
        'max_abs_local_P': float(
            np.max(abs(mixed))
        ),
        'L1_local_P': float(
            volume*np.sum(abs(mixed))
        ),
        'signed_integral_P': float(
            volume*np.sum(mixed)
        ),
        'Y_B2_integral': float(
            volume*np.sum(B*B)
        ),
        'Y_B_magnetic_energy': float(
            .5*volume*np.sum(B*B)
        ),
        'ampere_residual_spectral':
            ampere_residual,
        'divB_over_B_norm_spectral':
            divB_residual,
        'Y_microscopic_current':
            'NONE_TO_FIRST_ORDER',
        'Y_induced_source':
            'CURL_LAMBDA_EX_EQUIVALENT_ONLY',
        'interpretation':
            'OFFSHELL_TWO_CENTER_SUPERPOSITION_LINEAR_TRACE_RESPONSE_NOT_A_DEVICE',
        'full_Y_backreaction': 'NOT_SOLVED',
        'physical_source_support_and_Earth':
            'NOT_SOLVED'
    }


def run(root):
    """Constraint-first integrated audit without broad parameter sweeps."""
    root = Path(root)

    with (
        root/ARCHIVES['ph12_result'][0]
    ).open('r',encoding='utf-8') as stream:
        ph12 = json.load(stream)

    if ph12.get('branch') != '032H17A12D1R3X3B17-PH12':
        raise ValueError('Wrong PH12 branch')

    with (
        root/ARCHIVES['ph7_result'][0]
    ).open('r',encoding='utf-8') as stream:
        ph7 = json.load(stream)

    primary = evaluate_fixed_N()

    alternate = evaluate_fixed_N(
        Parameters(finite_volume=640),
        modes=8,
        h=1.e-3
    )

    prior = ph12['primary_gauged_equilibrium']

    assert abs(
        primary['bvp_omega']-prior['omega']
    )<5.e-8

    assert abs(
        primary['bvp_Noether_number']
        -prior['Noether_number']
    )<5.e-5

    assert abs(
        primary['bvp_energy_with_Coulomb_tail']
        -prior['canonical_energy'][
            'scalar_plus_electromagnetic_total_including_Coulomb_tail'
        ]
    )<5.e-4

    assert (
        primary['finite_volume']['gauss_residual']
        <1.e-9
    )

    assert (
        primary['finite_volume']['Gauss_flux_relative_error']
        <1.e-8
    )

    assert primary['relative_discrete_energy_error']<.03
    assert primary['relative_discrete_omega_error']<.03

    assert max(
        abs(v) for v in primary['gradient']
    )<.3

    assert abs(
        primary['hessian_min']
        -alternate['hessian_min']
    )<.05

    principal = exact_portal_principal(ph12)
    joint = exact_joint_scalar_carrier_hessian(ph12)
    momentum = noether_craft_theorem(ph7)

    linear_Y = {
        n:trace_induced_second_carrier(n=n)
        for n in (65,97,129)
    }

    portal_off = trace_induced_second_carrier(
        n=65,alpha=0.
    )

    coincident = trace_induced_second_carrier(
        n=65,same_center=True
    )

    single_spherical = {
        n:trace_induced_second_carrier(
            n=n,only_one=True
        )
        for n in (65,97,129)
    }

    assert all(
        a['ampere_residual_spectral']<1.e-10
        for a in linear_Y.values()
    )

    assert all(
        a['divB_over_B_norm_spectral']<1.e-10
        for a in linear_Y.values()
    )

    assert all(
        abs(a['signed_integral_P'])<1.e-12
        for a in linear_Y.values()
    )

    assert all(
        a['Y_B2_integral']>0
        and a['L1_local_P']>0
        for a in linear_Y.values()
    )

    assert portal_off['Y_B2_integral']==0
    assert portal_off['max_abs_local_P']==0
    assert coincident['Y_B2_integral']==0
    assert coincident['max_abs_local_P']==0

    assert (
        abs(
            linear_Y[129]['Y_B2_integral']
            -linear_Y[97]['Y_B2_integral']
        )/linear_Y[129]['Y_B2_integral']
        <.01
    )

    assert (
        single_spherical[129]['Y_B2_integral']
        /linear_Y[129]['Y_B2_integral']
        <1.e-5
    )

    history = provenance(root)

    gates = {
        'P0_PROVENANCE': (
            'PASS'
            if all(
                v['status']=='MATCH'
                for v in history.values()
            )
            else 'UNRESOLVED'
        ),
        'P1_PH12_INDEPENDENT_BVP_RECONSTRUCTION':
            'PASS_RADIAL_STATIC_SCOPED',
        'P1_FIXED_CHARGE_GAUSS_RELOADING':
            'PASS_NUMERIC_FV_SCOPED',
        'P1_RADIAL_ENERGY_HESSIAN': (
            'NEGATIVE_DIRECTION_FOUND'
            if primary['negative_eigenvalues']
            else 'NONNEGATIVE_SAMPLED_SUBSPACE_ONLY'
        ),
        'P1_FULL_RADIAL_DYNAMICAL_AND_ANGULAR_STABILITY':
            'NOT_CERTIFIED',
        'P1_PHI6_UV_NATURALNESS':
            'NOT_CERTIFIED',
        'P2_UNIVERSAL_METRIC_PRINCIPAL_HESSIAN':
            'EXACT_RANK_ONE_NECESSARY_CONDITION',
        'P2_JOINT_SOURCE_CARRIER_KINETIC':
            'RED_CONDITIONAL_UNSTABLE_BACKGROUND_FOUND',
        'P2_BACKGROUND_INDEPENDENT_MODE_HEALTH':
            'RED_COUNTEREXAMPLE_TO_UNRESTRICTED_PARAMETER_UNIVERSE',
        'P2_TWO_CARRIER_ACTUAL_BACKGROUND_AND_SOURCE':
            'NOT_SOLVED',
        'P2_TRACE_INDUCED_SECOND_CARRIER':
            'PASS_FIRST_ORDER_OFFSHELL_SUPERPOSITION_ONLY',
        'P2_MIXED_P_SPATIALLY_NONZERO':
            'PASS_LOCAL_PERIODIC_SCREEN_NO_SI',
        'P2_STATIC_MIXED_P_VOLUME':
            'ZERO_WITH_PERIODIC_BOUNDARY_WARD',
        'P2_EARTH_INTERACTION_AND_EXTERNAL_CRAFT_FORCE':
            'NOT_DERIVED',
        'B11_M6_COMPLETE_SIGNED_CAUSAL_CYCLE':
            'NOT_RUN',
        'P3_NEUTRAL_GE1G_GE1M':
            'NOT_CERTIFIED',
        'STRICT_COMPLETE_LT10MJ':
            'NOT_CERTIFIED',
        '006D_REPLACED': 'NO'
    }

    return {
        'branch': BRANCH,
        'previous_case':
            'PH12_ISOLATED_GAUGED_QBALL',
        'independent_radial_static_fixed_charge':
            primary,
        'radial_resolution_crosscheck': {
            'finite_volume':640,
            'hessian_min':
                alternate['hessian_min'],
            'negative_eigenvalues':
                alternate['negative_eigenvalues'],
            'gradient_max':float(
                max(
                    abs(v)
                    for v in alternate['gradient']
                )
            )
        },
        'universal_two_carrier_principal_gate':
            principal,
        'joint_scalar_carrier_principal_gate':
            joint,
        'whole_spacecraft_momentum_theorem':
            momentum,
        'PH12_pair_linear_trace_induced_Y': {
            'resolution_cases': {
                str(n):case
                for n,case in linear_Y.items()
            },
            'portal_slope_off':portal_off,
            'colocated_opposite_charge':coincident,
            'single_spherical_aliasing': {
                str(n):case
                for n,case in single_spherical.items()
            },
            'induction_source':
                'FULL_ACTION_MATTER_TRACE_LINEARIZATION_AT_P0',
            'Y_microscopic_source':
                'NONE_FOR_THIS_FIRST_ORDER_EQUATION',
            'composite_on_shell':
                'NO_OFFSHELL_TWO_CENTER_SUPERPOSITION',
            'fully_nonperturbative_conformal_Maxwell_matter':
                'NOT_SOLVED',
            'periodic_exterior':
                'NOT_CERTIFIED',
            'net_craft_force':
                'NOT_DERIVED'
        },
        'archival_provenance': history,
        'gates': gates,
        'verdict':
            'YELLOW_PH12_ISOLATED_SOURCE_WITH_RESTRICTED_STABILITY_AND_UNIVERSAL_PORTAL_HEALTH_OBSTRUCTIONS_NO_ENGINE'
    }
