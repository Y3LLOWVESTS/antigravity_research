"""GRAVITY2 campaign gate library: explicitly scoped partial-source controls.

Science purpose: derive necessary source-charge screening for the archived
Jordan-frame R3B local template, NOT replace PH14 charged source solutions.
Periodic X/Y fields, Earth/support/Einstein variations remain incomplete.

An external research plugin may implement ``run_gate(task, context)`` with a
separate ``independent_check(task, evidence, context)`` in a distinct module.
Neither function is authorized to promote a real gravitational survivor.
"""
from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np
import sympy as sp

GATES = ('ACTION_COMPLETENESS', 'CHARGE_BALANCE_CONTROL')
FIELDS_PARENT = ('results/gravity2/bridge07_runs/'
                 'g207_20261121T065202Z_450b9280/fields.npz')


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)


def signature(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def default_tasks():
    action = {
        'source_frame':'JORDAN', 'source_fields':2,
        'charges':[0.4,-0.4], 'frequencies':[1.25,1.25],
        'potential':'POSITIVE_CONVEX_LOCAL_TEMPLATE',
        'exterior':'PERIODIC_2D_CONTROL',
        'dynamical_source_and_X':False,
        'source_support_action':None, 'Earth_action':None,
        'neutral_action':None, 'Einstein_Hilbert_boundary_action':None,
        'metric_Hodge_variation_complete':False,
        'physical_SI_normalization':False,
    }
    return [
        dict(schema='gravity2.campaign.task.v1', id='JPAIR_ACTION_INVENTORY',
             candidate='R3B_JORDAN_OPPOSITE_CHARGE_CONTROL',
             gate='ACTION_COMPLETENESS', level='L0', requires=[],
             priority=100, action=action, module='campaign_science',
             independent='campaign_check'),
        dict(schema='gravity2.campaign.task.v1', id='JPAIR_CHARGE_CONTROL',
             candidate='R3B_JORDAN_OPPOSITE_CHARGE_CONTROL',
             gate='CHARGE_BALANCE_CONTROL', level='L1', requires=[],
             priority=90, action=action, module='campaign_science',
             independent='campaign_check'),
    ]


def validate_task(task):
    if not isinstance(task, dict) or task.get('schema')!='gravity2.campaign.task.v1':
        raise ValueError('unsupported task schema')
    ident = task.get('id','')
    if not isinstance(ident,str) or not re.fullmatch(r'[A-Z0-9_]{4,56}',ident):
        raise ValueError('unsafe task id')
    for key in ('candidate','gate','level','module','independent','action'):
        if key not in task:
            raise ValueError('missing '+key)
    if not re.fullmatch(r'[A-Z0-9_]{4,64}',task['candidate']):
        raise ValueError('unsafe candidate id')
    if task['level'] not in ('L0','L1','L2','L3','L4'):
        raise ValueError('invalid fidelity level')
    if task['module'] != 'campaign_science' or task['independent'] != 'campaign_check':
        raise ValueError('unreviewed gate providers not installed: fail closed')
    if task['gate'] not in GATES:
        raise ValueError('unreviewed scientific gate')
    if task['level'] != ('L0' if task['gate']=='ACTION_COMPLETENESS' else 'L1'):
        raise ValueError('gate-level mismatch')
    if task.get('requires') not in ([],):
        raise ValueError('gate dependencies not yet independently qualified')
    if task.get('priority') not in (90,100):
        raise ValueError('unreviewed priority')
    if task['action'] != default_tasks()[0]['action']:
        raise ValueError('new action/operator requires reviewed provider registration')
    if len(canonical(task)) > 8192:
        raise ValueError('task manifest too large')
    return task


def completeness(action):
    missing=[]
    for name in ('source_support_action','Earth_action','neutral_action',
                 'Einstein_Hilbert_boundary_action'):
        if not action.get(name): missing.append(name)
    for key in ('dynamical_source_and_X','metric_Hodge_variation_complete',
                'physical_SI_normalization'):
        if action.get(key) is not True: missing.append(key)
    assert missing, 'a partial action must not become complete automatically'
    return {
        'status':'BLOCKED_ACTION_INCOMPLETE',
        'missing_action_terms':missing,
        'operator': 'TWO_OPPOSITE_CHARGED_SCALARS_JORDAN_PORTAL',
        'complete_covariant_action':'NOT_DERIVED',
        'gates':{'G01_ACTION':'INCOMPLETE','G02_VARIATION':'PARTIAL_ONLY',
                 'G04_HEALTH':'NOT_DERIVED','G05_SOURCE':'NOT_ESTABLISHED',
                 'G07_METRIC':'NOT_DERIVED','G10_REACTION':'NOT_DERIVED'},
    }


def symbolic_local_control():
    a,P,f1,f2,q,om,w,z = sp.symbols('a P f1 f2 q om w z',real=True)
    # Two charge signs and equal frequencies, canonical quadratic temporal sector.
    Omega_plus=om-q*a
    Omega_minus=om+q*a
    L_time=w*(Omega_plus**2*f1**2+Omega_minus**2*f2**2)/2
    density= -sp.diff(L_time,a)
    expected=w*q*(Omega_plus*f1**2-Omega_minus*f2**2)
    assert sp.expand(density-expected)==0
    assert sp.expand(density.subs(f2,f1)+2*w*q*q*a*f1*f1)==0
    shift=sp.symbols('shift',real=True)
    # Opposite charges imply opposite gauge shifts of the two frequencies.
    independent_omega_plus,independent_omega_minus=sp.symbols('omega_p omega_m',real=True)
    time_general=w*((independent_omega_plus-q*a)**2*f1**2+
                    (independent_omega_minus+q*a)**2*f2**2)/2
    assert sp.simplify(time_general.subs({a:a+shift,
            independent_omega_plus:independent_omega_plus+q*shift,
            independent_omega_minus:independent_omega_minus-q*shift},simultaneous=True)-time_general)==0
    return 'EXACT_OPPOSITE_CHARGE_VARIATION_AND_GAUGE_SHIFT'


def charge_screen(root: Path, action):
    assert symbolic_local_control()
    q=float(action['charges'][0]); om=float(action['frequencies'][0])
    if q <= 0 or action['charges'][1] != -q:
        raise ValueError('invalid compensating charge control')
    rows=[]
    with np.load(root/FIELDS_PARENT,allow_pickle=False) as archive:
        if set(archive.files) != {f'{name}_{n}' for n in (9,15,23,31) for name in 'afb'}:
            raise ValueError('parent archive keys drift')
        for n in (9,15,23,31):
            h=2*math.pi/n
            a=np.asarray(archive[f'a_{n}'],dtype=float)
            b=np.asarray(archive[f'b_{n}'],dtype=float)
            f=np.asarray(archive[f'f_{n}'],dtype=float)
            D=lambda v,axis:(np.roll(v,-1,axis=axis)-np.roll(v,1,axis=axis))/(2*h)
            p=D(a,0)*D(b,1)-D(a,1)*D(b,0)
            w=np.exp(2*(.08*p-.005*p*p))
            positive=q*w*(om-q*a)*f*f
            negative=-q*w*(om+q*a)*f*f
            pair=positive+negative
            charged=float(h*h*np.sum(positive))
            pair_charge=float(h*h*np.sum(pair))
            # Frequency correction is an UNSOURCED control, not an equilibrium.
            # Adjust the negative field frequency by delta to kill the zero mode.
            norm=float(h*h*np.sum(w*f*f))
            delta=pair_charge/(q*norm)
            corrected=pair-q*delta*w*f*f
            assert abs(h*h*np.sum(corrected)) < 1e-11
            assert charged>0
            rows.append({
                'grid':n, 'single_charge':charged,
                'equal_frequency_pair_charge':pair_charge,
                'required_negative_frequency_shift_control':delta,
                'zero_mode_adjusted_charge':float(h*h*np.sum(corrected)),
                'local_current_rms_after_adjustment':float(np.sqrt(np.mean(corrected**2))),
                'scalar_and_X_stationary':'NOT_TESTED',
            })
    return {'status':'SCOPED_CONTROL_ONLY',
            'symbolic':symbolic_local_control(),
            'rows':rows,
            'historical':'PH14 opposing charges already investigated; not new sourced physics',
            'zero_mode_tuning':'PRESCRIBED_FREQUENCY_CONTROL_NOT_AN_EOM_SOLUTION',
            'full_Einstein_support':'NOT_DERIVED'}


def run_gate(task, context):
    validate_task(task)
    action=task['action']
    if task['gate']=='ACTION_COMPLETENESS':
        return completeness(action)
    if task['gate']=='CHARGE_BALANCE_CONTROL':
        return charge_screen(Path(context['root']),action)
    raise ValueError('unregistered task')
