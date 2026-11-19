"""GAMMA1-00R5 original-action lattice-multiplier / covariant identity gate."""
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
from antigravity_research.gamma1.gamma1_00r5_multiplier import (
  sha,load_profile,reconstruct_lattice_multiplier,exact_covariant_necessary_identities,
  exact_topological_bianchi,PH16_SHA,R3_PROFILE_SHA,
)
PARENTS={
 'PH16_source':('src/antigravity_research/ph16/ph16_04_joint_stationary.py',PH16_SHA),
 'R3_result':('results/data/gamma1_00r3_20261119T001454764826Z.json','192fb12a39294dfea3035605375aab6cd5591d1fb51ddbce8924ca78aa041287'),
 'R3_verification':('results/data/gamma1_00r3_verification_20261119T002902463013Z.json','a7014cfc54de6a4d0048239a897cb73b7f5db4e25d897e70c9a2c259e0f98a8c'),
 'R3_profile':('results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',R3_PROFILE_SHA),
 'R4R1_verification':('results/data/gamma1_00r4r1_verification_20261119T022355350163Z.json','292c5fe396d2d448467346e5d1d7e06f76497dc3da5b504777232c9dd4b251b8'),
}
SOURCES=[
 'src/antigravity_research/gamma1/gamma1_00r5_multiplier.py',
 'simulations/gamma1/gamma1_00r5_run.py',
 'tests/gamma1/test_gamma1_00r5.py',
 'tests/gamma1/verify_gamma1_00r5.py',
 'theory/gamma1/GAMMA1_00R5_SAME_ACTION_PORTAL_MULTIPLIER_LEDGER.md',
]


def parents_check():
    for k,(rel,expected) in PARENTS.items():
        path=ROOT/rel
        if sha(path)!=expected:
            raise RuntimeError('PARENT_SHA_DRIFT '+k)
        if path.suffix!='.py':
            side=path.with_name(path.name+'.sha256')
            if not side.is_file() or side.read_text().strip()!=expected+'  '+path.name:
                raise RuntimeError('PARENT_SIDECAR_DRIFT '+k)
    r3=json.loads((ROOT/PARENTS['R3_result'][0]).read_text())
    v3=json.loads((ROOT/PARENTS['R3_verification'][0]).read_text())
    v4=json.loads((ROOT/PARENTS['R4R1_verification'][0]).read_text())
    if r3['classification']!='PASS_SINGLE_MESH_REPLAY_MATCHED_SCOPED_ACTION_CONTRACT' or r3['native_profile_archive']['sha256']!=R3_PROFILE_SHA:
        raise RuntimeError('R3 provenance inconsistency')
    if v3['full_regression_passed']!=3033 or v3['result_sha256']!=PARENTS['R3_result'][1]:
        raise RuntimeError('R3 verification inconsistency')
    if v4['full_regression_passed']!=3072 or v4['original_R4_result_sha256']!='fc33edeec61f3e0e5c4b260b5aa5151328213356d9187eb7fab615f180ee278d':
        raise RuntimeError('R4R1 verification inconsistency')
    if not (r3['006D_replaced'] is False and v4['006D_replaced'] is False and v4['GAMMA1_01_authorized'] is False):
        raise RuntimeError('Historical physical claim changed')
    for rel,expected in r3['producer_shas'].items():
        if sha(ROOT/rel)!=expected:
            raise RuntimeError('R3 producing source modified: '+rel)
    return {'five_raw_parent_hashes':'PASS','R3_producing_sources':'PASS','R4R1_regression':3072}


