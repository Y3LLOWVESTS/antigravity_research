"""Independent GRAVITY2-06 restricted-action and evidence verifier.

Computes portal contribution to Gauss independently using derivative through
an auxiliary P variable; checks phase gauge invariance and negative controls.
"""
from __future__ import annotations

import json
import sympy as sp

from .engine import ROOT, atomic_json, atomic_text, digest
from . import bridge06 as run


def independent_algebra():
    a, da, f, df, B, om, q, alpha, beta, mu, lam=sp.symbols(
        'a da f df B om q alpha beta mu lam',real=True)
    P=sp.symbols('P',real=True)
    sig=alpha*P-beta*P*P
    omega=om-q*a
    kinetic=omega*omega*f*f-df*df
    V=mu*f*f/2+lam*f**4/4
    local=sp.exp(2*sig)*kinetic/2-sp.exp(4*sig)*V
    p_part=sp.diff(local,P)
    trace=sp.exp(-2*sig)*kinetic-4*V
    assert sp.simplify(p_part-sp.exp(4*sig)*trace*sp.diff(sig,P))==0
    # Independent chain rule in one-component geometric reduction P=B dA0.
    full=da**2/2+local.subs(P,B*da)
    displacement=da+B*p_part.subs(P,B*da)
    assert sp.simplify(sp.diff(full,da)-displacement)==0
    assert sp.simplify(sp.diff(full,a)+q*sp.exp(2*sig.subs(P,B*da))*omega*f*f)==0
    assert sp.simplify(sp.diff(full,da,f)-sp.diff(full,f,da))==0
    c=sp.symbols('c',real=True)
    assert sp.simplify(full.subs({om:om+q*c,a:a+c},simultaneous=True)-full)==0
    point={da:sp.Rational(1,2),B:2,a:sp.Rational(1,5),
           f:1,df:sp.Rational(1,3),om:sp.Rational(4,3),
           q:1,alpha:sp.Rational(1,13),beta:sp.Rational(1,97),
           mu:2,lam:sp.Rational(1,2)}
    assert sp.simplify((B*p_part.subs(P,B*da)).subs(point))!=0
    assert sp.simplify(sp.diff(full,da,f).subs(point))!=0
    assert sp.simplify(displacement.subs(B,0)-da)==0
    assert sp.simplify(displacement.subs({alpha:0,beta:0})-da)==0
    # Robin wall variation: -w (normal grad f)*delta f - kappa f*delta f.
    n,wall_k,w=sp.symbols('n wall_k w',real=True)
    assert sp.diff(-w*n*f-wall_k*f*f/2,f)==-w*n-wall_k*f
    return 'PASS_INDEPENDENT_REDUCED_EULER_PORTAL_GAUGE_AND_WALL'


