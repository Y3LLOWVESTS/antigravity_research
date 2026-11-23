"""GRAVITY2-06 bounded stationary-source/Gauss sourceability gate.

No AGMINER source import, no legacy writes, no PDE. Soft watchdog limits.
Existing GRAVITY2 code/checkpoint files are not modified.
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

from .engine import ROOT, atomic_json, atomic_text, digest, bytes_under
from .policy import PRESETS, GLOBAL_MIB
from .miner import supervise, _rss_available
from .action01_core import read_pinned
from . import bridge06_core as physics

BASE = ROOT / 'results/gravity2/bridge06_runs'
RUN_RE = re.compile(r'g206_\d{8}T\d{6}Z_[0-9a-f]{8}\Z')
SOURCES = ('bridge06_core.py', 'bridge06.py', 'bridge06_check.py')
MIB = 1024*1024
PARENTS = {
    'G05_SCIENCE': (
        'results/gravity2/bridge05_runs/g205_20261121T050912Z_42b36ffa/science.json',
        '38abeec2b2672d5c7b29c13fef1862d3301f1dfcad986c293933b5c6e2fc08ce'),
    'G05_INDEPENDENT': (
        'results/gravity2/bridge05_runs/g205_20261121T050912Z_42b36ffa/verification.json',
        'a718c7fb52c63be198a4b897259ad15d073c58c3ed838bb2a08f14aff740a2ac'),
}


def location(rid):
    if not RUN_RE.fullmatch(rid):
        raise ValueError('invalid GRAVITY2-06 run ID')
    return BASE/rid


def producer_hashes():
    pkg=Path(__file__).resolve().parent
    return {name:digest(pkg/name) for name in SOURCES}


def locks():
    previous={}
    for key,(rel,expected) in PARENTS.items():
        path=ROOT/rel
        actual=digest(path) if path.is_file() and not path.is_symlink() else None
        previous[key]={
            'path':rel, 'expected_sha256':expected,
            'actual_sha256':actual, 'status':'MATCH' if actual==expected else 'HOLD',
        }
    old,_=read_pinned(ROOT)
    return {
        'previous':previous,
        'historical':old,
        'all_match':all(x['status']=='MATCH' for x in previous.values())
                    and all(x['status']=='MATCH' for x in old.values()),
    }


def run(args):
    if args.level != 'L0' or args.workers != 1:
        raise ValueError('GRAVITY2-06 only L0/one worker; L1-L4 disabled')
    cap,ram,disk=PRESETS[args.preset]
    secs=60*args.minutes
    if not math.isfinite(secs) or not 0<secs<=cap:
        raise ValueError('minutes not within preset limit')
    if args.dry_run:
        print(json.dumps({
            'program':'GRAVITY2-06', 'scope':'REDUCED_STATIONARY_GAUSS_SUPPORT_GATE',
            'seconds_cap':secs, 'workers':1, 'rss_soft_mib':ram,
            'disk_soft_mib':disk, 'PDE':'DISABLED',
            'writes':False, 'legacy_AGMINER':'READ_ONLY_HASH',
        },indent=2))
        return 0
    if not _rss_available():
        raise ValueError('psutil required for worker memory watchdog')
    if bytes_under(ROOT/'results/gravity2') > (GLOBAL_MIB-disk)*MIB:
        raise ValueError('GRAVITY2 global disk reserve exceeded; no pruning')
    parent=locks()
    BASE.mkdir(parents=True,exist_ok=True,mode=0o700)
    rid=datetime.now(timezone.utc).strftime('g206_%Y%m%dT%H%M%SZ_')+secrets.token_hex(4)
    folder=location(rid)
    folder.mkdir(mode=0o700)
    manifest={
        'program':'GRAVITY2-06', 'run_id':rid,
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'preset':args.preset, 'seconds':secs, 'level':'L0',
        'workers':1, 'rss_soft_mib':ram, 'disk_soft_mib':disk,
        'producer_sha256':producer_hashes(),
        'legacy_AGMINER':'READ_ONLY_HASH_NO_EXECUTION',
        'prior_GRAVITY2_modifications':'NONE',
        'scope':'NOT_FULL_R3B_SOURCE_OR_EINSTEIN',
    }
    atomic_json(folder/'manifest.json', manifest)
    status='PARENT_HOLD'
    worker_log=''
    elapsed=0.
    peak=None
    exitcode=None
    evidence=None
    if parent['all_match']:
        env=dict(os.environ)
        env.update({
            'PYTHONPATH':str(ROOT/'src'), 'PYTHONDONTWRITEBYTECODE':'1',
            'OPENBLAS_NUM_THREADS':'1', 'OMP_NUM_THREADS':'1',
            'MKL_NUM_THREADS':'1', 'VECLIB_MAXIMUM_THREADS':'1',
        })
        child=subprocess.Popen([
            sys.executable,'-m','antigravity_research.gravity2.bridge06',
            '_worker','--output',str(folder/'_worker.json'),
        ],cwd=ROOT,env=env,stdin=subprocess.DEVNULL,
          stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
        start=time.monotonic()
        status,exitcode,peak,worker_log,_=supervise(child,folder,start+secs,ram,disk)
        elapsed=round(time.monotonic()-start,5)
        if status=='COMPLETED' and exitcode==0:
            try:
                evidence=json.loads((folder/'_worker.json').read_text())
            except (OSError,ValueError):
                status='WORKER_BAD_JSON'
        elif status=='COMPLETED':
            status='WORKER_ERROR'
        (folder/'_worker.json').unlink(missing_ok=True)
    atomic_text(folder/'worker.log',worker_log[-2048:])
    if evidence is None:
        evidence={'decision':'INCOMPLETE_NO_SCIENCE','qualified_survivors':0}
    science={
        'program':'GRAVITY2-06', 'run_id':rid, 'execution_status':status,
        'parent_locks':parent, 'evidence':evidence,
        'full_action':'NOT_DERIVED', 'real_source':'NOT_ESTABLISHED',
        'neutral_1kg_lift':'NOT_DERIVED', 'whole_craft_lift':'NOT_DERIVED',
        'complete_energy_SI':'NOT_CERTIFIED', '006D_replaced':False,
        'qualified_survivors':0, 'loaded_PDE':'NOT_AUTHORIZED',
        'full_regression':'NOT_RUN',
        'resource':{'elapsed_s':elapsed,'worker_peak_rss_mib':peak,
                    'exit_code':exitcode,'watchdog':'SOFT_PSUTIL_PROCESS'},
    }
    atomic_json(folder/'science.json', science)
    atomic_text(folder/'hashes.sha256',
                digest(folder/'manifest.json')+'  manifest.json\n'+
                digest(folder/'science.json')+'  science.json\n')
    print('GRAVITY2_06_RUN='+rid)
    print('EXECUTION='+status)
    print('PARENTS='+('LOCKED' if parent['all_match'] else 'HOLD'))
    print('DECISION='+evidence['decision'])
    print('PHYSICAL_SURVIVORS=0; LOADED_PDE=NOT_AUTHORIZED')
    print('SCIENCE_SHA256='+digest(folder/'science.json'))
    return 0 if status=='COMPLETED' else 3


def main(argv=None):
    p=argparse.ArgumentParser(prog='gravity2.bridge06')
    subs=p.add_subparsers(dest='command',required=True)
    r=subs.add_parser('run')
    r.add_argument('--level',choices=('L0','L1','L2','L3','L4'),default='L0')
    r.add_argument('--preset',choices=tuple(PRESETS),default='quick')
    r.add_argument('--minutes',type=float,default=.5)
    r.add_argument('--workers',type=int,default=1)
    r.add_argument('--dry-run',action='store_true')
    for command in ('verify','report'):
        subs.add_parser(command).add_argument('--run-id',required=True)
    w=subs.add_parser('_worker'); w.add_argument('--output',required=True)
    args=p.parse_args(argv)
    try:
        if args.command=='run':
            return run(args)
        if args.command=='_worker':
            target=Path(args.output)
            if (target.name!='_worker.json' or not RUN_RE.fullmatch(target.parent.name)
                    or target.parent.parent.resolve()!=BASE.resolve()):
                raise ValueError('worker output outside GRAVITY2-06')
            atomic_json(target,physics.evidence())
            return 0
        folder=location(args.run_id)
        if args.command=='verify':
            from .bridge06_check import verify
            return verify(folder)
        science=json.loads((folder/'science.json').read_text())
        e=science['evidence']
        print(json.dumps({
            'run_id':args.run_id,'execution':science['execution_status'],
            'decision':e['decision'],'local_variations':e.get('local_variations'),
            'stationary_and_wall':e.get('conditional_obstructions'),
            'gates':e.get('gates'), 'complete_energy':science['complete_energy_SI'],
            'whole_craft_lift':science['whole_craft_lift'],
        },indent=2))
        return 0
    except (OSError,ValueError,KeyError,AssertionError) as exc:
        print('GRAVITY2_06_HOLD='+repr(exc),file=sys.stderr)
        return 2
    return 2

if __name__=='__main__':
    raise SystemExit(main())
