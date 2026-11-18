"""PH16-04 immutable same-lattice-action runner; fail closed on drift."""
from __future__ import annotations

import hashlib
import json
import os
import sys

from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))

from antigravity_research.ph16.ph16_04_joint_stationary import report


PARENTS={
 'PH15_P8':(
     'src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py',
     '406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed'
 ),
 'PH15_P10':(
     'src/antigravity_research/agminer/hook17_ph15_p10_free_space.py',
     '25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'
 ),
 'PH11_SUPPORT':(
     'src/antigravity_research/agminer/hook17_ph11_universal_metric_support_gate.py',
     '03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba'
 ),
 'ALPHA1_M5V_FROZEN':(
     'src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py',
     'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'
 ),
 'PH16_01_SOURCE':(
     'src/antigravity_research/ph16/ph16_01_neutral_fluid_health.py',
     '7466a5c1a4613940ff6c57301375513629d0a940fb48e1d8ebe81bdbdf60ddbb'
 ),
 'PH16_02_SOURCE':(
     'src/antigravity_research/ph16/ph16_02_reciprocal_principal.py',
     'b16fa3141270cc446d761bc8459e5504325b994ac31a889c0ea88520161b0b48'
 ),
 'PH16_03_SOURCE':(
     'src/antigravity_research/ph16/ph16_03_number_closed_reaction.py',
     'c8c9724d80dff5c6b0832559ae645c8f515b1101a9a11612b629ec819ff8ae4b'
 ),
 'PH16_01_JSON':(
     'results/data/ph16_01_20261118T001752187817Z.json',
     '06f4aa6960645823e81e5d577288dadda8d579567456e8af05dd21369a4173ad'
 ),
 'PH16_02_JSON':(
     'results/data/ph16_02_20261118T033343237505Z.json',
     '95b549c75346e81fc62b20e919160954c48bf4abe6230beb5bbf40ddf34a68ee'
 ),
 'PH16_03_JSON':(
     'results/data/ph16_03_20261118T042539925053Z.json',
     '5db45e842666dd942300bd5497797c94e65d236e1646822556dadc7504a55167'
 ),
 'BETA1_04_JSON':(
     'results/data/beta1_04_20261117T184058123842Z.json',
     '2ff63f1e2cbad2dc09d192569701b5503da06ca384ca60546d6e83c8c61ae632'
 ),
}


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def main():
    parents={}

    for key,(relative,want) in PARENTS.items():
        path=ROOT/relative
        actual=sha(path) if path.is_file() else 'MISSING'

        if actual!=want:
            raise RuntimeError(
                f'FAIL_CLOSED_{key}_SHA '
                f'expected {want}, actual {actual}'
            )

        if key.endswith('_JSON'):
            side=path.with_suffix('.json.sha256')

            if (
                not side.is_file()
                or side.read_text().split()[0]!=actual
            ):
                raise RuntimeError(
                    'FAIL_CLOSED_PARENT_SIDECAR '+key
                )

        parents[key]={
            'path':relative,
            'sha256':actual,
            'status':'MATCH'
        }

    prev=json.loads(
        (ROOT/PARENTS['PH16_03_JSON'][0]).read_text()
    )

    if prev['primary_verdict']!=(
        'YELLOW_PH16_03_FIXED_NOETHER_Y_FLUID_'
        'REDUCED_STATIONARY_FULL_SOURCE_X_METRIC_OPEN'
    ):
        raise RuntimeError(
            'PH16-03 verdict provenance drift'
        )

    if (
        prev['006D_replaced']
        or prev['PH17_approved']!='NO'
    ):
        raise RuntimeError(
            'Historical physics promotion drift'
        )

    science=report()

    passed=(
        all(science['exact'].values())
        and all(science['gates'].values())
    )

    now=datetime.now(timezone.utc)

    source=ROOT/(
        'src/antigravity_research/ph16/'
        'ph16_04_joint_stationary.py'
    )
    tests=ROOT/(
        'tests/ph16/'
        'test_ph16_04_joint_stationary.py'
    )

    doc={
      'program':'ANTIGRAVITY_RESEARCH',
      'branch':'PH16-04',
      'timestamp_utc':now.isoformat(),
      'experiment':
          'JOINT_SAME_LATTICE_F_X_Y_NOETHER_NEUTRAL_MIMETIC_WARD_TWO_INITIALIZATIONS',
      'primary_verdict':(
          science['verdict']
          if passed else 'RED_PH16_04_SCOPED_GATE_FAILURE'
      ),
      'classification':science['classification'],
      'parent_sha256':parents,
      'source_sha256':sha(source),
      'runner_sha256':sha(__file__),
      'tests_sha256':sha(tests),
      'scoped_results':science,
      'scoped_gates_pass':bool(passed),
      'full_GR_Einstein_equations':'NOT_SOLVED',
      'real_material_support_and_Earth':'NOT_SOLVED',
      'whole_craft_Earth_down_craft_up':'NOT_DERIVED',
      'continuum_and_exterior':'NOT_CERTIFIED',
      'complete_constrained_dynamic_modes':'NOT_CERTIFIED',
      'real_1kg_torus_1g_at_1m':'NOT_CERTIFIED',
      'complete_SI_energy_lt10MJ':'NOT_CERTIFIED',
      'ALPHA1_M5V_frozen':True,
      '006D_replaced':False,
      'PH17_approved':'NO',
      'physical_heuristic':
          'APPROX_35_PERCENT_PENDING_EXECUTED_REVIEW',
      'BETA1_heuristic':
          'FROZEN_APPROX_70_PERCENT',
      'next':
          'PH16-05 continuum/exterior convergence '
          'and constrained Hessian; no PH17 transfer'
    }

    data=(
        json.dumps(
            doc,
            sort_keys=True,
            indent=2,
            allow_nan=False
        )+'\n'
    ).encode()

    stamp=now.strftime('%Y%m%dT%H%M%S%fZ')

    path=(
        ROOT/'results/data'/
        f'ph16_04_{stamp}.json'
    )
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with path.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

    digest=hashlib.sha256(data).hexdigest()

    with path.with_suffix('.json.sha256').open('x') as f:
        f.write(
            f'{digest}  {path.name}\n'
        )
        f.flush()
        os.fsync(f.fileno())

    print('PH16-04:',doc['primary_verdict'])
    print(
        'PARENTS:',
        len(parents),'/',len(PARENTS),'MATCH'
    )
    print(
        'EXACT:',
        sum(science['exact'].values()),
        '/',len(science['exact'])
    )
    print(
        'SCOPED:',
        sum(science['gates'].values()),
        '/',len(science['gates'])
    )

    for key,c in science['cases'].items():
        d=c['direct_weak_seed']
        s=c['Y_preconditioned_joint']

        print(
            'CASE',key,
            'joint_residual',
            format(s['final_residual_L2'],'.9g'),
            'N_err',
            format(
                max(abs(a-400.) for a in s['N']),
                '.9g'
            ),
            'mag_margin',
            format(
                s['frozen_magnetic_margin_min'],
                '.9g'
            ),
            'Bianchi',
            format(
                s['discrete_mimetic_divB_inf'],
                '.9g'
            ),
            'weak_start_residual',
            format(
                d['final_residual_L2'],
                '.9g'
            ),
            'weak_start_converged',
            bool(d['final_residual_L2']<1e-6),
            flush=True
        )

    print('METRIC_AND_EARTH_REACTION: NOT_DERIVED')
    print('COMPLETE_SI_ENERGY: NOT_CERTIFIED')
    print('006D_REPLACED: NO')
    print('RESULT_JSON:',path)
    print('SHA256:',digest)

    if not passed:
        raise RuntimeError(
            'PH16-04 gates failed; '
            'immutable RED artifact retained'
        )


if __name__=='__main__':
    main()
