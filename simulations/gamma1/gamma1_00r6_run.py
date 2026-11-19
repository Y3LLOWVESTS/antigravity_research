"""R6 read-only PH16-on-background trace/Maxwell operator fork."""
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
from antigravity_research.gamma1.gamma1_00r6_trace_kernel import (
    sha,read_lock,analyze,PH16_SHA,R3_PROFILE_SHA,R5_MULTIPLIER_SHA,
)

PARENTS={
 'PH16_source':('src/antigravity_research/ph16/ph16_04_joint_stationary.py',PH16_SHA),
 'R3_native':('results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',R3_PROFILE_SHA),
 'R5_multiplier':('results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz',R5_MULTIPLIER_SHA),
 'R5_result':('results/data/gamma1_00r5_20261119T024922295970Z.json','7afa65cb80e66808a7fb88d0370906b63c090efed50c9d1aba74d50769bc05fd'),
 'R5_verification':('results/data/gamma1_00r5_verification_20261119T030257621565Z.json','5140149466fadd1230206653177b4423dd39301ea9a7105c6eec81467da67150'),
 'R4R1_verification':('results/data/gamma1_00r4r1_verification_20261119T022355350163Z.json','292c5fe396d2d448467346e5d1d7e06f76497dc3da5b504777232c9dd4b251b8'),
}
SOURCES=[
 'src/antigravity_research/gamma1/gamma1_00r6_trace_kernel.py',
 'simulations/gamma1/gamma1_00r6_run.py',
 'tests/gamma1/test_gamma1_00r6.py',
 'tests/gamma1/verify_gamma1_00r6.py',
 'theory/gamma1/GAMMA1_00R6_RESTRICTED_TRACE_AND_KERNEL_FORK.md',
]


def provenance():
    for key,(rel,expected) in PARENTS.items():
        path=ROOT/rel
        if sha(path)!=expected:
            raise RuntimeError('PARENT_HASH_MISMATCH:'+key)
        if path.suffix in ('.npz','.json'):
            side=path.with_name(path.name+'.sha256')
            if not side.is_file() or side.read_text().strip()!=expected+'  '+path.name:
                raise RuntimeError('PARENT_SIDECAR_MISMATCH:'+key)
    last=json.loads((ROOT/PARENTS['R5_result'][0]).read_text())
    verification=json.loads((ROOT/PARENTS['R5_verification'][0]).read_text())
    if (last['classification']!='PASS_ACTUAL_LATTICE_MULTIPLIER_AND_SCOPED_COVARIANT_IDENTITIES'
        or verification['classification']!='ORIGINAL_ACTION_MULTIPLIER_AND_SCOPED_COVARIANT_GATES_VERIFIED'
        or verification['full_regression_passed']!=3091
        or verification['scientific_result_sha256']!=PARENTS['R5_result'][1]
        or last['derived_multiplier_archive']['sha256']!=R5_MULTIPLIER_SHA
        or last['GAMMA1_01_authorized'] is not False):
        raise RuntimeError('R5_PARENT_CONTRACT_DRIFT')
    for rel,expected in last['source_shas'].items():
        if sha(ROOT/rel)!=expected:
            raise RuntimeError('R5_PRODUCING_SOURCE_MODIFIED:'+rel)
    return 'PASS_SIX_IMMUTABLE_PARENTS_AND_R5_SOURCE_FILES'


def main():
    now=dt.datetime.now(dt.timezone.utc)
    basename='gamma1_00r6_'+now.strftime('%Y%m%dT%H%M%S%fZ')
    data=ROOT/'results/data';logs=ROOT/'results/logs'
    data.mkdir(parents=True,exist_ok=True)
    logs.mkdir(parents=True,exist_ok=True)
    out=data/(basename+'.json')
    side=out.with_name(out.name+'.sha256')
    log=logs/(basename+'.log')
    result={
      'branch':'GAMMA1-00R6','timestamp_utc':now.isoformat(),
      'classification':'FAILED_OR_INCOMPLETE',
      'parents':{key:{'path':rel,'expected':digest,'actual':sha(ROOT/rel)} for key,(rel,digest) in PARENTS.items()},
      'producing_sources':{rel:sha(ROOT/rel) for rel in SOURCES},
      'PH16_replay':'NOT_RUN',
      'complete_covariant_action':'NOT_CLOSED',
      'Einstein_metric':'NOT_SOLVED',
      'Lorentzian_constraint_health':'NOT_CERTIFIED',
      'source_free_exterior':'NOT_CERTIFIED',
      'Earth_down':'NOT_DERIVED','whole_craft_up':'NOT_DERIVED',
      'complete_SI_energy_lt10MJ':'NOT_CERTIFIED',
      'GAMMA1_01_authorized':False,'PH16_05_authorized':False,
      'PH17_authorized':False,'006D_replaced':False,
    }
    status=2
    try:
        result['verified_parent_chain']=provenance()
        if 'MISSING' in result['producing_sources'].values():
            raise RuntimeError('PRODUCING_SOURCE_MISSING')
        profile=read_lock(ROOT/PARENTS['R3_native'][0],R3_PROFILE_SHA)
        lam=read_lock(ROOT/PARENTS['R5_multiplier'][0],R5_MULTIPLIER_SHA)
        result_science=analyze(profile,lam)
        arrays=result_science.pop('arrays')
        archive=data/(basename+'_restricted_trace_12_L12.npz')
        with archive.open('xb') as f:
            np.savez_compressed(f,**arrays)
            f.flush();os.fsync(f.fileno())
        digest=sha(archive)
        with archive.with_name(archive.name+'.sha256').open('x') as f:
            f.write(digest+'  '+archive.name+'\n');f.flush();os.fsync(f.fileno())
        result.update(result_science)
        result.update({
          'restricted_trace_archive':{'path':str(archive.relative_to(ROOT)),'sha256':digest,'keys':sorted(arrays)},
          'classification':'PASS_RESTRICTED_STATIC_TRACE_AND_FAIL_NODAL_MAXWELL_MATCH',
          'decision':'NO_EXACT_SAME_NODAL_MAXWELL_REDUCTION; REQUIRE_CONTINUUM_GALERKIN_AND_FULL_LORENTZIAN_ACTION',
          'qualified_physical_survivors':[],
        })
        status=0
    except Exception as exc:
        result['error']=str(exc)
        result['traceback']=traceback.format_exc()
        result['decision']='STOP_PRESERVE_FAILURE_NO_PHYSICS_PROMOTION'
    raw=(json.dumps(result,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    with out.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    digest=hashlib.sha256(raw).hexdigest()
    with side.open('x') as f:f.write(digest+'  '+out.name+'\n');f.flush();os.fsync(f.fileno())
    statements=[
      'RESULT_JSON='+str(out),'RESULT_SHA256='+digest,
      'CLASSIFICATION='+result['classification'],
      'TRACE_ARCHIVE='+result.get('restricted_trace_archive',{}).get('path','NONE'),
      'TRACE_SHA256='+result.get('restricted_trace_archive',{}).get('sha256','NONE'),
      'PH16_REPLAY=NOT_RUN','GRAVITY_AND_CRAFT_FORCE=NOT_DERIVED',
      'GAMMA1_01_AUTOMATIC_AUTHORIZATION=NO','006D_REPLACED=NO',
      'RETURN_CODE='+str(status),
    ]
    with log.open('x') as f:f.write('\n'.join(statements)+'\n');f.flush();os.fsync(f.fileno())
    print('\n'.join(statements),flush=True)
    return status

if __name__=='__main__':raise SystemExit(main())
