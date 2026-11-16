"""PH15-P7: fixed-Noether, pointwise-Gauss, fixed-J coupled angular energy audit.

Hypothetical two-scalar/X-Maxwell fixed-Minkowski theory from PH15-P2/P5.
Static X fields are legitimate Maxwell initial data; Ampere is NOT an
initial constraint. A negative energy trial disproves local energetic
minimality of the TESTED source, not dynamical growth or universal no-go.
No full reciprocal Y, Einstein equations, spacecraft force or SI energy.
"""
from __future__ import annotations
import hashlib
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from scipy.linalg import eigh
from antigravity_research.agminer.hook17_ph15_p2p5_source import Source, Spec


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


class GeneralWinding(Source):
    def __init__(self, spec, winding):
        super().__init__(spec)
        if len(winding) != 2 or any(int(x) != x for x in winding):
            raise ValueError('Two integral windings required')
        self.spin = np.asarray(winding, dtype=int)

    def seed(self):
        out = []
        R2 = self.rho**2 + self.z**2
        for mass, n in zip(self.mass, self.spin):
            f = self.rho**abs(n)*np.exp(
                -R2/(2*(3.7 if n else 4.6)**2)
            )
            f *= math.sqrt(
                self.s.N*1.1/(2*mass*np.dot(self.w,f*f))
            )
            out.append(f)
        return np.asarray(out)


def neutral_weights(s, fld):
    M = fld['W']*fld['F']**2
    if np.min(fld['W']) <= 0 or np.min(M.sum(axis=0)) <= 0:
        raise ArithmeticError(
            'This control requires positive frequencies and densities'
        )
    den = M.sum(axis=0)
    return np.stack((M[1]/den,M[0]/den))


def envelopes(s, k):
    r,z = s.rho,s.z
    return np.asarray([
        (r/4)**k*np.exp(
            -.5*((r*r-R*R)/(5*R))**2-z*z/(2*wz*wz)
        )
        for R in (2.,4.,6.,9.)
        for wz in (2.,5.)
    ])


def q_density(s,fld,k,h):
    a = neutral_weights(s,fld)*h[None,:]
    ans = 0.
    for i in (0,1):
        f = fld['F'][i]
        ai = a[i]
        ff = f*f
        b = f*ai/2
        d = -f*ai**2/8

        ans += (
            .5*np.dot(s.w*b,s.L@b)
            + np.dot(s.w*d,s.L@f)
            + .5*k*k*np.dot(s.w*b*b,s.ang)
            + np.dot(s.w*(-1+3*ff)*ff*ff,ai*ai)
        )

    return float(ans)


def q_phase(s,fld,k,b):
    ans=0.
    for f in fld['F']:
        ans += .5*(
            np.dot(s.w*f*b,s.L@(f*b))
            -np.dot(s.w*f*b*b,s.L@f)
            +k*k*np.dot(s.w*f*f*b*b,s.ang)
        )
    return float(ans)


def q_cross(s,fld,k,h,b):
    a=neutral_weights(s,fld)*h[None,:]
    return float(k*sum(
        np.dot(
            s.w*fld['F'][i]**2*a[i]
            *(1 if i==0 else -1)
            *fld['V'][i]/s.rho,
            b
        )
        for i in (0,1)
    ))


