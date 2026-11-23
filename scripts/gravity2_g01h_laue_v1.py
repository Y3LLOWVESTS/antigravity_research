"""G01H: necessary Laue/Maxwell-source support closure, not a gravity device."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from math import pi
from pathlib import Path
import secrets
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'results/gravity2/g01h_runs'
C = 299792458.0

PARENTS = {
    'F0D': (
        'results/data/delta1_f0d_20261120T231924Z_vCnB6I/science.json',
        '2db67eea46adf84327c14c0177c1863148893217a377ac67a1f3a39ec9cb6465',
    ),
    'F0F': (
        'results/data/delta1_f0f_20261121T032200Z_42xBGt/science.json',
        '145f7db67b440cbd5e5f0c2023ccb1ac7ad9d2151b777f459e1c2fc3964c9e73',
    ),
    'F0F_VERIFIED': (
        'results/data/delta1_f0f_20261121T032200Z_42xBGt/verification.json',
        'db52ae4365636ec72cb399fa380c13d5333d98db64aaa8d03e5c8e07e0376c50',
    ),
    'F0G': (
        'results/data/delta1_f0g_20261121T033524Z_929whN/science.json',
        'c8e74278c73b4d74f43560f7dec275c8061ef3f83c33d52afe703a7360a91c1f',
    ),
    'F0G_VERIFIED': (
        'results/data/delta1_f0g_20261121T033524Z_929whN/verification.json',
        'b2def664dae9363fffc4be1d9d6e145f94e6d6ec9b793d0f24d4e39a33cbd566',
    ),
}

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def encode(obj):
    return (
        json.dumps(obj, indent=2, sort_keys=True, allow_nan=False)
        + '\n'
    ).encode()

def parents():
    out = {}
    for name, (relative, expected) in PARENTS.items():
        path = ROOT / relative
        if (
            not path.is_file()
            or path.is_symlink()
            or digest(path) != expected
        ):
            raise ValueError('PARENT_EVIDENCE_HOLD:' + name)
        out[name] = {'path': relative, 'sha256': expected}

    f0d = json.loads((ROOT / PARENTS['F0D'][0]).read_text())
    f0f = json.loads((ROOT / PARENTS['F0F'][0]).read_text())
    f0g = json.loads((ROOT / PARENTS['F0G'][0]).read_text())

    if f0d['status'] != (
        'SCOPED_QUADRATIC_OFFSTATE_UNSTABLE_ALL_NONNEGATIVE_STIFFNESS'
    ):
        raise ValueError('F0D_STATUS_DRIFT')

    if (
        f0f['portal']['direct_Hilbert_stress_fixed_theta']
        != 'EXACTLY_ZERO'
        or f0g['status']
        != 'EXTERIOR_MAXWELL_DIPOLE_TAIL_INWARD_AT_GE_1M_SCOPED'
        or f0g['source_radius_m'] != 2.0
        or f0g['u_ext_reference_J'] != 10000000.0
        or f0g['true_surface_gap_m'] != 1.0
        or f0g['axis_a_z_at_U10MJ_m_per_s2'] >= 0
    ):
        raise ValueError('F0_PARENT_SCIENCE_DRIFT')

    return out, f0g

def science(f0g):
    U = f0g['u_ext_reference_J']
    R = f0g['source_radius_m']
    gap = f0g['true_surface_gap_m']

    # Exterior standard Maxwell:
    # E = k(r)(3 mu n - zhat)
    # T^ij = (E^2/2) delta_ij - E_i E_j.
    # Angular and radial integrals:
    # int T^ij dV = U_ext diag(2/5,2/5,1/5).
    coeff = (2/5, 2/5, 1/5)
    surface_k2 = 3 * U / (4*pi*R**3)
    V = 4*pi*R**3/3
    remainder_energy_lower = 2*U/5
    cap = 10_000_000.0

    return {
        'schema': 'gravity2.g01h.laue.v1',
        'status':
            'PASS_NECESSARY_CONSERVATION_OBLIGATIONS_NOT_SOURCE_CLOSURE',
        'input': {
            'source_radius_m': R,
            'true_surface_gap_m': gap,
            'reference_exterior_field_energy_J': U,
        },
        'action_scoped':
            'EXTERIOR_STANDARD_MAXWELL_STRESS_PLUS_CONDITIONAL_STATIC_CONSERVED_COMPLETION',
        'exterior_stress_tensor_integral_J': [
            [coeff[i]*U if i == j else 0.0 for j in range(3)]
            for i in range(3)
        ],
        'required_remaining_interior_and_support_integral_J': [
            [-coeff[i]*U if i == j else 0.0 for j in range(3)]
            for i in range(3)
        ],
        'relative_exterior_stress_diagonal': list(coeff),
        'trace_ext_stress_integral_J': U,
        'necessary_missing_trace_integral_J': -U,
        'laue_assumptions': [
            'STATIC',
            'LOCAL_TOTAL_CONSERVATION_FLAT_BACKGROUND',
            'ISOLATED_FINITE_ENERGY',
            'VANISHING_BOUNDARY_VIRIAL_FLUX',
        ],
        'DEC_necessary_bound_scope':
            'IF_ALL_REMAINDER_SECTORS_OBEY_DEC_AND_HAVE_NONNEGATIVE_ENERGY',
        'DEC_required_remaining_energy_at_reference_J_min':
            remainder_energy_lower,
        'DEC_required_total_energy_at_reference_J_min':
            U + remainder_energy_lower,
        'DEC_max_exterior_field_energy_with_strict_10MJ_total_budget_J':
            cap / (1 + 2/5),
        'DEC_strict_10MJ_feasibility_at_REFERENCE_Uext':
            'FAIL_CONDITIONAL_BUDGET',
        'remaining_region_volume_assumed_sphere_m3': V,
        'min_average_abs_xx_remainder_stress_Pa_if_confined_to_sphere':
            2*U/(5*V),
        'min_average_abs_zz_remainder_stress_Pa_if_confined_to_sphere':
            U/(5*V),
        'surface_field_k_squared_J_per_m3': surface_k2,
        'max_surface_abs_normal_traction_Pa':
            2*surface_k2,
        'max_surface_abs_shear_traction_Pa':
            surface_k2,
        'surface_normal_traction_equator_Pa':
            surface_k2/2,
        'far_weak_field_mass_sign_if_Utot_positive':
            'POSITIVE_ACTIVE_MONOPOLE_ATTRACTIVE_ASYMPTOTICALLY',
        'far_weak_field_M_active_min_kg_if_DEC_at_reference':
            (U+remainder_energy_lower)/C**2,
        'F0G_exterior_only_axis_acceleration_1m_gap_reference_m_s2':
            f0g['axis_a_z_at_U10MJ_m_per_s2'],
        'F0F_all_stress_standoff_energy_bound_applicable':
            'NO_EXTERIOR_FIELD_STRESS_OCCUPIES_GAP',
        'complete_operating_energy_equals_total_gravitating_energy':
            'NOT_ESTABLISHED',
        'gravitational_payload_response': 'NOT_DERIVED',
        'source_current_support_action': 'NOT_DERIVED',
        'whole_craft_force': 'NOT_DERIVED',
        'sourceable_Einstein_metric': 'NOT_DERIVED',
        'quantum_uv_empirical': 'NOT_DERIVED',
        '006D_replaced': False,
        'physical_survivors': 0,
        'decision':
            'MUST_PROVIDE_LOCAL_SOURCED_STRESS_SUPPORT_AND_SAME_ACTION_BEFORE_ANY_PHYSICAL_PROMOTION',
        'next_gate':
            'G01_ACTION_LOCAL_SOURCE_SUPPORT_STRESS_AND_METRIC_VARIATION',
    }

def selftest():
    from fractions import Fraction as F

    m2, m4 = F(1,3), F(1,5)
    u = (1 + 3*m2)/2
    ez2 = 9*m4 - 6*m2 + 1
    ex2 = F(9,2)*(m2-m4)

    assert u == 1
    assert (u-ez2)/u == F(1,5)
    assert (u-ex2)/u == F(2,5)

    exterior = (F(2,5), F(2,5), F(1,5))
    matching = tuple(-v for v in exterior)

    def closed(candidate):
        return all(
            a+b == 0
            for a,b in zip(exterior,candidate)
        )

    assert closed(matching)
    assert not closed((F(0),F(0),F(0)))
    assert not closed(exterior)
    assert not closed((F(-2,5),F(-2,5),F(0)))
    assert F(39,100) < max(exterior)

    print('G01H_ANALYTIC_ANGULAR_MOMENTS=PASS')
    print('G01H_NEGATIVE_CONTROLS=4/4_REJECTED')
    print('G01H_SCOPE=NECESSARY_NOT_SUFFICIENT')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=('run','selftest'))
    args = parser.parse_args()

    if args.cmd == 'selftest':
        selftest()
        return 0

    import g01h_independent_v1 as independent

    parent_locks, f0g = parents()
    result = science(f0g)
    independent.review(result)

    if BASE.is_symlink():
        raise ValueError('UNSAFE_RUN_BASE')

    BASE.mkdir(parents=True, exist_ok=True)

    run_id = (
        datetime.now(timezone.utc).strftime(
            'g01h_%Y%m%dT%H%M%SZ_'
        ) + secrets.token_hex(4)
    )

    folder = BASE / run_id
    folder.mkdir(mode=0o700)

    manifest = {
        'schema': 'gravity2.g01h.manifest.v1',
        'run_id': run_id,
        'parents': parent_locks,
        'source_sha256': {
            'scripts/gravity2_g01h_laue_v1.py':
                digest(Path(__file__)),
            'scripts/g01h_independent_v1.py':
                digest(Path(independent.__file__)),
        },
    }

    for name, obj in (
        ('manifest.json',manifest),
        ('science.json',result),
    ):
        with (folder/name).open('xb') as stream:
            stream.write(encode(obj))

    code = independent.verify(folder)
    if code:
        return code

    print('G01H_RUN=' + run_id)
    print('G01H_OUTPUT_DIR=' + str(folder))
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print('G01H_HOLD=' + repr(exc),file=sys.stderr)
        sys.exit(3)
