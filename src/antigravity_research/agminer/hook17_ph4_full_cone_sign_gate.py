"""HOOK17-PH4: exact all-angle frozen-matter cone and far-field sign audit.

SCIENTIFIC QUESTION
-------------------
Can the PH3 parity-even mixed pseudoscalar conformal portal preserve both
local causal propagation and outward static finite-neutral test-matter
acceleration? Answer only within the defined homogeneous frozen-density
Maxwell two-carrier background and conditional dipolar exterior.

MODEL AND CONVENTIONS
---------------------
Metric (-,+,+,+), c=1 in the characteristic sector.
P=E_X dot B_Y + E_Y dot B_X (R3X1 orientation; sign absorbed into
coupling). Canonical Maxwell two-carrier L plus locally prescribed dust:
    L=0.5*(E_X²+E_Y²-B_X²-B_Y²)-rho*exp(sigma(P))
with sigma=kappa*P, sigma=-lambda*P², or sigma=+lambda*P².

For a constant background, F''(P)=chi=rho*exp(sigma)*
(sigma''+sigma'^2). Fixed coefficient F' multiplies a topological
mixed F_X wedge F_Y term and drops from the bulk principal symbol.
For spatial unit normal n, define six-vectors
    b=(B_Y,B_X), c=(E_Y cross n,E_X cross n),
    b_parallel=(n(n dot B_Y),n(n dot B_X)),
    b_transverse=b-b_parallel.
The temporal-gauge six-component principal matrix is
    M(s)=s²*I - diag(I-nnT,I-nnT)
         -chi*(s*b+c)(s*b+c)T, s=omega/k.
The determinant factorizes as
    det M=s^4*(s²-1)^3*(A*s²-2*C*s-D)
    A=1-chi*|b|²
    C=chi*b_transverse dot c
    D=1-chi*|b_parallel|²+chi*|c|².
The s=0 factors are temporal-gauge longitudinal constraints, NOT
propagating massless modes. Three unchanged physical branches remain
luminal and a fourth has the extraordinary roots.

For all normals, D(n)=1+chi*(|E|²-nT R n), where
R=sum_fields outer(field,field). Thus Dmin is given exactly by
an eigenvalue of this 3x3 symmetric matrix, without angle sampling.
For A>0 and Dmin>0: chi<0 implies all extraordinary roots lie
within [-1,1] for every normal. chi>0 and nonzero fields implies
superluminal roots in at least some normals. These are *frozen-dust*
wavefront checks, not full dynamical source/matter/gravity causality.

For an isolated dipolar far field P=A0/r^6 with A0 != 0, a neutral
static test body has a_r=-c²*d sigma/dr. Negative quadratic sigma
therefore gives -12*c²*lambda*A0²/r^13 (attraction to source);
positive quadratic gives +12*c²*lambda*A0²/r^13 (outward), but
its weak-field frozen-dust chi is positive for rho>0. These are
conditional far-field sign tests, not complete Earth/craft forces.

NO CERTIFICATION
----------------
The model has prescribed dust and carrier backgrounds, no microscopic
source equilibrium or supporting matter, no dynamical metric/gravity,
no universal Earth material EOS, no full B11-M6 pulse, no finite 1g/1m
loaded benchmark or whole-craft lift, and no certified <10MJ budget.
006D is unreplaced; M5V is frozen and never optimized here.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import math

import numpy as np
import sympy as sp

BRANCH = '032H17A12D1R3X3B17-PH4'
PROVENANCE = {
    'm5v_source': ('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py', 'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
    'm5v_result': ('results/data/b17_m5v_unified_20261114T203555409373Z_full_bundle.json', '53f63f93fe9f525302f516b6376fa227d4b46027e6a0f75ae4dd35404da8c52b'),
    'ph2_source': ('src/antigravity_research/agminer/hook17_ph2_source_causal_audit.py', 'b3747d1f2d5f094721e068fce06c2331eb5400a4485777604cfdb53a8de723d5'),
    'ph3_source': ('src/antigravity_research/agminer/hook17_ph3_causal_portal_gate.py', '7cb085be26aa69de6d8ca3e277fb8752c09ee50fb8d0f420d2f7eb539bb63285'),
    'ph3_result': ('results/data/032h17_ph3_causal_portal_20261115T001750156882Z.json', 'd9c76418fd8babb8d4d2788d10fb91367544982aa7846ffc002cf6cd742b4eda'),
}

@dataclass(frozen=True)
class Case:
    label: str
    law: str
    rho: float
    coupling: float
    ex: tuple[float,float,float]
    ey: tuple[float,float,float]
    bx: tuple[float,float,float]
    by: tuple[float,float,float]


def fields(case: Case):
    arrays = [np.asarray(getattr(case, name),dtype=float) for name in ('ex','ey','bx','by')]
    if any(a.shape!=(3,) or not np.all(np.isfinite(a)) for a in arrays):
        raise ValueError('Each field must be a finite 3-vector')
    if (not math.isfinite(case.rho) or not math.isfinite(case.coupling)
        or case.rho < 0 or case.coupling < 0):
        raise ValueError('rho and coupling must be finite and nonnegative')
    return arrays


def derivatives(law: str, coupling: float, p: float):
    if law == 'linear':
        return coupling*p, coupling, 0.0
    if law == 'even_negative':
        return -coupling*p*p, -2*coupling*p, -2*coupling
    if law == 'even_positive':
        return coupling*p*p, 2*coupling*p, 2*coupling
    raise ValueError('Unknown portal law')


def evaluate(case: Case) -> dict:
    ex,ey,bx,by = fields(case)
    p = float(ex@by+ey@bx)
    sigma,d1,d2 = derivatives(case.law, case.coupling, p)
    try:
        conformal = math.exp(sigma)
    except OverflowError as exc:
        raise ValueError('Uncontrolled conformal exponential') from exc
    if not math.isfinite(conformal) or conformal == 0:
        raise ValueError('Nonfinite/underflowed conformal factor')
    chi = case.rho*conformal*(d2+d1*d1)
    electric_sq = float(ex@ex+ey@ey)
    magnetic_sq = float(bx@bx+by@by)
    R = sum(np.outer(f,f) for f in (ex,ey,bx,by))
    eigenvalues = np.linalg.eigvalsh(R)
    A = 1-chi*magnetic_sq
    Dmin = 1+chi*(electric_sq-(eigenvalues[0] if chi<=0 else eigenvalues[-1]))
    Dmax = 1+chi*(electric_sq-(eigenvalues[-1] if chi<=0 else eigenvalues[0]))
    jac = 1-4*p*d1
    if not all(math.isfinite(float(x)) for x in (chi,A,Dmin,Dmax,jac)):
        raise ValueError('Nonfinite characteristic matrix')
    field_sq = electric_sq+magnetic_sq
    if abs(jac) <= 1e-12:
        verdict='RED_NONINVERTIBLE_METRIC_MAP_SCOPED'
    elif A<=0:
        verdict='RED_KINETIC_SCOPED'
    elif Dmin<=0:
        verdict='RED_GRADIENT_OR_HYPERBOLICITY_SCOPED'
    elif chi>0 and field_sq>0:
        verdict='RED_SUPERLUMINAL_EXISTS_EXACT_ALL_NORMALS_THEOREM'
    elif chi<0 and field_sq>0:
        verdict='PASS_SCOPED_ALL_NORMALS_SUBLUMINAL_FROZEN_DUST'
    else:
        verdict='PASS_SCOPED_LUMINAL_NO_COMPLETION'
    return {
        'case': asdict(case), 'P':p,'sigma':sigma,'sigma_prime':d1,
        'chi':chi,'A_kinetic':A,'D_min_all_normals':Dmin,
        'D_max_all_normals':Dmax,'background_R_eigenvalues':eigenvalues.tolist(),
        'conformal_trace_jacobian':jac, 'exact_all_normals_verdict':verdict,
        'full_matter_and_gravity_characteristics':'NOT_TESTED',
        'source_equilibrium':'NOT_DERIVED',
    }


def cone_roots(case: Case, normal: np.ndarray) -> dict:
    ex,ey,bx,by=fields(case)
    n=np.asarray(normal,dtype=float)
    if n.shape!=(3,) or not np.all(np.isfinite(n)) or np.linalg.norm(n)<1e-12:
        raise ValueError('Finite nonzero spatial normal required')
    n=n/np.linalg.norm(n)
    rec=evaluate(case)
    chi=rec['chi']
    b=np.r_[by,bx]
    c=np.r_[np.cross(ey,n),np.cross(ex,n)]
    bl=np.r_[n*(by@n), n*(bx@n)]
    bt=b-bl
    A=1-chi*(b@b)
    C=chi*(bt@c)
    D=1-chi*(bl@bl)+chi*(c@c)
    discriminant=C*C+A*D
    roots=None
    if A>0 and D>0 and discriminant>0:
        root=math.sqrt(discriminant)
        roots=[float((C-root)/A),float((C+root)/A)]
    return {'normal':n.tolist(),'A':float(A),'C':float(C),
            'D':float(D),'discriminant':float(discriminant),
            'extraordinary_phase_roots':roots}


def independent_six_by_six_determinant(case: Case, normal: np.ndarray, s: float) -> dict:
    """Independent 6x6 temporal-gauge determinant vs derived factorization."""
    if not math.isfinite(s) or abs(s)<1e-5 or abs(abs(s)-1)<1e-5:
        raise ValueError('Choose a nonsingular nonluminal trial frequency')
    ex,ey,bx,by=fields(case)
    n=np.asarray(normal,dtype=float)
    n=n/np.linalg.norm(n)
    rec=evaluate(case)
    chi=rec['chi']
    b=np.r_[by,bx]
    c=np.r_[np.cross(ey,n),np.cross(ex,n)]
    transverse=np.eye(3)-np.outer(n,n)
    block=np.zeros((6,6))
    block[:3,:3]=transverse
    block[3:,3:]=transverse
    v=s*b+c
    matrix=s*s*np.eye(6)-block-chi*np.outer(v,v)
    det=float(np.linalg.det(matrix))
    qr=cone_roots(case,n)
    expected=float(s**4*(s*s-1)**3*(qr['A']*s*s-2*qr['C']*s-qr['D']))
    error=abs(det-expected)/max(1.,abs(det),abs(expected))
    return {'numeric_determinant':det,'factored_determinant':expected,'relative_scaled_error':error}


def independent_full_lagrangian_second_variation(case:Case, normal:np.ndarray, s:float=1.23):
    """Finite-difference the actual full 3D L, NOT the factored symbol."""
    ex,ey,bx,by=fields(case)
    n=np.asarray(normal,dtype=float);n=n/np.linalg.norm(n)
    rec=evaluate(case)
    chi=rec['chi']
    trial=np.array([.12,-.23,.31,-.17,.07,.28],dtype=float)
    b=np.r_[by,bx]
    c=np.r_[np.cross(ey,n),np.cross(ex,n)]
    trans=np.eye(3)-np.outer(n,n)
    T=np.zeros((6,6));T[:3,:3]=trans;T[3:,3:]=trans
    v=s*b+c
    expected=float(trial@(s*s*np.eye(6)-T-chi*np.outer(v,v))@trial)
    def lag(t):
        dE1=s*t*trial[:3];dE2=s*t*trial[3:]
        dB1=t*np.cross(n,trial[:3]);dB2=t*np.cross(n,trial[3:])
        E1=ex+dE1; E2=ey+dE2; B1=bx+dB1;B2=by+dB2
        p=float(E1@B2+E2@B1)
        sigma,_,_=derivatives(case.law,case.coupling,p)
        return 0.5*(E1@E1+E2@E2-B1@B1-B2@B2)-case.rho*math.exp(sigma)
    h=.0015
    got=(lag(h)+lag(-h)-2*lag(0.))/(h*h)
    return {'full_L_second_difference':float(got),'analytical_symbol_quadratic':expected,'abs_error':float(abs(got-expected))}


def normals(count=128):
    if count<16:
        raise ValueError('Need at least 16 directional samples')
    axes=np.eye(3)
    values=[a for a in axes]+[-a for a in axes]
    golden=math.pi*(3-math.sqrt(5))
    for i in range(count):
        z=1-2*(i+.5)/count
        phi=i*golden
        t=math.sqrt(max(0,1-z*z))
        values.append(np.array([t*math.cos(phi),t*math.sin(phi),z]))
    return values


def directional_audit(case:Case,count=128):
    roots=[];D=[]
    for n in normals(count):
        item=cone_roots(case,n)
        D.append(item['D'])
        if item['extraordinary_phase_roots'] is not None:
            roots.extend(abs(x) for x in item['extraordinary_phase_roots'])
    rec=evaluate(case)
    return {'directions_tested':len(D),'smallest_sampled_D':min(D),
            'exact_min_D':rec['D_min_all_normals'],
            'max_abs_phase_speed_sampled':max(roots) if roots else None,
            'directional_sampling_is_proof':'NO_EXACT_MATRIX_EIGENVALUE_BOUND_IS_PROOF'}


def symbolic_and_farfield():
    r,amp,lam,cc,rho,p=sp.symbols('r amp lam cc rho p',positive=True)
    power=amp/r**6
    linear=-cc**2*sp.diff(lam*power,r)
    negative=-cc**2*sp.diff(-lam*power**2,r)
    positive=-cc**2*sp.diff(lam*power**2,r)
    assert sp.simplify(linear-6*cc**2*lam*amp/r**7)==0
    assert sp.simplify(negative+12*cc**2*lam*amp**2/r**13)==0
    assert sp.simplify(positive-12*cc**2*lam*amp**2/r**13)==0
    sigma=-lam*p**2
    chisp=sp.factor(sp.diff(sp.exp(sigma),p,2))
    assert sp.simplify(chisp-sp.exp(-lam*p*p)*(4*lam**2*p*p-2*lam))==0
    assert sp.simplify(1-4*p*sp.diff(sigma,p)-(1+8*lam*p*p))==0
    assert sp.diff(sigma,p).subs(p,0)==0
    # Full 3D characteristic factor at s=+/-1; exact causal sign theorem.
    s,chi,bt2,c2,btc,bl2=sp.symbols('s chi bt2 c2 btc bl2',real=True)
    A=1-chi*(bt2+bl2); C=chi*btc; D=1-chi*bl2+chi*c2
    F=A*s*s-2*C*s-D
    assert sp.simplify(F.subs(s,1)+chi*(bt2+2*btc+c2))==0
    assert sp.simplify(F.subs(s,-1)+chi*(bt2-2*btc+c2))==0
    return {'analytic_identities':8,
            'linear_farfield_signed_coefficient':'+6*c^2*kappa*A/r^7',
            'negative_even_farfield_signed_coefficient':'-12*c^2*lambda*A^2/r^13',
            'positive_even_farfield_signed_coefficient':'+12*c^2*lambda*A^2/r^13',
            'negative_even_chi_flip_at_abs_P':'1/sqrt(2*lambda)',
            'negative_even_conformal_jacobian':'1+8*lambda*P^2 > 0 for finite P',
            'zero_P_even_metric_force':'ZERO_TO_FIRST_ORDER',
            'dipole_at_r_over_r0_2_linear_accel_ratio':2**(-7),
            'dipole_at_r_over_r0_2_even_accel_ratio':2**(-13),
            'source_shape_and_1m_standoff':'NOT_MODELED'}


def cases():
    z=(0.,0.,0.); ez=(0.,0.,.35);bz=(0.,0.,.8)
    return [
      Case('linear_mixed','linear',.7,.45,ez,z,z,bz),
      Case('negative_even_mixed','even_negative',.35,.4,ez,z,z,bz),
      Case('positive_even_mixed','even_positive',.35,.4,ez,z,z,bz),
      Case('negative_even_large_P','even_negative',.35,.4,(0.,0.,1.2),z,z,(0.,0.,1.4)),
      Case('negative_even_gradient_failure','even_negative',1.,1.,(0.,0.,2.),z,z,(0.,0.,.1)),
      Case('negative_even_P_zero_nontrivial_fields','even_negative',.35,.4,ez,z,z,(.8,0.,0.)),
      Case('linear_no_matter','linear',0.,.45,ez,z,z,bz),
      Case('linear_no_coupling','linear',.7,0.,ez,z,z,bz),
      Case('linear_kinetic_failure','linear',2.,1.,(0.,0.,.15),z,z,(0.,0.,1.)),
      Case('negative_even_noncollinear','even_negative',.4,.4,(.24,.11,.35),(.1,-.14,.2),(.15,.04,-.11),(.13,.37,.22)),
      Case('linear_noncollinear','linear',.4,.4,(.24,.11,.35),(.1,-.14,.2),(.15,.04,-.11),(.13,.37,.22)),
      Case('zero_fields','even_negative',.4,.4,z,z,z,z),
    ]


def provenance(root:Path):
    result={}
    for key,(relative,expected) in PROVENANCE.items():
        path=root/relative
        if not path.is_file():
            result[key]={'status':'MISSING','expected':expected}
        else:
            got=sha256(path.read_bytes()).hexdigest()
            result[key]={'status':'MATCH' if got==expected else 'HASH_MISMATCH',
                         'actual':got,'expected':expected}
    return result


def run(root:Path):
    sym=symbolic_and_farfield()
    details={}
    for item in cases():
        entry=evaluate(item)
        entry['directions']=directional_audit(item,144)
        details[item.label]=entry
    assert details['linear_mixed']['exact_all_normals_verdict'].startswith('RED_SUPERLUMINAL')
    assert details['negative_even_mixed']['exact_all_normals_verdict'].startswith('PASS_SCOPED_ALL_NORMALS_SUBLUMINAL')
    assert details['positive_even_mixed']['exact_all_normals_verdict'].startswith('RED_SUPERLUMINAL')
    assert details['negative_even_large_P']['chi']>0
    assert details['negative_even_gradient_failure']['D_min_all_normals']<0
    checks={}
    for item in (cases()[1],cases()[9],cases()[10]):
        n=np.array([.37,-.52,.77]);n=n/np.linalg.norm(n)
        checks[item.label]={
           'determinants':[independent_six_by_six_determinant(item,n,s) for s in (.39,.73,1.27,-1.31)],
           'full_action_second_variation':independent_full_lagrangian_second_variation(item,n),
        }
        assert max(x['relative_scaled_error'] for x in checks[item.label]['determinants'])<1e-9
        assert checks[item.label]['full_action_second_variation']['abs_error']<3e-6
    hist=provenance(root)
    ok=all(entry['status']=='MATCH' for entry in hist.values())
    return {'branch':BRANCH,'frozen_reference':'ALPHA1_B17_M5V_NOT_REOPTIMIZED',
       'historical_provenance':hist,'exact_analytic_controls':sym,
       'pre_registered_12_cases':details,'independent_six_by_six_and_action_checks':checks,
       'gates':{
         'PH4_P0_PROVENANCE':'PASS' if ok else 'UNRESOLVED',
         'PH4_P1_ALL_3D_FROZEN_DUST_CHARACTERISTICS':'PASS_SCOPED_EXACT_CONE_THEOREM',
         'PH4_P1_NEGATIVE_QUADRATIC_CAUSAL_WINDOW':'CONDITIONAL_STRONG_FIELD_SIGN_FLIP',
         'PH4_P2_NEGATIVE_QUADRATIC_DIPOLE_REPULSION':'RED_WRONG_FARFIELD_SIGN_SCOPED',
         'PH4_P2_POSITIVE_QUADRATIC_DIPOLE_REPULSION':'OUTWARD_SIGN_BUT_RED_RESTRICTED_CAUSALITY',
         'PH4_P2_EVEN_DIPOLE_FARFIELD_DECAY':'R_MINUS_13_CONDITIONAL',
         'PH4_P2_MICROSCOPIC_SOURCE_AND_CONFINEMENT':'NOT_DERIVED',
         'PH4_P3_FULL_MATERIAL_AND_GRAVITY_MODES':'NOT_DERIVED',
         'PH4_P3_FINITE_NEUTRAL_GE1G_GE1M':'NOT_CERTIFIED',
         'PH4_P3_EARTH_DOWN_FULL_CRAFT_UP':'NOT_DERIVED',
         'PH4_B11_M6_FULL_CAUSAL_LOADED_IMPULSE':'NOT_RUN',
         'PH4_STRICT_COMPLETE_LT10MJ':'NOT_CERTIFIED',
         'PH4_006D_REPLACED':'NO',
       },
       'verdict':'YELLOW_WITH_SCOPED_CAUSALITY_REPULSION_TENSION_NO_PHYSICAL_ENGINE'}
