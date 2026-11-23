"""Independent GRAVITY2 campaign-science verifier.

Independently recalculates registered source action completeness and
charged-scalar Gauss controls, rather than trusting producer status labels.
Scientific PASS here never means Einstein gravity, real support, or lift.
"""
from __future__ import annotations

import importlib
import json
import math

import numpy as np
import sympy as sp

from .engine import ROOT, atomic_json, atomic_text, digest
from . import campaign_v2 as run


def independent_check(task,evidence,context):
    gate=task['gate']
    checks={}
    action=task['action']
    if gate=='ACTION_COMPLETENESS':
        missing=[k for k in ('source_support_action','Earth_action','neutral_action',
                'Einstein_Hilbert_boundary_action','dynamical_source_and_X',
                'metric_Hodge_variation_complete','physical_SI_normalization')
                if action.get(k) in (None,False,'')]
        checks['missing covariant action sectors']=bool(missing) and missing==evidence['missing_action_terms']
        checks['must block incomplete action']=evidence['status']=='BLOCKED_ACTION_INCOMPLETE'
        checks['not a physical completion']=evidence['complete_covariant_action']=='NOT_DERIVED'
    elif gate=='CHARGE_BALANCE_CONTROL':
        root=ROOT
        q=sp.Rational(2,5)
        A,OP,OM,F1,F2,W=sp.symbols('A OP OM F1 F2 W',real=True)
        # Derive density from varying two independent temporal charged fields.
        L=W*((OP-q*A)**2*F1**2+(OM+q*A)**2*F2**2)/2
        rho=-sp.diff(L,A)
        expected=W*q*((OP-q*A)*F1*F1-(OM+q*A)*F2*F2)
        checks['independent two-charge Euler']=sp.simplify(rho-expected)==0
        checks['equal-amplitude residual proportional to a']=sp.simplify(
            rho.subs({OP:OM,F2:F1})+2*W*q*q*A*F1*F1)==0
        c=sp.symbols('c',real=True)
        checks['opposing charge gauge shift']=sp.simplify(L.subs(
            {A:A+c,OP:OP+q*c,OM:OM-q*c},simultaneous=True)-L)==0
        rows=evidence['rows']
        checks['four parent grid controls']=[r['grid'] for r in rows]==[9,15,23,31]
        with np.load(root/'results/gravity2/bridge07_runs/'
                'g207_20261121T065202Z_450b9280/fields.npz',allow_pickle=False) as ar:
            for entry in rows:
                n=entry['grid']; h=2*math.pi/n
                A=np.array(ar[f'a_{n}'],dtype=float)
                B=np.array(ar[f'b_{n}'],dtype=float)
                F=np.array(ar[f'f_{n}'],dtype=float)
                Dx=lambda v,axis:(np.roll(v,-1,axis=axis)-np.roll(v,1,axis=axis))/(2*h)
                wedge=Dx(A,0)*Dx(B,1)-Dx(A,1)*Dx(B,0)
                W=np.exp(.16*wedge-.01*wedge*wedge)
                first=.4*W*(1.25-.4*A)*F*F
                second=-.4*W*(1.25+.4*A)*F*F
                pair=first+second
                required=float(h*h*np.sum(pair)) / (.4*float(h*h*np.sum(W*F*F)))
                balanced=pair-.4*required*W*F*F
                checks[f'charge integral n={n}']=abs(float(h*h*np.sum(first))-
                    entry['single_charge'])<1e-10 and first.min()>0
                checks[f'opposite current n={n}']=abs(float(h*h*np.sum(pair))-
                    entry['equal_frequency_pair_charge'])<1e-10
                checks[f'control frequency n={n}']=abs(required-
                    entry['required_negative_frequency_shift_control'])<1e-12
                checks[f'zero mode n={n}']=abs(float(h*h*np.sum(balanced)))<1e-11
                checks[f'local source still nontrivial n={n}']=abs(float(np.sqrt(np.mean(balanced**2)))-
                    entry['local_current_rms_after_adjustment'])<1e-12
        checks['tuning not a physical equilibrium']=evidence['status']=='SCOPED_CONTROL_ONLY' and (
            'NOT_AN_EOM' in evidence['zero_mode_tuning'])
    else:
        raise ValueError('unknown independent scientific gate')
    if not checks or not all(checks.values()):
        raise ValueError('scientific independent gate failed '+gate)
    return checks


