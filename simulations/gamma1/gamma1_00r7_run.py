"""GAMMA1-00R7 immutable parent-hash locked Green/Maxwell weak-form audit."""
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
from antigravity_research.gamma1.gamma1_00r7_green_fv import (
    sha, analyze, PH16_SHA,P8_SHA,P10_SHA,R3_SHA,R6_SHA,R6_VERIFY_SHA,
)
PARENTS={
 'PH16_source':('src/antigravity_research/ph16/ph16_04_joint_stationary.py',PH16_SHA),
 'P10_ring_source':('src/antigravity_research/agminer/hook17_ph15_p10_free_space.py',P10_SHA),
 'P8_FV_source':('src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py',P8_SHA),
 'R3_native':('results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',R3_SHA),
 'R6_result':('results/data/gamma1_00r6_20261119T032110913285Z.json',R6_SHA),
 'R6_verification':('results/data/gamma1_00r6_verification_20261119T034852957987Z.json',R6_VERIFY_SHA),
}
SOURCES=[
 'src/antigravity_research/gamma1/gamma1_00r7_green_fv.py',
 'simulations/gamma1/gamma1_00r7_run.py',
 'tests/gamma1/test_gamma1_00r7.py',
 'tests/gamma1/verify_gamma1_00r7.py',
 'theory/gamma1/GAMMA1_00R7_GREEN_TO_MAXWELL_WEAK_FORM_LEDGER.md',
]


def parent_check():
    for key,(rel,expected) in PARENTS.items():
        file=ROOT/rel
        if sha(file)!=expected:
            raise RuntimeError('PARENT_HASH_DRIFT_'+key)
        if file.suffix in ('.json','.npz'):
            s=file.with_name(file.name+'.sha256')
            if not s.is_file() or s.read_text().strip()!=expected+'  '+file.name:
                raise RuntimeError('PARENT_SIDECAR_DRIFT_'+key)
    d=json.loads((ROOT/PARENTS['R6_result'][0]).read_text())
    v=json.loads((ROOT/PARENTS['R6_verification'][0]).read_text())
    if (d['classification']!='PASS_RESTRICTED_STATIC_TRACE_AND_FAIL_NODAL_MAXWELL_MATCH'
        or v['classification']!='RESTRICTED_TRACE_MATCH_AND_NODAL_MAXWELL_MISMATCH_INDEPENDENTLY_VERIFIED'
        or v['full_regression_passed']!=3107 or v['scientific_result_sha256']!=R6_SHA
        or d['GAMMA1_01_authorized'] is not False or d['006D_replaced'] is not False):
        raise RuntimeError('R6_PARENT_CONTRACT_DRIFT')
    for rel,expected in d['producing_sources'].items():
        if sha(ROOT/rel)!=expected:
            raise RuntimeError('R6_PRODUCER_MODIFIED_'+rel)
    return 'SIX_PARENTS_R6_PRODUCER_CHAIN_VERIFIED'


def main():
    now=dt.datetime.now(dt.timezone.utc)
    tag='gamma1_00r7_'+now.strftime('%Y%m%dT%H%M%S%fZ')
    data=ROOT/'results/data';logs=ROOT/'results/logs'
    data.mkdir(parents=True,exist_ok=True);logs.mkdir(parents=True,exist_ok=True)
    out=data/(tag+'.json');side=out.with_name(out.name+'.sha256');log=logs/(tag+'.log')
    result={
      'branch':'GAMMA1-00R7','timestamp_utc':now.isoformat(),
      'classification':'FAILED_OR_INCOMPLETE',
      'parent_hashes':{k:{'path':r,'expected':h,'actual':sha(ROOT/r)} for k,(r,h) in PARENTS.items()},
      'source_hashes':{r:sha(ROOT/r) for r in SOURCES},
      'original_PH16_source_replay':'NOT_RUN',
      'continuum_Maxwell_bridge':'NOT_CERTIFIED','full_covariant_action':'NOT_CLOSED',
      'Einstein_metric':'NOT_SOLVED','Lorentzian_mode_health':'NOT_CERTIFIED',
      'Earth_down':'NOT_DERIVED','whole_craft_up':'NOT_DERIVED',
      'complete_energy_lt10MJ':'NOT_CERTIFIED',
      'GAMMA1_01_authorized':False,'PH16_05_authorized':False,
      'PH17_authorized':False,'006D_replaced':False,
    }
    code=2
    try:
        result['provenance']=parent_check()
        if 'MISSING' in result['source_hashes'].values():
            raise RuntimeError('R7_SOURCE_MISSING')
        archive=ROOT/PARENTS['R3_native'][0]
        with np.load(archive,allow_pickle=False) as f:
            native={k:f[k].copy() for k in ('A_X','A_Y')}
        report=analyze(native)
        result.update({
          'classification':'PASS_WEIGHTED_FV_SMOOTH_PROBE_TREND_NATIVE_MISMATCH_OPEN',
          'science':report,
          'decision':'CONDITIONAL_SMOOTH_PROBE_CORRESPONDENCE_ONLY_REQUIRE_BOUNDARY_DTN_AND_NATIVE_OPERATOR_CONVERGENCE',
          'qualified_physical_survivors':[],
        })
        code=0
    except Exception as exc:
        result['error']=str(exc);result['traceback']=traceback.format_exc()
        result['decision']='PRESERVE_FAILURE_NO_PROMOTION'
    raw=(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with out.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    h=hashlib.sha256(raw).hexdigest()
    with side.open('x') as f:f.write(h+'  '+out.name+'\n');f.flush();os.fsync(f.fileno())
    statements=[
      'RESULT_JSON='+str(out),'RESULT_SHA256='+h,'CLASSIFICATION='+result['classification'],
      'PH16_SOURCE_REPLAY=NOT_RUN','EARTH_CRAFT_GRAVITY=NOT_DERIVED',
      'GAMMA1_01_AUTOMATIC_AUTHORIZATION=NO','006D_REPLACED=NO','RETURN_CODE='+str(code),
    ]
    with log.open('x') as f:f.write('\n'.join(statements)+'\n')
    print('\n'.join(statements),flush=True)
    return code

if __name__=='__main__':raise SystemExit(main())
