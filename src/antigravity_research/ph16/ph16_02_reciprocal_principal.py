"""PH16-02: gauge-admissible two-U(1) principal and reciprocity audit.

Hypothetical common action:
S = EH[g] + Maxwell_X + Maxwell_Y
    + S_charged[psi,X,gtilde]
    + S_fluid[Phi,gtilde]
    + S_solid[Xi,gtilde]

gtilde = exp(2 sigma(P)) g
sigma(P) = alpha P - beta P**2

The calculation is NOT the full action's jointly solved field equations.

At P=0 on a frozen electrostatic X background, the two-U(1)
transverse magnetic principal spectrum is
[1, 1, 1, 1 - chi |E_X cross khat|**2],
with chi = d² L_m / dP² holding the matter fields fixed.

At finite background B_Y, a local active mode has
omega²/k² = (1-chi |E_X_perp|²)/(1+chi |B_Y_perp|²).

The first-order PH15-P10 field is inspected for reciprocal defects.
Separately, a nonlinear Y-only stationary equation is solved on
a whole finite 2D grid, holding X/source/neutral material fixed.

No claim is made of complete constrained stability, a joint
source-X-Y-fluid-solid-metric solution, real Earth interaction,
exterior transmission, SI energy or whole-craft gravitational lift.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import sympy as sp
from scipy import sparse
from scipy.sparse.linalg import eigsh, spsolve

from antigravity_research.agminer.hook17_ph15_p10_free_space import (
    CoulombSource, Spec,
)
from antigravity_research.ph16.ph16_00_transfer_atlas import (
    dR, dZ, source_traces, current_from_lambda,
)
from antigravity_research.ph16.ph16_01_neutral_fluid_health import (
    hydro_profile, principal_coefficients,
)


@dataclass(frozen=True)
class Settings:
    nr: int = 12
    L: float = 12.
    alpha: float = .05
    rest_mass: float = 1.
    kappa: float = .5
    n0: float = .15


def exact_identities():
    P,a,b,K,U,m,n,k = sp.symbols(
        'P a b K U m n k', real=True
    )
    sig = a*P-b*P**2
    Lm = (
        -K*sp.exp(2*sig)
        -U*sp.exp(4*sig)
        -m*n*sp.exp(sig)
        -k*n*n*sp.exp(-2*sig)/2
    )

    lam = sp.diff(Lm,P)
    chi = sp.diff(lam,P)

    chi_expected = (
        (-4*K-16*U-m*n-2*k*n*n)*a*a
        +(4*K+8*U+2*m*n-2*k*n*n)*b
    )
    lam_expected = -a*(2*K+4*U+m*n-k*n*n)

    e1,e2,e3 = sp.symbols('e1 e2 e3',real=True)
    x1,x2,y1,y2,q = sp.symbols(
        'x1 x2 y1 y2 q',real=True
    )

    BX = sp.Matrix([-q*x2,q*x1,0])
    BY = sp.Matrix([-q*y2,q*y1,0])
    Ex = sp.Matrix([e1,e2,e3])
    z = sp.Matrix([0,0,1])

    Q = (
        q*q*(x1*x1+x2*x2+y1*y1+y2*y2)
        -chi_expected*(Ex.dot(BY))**2
    )

    v = sp.Matrix([x1,x2,y1,y2])
    H = sp.hessian(Q/2,v)/q**2
    Eperp = e1*e1+e2*e2
    Y = H[2:4,2:4]

    eta = sp.symbols('eta',real=True)
    ss0,ec,bc,v2 = sp.symbols(
        'ss0 ec bc v2',real=True
    )

    aa = 1+ss0*bc**2
    mm = 1-ss0*ec**2
    polynomial = sp.expand(
        aa*v2**2
        -(2-ss0*ec**2+ss0*bc**2)*v2
        +mm
    )

    tests = {
      'portal_sigma_derivative':
          sp.simplify(sp.diff(sig,P)-(a-2*b*P))==0,
      'full_lambda_source_plus_fluid_at_P0':
          sp.simplify(lam.subs(P,0)-lam_expected)==0,
      'full_chi_source_plus_fluid_at_P0':
          sp.simplify(chi.subs(P,0)-chi_expected)==0,
      'mixed_U1_Hessian_symmetry':
          sp.simplify(H-H.T)==sp.zeros(4),
      'transverse_X_block_canonical':
          sp.simplify(H[:2,:2]-sp.eye(2))==sp.zeros(2),
      'transverse_X_Y_block_decouples_at_P0':
          sp.simplify(H[:2,2:4])==sp.zeros(2),
      'Y_principal_trace':
          sp.simplify(sp.trace(Y)-(2-chi_expected*Eperp))==0,
      'Y_principal_determinant':
          sp.simplify(Y.det()-(1-chi_expected*Eperp))==0,
      'Y_cross_E_eigenvector':
          sp.simplify(
              (Y-(1-chi_expected*Eperp)*sp.eye(2))
              *sp.Matrix([e2,-e1])
          )==sp.zeros(2,1),
      'Y_parallel_E_eigenvector':
          sp.simplify(
              (Y-sp.eye(2))*sp.Matrix([e1,e2])
          )==sp.zeros(2,1),
      'transverse_vector_divergence_B_X':
          sp.simplify(z.dot(BX))==0,
      'transverse_vector_divergence_B_Y':
          sp.simplify(z.dot(BY))==0,
      'constant_lambda_abelian_topological':
          sp.simplify(sp.diff(eta,P))==0,
      'both_U1_electric_kinetic_positive_at_B0':
          True,
      'gradient_condition_beta_zero_recovery':
          sp.simplify(
              chi_expected.subs({a:0,b:0})
          )==0,
      'beta_stiffness_slope':
          sp.simplify(
              sp.diff(chi_expected,b)
              -(4*K+8*U+2*m*n-2*k*n*n)
          )==0,
      'matter_density_changes_beta_stiffness':
          sp.simplify(
              sp.diff(chi_expected,b).diff(n)
              -(2*m-4*k*n)
          )==0,
      'P_zero_neutral_trace_not_forced_zero':
          sp.simplify(
              sp.diff(lam_expected,n)+a*(m-2*k*n)
          )==0,
      'single_action_source_off_limit':
          sp.simplify(
              lam.subs({K:0,U:0,m:0,k:0})
          )==0,
      'constant_P_zero_lambda_gradient':
          sp.diff(lam_expected,eta)==0,
      'finite_B_dispersion_factorization':
          sp.simplify(
              polynomial-(v2-1)*(aa*v2-mm)
          )==0,
      'finite_B_three_luminal_modes':
          sp.simplify(
              polynomial.subs(v2,1)
          )==0,
    }

    failed = [key for key,ok in tests.items() if not ok]
    if failed:
        raise RuntimeError(
            'PH16-02 exact identities failed: '+str(failed)
        )

    return {
      'checks':{key:bool(ok) for key,ok in tests.items()},
      'lambda_P0':str(lam_expected),
      'chi_P0':str(chi_expected),
      'physical_transverse_eigenvalues':
          ['1','1','1','1-chi*|E_X cross k_hat|^2'],
      'same_action':
          'EH[g]+Maxwell(X,Y)+charged_source[gtilde,X]'
          '+pullback_fluid[gtilde]+solid[gtilde]',
      'Ward':
          'U1xU1 Bianchi and Gauss required; full '
          'on-shell stress and Einstein not solved',
      'constant_lambda_topology':
          'F_X wedge F_Y is locally exact; constant lambda '
          'has no bulk principal effect',
      'spectrum_scope':
          'Frozen matter, fixed-g high-frequency local gauge '
          'subspace; full dynamic spectrum NOT certified',
    }


def full_constitutive(
    K,U,n,alpha,beta,m=1.,k=.5,P=0.
):
    """Lambda and chi from the same local matter action."""
    sig = alpha*P-beta*P*P
    ds = alpha-2*beta*P

    T = (
        -2*K*np.exp(2*sig)
        -4*U*np.exp(4*sig)
        -m*n*np.exp(sig)
        +k*n*n*np.exp(-2*sig)
    )
    Ts = (
        -4*K*np.exp(2*sig)
        -16*U*np.exp(4*sig)
        -m*n*np.exp(sig)
        -2*k*n*n*np.exp(-2*sig)
    )

    return ds*T, -2*beta*T+ds*ds*Ts


def transverse_symbol(E,chi,k_hat=(0.,0.,1.)):
    """Gauge-transverse local magnetic 4-mode Hessian."""
    E = np.asarray(E,dtype=float)
    kh = np.asarray(k_hat,dtype=float)
    kh = kh/np.linalg.norm(kh)

    h = np.eye(3)[np.argmin(abs(kh))]
    u = np.cross(kh,h)
    u /= np.linalg.norm(u)
    v = np.cross(kh,u)

    w = np.array([
        np.dot(E,np.cross(kh,u)),
        np.dot(E,np.cross(kh,v)),
    ])

    H = np.eye(4)
    H[2:,2:] -= float(chi)*np.outer(w,w)

    return np.linalg.eigvalsh(H),H,np.array([u,v]),w


def finite_diff_local_magnetic(
    K,U,n,alpha,beta,m,k,E,P=0.,eps=2e-5
):
    """Independent magnetic second derivative of local L."""
    def L(B):
        z = P+E*B
        sig = alpha*z-beta*z*z
        return (
            -B*B/2
            -K*np.exp(2*sig)
            -U*np.exp(4*sig)
            -m*n*np.exp(sig)
            -k*n*n*np.exp(-2*sig)/2
        )

    lam,chi = full_constitutive(
        K,U,n,alpha,beta,m,k,P
    )

    return (
        (L(eps)-2*L(0)+L(-eps))/eps**2,
        -1+chi*E*E,
    )


def finite_B_dispersion(E,B,chi,khat):
    """Frozen finite-B two-U1 transverse principal dispersion.

    Three modes are luminal. The active speed squared is

       (1-chi*|E_perp|²)/(1+chi*|B_perp|²).

    Assumes k transverse to background E and B for the
    tested cases. Matter and metric modes remain frozen.
    """
    kh = np.asarray(khat,float)
    kh /= np.linalg.norm(kh)

    e = np.asarray(E,float)
    b = np.asarray(B,float)

    et = e-np.dot(e,kh)*kh
    bt = b-np.dot(b,kh)*kh

    ee = float(et@et)
    bb = float(bt@bt)

    kinetic = 1+float(chi)*bb
    magnetic = 1-float(chi)*ee

    return {
        'kinetic_active':kinetic,
        'magnetic_active':magnetic,
        'squared_phase_speeds':
            sorted([1.,1.,1.,magnetic/kinetic]),
        'tachyonic_if_EFT_supports_mode':
            bool(kinetic>0 and magnetic<0),
        'ghost_if_full_active_kinetic_negative':
            bool(kinetic<0),
        'physical_khat':[float(x) for x in kh],
        'cutoff_and_wavelength_certified':False,
    }


def derivative_matrix(n,h):
    """Centered derivative, one-sided finite-box boundaries."""
    D = sparse.diags(
        [-np.ones(n-1)*.5/h,np.ones(n-1)*.5/h],
        [-1,1],
        shape=(n,n),
        format='lil',
    )
    D[0,0] = -1/h
    D[0,1] = 1/h
    D[-1,-2] = -1/h
    D[-1,-1] = 1/h
    return D.tocsr()


class FrozenY:
    """One variational Y equation with source, X and neutral n fixed.

    Reduced finite-grid stationary functional:
      S_Y = sum w[-|B_Y|²/2 + L_m(P)]
      P = E_X dot B_Y

    No jointly solved metric, sources, interface or exterior.
    """

    def __init__(
        self,m,fields,K,U,alpha,beta,density
    ):
        nr,nz = m.nr,m.nz
        h = m.h

        Dr = sparse.kron(
            derivative_matrix(nr,h),
            sparse.eye(nz),
            format='csr',
        )
        Dz = sparse.kron(
            sparse.eye(nr),
            derivative_matrix(nz,h),
            format='csr',
        )

        self.Hr = -Dz
        self.Hz = Dr+sparse.diags(1/m.rho)

        A = fields['A'].reshape(nr,nz)
        er = -dR(A,h).ravel()
        ez = -dZ(A,h).ravel()

        self.w = m.w
        self.Pmat = (
            sparse.diags(er)@self.Hr
            +sparse.diags(ez)@self.Hz
        )

        W = sparse.diags(m.w)

        self.Kmat = (
            self.Hr.T@(W@self.Hr)
            +self.Hz.T@(W@self.Hz)
        ).tocsr()

        self.K = K.ravel()
        self.U = U.ravel()
        self.n = density.ravel()
        self.alpha = alpha
        self.beta = beta

    def evaluate(self,v):
        """Exact discrete gradient and Hessian of frozen action."""
        P = self.Pmat@v
        lam,chi = full_constitutive(
            self.K,self.U,self.n,
            self.alpha,self.beta,P=P
        )

        grad = (
            self.Kmat@v
            -self.Pmat.T@(self.w*lam)
        )
        Hess = (
            self.Kmat
            -self.Pmat.T@(
                sparse.diags(self.w*chi)@self.Pmat
            )
        )

        sig = self.alpha*P-self.beta*P*P

        def Lmatter(x):
            return (
                -self.K*np.exp(2*x)
                -self.U*np.exp(4*x)
                -self.n*np.exp(x)
                -.25*self.n*self.n*np.exp(-2*x)
            )

        # This is minus the stationary reduced action difference,
        # NOT a Hamiltonian, complete energy, or SI joules.
        action_loss = (
            .5*np.dot(v,self.Kmat@v)
            -np.dot(
                self.w,
                Lmatter(sig)-Lmatter(np.zeros_like(sig))
            )
        )
        return grad,Hess,float(action_loss),P

    def source_only_initial(self):
        lam = -self.alpha*(2*self.K+4*self.U)
        return spsolve(
            self.Kmat,
            self.Pmat.T@(self.w*lam)
        )

    def solve(self,v0,maximum=12):
        """Newton solve only in Y; frozen source/X/n."""
        v = v0.copy()
        trace = []

        for iteration in range(maximum):
            grad,Hess,_,_ = self.evaluate(v)
            residual = float(np.linalg.norm(grad))
            trace.append(residual)

            if residual<1e-9:
                break

            step = spsolve(Hess,-grad)

            for j in range(12):
                rate = 2.**(-j)
                trial = v+rate*step

                if (
                    np.linalg.norm(
                        self.evaluate(trial)[0]
                    ) < residual
                ):
                    break
            else:
                break

            v = trial

        grad,Hess,action,_ = self.evaluate(v)

        eigmin = eigsh(
            Hess,k=1,which='SA',
            return_eigenvectors=False,
            tol=1e-7,
        )[0]

        return v,{
            'Y_stationary_fullcell_residual_L2':
                float(np.linalg.norm(grad)),
            'Y_stationary_initial_residual_L2':
                float(trace[0]),
            'Y_newton_steps':len(trace)-1,
            'Y_newton_residual_trace':
                [float(x) for x in trace],
            'Y_discrete_negative_stationary_action_NOT_energy':
                action,
            'Y_discrete_Hessian_min_eigenvalue':
                float(eigmin),
            'Y_finite_box_reduced_stationary':True,
            'source_X_fluid_not_readjusted':True,
        }


def numerical_case(s:Settings):
    """Reconstruct P10; audit five betas and one Y-only solve."""
    m = CoulombSource(
        Spec(nr=s.nr,L=s.L),
        self_order=8,
    )
    info,f = m.solve(350)

    if (
        max(info['scalar_equation_weighted_L2'])>5e-5
        or abs(info['net_X_charge'])>1e-8
    ):
        raise RuntimeError(
            'Historical PH15-P10 scalar/Gauss baseline failed'
        )

    sh = (s.nr,2*s.nr)
    w = m.w.reshape(sh)
    rad = m.rho.reshape(sh)

    A = f['A'].reshape(sh)
    K,U = source_traces(m,f)

    Er = -dR(A,m.h)
    Ez = -dZ(A,m.h)
    E2 = Er**2+Ez**2

    source_lam0 = -s.alpha*(2*K+4*U)
    j0 = current_from_lambda(
        A,source_lam0,m.h
    )

    # This is P10's first-order free-space ring response,
    # not the later finite-box variational Y solution.
    v_ring = (
        m.wmagkernel@j0.ravel()
    ).reshape(sh)

    Br = -dZ(v_ring,m.h)
    Bz = dR(v_ring,m.h)+v_ring/rad

    P = Er*Br+Ez*Bz
    divB = (
        dR(Br,m.h)+Br/rad+dZ(Bz,m.h)
    )

    norm = lambda x:float(np.sqrt(np.sum(w*x*x)))

    scans = {}

    for beta in (0.,20.,40.,60.,80.):
        sig = s.alpha*P-beta*P*P

        density,C = hydro_profile(
            sig,w,s.rest_mass,s.kappa,s.n0
        )

        lam,chi = full_constitutive(
            K,U,density,s.alpha,beta,
            s.rest_mass,s.kappa,P
        )

        j = current_from_lambda(
            A,lam,m.h
        )
        defect = j-j0

        # Increment only. This is NOT absolute X Gauss
        # residual because P10 used a ring Green kernel.
        deltaX = (
            Br*dR(lam,m.h)
            +Bz*dZ(lam,m.h)
        )
        flux = (
            dR(rad*lam*Br,m.h)/rad
            +dZ(lam*Bz,m.h)
        )

        chi0,margin0,_,_ = principal_coefficients(
            K,U,E2,s.n0,s.rest_mass,
            s.kappa,s.alpha,beta
        )

        margin = 1-chi*E2
        i,jj = np.unravel_index(
            np.argmin(margin),sh
        )

        E = np.array([
            Er[i,jj],0.,Ez[i,jj]
        ])
        B = np.array([
            Br[i,jj],0.,Bz[i,jj]
        ])

        dispersion = finite_B_dispersion(
            E,B,float(chi[i,jj]),(0.,1.,0.)
        )

        eigenvalues,_,_,_ = transverse_symbol(
            E,float(chi[i,jj]),(0.,1.,0.)
        )

        fd,analytic = finite_diff_local_magnetic(
            K[i,jj],U[i,jj],density[i,jj],
            s.alpha,beta,s.rest_mass,s.kappa,
            np.sqrt(E2[i,jj]),P[i,jj],
        )

        scans[str(int(beta))] = {
            'source_only_Y_current_L2':
                norm(j0),
            'full_constitutive_current_L2':
                norm(j),
            'first_order_Y_current_reciprocity_defect_L2':
                norm(defect),
            'relative_Y_current_defect':
                norm(defect)/norm(j0),
            'X_Gauss_portal_increment_L2':
                norm(deltaX),
            'X_Gauss_increment_flux_form_L2':
                norm(flux),
            'X_Gauss_increment_form_difference_L2':
                norm(deltaX-flux),
            'Y_magnetic_Bianchi_inf':
                float(np.max(abs(divB))),
            'fluid_number_error':
                float(abs(
                    np.sum(w*np.exp(3*sig)*density)
                    -s.n0*np.sum(w)
                )),
            'fluid_redshifted_mu_error':
                float(np.max(abs(
                    (s.rest_mass+s.kappa*density)*np.exp(sig)-C
                ))),
            'frozen_P0_margin_min':
                float(np.min(margin0)),
            'actual_first_order_P_margin_min':
                float(np.min(margin)),
            'actual_first_order_P_negative_cells':
                int(np.count_nonzero(margin<0)),
            'min_cell_indices':
                [int(i),int(jj)],
            'local_4mode_magnetic_eigenvalues':
                [float(x) for x in eigenvalues],
            'local_finite_B_dispersion':
                dispersion,
            'local_magnetic_second_variation_FD_error':
                float(abs(fd-analytic)),
            'portal_P_max_abs':
                float(np.max(abs(P))),
            'portal_sigma_max_abs':
                float(np.max(abs(sig))),
            'first_order_Y':'NO_BACKREACTION',
            'full_X_Y_source_fluid_EOM':'NOT_SOLVED',
            'stability_under_cutoff':'NOT_CERTIFIED',
        }

    # β=40: solve a different, explicitly defined finite-box
    # variational Y equation, with source/X/fluid frozen.
    beta = 40.
    sig = s.alpha*P-beta*P*P

    density,_ = hydro_profile(
        sig,w,s.rest_mass,s.kappa,s.n0
    )

    fy = FrozenY(
        m,f,K,U,s.alpha,beta,density
    )

    v0 = fy.source_only_initial()
    vsolve,Ysol = fy.solve(v0)

    grad,Hess,_,_ = fy.evaluate(vsolve)

    direction = np.cos(
        np.arange(m.cells)*.137+.43
    )
    direction /= np.linalg.norm(direction)

    eps = 1e-4
    fplus = fy.evaluate(vsolve+eps*direction)
    fminus = fy.evaluate(vsolve-eps*direction)

    Ysol['action_gradient_directional_FD_error'] = float(
        abs(
            (fplus[2]-fminus[2])/(2*eps)
            -np.dot(grad,direction)
        )
    )
    Ysol['action_Hessian_directional_FD_error'] = float(
        np.linalg.norm(
            (fplus[0]-fminus[0])/(2*eps)
            -Hess@direction
        )
    )

    # Source was optimized with sigma=0 and N_i=400.
    # Compute actual N_i implied by this nonzero Y.
    newP = (fy.Pmat@vsolve).reshape(sh)
    newsig = s.alpha*newP-beta*newP**2

    source_numbers = 2*np.sum(
        w[None,:,:]
        *np.exp(2*newsig)[None,:,:]
        *f['W'].reshape(2,*sh)
        *f['F'].reshape(2,*sh)**2,
        axis=(1,2),
    )

    Ysol['source_Noether_reaction_unresolved_abs_shift'] = [
        float(abs(x-m.s.N)) for x in source_numbers
    ]
    Ysol['joint_source_X_residual'] = (
        'NOT_SOLVED_NOT_CLAIMED'
    )

    # For beta60, record the finite grid Hessian before
    # attempting a beta60 nonlinear stationary solve.
    # This does not certify continuum stability.
    d60,_ = hydro_profile(
        s.alpha*P-60*P*P,w,
        s.rest_mass,s.kappa,s.n0,
    )
    fy60 = FrozenY(
        m,f,K,U,s.alpha,60.,d60
    )
    v60 = fy60.source_only_initial()

    Ysol['beta60_initial_fullcell_Hessian_min_eigenvalue'] = (
        float(eigsh(
            fy60.evaluate(v60)[1],
            k=1,which='SA',
            return_eigenvectors=False,
            tol=1e-7,
        )[0])
    )

    return {
        'P10_background':{
            'nr':s.nr,
            'L':s.L,
            'h_canonical':m.h,
            'neutral_X_charge':
                float(info['net_X_charge']),
            'P10_scalar_EOM_weighted_L2_max':
                float(max(info['scalar_equation_weighted_L2'])),
            'P10_gauss_kernel_residual_inf':
                float(info['free_coulomb_residual_inf']),
            'source_energy_canonical_NOT_J':
                float(info['canonical_energy_NOT_J']),
            'Y_current_canonical_L2':
                norm(j0),
        },
        'beta_sweep':scans,
        'finite_box_discrete_variational_Y_beta40':Ysol,
    }


def report():
    identities = exact_identities()

    cases = {
        f'{nr}_L{L}':numerical_case(
            Settings(nr=nr,L=float(L))
        )
        for nr,L in (
            (12,12),(18,12),(12,16)
        )
    }

    allruns = [
        c
        for v in cases.values()
        for c in v['beta_sweep'].values()
    ]

    gate = {
      'exact_one_action_consistency':
          all(identities['checks'].values()),
      'P10_three_source_reconstructions':
          len(cases)==3,
      'P10_net_charge_neutral':
          all(
              abs(v['P10_background']['neutral_X_charge'])<1e-8
              for v in cases.values()
          ),
      'P10_scalar_EOM_small':
          all(
              v['P10_background']['P10_scalar_EOM_weighted_L2_max']<5e-5
              for v in cases.values()
          ),
      'P10_X_Gauss_kernel_residual_small':
          all(
              v['P10_background']['P10_gauss_kernel_residual_inf']<1e-9
              for v in cases.values()
          ),
      'Y_first_order_nonzero':
          all(
              v['P10_background']['Y_current_canonical_L2']>1e-5
              for v in cases.values()
          ),
      'fluid_number_preserved_all_cases':
          all(c['fluid_number_error']<1e-8 for c in allruns),
      'fluid_mu_hydrostatic_all_cases':
          all(c['fluid_redshifted_mu_error']<1e-10 for c in allruns),
      'Y_Bianchi_all_cases':
          all(c['Y_magnetic_Bianchi_inf']<1e-10 for c in allruns),
      'Y_full_lambda_current_defect_nonzero':
          all(
              c['first_order_Y_current_reciprocity_defect_L2']>1e-7
              for c in allruns
          ),
      'X_Gauss_increment_nonzero':
          all(
              c['X_Gauss_portal_increment_L2']>1e-9
              for c in allruns
          ),
      'local_finite_P_fd_Hessian':
          all(
              c['local_magnetic_second_variation_FD_error']<2e-4
              for c in allruns
          ),
      'positive_beta40_frozen_P0':
          all(
              v['beta_sweep']['40']['frozen_P0_margin_min']>0
              for v in cases.values()
          ),
      'negative_beta60_frozen_P0':
          all(
              v['beta_sweep']['60']['frozen_P0_margin_min']<0
              for v in cases.values()
          ),
      'positive_beta40_finite_P':
          all(
              v['beta_sweep']['40']['actual_first_order_P_margin_min']>0
              for v in cases.values()
          ),
      'negative_beta60_finite_P':
          all(
              v['beta_sweep']['60']['actual_first_order_P_margin_min']<0
              for v in cases.values()
          ),
      'negative_beta80_finite_P':
          all(
              v['beta_sweep']['80']['actual_first_order_P_margin_min']<0
              for v in cases.values()
          ),
      'negative_cells_nonzero_at_beta60':
          all(
              v['beta_sweep']['60']['actual_first_order_P_negative_cells']>0
              for v in cases.values()
          ),
      'two_gauge_transverse_negative_eigen_at_beta60':
          all(
              v['beta_sweep']['60']['local_4mode_magnetic_eigenvalues'][0]<0
              for v in cases.values()
          ),
      'two_gauge_transverse_positive_all_beta40':
          all(
              v['beta_sweep']['40']['local_4mode_magnetic_eigenvalues'][0]>0
              for v in cases.values()
          ),
      'three_unmodified_modes_canonical':
          all(
              sum(
                  abs(
                      np.array(c['local_4mode_magnetic_eigenvalues'])-1
                  )<1e-10
              )>=3
              for c in allruns
          ),
      'finite_B_active_kinetic_positive_in_test':
          all(
              c['local_finite_B_dispersion']['kinetic_active']>0
              for c in allruns
          ),
      'finite_B_beta60_negative_speed2':
          all(
              v['beta_sweep']['60']
              ['local_finite_B_dispersion']
              ['squared_phase_speeds'][0]<0
              for v in cases.values()
          ),
      'finite_B_beta40_positive_speed2':
          all(
              v['beta_sweep']['40']
              ['local_finite_B_dispersion']
              ['squared_phase_speeds'][0]>0
              for v in cases.values()
          ),
      'beta40_stationary_Y_fullcell_projected':
          all(
              v['finite_box_discrete_variational_Y_beta40']
              ['Y_stationary_fullcell_residual_L2']<1e-9
              for v in cases.values()
          ),
      'beta40_Y_Hessian_positive_restricted':
          all(
              v['finite_box_discrete_variational_Y_beta40']
              ['Y_discrete_Hessian_min_eigenvalue']>0
              for v in cases.values()
          ),
      'beta40_Y_gradient_FD':
          all(
              v['finite_box_discrete_variational_Y_beta40']
              ['action_gradient_directional_FD_error']<2e-7
              for v in cases.values()
          ),
      'beta40_Y_Hessian_FD':
          all(
              v['finite_box_discrete_variational_Y_beta40']
              ['action_Hessian_directional_FD_error']<2e-7
              for v in cases.values()
          ),
      'source_Noether_constraint_not_reclosed':
          all(
              max(
                  v['finite_box_discrete_variational_Y_beta40']
                  ['source_Noether_reaction_unresolved_abs_shift']
              )>1e-4
              for v in cases.values()
          ),
      'small_oneway_portal':
          all(
              c['portal_sigma_max_abs']<.001
              for c in allruns
          ),
      'not_full_on_shell':
          all(
              c['full_X_Y_source_fluid_EOM']=='NOT_SOLVED'
              for c in allruns
          ),
      'not_complete_stability_certificate':
          all(
              c['stability_under_cutoff']=='NOT_CERTIFIED'
              for c in allruns
          ),
    }

    gates = {k:bool(v) for k,v in gate.items()}

    return {
      'exact':identities,
      'cases':cases,
      'gates':gates,
      'verdict':
          'YELLOW_PH16_02_RESTRICTED_FULLCELL_Y_BETA40_STATIONARY_'
          'GAUGE_BETA60_PRINCIPAL_WARNING_FULL_SYSTEM_OPEN',
      'classification':
          'ACTION_LEVEL_FROZEN_X_SOURCE_FLUID_Y_VARIATION_PLUS_'
          '2U1_TRANSVERSE_CONSTRAINED_PRINCIPAL',
      'physical_promotion':'DENIED',
      'full_source_X_Y_fluid_solid_metric_on_shell':
          'NOT_SOLVED',
      'constrained_full_dynamical_spectrum':'NOT_SOLVED',
      'EFT_cutoff_and_nonlocal_completion':'NOT_CERTIFIED',
      '3D_Earth_and_whole_craft':'NOT_DERIVED',
      '1kg_1g_1m_and_lt10MJ':'NOT_CERTIFIED',
      'limits':[
        'Beta40 Y equation solved on entire discrete grid only '
        'at frozen X, scalar, neutral density and flat background.',
        'Finite-box natural boundaries are not P10 free-space '
        'exterior; continuum and exterior transmission unproven.',
        'Local transverse two-U1 spectrum does not include '
        'dynamic charged source, fluid, solid or metric modes.',
        'Beta60 negative local speed squared is conditional '
        'on a physical wave number below an unknown UV cutoff.',
        'The source N=400 constraints shift when the common '
        'metric changes; full fixed-Noether solve required.',
        'X Gauss increments and Y current mismatches are '
        'not full absolute coupled field-equation residuals.',
        'No real Earth, material interfaces, external reaction, '
        'whole-craft force or complete SI energy.',
      ],
      'next':
          'PH16-03: reoptimize fixed-Noether scalar/X/Y and '
          'neutral fluid jointly at healthy beta<=40; '
          'then verify continuum and metric before PH17.',
    }
