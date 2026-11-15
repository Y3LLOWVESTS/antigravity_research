"""PH10 bounded-well on-shell-at-zero-field, off-shell-at-loading gate."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys
from antigravity_research.agminer import hook17_ph10_bounded_well_source_gate as ph10

def main():
    root=Path.cwd();result=ph10.run(root)
    now=datetime.now(timezone.utc)
    result['execution']={
        'utc':now.isoformat(),'python':sys.version,'platform':platform.platform(),
        'module_sha256':sha256(Path(ph10.__file__).read_bytes()).hexdigest(),
        'simulation_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    path=root/'results/data'/('032h17_ph10_bounded_well_'+now.strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as stream:
        json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    print('RUN='+result['branch'])
    print('HISTORY='+result['gates']['P0_PROVENANCE'])
    for mode in result['primary']['eigenstates']:
        print('MODE_L='+str(mode['l'])+' POTENTIAL_DEPTH='+str(mode['depth'])
            +' MASS_SQUARED_INSIDE='+str(mode['minimum_quadratic_mass_squared'])
            +' MATCH_RESIDUAL='+str(mode['match_residual']))
    for r in result['primary']['independent_continuum_radial_virial']:
        print('VIRIAL_L='+str(r['l'])+' RELATIVE_RESIDUAL='+str(r['relative_variational_residual'])
              +' FRACTION_OUTSIDE_WELL='+str(r['fraction_outside_well']))
    p=result['primary']
    print('LOADED_UPPER_PROBE='+str(p['upper_probe']))
    print('LOADED_LOWER_PROBE='+str(p['lower_probe']))
    print('GAUGE_LOADED_SCALAR_KG_X='+str(p['scalar_KG_residual_from_loaded_X']))
    print('GAUGE_LOADED_SCALAR_KG_Y='+str(p['scalar_KG_residual_from_loaded_Y_exact_gauge_correction']))
    print('RELATIVE_DOMAIN_P_DIFFERENCE='+str(result['domain_P_relative_difference']))
    print('PARTIAL_CANONICAL_ENERGY='+str(p['partial_energy']))
    for key,value in result['gates'].items():
        print('GATE_'+key+'='+value)
    print('VERDICT='+result['verdict'])
    print('JSON='+str(path))
    return 0 if result['gates']['P0_PROVENANCE']=='PASS' else 2

if __name__=='__main__':
    raise SystemExit(main())