def main():
    now=dt.datetime.now(dt.timezone.utc)
    name='gamma1_00r5_'+now.strftime('%Y%m%dT%H%M%S%fZ')
    data=ROOT/'results/data';logs=ROOT/'results/logs'
    data.mkdir(parents=True,exist_ok=True);logs.mkdir(parents=True,exist_ok=True)
    output=data/(name+'.json');side=data/(name+'.json.sha256');log=logs/(name+'.log')
    result={
      'branch':'GAMMA1-00R5','timestamp_utc':now.isoformat(),
      'classification':'FAILED_OR_INCOMPLETE',
      'parents':{k:{'path':rel,'expected':expected,'actual':sha(ROOT/rel)} for k,(rel,expected) in PARENTS.items()},
      'source_shas':{p:sha(ROOT/p) for p in SOURCES},
      'PH16_replay':'NOT_RUN','Einstein_metric':'NOT_SOLVED',
      'complete_covariant_action':'NOT_CLOSED',
      'full_Lorentzian_health':'NOT_CERTIFIED',
      'Earth_down':'NOT_DERIVED','whole_craft_up':'NOT_DERIVED',
      'complete_energy_lt10MJ':'NOT_CERTIFIED',
      'GAMMA1_01_authorized':False,'PH16_05_authorized':False,
      'PH17_authorized':False,'006D_replaced':False,
    }
    status=2
    try:
        result['parent_chain']=parents_check()
        if 'MISSING' in result['source_shas'].values():
            raise RuntimeError('R5 producing source missing')
        profile=load_profile(ROOT/PARENTS['R3_profile'][0])
        analysis=reconstruct_lattice_multiplier(profile)
        cov=exact_covariant_necessary_identities()
        bianchi=exact_topological_bianchi()
        if not (all(cov.values()) and all(bianchi.values())):
            raise RuntimeError('Exact necessary identity failed')
        summ=analysis['summary']
        if not (summ['lattice_multiplier_negative_cells']==288 and summ['sigma_prime_positive_cells']==288):
            raise RuntimeError('Unexpected on-background multiplier sign; inspect raw result')
        if max(summ['X_total_norm'],summ['Y_total_norm'])>=1e-6:
            raise RuntimeError('On-background X/Y stationarity failed')
        npz=data/(name+'_lattice_multiplier_12_L12.npz')
        with npz.open('xb') as f:
            np.savez_compressed(f,**analysis['arrays']);f.flush();os.fsync(f.fileno())
        npzsha=sha(npz)
        with npz.with_name(npz.name+'.sha256').open('x') as f:
            f.write(npzsha+'  '+npz.name+'\n');f.flush();os.fsync(f.fileno())
        result.update({
          'classification':'PASS_ACTUAL_LATTICE_MULTIPLIER_AND_SCOPED_COVARIANT_IDENTITIES',
          'scientific_scope':'PH16_NATIVE_ROUTHIAN_PLUS_FORMAL_UNIVERSAL_METRIC_IDENTITIES',
          'exact_covariant_necessary_identities':cov,
          'exact_offshell_two_U1_Bianchi_and_topological_controls':bianchi,
          'canonical_lattice_results':summ,
          'derived_multiplier_archive':{'path':str(npz.relative_to(ROOT)),'sha256':npzsha,'keys':sorted(analysis['arrays'])},
          'lattice_lambda_vs_covariant_lambda':'NOT_IDENTIFIED_DIFFERENT_ACTION_LEVELS',
          'Earth_support_EOS':'UNSPECIFIED',
          'true_exterior':'NOT_CERTIFIED',
          'SI_normalization':'NOT_SUPPLIED',
          'physical_survivors':[],
          'next_decision':'REQUIRE_COMPLETE_LORENTZIAN_ACTION_BEFORE_EINSTEIN_RESPONSE_OR_NEW_PDE',
        })
        status=0
    except Exception as exc:
        result['error']=str(exc);result['traceback']=traceback.format_exc()
        result['next_decision']='STOP_PRESERVE_FAILURE_NO_PROMOTION'
    raw=(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    with output.open('xb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
    digest=hashlib.sha256(raw).hexdigest()
    with side.open('x') as f:f.write(digest+'  '+output.name+'\n');f.flush();os.fsync(f.fileno())
    info=['RESULT_JSON='+str(output),'RESULT_SHA256='+digest,
          'CLASSIFICATION='+result['classification'],
          'MULTIPLIER_ARCHIVE='+result.get('derived_multiplier_archive',{}).get('path','NONE'),
          'MULTIPLIER_SHA256='+result.get('derived_multiplier_archive',{}).get('sha256','NONE'),
          'FULL_LORENTZIAN_HEALTH=NOT_CERTIFIED','EARTH_DOWN_WHOLE_CRAFT_UP=NOT_DERIVED',
          '006D_REPLACED=NO','RETURN_CODE='+str(status)]
    with log.open('x') as f:f.write('\n'.join(info)+'\n');f.flush();os.fsync(f.fileno())
    print('\n'.join(info),flush=True)
    return status

if __name__=='__main__':raise SystemExit(main())
