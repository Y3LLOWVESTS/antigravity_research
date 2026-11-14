"""B17-M5V / ALPHA-1R17: terminal artificial same-action exterior audit.

Constructs ONE reduced stationary functional with the M5P boundary Hessian,
M5T cylindrical cell-averaged C2 material coefficients, and M5I/M5Q translated
compact net-neutral prescribed source. Earth, craft and common variations are
independently checked. This is NOT a source, hull or metric action.

No physically sourced antigravity, Noether Earth reaction, whole-craft lift,
complete conservative device energy or sub-10-MJ device is certified.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import subprocess
import sys
import traceback

import numpy as np
from scipy.sparse.linalg import spsolve

from . import hook17_r3b_m5o_fixed_box as m5o
from . import hook17_r3b_m5p_exterior_boundary as m5p
from . import hook17_r3b_m5q_translation_balance as m5q
from . import hook17_r3b_m5r_interaction_closure as m5r
from . import hook17_r3b_m5t_variational_cell_material as m5t
from .hook17_r3b_m5m_translation_consistency import (
    carrier_action_conversion_j_per_native,
)

BRANCH = '032H17A12D1R3X3B17-ALPHA1R17-M5V-UNIFIED'
EXPECTED_SHA256={
    'm5o':'e75e0b11b05b04a1561d4e1e628e6c6b62c2a7f2c36912b85041bec95b8969d3',
    'm5p':'e49f7eb2ac7f700d0f2608bd556e3729cf0941932704761f9b9118d9607c2243',
    'm5q':'93ed171e95cd4344efd3ca6f36661b977d18383a70c9a319e73c1d79ea12abf0',
    'm5r':'fb6604fbbf054843bce1354b61b8c29285092e766fb6fc2c553a62490af7a66a',
    'm5t':'7b613fc98d3d7247483ea1f0dcb89e492131e46d3f7f549097d73a98cc41ffa5',
}

PARENTS = {
    'm5o':'hook17_r3b_m5o_fixed_box',
    'm5p':'hook17_r3b_m5p_exterior_boundary',
    'm5q':'hook17_r3b_m5q_translation_balance',
    'm5r':'hook17_r3b_m5r_interaction_closure',
    'm5t':'hook17_r3b_m5t_variational_cell_material',
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def provenance():
    root=Path(__file__).resolve().parent
    return {key:sha(root/(name+'.py')) for key,name in PARENTS.items()}


def verify_provenance():
    actual=provenance()
    reference=m5r.provenance()
    if actual != EXPECTED_SHA256:
        raise RuntimeError('M5V pinned source provenance drift: '+json.dumps(actual))
    if reference != {k:actual[k] for k in reference}:
        raise RuntimeError('M5R provenance drift')
    m5t.validate_legacy_provenance()
    return actual


def verify_historical_evidence(folder):
    """Match historical M5U code snapshots to M5U-X1 erratum, fail closed."""
    ufiles=sorted(folder.glob('b17_m5u_decision_*_full_bundle.json'))
    efiles=sorted(folder.glob('b17_m5u_x1_erratum_*.json'))
    for upath in reversed(ufiles):
        try:
            original=json.loads(upath.read_text())
            if (original.get('branch') !=
                '032H17A12D1R3X3B17-ALPHA1R16-M5U-DECISION'
                or len(original.get('results',{}))!=40
                or len(original.get('manifest',[]))!=42
                or set(original.get('errors',{}))!={
                    'c2_original_h005_source_q8',
                    'c2_original_h005_source_q12'}):
                continue
            if original.get('regression',{}).get('exit_code')!=0:
                continue
            shots=original['source_snapshot']
            if any(shots[k]['sha256']!=EXPECTED_SHA256[k]
                   for k in EXPECTED_SHA256):
                continue
        except (OSError,KeyError,TypeError,ValueError):
            continue
        digest=sha(upath)
        for epath in reversed(efiles):
            try:
                erratum=json.loads(epath.read_text())
                if (erratum.get('parent_sha256')==digest
                    and erratum.get('research_screen_pass') is True
                    and erratum.get('original_run_certified_complete') is False
                    and erratum.get('valid_new_cases')==2):
                    return {
                        'parent_path':str(upath.resolve()),
                        'parent_sha256':digest,
                        'erratum_path':str(epath.resolve()),
                        'erratum_sha256':sha(epath),
                        'original_40_of_42_remains_incomplete':True,
                        'historic_regression_passed':True,
                        'historical_cases':{k:original['results'].get(k)
                          for k in ('c2_original_h004_center',
                                    'c2_extended_h004_center',
                                    'c2_original_h005_source_q4')},
                    }
            except (OSError,TypeError,ValueError):
                continue
    raise RuntimeError('Original M5U and matching X1 erratum not found; fail closed')


def manifest(mode):
    if mode not in ('preflight','full'):
        raise ValueError(mode)
    jobs=[]
    def add(name, **kw):
        if name in {x['name'] for x in jobs}:
            raise ValueError('Duplicate name '+name)
        settings=dict(domain='compact',h=.2,closure='dipole_trace',
                      profile='c2',width=.5,phase=0.,cell_q=8,source_q=6,
                      step=1.e-4,source_scale=1.,resolve=False)
        settings.update(kw)
        if any(settings==x['parameters'] for x in jobs):
            raise ValueError('Duplicate parameters '+name)
        jobs.append(dict(name=name,parameters=settings))
    add('preflight_compact_h020_resolved',resolve=True)
    add('preflight_compact_h020_dirichlet',closure='dirichlet')
    add('preflight_compact_h020_zero',source_scale=0.)
    if mode=='preflight':
        return jobs
    for domain in ('compact','original','extended'):
        for h in (.1,.0625,.05,.04):
            add(f'c2_{domain}_h{h:g}_trace',domain=domain,h=h,
                resolve=(h in (.1,.05) and domain!='compact'))
    for domain in ('original','extended'):
        for h in (.05,.04):
            for phase in (-.25,.25):
                add(f'phase_{domain}_{h:g}_{phase:+g}',
                    domain=domain,h=h,phase=phase)
    for domain in ('original','extended'):
        for closure in ('dipole_robin','dirichlet'):
            add(f'boundary_{domain}_{closure}',
                domain=domain,h=.05,closure=closure)
    for domain,h in (('compact',.1),('original',.05),('extended',.05)):
        for q in (4,12,16):
            add(f'cellq_{domain}_{h:g}_q{q}',
                domain=domain,h=h,cell_q=q)
    for domain in ('original','extended'):
        add('sourceq4_'+domain,domain=domain,h=.05,source_q=4)
    for domain in ('original','extended'):
        for step in (1.e-3,1.e-5):
            add(f'step_{domain}_{step:g}',domain=domain,h=.05,
                step=step,resolve=True)
    for width in (.25,.75):
        add(f'width_extended_{width:g}',domain='extended',h=.05,width=width)
    add('outer21_h010',domain='outer21',h=.1)
    add('outer21_h00625',domain='outer21',h=.0625)
    add('control_extended_h005_zero',domain='extended',h=.05,source_scale=0.)
    add('control_original_h005_half_amplitude',domain='original',h=.05,source_scale=.5)
    add('control_original_h005_current_reversal',domain='original',h=.05,
        reverse_current=True)
    add('control_C1_original_h01',domain='original',h=.1,
        profile='c1',width=.25)
    return jobs


def stationary(field,ops,source_shift,earth_coord,craft_coord,
               profile,width,cell_q,source_q,source_scale,
               earth_present,reverse_current=False,solve=True):
    """One discrete functional Q=conv*(u.H.u/2-u.W.j), with fixed box."""
    j,audit=m5o.source_rhs(field,ops,source_shift,
                           reversed_current=reverse_current,order=source_q)
    j=source_scale*j
    beta,de,dc=m5t.dual_cell_beta({'field':field},
         earth=earth_coord,craft=craft_coord,profile=profile,width=width,
         order=cell_q,earth_present=earth_present)
    A,H,W,asym=m5o.weighted(field,ops,beta)
    u=spsolve(A,j) if solve else None
    conv=carrier_action_conversion_j_per_native(field['h'])
    return dict(j=j,source_audit=audit,beta=beta,de=de,dc=dc,
                A=A,H=H,W=W,asym=asym,u=u,conv=conv)


def q_on_shell(state):
    u=state['u']
    return -.5*state['conv']*float(np.dot(u,state['W']*state['j']))


def q_off_shell(state,u):
    return state['conv']*(.5*float(u@(state['H']@u))
                          -float(u@(state['W']*state['j'])))


def run_case(domain='compact',h=.2,closure='dipole_trace',profile='c2',
             width=.5,phase=0.,cell_q=8,source_q=6,step=1.e-4,
             source_scale=1.,resolve=False,reverse_current=False):
    if (profile not in ('c1','c2') or closure not in
        ('dipole_trace','dipole_robin','dirichlet') or
        cell_q not in (4,8,12,16) or source_q not in (4,6) or
        not (0 < step<=.002) or not (-.5<=phase<=.5) or
        not (0<=source_scale<=1) or width<=0 or
        domain not in m5p.BOUNDS):
        raise ValueError('Invalid M5V configuration')
    field=m5o.mesh(h,m5p.BOUNDS[domain])
    ops,boundary=m5p.robin_operators(field,closure)
    shift=h*phase
    def make(earth,craft,present,do_solve=True):
        return stationary(field,ops,craft,earth,craft,profile,width,cell_q,
                          source_q,source_scale,present,reverse_current,do_solve)
    on=make(shift,shift,True)
    off=make(shift,shift,False)
    conv=on['conv']
    for item in (on,off):
        if not np.array_equal(on['W'],item['W']):
            raise ArithmeticError('Material-dependent source weights')
    W=on['W']
    Hzero=m5o.weighted(field,ops,np.zeros_like(on['beta']))[1]
    def h_dq(state,betaderiv):
        if not np.any(betaderiv):
            return 0.0
        delta=m5o.weighted(field,ops,betaderiv)[1]-Hzero
        return .5*conv*float(state['u']@(delta@state['u']))
    da_on=h_dq(on,on['de'])
    da_off=h_dq(off,off['de'])
    dc_on=h_dq(on,on['dc'])
    dc_off=h_dq(off,off['dc'])
    dsource,daudit=m5q.analytic_source_translation(field,shift,source_q)
    if reverse_current:
        nphi=ops['k_phi'].shape[0]
        dsource[nphi:]*=-1
    dsource*=source_scale
    def source_work(state):
        return -conv*float(state['u']@(W*dsource))
    j_on=source_work(on)
    j_off=source_work(off)
    analytic={
      'earth':da_on-da_off,
      'craft_operator':dc_on-dc_off,
      'craft_source':j_on-j_off,
    }
    analytic['craft']=analytic['craft_operator']+analytic['craft_source']
    analytic['common']=analytic['earth']+analytic['craft']
    numerical={}
    source_fd=[]
    for sign in (1.,-1.):
        jj,_=m5o.source_rhs(field,ops,shift+sign*step,
                           reversed_current=reverse_current,order=source_q)
        source_fd.append(jj*source_scale)
    srcfd=(source_fd[0]-source_fd[1])/(2*step)
    src_fd_work=-conv*float((on['u']-off['u'])@(W*srcfd))
    src_defect=float(np.linalg.norm(srcfd-dsource)
        /max(np.linalg.norm(dsource),1.))
    for leg in ('earth','craft','common'):
        operator_contribution=0.0
        for present,baseline,sign in ((True,on,1.),(False,off,-1.)):
            if not present and leg=='earth':
                continue
            beta=[]
            for direction in (1.,-1.):
                e=shift+(direction*step if leg in ('earth','common') else 0.)
                c=shift+direction*step if leg in ('craft','common') else shift
                coeff=m5t.dual_cell_beta({'field':field},earth=e,
                    craft=c,profile=profile,width=width,order=cell_q,
                    earth_present=present)[0]
                beta.append(coeff)
            db=(beta[0]-beta[1])/(2*step)
            if np.any(db):
                Hvariation=m5o.weighted(field,ops,db)[1]-Hzero
                operator_contribution+=sign*.5*conv*float(
                    baseline['u']@(Hvariation@baseline['u']))
        source_contribution=src_fd_work if leg in ('craft','common') else 0.
        numerical[leg]=operator_contribution+source_contribution
    defects={leg:numerical[leg]-analytic[leg]
             for leg in ('earth','craft','common')}
    resolved_q=None
    if resolve:
        resolved_q={}
        for leg in ('earth','craft','common'):
            qs=[]
            for sign in (1.,-1.):
                e=shift+(sign*step if leg in ('earth','common') else 0.)
                c=shift+sign*step if leg in ('craft','common') else shift
                qs.append(q_on_shell(make(e,c,True))-
                          q_on_shell(make(e,c,False)))
            resolved_q[leg]=(qs[0]-qs[1])/(2*step)
    resolved_defects=(None if resolved_q is None else
        {leg:resolved_q[leg]-analytic[leg]
         for leg in ('earth','craft','common')})
    residual={key:max(float(np.linalg.norm(s['A']@s['u']-s['j'])/
             max(np.linalg.norm(s['j']),1.)) for s in (on,off))
             for key in ('linear',)}
    residual['weighted_stationarity']=max(float(np.linalg.norm(
         s['H']@s['u']-W*s['j'])/max(np.linalg.norm(W*s['j']),1.))
         for s in (on,off))
    residual['weighted_asymmetry']=max(float(s['asym']) for s in (on,off))
    residual['source_neutrality_max_relative']=max(abs(float(s['source_audit']['net_charge_after_projection_rel'])) for s in (on,off))
    action_on=q_on_shell(on); action_off=q_on_shell(off)
    identity_error=max(abs(q_off_shell(s,s['u'])-q_on_shell(s))
                      for s in (on,off))
    result={
       'parameters':dict(domain=domain,h=h,closure=closure,profile=profile,
                         width=width,phase=phase,cell_q=cell_q,
                         source_q=source_q,step=step,source_scale=source_scale,
                         resolve=resolve,reverse_current=reverse_current),
       'scope':'PRESCRIBED_REDUCED_CARRIER_ACTION_M5P_BOUNDARY_M5T_CELL',
       'Q_earth_on_j':action_on,'Q_earth_off_j':action_off,
       'Q_interaction_j':action_on-action_off,
       'analytic_j_m':analytic,
       'independent_fixed_u_j_m':numerical,
       'fixed_u_minus_analytic_j_m':defects,
       'resolved_onshell_j_m':resolved_q,
       'resolved_minus_analytic_j_m':resolved_defects,
       'source_derivative_relative_defect':src_defect,
       'stationarity':residual,
       'on_shell_identity_abs_j':identity_error,
       'boundary_audit':boundary,
       'earth_on_source_audit':{k:v for k,v in on['source_audit'].items()
                      if k not in ('reference_moments',)},
       'source_amplitude_artificial':m5o.AMPLITUDE,
       'common_translation_residual_j_m':analytic['common'],
       'boundary_reaction_not_derived':True,
       'physical_noether_reciprocity_certified':False,
       'whole_spacecraft_lift_certified':False,
       'complete_operating_energy_j':None,
       '006d_replaced':False,
    }
    return result


def summary(jobs,results,errors):
    cases={k:results[k] for k in results}
    def pick(name):
        return cases.get(name)
    centers={}
    for domain in ('compact','original','extended'):
        centers[domain]={}
        for h in (.1,.0625,.05,.04):
            r=pick(f'c2_{domain}_h{h:g}_trace')
            if r:
                centers[domain][str(h)]={
                   'earth_j_m':r['analytic_j_m']['earth'],
                   'craft_j_m':r['analytic_j_m']['craft'],
                   'common_j_m':r['analytic_j_m']['common'],
                   'interaction_j':r['Q_interaction_j']}
    extrapolations={}
    for domain in ('compact','original','extended'):
        def zero_h2(ha,hb):
            aa=pick(f'c2_{domain}_h{ha:g}_trace')
            bb=pick(f'c2_{domain}_h{hb:g}_trace')
            if aa is None or bb is None:
                return None
            ya=aa['analytic_j_m']['earth']
            yb=bb['analytic_j_m']['earth']
            return (ha**2*yb-hb**2*ya)/(ha**2-hb**2)
        v1=zero_h2(.0625,.05)
        v2=zero_h2(.05,.04)
        extrapolations[domain]={
            'h2_00625_005_intercept_j_m':v1,
            'h2_005_004_intercept_j_m':v2,
            'intercept_disagreement_j_m':(None if v1 is None or v2 is None
                                            else v2-v1),
            'extrapolation_is_not_proof':True}
    phase_screens={}
    for domain in ('original','extended'):
        for h in (.05,.04):
            base=pick(f'c2_{domain}_h{h:g}_trace')
            variations=[pick(f'phase_{domain}_{h:g}_{v:+g}')
                        for v in (-.25,.25)]
            if base and all(variations):
                z=[x['analytic_j_m'] for x in [base]+variations]
                phase_screens[f'{domain}:{h:g}']={
                    'earth_spread_j_m':max(x['earth'] for x in z)-min(x['earth'] for x in z),
                    'common_spread_j_m':max(x['common'] for x in z)-min(x['common'] for x in z),
                    'max_abs_common_j_m':max(abs(x['common']) for x in z)}
    quadrature={}
    for domain,h in (('compact',.1),('original',.05),('extended',.05)):
        reference=pick(f'c2_{domain}_h{h:g}_trace')
        others=[pick(f'cellq_{domain}_{h:g}_q{q}') for q in (4,12,16)]
        if reference and all(others):
            sequence=[reference]+others
            z=[x['analytic_j_m']['earth'] for x in sequence]
            quadrature[f'{domain}:{h:g}']={
                'earth_spread_q4_q8_q12_q16_j_m':max(z)-min(z),
                'earth_q12_q16_j_m':others[1]['analytic_j_m']['earth']-
                                     others[2]['analytic_j_m']['earth']}
    resolved=[]
    offshell=[]
    for name,row in cases.items():
        if row['resolved_minus_analytic_j_m'] is not None:
            resolved.append({'name':name,'max_abs_j_m':max(
                 abs(x) for x in row['resolved_minus_analytic_j_m'].values())})
        offshell.append({'name':name,'max_abs_j_m':max(
            abs(x) for x in row['fixed_u_minus_analytic_j_m'].values())})
    negative=[r for r in cases.values() if r['parameters']['source_scale']==0.]
    negative_pass=bool(negative) and all(
        abs(r['Q_interaction_j'])<1.e-10 and
        max(abs(x) for x in r['analytic_j_m'].values())<1.e-10 for r in negative)
    cell_pass=bool(quadrature) and all(
        abs(x['earth_q12_q16_j_m'])<.005 for x in quadrature.values())
    independent_pass=bool(resolved) and all(x['max_abs_j_m']<.005 for x in resolved)
    fixed_pass=bool(offshell) and all(x['max_abs_j_m']<.005 for x in offshell)
    complete=len(results)==len(jobs) and not errors
    fine=[]
    for domain in ('original','extended'):
        for h in (.05,.04):
            r=pick(f'c2_{domain}_h{h:g}_trace')
            if r: fine.append(r)
    def er(domain,h):
        x=pick(f'c2_{domain}_h{h:g}_trace')
        return None if x is None else x['analytic_j_m']['earth']
    def cr(domain,h):
        x=pick(f'c2_{domain}_h{h:g}_trace')
        return None if x is None else x['analytic_j_m']['common']
    f1=er('extended',.04);f2=er('original',.04);f3=er('extended',.05)
    f4=cr('extended',.04)
    boundary_sensitivity={}
    for domain in ('original','extended'):
        base=pick(f'c2_{domain}_h0.05_trace')
        if base:
            boundary_sensitivity[domain]={}
            for closure in ('dipole_robin','dirichlet'):
                row=pick(f'boundary_{domain}_{closure}')
                if row:
                    boundary_sensitivity[domain][closure]={
                        leg:row['analytic_j_m'][leg]-base['analytic_j_m'][leg]
                        for leg in ('earth','craft','common')}
    source_quad={}
    for domain in ('original','extended'):
        base=pick(f'c2_{domain}_h0.05_trace')
        other=pick('sourceq4_'+domain)
        if base and other:
            source_quad[domain]={leg:other['analytic_j_m'][leg]-
                base['analytic_j_m'][leg] for leg in ('earth','craft','common')}
    half=pick('control_original_h005_half_amplitude')
    basehalf=pick('c2_original_h0.05_trace')
    scaling=(half is not None and basehalf is not None and
        abs(half['Q_interaction_j']-.25*basehalf['Q_interaction_j'])<1.e-7
        and all(abs(half['analytic_j_m'][key]-.25*basehalf['analytic_j_m'][key])<1.e-6
                for key in ('earth','craft','common')))
    fine_metrics=dict(
        domain_earth_difference_j_m=None if f1 is None or f2 is None else abs(f1-f2),
        mesh_earth_change_004_005_j_m=None if f1 is None or f3 is None else abs(f1-f3),
        extended_abs_common_004_j_m=None if f4 is None else abs(f4),
        phase_extended_004=phase_screens.get('extended:0.04'))
    screen=complete and all(x is not None for x in (f1,f2,f3,f4)) and (
        abs(f1-f2)<.005 and abs(f1-f3)<.08 and abs(f4)<.01 and
        phase_screens.get('extended:0.04',{}).get('earth_spread_j_m',1) < .01
        and all(extrapolations[k]['intercept_disagreement_j_m'] is not None
                and abs(extrapolations[k]['intercept_disagreement_j_m'])<.005
                for k in ('original','extended'))
        and abs(extrapolations['original']['h2_005_004_intercept_j_m']-
                extrapolations['extended']['h2_005_004_intercept_j_m'])<.005)
    gates={
       'V0_registered_complete':'PASS' if complete else 'INCOMPLETE',
       'V1_provenance_and_stationary_action':'PASS' if complete and all(
           x['stationarity']['weighted_stationarity']<1.e-8 and
           x['on_shell_identity_abs_j']<1.e-7 and
           x['stationarity']['source_neutrality_max_relative']<1.e-10 for x in cases.values()) else 'FAIL_OR_INCOMPLETE',
       'V2_independent_fixed_field_derivatives':'PASS' if complete and fixed_pass else 'FAIL_OR_INCOMPLETE',
       'V3_independent_resolved_Earth_craft_common':'PASS_SCREEN_ONLY' if complete and independent_pass else 'FAIL_OR_INCOMPLETE',
       'V4_source_free_negative_controls':'PASS' if complete and negative_pass else 'FAIL_OR_INCOMPLETE',
       'V4B_prescribed_source_quadratic_scaling':'PASS' if complete and scaling else 'FAIL_OR_INCOMPLETE',
       'V4C_source_quadrature_4_vs_6':'PASS_SCREEN_ONLY' if complete and
           len(source_quad)==2 and all(abs(v)<.001 for row in source_quad.values()
               for v in row.values()) else 'FAIL_OR_INCOMPLETE',
       'V5_C2_material_quadrature':'PASS_SCREEN_ONLY' if complete and cell_pass else 'FAIL_OR_INCOMPLETE',
       'V6_C2_mesh_domain_phase':'PASS_SCREEN_ONLY' if screen else 'NOT_CERTIFIED',
       'V7_continuum_limit_and_real_exterior_DtN':'NOT_CERTIFIED',
       'V8_independent_source_enclosure_hull_support_action':'NOT_DERIVED',
       'V9_whole_spacecraft_external_force':'NOT_DERIVED',
       'V10_physical_Noether_metric_impulse_complete_energy':'NOT_ESTABLISHED',
    }
    verdict=('INCOMPLETE_NO_DECISION' if not complete else
             'UNIFIED_REDUCED_ACTION_NUMERIC_SCREEN_PASSED_NOT_A_CRAFT'
             if all(gates[key].startswith('PASS') for key in
                 ('V1_provenance_and_stationary_action','V2_independent_fixed_field_derivatives',
                  'V3_independent_resolved_Earth_craft_common',
                  'V4_source_free_negative_controls','V4B_prescribed_source_quadratic_scaling',
                  'V4C_source_quadrature_4_vs_6',
                  'V5_C2_material_quadrature','V6_C2_mesh_domain_phase'))
             else 'UNIFIED_REDUCED_ACTION_NOT_CERTIFIED')
    return dict(cases=len(cases),errors=len(errors),grid_centers=centers,
                phase=phase_screens,quadrature=quadrature,
                h2_extrapolations=extrapolations,
                boundary_sensitivity=boundary_sensitivity,
                source_quadrature=source_quad,
                resolved_checks=resolved,off_shell_checks=offshell,
                negative_controls=len(negative),fine_metrics=fine_metrics,
                gates=gates,decision=verdict,
                artificial_model_complete=False,
                physical_antigravity=False,
                whole_spacecraft_lift=False,
                physically_sourced_action=False,
                complete_energy_under_10MJ=False,
                conservation_certified=False,
                **{"006d_replaced":False})


def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode',choices=('preflight','full'),default='preflight')
    ap.add_argument('--results-dir',default='results/data')
    ap.add_argument('--resume')
    ap.add_argument('--max-new-cases',type=int)
    ap.add_argument('--regression',action='store_true')
    args=ap.parse_args(argv)
    if args.max_new_cases is not None and args.max_new_cases <1:
        ap.error('max-new-cases must be positive')
    fingerprints=verify_provenance()
    folder=Path(args.results_dir).resolve();folder.mkdir(parents=True,exist_ok=True)
    evidence=verify_historical_evidence(folder)
    jobs=manifest(args.mode)
    identity={'source_sha256':{**fingerprints,'m5v':sha(__file__)},
              'manifest':jobs,'mode':args.mode,
              'historical_evidence':evidence}
    if args.resume:
        path=Path(args.resume).resolve();record=json.loads(path.read_text())
        if any(record.get(k)!=v for k,v in identity.items()):
            ap.error('Resume refused: source or manifest changed')
    else:
        timestamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        path=folder/f'b17_m5v_unified_{timestamp}_{args.mode}_bundle.json'
        record={'branch':BRANCH,'status':'RUNNING',**identity,
                'source_snapshot':{key:{'sha256':fingerprints[key],
                    'code':(Path(__file__).resolve().parent/(name+'.py')).read_text()}
                    for key,name in PARENTS.items()},
                'results':{},'errors':{},'summary':None,'regression':None,
                'environment':{'python':sys.version.split()[0],
                               'os':platform.platform()},
                'claims':{'complete_artificial_model':False,'whole_craft_lift':False}}
    def save():
        tmp=path.with_name(path.name+'.tmp')
        with tmp.open('w') as stream:
            json.dump(record,stream,indent=2,sort_keys=True,allow_nan=False)
            stream.write('\n');stream.flush();os.fsync(stream.fileno())
        os.replace(tmp,path)
    if not args.resume:save()
    fresh=0
    try:
        for i,job in enumerate(jobs,1):
            name=job['name']
            if name in record['results']:
                print(f'[{i}/{len(jobs)}] REUSED {name}',flush=True);continue
            if args.max_new_cases is not None and fresh>=args.max_new_cases:
                record['status']='PARTIAL_NOT_CERTIFIED';save()
                print('RESUME_BUNDLE:',path,flush=True);return 2
            print(f'[{i}/{len(jobs)}] {name}',flush=True)
            try:
                row=run_case(**job['parameters'])
                record['results'][name]=row
                record['errors'].pop(name,None)
                print('  Earth/craft/common [J/m]',*[f'{row["analytic_j_m"][k]:.9g}'
                      for k in ('earth','craft','common')],flush=True)
                print('  Max fixed-u error [J/m]',max(map(abs,row['fixed_u_minus_analytic_j_m'].values())),flush=True)
            except Exception:
                record['errors'][name]=traceback.format_exc()
                print('  ERROR',record['errors'][name],flush=True)
            fresh+=1;save()
        record['summary']=summary(jobs,record['results'],record['errors'])
        if args.regression and record['regression'] is None:
            process=subprocess.run([sys.executable,'-m','pytest','-q'],
                stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,
                env={**os.environ,'PYTHONPATH':str(Path.cwd()/'src')},check=False)
            record['regression']={'exit_code':process.returncode,
                                  'log_tail':process.stdout[-8000:]}
            print(process.stdout[-2000:],flush=True)
        good=(record['summary']['gates']['V0_registered_complete']=='PASS'
              and (record['regression'] is None or record['regression']['exit_code']==0))
        record['status']='COMPLETE_NUMERICAL_DECISION_ONLY' if good else 'FAILED_OR_INCOMPLETE'
        save()
        print('UPLOAD_ONLY:',path,flush=True)
        print('VERDICT:',record['summary']['decision'],flush=True)
        print('GATES:',json.dumps(record['summary']['gates'],indent=2),flush=True)
        return 0 if good else 1
    except KeyboardInterrupt:
        record['status']='INTERRUPTED';save()
        print('RESUME_BUNDLE:',path,flush=True)
        return 130


if __name__=='__main__':
    raise SystemExit(main())
