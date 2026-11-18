"""PH16-00 fail-closed immutable exact-action transfer and neutral-loading audit."""
from __future__ import annotations
import hashlib,json,os,sys
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))

from antigravity_research.ph16.ph16_00_transfer_atlas import report

PARENTS={
 'PH15_P1_THEOREM':(
    'src/antigravity_research/agminer/hook17_ph15_p1_theorem.py',
    '9ce430fa8a0e155ef330de27f1a8461c93a970385db4eeb53507c87253c07ca5'),
 'PH15_P8_SOURCE':(
    'src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py',
    '406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed'),
 'PH15_P10_SOURCE':(
    'src/antigravity_research/agminer/hook17_ph15_p10_free_space.py',
    '25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'),
 'PH11_SUPPORT':(
    'src/antigravity_research/agminer/hook17_ph11_universal_metric_support_gate.py',
    '03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba'),
 'ALPHA1_FROZEN_M5V':(
    'src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py',
    'ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
 'BETA1_00_JSON':(
    'results/data/beta1_00_20261116T200742656266Z.json',
    '866a305e4d7618d174ff63e864a3d7054ffc9133284e0e5c3637dec89145f708'),
 'BETA1_1B1_JSON':(
    'results/data/beta1_1b1_20261117T001913743770Z.json',
    '1468220d56a8555207f3f7e7960880636bc0ccb88bc344ad0d748e5e61a91b11'),
 'BETA1_02_JSON':(
    'results/data/beta1_02_20261117T164856020351Z.json',
    '723e21b16c003fdc6962455617ca56e9c390db10e43c1c55bfaec6e10efc3881'),
 'BETA1_03_JSON':(
    'results/data/beta1_03_20261117T180317015064Z.json',
    '86b7b2601e7181ba59b6f5c95932246f2c97b98046b83b3d817601e806dc44f0'),
 'BETA1_04_JSON':(
    'results/data/beta1_04_20261117T184058123842Z.json',
    '2ff63f1e2cbad2dc09d192569701b5503da06ca384ca60546d6e83c8c61ae632'),
}

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def provenance_check():
    out={}
    for name,(rel,want) in PARENTS.items():
        file=ROOT/rel
        got=sha(file) if file.is_file() else 'MISSING'
        if got!=want:
            raise RuntimeError(
                f'PARENT_SHA_MISMATCH {name}: {got}; expected {want}'
            )
        if name.startswith('BETA1_'):
            side=file.with_suffix('.json.sha256')
            if (
                not side.is_file()
                or side.read_text().split()[0]!=want
            ):
                raise RuntimeError('PARENT_SIDECAR_MISMATCH '+name)
        out[name]={
            'path':rel,
            'sha256':got,
            'status':'MATCH'
        }
    return out

def main():
    parents=provenance_check()

    prior=json.loads(
        (ROOT/PARENTS['BETA1_04_JSON'][0]).read_text()
    )

    if prior['primary_verdict']!=(
        'YELLOW_EXACT_TOY_EXTERNAL_FORCE_LEDGER_'
        'REAL_GRAVITY_AND_M5V_SOURCE_MISSING'
    ):
        raise RuntimeError('BETA1-04 verdict changed unexpectedly')

    if (
        prior['006D_replaced']
        or prior['physical_transfer']!='NOT_AUTHORIZED'
    ):
        raise RuntimeError('Frozen BETA1 promotion guard violated')

    r=report()

    if (
        not all(r['exact']['checks'].values())
        or not all(r['gates'].values())
    ):
        raise RuntimeError('PH16-00 scientific gate FAIL')

    source=ROOT/(
        'src/antigravity_research/ph16/'
        'ph16_00_transfer_atlas.py'
    )
    verifier=ROOT/(
        'tests/ph16/test_ph16_00_transfer_atlas.py'
    )

    now=datetime.now(timezone.utc)

    doc={
       'project':'ANTIGRAVITY_RESEARCH',
       'branch':'PH16-00',
       'timestamp_utc':now.isoformat(),
       'experiment':
           'UNIVERSAL_TRACE_LOADING_SINGLE_ACTION_OBLIGATION_PREFLIGHT',
       'classification':
           'THEOREM_LEVEL_ACTION_VARIATION_PLUS_PRESCRIBED_'
           'TRACE_SENSITIVITY_NOT_FULL_PHYSICAL_CLOSURE',
       'primary_verdict':r['verdict'],
       'parent_source_sha256':parents,
       'source_sha256':sha(source),
       'runner_sha256':sha(__file__),
       'verifier_sha256':sha(verifier),
       'scoped_results':r,
       'PH16_full_source_X_Y_neutral_metric_on_shell':'NOT_SOLVED',
       'neutral_Earth_support_action':'DECLARED_NOT_DERIVED_OR_SOLVED',
       'true_external_metric_force':'NOT_DERIVED',
       'whole_craft_force':'NOT_DERIVED',
       '1kg_neutral_torus_1g_1m':'NOT_CERTIFIED',
       'complete_energy_SI_lt10MJ':'NOT_CERTIFIED',
       'PH16_stable_modes':'NOT_CERTIFIED',
       'PH17_approved':'NO',
       '006D_replaced':False,
       'ALPHA1_M5V_frozen':True,
       'physical_heuristic':
           'APPROX_35_PERCENT_UNCHANGED_PENDING_PHYSICAL_CLOSURE',
       'BETA1_heuristic':
           'FROZEN_APPROX_70_PERCENT_PIVOT_READINESS',
       'physical_transfer':'REQUIREMENTS_ONLY',
       'next':
           'PH16-01: explicitly covariant charged source, '
           'conserved neutral fluid, support action, metric '
           'P variation and fully reciprocal constraints; '
           'test full-cell EOM before 3D Earth force',
    }

    blob=(
        json.dumps(
            doc,
            indent=2,
            sort_keys=True,
            allow_nan=False
        )+'\n'
    ).encode()

    stamp=now.strftime('%Y%m%dT%H%M%S%fZ')
    path=ROOT/'results/data'/f'ph16_00_{stamp}.json'
    path.parent.mkdir(parents=True,exist_ok=True)

    with path.open('xb') as f:
        f.write(blob)
        f.flush()
        os.fsync(f.fileno())

    digest=hashlib.sha256(blob).hexdigest()

    with path.with_suffix('.json.sha256').open('x') as f:
        f.write(f'{digest}  {path.name}\n')
        f.flush()
        os.fsync(f.fileno())

    print('PH16-00:',doc['primary_verdict'])
    print('HISTORICAL SHA:',len(parents),'/',len(PARENTS),'MATCH')
    print(
        'EXACT ACTION CHECKS:',
        sum(r['exact']['checks'].values()),
        '/',
        len(r['exact']['checks'])
    )
    print(
        'NUMERICAL/SCOPED GATES:',
        sum(r['gates'].values()),
        '/',
        len(r['gates'])
    )

    for key,c in r['cases'].items():
        p=c['prescribed_neutral_diagnostic']
        print(
            'CASE',key,
            'P10_source_Y_jnorm',
            format(p['source_Y_current_weighted_L2'],'.9g'),
            'neutral_trace_delta_jnorm',
            format(p['neutral_increment_Y_current_weighted_L2'],'.9g'),
            'sensitivity_relative',
            format(p['neutral_increment_relative_to_source'],'.5g')
        )

    print('PH15_SOURCE_ONLY_Y_LOADED_EARTH: INCOMPLETE')
    print('FULL_SOURCE_X_Y_NEUTRAL_METRIC: NOT_SOLVED')
    print('EARTH_DOWN_CRAFT_UP: NOT_DERIVED')
    print('006D_REPLACED: NO')
    print('PHYSICAL_HEURISTIC: ~35%; BETA1: ~70% FROZEN')
    print('RESULT_JSON:',path)
    print('SHA256:',digest)

if __name__=='__main__':
    main()
