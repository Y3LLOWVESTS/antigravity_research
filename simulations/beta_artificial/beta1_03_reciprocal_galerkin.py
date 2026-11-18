"""BETA1-03 immutable PH15-P10 nonzero-alpha reciprocal L1 scientific runner."""
from __future__ import annotations
import hashlib,json,os,sys
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from antigravity_research.beta_artificial.beta1_03_reciprocal_galerkin import report

PARENTS={
 'PH15_P10_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p10_free_space.py','25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'),
 'PH15_P8_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py','406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed'),
 'PH15_P1_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p1_theorem.py','9ce430fa8a0e155ef330de27f1a8461c93a970385db4eeb53507c87253c07ca5'),
 'FROZEN_M5V_SOURCE':('src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py','ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f'),
 'BETA1_00_JSON':('results/data/beta1_00_20261116T200742656266Z.json','866a305e4d7618d174ff63e864a3d7054ffc9133284e0e5c3637dec89145f708'),
 'BETA1_01_JSON':('results/data/beta1_01_20261116T215749728579Z.json','706856dd6e469911f1845415c48ab30485f9027f238620c69af895b97fbf1579'),
 'BETA1_1B0_JSON':('results/data/beta1_1b0_20261116T235042989026Z.json','e60c13e66bacc77f38a3c97c390073151540132843ff1e22241936884a17fc0b'),
 'BETA1_1B1_JSON':('results/data/beta1_1b1_20261117T001913743770Z.json','1468220d56a8555207f3f7e7960880636bc0ccb88bc344ad0d748e5e61a91b11'),
 'BETA1_02_JSON':('results/data/beta1_02_20261117T164856020351Z.json','723e21b16c003fdc6962455617ca56e9c390db10e43c1c55bfaec6e10efc3881'),
}

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    provenance={}
    for name,(rel,expected) in PARENTS.items():
        path=ROOT/rel
        got=sha(path) if path.is_file() else None
        if got!=expected:raise RuntimeError(f'FAIL-CLOSED {name} SHA drift: {got} != {expected}')
        if name.startswith('BETA1_'):
            side=path.with_suffix('.json.sha256')
            if not side.is_file() or side.read_text().split()[0]!=got:
                raise RuntimeError('FAIL-CLOSED historic sidecar: '+name)
        provenance[name]={'path':rel,'sha256':got,'status':'MATCH'}
    previous=json.loads((ROOT/PARENTS['BETA1_02_JSON'][0]).read_text())
    if previous['primary_verdict']!='YELLOW_ACTION_SOURCED_PASSIVE_INTERFACE_TOY_C2_NOT_EXACT_PHYSICAL_MATERIAL_OPEN':
        raise RuntimeError('BETA1-02 scientific verdict drift')
    previous=json.loads((ROOT/PARENTS['BETA1_1B1_JSON'][0]).read_text())
    if previous['verdict']!='YELLOW_ALPHA0_CONSTRAINED_Y_GRADIENT_INSTABILITY_BETA100_NONZERO_ALPHA_OPEN':
        raise RuntimeError('BETA1-1B1 scientific verdict drift')
    result=report()
    if not all(result['gates'].values()):
        raise RuntimeError('FAIL-CLOSED new scientific gates: '+str({k:v for k,v in result['gates'].items() if not v}))
    now=datetime.now(timezone.utc);stamp=now.strftime('%Y%m%dT%H%M%S%fZ')
    module=ROOT/'src/antigravity_research/beta_artificial/beta1_03_reciprocal_galerkin.py'
    tests=ROOT/'tests/beta_artificial/test_beta1_03_reciprocal_galerkin.py'
    doc={
     'program':'BETA-1','branch':'BETA1-03',
     'experiment':'NONZERO_ALPHA_RECIPROCAL_SOURCE_X_Y_FIXED_NOETHER_REDUCED_ACTION',
     'timestamp_utc':now.isoformat(),
     'classification':result['classification'],'primary_verdict':result['verdict'],
     'parent_source_sha256':provenance,
     'source_sha256':sha(module),'runner_sha256':sha(__file__),'independent_verifier_sha256':sha(tests),
     'scoped_results':result,
     'on_shell_scope':'STATIONARY_ONLY_IN_20_DIMENSIONAL_GALERKIN_SPACE',
     'full_source_X_Y_on_shell':'NOT_CERTIFIED',
     'neutral_metric_matter':'NOT_SOLVED',
     'constrained_dynamic_health':'NOT_CERTIFIED',
     'continuum_exterior':'NOT_CERTIFIED',
     'earth_down_craft_up':'NOT_DERIVED',
     'whole_craft_force':'NOT_DERIVED',
     'complete_energy_SI':'NOT_AVAILABLE',
     'neutral_torus_1kg_1g_1m':'NOT_CERTIFIED',
     'physical_transfer':'NOT_AUTHORIZED',
     '006D_replaced':False,'ALPHA1_M5V_frozen':True,
     'completion_heuristic':'UNCHANGED_APPROX_35_PERCENT',
     'next':'BETA1-04 exact exterior force/support Ward and whole-craft interaction atlas, then PH16 pivot decision',
    }
    blob=(json.dumps(doc,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    dst=ROOT/'results/data'/f'beta1_03_{stamp}.json'
    dst.parent.mkdir(parents=True,exist_ok=True)
    with dst.open('xb') as fp:
        fp.write(blob);fp.flush();os.fsync(fp.fileno())
    digest=hashlib.sha256(blob).hexdigest()
    side=dst.with_suffix('.json.sha256')
    with side.open('x') as fp:
        fp.write(f'{digest}  {dst.name}\n');fp.flush();os.fsync(fp.fileno())
    print('BETA1-03:',result['verdict'])
    print('PROVENANCE:',len(provenance),'/',len(PARENTS),'MATCH')
    print('EXACT IDENTITIES:',sum(result['symbolic']['checks'].values()),'/',len(result['symbolic']['checks']))
    print('SCIENTIFIC GATES:',sum(result['gates'].values()),'/',len(result['gates']))
    for name,c in result['cases'].items():
        r=c['fixed_beta_scans']['40'][1]
        print('CASE',name,'Y_alpha0p05_beta40=',format(r['Y_norm'],'.10g'),
         'projected_EOM=',format(r['reduced_stationarity'],'.4g'),
         'UNPROJECTED_EOM=',format(c['omitted_equation_probe']['unprojected_joint_L2'],'.6g'),
         'Y_beta80_Schur=',round(c['beta80_negative_control']['Y_Schur_static_min'],6),flush=True)
    print('BETA_AFFECTS_LEADING_ALPHA_Y: YES')
    print('FULL_SOURCE_X_Y_PDE: OPEN; NONCONVERGED')
    print('EARTH_FORCE: NOT_DERIVED; 006D_REPLACED: NO')
    print('RESULT_JSON:',dst)
    print('SHA256:',digest)

if __name__=='__main__':main()
