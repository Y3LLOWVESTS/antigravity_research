"""BETA1-04: immutable exact force, stress, support, momentum controls."""
from __future__ import annotations
from datetime import datetime,timezone
import hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from antigravity_research.beta_artificial.beta1_04_external_ledger import report

PARENTS={
 'M5V_FROZEN_SOURCE':('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py','ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
 'M5P_EXTERIOR_SOURCE':('src/antigravity_research/agminer/hook17_r3b_m5p_exterior_boundary.py','e49f7eb2ac7f700d0f2608bd556e3729cf0941932704761f9b9118d9607c2243'),
 'M5T_C2_SOURCE':('src/antigravity_research/agminer/hook17_r3b_m5t_variational_cell_material.py','7b613fc98d3d7247483ea1f0dcb89e492131e46d3f7f549097d73a98cc41ffa5'),
 'PH11_SUPPORT_SOURCE':('src/antigravity_research/agminer/hook17_ph11_universal_metric_support_gate.py','03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba'),
 'PH15_P10_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p10_free_space.py','25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'),
 'BETA1_00_JSON':('results/data/beta1_00_20261116T200742656266Z.json','866a305e4d7618d174ff63e864a3d7054ffc9133284e0e5c3637dec89145f708'),
 'BETA1_1B1_JSON':('results/data/beta1_1b1_20261117T001913743770Z.json','1468220d56a8555207f3f7e7960880636bc0ccb88bc344ad0d748e5e61a91b11'),
 'BETA1_02_JSON':('results/data/beta1_02_20261117T164856020351Z.json','723e21b16c003fdc6962455617ca56e9c390db10e43c1c55bfaec6e10efc3881'),
 'BETA1_03_JSON':('results/data/beta1_03_20261117T180317015064Z.json','86b7b2601e7181ba59b6f5c95932246f2c97b98046b83b3d817601e806dc44f0'),
}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check_parents():
    result={}
    for name,(relative,expect) in PARENTS.items():
        path=ROOT/relative
        actual=sha(path) if path.is_file() else None
        if actual!=expect:
            raise RuntimeError(f'FAIL-CLOSED historical SHA mismatch: {name}: {actual} expected {expect}')
        if name.startswith('BETA1_'):
            side=path.with_suffix('.json.sha256')
            if not side.is_file() or side.read_text().split()[0]!=actual:
                raise RuntimeError(f'FAIL-CLOSED historical SHA sidecar mismatch: {name}')
        result[name]={'path':relative,'sha256':actual,'status':'MATCH'}
    return result

def main():
    parents=check_parents()
    b3=json.loads((ROOT/PARENTS['BETA1_03_JSON'][0]).read_text())
    b2=json.loads((ROOT/PARENTS['BETA1_02_JSON'][0]).read_text())
    if b3['primary_verdict']!='YELLOW_NONZERO_ALPHA_REDUCED_RECIPROCITY_PASSES_FULL_ONSHELL_AND_METRIC_OPEN':
        raise RuntimeError('BETA1-03 verdict drift')
    if b2['primary_verdict']!='YELLOW_ACTION_SOURCED_PASSIVE_INTERFACE_TOY_C2_NOT_EXACT_PHYSICAL_MATERIAL_OPEN':
        raise RuntimeError('BETA1-02 verdict drift')
    science=report()
    if not all(science['gates'].values()):
        raise RuntimeError('FAIL-CLOSED new scientific gates: '+str({k:v for k,v in science['gates'].items() if not v}))
    now=datetime.now(timezone.utc)
    stamp=now.strftime('%Y%m%dT%H%M%S%fZ')
    source=ROOT/'src/antigravity_research/beta_artificial/beta1_04_external_ledger.py'
    verifier=ROOT/'tests/beta_artificial/test_beta1_04_external_ledger.py'
    doc={
        'program':'BETA-1','branch':'BETA1-04','timestamp_utc':now.isoformat(),
        'experiment':'EXACT_REACTION_STRESS_EXTERIOR_TRANSLATION_AND_CAUSAL_TOY_FIELD_LEDGER',
        'classification':science['classification'],'primary_verdict':science['status'],
        'parent_source_sha256':parents,'source_sha256':sha(source),
        'runner_sha256':sha(__file__),'independent_verifier_sha256':sha(verifier),
        'scoped_results':science,
        'toy_external_force':'DERIVED_ONLY_FOR_OPPOSITE_CHARGED_1D_SCALAR_ANALOG',
        'physical_neutral_Earth_metric_response':'NOT_DERIVED',
        'true_3D_exterior':'NOT_DERIVED',
        'source_X_Y_material_metric_on_shell':'NOT_CERTIFIED',
        'whole_craft_gravitational_force':'NOT_DERIVED',
        'Earth_down_craft_up_physical':'NOT_DERIVED',
        'causal_finite_source_cycle':'NOT_CERTIFIED',
        'complete_energy_SI':'NOT_AVAILABLE',
        'neutral_torus_1kg_1g_1m':'NOT_CERTIFIED',
        'physical_transfer':'NOT_AUTHORIZED',
        '006D_replaced':False,'ALPHA1_M5V_frozen':True,
        'completion_heuristic_physical':'UNCHANGED_APPROX_35_PERCENT',
        'completion_heuristic_BETA1':'BASELINE_APPROX_55_PERCENT_PENDING_POSTMORTEM',
        'next':'BETA1-04 postmortem: decide PH16 pivot; B11-M6 remains separate',
    }
    data=(json.dumps(doc,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    path=ROOT/'results/data'/f'beta1_04_{stamp}.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data);stream.flush();os.fsync(stream.fileno())
    digest=hashlib.sha256(data).hexdigest()
    side=path.with_suffix('.json.sha256')
    with side.open('x') as stream:
        stream.write(f'{digest}  {path.name}\n');stream.flush();os.fsync(stream.fileno())
    print('BETA1-04:',doc['primary_verdict'])
    print('HISTORICAL PROVENANCE:',len(parents),'/',len(PARENTS),'MATCH')
    print('EXACT IDENTITIES:',sum(science['symbolic'].values()),'/',len(science['symbolic']))
    print('SCOPED SCIENTIFIC GATES:',sum(science['gates'].values()),'/',len(science['gates']))
    st=science['static'];d=science['dynamics']['earth_present']
    print('TOY_STATIC_EARTH_FORCE:',st['force_earth'])
    print('TOY_STATIC_CRAFT_FORCE:',st['force_craft_source'])
    print('TOY_LOCAL_WARD_INF:',st['local_Ward_residual_inf'])
    print('TOY_DYNAMIC_IMPULSE_CRAFT:',d['integral_C'])
    print('TOY_DYNAMIC_EARTH_IMPULSE:',d['integral_E'])
    print('TOY_FIELD_MOMENTUM_CHANGE:',d['field_momentum_change'])
    print('TOY_TOTAL_MOMENTUM_MAX_ERROR:',d['momentum_max_error'])
    print('TOY_TOTAL_ENERGY_MAX_ERROR:',d['energy_max_error'])
    print('TOY_SUPPORT_REACTION_RESIDUAL:',d['spring_internal_force_max_residual'])
    print('PH15_NEUTRAL_EARTH_INTERACTION: NOT_DERIVED')
    print('ALPHA_M5V_PRESCRIBED_DERIVATIVES: NOT_CERTIFIED_THRUST')
    print('006D_REPLACED: NO')
    print('RESULT_JSON:',path)
    print('SHA256:',digest)

if __name__=='__main__':main()