def verify(folder):
    checks={}
    def gate(label,ok):
        checks[label]=bool(ok)
        if not ok:raise AssertionError(label)
    try:
        man=json.loads((folder/'manifest.json').read_text())
        sci=json.loads((folder/'science.json').read_text())
        ledger=dict(x.split('  ',1)[::-1] for x in (folder/'hashes.sha256').read_text().splitlines())
        for name in ('manifest.json','science.json'):
            gate('file SHA '+name,ledger[name]==digest(folder/name))
        gate('linkage',man['run_id']==sci['run_id']==folder.name)
        gate('source hash locks',man['code_sha256']==run.core_hashes())
        gate('live source parents',sci['parent_locks']==run.parent_locks())
        gate('parent Sha complete',all(x['match'] for x in sci['parent_locks'].values())
             if sci['state']=='COMPLETED' else True)
        gate('registered task collection pinned',
             man['tasks_sha256']==run.science.signature(sci['registered_tasks']))
        gate('known run state',sci['state'] in ('COMPLETED','PARENT_HOLD',
             'TIME_BUDGET_EXCEEDED','USER_STOP','USER_INTERRUPT',
             'STORAGE_LIMIT','WORKER_ERROR','MEMORY_LIMIT','WORKER_UNRESPONSIVE','REVIEW_HOLD'))
        gate('L0-L1 only',man['level'] in ('L0','L1') and man['workers']==1)
        gate('immutable source scope',man['AGMINER']=='NOT_EXECUTED' and man['L2_L4']=='LOCKED')
        gate('no gravity claim',sci['qualified_physical_survivors']==0
             and sci['whole_craft_lift']=='NOT_DERIVED' and sci['energy_J']=='NOT_CERTIFIED'
             and sci['006D_replaced'] is False)
        gate('no full regression claim',sci['full_repository_regression']=='NOT_RUN')
        gate('no invented action',sci['scope']=='FINITE_REGISTERED_GATES_NO_SELF_INVENTED_ACTION')
        selected={j['id']:j for j in sci['registered_tasks']}
        seen=set();checked={}
        for item in sci['jobs']:
            ident=item['id'];gate('unique job '+ident,ident not in seen and ident in selected)
            seen.add(ident)
            job=selected[ident]
            run.validate_job(job)
            gate('job fingerprint '+ident,item['fingerprint']==run.fingerprint(
                 job,sci['parent_locks'],man['code_sha256']))
            ref=item['evidence'];file=ROOT/ref['path']
            gate('evidence SHA '+ident,file.is_file() and digest(file)==ref['sha256'])
            ev=json.loads(file.read_text())
            verifier=importlib.import_module('antigravity_research.gravity2.'+job['independent'])
            independent=run.reviewed_checks(job,ev)
            gate('per-job verified science '+ident,
                 item.get('verification_status')=='VERIFIED'
                 and item.get('scientific_verdict')==ev['status']
                 and item.get('review_checks')==independent)
            for key,val in independent.items():
                gate(ident+' | '+key,val)
            gate('science prerequisites '+ident,all(
                 run.parent_ready(list(checked.values()), dep)
                 for dep in job['requires']))
            if item['status']=='REUSED_VERIFIED':
                parent=run.locate(ref['from_run'])
                if parent==folder:
                    gate('cached source different '+ident,False)
                else:
                    originating=[p for p in run.BASE.glob('g2camp2_*')
                        if p!=folder and run.certified_entry(
                            p,job,item['fingerprint'],ref)]
                    gate('cached evidence previously certified '+ident,bool(originating))
                gate('cached provenance '+ident,item.get('cache_origin')=='REUSED')
            else:
                gate('new evidence owned '+ident,ref['from_run']==folder.name
                     and item['status']==ev['status']
                     and item.get('cache_origin')=='FRESH')
            checked[ident]=item
        gate('processed+remaining complete',seen|set(sci['remaining'])==set(selected))
        gate('skipped separate',set(x['id'] for x in sci['skipped']).issubset(set(sci['remaining'])))
        if sci['state']=='COMPLETED':
            gate('completed jobs all processed or blocked',
                 len(sci['remaining'])==len(sci['skipped']))
            status='PASS_SCOPED_CAMPAIGN_NO_LIFT'
        else:
            status='PASS_INCOMPLETE_EVIDENCE_ONLY'
        result={'program':'GRAVITY2_CAMPAIGN_INDEPENDENT','run_id':folder.name,
                'status':status,'checks':checks,
                'science_sha256':digest(folder/'science.json'),
                'physical_success':False}
    except Exception as exc:
        result={'program':'GRAVITY2_CAMPAIGN_INDEPENDENT','run_id':folder.name,
                'status':'HOLD','checks':checks,'error':repr(exc),
                'physical_success':False}
    path=folder/'verification.json'
    if path.exists():
        if json.loads(path.read_text())!=result:
            print('GRAVITY2_CAMPAIGN_REVERIFY_DIFFERED_NO_OVERWRITE')
            return 3
    else:
        atomic_json(path,result)
        atomic_text(folder/'verification.sha256',digest(path)+'  verification.json\n')
    print('GRAVITY2_CAMPAIGN_VERIFY='+result['status'])
    print('CHECKS='+str(sum(checks.values()))+'/'+str(len(checks)))
    if 'error' in result:print('ERROR='+result['error'])
    print('VERIFICATION_SHA256='+digest(path))
    return 0 if result['status']=='PASS_SCOPED_CAMPAIGN_NO_LIFT' else 3
