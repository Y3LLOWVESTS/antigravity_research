"""Independent Maxwell spherical and boundary-virial audit."""
from __future__ import annotations
from hashlib import sha256
import json
from math import pi
from pathlib import Path
import numpy as np

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def encode(d):
    return (
        json.dumps(d,indent=2,sort_keys=True,allow_nan=False)
        + '\n'
    ).encode()

def numerical(n_mu=32,n_phi=64):
    # Independent vector-field integration.
    # For E ~ r^-3, radial integration is analytic:
    # int_R^infinity (R/r)^6 r^2 dr = R^3/3.
    mu,w = np.polynomial.legendre.leggauss(n_mu)
    phi = 2*pi*(np.arange(n_phi)+.5)/n_phi

    n = np.stack((
        np.sqrt(1-mu[:,None]**2)*np.cos(phi),
        np.sqrt(1-mu[:,None]**2)*np.sin(phi),
        np.broadcast_to(mu[:,None],(n_mu,n_phi)),
    ),axis=-1)

    e = 3*mu[:,None,None]*n - np.array([0.,0.,1.])
    u = .5*np.sum(e*e,axis=-1)

    T = (
        u[...,None,None]*np.eye(3)
        - e[..., :,None]*e[...,None,:]
    )

    weights = np.broadcast_to(
        w[:,None]*(2*pi/n_phi),u.shape
    )

    angular = np.einsum(
        'ij,ijab->ab',weights,T
    )
    energy = np.sum(weights*u)

    # Surface virial identity:
    # Integral exterior T_ij dV =
    # -R^3 Integral n_i T_jk n_k dOmega.
    tn = np.einsum('...ij,...j->...i',T,n)
    boundary = (
        -3*np.einsum(
            'ij,ija,ijb->ab',weights,n,tn
        )/energy
    )

    volume = angular/energy
    return volume,boundary,float(energy)

def review(s):
    assert s['schema']=='gravity2.g01h.laue.v1'
    assert s['status']==(
        'PASS_NECESSARY_CONSERVATION_OBLIGATIONS_NOT_SOURCE_CLOSURE'
    )

    data=s['input']
    U=float(data['reference_exterior_field_energy_J'])
    R=float(data['source_radius_m'])
    gap=float(data['true_surface_gap_m'])

    assert U==1e7 and R==2.0 and gap==1.0

    expected=np.diag([.4,.4,.2])
    volume=np.asarray(
        s['exterior_stress_tensor_integral_J']
    )/U
    remainder=np.asarray(
        s['required_remaining_interior_and_support_integral_J']
    )/U

    assert np.max(np.abs(volume-expected))<1e-12
    assert np.max(np.abs(volume+remainder))<1e-12

    convergence=[]

    for count in (8,16,32,64):
        calculated,surface,energy=numerical(
            count,2*count
        )

        error=float(max(
            np.max(np.abs(calculated-expected)),
            np.max(np.abs(calculated-surface)),
            abs(energy-4*pi),
        ))

        assert error<1e-11,(count,error)

        convergence.append({
            'n_mu':count,
            'n_phi':2*count,
            'max_error':error,
        })

    k2=3*U/(4*pi*R**3)

    assert abs(
        s['surface_field_k_squared_J_per_m3']/k2-1
    )<1e-12

    assert abs(
        s['max_surface_abs_normal_traction_Pa']-2*k2
    )/k2<1e-12

    assert abs(
        s['max_surface_abs_shear_traction_Pa']-k2
    )/k2<1e-12

    assert abs(
        s['DEC_required_remaining_energy_at_reference_J_min']/U-.4
    )<1e-12

    assert abs(
        s['DEC_required_total_energy_at_reference_J_min']/U-1.4
    )<1e-12

    assert abs(
        s['DEC_max_exterior_field_energy_with_strict_10MJ_total_budget_J']
        -1e7/1.4
    )<1e-8

    assert (
        s['F0G_exterior_only_axis_acceleration_1m_gap_reference_m_s2']
        < 0
    )

    for field in (
        'gravitational_payload_response',
        'source_current_support_action',
        'whole_craft_force',
        'sourceable_Einstein_metric',
        'quantum_uv_empirical',
    ):
        assert s[field]=='NOT_DERIVED'

    assert (
        s['F0F_all_stress_standoff_energy_bound_applicable']
        =='NO_EXTERIOR_FIELD_STRESS_OCCUPIES_GAP'
    )

    assert s['physical_survivors']==0
    assert s['006D_replaced'] is False

    return {
        'status':'PASS_NECESSARY_LAUE_BUDGET_NOT_GRAVITY',
        'quadrature_convergence':convergence,
        'physical_survivors':0,
        'whole_craft_lift':False,
    }

def verify(folder):
    import gravity2_g01h_laue_v1 as producer

    try:
        manifest=json.loads(
            (folder/'manifest.json').read_text()
        )
        science=json.loads(
            (folder/'science.json').read_text()
        )

        expected={
            'scripts/gravity2_g01h_laue_v1.py':
                digest(Path(producer.__file__)),
            'scripts/g01h_independent_v1.py':
                digest(Path(__file__)),
        }

        if manifest['source_sha256']!=expected:
            raise ValueError('SOURCE_PROVENANCE_DRIFT')

        parents,f0g=producer.parents()

        if manifest['parents']!=parents:
            raise ValueError('PARENT_PROVENANCE_DRIFT')

        if producer.science(f0g)!=science:
            raise ValueError('SCIENCE_RECOMPUTATION_DRIFT')

        result=review(science)

        result.update({
            'manifest_sha256':
                digest(folder/'manifest.json'),
            'science_sha256':
                digest(folder/'science.json'),
        })

        dest=folder/'verification.json'
        raw=encode(result)

        if dest.exists():
            if dest.read_bytes()!=raw:
                raise ValueError('IMMUTABLE_VERIFICATION_DRIFT')
        else:
            with dest.open('xb') as stream:
                stream.write(raw)

        print(
            'G01H_INDEPENDENT_VERIFY='
            +result['status']
        )
        return 0

    except Exception as exc:
        print('G01H_VERIFY_HOLD='+repr(exc))
        return 3

if __name__=='__main__':
    import argparse,re,sys

    parser=argparse.ArgumentParser()
    parser.add_argument('--run-id',required=True)
    args=parser.parse_args()

    if not re.fullmatch(
        r'g01h_\d{8}T\d{6}Z_[a-f0-9]{8}',
        args.run_id
    ):
        print('G01H_VERIFY_HOLD=UNSAFE_RUN_ID')
        sys.exit(3)

    root=Path(__file__).resolve().parents[1]
    folder=root/'results/gravity2/g01h_runs'/args.run_id

    if not folder.is_dir() or folder.is_symlink():
        print('G01H_VERIFY_HOLD=MISSING_RUN')
        sys.exit(3)

    sys.exit(verify(folder))
