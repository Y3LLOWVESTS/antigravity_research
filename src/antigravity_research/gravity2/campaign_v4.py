"""GRAVITY2 campaign v4: resource-bounded job runner with reviewed dependencies.

The execution platform can accept new, SHA-pinned, separately verified
scientific gate providers without editing this scheduler. It does NOT create
new physical laws or bypass missing source, Earth, support or metric actions.

Run from repository root with PYTHONPATH=src. This module adds no dependency
on AGMINER implementation; it reuses GRAVITY2's previously tested watchdog.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib
import numpy as np
import json
import math
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import time

from . import campaign_science as science
from . import scientific_inputs_v3 as inputs
from . import review_contracts_v4 as contracts
from .engine import ROOT, atomic_json, atomic_text, bytes_under, digest
from .miner import _rss_available, supervise
from .policy import PRESETS, GLOBAL_MIB

PKG = Path(__file__).resolve().parent
BASE = ROOT / 'results/gravity2/campaign_v4_runs'
REGISTRY = ROOT / 'results/gravity2/campaign_registry'
RUN_RE = re.compile(r'g2camp4_\d{8}T\d{6}Z_[a-f0-9]{8}\Z')
MOD_RE = re.compile(r'[a-z][a-z0-9_]{3,64}\Z')
MIB = 1024 * 1024
PARENTS = {
    'G08_SCIENCE': (
        'results/gravity2/bridge08_runs/g208_20261121T070239Z_467d6a03/science.json',
        'a883cbe884ef97b839995da7437cf2a3d8c0451dc1415f88caf6ed314ac5e419',
    ),
    'G08_VERIFICATION': (
        'results/gravity2/bridge08_runs/g208_20261121T070239Z_467d6a03/verification.json',
        'fb14efd798d6a58472421ab611c896c974aff62f743d7666219f0cecd3d676c9',
    ),
    'G07_ARCHIVE': (
        science.FIELDS_PARENT,
        'ee9c9557d6d30897d8ed3a4872b11bc464c17af37d98f87c4047884bb0bcc46d',
    ),
}
CORE_FILES = ('campaign_science.py', 'campaign.py', 'campaign_check.py', 'campaign_v2.py', 'campaign_check_v2.py', 'campaign_v3.py', 'campaign_check_v3.py', 'scientific_inputs_v3.py', 'campaign_v4.py', 'campaign_check_v4.py', 'review_contracts_v4.py')


def locate(rid):
    if not RUN_RE.fullmatch(rid):
        raise ValueError('unsafe run ID')
    return BASE / rid


def core_hashes():
    out={n: digest(PKG / n) for n in CORE_FILES}
    out['tests/gravity2/test_campaign.py']=digest(ROOT/'tests/gravity2/test_campaign.py')
    out['tests/gravity2/test_campaign_v2.py']=digest(ROOT/'tests/gravity2/test_campaign_v2.py')
    out['tests/gravity2/test_campaign_v3.py']=digest(ROOT/'tests/gravity2/test_campaign_v3.py')
    out['tests/gravity2/test_campaign_v4.py']=digest(ROOT/'tests/gravity2/test_campaign_v4.py')
    return out


def provider_file(name):
    if not isinstance(name, str) or not MOD_RE.fullmatch(name):
        raise ValueError('unsafe provider module')
    p = PKG/(name+'.py')
    if not p.is_file() or p.is_symlink():
        raise ValueError('provider module absent or symlink')
    return p


def validate_job(job):
    if not isinstance(job, dict) or job.get('schema') != 'gravity2.campaign.task.v1':
        raise ValueError('wrong task schema')
    cid=job.get('id')
    if not isinstance(cid,str) or not re.fullmatch(r'[A-Z0-9_]{4,56}',cid):
        raise ValueError('unsafe job ID')
    candidate=job.get('candidate')
    if not isinstance(candidate,str) or not re.fullmatch(r'[A-Z0-9_]{4,64}',candidate):
        raise ValueError('unsafe candidate ID')
    if job.get('level') not in ('L0','L1','L2','L3','L4'):
        raise ValueError('unknown fidelity')
    if not isinstance(job.get('action'),dict) or not job['action']:
        raise ValueError('missing action declaration')
    if not isinstance(job.get('gate'),str) or not re.fullmatch(r'[A-Z0-9_]{4,64}',job['gate']):
        raise ValueError('unsafe gate')
    deps=job.get('requires')
    if not isinstance(deps,list) or len(deps)>10 or any(
        not isinstance(d,str) or not re.fullmatch(r'[A-Z0-9_]{4,56}',d) for d in deps
    ) or len(set(deps))!=len(deps):
        raise ValueError('invalid dependencies')
    if not isinstance(job.get('priority'),int) or not 0 <= job['priority'] <= 100:
        raise ValueError('invalid priority')
    producer, independent = job.get('module'), job.get('independent')
    for name in (producer,independent):
        provider_file(name)
    if producer == independent:
        raise ValueError('independent verifier must be a different module')
    if job.get('provider_sha256') and job['provider_sha256'] != digest(provider_file(producer)):
        raise ValueError('producer SHA drift')
    if job.get('independent_sha256') and job['independent_sha256'] != digest(provider_file(independent)):
        raise ValueError('independent source SHA drift')
    contracts.authorize_registration(job)
    if len(science.canonical(job)) > 16_384:
        raise ValueError('task manifest exceeds size bound')
    # Fidelity is an authorization question, not a time-budget flag.
    if job['level'] in ('L2','L3','L4'):
        if not job.get('physical_action_evidence'):
            raise ValueError('L2+ requires explicit independently audited action evidence')
        raise ValueError('L2-L4 integration not scientifically authorized in this release')
    if producer == 'campaign_science':
        science.validate_task(job)
    return job


def jobs():
    all_jobs = [dict(j) for j in science.default_tasks()]
    if REGISTRY.is_dir():
        for p in sorted(REGISTRY.glob('*.json')):
            if p.is_symlink() or p.stat().st_size > 16_384:
                raise ValueError('unsafe candidate registry file')
            all_jobs.append(json.loads(p.read_text()))
    ids=set()
    for j in all_jobs:
        validate_job(j)
        if j['id'] in ids:
            raise ValueError('duplicate task ID: '+j['id'])
        ids.add(j['id'])
    # At most 2 distinct source-action families per campaign.
    families={j['candidate'] for j in all_jobs}
    if len(families)>2:
        raise ValueError('more than two registered research candidates')
    for j in all_jobs:
        if j['id'] in j['requires'] or any(k not in ids for k in j['requires']):
            raise ValueError('unknown/self dependency: '+j['id'])
    pending={j['id']:set(j['requires']) for j in all_jobs}
    ordered=[]
    while pending:
        ready=sorted((k for k,v in pending.items() if not v),key=str)
        if not ready:
            raise ValueError('task dependency cycle')
        for ident in ready:
            ordered.append(ident)
            pending.pop(ident)
        for d in pending.values():
            d.difference_update(ready)
    # Stable priority ordering within DAG levels is enforced at dispatch.
    return all_jobs


def dispatch_order(selection):
    """Priority within a dependency-respecting deterministic topological order."""
    remaining={j['id']:j for j in selection}
    result=[]
    while remaining:
        visited={j['id'] for j in result}
        ready=[j for j in remaining.values() if set(j['requires']).issubset(visited)]
        if not ready:
            raise ValueError('invalid dependency ordering')
        selected=sorted(ready,key=lambda j:(-j['priority'],j['id']))[0]
        result.append(selected)
        del remaining[selected['id']]
    return result


def parent_locks():
    result={}
    for name,(rel,expected) in PARENTS.items():
        f=ROOT/rel
        actual=digest(f) if f.is_file() and not f.is_symlink() else None
        result[name]={'relative_path':rel, 'expected_sha256':expected,
                      'actual_sha256':actual,'match':actual==expected}
    return result


def fingerprint(job,parents,core):
    return science.signature({'job':job,'parents':parents,'core':core,
        'provider':digest(provider_file(job['module'])),
        'independent':digest(provider_file(job['independent'])),
        'scientific_inputs':inputs.manifest(ROOT,job)})



def reviewed_checks(job, evidence):
    """Enforce exact independently calculated review contracts."""
    contracts.authorize_registration(job)

    if not isinstance(evidence, dict):
        raise ValueError('REVIEW_EVIDENCE_TYPE')

    rule = contracts.CONTRACTS[job['gate']]

    if evidence.get('status') != rule['verdict']:
        raise ValueError('REVIEW_VERDICT')

    module = importlib.import_module(
        'antigravity_research.gravity2.' + job['independent']
    )

    raw = module.independent_check(
        job, evidence, {'root': str(ROOT)}
    )

    if not isinstance(raw, dict) or not raw:
        raise ValueError('REVIEW_MISSING')

    if not all(
        isinstance(k, str)
        and isinstance(v, (bool, np.bool_))
        for k, v in raw.items()
    ):
        raise ValueError('REVIEW_NON_BOOLEAN')

    checks = {
        k: bool(v)
        for k, v in raw.items()
    }

    return contracts.enforce(job, evidence, checks)



def parent_ready(done, ident):
    """Only an independently reviewed scientific PASS authorizes a child."""
    return any(
        item["id"] == ident
        and item.get("verification_status") == "VERIFIED"
        and item.get("scientific_verdict") == "PASS_SCOPED"
        and isinstance(item.get("review_checks"), dict)
        and bool(item["review_checks"])
        and all(
            type(value) is bool and value
            for value in item["review_checks"].values()
        )
        for item in done
    )


def certified_entry(folder, job, fp, expected_ref=None):
    """Check immutable evidence and individual scientific authorization."""
    try:
        if not RUN_RE.fullmatch(folder.name) or folder.is_symlink():
            return None

        vp = folder / "verification.json"
        verification = json.loads(vp.read_text())
        science_data = json.loads((folder / "science.json").read_text())
        manifest = json.loads((folder / "manifest.json").read_text())

        sidecar = (folder / "verification.sha256").read_text().strip()

        ledger = dict(
            line.split("  ", 1)[::-1]
            for line in (folder / "hashes.sha256").read_text().splitlines()
        )

        if (
            sidecar != digest(vp) + "  verification.json"
            or verification.get("status") not in (
                "PASS_SCOPED_CAMPAIGN_NO_LIFT",
                "PASS_INCOMPLETE_EVIDENCE_ONLY",
            )
            or verification.get("science_sha256")
                != digest(folder / "science.json")
            or not isinstance(verification.get("checks"), dict)
            or not verification["checks"]
            or not all(
                type(value) is bool and value
                for value in verification["checks"].values()
            )
            or ledger.get("science.json")
                != digest(folder / "science.json")
            or ledger.get("manifest.json")
                != digest(folder / "manifest.json")
            or manifest.get("run_id") != science_data.get("run_id")
            or science_data["run_id"] != folder.name
            or manifest.get("code_sha256") != core_hashes()
            or science_data.get("parent_locks") != parent_locks()
            or manifest.get("tasks_sha256")
                != science.signature(science_data["registered_tasks"])
        ):
            return None

        completed = science_data["state"] == "COMPLETED"
        verified_complete = (
            verification["status"] == "PASS_SCOPED_CAMPAIGN_NO_LIFT"
        )

        if completed != verified_complete:
            return None

        registered = {
            entry["id"]: entry
            for entry in science_data["registered_tasks"]
        }

        if registered.get(job["id"]) != job:
            return None

        entry = next(
            (
                item for item in science_data["jobs"]
                if item["id"] == job["id"]
                and item["fingerprint"] == fp
            ),
            None,
        )

        if (
            entry is None
            or entry.get("verification_status") != "VERIFIED"
        ):
            return None

        if entry.get('scientific_input_manifest') != inputs.manifest(ROOT, job):
            return None
        ref = entry["evidence"]

        if expected_ref is not None and expected_ref != ref:
            return None

        if not RUN_RE.fullmatch(ref.get("from_run", "")):
            return None

        evidence_file = ROOT / ref["path"]

        if (
            evidence_file.is_symlink()
            or not evidence_file.is_file()
            or not evidence_file.resolve().is_relative_to(BASE.resolve())
            or digest(evidence_file) != ref["sha256"]
        ):
            return None

        evidence = json.loads(evidence_file.read_text())
        checks = reviewed_checks(job, evidence)

        if (
            entry.get("scientific_verdict") != evidence["status"]
            or entry.get("review_checks") != checks
            or entry.get("cache_origin") not in ("FRESH", "REUSED")
        ):
            return None

        if entry["cache_origin"] == "FRESH":
            if entry["status"] != evidence["status"]:
                return None
        else:
            if entry["status"] != "REUSED_VERIFIED":
                return None

        return ref, evidence, checks

    except (
        OSError,
        KeyError,
        ValueError,
        TypeError,
        AssertionError,
        ImportError,
        AttributeError,
    ):
        return None


def verified_cache(job, fp):
    """Reuse only an individually reviewed and sealed v2 scientific gate."""
    if not BASE.is_dir():
        return None

    for folder in sorted(BASE.glob("g2camp4_*"), reverse=True):
        accepted = certified_entry(folder, job, fp)
        if accepted is not None:
            return accepted

    return None


def worker(input_file,output_file):
    source=Path(input_file); target=Path(output_file)
    if (target.name!='_worker.json' or not RUN_RE.fullmatch(target.parent.name)
            or target.parent.parent.resolve()!=BASE.resolve()
            or source.resolve()!=target.parent.joinpath('_input.json').resolve()):
        raise ValueError('worker destination not owned')
    job=json.loads(source.read_text())
    validate_job(job)
    # No shell, eval, arbitrary URLs or user-supplied executable commands.
    module=importlib.import_module('antigravity_research.gravity2.'+job['module'])
    before=inputs.manifest(ROOT,job)
    ev=module.run_gate(job,{'root':str(ROOT)})
    if before!=inputs.manifest(ROOT,job):
        raise ValueError('SCIENTIFIC_INPUT_DRIFT_DURING_WORKER')
    if not isinstance(ev,dict) or not ev.get('status'):
        raise ValueError('producer did not return a structured verdict')
    if ev['status'] not in ('BLOCKED_ACTION_INCOMPLETE','SCOPED_CONTROL_ONLY',
                            'UNDERDETERMINED','FAIL_SCOPED','PASS_SCOPED'):
        raise ValueError('unapproved physical promotion')
    if len(science.canonical(ev)) > 262_144:
        raise ValueError('worker evidence exceeds size cap')
    atomic_json(target,ev)


def _make_id():
    return datetime.now(timezone.utc).strftime('g2camp4_%Y%m%dT%H%M%SZ_')+secrets.token_hex(4)


def execute(args):
    if args.workers!=1 or args.level not in ('L0','L1'):
        raise ValueError('only bounded L0/L1 one-worker campaigns authorized')
    cap,ram,disk=PRESETS[args.preset]
    limit=60*args.minutes
    if not math.isfinite(limit) or not 0<limit<=cap:
        raise ValueError('invalid time budget')
    registered=jobs()
    selection=[j for j in registered if int(j['level'][1:])<=int(args.level[1:])]
    priorities=dispatch_order(selection)
    if args.dry_run:
        print(json.dumps({'program':'GRAVITY2_CAMPAIGN','selected_level':args.level,
           'seconds_ceiling':limit,'rss_soft_mib':ram,'disk_soft_mib':disk,'workers':1,
           'tasks':[{'id':j['id'],'gate':j['gate'],'candidate':j['candidate']} for j in priorities],
           'future_gates':'L2_L4_REQUIRE_NEW_INDEPENDENTLY_REVIEWED_PHYSICS',
           'writes':'NONE'},indent=2))
        return 0
    if not _rss_available():
        raise ValueError('psutil watchdog unavailable')
    if bytes_under(ROOT/'results/gravity2')>(GLOBAL_MIB-disk)*MIB:
        raise ValueError('global storage reserve exceeded')
    p=parent_locks(); code=core_hashes()
    if args.resume:
        old=locate(args.resume)
        former=json.loads((old/'science.json').read_text())
        oldman=json.loads((old/'manifest.json').read_text())
        previous_verification=json.loads((old/'verification.json').read_text())
        if (previous_verification.get('status')!='PASS_INCOMPLETE_EVIDENCE_ONLY' or
                previous_verification.get('science_sha256')!=digest(old/'science.json')):
            raise ValueError('cannot resume unverified incomplete run')
        if former['state']=='COMPLETED':
            raise ValueError('completed immutable run cannot resume')
        if (oldman['code_sha256']!=code or former['parent_locks']!=p
                or oldman['tasks_sha256']!=science.signature(priorities)):
            raise ValueError('resume provenance drift')
    rid=_make_id(); folder=locate(rid)
    folder.mkdir(parents=True,mode=0o700)
    manifest={'schema':'gravity2.campaign.v1','run_id':rid,
        'created_utc':datetime.now(timezone.utc).isoformat(),
        'level':args.level,'preset':args.preset,'wall_seconds':limit,
        'ram_soft_mib':ram,'disk_soft_mib':disk,'workers':1,
        'code_sha256':code,'tasks_sha256':science.signature(priorities),
        'resume_from':args.resume,'AGMINER':'NOT_EXECUTED','L2_L4':'LOCKED'}
    atomic_json(folder/'manifest.json',manifest)
    parent_ok=all(x['match'] for x in p.values())
    state='COMPLETED' if parent_ok else 'PARENT_HOLD'
    done=[]; skipped=[]; start=time.monotonic(); deadline=start+limit
    print('GRAVITY2_CAMPAIGN_RUN='+rid,flush=True)
    print('PARENTS='+('LOCKED' if parent_ok else 'HOLD'),flush=True)
    try:
        if parent_ok:
            for job in priorities:
                ident=job['id']
                if (folder/'stop.request').is_file():
                    state='USER_STOP';break
                if time.monotonic()>=deadline:
                    state='TIME_BUDGET_EXCEEDED';break
                if bytes_under(ROOT/'results/gravity2')>(GLOBAL_MIB-disk)*MIB:
                    state='STORAGE_LIMIT';break
                if not all(parent_ready(done, dep) for dep in job['requires']):
                    skipped.append({'id':ident,'reason':'PREREQUISITES_NOT_PROVED'})
                    continue
                before=inputs.manifest(ROOT,job)
                fp=fingerprint(job,p,code)
                cached=None if args.fresh else verified_cache(job,fp)
                if cached is not None:
                    ref,ev,checks=cached
                    label='REUSED_VERIFIED'
                    origin='REUSED'
                    peak=None
                else:
                    inp=folder/'_input.json';out=folder/'_worker.json'
                    atomic_json(inp,job)
                    env=dict(os.environ)
                    env.update({'PYTHONPATH':str(ROOT/'src'),'PYTHONDONTWRITEBYTECODE':'1',
                        'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1',
                        'MKL_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'})
                    proc=subprocess.Popen([sys.executable,'-m',
                        'antigravity_research.gravity2.campaign_v4','_worker',
                        '--input',str(inp),'--output',str(out)],cwd=ROOT,env=env,
                        stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,start_new_session=True)
                    outcome,rc,peak,stdout,trunc=supervise(proc,folder,deadline,ram,disk)
                    inp.unlink(missing_ok=True)
                    if outcome!='COMPLETED' or rc!=0 or not out.is_file():
                        state=outcome if outcome!='COMPLETED' else 'WORKER_ERROR'
                        atomic_text(folder/'worker_failure.log',str(stdout)[-2048:])
                        break
                    ev=json.loads(out.read_text())
                    out.unlink(missing_ok=True)
                    target=folder/(ident+'.json')
                    if len(science.canonical(ev)) > 262_144:
                        raise ValueError('worker evidence exceeds size cap')
                    atomic_json(target,ev)
                    try:
                        checks=reviewed_checks(job,ev)
                    except Exception as exc:
                        state='REVIEW_HOLD'
                        atomic_text(folder/'review_failure.log',repr(exc)[:2048]+'\n')
                        break
                    ref={'path':str(target.relative_to(ROOT)),
                         'sha256':digest(target),'from_run':rid}
                    label=ev['status']
                    origin='FRESH'
                if before!=inputs.manifest(ROOT,job):
                    state='INPUT_DRIFT_HOLD'
                    break
                done.append({'id':ident,'candidate':job['candidate'],'gate':job['gate'],
                             'status':label,'scientific_verdict':ev['status'],
                             'verification_status':'VERIFIED',
                             'cache_origin':origin,'review_checks':checks,
                             'scientific_input_manifest':before,
                             'fingerprint':fp,'evidence':ref,
                             'worker_peak_rss_mib':peak})
                print(ident+'='+label,flush=True)
    except KeyboardInterrupt:
        state='USER_INTERRUPT'
    finally:
        remaining=[j['id'] for j in priorities if j['id'] not in {e['id'] for e in done}]
        board={f'G{i:02d}':'NOT_DERIVED' for i in range(12)}
        board.update({'G00':'PASS_PARENT_SHA' if parent_ok else 'PARENT_HOLD',
            'G01':'INCOMPLETE_SUPPORT_EARTH_NEUTRAL_EINSTEIN',
            'G02':'SCOPED_SOURCE_ONLY','G03':'PARTIAL_WARD_ONLY',
            'G05':'PERIODIC_SINGLE_CHARGE_OBSTRUCTED_JPAIR_CONTROL_ONLY'})
        science_out={'program':'GRAVITY2_AUTONOMOUS_CAMPAIGN','run_id':rid,
           'state':state,'parent_locks':p,'registered_tasks':priorities,
           'jobs':done,'skipped':skipped,'remaining':remaining,
           'scientific_board':board,
           'next_missing_physics':[
             'complete off-shell source/X/Y/neutral/Earth/support/Einstein action',
             'physical metric Hodge and constrained mode derivation',
             'finite source with conserved charges and dynamic supports',
             'exterior/Earth/craft force, mode/UV and complete SI energy'],
           'candidate_count':len({j['candidate'] for j in priorities}),
           'qualified_physical_survivors':0,
           '006D_replaced':False,'whole_craft_lift':'NOT_DERIVED',
           'energy_J':'NOT_CERTIFIED','full_repository_regression':'NOT_RUN',
           'elapsed_s':round(time.monotonic()-start,4),
           'scope':'FINITE_REGISTERED_GATES_NO_SELF_INVENTED_ACTION'}
        atomic_json(folder/'science.json',science_out)
        atomic_text(folder/'hashes.sha256',''.join(digest(folder/n)+'  '+n+'\n'
                         for n in ('manifest.json','science.json')))
    print('EXECUTION='+state)
    print('PROCESSED='+str(len(done))+'/'+str(len(priorities)))
    print('PHYSICAL_SURVIVORS=0; GRAVITY=NOT_DERIVED')
    print('SCIENCE_SHA256='+digest(folder/'science.json'))
    from .campaign_check_v4 import verify
    verified=verify(folder)
    return 0 if state=='COMPLETED' and verified==0 else 3


def register(filepath):
    src=Path(filepath)
    if not src.is_file() or src.is_symlink() or src.stat().st_size>16_384:
        raise ValueError('invalid registration source')
    job=json.loads(src.read_text());validate_job(job)
    if job['id'] in {j['id'] for j in jobs()}:
        raise ValueError('candidate gate already registered')
    REGISTRY.mkdir(parents=True,exist_ok=True,mode=0o700)
    target=REGISTRY/(job['id']+'.json')
    # Pin the exact science and independent providers on registration.
    job['provider_sha256']=digest(provider_file(job['module']))
    job['independent_sha256']=digest(provider_file(job['independent']))
    atomic_json(target,job)
    print('REGISTERED='+job['id'])
    print('REGISTRATION_SHA256='+digest(target))
    return 0


def main(argv=None):
    p=argparse.ArgumentParser(prog='gravity2.campaign_v4')
    sub=p.add_subparsers(dest='cmd',required=True)
    for name in ('run','resume'):
        x=sub.add_parser(name)
        x.add_argument('--level',choices=['L0','L1','L2','L3','L4'],default='L1')
        x.add_argument('--preset',choices=tuple(PRESETS),default='quick')
        x.add_argument('--minutes',type=float,default=1.0)
        x.add_argument('--workers',type=int,default=1)
        x.add_argument('--dry-run',action='store_true')
        x.add_argument('--fresh',action='store_true')
        if name=='resume':x.add_argument('--run-id',required=True)
    for name in ('verify','report','stop'):
        sub.add_parser(name).add_argument('--run-id',required=True)
    sub.add_parser('candidates')
    sub.add_parser('status')
    sub.add_parser('needs')
    x=sub.add_parser('register');x.add_argument('--file',required=True)
    w=sub.add_parser('_worker');w.add_argument('--input',required=True);w.add_argument('--output',required=True)
    a=p.parse_args(argv)
    try:
        if a.cmd in ('run','resume'):
            a.resume=a.run_id if a.cmd=='resume' else None
            return execute(a)
        if a.cmd=='_worker':worker(a.input,a.output);return 0
        if a.cmd=='register':return register(a.file)
        if a.cmd=='candidates':
            for j in jobs():print(j['id'],'|',j['candidate'],'|',j['gate'],'|',j['level'])
            return 0
        if a.cmd=='needs':
            print('BLOCKED: physical source/support/Earth/Einstein action is not yet specified.')
            print('OPEN: new reviewed SHA-pinned gate providers can register without scheduler edits.')
            print('UNAUTHORIZED: L2-L4 and physical survivor promotion.')
            return 0
        if a.cmd=='status':
            if BASE.exists():
                for fold in sorted(BASE.glob('g2camp4_*'),reverse=True)[:12]:
                    if RUN_RE.fullmatch(fold.name) and (fold/'science.json').is_file():
                        s=json.loads((fold/'science.json').read_text())
                        print(fold.name,s['state'],len(s['jobs']))
            return 0
        fold=locate(a.run_id)
        if a.cmd=='verify':
            from .campaign_check_v4 import verify
            return verify(fold)
        if a.cmd=='stop':
            if not fold.is_dir() or (fold/'science.json').exists():
                raise ValueError('only active unsealed campaigns can be stopped')
            atomic_text(fold/'stop.request','STOP_REQUESTED\n')
            return 0
        if a.cmd=='report':
            s=json.loads((fold/'science.json').read_text())
            print(json.dumps({'run':s['run_id'],'state':s['state'],
                'jobs':s['jobs'],'next_missing_physics':s['next_missing_physics'],
                'whole_craft_lift':s['whole_craft_lift']},indent=2))
            return 0
    except (OSError,KeyError,ValueError,RuntimeError,AssertionError) as exc:
        print('GRAVITY2_CAMPAIGN_HOLD='+repr(exc),file=sys.stderr)
        return 2
    return 2


if __name__=='__main__':
    raise SystemExit(main())