def verify(folder):
    checks={}
    def gate(name,ok):
        checks[name]=bool(ok)
        if not ok:
            raise AssertionError(name)
    try:
        man=json.loads((folder/'manifest.json').read_text())
        sci=json.loads((folder/'science.json').read_text())
        hashes=dict(row.split('  ',1)[::-1] for row in (folder/'hashes.sha256').read_text().splitlines())
        gate('manifest SHA',hashes['manifest.json']==digest(folder/'manifest.json'))
        gate('science SHA',hashes['science.json']==digest(folder/'science.json'))
        gate('run ID',man['run_id']==sci['run_id']==folder.name)
        gate('source files SHA',man['producer_sha256']==run.producer_hashes())
        gate('L0 and one worker',man['level']=='L0' and man['workers']==1)
        gate('budget and watchdog',man['seconds']>0 and sci['resource']['watchdog']=='SOFT_PSUTIL_PROCESS')
        gate('no historical write declaration',man['prior_GRAVITY2_modifications']=='NONE')
        gate('no AGMINER execution declaration',man['legacy_AGMINER']=='READ_ONLY_HASH_NO_EXECUTION')
        gate('parent report live',sci['parent_locks']==run.locks())
        gate('no complete action',sci['full_action']=='NOT_DERIVED' and sci['real_source']=='NOT_ESTABLISHED')
        gate('no lift or energy promotion',sci['whole_craft_lift']=='NOT_DERIVED' and sci['complete_energy_SI']=='NOT_CERTIFIED' and not sci['006D_replaced'])
        gate('no loaded solver',sci['loaded_PDE']=='NOT_AUTHORIZED' and sci['qualified_survivors']==0)
        gate('no full regression',sci['full_regression']=='NOT_RUN')
        gate('bounded outcome label',sci['execution_status'] in {
            'COMPLETED','PARENT_HOLD','TIME_BUDGET_EXCEEDED','MEMORY_LIMIT',
            'STORAGE_LIMIT','WORKER_ERROR','WORKER_BAD_JSON','USER_STOP',
            'USER_INTERRUPT','WORKER_UNRESPONSIVE',
        })
        if sci['execution_status']=='COMPLETED':
            e=sci['evidence']; v=e['local_variations']; wall=e['conditional_obstructions']
            gate('real parent locks',sci['parent_locks']['all_match'] is True)
            gate('sourceaction decision',e['decision']=='FULL_PORTAL_GAUSS_CHANGES_STATIONARY_BOUND; SOURCE_UNDERDETERMINED')
            gate('Gauss polarization',v['Gauss_Euler']=='div(grad A0 + B*Pi)=-q*w*Omega*f^2')
            gate('exact local Euler',v['exact_Euler_derivatives']=='PASS')
            gate('reciprocity scoped',v['mixed_source_A0prime_reciprocity_residual']=='0')
            gate('phase gauge control',v['gauge_stationary_phase_shift_residual']=='0')
            gate('polarization missing negative control',v['omit_portal_polarization_negative_control']=='FAIL_AS_REQUIRED')
            gate('fixed wall boundary condition',wall['natural_Robin']=='w*n.grad(f)+kappa*f=0')
            gate('fixed-wall only, not material',wall['material_wall_dynamical_traction']=='NOT_DERIVED')
            gate('frozen-Gauss hypothesis explicit',wall['ordinary_Gauss_frozen_w_only'].startswith('-Delta A0+q^2'))
            gate('full-portal no maximum-principle inference','invalidates' in wall['full_portal_Gauss_difference'])
            gate('no unsupported static-to-stationary no-go','FULL_PORTAL_OPEN' in e['gates']['G05_SOURCE'])
            gate('historical loaded failure preserved',e['history']['r3b_loaded_min_m_s2']==-129.67185782242464)
            gate('field capacity only',e['history']['r3b_prescribed_field_capacity_J']==1.5429162116460216)
            gate('independent reduced variation and negative controls',independent_algebra().startswith('PASS_'))
            status='PASS_SCOPED_STATIONARY_GAUSS_PREFLIGHT_NO_SOURCE'
        else:
            gate('incomplete not promoted',sci['qualified_survivors']==0)
            status='PASS_INCOMPLETE_EVIDENCE_ONLY'
        report={'program':'GRAVITY2-06-INDEPENDENT','run_id':folder.name,
                'status':status,'checks':checks,'science_sha256':digest(folder/'science.json'),
                'physical_lift':'NOT_DERIVED'}
    except Exception as exc:
        report={'program':'GRAVITY2-06-INDEPENDENT','run_id':folder.name,
                'status':'HOLD','checks':checks,'error':repr(exc),'physical_lift':'NOT_DERIVED'}
    path=folder/'verification.json'
    if path.is_file():
        if json.loads(path.read_text())!=report:
            print('VERIFICATION_RECHECK_DIFFERS_NO_OVERWRITE')
            return 3
    else:
        atomic_json(path,report)
        atomic_text(folder/'verification.sha256',digest(path)+'  verification.json\n')
    print('GRAVITY2_06_VERIFY='+report['status'])
    print('CHECKS='+str(sum(checks.values()))+'/'+str(len(checks)))
    if 'error' in report:
        print('ERROR='+report['error'])
    print('VERIFICATION_SHA256='+digest(path))
    return 0 if report['status']=='PASS_SCOPED_STATIONARY_GAUSS_PREFLIGHT_NO_SOURCE' else 3
