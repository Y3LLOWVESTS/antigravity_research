"""PH16-04: same-discrete-Routhian joint scalar, X, Y, frequency, neutral fluid.

Canonical hypothetical portal: sigma(P)=alpha P-beta P².

The physically required Einstein metric, Earth, solid, exterior transmission,
full stability, SI and UV completion remain entirely unsolved.

Free-space X/Y inverse ring kernels produce a stationary discrete quadratic
field action. Field gradients in P use a separate finite-cell operator,
differentiated exactly as part of this DEFINED lattice action.

Continuum compatibility of the mixed-kernel discretization remains OPEN.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import sympy as sp

from scipy import sparse, linalg
from scipy.optimize import minimize

from antigravity_research.agminer.hook17_ph15_p10_free_space import (
    CoulombSource, Spec,
)


def derivative_matrix(n,h):
    D=sparse.diags(
        [-np.ones(n-1)*.5/h,np.ones(n-1)*.5/h],
        [-1,1],shape=(n,n),format='lil'
    )
    D[0,0]=-1/h
    D[0,1]=1/h
    D[-1,-2]=-1/h
    D[-1,-1]=1/h
    return D.tocsr()


def hydro_profile(sigma,weights,m,k,n0):
    C=(
        k*n0*np.sum(weights)
        +m*np.sum(weights*np.exp(3*sigma))
    )/np.sum(weights*np.exp(2*sigma))

    n=(C*np.exp(-sigma)-m)/k

    if np.min(n)<=0:
        raise ArithmeticError(
            'Fluid vacuum boundary unsupported'
        )
    return n,C


@dataclass(frozen=True)
class Settings:
    nr:int=12
    L:float=12.0
    alpha:float=0.05
    beta:float=40.0
    n0:float=0.15
    mass:float=1.0
    kappa:float=0.5


class JointAction:
    def __init__(self,m,s:Settings):
        self.m=m
        self.s=s
        self.N=m.cells
        self.w=m.w
        self.q=m.q
        self.rootw=np.sqrt(self.w)

        self.Kx=self._inverse_ring(m.wkernel)
        self.Ky=self._inverse_ring(m.wmagkernel)

        self.Dr=sparse.kron(
            derivative_matrix(m.nr,m.h),
            sparse.eye(m.nz),
            format='csr'
        )
        self.Dz=sparse.kron(
            sparse.eye(m.nr),
            derivative_matrix(m.nz),
            format='csr'
        ) if False else sparse.kron(
            sparse.eye(m.nr),
            derivative_matrix(m.nz,m.h),
            format='csr'
        )

        self.BR=-self.Dz
        self.BZ=(
            sparse.diags(1/m.rho)
            @self.Dr
            @sparse.diags(m.rho)
        ).tocsr()

        self._prepare_scalar_edges()

    def _inverse_ring(self,G):
        # W G is symmetric. The reciprocal inverse is a
        # finite-source-cell Green quadratic field cost.
        S=(
            self.rootw[:,None]*G
        )/self.rootw[None,:]

        err=np.max(abs(S-S.T))
        if err>1e-9:
            raise RuntimeError(
                'Ring kernel violates weighted reciprocity'
            )

        C=linalg.cho_factor(
            (S+S.T)/2,
            check_finite=False
        )
        inverse=linalg.cho_solve(
            C,np.eye(self.N),check_finite=False
        )

        return (
            self.rootw[:,None]*inverse
        )*self.rootw[None,:]

    def _prepare_scalar_edges(self):
        mat=self.m.L.tocsr()
        w=self.w

        self.edge_i=[]
        self.edge_j=[]
        self.edge_c=[]

        for i in range(self.N):
            for k in range(
                mat.indptr[i],mat.indptr[i+1]
            ):
                j=mat.indices[k]
                if j>i and mat.data[k]<0:
                    self.edge_i.append(i)
                    self.edge_j.append(j)
                    self.edge_c.append(
                        -w[i]*mat.data[k]
                    )

        self.edge_i=np.asarray(
            self.edge_i,dtype=int
        )
        self.edge_j=np.asarray(
            self.edge_j,dtype=int
        )
        self.edge_c=np.asarray(self.edge_c)

        self.boundary=w*np.asarray(
            mat@np.ones(self.N)
        )

        if np.min(self.boundary)<-1e-8:
            raise ArithmeticError(
                'Negative boundary field energy'
            )

        self.boundary=np.maximum(
            self.boundary,0
        )

        r=np.cos(np.arange(self.N)*.123)
        lhs=float(np.dot(
            w*r,mat@r
        ))
        rhs=float(
            np.sum(
                self.edge_c*
                (r[self.edge_i]-r[self.edge_j])**2
            )
            +np.dot(self.boundary,r*r)
        )

        self.edge_identity=abs(lhs-rhs)

        if self.edge_identity>1e-7:
            raise ArithmeticError(
                'Scalar finite-volume edge decomposition failed'
            )

    def pack(self,F,A,y):
        return np.concatenate((
            F.ravel(),
            np.asarray(A).ravel(),
            np.asarray(y).ravel()
        ))

    def unpack(self,x):
        n=self.N
        return (
            x[:2*n].reshape(2,n),
            x[2*n:3*n],
            x[3*n:4*n]
        )

    def evaluate(self,x,details=False):
        F,A,Y=self.unpack(x)
        s=self.s
        w=self.w
        ncell=self.N

        Er=-self.Dr@A
        Ez=-self.Dz@A

        Br=self.BR@Y
        Bz=self.BZ@Y

        divB=(
            self.Dr@(self.m.rho*Br)
        )/self.m.rho+self.Dz@Bz

        curlE=self.Dr@Ez-self.Dz@Er

        P=Er*Br+Ez*Bz
        sigma=s.alpha*P-s.beta*P*P
        ds=s.alpha-2*s.beta*P

        e2=np.exp(2*sigma)
        e4=e2*e2

        n,C=hydro_profile(
            sigma.reshape(self.m.nr,self.m.nz),
            w.reshape(self.m.nr,self.m.nz),
            s.mass,s.kappa,s.n0
        )
        nlabel=n.ravel()*np.exp(3*sigma)

        f2=F*F
        I=f2@(w*e2)

        if np.min(I)<1e-7:
            raise ArithmeticError(
                'Degenerate charged scalar'
            )

        omega=(
            self.m.s.N/2
            +self.q*np.sum(
                f2*(w*e2*A)[None,:],
                axis=1
            )
        )/I

        W=omega[:,None]-self.q[:,None]*A[None,:]

        sourceN=2*np.sum(
            f2*W*(w*e2)[None,:],
            axis=1
        )

        # Scalar gradient decomposition from the same
        # exact finite-volume edge action.
        edge_u=self.edge_i
        edge_v=self.edge_j
        c=self.edge_c

        fc=F[:,edge_u]-F[:,edge_v]

        edge_coeff=(
            c*(e2[edge_u]+e2[edge_v])/2
        )

        grad_energy=(
            np.sum(edge_coeff[None,:]*fc**2)
            +np.sum(
                self.boundary[None,:]
                *e2[None,:]*f2
            )
        )

        grad_F=np.zeros_like(F)
        local_dsigma=np.zeros(ncell)

        for i in range(2):
            np.add.at(
                grad_F[i],
                edge_u,
                2*edge_coeff*fc[i]
            )
            np.add.at(
                grad_F[i],
                edge_v,
                -2*edge_coeff*fc[i]
            )

            grad_F[i]+=(
                2*self.boundary*e2*F[i]
            )

            half=c*fc[i]**2

            np.add.at(
                local_dsigma,
                edge_u,
                e2[edge_u]*half
            )
            np.add.at(
                local_dsigma,
                edge_v,
                e2[edge_v]*half
            )

            local_dsigma+=(
                2*self.boundary*e2*f2[i]
            )

        U=(
            np.sum(
                f2-2*f2**2+2*f2**3,
                axis=0
            )
            +self.m.s.g*f2[0]*f2[1]
        )

        e_potential=np.dot(
            w*e4,U
        )

        kinetic=-np.dot(
            w*e2,
            np.sum(W**2*f2,axis=0)
        )

        fluid=np.dot(
            w,
            s.mass*nlabel*np.exp(sigma)
            +0.5*s.kappa*nlabel**2
            *np.exp(-2*sigma)
        )

        ex=-.5*A@self.Kx@A
        ey=.5*Y@self.Ky@Y

        R=float(
            np.dot(
                omega,
                np.full(2,self.m.s.N)
            )
            +grad_energy
            +e_potential
            +kinetic
            +fluid
            +ex
            +ey
        )

        # Envelope derivatives: omega and nlabel satisfy
        # their fixed-number stationarity constraints.
        for i in range(2):
            der=(
                2*F[i]*
                (
                    1-4*f2[i]+6*f2[i]**2
                    +self.m.s.g*f2[1-i]
                )
            )

            grad_F[i]+=(
                w*e4*der
                -2*w*e2*W[i]**2*F[i]
            )

        local_dsigma+=(
            4*w*e4*U
            -2*w*e2*np.sum(W**2*f2,axis=0)
        )
        local_dsigma+=(
            w*(
                s.mass*nlabel*np.exp(sigma)
                -s.kappa*nlabel**2*np.exp(-2*sigma)
            )
        )

        lam=-local_dsigma*ds/w

        local_second=np.zeros(ncell)
        for i in range(2):
            edge_sq=c*fc[i]**2

            np.add.at(
                local_second,
                edge_u,
                2*e2[edge_u]*edge_sq
            )
            np.add.at(
                local_second,
                edge_v,
                2*e2[edge_v]*edge_sq
            )

            local_second+=(
                4*self.boundary*e2*f2[i]
            )

        local_second+=(
            16*w*e4*U
            -4*w*e2*np.sum(W**2*f2,axis=0)
        )
        local_second+=(
            w*(
                s.mass*nlabel*np.exp(sigma)
                +2*s.kappa*nlabel**2
                *np.exp(-2*sigma)
            )
        )

        chi=(
            -local_second*ds*ds
            +2*s.beta*local_dsigma
        )/w

        frozen_margin=(
            1-chi*(Er*Er+Ez*Ez)
        )

        gradP=-w*lam

        C_A=(
            -sparse.diags(Br)@self.Dr
            -sparse.diags(Bz)@self.Dz
        )

        C_Y=(
            sparse.diags(Er)@self.BR
            +sparse.diags(Ez)@self.BZ
        )

        grad_A=(
            -(self.Kx@A)
            +w*2*np.sum(
                self.q[:,None]
                *e2[None,:]*W*f2,
                axis=0
            )
            +C_A.T@gradP
        )

        grad_Y=(
            self.Ky@Y
            +C_Y.T@gradP
        )

        result=np.concatenate((
            grad_F.ravel(),
            np.asarray(grad_A).ravel(),
            np.asarray(grad_Y).ravel()
        ))

        if not details:
            return R,result

        return R,result,dict(
            omega=omega.tolist(),
            N=sourceN.tolist(),
            neutralN=float(np.dot(w,nlabel)),
            sigma_max=float(np.max(abs(sigma))),
            Pmax=float(np.max(abs(P))),
            F_grad_norm=float(np.linalg.norm(grad_F)),
            X_grad_norm=float(np.linalg.norm(grad_A)),
            Y_grad_norm=float(np.linalg.norm(grad_Y)),
            bare_X_Green_shift_due_to_portal_inf=float(
                np.max(abs(
                    A-self.m.wkernel@(
                        2*np.sum(
                            self.q[:,None]
                            *e2[None,:]*W*f2,
                            axis=0
                        )
                    )
                ))
            ),
            portal_X_variation_L2=float(
                np.linalg.norm(C_A.T@gradP)
            ),
            Y_source_norm=float(
                np.linalg.norm(C_Y.T@gradP)
            ),
            min_F=float(np.min(F)),
            min_n=float(np.min(n)),
            neutral_mu_res=float(np.ptp(
                (s.mass+s.kappa*n)
                *np.exp(sigma.reshape(n.shape))
            )),
            frozen_magnetic_margin_min=float(
                np.min(frozen_margin)
            ),
            frozen_negative_cells=int(
                np.count_nonzero(frozen_margin<0)
            ),
            X_Noether_charge=float(
                np.dot(self.q,sourceN)
            ),
            Y_norm=float(np.linalg.norm(Y)),
            discrete_mimetic_divB_inf=float(
                np.max(abs(divB))
            ),
            discrete_curlE_inf=float(
                np.max(abs(curlE))
            ),
            Routhian_NOT_J=R,
            edge_decomposition_error=self.edge_identity
        )

    def initialize(self,info,fields):
        F=fields['F']
        A=fields['A']

        x=self.pack(
            F,A,np.zeros(self.N)
        )

        R,g,d=self.evaluate(x,True)

        # First-order Y initializer from the same
        # discrete portal gradient.
        Y=linalg.solve(
            self.Ky,
            -g[3*self.N:],
            assume_a='pos',
            check_finite=False
        )

        return self.pack(F,A,Y)

    def precondition_Y(self,x):
        """Find a frozen-F/X Y stationary starting point.

        INITIALIZER ONLY, never a joint solution claim.
        """
        seed=x.copy()
        n=self.N

        def fun(y):
            ystate=seed.copy()
            ystate[3*n:]=y
            R,g=self.evaluate(ystate)
            return R,g[3*n:]

        opt=minimize(
            fun,
            seed[3*n:].copy(),
            jac=True,
            method='L-BFGS-B',
            options={
                'maxiter':250,
                'gtol':3e-8,
                'maxls':40,
                'maxcor':20,
                'ftol':0.
            }
        )

        seed[3*n:]=opt.x

        return seed,{
            'iterations':int(opt.nit),
            'success':bool(opt.success),
            'Y_only_gradient_L2':float(
                np.linalg.norm(opt.jac)
            )
        }

    def solve(self,x,maxiter=450):
        """Attempt complete F/X/Y lattice stationarity.

        All F, X and Y variables respond to one Routhian.
        The solver uses matrix-free Krylov root finding.
        Success is checked from the actual absolute gradient.
        """
        from scipy.optimize import root

        residual0=float(
            np.linalg.norm(self.evaluate(x)[1])
        )

        scale=np.tile(
            np.maximum(self.rootw,1.),
            4
        )

        def fun(z):
            return (
                self.evaluate(z/scale)[1]/scale
            )

        op=root(
            fun,
            x*scale,
            method='krylov',
            options={
                'fatol':1e-9,
                'maxiter':maxiter,
                'disp':False,
                'line_search':'armijo'
            }
        )

        # PH16_04R2_BOUNDED_ITERATE_CONTINUATION
        # If the 450-step Krylov solve stalls, resume the SAME
        # root problem from its last iterate, never from a reset.
        # Keep native success and the unscaled actual gradient
        # as independent, unchanged acceptance criteria.
        history = []
        candidate = op.x/scale
        actual_residual = float(np.linalg.norm(self.evaluate(candidate)[1]))
        history.append({
            'stage': 0,
            'maxiter': int(maxiter),
            'native_success': bool(op.success),
            'actual_gradient_L2': actual_residual,
            'reported_iterations': int(getattr(op, 'nit', -1)),
        })
        if maxiter >= 400 and not (op.success and actual_residual < 1e-6):
            for stage in (1, 2):
                old = actual_residual
                trial = root(fun, op.x, method='krylov', options={
                    'fatol': 1e-9,
                    'maxiter': 100,
                    'disp': False,
                    'line_search': 'armijo',
                })
                trial_residual = float(np.linalg.norm(
                    self.evaluate(trial.x/scale)[1]
                ))
                history.append({
                    'stage': stage,
                    'maxiter': 100,
                    'native_success': bool(trial.success),
                    'actual_gradient_L2': trial_residual,
                    'reported_iterations': int(getattr(trial, 'nit', -1)),
                })
                if not np.isfinite(trial_residual) or trial_residual >= old:
                    # Discard a worsening step; no fictitious convergence.
                    break
                op = trial
                actual_residual = trial_residual
                if op.success and actual_residual < 1e-6:
                    break

        xf=op.x/scale
        R,g,d=self.evaluate(xf,True)

        d.update(
            initial_residual_L2=residual0,
            final_residual_L2=float(
                np.linalg.norm(g)
            ),
            root_success=bool(op.success),
            root_message=str(op.message),
            root_nit=int(
                getattr(op,'nit',-1)
            ),
            ph16_04r2_bounded_continuation=history,
            ph16_04r2_native_success_unmodified=bool(op.success)
        )

        return xf,d


def exact_atlas():
    """Exact fixed-Noether and same-action identities."""
    P,a,b,omega,N,q,A,F,K,U,n,m,k=sp.symbols(
        'P alpha beta omega N q A F K U n m kappa',
        real=True
    )

    sig=a*P-b*P**2
    e2=sp.exp(2*sig)
    e4=sp.exp(4*sig)
    W=omega-q*A

    mat=(
        e2*(K-W**2*F**2)
        +e4*U
        +m*n*sp.exp(sig)
        +k*n**2*sp.exp(-2*sig)/2
    )

    R=omega*N+mat

    current=2*e2*W*F**2
    lam=-sp.diff(mat,P)
    nphys=n*sp.exp(-3*sig)

    e1,e2p=sp.symbols(
        'e1 e2p',real=True
    )
    B=sp.symbols('B',real=True)
    pq=e1*B

    tests={
      'sigma_prime':
          sp.simplify(
              sp.diff(sig,P)-(a-2*b*P)
          )==0,
      'omega_fixed_N':
          sp.simplify(
              sp.diff(R,omega)-(N-current)
          )==0,
      'source_X_current':
          sp.simplify(
              sp.diff(R,A)-q*current
          )==0,
      'portal_lambda_same_action':
          sp.simplify(
              sp.diff(R,P)+lam
          )==0,
      'portal_beta_zero_no_quadratic':
          sp.simplify(
              sig.subs(b,0)-a*P
          )==0,
      'portal_off_zero_derivative':
          sp.simplify(
              lam.subs({a:0,b:0})
          )==0,
      'local_mixed_A_P_reciprocal':
          sp.simplify(
              sp.diff(R,A,P)-sp.diff(R,P,A)
          )==0,
      'local_mixed_F_P_reciprocal':
          sp.simplify(
              sp.diff(R,F,P)-sp.diff(R,P,F)
          )==0,
      'neutral_label_conformal_weight':
          sp.simplify(
              sp.exp(3*sig)*nphys-n
          )==0,
      'neutral_hydrostatic_mu':
          sp.simplify(
              sp.diff(mat,n)
              -sp.exp(sig)*(m+k*nphys)
          )==0,
      'fixed_X_Y_P_zero_if_E_zero':
          sp.simplify(pq.subs(e1,0))==0,
      'local_U1_P_bilinearity':
          sp.simplify(
              sp.diff(pq,e1,B)-1
          )==0,
    }

    if not all(tests.values()):
        raise AssertionError(
            'Exact source/portal identities failed: '
            +str(tests)
        )

    return {
        name:bool(ok)
        for name,ok in tests.items()
    }


def independent_fd(obj,x,indices=None,h=1e-4):
    """Independent centered differences of the total Routhian."""
    if indices is None:
        n=obj.N
        indices=[
            0,
            n//2,
            2*n-1,
            2*n+n//2,
            3*n-1,
            3*n+n//3,
            4*n-1
        ]

    E,g=obj.evaluate(x)
    out=[]

    for idx in indices:
        xp=x.copy()
        xm=x.copy()
        xp[idx]+=h
        xm[idx]-=h

        fd=(
            obj.evaluate(xp)[0]
            -obj.evaluate(xm)[0]
        )/(2*h)

        out.append({
            'index':int(idx),
            'fd':float(fd),
            'gradient':float(g[idx]),
            'error':float(abs(fd-g[idx]))
        })

    return out


def case(s):
    """Two initializations of one defined lattice Routhian."""
    m=CoulombSource(
        Spec(nr=s.nr,L=s.L),
        self_order=8
    )

    p10,source=m.solve(350)
    obj=JointAction(m,s)

    x=obj.initialize(p10,source)
    initial_R,initial_g,initial_d=obj.evaluate(
        x,True
    )

    fds=independent_fd(obj,x)

    # Independent weak-field initialization.
    direct_x,direct=obj.solve(
        x,
        maxiter=450 if s.nr==12 else 80
    )

    # Y-preconditioned initialization.
    pre_seed,pre=obj.precondition_Y(x)

    pre_x,pre_solved=obj.solve(
        pre_seed,maxiter=450
    )

    differences={
      'Y_solution_distance_L2':float(
          np.linalg.norm(
              obj.unpack(direct_x)[2]
              -obj.unpack(pre_x)[2]
          )
      ),
      'Routhian_difference_NOT_energy':float(
          direct['Routhian_NOT_J']
          -pre_solved['Routhian_NOT_J']
      ),
      'both_reached_stationarity':bool(
          direct['final_residual_L2']<1e-6
          and pre_solved['final_residual_L2']<1e-6
      ),
      'same_lattice_action':True
    }

    return {
      'mesh':{
          'nr':s.nr,
          'L':s.L,
          'h':m.h
      },
      'P10':{
          'source_eom_max':float(
              max(p10['scalar_equation_weighted_L2'])
          ),
          'N':[
              float(v)
              for v in p10['individual_Noether']
          ],
          'source_energy_NOT_J':float(
              p10['canonical_energy_NOT_J']
          )
      },
      'initial':initial_d,
      'finite_difference':fds,
      'direct_weak_seed':direct,
      'Y_only_seed':pre,
      'Y_preconditioned_joint':pre_solved,
      'initialization_sensitivity':differences,
      'discrete_exterior':
          'RECIPROCAL_RING_GREENS_PLUS_MIMETIC_P_NOT_CONTINUUM_PROOF',
      'physical_earth_metric':'NOT_SOLVED'
    }


def report():
    # PH16_04R1_ISOLATED_MESH
    # Each case uses the identical scientific action and solver,
    # but gets its own interpreter, SciPy and BLAS process state.
    # No physical parameters, solver tolerances, or gates change.
    records = {}

    child_env = dict(os.environ)
    srcdir = str(Path(__file__).resolve().parents[2])

    child_env["PYTHONPATH"] = (
        srcdir
        + (
            os.pathsep + child_env["PYTHONPATH"]
            if child_env.get("PYTHONPATH")
            else ""
        )
    )

    child_env["OPENBLAS_NUM_THREADS"] = "1"
    child_env["OMP_NUM_THREADS"] = "1"
    child_env["VECLIB_MAXIMUM_THREADS"] = "1"

    for nr, L in ((12, 12), (18, 12), (12, 16)):
        print(
            f"PH16-04R1 isolated mesh START {nr}_L{L}",
            file=sys.stderr,
            flush=True,
        )

        child = subprocess.run(
            [
                sys.executable,
                "-m",
                "antigravity_research.ph16.ph16_04_joint_stationary",
                "--single-case",
                str(nr),
                str(L),
            ],
            env=child_env,
            capture_output=True,
            text=True,
            timeout=240,
            check=False,
        )

        if child.returncode != 0:
            raise RuntimeError(
                f"PH16-04R1 mesh {nr}_L{L} failed with "
                f"exit code {child.returncode}: "
                + child.stderr[-4000:]
            )

        try:
            record = json.loads(child.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"PH16-04R1 mesh {nr}_L{L} returned invalid JSON: "
                + child.stdout[-2000:]
            ) from exc

        if (
            record["mesh"]["nr"] != nr
            or record["mesh"]["L"] != float(L)
        ):
            raise RuntimeError("Isolated mesh identity mismatch.")

        records[f"{nr}_L{L}"] = record

        outcome = record["Y_preconditioned_joint"]

        print(
            f"PH16-04R1 mesh DONE {nr}_L{L} "
            f"residual={outcome['final_residual_L2']:.10g} "
            f"native_success={outcome['root_success']}",
            file=sys.stderr,
            flush=True,
        )

    exact=exact_atlas()

    sol=[
        r['Y_preconditioned_joint']
        for r in records.values()
    ]

    gates={
      'exact_action_identities':
          all(exact.values()),

      'three_independent_mesh_domain_reconstructions':
          len(records)==3,

      'protected_P10_seed_EOM':
          all(
              r['P10']['source_eom_max']<5e-5
              for r in records.values()
          ),

      'symmetric_positive_reciprocal_ring_operators':
          all(
              r['initial']['edge_decomposition_error']<1e-7
              for r in records.values()
          ),

      'independent_F_X_Y_finite_difference':
          all(
              max(z['error'] for z in r['finite_difference'])<5e-5
              for r in records.values()
          ),

      'initial_individual_Noether_fixed':
          all(
              max(abs(v-400) for v in r['initial']['N'])<1e-8
              for r in records.values()
          ),

      'postsolve_individual_Noether_fixed':
          all(
              max(abs(v-400) for v in c['N'])<1e-8
              for c in sol
          ),

      'neutral_integrated_number_conserved':
          all(
              abs(c['neutralN']-r['initial']['neutralN'])<1e-7
              for c,r in zip(
                  sol,records.values()
              )
          ),

      'neutral_hydrostatic_chemical_balance':
          all(
              c['neutral_mu_res']<1e-10
              for c in sol
          ),

      'finite_Y_nonzero':
          all(
              c['Y_norm']>1e-5
              for c in sol
          ),

      'joint_F_X_Y_residual_small':
          all(
              c['final_residual_L2']<1e-6
              for c in sol
          ),

      'joint_F_X_Y_individual_residual_small':
          all(
              max(
                  c['F_grad_norm'],
                  c['X_grad_norm'],
                  c['Y_grad_norm']
              )<1e-6
              for c in sol
          ),

      'joint_solver_reported_convergence':
          all(
              c['root_success']
              for c in sol
          ),

      'mimetic_magnetic_Bianchi':
          all(
              c['discrete_mimetic_divB_inf']<1e-10
              for c in sol
          ),

      'mimetic_electric_curl_zero':
          all(
              c['discrete_curlE_inf']<1e-10
              for c in sol
          ),

      'frozen_beta40_magnetic_margin_positive':
          all(
              c['frozen_magnetic_margin_min']>0
              for c in sol
          ),

      'frozen_beta40_no_negative_cells':
          all(
              c['frozen_negative_cells']==0
              for c in sol
          ),

      'both_initializations_reported_without_uniqueness_claim':
          all(
              'Y_solution_distance_L2'
              in r['initialization_sensitivity']
              for r in records.values()
          ),

      'metric_force_not_claimed':
          all(
              r['physical_earth_metric']=='NOT_SOLVED'
              for r in records.values()
          ),
    }

    gates={
        name:bool(value)
        for name,value in gates.items()
    }

    return {
      'exact':exact,
      'cases':records,
      'gates':gates,
      'verdict':
          'YELLOW_PH16_04_JOINT_DISCRETE_SOURCE_X_Y_FLUID_SADDLE_TWO_SEEDS_METRIC_OPEN',
      'classification':
          'FINITE_LATTICE_SINGLE_ROUTHIAN_F_X_Y_OMEGA_NEUTRAL_HYDROSTATIC',
      'physical_promotion':'NO',
      'full_constrained_modes':'NOT_CERTIFIED',
      'Earth_down_craft_up':'NOT_DERIVED',
      '1kg_1g_1m':'NOT_CERTIFIED',
      'complete_SI_energy_lt10MJ':'NOT_CERTIFIED',
      'continuum_and_true_exterior':'NOT_CERTIFIED',
      'limits':[
        'Joint scalar F/X/Y stationary gradients tested in one defined finite lattice action, NOT Einstein dynamics',
        'Finite ring Greens and mimetic portal require independent continuum consistency and exterior verification',
        'Same-action F/X/Y/neutral hydrostatic Routhian excludes solid supports and full neutral dynamics',
        'Different initializers expose numerical basin sensitivity; uniqueness is not established',
        'Frozen magnetic principal coefficient positive is not a full dynamical stability certificate',
        'Canonical stationary Routhian is neither complete Hamiltonian nor joules nor derived external force',
      ],
      'next':
          'PH16-05: continuum/exterior operator consistency, basin and constrained Hessian; then source UV/material and Einstein Earth force'
    }


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "--single-case":
        nr = int(sys.argv[2])
        L = float(sys.argv[3])
        result = case(Settings(nr=nr, L=L))
        print(json.dumps(result, sort_keys=True, allow_nan=False))
    else:
        raise SystemExit(
            "Use --single-case nr L, or import report()"
        )
