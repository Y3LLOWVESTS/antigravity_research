"""Independent R10 verifier. Does not import R10 producing-science module.

Rebuilds local fixed-frequency/number-label Lagrangian from original PH16
and uses numerical SECOND differences; verifies frozen Maxwell block with
eigenvalues, parent/provenance hashes and explicit no-promotion gates.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def independent_second_variation(d):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
       CoulombSource,Spec,JointAction,Settings,
    )

    with np.load(
        ROOT/d['parents']['R3_native']['path'],
        allow_pickle=False
    ) as f:
        F=np.array([f['F_plus'],f['F_minus']])
        A=f['A_X']
        Y=f['A_Y']
        P=f['P']
        n=f['neutral_n']
        sigref=f['sigma']
        w=f['weights']

    m=CoulombSource(Spec(nr=12,L=12),self_order=8)
    o=JointAction(m,Settings(nr=12,L=12))

    assert np.max(abs(w-o.w))<1e-11

    f2=F**2
    e2=np.exp(2*sigref)

    omega=(
        m.s.N/2
        +o.q*np.sum(f2*(w*e2*A)[None,:],axis=1)
    )/(f2@(w*e2))

    W=omega[:,None]-o.q[:,None]*A[None,:]
    nlab=n*np.exp(3*sigref)

    # Independent direct local cell energy.
    gradients=np.zeros(o.N)
    differences=F[:,o.edge_i]-F[:,o.edge_j]

    for k in range(2):
        edge_half=o.edge_c*differences[k]**2/2
        np.add.at(gradients,o.edge_i,edge_half)
        np.add.at(gradients,o.edge_j,edge_half)

    gradients+=o.boundary*np.sum(f2,axis=0)

    potential=(
        np.sum(f2-2*f2**2+2*f2**3,axis=0)
        +m.s.g*f2[0]*f2[1]
    )

    def local_energy(q):
        z=.05*q-40*q*q
        a=np.exp(2*z)

        return (
            a*(gradients-w*np.sum(F**2*W**2,axis=0))
            +w*a*a*potential
            +w*(
                o.s.mass*nlab*np.exp(z)
                +.5*o.s.kappa*nlab**2*np.exp(-2*z)
            )
        )

    h=3e-4
    value=local_energy(P)
    up=local_energy(P+h)
    dn=local_energy(P-h)

    derivative=-(up-dn)/(2*h)/w
    second=-(up-2*value+dn)/(h*h)/w

    exr=-o.Dr@A
    exz=-o.Dz@A
    byr=o.BR@Y
    byz=o.BZ@Y

    E2=exr**2+exz**2
    B2=byr**2+byz**2

    margin_e=1+second*B2
    margin_b=1-second*E2

    stored=d['evidence']['beta40']

    assert abs(
        float(derivative.min())-stored['lambda_range'][0]
    )<2e-4

    assert abs(
        float(derivative.max())-stored['lambda_range'][1]
    )<2e-4

    assert abs(
        float(second.min())-stored['chi_range'][0]
    )<2e-2

    assert abs(
        float(second.max())-stored['chi_range'][1]
    )<2e-2

    assert abs(
        float(margin_e.min())-stored['electric_rank_one_min']
    )<1e-4

    assert abs(
        float(margin_b.min())-stored['magnetic_rank_one_min']
    )<1e-4

    # Direct 3x3 Hessian eigenvalue controls on six native cells.
    for cell in (0,17,59,106,211,287):
        eb=np.array([byr[cell],byz[cell],0.])
        ee=np.array([exr[cell],exz[cell],0.])

        KE=np.eye(3)+second[cell]*np.outer(eb,eb)
        KB=np.eye(3)-second[cell]*np.outer(ee,ee)

        assert min(np.linalg.eigvalsh(KE))>.99
        assert min(np.linalg.eigvalsh(KB))>.2

        assert np.isclose(
            max(np.linalg.eigvalsh(KE)),
            margin_e[cell],
            rtol=1e-5,
            atol=1e-6
        )

        assert np.isclose(
            min(np.linalg.eigvalsh(KB)),
            margin_b[cell],
            rtol=1e-5,
            atol=1e-6
        )

    # Frozen beta60 profile. Only fixed-number frequencies reclose.
    sig60=.05*P-60*P**2
    w2=np.exp(2*sig60)

    om60=(
        m.s.N/2
        +o.q*np.sum(f2*(w*w2*A)[None,:],axis=1)
    )/(f2@(w*w2))

    W60=om60[:,None]-o.q[:,None]*A[None,:]

    def local_60(q):
        z=.05*q-60*q*q
        a=np.exp(2*z)

        return (
            a*(gradients-w*np.sum(F**2*W60**2,axis=0))
            +w*a*a*potential
            +w*(
                o.s.mass*nlab*np.exp(z)
                +.5*o.s.kappa*nlab**2*np.exp(-2*z)
            )
        )

    c60=-(
        local_60(P+h)
        -2*local_60(P)
        +local_60(P-h)
    )/(h*h)/w

    bad=int(np.sum(1-c60*E2<0))

    assert bad==d['evidence'][
        'beta60_OFFSHELL_FROZEN_PROFILE_CONTROL'
    ]['negative_magnetic_cells']==4

    return {
      'lambda_FD_max_abs_vs_claim':max(
          abs(float(derivative.min())-stored['lambda_range'][0]),
          abs(float(derivative.max())-stored['lambda_range'][1])
      ),
      'chi_FD_max_abs_extrema_vs_claim':max(
          abs(float(second.min())-stored['chi_range'][0]),
          abs(float(second.max())-stored['chi_range'][1])
      ),
      'electric_min_FD':float(margin_e.min()),
      'magnetic_min_FD':float(margin_b.min()),
      'beta60_negative_magnetic_cells_FD':bad,
    }


def verify(path):
    p=Path(path).resolve()
    assert p.parent==ROOT/'results/data'

    assert re.fullmatch(
        r'gamma1_00r10_\d{8}T\d{12}Z\.json',
        p.name
    )

    assert p.with_name(
        p.name+'.sha256'
    ).read_text().strip()==sha(p)+'  '+p.name

    d=json.loads(p.read_text())

    assert d['branch']=='GAMMA1-00R10'
    assert d['classification']==(
        'PASS_RESTRICTED_LORENTZIAN_MATTER_REDUCTION_AND_FROZEN_MODE_PREFLIGHT'
    )

    assert len(d['parents'])==6

    for item in d['parents'].values():
        assert (
            sha(ROOT/item['path'])
            ==item['expected_sha256']
            ==item['actual_sha256']
        )

    for rel,digest in d['producing_sources'].items():
        assert sha(ROOT/rel)==digest

    assert len(d['exact_restricted_identities'])==13
    assert all(d['exact_restricted_identities'].values())

    result=independent_second_variation(d)

    assert d['complete_Lorentzian_action']=='NOT_CLOSED'
    assert d['complete_offshell_Ward_Noether_Bianchi']=='NOT_CLOSED'
    assert d['full_constrained_mode_health']=='NOT_CERTIFIED'
    assert d['Einstein_stress_metric']=='NOT_DERIVED'
    assert d['whole_craft_up']=='NOT_DERIVED'
    assert d['complete_operating_energy_lt10MJ']=='NOT_CERTIFIED'
    assert d['qualified_full_gravity_bridge_survivors']==[]
    assert d['GAMMA1_01_authorized'] is False
    assert d['006D_replaced'] is False

    print('GAMMA1_00R10_INDEPENDENT_VERIFICATION=PASS')
    print('DIRECT_STATIC_SCALAR_FLUID_SECOND_VARIATION=PASS')
    print('RESTRICTED_ELECTRIC_AND_MAGNETIC_EIGEN_CHECK=PASS')

    for name,value in result.items():
        print(name.upper()+'='+str(value))

    print('RESULT_SHA256='+sha(p))


if __name__=='__main__':
    if len(sys.argv)!=2:
        raise SystemExit('Provide exact R10 result JSON')

    verify(sys.argv[1])