def mode(s,fld,k):
    B=envelopes(s,k)
    n=len(B)

    AA=np.zeros((n,n))
    BB=np.zeros((n,n))
    AB=np.zeros((n,n))
    GA=np.zeros((n,n))
    GB=np.zeros((n,n))

    c=neutral_weights(s,fld)
    f=fld['F']

    for i in range(n):
        for j in range(n):
            AA[i,j]=.25*(
                q_density(s,fld,k,B[i]+B[j])
                -q_density(s,fld,k,B[i]-B[j])
            )
            BB[i,j]=.25*(
                q_phase(s,fld,k,B[i]+B[j])
                -q_phase(s,fld,k,B[i]-B[j])
            )
            AB[i,j]=.5*q_cross(s,fld,k,B[i],B[j])

            GA[i,j]=sum(
                np.dot(
                    s.w*f[m]**2*c[m]**2*B[i],
                    B[j]
                )
                for m in (0,1)
            )
            GB[i,j]=sum(
                np.dot(
                    s.w*f[m]**2*B[i],
                    B[j]
                )
                for m in (0,1)
            )

    Q=np.block([[AA,AB],[AB.T,BB]])
    G=np.block([
        [GA,np.zeros_like(GA)],
        [np.zeros_like(GB),GB]
    ])

    if np.linalg.cond(G)>1e14:
        raise ArithmeticError('Ill-conditioned modal Gram')

    ev,v=eigh(Q,G)
    de=eigh(AA,GA,eigvals_only=True)[0]
    pe=eigh(BB,GB,eigvals_only=True)[0]

    schur=(
        eigh(
            AA-AB@np.linalg.solve(BB,AB.T),
            GA,
            eigvals_only=True
        )[0]
        if pe>1e-10 else None
    )

    h=v[:n,0]@B
    b=v[n:,0]@B

    norm=max(
        np.max(abs(c*h[None,:])),
        np.max(abs(b))
    )
    h/=norm
    b/=norm

    Qa=q_density(s,fld,k,h)
    Qb=q_phase(s,fld,k,b)
    Qc=q_cross(s,fld,k,h,b)

    return {
        'k':k,
        'density_eigen':float(de),
        'phase_eigen':float(pe),
        'coupled_eigen':float(ev[0]),
        'schur_eigen':(
            float(schur) if schur is not None else None
        ),
        'Q_density':Qa,
        'Q_phase':Qb,
        'Q_cross':Qc,
        'Q_total':Qa+Qb+Qc,
        'H_symmetry':float(np.max(abs(Q-Q.T))),
        'eigen_residual':float(
            np.linalg.norm(
                Q@v[:,0]-ev[0]*(G@v[:,0])
            )
        ),
        'gram_condition':float(np.linalg.cond(G))
    },h,b


def direct_energy(s,fld,k,h,b,t,angles=48):
    if angles < 4*k+16:
        raise ValueError('Angular integration too coarse')

    a=neutral_weights(s,fld)*h[None,:]
    total=0.

    for phi in (2*np.pi/angles)*np.arange(angles):
        cp=math.cos(k*phi)
        sp=math.sin(k*phi)

        for i in (0,1):
            f=fld['F'][i]
            ai=a[i]
            fac=1+t*ai*cp

            if np.min(fac)<=0:
                raise ValueError('Negative density')

            eps=(1 if i==0 else -1)

            psi=(
                f*np.sqrt(fac)
                *np.exp(1j*eps*t*b*sp)
            )

            grad=float(
                np.vdot(
                    psi,
                    s.w*(s.L@psi)
                ).real
            )

            ang_amp=np.dot(
                s.w,
                (
                    f*t*k*ai*sp
                    /(2*np.sqrt(fac)*s.rho)
                )**2
            )

            ang_phase=np.dot(
                s.w,
                f*f*fac*(
                    fld['V'][i]
                    +eps*t*k*b*cp/s.rho
                )**2
            )

            ff=f*f*fac
            tim=np.dot(s.w,fld['W'][i]**2*ff)
            U=np.dot(
                s.w,
                s.mass[i]**2*ff
                -2*ff**2
                +2*ff**3
            )

            total+=(
                grad+ang_amp+ang_phase+tim+U
            )/angles

    return float(total)


def conserved(s,fld,k,h,b,t,angles=48):
    c=neutral_weights(s,fld)
    F=fld['F']
    W=fld['W']

    pre=2*np.sum(
        s.q[:,None]*W*F**2,
        axis=0
    )

    nums=np.zeros(2)
    J=0.
    diff=0.

    for phi in (2*np.pi/angles)*np.arange(angles):
        cs=math.cos(k*phi)

        density=F**2*(
            1+t*c*h[None,:]*cs
        )

        charge=2*np.sum(
            s.q[:,None]*W*density,
            axis=0
        )

        diff=max(
            diff,
            float(np.max(abs(charge-pre)))
        )

        nums += (
            2*np.sum(
                W*density*s.w[None,:],
                axis=1
            )/angles
        )

        for i in (0,1):
            theta_phi=(
                s.spin[i]
                +(1 if i==0 else -1)*t*k*b*cs
            )

            J+=(
                2*np.dot(
                    s.w*W[i]*density[i],
                    theta_phi
                )/angles
            )

    return {
        'N':nums.tolist(),
        'total_Jz_matter_canonical':float(J),
        'net_charge':float(np.dot(s.q,nums)),
        'max_pointwise_Gauss_delta':diff
    }


