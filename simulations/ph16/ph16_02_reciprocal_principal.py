"""PH16-02 immutable scientific runner and provenance audit."""

from __future__ import annotations

import hashlib
import json
import os
import sys

from datetime import datetime,timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))

from antigravity_research.ph16.ph16_02_reciprocal_principal import report


PARENTS = {
    'PH15_P1':(
        'src/antigravity_research/agminer/hook17_ph15_p1_theorem.py',
        '9ce430fa8a0e155ef330de27f1a8461c93a970385db4eeb53507c87253c07ca5',
    ),
    'PH15_P8':(
        'src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py',
        '406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed',
    ),
    'PH15_P10':(
        'src/antigravity_research/agminer/hook17_ph15_p10_free_space.py',
        '25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb',
    ),
    'PH11_SUPPORT':(
        'src/antigravity_research/agminer/hook17_ph11_universal_metric_support_gate.py',
        '03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba',
    ),
    'FROZEN_M5V':(
        'src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py',
        'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f',
    ),
    'BETA1_00_JSON':(
        'results/data/beta1_00_20261116T200742656266Z.json',
        '866a305e4d7618d174ff63e864a3d7054ffc9133284e0e5c3637dec89145f708',
    ),
    'BETA1_1B1_JSON':(
        'results/data/beta1_1b1_20261117T001913743770Z.json',
        '1468220d56a8555207f3f7e7960880636bc0ccb88bc344ad0d748e5e61a91b11',
    ),
    'BETA1_02_JSON':(
        'results/data/beta1_02_20261117T164856020351Z.json',
        '723e21b16c003fdc6962455617ca56e9c390db10e43c1c55bfaec6e10efc3881',
    ),
    'BETA1_03_JSON':(
        'results/data/beta1_03_20261117T180317015064Z.json',
        '86b7b2601e7181ba59b6f5c95932246f2c97b98046b83b3d817601e806dc44f0',
    ),
    'BETA1_04_JSON':(
        'results/data/beta1_04_20261117T184058123842Z.json',
        '2ff63f1e2cbad2dc09d192569701b5503da06ca384ca60546d6e83c8c61ae632',
    ),
    'PH16_00_JSON':(
        'results/data/ph16_00_20261117T193302236321Z.json',
        '0f6025bbdaa1fe6da12bbd6d1044c192cbb40a1006d3103b76f8e9c0b3f8576e',
    ),
    'PH16_01_JSON':(
        'results/data/ph16_01_20261118T001752187817Z.json',
        '06f4aa6960645823e81e5d577288dadda8d579567456e8af05dd21369a4173ad',
    ),
    'PH16_01_SOURCE':(
        'src/antigravity_research/ph16/ph16_01_neutral_fluid_health.py',
        '7466a5c1a4613940ff6c57301375513629d0a940fb48e1d8ebe81bdbdf60ddbb',
    ),
}


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def main():
    parents = {}

    for name,(relative,expected) in PARENTS.items():
        path = ROOT/relative

        actual = (
            sha(path) if path.is_file() else 'MISSING'
        )

        if actual != expected:
            raise RuntimeError(
                f'PARENT_SHA_MISMATCH {name}: '
                f'{actual} expected {expected}'
            )

        if name.endswith('_JSON'):
            side = path.with_suffix('.json.sha256')

            if (
                not side.is_file()
                or side.read_text().split()[0] != expected
            ):
                raise RuntimeError(
                    'PARENT_SIDECAR_MISMATCH '+name
                )

        parents[name] = {
            'path':relative,
            'sha256':actual,
            'status':'MATCH',
        }

    previous = json.loads(
        (ROOT/PARENTS['PH16_01_JSON'][0]).read_text()
    )

    expected_verdict = (
        'YELLOW_PH16_01_COVARIANT_FLUID_EQUILIBRIUM_'
        'AND_FROZEN_PRINCIPAL_OBSTRUCTION_FULL_RECIPROCITY_OPEN'
    )

    if previous['primary_verdict'] != expected_verdict:
        raise RuntimeError(
            'Historical PH16-01 verdict changed'
        )

    if (
        previous['006D_replaced']
        or previous['PH17_approved'] != 'NO'
    ):
        raise RuntimeError(
            'Historical physical-promotion guard violated'
        )

    results = report()

    if (
        not all(results['exact']['checks'].values())
        or not all(results['gates'].values())
    ):
        raise RuntimeError(
            'PH16-02 scientific gates FAILED: '
            +str([
                k for k,v in results['gates'].items()
                if not v
            ])
        )

    now = datetime.now(timezone.utc)

    source = ROOT/(
        'src/antigravity_research/ph16/'
        'ph16_02_reciprocal_principal.py'
    )
    tests = ROOT/(
        'tests/ph16/test_ph16_02_reciprocal_principal.py'
    )

    doc = {
        'program':'ANTIGRAVITY_RESEARCH',
        'branch':'PH16-02',
        'timestamp_utc':now.isoformat(),
        'primary_verdict':results['verdict'],
        'classification':results['classification'],
        'experiment':
            'FINITE_GRID_FROZEN_Y_VARIATION_AND_'
            'GAUSS_ADMISSIBLE_TWO_U1_LOCAL_PRINCIPAL',
        'parent_sha256':parents,
        'source_sha256':sha(source),
        'runner_sha256':sha(__file__),
        'tests_sha256':sha(tests),
        'scoped_results':results,
        'physical_full_source_X_Y_fluid_solid_metric_on_shell':
            'NOT_SOLVED',
        'full_constrained_dynamical_health':
            'NOT_CERTIFIED',
        'physical_Earth_down_craft_up':'NOT_DERIVED',
        'true_exterior':'NOT_CERTIFIED',
        '1kg_1g_1m':'NOT_CERTIFIED',
        'complete_energy_SI_lt10MJ':'NOT_CERTIFIED',
        'PH17_approved':'NO',
        '006D_replaced':False,
        'ALPHA1_M5V_frozen':True,
        'physical_heuristic':
            'APPROX_35_PERCENT_REASSESS_AFTER_VERIFIED_SCIENTIFIC_REVIEW',
        'BETA1_heuristic':
            'FROZEN_APPROX_70_PERCENT',
        'next':
            'PH16-03 fixed-Noether coupled source/X/Y/fluid '
            'at beta<=40; exterior and GR remain open',
    }

    encoded = (
        json.dumps(
            doc,indent=2,sort_keys=True,allow_nan=False
        )+'\n'
    ).encode()

    path = (
        ROOT/'results/data'/
        ('ph16_02_'+now.strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    )

    path.parent.mkdir(
        parents=True,exist_ok=True
    )

    with path.open('xb') as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())

    digest = hashlib.sha256(encoded).hexdigest()
    sidecar = path.with_suffix('.json.sha256')

    with sidecar.open('x') as stream:
        stream.write(
            f'{digest}  {path.name}\n'
        )
        stream.flush()
        os.fsync(stream.fileno())

    print('PH16-02:',doc['primary_verdict'])
    print(
        'HISTORICAL PARENTS:',
        len(parents),'/',len(PARENTS),'MATCH'
    )
    print(
        'EXACT IDENTITIES:',
        sum(results['exact']['checks'].values()),
        '/',len(results['exact']['checks'])
    )
    print(
        'SCOPED GATES:',
        sum(results['gates'].values()),
        '/',len(results['gates'])
    )

    for name,case in results['cases'].items():
        y = case['finite_box_discrete_variational_Y_beta40']
        b60 = case['beta_sweep']['60']

        print(
            'CASE',name,
            'Y40_residual',
            y['Y_stationary_fullcell_residual_L2'],
            'Y40_Hessian_min',
            y['Y_discrete_Hessian_min_eigenvalue'],
            'Noether_shift_max',
            max(y['source_Noether_reaction_unresolved_abs_shift']),
            'beta60_mode_speed_squared',
            b60['local_finite_B_dispersion']['squared_phase_speeds'][0],
        )

    print('JOINT_SOURCE_X_Y_NEUTRAL_METRIC: NOT_SOLVED')
    print('WHOLE_CRAFT_EARTH_FORCE: NOT_DERIVED')
    print('006D_REPLACED: NO')
    print('PHYSICAL_HEURISTIC: ~35%')
    print('BETA1_HEURISTIC: ~70% FROZEN')
    print('RESULT_JSON:',path)
    print('SHA256:',digest)


if __name__ == '__main__':
    main()
