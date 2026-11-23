"""Sealed versioned toy response + failure-memory research run and verifier."""
import argparse
from datetime import datetime,timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import secrets
import sys
import tempfile

from . import response_v7, response_check_v7, planner_v8

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT/'results/gravity2/research_v8_runs'
SCHEMA = 'gravity2.research.v8'
RUN_RE = re.compile(r'g2research8_\d{8}T\d{6}Z_[a-f0-9]{8}\Z')
SOURCES = ('response_v7.py','response_check_v7.py','planner_v8.py','research_v8.py')
PARENTS = {
  '006D':('simulations/006d_finite_thickness_conserved_source.py','e303b3bb454d19cc16516e189e6db559d1812dad733f9e02bf1ecafce2594d76'),
  'v4_science':('results/gravity2/campaign_v4_runs/g2camp4_20261121T184146Z_73cb7751/science.json','2e631798707cb18237f97b9e171b56e5d2c2183f2d87dff0758c99f789b6068c'),
  'v4_review':('results/gravity2/campaign_v4_runs/g2camp4_20261121T184146Z_73cb7751/verification.json','b61ebb4cad5abc4bea29404fa35c9c3174c51b1c1d1afb8d5b30e4d42321cd30'),
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def serialize(obj):
    return (json.dumps(obj,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()


def source_locks():
    paths=[Path(__file__).parent/name for name in SOURCES]
    paths.append(ROOT/'tests/gravity2/test_research_v8.py')
    if any(not p.is_file() or p.is_symlink() for p in paths):
        raise ValueError('RESEARCH_SOURCE_MISSING')
    return {str(p.relative_to(ROOT)):digest(p) for p in paths}


def parent_locks():
    locks={}
    for name,(rel,expected) in PARENTS.items():
        p=ROOT/rel
        if not p.is_file() or p.is_symlink() or digest(p)!=expected:
            raise ValueError('PINNED_PARENT_DRIFT:'+name)
        locks[name]={'path':rel,'sha256':expected}
    from . import registry_v6
    snap,head=registry_v6._snapshot(registry_v6.BASE,registry_v6._baseline())
    if snap['tasks']:
        raise ValueError('UNINTEGRATED_NEW_PHYSICS_GATE_HOLD')
    locks['registry_v6']={'head_sha256':head,'registered_tasks':0}
    return locks


def request_input(path):
    if path is None:
        return {'schema':'gravity2.research.request.v8',
                'model':response_v7.example(),'cards':[]}
    p=Path(path)
    if p.is_symlink() or not p.is_file() or p.stat().st_size>32768:
        raise ValueError('UNSAFE_RESEARCH_REQUEST')
    doc=json.loads(p.read_bytes())
    if not isinstance(doc,dict) or set(doc)!={'schema','model','cards'} or doc['schema']!='gravity2.research.request.v8':
        raise ValueError('INVALID_RESEARCH_REQUEST')
    return doc


def compute(request):
    result=response_v7.compute(request['model'])
    checks=response_check_v7.review(request['model'],result)
    plan=planner_v8.select(result,checks,request['cards'])
    return {'status':'PASS_SCOPED_RESEARCH_NO_GRAVITY','response':result,
            'independent_checks':checks,'plan':plan,
            'physical_source':'NOT_DERIVED','Einstein_gravity':'NOT_DERIVED',
            'neutral_torus_1g_1m':'NOT_DERIVED','whole_craft_lift':'NOT_DERIVED',
            'complete_energy_under_10MJ':'NOT_CERTIFIED',
            '006D_replaced':False,'new_physics_experiments':0}


def immutable(path,data):
    if path.exists() or path.is_symlink():
        raise ValueError('IMMUTABLE_EVIDENCE_EXISTS')
    fd,tmp=tempfile.mkstemp(dir=path.parent,prefix='.staged_')
    try:
        with os.fdopen(fd,'wb') as stream:
            stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.link(tmp,path)
        dfd=os.open(str(path.parent),os.O_RDONLY)
        try:os.fsync(dfd)
        finally:os.close(dfd)
    finally:Path(tmp).unlink(missing_ok=True)


def locate(rid):
    if not isinstance(rid,str) or not RUN_RE.fullmatch(rid):
        raise ValueError('INVALID_RUN_ID')
    return BASE/rid


def verify(folder):
    try:
        if folder.is_symlink() or not folder.is_dir() or not RUN_RE.fullmatch(folder.name):
            raise ValueError('UNSAFE_RUN_FOLDER')
        paths=[folder/p for p in ('manifest.json','science.json','hashes.sha256')]
        if any(not p.is_file() or p.is_symlink() for p in paths):
            raise ValueError('EVIDENCE_FILE_MISSING')
        ledger=dict(line.split('  ',1)[::-1] for line in paths[2].read_text().splitlines())
        for p in paths[:2]:
            if ledger.get(p.name)!=digest(p):
                raise ValueError('HASH_LEDGER_DRIFT:'+p.name)
        manifest=json.loads(paths[0].read_text())
        result=json.loads(paths[1].read_text())
        if (manifest['schema']!=SCHEMA or manifest['run_id']!=folder.name or
            manifest['sources']!=source_locks() or manifest['parents']!=parent_locks()):
            raise ValueError('PROVENANCE_DRIFT')
        if result!=compute(manifest['request']):
            raise ValueError('INDEPENDENT_RECOMPUTATION_DRIFT')
        verdict={'status':'PASS_SCOPED_RESEARCH_NO_LIFT','run_id':folder.name,
                 'manifest_sha256':digest(paths[0]),'science_sha256':digest(paths[1]),
                 'review_checks':len(result['independent_checks']),
                 'physical_gravity':False}
        dst=folder/'verification.json'
        enc=serialize(verdict)
        if dst.exists():
            if dst.is_symlink() or dst.read_bytes()!=enc:
                raise ValueError('VERIFICATION_IMMUTABILITY_HOLD')
        else:
            immutable(dst,enc)
            immutable(folder/'verification.sha256',(digest(dst)+'  verification.json\n').encode())
        if ((folder/'verification.sha256').read_text().strip()!=digest(dst)+'  verification.json'):
            raise ValueError('VERIFICATION_LEDGER_DRIFT')
        print('GRAVITY2_V8_VERIFY=PASS_SCOPED_RESEARCH_NO_LIFT')
        print('VERIFICATION_SHA256='+digest(dst))
        return 0
    except (OSError,ValueError,TypeError,KeyError,AssertionError) as exc:
        print('GRAVITY2_V8_HOLD='+repr(exc),file=sys.stderr)
        return 3


def run(path=None,dry=False):
    request=request_input(path)
    science=compute(request)
    parents=parent_locks()
    sources=source_locks()
    if dry:
        print('GRAVITY2_V8_DRY_RUN=PASS_WRITES_NONE')
        print('NEXT_GATE='+science['plan']['next_gate'])
        return 0
    rid=datetime.now(timezone.utc).strftime('g2research8_%Y%m%dT%H%M%SZ_')+secrets.token_hex(4)
    if BASE.is_symlink():raise ValueError('UNSAFE_RUN_BASE')
    BASE.mkdir(parents=True,exist_ok=True,mode=0o700)
    folder=locate(rid)
    folder.mkdir(mode=0o700)
    manifest={'schema':SCHEMA,'run_id':rid,'request':request,'sources':sources,
              'parents':parents,'physical_scope':'TOY_AND_UNVERIFIED_PLAN_ONLY'}
    immutable(folder/'manifest.json',serialize(manifest))
    immutable(folder/'science.json',serialize(science))
    immutable(folder/'hashes.sha256', ''.join(digest(folder/name)+'  '+name+'\n' for name in ('manifest.json','science.json')).encode())
    print('GRAVITY2_V8_RUN='+rid)
    print('NEXT_GATE='+science['plan']['next_gate'])
    print('PHYSICAL_GRAVITY=NOT_DERIVED')
    return verify(folder)


def main(argv=None):
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('run');a.add_argument('--input');a.add_argument('--dry-run',action='store_true')
    b=sub.add_parser('verify');b.add_argument('--run-id',required=True)
    args=p.parse_args(argv)
    try:
        return run(args.input,args.dry_run) if args.cmd=='run' else verify(locate(args.run_id))
    except (OSError,ValueError,TypeError,KeyError) as exc:
        print('GRAVITY2_V8_HOLD='+repr(exc),file=sys.stderr)
        return 3


if __name__=='__main__':
    raise SystemExit(main())
