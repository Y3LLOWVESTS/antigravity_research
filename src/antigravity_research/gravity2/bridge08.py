"""GRAVITY2-08: bounded re-evaluation of *sealed* G07 fields, no PDE.

L0 source/X Gauss zero-mode and action-provenance audit. The previous
GRAVITY2-07 run and all legacy producers remain immutable. A failure of the
periodic single-sign-charge model is NOT a finite-exterior R3B no-go.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import time

import numpy as np

from .engine import ROOT, atomic_json, atomic_text, digest, bytes_under
from .policy import PRESETS, GLOBAL_MIB
from .miner import supervise, _rss_available
from .action01_core import read_pinned
from . import bridge08_core as physics

BASE=ROOT/'results/gravity2/bridge08_runs'
PARENT_DIR='results/gravity2/bridge07_runs/g207_20261121T065202Z_450b9280'
PARENTS={
  'G07_MANIFEST':(PARENT_DIR+'/manifest.json','b54dabfb4463af6a40fac60e541d6c69bb5d843c6bc29ff83f1b469f267a3b38'),
  'G07_SCIENCE':(PARENT_DIR+'/science.json','458d7309da70a944380f8fc73cb1b93f19e80b981ed64d1f97c64c62cabd04d1'),
  'G07_VERIFICATION':(PARENT_DIR+'/verification.json','c82f313b55effd19d90fca9b2306aca104d96296369011262a0ee07cbe113379'),
  'G07_FIELDS':(PARENT_DIR+'/fields.npz','ee9c9557d6d30897d8ed3a4872b11bc464c17af37d98f87c4047884bb0bcc46d'),
}
SOURCE_NAMES=(
    'src/antigravity_research/gravity2/bridge08_core.py',
    'src/antigravity_research/gravity2/bridge08.py',
    'src/antigravity_research/gravity2/bridge08_check.py',
    'tests/gravity2/test_bridge08.py',
)
RUN_RE=re.compile(r'g208_\d{8}T\d{6}Z_[0-9a-f]{8}\Z')
MIB=1024*1024


def owned(run_id):
    if not RUN_RE.fullmatch(run_id):
        raise ValueError('invalid GRAVITY2-08 run ID')
    return BASE/run_id


def source_hashes():
    return {name:digest(ROOT/name) for name in SOURCE_NAMES}


def parents():
    locks={}
    for name,(relative,sha) in PARENTS.items():
        file=ROOT/relative
        actual=digest(file) if file.is_file() and not file.is_symlink() else None
        locks[name]={'path':relative,'expected_sha256':sha,'actual_sha256':actual,
                     'status':'MATCH' if actual==sha else 'HOLD'}
    historical,_=read_pinned(ROOT)
    parent_manifest=ROOT/PARENT_DIR/'manifest.json'
    code=[]
    if parent_manifest.is_file():
        manifest=json.loads(parent_manifest.read_text())
        for filename,sha in manifest.get('producer_sha256',{}).items():
            path=ROOT/filename
            actual=digest(path) if path.is_file() and not path.is_symlink() else None
            code.append({'path':filename,'expected_sha256':sha,
                         'actual_sha256':actual,'status':'MATCH' if sha==actual else 'HOLD'})
    return {'previous':locks,'prior_source_code':code,'historical':historical,
            'all_match':all(x['status']=='MATCH' for x in locks.values())
                        and len(code)==4 and all(x['status']=='MATCH' for x in code)
                        and all(x['status']=='MATCH' for x in historical.values())}


def worker(path):
    target=Path(path)
    if (target.name!='_worker.json' or not RUN_RE.fullmatch(target.parent.name)
            or target.parent.parent.resolve()!=BASE.resolve()):
        raise ValueError('unsafe worker output path')
    with np.load(ROOT/PARENT_DIR/'fields.npz',allow_pickle=False) as arrays:
        result=physics.scientific_evidence(arrays)
    atomic_json(target,result)


def run(args):
    if args.level!='L0' or args.workers!=1:
        raise ValueError('GRAVITY2-08 L0 single worker only; L1-L4 disabled')
    max_sec,ram,disk=PRESETS[args.preset]
    seconds=args.minutes*60
    if not math.isfinite(seconds) or not 0<seconds<=min(max_sec,30):
        raise ValueError('GRAVITY2-08 time ceiling is 30 seconds')
    if args.dry_run:
        print(json.dumps({'program':'GRAVITY2-08','level':'L0',
              'source':'SEALED_G07_FIELDS_READ_ONLY','seconds_cap':seconds,
              'workers':1,'rss_soft_mib':ram,'disk_soft_mib':disk,
              'L1_L4':'LOCKED','writes':False},indent=2))
        return 0
    if not _rss_available():
        raise ValueError('psutil watchdog missing')
    if bytes_under(ROOT/'results/gravity2')>(GLOBAL_MIB-disk)*MIB:
        raise ValueError('GRAVITY2 disk budget exceeded')
    locks=parents()
    BASE.mkdir(parents=True,exist_ok=True,mode=0o700)
    run_id=datetime.now(timezone.utc).strftime('g208_%Y%m%dT%H%M%SZ_')+secrets.token_hex(4)
    folder=owned(run_id)
    folder.mkdir(mode=0o700)
    manifest={'program':'GRAVITY2-08','run_id':run_id,
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'level':'L0','preset':args.preset,'workers':1,
        'seconds_ceiling':seconds,'rss_soft_mib':ram,'disk_soft_mib':disk,
        'source_hashes':source_hashes(),'no_prior_source_modification':True,
        'AGMINER':'HASHED_NO_EXECUTION','model':'PERIODIC_2D_SINGLE_X_CHARGED_SCALAR'}
    atomic_json(folder/'manifest.json',manifest)
    status='PARENT_HOLD';result=None;elapsed=0.;peak=None;exitcode=None;log=''
    if locks['all_match']:
        env=os.environ.copy()
        env.update({'PYTHONPATH':str(ROOT/'src'),'PYTHONDONTWRITEBYTECODE':'1',
                    'OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1',
                    'VECLIB_MAXIMUM_THREADS':'1'})
        child=subprocess.Popen([
            sys.executable,'-m','antigravity_research.gravity2.bridge08',
            '_worker','--output',str(folder/'_worker.json')],
            cwd=ROOT,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,start_new_session=True)
        start=time.monotonic()
        status,exitcode,peak,log,_=supervise(child,folder,start+seconds,ram,disk)
        elapsed=round(time.monotonic()-start,5)
        if status=='COMPLETED' and exitcode==0:
            try:
                result=json.loads((folder/'_worker.json').read_text())
            except (ValueError,OSError):
                status='WORKER_BAD_JSON'
        elif status=='COMPLETED':
            status='WORKER_ERROR'
        (folder/'_worker.json').unlink(missing_ok=True)
    atomic_text(folder/'worker.log',log[-2048:])
    if status!='COMPLETED':
        result={'decision':'INCOMPLETE_NO_SCIENCE','physical_survivors':0}
    science={
        'program':'GRAVITY2-08','run_id':run_id,'execution_status':status,
        'parents':locks,'evidence':result,
        'source_and_X_solving':'NOT_AUTHORIZED_BECAUSE_PERIODIC_GAUSS_OBSTRUCTION',
        'external_neutralizer':'NOT_INTRODUCED','physical_finite_source':'NOT_ESTABLISHED',
        'Einstein_gravity':'NOT_SOLVED','whole_craft_lift':'NOT_DERIVED',
        'complete_energy_SI':'NOT_CERTIFIED','qualified_physical_survivors':0,
        '006D_replaced':False,'full_repository_regression':'NOT_RUN',
        'L2_authorized':False,'resource':{'elapsed_s':elapsed,
                 'worker_peak_rss_mib':peak,'exit_code':exitcode,
                 'watchdog':'SOFT_PSUTIL_PROCESS'}}
    atomic_json(folder/'science.json',science)
    atomic_text(folder/'hashes.sha256', ''.join(digest(folder/n)+'  '+n+'\n'
               for n in ('manifest.json','science.json')))
    print('GRAVITY2_08_RUN='+run_id)
    print('EXECUTION='+status)
    print('PARENTS='+('LOCKED' if locks['all_match'] else 'HOLD'))
    print('DECISION='+result['decision'])
    if status=='COMPLETED':
        for row in result['rows']:
            print('N='+str(row['n'])+' Q_X='+str(row['charge_integral_canonical'])
               +' E_X_RMS='+str(row['X_euler_rms'])
               +' E_F_RMS='+str(row['scalar_euler_rms'])
               +' E_Y_RMS='+str(row['Y_euler_rms']))
    print('PHYSICAL_SURVIVORS=0; FULL_GRAVITY=NOT_SOLVED')
    print('SCIENCE_SHA256='+digest(folder/'science.json'))
    return 0 if status=='COMPLETED' else 3


def main(argv=None):
    p=argparse.ArgumentParser(prog='gravity2.bridge08')
    sub=p.add_subparsers(dest='command',required=True)
    a=sub.add_parser('run')
    a.add_argument('--level',choices=('L0','L1','L2','L3','L4'),default='L0')
    a.add_argument('--preset',choices=tuple(PRESETS),default='quick')
    a.add_argument('--minutes',type=float,default=.5)
    a.add_argument('--workers',type=int,default=1)
    a.add_argument('--dry-run',action='store_true')
    for cmd in ('verify','report'):
        sub.add_parser(cmd).add_argument('--run-id',required=True)
    w=sub.add_parser('_worker');w.add_argument('--output',required=True)
    args=p.parse_args(argv)
    try:
        if args.command=='run':return run(args)
        if args.command=='_worker':worker(args.output);return 0
        folder=owned(args.run_id)
        if args.command=='verify':
            from .bridge08_check import verify
            return verify(folder)
        science=json.loads((folder/'science.json').read_text())
        print(json.dumps({'run_id':args.run_id,'execution':science['execution_status'],
            'decision':science['evidence']['decision'],
            'rows':science['evidence'].get('rows'),
            'claim':'NOT_PHYSICAL_SOURCE_OR_LIFT'},indent=2))
        return 0
    except (OSError,ValueError,RuntimeError,KeyError,AssertionError) as exc:
        print('GRAVITY2_08_HOLD='+repr(exc),file=sys.stderr)
        return 2
    return 2

if __name__=='__main__':
    raise SystemExit(main())
