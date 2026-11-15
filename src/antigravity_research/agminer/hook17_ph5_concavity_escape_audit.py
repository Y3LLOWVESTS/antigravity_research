"""HOOK17-PH5: parity, radial-force, and characteristic compatibility.

The PH1--PH4 action family uses two canonical U(1) fields, the invariant
P = E_X.B_Y + E_Y.B_X, and a universal conformal physical metric
    g_tilde = exp(2*sigma(P)) g.

For an IMMOBILE, UNIFORMLY PRESCRIBED positive dust density rho, the
local reduced Lagrangian is L=Maxwell-rho*F(P), F=exp(sigma)>0. Its
material curvature is chi=rho*F''(P). PH4 derived the restricted two-
carrier characteristic cone: chi>0 gives a superluminal extraordinary
mode for nonzero backgrounds when kinetic/gradient coefficients pass;
chi<0 with K>0 and D_min>0 gives the all-normal subluminal control.

PH5 establishes a theorem connecting this cone to the static radial
sign, WITHOUT assuming a specific quadratic portal:

If F is C2, even, positive, and F''<=0 throughout [0,P] (or [P,0]),
then F'(0)=0 and P*F'(P)<=0. With an exterior ray P=A*r^-m,
    a_r/c^2 = m*P*F'(P)/(r*F(P)) <= 0.
Thus positive radial test-matter repulsion somewhere on this ray
requires F''>0 somewhere between zero and P. This does NOT prove an
unhealthy physical system: the intermediate curvature may occur only
in vacuum or be cured by dynamical material, UV, gravity, etc. It is a
scoped conditional obstruction to an everywhere-sub-luminal parity-even
pure-P frozen-dust completion with continuously occupied material.

PH5 also falsifies an overbroad no-go claim using an explicit parity-
ODD candidate sigma(P)=a*P-b*P^2 with a,b>0. For
    0<P<a/(2b), (a-2bP)^2<2b, rho>0,
this candidate has simultaneously a_r>0 and chi<0. It is globally
positive (F=exp(sigma)), but not globally concave. Parity/CP breaking,
source equilibrium, Earth coupling, full mode health, naturalness,
confinement, and complete energy are entirely unknown.

This experiment makes NO physical spacecraft-lift claim, NO new field
capacity claim, and does not replace 006D or reopen frozen ALPHA-1.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import math

import numpy as np
import sympy as sp

BRANCH = '032H17A12D1R3X3B17-PH5'
ARCHIVES = {
    'm5v_source': ('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py', 'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
    'm5v_result': ('results/data/b17_m5v_unified_20261114T203555409373Z_full_bundle.json', '53f63f93fe9f525302f516b6376fa227d4b46027e6a0f75ae4dd35404da8c52b'),
    'ph4_source': ('src/antigravity_research/agminer/hook17_ph4_full_cone_sign_gate.py', '24328b6f6f67207d9fd868be7e6b1c78118812d3c68de83cea7bead0b423a810'),
    'ph4_result': ('results/data/032h17_ph4_full_cone_sign_20261115T003656120100Z.json', '4411f476fa4d21b1261f105a4ba2c955efd5cc8d61573facdbb7a7c86c0c14f8'),
}


@dataclass(frozen=True)
class Trial:
    name: str
    law: str
    a: float
    b: float
    rho: float
    ex: tuple[float,float,float] = (0.,0.,.35)
    ey: tuple[float,float,float] = (0.,0.,0.)
    bx: tuple[float,float,float] = (0.,0.,0.)
    by: tuple[float,float,float] = (0.,0.,.8)


def sigma_derivatives(law: str, a: float, b: float, p: float):
    if law == 'mixed_odd':
        return a*p-b*p*p, a-2*b*p, -2*b
    if law == 'negative_even':
        return -b*p*p, -2*b*p, -2*b
    if law == 'positive_even':
        return b*p*p, 2*b*p, 2*b
    if law == 'linear':
        return a*p, a, 0.
    raise ValueError('Unknown portal function')


def evaluate(t: Trial, exponent: float = 6.0, radius: float = 1.0):
    """Physical test-mass sign and *restricted* full-angle cone at one P."""
    nums=(t.a,t.b,t.rho,exponent,radius)
    if not all(math.isfinite(x) for x in nums) or min(t.a,t.b,t.rho)<0 or exponent<=0 or radius<=0:
        raise ValueError('Finite nonnegative coefficients, positive radius/power')
    E1,E2,B1,B2=(np.asarray(x,dtype=float) for x in (t.ex,t.ey,t.bx,t.by))
    if any(v.shape!=(3,) or not np.all(np.isfinite(v)) for v in (E1,E2,B1,B2)):
        raise ValueError('Finite three-component carrier backgrounds required')
    p=float(E1@B2+E2@B1)
    s,s1,s2=sigma_derivatives(t.law,t.a,t.b,p)
    try: F=math.exp(s)
    except OverflowError as exc: raise ValueError('Conformal factor overflows') from exc
    if not math.isfinite(F) or F<=0: raise ValueError('Invalid conformal factor')
    chi=t.rho*F*(s2+s1*s1)
    electric2=float(E1@E1+E2@E2)
    magnetic2=float(B1@B1+B2@B2)
    R=sum((np.outer(v,v) for v in (E1,E2,B1,B2)), np.zeros((3,3)))
    eigen=np.linalg.eigvalsh(R)
    K=1-chi*magnetic2
    Dmin=1+chi*(electric2-(eigen[0] if chi<=0 else eigen[-1]))
    jac=1-4*p*s1
    radial_shape=exponent*p*s1/radius
    if not all(math.isfinite(v) for v in (chi,K,Dmin,jac,radial_shape)):
        raise ValueError('Nonfinite result')
    if abs(jac)<=1e-12: cone='RED_METRIC_JACOBIAN'
    elif K<=0: cone='RED_KINETIC'
    elif Dmin<=0: cone='RED_GRADIENT'
    elif chi>0 and electric2+magnetic2>0: cone='RED_SUPERLUMINAL_SCOPED'
    elif chi<0 and electric2+magnetic2>0: cone='PASS_SUBLUMINAL_SCOPED'
    else: cone='LUMINAL_SCOPED'
    return {
        'name':t.name,'law':t.law,'P':p,'sigma':s,'sigma_prime':s1,
        'F':F,'F_prime':F*s1,'F_double_prime':F*(s2+s1*s1),
        'chi':chi,'K':K,'Dmin':Dmin,'conformal_trace_jacobian':jac,
        'a_radial_over_c_squared_shape_units':radial_shape,
        'outward_test_matter':radial_shape>0,'cone_gate':cone,
        'source_and_matter_self_consistent':False,
    }


def exact_theorems():
    p,a,b,r,m,cc=sp.symbols('p a b r m cc', positive=True)
    Fm=sp.exp(a*p-b*p*p)
    d1=sp.diff(Fm,p)
    d2=sp.diff(Fm,p,2)
    assert sp.simplify(d1/Fm-(a-2*b*p))==0
    assert sp.simplify(d2/Fm-((a-2*b*p)**2-2*b))==0
    P=sp.symbols('A',positive=True)/r**m
    sig=a*P-b*P**2
    ar=-cc**2*sp.diff(sig,r)
    assert sp.simplify(ar-cc**2*m*P*(a-2*b*P)/r)==0
    even_neg=sp.exp(-b*p*p)
    even_pos=sp.exp(b*p*p)
    assert sp.diff(even_neg,p).subs(p,0)==0
    assert sp.diff(even_pos,p).subs(p,0)==0
    assert sp.diff(even_neg,p,2).subs(p,0)==-2*b
    assert sp.diff(even_pos,p,2).subs(p,0)==2*b
    assert sp.simplify(1-4*p*(a-2*b*p)-(1-4*a*p+8*b*p*p))==0
    # For an arbitrary positive even C2 F, F'(P)=integral_0^P F''(q)dq.
    q=sp.symbols('q', real=True)
    G=sp.Function('G')
    identity=sp.Integral(sp.diff(G(q),q,2),(q,0,p))
    assert sp.simplify(identity.doit()-(sp.diff(G(p),p)-sp.diff(G(q),q).subs(q,0)))==0
    # A positive globally concave C1 function on the whole real line
    # cannot have any nonzero slope: the tangent line would become negative
    # in one direction. This is a mathematical statement, not a UV claim.
    return {'exact_symbolic_identities':10,
            'even_concavity_theorem':'F even, F>0, F_double_prime<=0 on [0,P] => P*F_prime(P)<=0 => a_r<=0',
            'repulsion_mvt':'P*F_prime(P)>0 with F_prime(0)=0 => exists q between 0,P with F_double_prime(q)>0',
            'global_positive_concavity':'Positive, globally concave F:R->(0,infinity) must be constant',
            'parity_odd_escaper':'sigma=a*P-b*P^2; a>0,b>0, 0<P<a/(2b), (a-2bP)^2<2b',
            'farfield_decay':'mixed odd a_r~+m*c^2*a*A/r^(m+1), even a_r~r^(-2m-1)',
            'physical_Earth_coverage':'NOT_ESTABLISHED'}


def independent_six_determinant(t:Trial, n:np.ndarray,s:float):
    """Rebuild the unprojected 6x6 symbol; compare rank-one factorization."""
    n=np.asarray(n,dtype=float)
    if n.shape!=(3,) or not np.all(np.isfinite(n)) or np.linalg.norm(n)==0 or not math.isfinite(s):
        raise ValueError('Finite nonzero normal and frequency required')
    n=n/np.linalg.norm(n)
    E1,E2,B1,B2=(np.asarray(x,dtype=float) for x in (t.ex,t.ey,t.bx,t.by))
    chi=evaluate(t)['chi']
    vec=np.r_[B2,B1]
    c=np.r_[np.cross(E2,n),np.cross(E1,n)]
    longitudinal=np.r_[n*(B2@n),n*(B1@n)]
    transverse=vec-longitudinal
    A=1-chi*(vec@vec)
    C=chi*(transverse@c)
    D=1-chi*(longitudinal@longitudinal)+chi*(c@c)
    Q=np.eye(3)-np.outer(n,n)
    M=np.eye(6)*s*s
    M[:3,:3]-=Q;M[3:,3:]-=Q
    M-=chi*np.outer(s*vec+c,s*vec+c)
    det=float(np.linalg.det(M))
    expected=float(s**4*(s*s-1)**3*(A*s*s-2*C*s-D))
    return abs(det-expected)/max(1,abs(det),abs(expected))


def finite_difference_radial(t:Trial, radius=2., exponent=6., p_at_radius=.28):
    """Differentiate a prescribed ray P=A/r^m; geometry only."""
    if min(radius,exponent,p_at_radius)<=0: raise ValueError('Positive geometry values required')
    A=p_at_radius*radius**exponent
    def sig_at(r):
        return sigma_derivatives(t.law,t.a,t.b,A/r**exponent)[0]
    h=radius*1e-5
    finite=-(sig_at(radius+h)-sig_at(radius-h))/(2*h)
    p=A/radius**exponent
    analytical=exponent*p*sigma_derivatives(t.law,t.a,t.b,p)[1]/radius
    return {'finite_difference_a_over_c2':finite,'exact_a_over_c2':analytical,
            'absolute_error':abs(finite-analytical),'r':radius,'P':p}


def prescribed_cases():
    return [
        Trial('even_concave_inward','negative_even',0.,.4,.35),
        Trial('even_convex_outward','positive_even',0.,.4,.35),
        Trial('odd_concave_outward','mixed_odd',.3,.4,.35),
        Trial('odd_convex_at_high_P','mixed_odd',.3,.4,.35,ex=(0.,0.,1.2),by=(0.,0.,1.4)),
        Trial('linear_outward_unsafe','linear',.3,0.,.35),
        Trial('odd_background_matter_off','mixed_odd',.3,.4,0.),
        Trial('odd_no_carrier_fields','mixed_odd',.3,.4,.35,ex=(0.,0.,0.),by=(0.,0.,0.)),
        Trial('odd_high_density_gradient_failure','mixed_odd',.3,2.0,8.,ex=(0.,0.,.35),by=(0.,0.,.8)),
    ]


def archival(root:Path):
    result={}
    for name,(relative,expected) in ARCHIVES.items():
        path=root/relative
        if not path.is_file():
            result[name]={'status':'MISSING'}
        else:
            actual=sha256(path.read_bytes()).hexdigest()
            result[name]={'status':'MATCH' if expected is None or expected==actual else 'MISMATCH', 'sha256':actual,
                          'sha_fingerprint_recorded':expected is not None}
    return result


def run(root:Path):
    theorems=exact_theorems()
    rows={x.name:evaluate(x) for x in prescribed_cases()}
    assert rows['even_concave_inward']['cone_gate']=='PASS_SUBLUMINAL_SCOPED'
    assert not rows['even_concave_inward']['outward_test_matter']
    assert rows['even_convex_outward']['cone_gate']=='RED_SUPERLUMINAL_SCOPED'
    assert rows['even_convex_outward']['outward_test_matter']
    assert rows['odd_concave_outward']['cone_gate']=='PASS_SUBLUMINAL_SCOPED'
    assert rows['odd_concave_outward']['outward_test_matter']
    normals=(np.array([.31,.55,.77]),np.array([.9,-.25,.36]),np.array([0.,0.,1.]))
    determinants={x.name:[independent_six_determinant(x,n,s) for n in normals for s in (.39,.73,1.27)]
                  for x in (prescribed_cases()[0],prescribed_cases()[2],prescribed_cases()[3])}
    assert all(max(errors)<1e-11 for errors in determinants.values())
    radial={x.name:finite_difference_radial(x) for x in prescribed_cases()[:3]}
    assert all(v['absolute_error']<1e-9 for v in radial.values())
    history=archival(root)
    ok=all(r['status']=='MATCH' for r in history.values())
    return {'branch':BRANCH,'frozen_alpha1':'M5V_UNTOUCHED','source_provenance':history,
            'symbolic_theorems':theorems,'eight_pre_registered_cases':rows,
            'independent_full_6x6_determinant_residuals':determinants,
            'independent_radial_derivative_controls':radial,
            'gates':{
                'PH5_P0_HISTORY':'PASS_SCOPED' if ok else 'UNRESOLVED',
                'PH5_P1_EVEN_CONCAVITY_REPULSION_THEOREM':'PASS_SCOPED_WITH_MATERIAL_COVERAGE_ASSUMPTION',
                'PH5_P1_MIXED_ODD_LOCAL_CAUSAL_REPULSION':'PASS_SCOPED_KINEMATIC_COUNTEREXAMPLE_ONLY',
                'PH5_P1_GLOBAL_CAUSAL_UV_COMPLETION':'NOT_ESTABLISHED',
                'PH5_P2_PARITY_CP_EMPIRICAL_PROTECTION':'NOT_ESTABLISHED',
                'PH5_P2_MICROSCOPIC_SOURCE_EOM':'NOT_SOLVED',
                'PH5_P2_FULL_CONSTRAINED_MODES':'NOT_DERIVED',
                'PH5_P3_NEUTRAL_1G_AT_1M':'NOT_CERTIFIED',
                'PH5_P3_EARTH_DOWN_CRAFT_UP':'NOT_DERIVED',
                'PH5_B11_M6_COMPLETE_CAUSAL_IMPULSE':'NOT_RUN',
                'PH5_COMPLETE_LT10MJ':'NOT_CERTIFIED',
                'PH5_006D_REPLACED':'NO'},
            'verdict':'YELLOW_PARITY_ODD_LOCAL_COMPATIBILITY_NOT_PHYSICAL_MODEL'}
