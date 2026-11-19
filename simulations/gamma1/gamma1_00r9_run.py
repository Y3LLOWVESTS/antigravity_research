"""Immutable R9 finite-exterior axis-regular azimuthal Maxwell comparator."""
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

from antigravity_research.gamma1.gamma1_00r9_axis_regular import (
    sha,analyze,
    PH16_SHA,P8_SHA,P10_SHA,R3_SHA,
    R8_RESULT_SHA,R8_VERIFY_SHA,R8_ARCHIVE_SHA,
)

PARENTS = {
    'PH16_source':(
        'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
        PH16_SHA,
    ),
    'P8_source':(
        'src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py',
        P8_SHA,
    ),
    'P10_source':(
        'src/antigravity_research/agminer/hook17_ph15_p10_free_space.py',
        P10_SHA,
    ),
    'R3_native':(
        'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',
        R3_SHA,
    ),
    'R8_science':(
        'results/data/gamma1_00r8_20261119T043910994414Z.json',
        R8_RESULT_SHA,
    ),
    'R8_verification':(
        'results/data/gamma1_00r8_verification_20261119T045224126507Z.json',
        R8_VERIFY_SHA,
    ),
    'R8_interface':(
        'results/data/gamma1_00r8_20261119T043910994414Z_interface_Schur_12_L12.npz',
        R8_ARCHIVE_SHA,
    ),
}

PRODUCERS = [
    'src/antigravity_research/gamma1/gamma1_00r9_axis_regular.py',
    'simulations/gamma1/gamma1_00r9_run.py',
    'tests/gamma1/test_gamma1_00r9.py',
    'tests/gamma1/verify_gamma1_00r9.py',
    'theory/gamma1/GAMMA1_00R9_AXIS_REGULAR_Y_FORK.md',
]


def ancestry():
    for label,(rel,expected) in PARENTS.items():
        path = ROOT/rel

        if sha(path) != expected:
            raise RuntimeError('PARENT_SHA_MISMATCH_'+label)

        if path.suffix in ('.json','.npz'):
            side = path.with_name(path.name+'.sha256')

            if (
                not side.is_file()
                or side.read_text().strip()!=expected+'  '+path.name
            ):
                raise RuntimeError('PARENT_SIDECAR_MISMATCH_'+label)

    r8 = json.loads(
        (ROOT/PARENTS['R8_science'][0]).read_text()
    )

    v8 = json.loads(
        (ROOT/PARENTS['R8_verification'][0]).read_text()
    )

    if not (
        r8['classification']
        =='PASS_FINITE_EXTERIOR_SCHUR_X_IMPROVES_Y_RESIDUAL_OPEN'

        and v8['classification']
        =='FINITE_EXTERIOR_SCHUR_NATIVE_DISCRIMINANT_INDEPENDENT_AND_REGRESSION_VERIFIED'

        and v8['full_regression_passed']==3148
        and v8['scientific_result_sha256']==R8_RESULT_SHA
        and r8['interface_archive']['sha256']==R8_ARCHIVE_SHA
        and r8['GAMMA1_01_authorized'] is False
        and r8['006D_replaced'] is False
    ):
        raise RuntimeError('R8_PROVENANCE_CONTRACT_DRIFT')

    for rel,expected in r8['producing_sources'].items():
        if sha(ROOT/rel)!=expected:
            raise RuntimeError('R8_SOURCE_CHANGED_'+rel)

    return {
        'parent_hash_count':7,
        'R8_producing_files_checked':len(r8['producing_sources']),
        'prior_full_regression':3148,
    }


