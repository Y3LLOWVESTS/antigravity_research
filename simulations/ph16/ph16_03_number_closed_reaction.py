"""Fail-closed provenance/immutability and PH16-03 coupled-sector experiment."""
from __future__ import annotations
import hashlib,json,os,sys
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'))
from antigravity_research.ph16.ph16_03_number_closed_reaction import report

PARENTS={
 'PH15_P10_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p10_free_space.py','25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb'),
 'PH15_P8_SOURCE':('src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py','406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed'),
 'PH16_01_SOURCE':('src/antigravity_research/ph16/ph16_01_neutral_fluid_health.py','7466a5c1a4613940ff6c57301375513629d0a940fb48e1d8ebe81bdbdf60ddbb'),
 'PH16_02_SOURCE':('src/antigravity_research/ph16/ph16_02_reciprocal_principal.py','b16fa3141270cc446d761bc8459e5504325b994ac31a889c0ea88520161b0b48'),
 'PH16_00_JSON':('results/data/ph16_00_20261117T193302236321Z.json','0f6025bbdaa1fe6da12bbd6d1044c192cbb40a1006d3103b76f8e9c0b3f8576e'),
 'PH16_01_JSON':('results/data/ph16_01_20261118T001752187817Z.json','06f4aa6960645823e81e5d577288dadda8d579567456e8af05dd21369a4173ad'),
 'PH16_02_JSON':('results/data/ph16_02_20261118T033343237505Z.json','95b549c75346e81fc62b20e919160954c48bf4abe6230beb5bbf40ddf34a68ee'),
}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def run():
    parents={}
    for k,(rel,want) in PARENTS.items():
        f=ROOT/rel
        got=sha(f) if f.is_file() else 'MISSING'
        if got!=want:raise RuntimeError(f'FAIL_CLOSED_PARENT_SHA {k}: expected {want}; got {got}')
        if k.endswith('JSON'):
            side=f.with_suffix('.json.sha256')
            if not side.is_file() or side.read_text().split()[0]!=got:
                raise RuntimeError('FAIL_CLOSED_PARENT_SIDECAR '+k)
        parents[k]={'path':rel,'sha256':got,'status':'MATCH'}
    prev=json.loads((ROOT/PARENTS['PH16_02_JSON'][0]).read_text())
    if prev['primary_verdict']!='YELLOW_PH16_02_RESTRICTED_FULLCELL_Y_BETA40_STATIONARY_GAUGE_BETA60_PRINCIPAL_WARNING_FULL_SYSTEM_OPEN':
        raise RuntimeError('PH16-02 verdict changed')
    if prev['006D_replaced'] or prev['PH17_approved']!='NO':
        raise RuntimeError('PH16-02 physical promotion changed')
    results=report()
    passed=all(results['exact'].values()) and all(results['gates'].values())
    now=datetime.now(timezone.utc)
    source=ROOT/'src/antigravity_research/ph16/ph16_03_number_closed_reaction.py'
    tests=ROOT/'tests/ph16/test_ph16_03_number_closed_reaction.py'
    doc={
      'program':'ANTIGRAVITY_RESEARCH','branch':'PH16-03',
      'timestamp_utc':now.isoformat(),
      'experiment':'FIXED_NOETHER_COUPLED_Y_FREQUENCY_HYDROSTATIC_NUMBER_REACTION_FROZEN_SOURCE_X',
      'primary_verdict':results['verdict'] if passed else 'RED_PH16_03_SCOPED_GATE_FAILURE',
      'classification':'ONE_ACTION_REDUCED_ROUTHIAN_Y_OMEGA_HYDROSTATIC_FLUID_FIXED_SOURCE_X',
      'parent_sha256':parents,'source_sha256':sha(source),'runner_sha256':sha(__file__),'tests_sha256':sha(tests),
      'scoped_results':results,'scoped_gates_pass':passed,
      'source_F_and_X_profiles':'FROZEN_NOT_VARIATIONALLY_CLOSED',
      'source_X_gauss_full_absolute':'NOT_SOLVED',
      'neutral_fluid_dynamical_support':'NOT_SOLVED',
      'gravity_Einstein_EOM':'NOT_SOLVED',
      'full_coupled_constrained_modes':'NOT_CERTIFIED',
      'physical_Earth_down_craft_up':'NOT_DERIVED',
      '1kg_torus_1g_at_1m':'NOT_CERTIFIED',
      'complete_SI_energy_lt10MJ':'NOT_CERTIFIED',
      '006D_replaced':False,'PH17_approved':'NO','ALPHA1_M5V_frozen':True,
      'physical_heuristic':'APPROX_35_PERCENT_REASSESS_AFTER_HUMAN_REVIEW',
      'BETA1_heuristic':'FROZEN_APPROX_70_PERCENT',
      'next':'PH16-04: independently covary F and X in same discrete action and derive exact source/X gradients; test 3D exterior and metric later',
      'limits':[
        'No fully coupled PH16 stationary solution: the source profiles F and X remain frozen',
        'Y/omega/neutral fluid are jointly self-consistent only in the reduced finite-cell Routhian',
        'X and scalar EOM defect diagnostics mix quadrature/finite-difference operators; not exact action gradients',
        'No material supports, Einstein metric, full gauge-constrained hyperbolicity, source UV realization or Earth reaction',
        'Routhian is not Hamiltonian, not joules; complete system energy cannot be certified',
      ],
    }
    output=json.dumps(doc,sort_keys=True,indent=2,allow_nan=False).encode()+b'\n'
    stamp=now.strftime('%Y%m%dT%H%M%S%fZ')
    dest=ROOT/'results/data'/f'ph16_03_{stamp}.json'
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('xb') as f:f.write(output);f.flush();os.fsync(f.fileno())
    digest=hashlib.sha256(output).hexdigest()
    with dest.with_suffix('.json.sha256').open('x') as f:
        f.write(f'{digest}  {dest.name}\n');f.flush();os.fsync(f.fileno())
    print('PH16-03:',doc['primary_verdict'])
    print('PARENTS:',len(parents),'/',len(PARENTS),'MATCH')
    print('EXACT:',sum(results['exact'].values()),'/',len(results['exact']))
    print('SCOPED:',sum(results['gates'].values()),'/',len(results['gates']))
    for k,c in results['cases'].items():
        print('CASE',k,'Y_residual',format(c['inner']['residual_L2'],'.9g'),
        'N_err',format(c['source_N_residual_max'],'.9g'),
        'old_N_err',format(c['frozen_P10_omega_Noether_defect_abs'],'.9g'),
        'fluid_N_err',format(c['neutral_number_residual'],'.9g'),
        'source_mixed_EOM',format(max(c['source_frozen_EOM_diagnostic_weighted_L2']),'.9g'),
        'X_mixed_defect',format(c['X_mixed_discretization_kernel_defect_inf'],'.9g'))
    print('F+X+METRIC: NOT_SOLVED')
    print('EARTH/WHOLE_CRAFT_FORCE: NOT_DERIVED')
    print('006D_REPLACED: NO')
    print('RESULT_JSON:',dest)
    print('SHA256:',digest)
    if not passed:raise RuntimeError('PH16-03 science gate failure; immutable RED artifact written')

if __name__=='__main__':run()
