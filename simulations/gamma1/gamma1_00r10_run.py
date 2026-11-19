"""Append-only R10 theorem-first Lorentzian preflight; no PDE or source replay."""
from __future__ import annotations
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))

from antigravity_research.gamma1.gamma1_00r10_lorentzian_preflight import (
    sha,exact_lorentzian_necessary_identities,numerical_evidence,
    PH16_SHA,R3_SHA,R5_SHA,R9_RESULT_SHA,R9_VERIFY_SHA,R9_ARCHIVE_SHA,
)

PARENTS={
 'PH16_original':(
     'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
     PH16_SHA
 ),
 'R3_native':(
     'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',
     R3_SHA
 ),
 'R5_multiplier':(
     'results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz',
     R5_SHA
 ),
 'R9_result':(
     'results/data/gamma1_00r9_20261119T050922694396Z.json',
     R9_RESULT_SHA
 ),
 'R9_verify':(
     'results/data/gamma1_00r9_verification_20261119T052236433890Z.json',
     R9_VERIFY_SHA
 ),
 'R9_axis_archive':(
     'results/data/gamma1_00r9_20261119T050922694396Z_Y_axis_regular_12_L12.npz',
     R9_ARCHIVE_SHA
 ),
}

SOURCES=[
 'src/antigravity_research/gamma1/gamma1_00r10_lorentzian_preflight.py',
 'simulations/gamma1/gamma1_00r10_run.py',
 'tests/gamma1/test_gamma1_00r10.py',
 'tests/gamma1/verify_gamma1_00r10.py',
 'theory/gamma1/GAMMA1_00R10_LORENTZIAN_COMPLETION_OBSTRUCTION_LEDGER.md',
]


def ancestor_lock():
    for label,(rel,digest) in PARENTS.items():
        path=ROOT/rel
        if sha(path)!=digest:
            raise RuntimeError('PARENT_SHA_DRIFT_'+label)

        if path.suffix in ('.json','.npz'):
            side=path.with_name(path.name+'.sha256')
            if (
                not side.is_file()
                or side.read_text().strip()!=digest+'  '+path.name
            ):
                raise RuntimeError('PARENT_SIDECAR_DRIFT_'+label)

    doc=json.loads(
        (ROOT/PARENTS['R9_result'][0]).read_text()
    )
    verification=json.loads(
        (ROOT/PARENTS['R9_verify'][0]).read_text()
    )

    if not (
        doc['classification']
        =='PASS_AXIS_REGULAR_Y_IMPROVEMENT_QUADRATURE_RESIDUAL_OPEN'
        and verification['classification']
        =='AXIS_REGULAR_Y_COMPARATOR_AND_RESIDUAL_INDEPENDENTLY_VERIFIED'
        and verification['full_regression_passed']==3176
        and verification['scientific_result_sha256']==R9_RESULT_SHA
        and verification['archive_sha256']==R9_ARCHIVE_SHA
        and doc['GAMMA1_01_authorized'] is False
        and doc['006D_replaced'] is False
    ):
        raise RuntimeError('R9_PARENT_CONTRACT_DRIFT')

    for rel,digest in doc['producing_sources'].items():
        if sha(ROOT/rel)!=digest:
            raise RuntimeError('R9_PRODUCING_SOURCE_DRIFT_'+rel)

    return {
        'parent_SHA_verified':6,
        'R9_producer_SHA_verified':len(doc['producing_sources']),
        'previous_regression':3176,
    }


def main():
    now=dt.datetime.now(dt.timezone.utc)
    tag='gamma1_00r10_'+now.strftime('%Y%m%dT%H%M%S%fZ')

    results=ROOT/'results/data'
    logs=ROOT/'results/logs'
    results.mkdir(parents=True,exist_ok=True)
    logs.mkdir(parents=True,exist_ok=True)

    out=results/(tag+'.json')
    side=out.with_name(out.name+'.sha256')
    log=logs/(tag+'.log')

    doc={
      'branch':'GAMMA1-00R10',
      'timestamp_utc':now.isoformat(),
      'classification':'FAILED_OR_INCOMPLETE',

      'parents':{
          k:{
              'path':p,
              'expected_sha256':h,
              'actual_sha256':sha(ROOT/p)
          }
          for k,(p,h) in PARENTS.items()
      },

      'producing_sources':{
          p:sha(ROOT/p) for p in SOURCES
      },

      'complete_Lorentzian_action':'NOT_CLOSED',
      'complete_offshell_Ward_Noether_Bianchi':'NOT_CLOSED',
      'Einstein_stress_metric':'NOT_DERIVED',
      'full_constrained_mode_health':'NOT_CERTIFIED',
      'Earth_down':'NOT_DERIVED',
      'whole_craft_up':'NOT_DERIVED',
      'actual_PH16_source_replay':'NOT_RUN',
      'complete_operating_energy_lt10MJ':'NOT_CERTIFIED',
      'GAMMA1_01_authorized':False,
      'PH16_05_authorized':False,
      'PH17_authorized':False,
      '006D_replaced':False,
    }

    status=2

    try:
        doc['ancestry']=ancestor_lock()

        if 'MISSING' in doc['producing_sources'].values():
            raise RuntimeError('R10_PRODUCER_MISSING')

        with np.load(
            ROOT/PARENTS['R3_native'][0],
            allow_pickle=False
        ) as f:
            native={k:f[k].copy() for k in f.files}

        with np.load(
            ROOT/PARENTS['R5_multiplier'][0],
            allow_pickle=False
        ) as f:
            r5={k:f[k].copy() for k in f.files}

        identities=exact_lorentzian_necessary_identities()
        evidence=numerical_evidence(native,r5)

        doc.update({
          'classification':
              'PASS_RESTRICTED_LORENTZIAN_MATTER_REDUCTION_AND_FROZEN_MODE_PREFLIGHT',

          'scientific_scope':
              'STATIC_CHARGED_SCALAR_FLUID_REDUCTION_AND_INSTANTANEOUS_U1_BLOCKS_ONLY',

          'exact_restricted_identities':identities,
          'evidence':evidence,

          'qualified_full_gravity_bridge_survivors':[],

          'decision':
              'CONDITIONAL_STATIC_MATTER_PARENT_EXISTS; FINITE_RING_MAXWELL_AND_COMPLETE_LORENTZIAN_EARTH_SUPPORT_EINSTEIN_ACTION_UNPROVEN',
        })

        status=0

    except Exception as exc:
        doc['error']=str(exc)
        doc['traceback']=traceback.format_exc()
        doc['decision']='PRESERVE_FAILURE_STOP_NO_PROMOTION'

    raw=(
        json.dumps(
            doc,
            indent=2,
            sort_keys=True,
            allow_nan=False
        )+'\n'
    ).encode()

    with out.open('xb') as f:
        f.write(raw)
        f.flush()
        os.fsync(f.fileno())

    digest=hashlib.sha256(raw).hexdigest()

    with side.open('x') as f:
        f.write(digest+'  '+out.name+'\n')
        f.flush()
        os.fsync(f.fileno())

    lines=[
      'RESULT_JSON='+str(out),
      'RESULT_SHA256='+digest,
      'CLASSIFICATION='+doc['classification'],
      'EINSTEIN_EARTH_CRAFT=NOT_DERIVED',
      'FULL_LORENTZIAN_MODES=NOT_CERTIFIED',
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