def main():
    now = dt.datetime.now(dt.timezone.utc)
    name = 'gamma1_00r9_'+now.strftime('%Y%m%dT%H%M%S%fZ')

    data = ROOT/'results/data'
    logs = ROOT/'results/logs'
    data.mkdir(parents=True,exist_ok=True)
    logs.mkdir(parents=True,exist_ok=True)

    resultfile = data/(name+'.json')
    log = logs/(name+'.log')

    result = {
        'branch':'GAMMA1-00R9',
        'timestamp_utc':now.isoformat(),
        'classification':'FAILED_OR_INCOMPLETE',

        'parents':{
            label:{
                'path':rel,
                'expected_sha256':expected,
                'actual_sha256':sha(ROOT/rel),
            }
            for label,(rel,expected) in PARENTS.items()
        },

        'producing_sources':{
            rel:sha(ROOT/rel) for rel in PRODUCERS
        },

        'PH16_source_replay':'NOT_RUN',
        'continuum_azimuthal_Maxwell':'NOT_CERTIFIED',
        'complete_Lorentzian_action':'NOT_CLOSED',
        'Einstein_metric':'NOT_SOLVED',
        'Lorentzian_mode_health':'NOT_CERTIFIED',
        'Earth_down':'NOT_DERIVED',
        'whole_craft_up':'NOT_DERIVED',
        'complete_SI_energy_lt10MJ':'NOT_CERTIFIED',
        'GAMMA1_01_authorized':False,
        'PH16_05_authorized':False,
        'PH17_authorized':False,
        '006D_replaced':False,
    }

    status = 2

    try:
        result['ancestry'] = ancestry()

        if 'MISSING' in result['producing_sources'].values():
            raise RuntimeError('R9_PRODUCER_NOT_PRESENT')

        with np.load(
            ROOT/PARENTS['R3_native'][0],
            allow_pickle=False
        ) as p:
            y = p['A_Y'].copy()

        with np.load(
            ROOT/PARENTS['R8_interface'][0],
            allow_pickle=False
        ) as a:
            baseline = {k:a[k].copy() for k in a.files}

        report = analyze({'A_Y':y},baseline)
        arrays = report.pop('data_arrays')

        archive = data/(name+'_Y_axis_regular_12_L12.npz')

        with archive.open('xb') as f:
            np.savez_compressed(f,**arrays)
            f.flush()
            os.fsync(f.fileno())

        archive_sha = sha(archive)

        with archive.with_name(
            archive.name+'.sha256'
        ).open('x') as f:
            f.write(archive_sha+'  '+archive.name+'\n')
            f.flush()
            os.fsync(f.fileno())

        result.update({
            'classification':
                'PASS_AXIS_REGULAR_Y_IMPROVEMENT_QUADRATURE_RESIDUAL_OPEN',

            'scientific_scope':
                'FINITE_STATIC_AZIMUTHAL_MAXWELL_COMPARATOR_ON_FROZEN_R3',

            'science':report,

            'archive':{
                'path':str(archive.relative_to(ROOT)),
                'sha256':archive_sha,
                'keys':sorted(arrays),
            },

            'qualified_physical_survivors':[],

            'decision':
                'Y_AXIS_REGULAR_COMPARATOR_IMPROVES_BUT_20_PERCENT_RESIDUAL; NEED_ON_SHELL_MESH_REDUCTION_AND_COVARIANT_ACTION',
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

    with resultfile.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(raw).hexdigest()

    with resultfile.with_name(
        resultfile.name+'.sha256'
    ).open('x') as f:
        f.write(digest+'  '+resultfile.name+'\n')
        f.flush()
        os.fsync(f.fileno())

    lines = [
        'RESULT_JSON='+str(resultfile),
        'RESULT_SHA256='+digest,
        'CLASSIFICATION='+result['classification'],
        'R9_ARCHIVE='+result.get('archive',{}).get('path','NONE'),
        'R9_ARCHIVE_SHA256='+result.get('archive',{}).get('sha256','NONE'),
        'PH16_REPLAY=NOT_RUN',
        'EINSTEIN_EARTH_CRAFT=NOT_DERIVED',
        'GAMMA1_01_AUTHORIZED=NO',
        '006D_REPLACED=NO',
        'RETURN_CODE='+str(status),
    ]

    with log.open('x') as f:
        f.write('\n'.join(lines)+'\n')
        f.flush()
        os.fsync(f.fileno())

    print('\n'.join(lines),flush=True)
    return status


if __name__=='__main__':
    raise SystemExit(main())
