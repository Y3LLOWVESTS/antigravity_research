"""Independent F0G: integrate exterior active stress against Green kernel.

Uses numerical radial multipoles instead of source closed-form f0/f2.
"""
import hashlib
import json
import math
import os
from pathlib import Path
from scipy.integrate import quad

RUN = Path(os.environ['F0G_RUN']).resolve()
s = json.loads((RUN/'science.json').read_bytes())
checks = {}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def check(name,value):
    checks[name] = bool(value)
    if not checks[name]:
        raise AssertionError(name)

def potential_dimensionless(rho,z):
    # rho,z measured in source-radius units, x>=1.
    x = math.hypot(rho,z)
    mu = z/x
    P2 = (3*mu*mu-1)/2
    total = 0.0

    for l,P in ((0,1.0),(2,P2)):
        left = quad(
            lambda t:t**(l-4),
            1,x,
            epsabs=2e-13
        )[0]
        right = quad(
            lambda t:t**(-l-5),
            x,math.inf,
            epsabs=2e-13
        )[0]
        total += (
            -6/(2*l+1)
            *(left/x**(l+1)+x**l*right)*P
        )

    return total

def finite_diff_az(rho,z,h=0.001):
    # 5-point derivative -dPhi/d(z/R)
    vals = [
        potential_dimensionless(rho,z+f*h)
        for f in (-2,-1,1,2)
    ]
    return (
        -(vals[0]-8*vals[1]+8*vals[2]-vals[3])
        /(12*h)
    )

v = {
    'program':
        'F0G_INDEPENDENT_EXTERIOR_STRESS_MULTIPOLE_VERIFIER',
    'verifier_sha256': sha(Path(__file__)),
    'checks': checks,
    'regression': 'NOT_RUN',
    'complete_energy': 'NOT_DERIVED',
    'physical_source': 'NOT_DERIVED',
    'whole_craft_force': 'NOT_DERIVED',
}

try:
    check(
        'science producer',
        sha(RUN/'f0g.py') == s['source_sha256']
    )
    check(
        'science sidecar',
        (RUN/'science.json.sha256').read_text().split()
        == [sha(RUN/'science.json'),'science.json']
    )
    check(
        'all parent hashes',
        len(s['parents']) == 4
        and all(
            sha(Path(p)) == h
            for p,h in s['parents'].items()
        )
    )
    check(
        'scope recorded',
        s['status'] ==
        'EXTERIOR_MAXWELL_DIPOLE_TAIL_INWARD_AT_GE_1M_SCOPED'
    )
    check(
        'Maxwell trace',
        sum(
            s['stress_eigenvalue_control']['principal_Tii_over_u']
        ) == 1
        and s['stress_eigenvalue_control']['active_over_u'] == 2
    )

    # Independent dipole exterior field-energy integral.
    R = s['source_radius_m']
    angular = quad(
        lambda mu:1+3*mu*mu,
        -1,1
    )[0]
    energy = (
        (2*math.pi/(32*math.pi**2))
        * angular
        * quad(
            lambda rr:rr**(-4),
            R,math.inf
        )[0]
    )

    check(
        'independent dipole energy',
        abs(energy-1/(12*math.pi*R**3)) < 1e-13
    )

    # Reconstruct each gravitational acceleration
    # independently from the Green-function potential.
    for row in s['probes']:
        rho = row['rho_m']/R
        z = row['z_m']/R
        nu = finite_diff_az(rho,z)

        check(
            'multipole force '+row['label'],
            abs(nu-row['a_z_normalized']) < 1e-8
        )
        check(
            'probe sign '+row['label'],
            (nu>0) == (row['classification']=='OUTWARD')
            and (nu<0) == (row['classification']=='INWARD')
        )

    # Exact global sign proof.
    # N(x,mu²) is affine in mu².
    # Its maximum for x>=1.5 occurs at mu²=0.
    # N(x,0) decreases for x>=1.5.
    xmin = s[
        'all_angles_in_upper_hemisphere_standoff_sign'
    ]['r_over_R_min']

    N0 = -10*xmin**3+27*xmin-15

    check(
        'global sign upper polynomial',
        N0 < 0
        and -30*xmin*xmin+27 < 0
        and xmin >= 1.5
    )

    for xx in (1.5,2,4,10):
        for mu in (0,0.2,0.7,1):
            norm = (
                mu*(-10*xx**3+27*xx-15+45*mu*mu*(1-xx))
                /(5*xx**5)
            )
            check(
                'sign x%.2f mu%.2f'%(xx,mu),
                norm <= 0
            )

    # Genuine near-surface positive sign control.
    crossover = s['axis_outward_shell_edge_r_over_R']
    norm = lambda x:(
        -2/x**2-18/(5*x**4)+6/x**5
    )

    check(
        'crossing root',
        1 < crossover < 1.05
        and abs(norm(crossover)) < 1e-11
    )
    check(
        'positive collar',
        norm(1.01)>0 and norm(1.5)<0
    )

    # Independent conversion to physical SI units.
    G = 6.67430e-11
    c = 299792458.0
    U = 10_000_000.0
    g = 9.80665

    az = (
        finite_diff_az(0,1.5)
        *G*U/(c*c*R*R)
    )

    check(
        'SI force unit',
        abs(
            az/s['axis_a_z_at_U10MJ_m_per_s2']-1
        ) < 1e-8
    )
    check(
        'energy magnitude label',
        abs(
            U*g/abs(az)
            /s['axis_U_required_for_1g_MAGNITUDE_J']-1
        ) < 1e-8
    )
    check(
        'force always inward for positive exterior energy',
        az < 0
        and s['axis_1g_sign_at_any_positive_U']
        == 'INWARD_NOT_OUTWARD'
    )
    check(
        'not whole-craft',
        s['earth_craft_reaction']=='NOT_DERIVED'
        and s['physical_source_support_action']=='NOT_DERIVED'
    )
    check(
        'no energy promotion',
        s['complete_operating_energy']=='NOT_CERTIFIED'
        and s['regression']=='NOT_RUN_SCOPED_THEOREM_PREFLIGHT'
    )
    check(
        'cannot replace 006D',
        s['006D_replaced'] is False
    )

    v['status'] = 'PASS_SCOPED_EXTERNAL_MAXWELL_STRESS_ONLY'

except Exception as exc:
    v['status'] = 'HOLD'
    v['error'] = repr(exc)

with (RUN/'verification.json').open('x') as f:
    json.dump(v,f,sort_keys=True,indent=2,allow_nan=False)
    f.write('\n')

(RUN/'verification.json.sha256').write_text(
    sha(RUN/'verification.json')
    +'  verification.json\n'
)

print('F0G_VERIFY =',v['status'])
print(
    'FOCUSED_CHECKS =',
    sum(checks.values()),'/',len(checks)
)
print(
    'VERIFICATION_SHA256 =',
    sha(RUN/'verification.json')
)

if v['status'] == 'HOLD':
    raise SystemExit(1)
