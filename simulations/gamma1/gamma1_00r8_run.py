"""GAMMA1-00R8 immutable finite-exterior Schur complement audit."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))

from antigravity_research.gamma1.gamma1_00r8_boundary_schur import (
    sha,analyze,PH16_SHA,P8_SHA,P10_SHA,R3_SHA,R7_SHA,R7_VERIFY_SHA,
)

PARENTS = {
 'PH16_source':(
    'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
    PH16_SHA,
 ),
 'P8_finite_volume_source':(
    'src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py',
    P8_SHA,
 ),
 'P10_ring_green_source':(
    'src/antigravity_research/agminer/hook17_ph15_p10_free_space.py',
    P10_SHA,
 ),
 'R3_native':(
    'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',
    R3_SHA,
 ),
 'R7_result':(
    'results/data/gamma1_00r7_20261119T040312289588Z.json',
    R7_SHA,
 ),
 'R7_verification':(
    'results/data/gamma1_00r7_verification_20261119T041623492189Z.json',
    R7_VERIFY_SHA,
 ),
}

PRODUCERS = [
 'src/antigravity_research/gamma1/gamma1_00r8_boundary_schur.py',
 'simulations/gamma1/gamma1_00r8_run.py',
 'tests/gamma1/test_gamma1_00r8.py',
 'tests/gamma1/verify_gamma1_00r8.py',
 'theory/gamma1/GAMMA1_00R8_EXTERIOR_SCHUR_AND_NATIVE_DISCRIMINANT.md',
]


def ancestry():
    for label,(rel,expected) in PARENTS.items():
        path = ROOT/rel

        if sha(path) != expected:
            raise RuntimeError('PARENT_RAW_SHA_DRIFT_'+label)

        if path.suffix in ('.json','.npz'):
            sc = path.with_name(path.name+'.sha256')

            if (
                not sc.is_file()
                or sc.read_text().strip() != expected+'  '+path.name
            ):
                raise RuntimeError('PARENT_SIDECAR_DRIFT_'+label)

    d = json.loads(
        (ROOT/PARENTS['R7_result'][0]).read_text()
    )
    v = json.loads(
        (ROOT/PARENTS['R7_verification'][0]).read_text()
    )

    if not (
        d['classification']
        == 'PASS_WEIGHTED_FV_SMOOTH_PROBE_TREND_NATIVE_MISMATCH_OPEN'
        and v['classification']
        == 'WEIGHTED_FV_SMOOTH_PROBE_BRIDGE_SCOPED_AND_FULL_REGRESSION_VERIFIED'
        and v['full_regression_passed'] == 3124
        and v['scientific_result_sha256'] == R7_SHA
        and d['GAMMA1_01_authorized'] is False
        and d['006D_replaced'] is False
    ):
        raise RuntimeError('R7_VERIFICATION_CHAIN_DRIFT')

    for rel,expected in d['source_hashes'].items():
        if sha(ROOT/rel) != expected:
            raise RuntimeError('R7_PRODUCING_SOURCE_CHANGED_'+rel)

    return {
      'six_parent_raw_hashes':'PASS',
      'R7_producing_files_checked':len(d['source_hashes']),
      'R7_full_regression':3124,
    }


def main():
    now = dt.datetime.now(dt.timezone.utc)
    basename = (
        'gamma1_00r8_'
        +now.strftime('%Y%m%dT%H%M%S%fZ')
    )

    data = ROOT/'results/data'
    logs = ROOT/'results/logs'

    data.mkdir(parents=True,exist_ok=True)
    logs.mkdir(parents=True,exist_ok=True)

    out = data/(basename+'.json')
    side = out.with_name(out.name+'.sha256')
    log = logs/(basename+'.log')

    result = {
      'branch':'GAMMA1-00R8',
      'timestamp_utc':now.isoformat(),
      'classification':'FAILED_OR_INCOMPLETE',

      'parents':{
          key:{
              'path':rel,
              'expected':expected,
              'actual':sha(ROOT/rel),
          }
          for key,(rel,expected) in PARENTS.items()
      },

      'producing_sources':{
          rel:sha(ROOT/rel)
          for rel in PRODUCERS
      },

      'PH16_source_replay':'NOT_RUN',
      'finite_DtN_is_infinite':'NO',
      'continuum_Maxwell_equivalence':'NOT_CERTIFIED',
      'full_Lorentzian_action':'NOT_CLOSED',
      'Einstein_metric':'NOT_SOLVED',
      'full_Lorentzian_mode_health':'NOT_CERTIFIED',
      'Earth_down':'NOT_DERIVED',
      'whole_craft_up':'NOT_DERIVED',
      'SI_energy_lt10MJ':'NOT_CERTIFIED',

      'GAMMA1_01_authorized':False,
      'PH16_05_authorized':False,
      'PH17_authorized':False,
      '006D_replaced':False,
    }

    status = 2

    try:
        result['ancestry'] = ancestry()

        if 'MISSING' in result['producing_sources'].values():
            raise RuntimeError('R8_PRODUCING_SOURCE_MISSING')

        with np.load(
            ROOT/PARENTS['R3_native'][0],
            allow_pickle=False
        ) as r3:
            native = {
                k:r3[k].copy()
                for k in ('A_X','A_Y')
            }

        report = analyze(native)
        archived = report.pop('archive')

        archive = data/(
            basename+'_interface_Schur_12_L12.npz'
        )

        with archive.open('xb') as f:
            np.savez_compressed(f,**archived)
            f.flush()
            os.fsync(f.fileno())

        archive_sha = sha(archive)

        with archive.with_name(
            archive.name+'.sha256'
        ).open('x') as f:
            f.write(
                archive_sha+'  '+archive.name+'\n'
            )
            f.flush()
            os.fsync(f.fileno())

        result.update({
          'classification':
              'PASS_FINITE_EXTERIOR_SCHUR_X_IMPROVES_Y_RESIDUAL_OPEN',

          'scientific_scope':
              'WEIGHTED_FV_FINITE_OUTER_DIRICHLET_SCHUR_TO_ORIGINAL_12_L12',

          'science':report,

          'interface_archive':{
              'path':str(archive.relative_to(ROOT)),
              'sha256':archive_sha,
              'keys':sorted(archived),
          },

          'decision':
              'BOUNDARY_MATTERS_BUT_Y_AND_OPERATOR_EQUIVALENCE_OPEN; DO_NOT_PROMOTE_TO_GRAVITY',

          'qualified_physical_survivors':[],
        })

        status = 0

    except Exception as exc:
        result['error'] = str(exc)
        result['traceback'] = traceback.format_exc()
        result['decision'] = (
            'PRESERVE_FAILURE_NO_PHYSICAL_PROMOTION'
        )

    raw = (
        json.dumps(
            result,
            sort_keys=True,
            indent=2,
            allow_nan=False
        )+'\n'
    ).encode()

    with out.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(raw).hexdigest()

    with side.open('x') as f:
        f.write(
            digest+'  '+out.name+'\n'
        )
        f.flush()
        os.fsync(f.fileno())

    lines = [
      'RESULT_JSON='+str(out),
      'RESULT_SHA256='+digest,
      'CLASSIFICATION='+result['classification'],

      'INTERFACE_ARCHIVE='
        +result.get('interface_archive',{}).get('path','NONE'),

      'INTERFACE_SHA256='
        +result.get('interface_archive',{}).get('sha256','NONE'),

      'PH16_REPLAY=NOT_RUN',
      'TRUE_EXTERIOR=NOT_CERTIFIED',
      'EINSTEIN_EARTH_CRAFT=NOT_DERIVED',
      '006D_REPLACED=NO',
      'GAMMA1_01_AUTHORIZED=NO',
      'RETURN_CODE='+str(status),
    ]

    with log.open('x') as f:
        f.write('\n'.join(lines)+'\n')
        f.flush()
        os.fsync(f.fileno())

    print('\n'.join(lines),flush=True)
    return status


if __name__ == '__main__':
    raise SystemExit(main())
