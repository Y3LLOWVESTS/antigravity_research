"""DELTA1-F0G: exterior Maxwell-dipole stress gravitational response.

SCOPE: Analytic linearized-GR *contribution* of the exterior electric field
of F0D's frozen uniform-polarization trial. The material source/support
stress, interior fields, exact stationary solution, Earth/craft coupling
and complete SI energy are NOT calculated.
"""
import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(os.environ['F0G_RUN']).resolve()
P_F0F = Path(os.environ['F0F_PARENT']).resolve()
P_F0D = Path(os.environ['F0D_PARENT']).resolve()
P_F0C = Path(os.environ['F0C_PARENT']).resolve()

PARENT_HASHES = {
    str(P_F0F/'science.json'):
        '145f7db67b440cbd5e5f0c2023ccb1ac7ad9d2151b777f459e1c2fc3964c9e73',
    str(P_F0F/'verification.json'):
        'db52ae4365636ec72cb399fa380c13d5333d98db64aaa8d03e5c8e07e0376c50',
    str(P_F0D/'science.json'):
        '2db67eea46adf84327c14c0177c1863148893217a377ac67a1f3a39ec9cb6465',
    str(P_F0C/'science.json'):
        '3c671e54a44a23bd12d2fe2451aed6388bb3c4f6da37408d7abe54c808540f7f',
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def write(name, data):
    p = RUN/name
    with p.open('x') as stream:
        json.dump(data, stream, sort_keys=True, indent=2, allow_nan=False)
        stream.write('\n')
    (RUN/(name+'.sha256')).write_text(
        sha(p)+'  '+name+'\n'
    )

def scalar_P2(mu):
    return (3*mu*mu-1)/2

def f0(x):
    return 1/(3*x)-1/(12*x**4)

def f2(x):
    return 1/(5*x**3)-1/(6*x**4)

def phi_normalized(x, mu):
    return -6*(f0(x)+f2(x)*scalar_P2(mu))

def az_normalized(x, mu):
    # a_z / [G U_ext /(c^2 R^2)]
    return mu*(-10*x**3+27*x-15+45*mu*mu*(1-x))/(5*x**5)

r = {
    'program':
        'DELTA1-F0G_EXTERIOR_MAXWELL_DIPOLE_METRIC_STRESS_SIGN_GATE',
    'utc': datetime.now(timezone.utc).isoformat(),
    'source_sha256': sha(Path(__file__)),
    'parents': PARENT_HASHES,
    'regression': 'NOT_RUN_SCOPED_THEOREM_PREFLIGHT',
    'physical_source_support_action': 'NOT_DERIVED',
    'material_stress_and_interior_fields': 'NOT_INCLUDED',
    'full_stress_conservation': 'NOT_CLOSED',
    'neutral_payload_gravitational_lift': 'NOT_DERIVED',
    'earth_craft_reaction': 'NOT_DERIVED',
    'complete_operating_energy': 'NOT_CERTIFIED',
    '006D_replaced': False,
}

try:
    for filename, hashval in PARENT_HASHES.items():
        need(
            sha(Path(filename)) == hashval,
            'parent SHA mismatch '+filename
        )

    f0f = json.loads((P_F0F/'science.json').read_bytes())
    f0fv = json.loads((P_F0F/'verification.json').read_bytes())
    f0d = json.loads((P_F0D/'science.json').read_bytes())
    f0c = json.loads((P_F0C/'science.json').read_bytes())

    need(
        f0f['status'] ==
        'PASS_SCOPED_THEOREM_AND_CONDITIONAL_OBSTRUCTION',
        'F0F status'
    )
    need(
        f0fv['status'] ==
        'PASS_SCOPED_EXACT_PORTAL_AND_CONDITIONAL_DEC_BOUND',
        'F0F verification'
    )
    need(
        f0d['status'] ==
        'SCOPED_QUADRATIC_OFFSTATE_UNSTABLE_ALL_NONNEGATIVE_STIFFNESS',
        'F0D status'
    )
    need(
        f0c['status'] ==
        'LOADED_AXIAL_TRIAL_COMPLETE_PHYSICAL_MODE_UNDERDETERMINED',
        'F0C status'
    )
    need(
        f0f['portal']['direct_Hilbert_stress_fixed_theta'] ==
        'EXACTLY_ZERO',
        'portal negative control'
    )

    R = float(f0d['assumed_parameters']['source_radius_m'])
    need(R == 2.0, 'source radius differs')
    need(
        f0d['uniform_dipole_trial']['gradient_cost'] == 0,
        'wrong F0D trial'
    )

    # Exterior electric dipole:
    #
    # E = p/(4*pi*r^3)*(3*mu*rhat - zhat), B=0
    # u_EM = p^2*(1+3*mu^2)/(32*pi^2*r^6)
    # U_ext = p^2/(12*pi*R^3)
    #
    # Maxwell: T00=u and sum_i Tii=u.
    # rho_active=(T00+sum_i Tii)/c^2=2*u/c^2.
    #
    # Only exterior stress is calculated.
    #
    # Phi = -6*G*U_ext/(c^2*R)
    #       * [f0(x)+f2(x)*P2(mu)]
    #
    # x=r/R, mu=z/r.
    #
    # a_z/[G*U_ext/(c^2*R^2)]
    # = mu*(-10*x^3+27*x-15+45*mu^2*(1-x))/(5*x^5).
    #
    # For x>=1.5 and 0<=mu<=1:
    # numerator <= -8.25 < 0.

    G = 6.67430e-11
    c = 299792458.0
    U = 10_000_000.0
    g = 9.80665
    d = 1.0

    x_min = (R+d)/R
    need(x_min == 1.5, 'true stand-off')

    upper_num = -10*x_min**3+27*x_min-15

    need(
        abs(upper_num+8.25) < 1e-13,
        'analytic numerator cap'
    )
    need(
        27-30*x_min*x_min < 0,
        'radial derivative negative'
    )

    # Historical F0C locations are read from the original JSON.
    p_a = next(
        row['worst_r_z_m']
        for row in f0c['rows']
        if row['case'] == 'loaded'
        and row['flip']
        and row['h'] == 0.05
        and row['L'] == 7.5
    )
    p_b = next(
        row['worst_r_z_m']
        for row in f0c['rows']
        if row['case'] == 'loaded'
        and not row['flip']
        and row['h'] == 0.05
        and row['L'] == 6
    )

    probes = [
        ('axis_at_one_m_gap', 0.0, 3.0),
        ('F0C_loaded_worst_A', *p_a),
        ('F0C_loaded_worst_B', *p_b),
        ('off_axis_one_m_plus', 1.0, 3.0),
        ('surface_near_axis_positive_control', 0.0, 2.02),
    ]

    scale = G*U/(c*c*R*R)
    rows = []

    for name,rho,z in probes:
        dist = math.hypot(rho,z)
        x = dist/R
        mu = z/dist
        norm = az_normalized(x,mu)

        rows.append({
            'label': name,
            'rho_m': rho,
            'z_m': z,
            'r_over_R': x,
            'surface_gap_m': dist-R,
            'a_z_normalized': norm,
            'a_z_for_U10MJ_m_per_s2': norm*scale,
            'classification':
                'OUTWARD' if norm > 0
                else 'INWARD' if norm < 0
                else 'ZERO',
        })

    need(
        all(row['a_z_normalized'] < 0 for row in rows[:4]),
        'stand-off probe inward sign'
    )
    need(
        rows[-1]['a_z_normalized'] > 0,
        'near-surface positive control'
    )

    # Sign reversal along the polar axis.
    lo,hi = 1.0,1.5
    for _ in range(65):
        mid = (lo+hi)/2
        if az_normalized(mid,1.0) > 0:
            lo = mid
        else:
            hi = mid

    axis_cross = (lo+hi)/2
    need(1 < axis_cross < 1.05, 'axis crossover')

    required_hypothetical = (
        U*g/abs(rows[0]['a_z_for_U10MJ_m_per_s2'])
    )

    r.update({
        'status':
            'EXTERIOR_MAXWELL_DIPOLE_TAIL_INWARD_AT_GE_1M_SCOPED',
        'source_radius_m': R,
        'true_surface_gap_m': d,
        'u_ext_reference_J': U,
        'reference_energy_is_NOT_measured_F0D_energy': True,
        'exterior_field':
            'E=p/(4*pi*r^3)*(3*mu*rhat-zhat), B=0',
        'exterior_energy_identity':
            'U_ext=p^2/(12*pi*R^3)',
        'active_density':
            'rho_active=2*u_EM/c^2 (Maxwell trace-free exterior)',
        'stress_eigenvalue_control': {
            'T00_over_u': 1,
            'principal_Tii_over_u': [-1,1,1],
            'active_over_u': 2,
            'DEC_saturated': True,
        },
        'potential_dimensionless':
            'Phi/[G*U_ext/(c^2*R)]=-6*(f0(x)+f2(x)*P2(mu))',
        'f0': '1/(3*x)-1/(12*x^4)',
        'f2': '1/(5*x^3)-1/(6*x^4)',
        'a_z_dimensionless':
            'mu*(-10*x^3+27*x-15+45*mu^2*(1-x))/(5*x^5)',
        'all_angles_in_upper_hemisphere_standoff_sign': {
            'r_over_R_min': x_min,
            'mu_range': [0,1],
            'numerator_upper_at_x_min_mu0': upper_num,
            'radial_derivative_upper_at_x_min':
                27-30*x_min*x_min,
            'outcome':
                'a_z<=0 for all z>=0 and r>=R+1m; '
                'strictly negative if z>0',
        },
        'axis_outward_shell_edge_r_over_R': axis_cross,
        'axis_outward_shell_edge_gap_m':
            R*(axis_cross-1),
        'probes': rows,
        'axis_a_z_at_U10MJ_m_per_s2':
            rows[0]['a_z_for_U10MJ_m_per_s2'],
        'axis_U_required_for_1g_MAGNITUDE_J':
            required_hypothetical,
        'axis_1g_sign_at_any_positive_U':
            'INWARD_NOT_OUTWARD',
        'claims_and_limitations': [
            'Only exterior Maxwell field stress is varied '
            'in linearized Einstein source; not full conserved tensor',
            'EM stress extends into gap, unlike conditional '
            'F0F all-stress-away bound',
            'The dipole originates from F0D prescribed uniform '
            'source, not a jointly solved stationary source',
            'Actual F0D canonical trial energy is not '
            'measured in SI joules',
            'The 1m spherical gap and upper-half-space '
            'are not an all-torus coupled test',
            'Support and interior fields can change metric '
            'and force; no global no-go',
            'No actual Earth reaction or whole-craft '
            'momentum balance is derived',
        ],
        'decision':
            'EXTERIOR_DIPOLE_STRESS_TAIL_ALONE_CANNOT_'
            'SUPPLY_OUTWARD_1G_AT_GE_1M',
    })

except Exception as exc:
    r['status'] = 'HOLD'
    r['error'] = repr(exc)

write('science.json',r)

print('F0G_STATUS =',r['status'])

if r['status'] != 'HOLD':
    print(
        'AXIS_FORCE_AT_10MJ_m_s2 =',
        r['axis_a_z_at_U10MJ_m_per_s2']
    )
    print(
        'CROSSOVER_GAP_m =',
        r['axis_outward_shell_edge_gap_m']
    )
    print(
        'ALL_ANGLES_1M_SIGN =',
        r['all_angles_in_upper_hemisphere_standoff_sign']['outcome']
    )
    print('WHOLE_CRAFT_FORCE =',r['earth_craft_reaction'])

print('SCIENCE_SHA256 =',sha(RUN/'science.json'))

if r['status'] == 'HOLD':
    raise SystemExit(1)
