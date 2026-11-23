"""Closed-failure memory; deterministic prioritization, no auto-physics promotion."""
from .response_v7 import VERDICT

CLOSED = {
    '006D':'POSITIVE_ENERGY_GR_NEAR_FIELD_BUT_1_OVER_G_ENERGY',
    'R3A':'ORDINARY_MATTER_SUPPRESSION_1P84E15',
    'R3B':'PRESCRIBED_JOULE_CAPACITY_UNSOURCED',
    'R3X1':'LORENTZIAN_SIGN_ERRATUM',
    'B15':'ANGLE_ONLY_FAILED', 'B16':'WEAK_LOADING_FAILED',
    'PH16_04R2':'FINITE_LATTICE_STATIONARITY_ONLY',
    'ACT0':'SCOPED_ACTION_OBSTRUCTION',
}


def select(response, checks, candidates=None):
    if response.get('status') != VERDICT or not checks or not all(type(v) is bool and v for v in checks.values()):
        raise ValueError('UNVERIFIED_SCREENING_NO_PLANNING')
    candidates = [] if candidates is None else candidates
    if not isinstance(candidates,list) or len(candidates)>2:
        raise ValueError('MAX_TWO_CANDIDATES')
    admitted,rejected,ids = [],[],set()
    for card in candidates:
        if not isinstance(card,dict) or set(card) != {'id','family','new_action_term','historical_obstruction_changed','cheap_falsifier'}:
            raise ValueError('CANDIDATE_SCHEMA_HOLD')
        if not isinstance(card['id'],str) or not card['id'].isascii() or not card['id'].replace('_','').isalnum() or card['id'] in ids:
            raise ValueError('CANDIDATE_ID_HOLD')
        ids.add(card['id'])
        fields = ('new_action_term','historical_obstruction_changed','cheap_falsifier')
        if not all(isinstance(card[k],str) and len(card[k])<=500 for k in fields):
            raise ValueError('CANDIDATE_CONTENT_HOLD')
        if card['family'] not in ('M0','M1','M2'):
            reason='UNAUTHORIZED_FAMILY'
        elif not all(card[k].strip() for k in fields):
            reason='NO_NEW_MECHANISM'
        elif card['historical_obstruction_changed'] not in CLOSED:
            reason='UNKNOWN_CLOSED_FAILURE'
        else:
            admitted.append({'id':card['id'],'status':'UNVERIFIED_IDEA_ONLY','next':'G01_ACTION','cheap_falsifier':card['cheap_falsifier']})
            continue
        rejected.append({'id':card['id'],'reason':reason})
    return {
        'status':'PLAN_ONLY', 'next_gate':'G01_ACTION',
        'next_task':'Derive covariant SAME-ACTION Einstein/Hodge/source/X/Y/neutral/Earth/support variations and Ward/Bianchi identities',
        'cheap_negative_control':'Reject prescribed source current, gauge violation, unsupported lifting force, and unbounded energy',
        'historical_failures':CLOSED,
        'unverified_ideas':admitted, 'rejected_ideas':rejected,
        'physically_authorized_runs':0, 'physical_survivors':0,
        'gravity':'NOT_DERIVED', 'SI_energy':'NOT_CERTIFIED',
    }
