"""GAMMA1-00R11: immutable PH16 fixed-charge Schur and conditional U1 symbol audit.

No full Lorentzian action, Einstein/Earth response, physical lift, or SI completion.
"""
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
from antigravity_research.gamma1.gamma1_00r11_constrained_symbol import (
    sha,analyze,PH16_SHA,R3_SHA,R5_SHA,R10_SHA,R10_VERIFY_SHA,R9_SHA,
)

PARENTS={
  'PH16_original':('src/antigravity_research/ph16/ph16_04_joint_stationary.py',PH16_SHA),
  'R3_native':('results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',R3_SHA),
  'R5_multiplier':('results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz',R5_SHA),
  'R9_science':('results/data/gamma1_00r9_20261119T050922694396Z.json',R9_SHA),
  'R10_science':('results/data/gamma1_00r10_20261119T065042059747Z.json',R10_SHA),
  'R10_verification':('results/data/gamma1_00r10_verification_20261119T070450958407Z.json',R10_VERIFY_SHA),
}
PRODUCERS=[
 'src/antigravity_research/gamma1/gamma1_00r11_constrained_symbol.py',
 'simulations/gamma1/gamma1_00r11_run.py',
 'tests/gamma1/test_gamma1_00r11.py',
 'tests/gamma1/verify_gamma1_00r11.py',
 'theory/gamma1/GAMMA1_00R11_NOETHER_SCHUR_AND_FROZEN_SYMBOL_LEDGER.md',
]


def ancestry():
    for label,(rel,h) in PARENTS.items():
        path=ROOT/rel
        if sha(path)!=h:raise RuntimeError('PARENT_SHA_DRIFT_'+label)
        if path.suffix in ('.json','.npz'):
            side=path.with_name(path.name+'.sha256')
            if not side.is_file() or side.read_text().strip()!=h+'  '+path.name:
                raise RuntimeError('PARENT_SIDECAR_DRIFT_'+label)
    d=json.loads((ROOT/PARENTS['R10_science'][0]).read_text())
    v=json.loads((ROOT/PARENTS['R10_verification'][0]).read_text())
    if not (
      d['classification']=='PASS_RESTRICTED_LORENTZIAN_MATTER_REDUCTION_AND_FROZEN_MODE_PREFLIGHT'
      and v['classification']=='RESTRICTED_LORENTZIAN_PREFLIGHT_INDEPENDENT_AND_REGRESSION_VERIFIED'
      and v['full_regression_passed']==3195
      and v['scientific_result_sha256']==R10_SHA
      and d['GAMMA1_01_authorized'] is False
      and d['006D_replaced'] is False
    ):raise RuntimeError('R10_PARENT_CONTRACT_DRIFT')
    for rel,h in d['producing_sources'].items():
        if sha(ROOT/rel)!=h:raise RuntimeError('R10_SOURCE_CHANGED_'+rel)
    return {'six_parent_raw_Shas':'PASS',
            'R10_producer_Shas_checked':len(d['producing_sources']),
            'previous_full_regression':3195}


def main():
    now=dt.datetime.now(dt.timezone.utc)
    name='gamma1_00r11_'+now.strftime('%Y%m%dT%H%M%S%fZ')
    data=ROOT/'results/data'; logs=ROOT/'results/logs'
    data.mkdir(parents=True,exist_ok=True);logs.mkdir(parents=True,exist_ok=True)
    path=data/(name+'.json')
    doc={
      'branch':'GAMMA1-00R11','timestamp_utc':now.isoformat(),
      'classification':'FAILED_OR_INCOMPLETE',
      'parents':{k:{'path':rel,'expected':h,'actual':sha(ROOT/rel)} for k,(rel,h) in PARENTS.items()},
      'producing_sources':{rel:sha(ROOT/rel) for rel in PRODUCERS},
      'full_Lorentzian_action':'NOT_CLOSED',
      'full_constrained_scalar_fluid_gravity_health':'NOT_CERTIFIED',
      'Einstein_metric':'NOT_SOLVED','Earth_down':'NOT_DERIVED',
      'whole_craft_up':'NOT_DERIVED','complete_energy_lt10MJ':'NOT_CERTIFIED',
      'PH16_replay':'NOT_RUN','M0_full_physical_survivor':False,
      'GAMMA1_01_authorized':False,'PH16_05_authorized':False,
      'PH17_authorized':False,'006D_replaced':False,
    }
    status=2
    try:
        doc['provenance']=ancestry()
        if 'MISSING' in doc['producing_sources'].values():raise RuntimeError('PRODUCER_MISSING')
        with np.load(ROOT/PARENTS['R3_native'][0],allow_pickle=False) as f:
            native={k:f[k].copy() for k in f.files}
        with np.load(ROOT/PARENTS['R5_multiplier'][0],allow_pickle=False) as f:
            r5={k:f[k].copy() for k in f.files}
        science=analyze(native,r5)
        arrays=science.pop('arrays')
        archive=data/(name+'_Noether_Schur_12_L12.npz')
        with archive.open('xb') as f:
            np.savez_compressed(f,**arrays);f.flush();os.fsync(f.fileno())
        digest=sha(archive)
        with archive.with_name(archive.name+'.sha256').open('x') as f:
            f.write(digest+'  '+archive.name+'\n');f.flush();os.fsync(f.fileno())
        doc.update({
          'classification':'PASS_RANK_TWO_NONLOCAL_NOETHER_HESSIAN_AND_CONDITIONAL_FROZEN_U1_SYMBOL',
          'scientific_scope':'STATIC_FIXED_NOETHER_EXACT; LOCAL_FROZEN_TWO_U1_ONLY_HYPOTHETICAL',
          'science':science,
          'archive':{'path':str(archive.relative_to(ROOT)),'sha256':digest,'keys':sorted(arrays)},
          'decision':'DO_NOT_IDENTIFY_R10_CHI_WITH_FULL_LORENTZIAN_LOCAL_KINETIC_HESSIAN; COMPLETE_ACTION_UNSPECIFIED',
          'qualified_full_gravity_bridge_survivors':[],
        })
        status=0
    except Exception as exc:
        doc['error']=str(exc);doc['traceback']=traceback.format_exc()
        doc['decision']='PRESERVE_FAILURE_NO_PROMOTION'
    raw=(json.dumps(doc,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with path.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    digest=hashlib.sha256(raw).hexdigest()
    with path.with_name(path.name+'.sha256').open('x') as f:
        f.write(digest+'  '+path.name+'\n');f.flush();os.fsync(f.fileno())
    lines=[
      'RESULT_JSON='+str(path),'RESULT_SHA256='+digest,
      'CLASSIFICATION='+doc['classification'],
      'NOETHER_ARCHIVE='+doc.get('archive',{}).get('path','NONE'),
      'NOETHER_ARCHIVE_SHA256='+doc.get('archive',{}).get('sha256','NONE'),
      'FULL_LORENTZIAN_HEALTH=NOT_CERTIFIED','EARTH_CRAFT_GRAVITY=NOT_DERIVED',
      'GAMMA1_01_AUTHORIZED=NO','006D_REPLACED=NO','RETURN_CODE='+str(status),
    ]
    log=logs/(name+'.log')
    with log.open('x') as f:f.write('\n'.join(lines)+'\n');f.flush();os.fsync(f.fileno())
    print('\n'.join(lines),flush=True)
    return status

if __name__=='__main__':raise SystemExit(main())
