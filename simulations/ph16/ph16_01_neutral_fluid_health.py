"""PH16-01 immutable covariant neutral-fluid and frozen principal-health audit."""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from antigravity_research.ph16.ph16_01_neutral_fluid_health import report

PARENTS={
 'PH15_P1_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p1_theorem.py','9ce430fa8a0e155ef330de27f1a8461c93a970385db4eeb53507c87253c07ca5'),
 'PH15_P8_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py','406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed'),
 'PH15_P10_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p10_free_space.py','25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'),
 'PH11_SUPPORT':('src/antigravity_research/agminer/hook17_ph11_universal_metric_support_gate.py','03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba'),
 'ALPHA_M5V':('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py','ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
 'BETA1_00_JSON':('results/data/beta1_00_20261116T200742656266Z.json','866a305e4d7618d174ff63e864a3d7054ffc9133284e0e5c3637dec89145f708'),
 'BETA1_1B1_JSON':('results/data/beta1_1b1_20261117T001913743770Z.json','1468220d56a8555207f3f7e7960880636bc0ccb88bc344ad0d748e5e61a91b11'),
 'BETA1_02_JSON':('results/data/beta1_02_20261117T164856020351Z.json','723e21b16c003fdc6962455617ca56e9c390db10e43c1c55bfaec6e10efc3881'),
 'BETA1_03_JSON':('results/data/beta1_03_20261117T180317015064Z.json','86b7b2601e7181ba59b6f5c95932246f2c97b98046b83b3d817601e806dc44f0'),
 'BETA1_04_JSON':('results/data/beta1_04_20261117T184058123842Z.json','2ff63f1e2cbad2dc09d192569701b5503da06ca384ca60546d6e83c8c61ae632'),
 'PH16_00_JSON':('results/data/ph16_00_20261117T193302236321Z.json','0f6025bbdaa1fe6da12bbd6d1044c192cbb40a1006d3103b76f8e9c0b3f8576e'),
}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    parents={}
    for name,(relative,expected) in PARENTS.items():
        path=ROOT/relative
        actual=sha(path) if path.is_file() else 'MISSING'
        if actual!=expected:
            raise RuntimeError(f'FAIL_CLOSED_PARENT_SHA {name}: {actual} != {expected}')
        if name.startswith(('BETA1_','PH16_00')):
            side=path.with_suffix('.json.sha256')
            if not side.is_file() or side.read_text().split()[0]!=actual:
                raise RuntimeError('FAIL_CLOSED_PARENT_SIDECAR: '+name)
        parents[name]={'path':relative,'sha256':actual,'status':'MATCH'}
    ph16=json.loads((ROOT/PARENTS['PH16_00_JSON'][0]).read_text())
    if ph16['primary_verdict']!='YELLOW_PH16_00_UNIVERSAL_TRACE_LOADING_PREFLIGHT_PH15_SOURCE_ONLY_Y_INCOMPLETE':
        raise RuntimeError('PH16-00 verdict drift')
    if ph16['006D_replaced'] or ph16['PH17_approved']!='NO':
        raise RuntimeError('PH16-00 claims drift')
    r=report()
    if not all(r['symbolic']['checks'].values()) or not all(r['gates'].values()):
        raise RuntimeError('FAIL_CLOSED_SCIENTIFIC_GATES '+str([k for k,v in r['gates'].items() if not v]))
    now=datetime.now(timezone.utc)
    module=ROOT/'src/antigravity_research/ph16/ph16_01_neutral_fluid_health.py'
    tests=ROOT/'tests/ph16/test_ph16_01_neutral_fluid_health.py'
    doc={
      'program':'ANTIGRAVITY_RESEARCH','branch':'PH16-01',
      'timestamp_utc':now.isoformat(),
      'experiment':'COVARIANT_NEUTRAL_FLUID_ACTION_HYDROSTATIC_RECIPROCITY_AND_FROZEN_PRINCIPAL_HEALTH',
      'classification':r['classification'],'primary_verdict':r['verdict'],
      'parent_source_sha256':parents,
      'source_sha256':sha(module),'runner_sha256':sha(__file__),'verifier_sha256':sha(tests),
      'scoped_results':r,
      'full_conserved_real_Earth_material':'NOT_SOLVED',
      'full_X_Y_source_on_shell':'NOT_SOLVED',
      'dynamical_Einstein_equations':'NOT_SOLVED',
      'complete_constrained_modes':'NOT_CERTIFIED',
      'real_neutral_torus_1kg_1g_1m':'NOT_CERTIFIED',
      'whole_craft_Earth_force':'NOT_DERIVED',
      'SI_lt10MJ_complete_energy':'NOT_CERTIFIED',
      'physical_transfer':'RESTRICTED_NECESSARY_CONDITIONS_ONLY',
      'PH17_approved':'NO','ALPHA1_M5V_frozen':True,'006D_replaced':False,
      'physical_heuristic':'APPROX_35_PERCENT_REASSESS_AFTER_REVIEW',
      'BETA1_heuristic':'FROZEN_APPROX_70_PERCENT',
      'next':'PH16-02: full-cell reciprocal X/Y/source/neutral constrained EOM and principal health; no PH17 promotion',
    }
    encoded=(json.dumps(doc,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    dst=ROOT/'results/data'/f"ph16_01_{now.strftime('%Y%m%dT%H%M%S%fZ')}.json"
    dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as out:
        out.write(encoded);out.flush();os.fsync(out.fileno())
    digest=hashlib.sha256(encoded).hexdigest()
    with dst.with_suffix('.json.sha256').open('x') as out:
        out.write(f'{digest}  {dst.name}\n');out.flush();os.fsync(out.fileno())
    print('PH16-01:',doc['primary_verdict'])
    print('HISTORICAL PARENTS:',len(parents),'/',len(PARENTS),'MATCH')
    print('EXACT SYMBOLIC:',sum(r['symbolic']['checks'].values()),'/',len(r['symbolic']['checks']))
    print('SCOPED GATES:',sum(r['gates'].values()),'/',len(r['gates']))
    for k,v in r['cases'].items():
        f=v['neutral_hydrostatic_ONE_WAY'];h=v['principal_Y_frozen_background']
        print('CASE',k,'hydro_to_arbitrary',format(f['ratio_hydro_over_arbitrary'],'.7g'),
              'beta_critical',format(h['beta_first_local_zero_stiffness'],'.8g'),
              'margin40',format(h['scans']['40']['minimum_frozen_magnetic_margin'],'.8g'),
              'margin60',format(h['scans']['60']['minimum_frozen_magnetic_margin'],'.8g'),flush=True)
    print('FULL_NEUTRAL_MATTER_X_Y_METRIC: NOT_SOLVED')
    print('REAL_EARTH_DOWN_CRAFT_UP: NOT_DERIVED')
    print('006D_REPLACED: NO')
    print('PHYSICAL_HEURISTIC: ~35%; BETA1: ~70% FROZEN')
    print('RESULT_JSON:',dst)
    print('SHA256:',digest)

if __name__=='__main__':main()