def portal():
    import sympy as sp

    p,a,b,K,U=sp.symbols(
        'P alpha beta K U',
        real=True
    )

    sig=a*p-b*p**2
    lm=-sp.exp(2*sig)*K-sp.exp(4*sig)*U

    l0=sp.expand(
        sp.diff(lm,p).subs(p,0)
    )
    l1=sp.expand(
        sp.diff(lm,p,2).subs(p,0)
    )

    assert sp.simplify(
        l0+2*a*(K+2*U)
    )==0

    assert sp.simplify(
        l1-4*b*(K+2*U)+4*a*a*(K+4*U)
    )==0

    return {
        'lambda0':str(l0),
        'dlambda_dP_0':str(l1),
        'leading_sigma':(
            'alpha*P with P=O(alpha) => O(alpha^2)'
        ),
        'beta_P_squared':(
            'subleading in far dipole field'
        ),
        'Earth_craft_force':'NOT_DERIVED'
    }


def examine(name,spec,wind,full_quadrature):
    s=GeneralWinding(spec,wind)
    src,fld=s.solve(300)

    if (
        max(src['scalar_EOM_weighted_L2'])>3e-4
        or src['Gauss_L2']>1e-8
        or src['Ampere_L2']>1e-8
        or abs(src['electric_charge'])>1e-8
        or src['optimizer']['scaled_gradient_inf']>2e-5
    ):
        raise ArithmeticError(
            name+': source field equations not sufficiently satisfied'
        )

    modes=[]

    for k in (1,2,3):
        m,h,b=mode(s,fld,k)

        if full_quadrature and k<=2:
            E0=direct_energy(
                s,fld,k,h,b,0
            )
            trials=[]

            for t in (.04,.08,.12):
                de=(
                    direct_energy(
                        s,fld,k,h,b,t
                    )-E0
                )

                c=conserved(
                    s,fld,k,h,b,t
                )

                c.update({
                    't':t,
                    'delta_E':de,
                    'Q_independent':de/t**2,
                    'Q_predicted':m['Q_total'],
                    'Q_difference':(
                        de/t**2-m['Q_total']
                    )
                })

                if (
                    abs(
                        c['max_pointwise_Gauss_delta']
                    )>1e-10
                    or max(
                        abs(
                            np.array(c['N'])-spec.N
                        )
                    )>1e-8
                    or abs(
                        c['total_Jz_matter_canonical']
                        -src['Jz']
                    )>1e-7
                ):
                    raise ArithmeticError(
                        name+': Noether/Gauss/J conservation failure'
                    )

                trials.append(c)

            m['independent_3D_angles']=trials

        modes.append(m)

    Y=s.first_order_Y(fld)

    return {
        'spec':vars(spec),
        'winding':list(wind),
        'energy_canonical_NOT_J':src['energy'],
        'Noether':src['Noether'],
        'net_charge':src['electric_charge'],
        'Jz':src['Jz'],
        'Gauss_L2':src['Gauss_L2'],
        'Ampere_L2':src['Ampere_L2'],
        'scalar_EOM_L2':src[
            'scalar_EOM_weighted_L2'
        ],
        'gradient_inf':src[
            'optimizer'
        ]['scaled_gradient_inf'],
        'angular_modes':modes,
        'Y_first_order':{
            'electric_source_norm':Y['Y_rho_L2'],
            'magnetic_source_norm':Y['Y_jphi_L2'],
            'axial_dipole_coefficient_NOT_FORCE':Y[
                'dipole_axis_sigma_alphaP_coefficient'
            ],
            'dipole_method_rel_err':Y[
                'dipole_identity_rel_error'
            ]
        }
    }


def run(root:Path,quick=False):
    cases=[
        ('old_asym24',Spec(n=24,mminus=1.08),(1,-1),True),
        ('old_asym36',Spec(n=36,mminus=1.08),(1,-1),True),
        ('old_asym48',Spec(n=48,mminus=1.08),(1,-1),False),

        ('spin_asym24',Spec(n=24,mminus=1.08),(2,-1),True),
        ('spin_asym36',Spec(n=36,mminus=1.08),(2,-1),True),
        ('spin_asym48',Spec(n=48,mminus=1.08),(2,-1),False),

        ('spin_asym36_L24',
         Spec(n=36,L=24.,mminus=1.08),(2,-1),False),

        ('spin_asym48_L32',
         Spec(n=48,L=32.,mminus=1.08),(2,-1),False),

        ('mirror_asym24',Spec(n=24,mminus=1.08),(1,-2),True),
        ('mirror_asym36',Spec(n=36,mminus=1.08),(1,-2),False),

        ('old_sym24',Spec(n=24),(1,-1),False),
        ('null_nonwind24',Spec(n=24),(0,0),False)
    ]

    if quick:
        cases=[
            cases[0],
            cases[3],
            cases[8]
        ]

    result={}

    for name,spec,wind,full in cases:
        res=examine(
            name,spec,wind,full
        )
        result[name]=res
        mm=res['angular_modes']

        print(
            'CASE',name,
            'E',round(res['energy_canonical_NOT_J'],6),
            'J',round(res['Jz'],6),
            'density_k1',round(mm[0]['density_eigen'],8),
            'mixed_k1',round(mm[0]['coupled_eigen'],8),
            'mixed_k2',round(mm[1]['coupled_eigen'],8),
            'mixed_k3',round(mm[2]['coupled_eigen'],8),
            'Y_rho',round(
                res['Y_first_order']['electric_source_norm'],6
            ),
            'Y_jphi',round(
                res['Y_first_order']['magnetic_source_norm'],6
            ),
            flush=True
        )

    for key in (
        'old_asym24',
        'spin_asym24',
        'mirror_asym24'
    ):
        mm=result[key]['angular_modes'][0]

        if (
            mm['coupled_eigen']>=0
            or any(
                x['delta_E']>=0
                for x in mm['independent_3D_angles']
            )
        ):
            raise AssertionError(
                'Failed key energetic falsifier: '+key
            )

    if (
        result['spin_asym24']['angular_modes'][0]['density_eigen']
        <=0
    ):
        raise AssertionError(
            'The phase-induced false-survivor contrast was lost'
        )

    srcpath=Path(__file__)
    parent=srcpath.with_name(
        'hook17_ph15_p2p5_source.py'
    )

    artifact={
        'branch':'PH15-P7-EXACT_GAUSS_NOETHER_J_AMPLITUDE_PHASE',
        'date_utc':datetime.now(timezone.utc).isoformat(),
        'source_SHA256':sha(srcpath),
        'parent_SHA256':sha(parent),
        'scope':(
            'FINITE_BOX_X_SECTOR_FROZEN_X_'
            'ADMISSIBLE_INITIAL_DATA'
        ),
        'mode_basis':(
            'EIGHT_AXIS_REGULAR_ENVELOPES_BY_TWO_CHANNELS; '
            'k=1,2,3'
        ),
        'portal':portal(),
        'cases':result,
        'full_constrained_dynamic_spectrum':'NOT_DERIVED',
        'reciprocal_X_Y_matter':'NOT_SOLVED',
        'free_space_exterior':'NOT_CERTIFIED',
        'physical_source':'NOT_IDENTIFIED',
        'complete_SI_energy':'NOT_AVAILABLE',
        'Earth_down_craft_up':'NOT_DERIVED',
        '006D_replaced':False,
        'M5V_status':'FROZEN'
    }

    stamp=datetime.now(
        timezone.utc
    ).strftime('%Y%m%dT%H%M%S%fZ')

    path=root/'results/data'/f'032h17_ph15_p7_{stamp}.json'

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open('x') as stream:
        json.dump(
            artifact,
            stream,
            indent=2,
            sort_keys=True,
            allow_nan=False
        )

    print('RESULT_PATH='+str(path))
    print('RESULT_SHA256='+sha(path))
    print('PH15_P7=PASS_SCOPED_FALSIFICATION')

    return artifact


if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1] not in ('quick','full'):
        raise SystemExit(
            'Usage: python module.py quick|full'
        )

    run(
        Path.cwd(),
        quick=(
            len(sys.argv)>1
            and sys.argv[1]=='quick'
        )
    )
