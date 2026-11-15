"""PH8 static 3D sourced field and on-shell obstruction audit; unique JSON."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys
from antigravity_research.agminer import hook17_ph8_finite_scalar_source_gate as ph8

def main():
    root=Path.cwd()
    result=ph8.run(root)
    now=datetime.now(timezone.utc)
    result['execution']={
        'timestamp_utc':now.isoformat(), 'python':sys.version,
        'platform':platform.platform(),
        'module_sha256':sha256(Path(ph8.__file__).read_bytes()).hexdigest(),
        'simulation_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    dest=root/'results/data'/('032h17_ph8_finite_scalar_source_'+now.strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('x',encoding='utf-8') as file:
        json.dump(result,file,indent=2,sort_keys=True,allow_nan=False)
        file.write('\n')
    p=result['primary_source_solution']
    print('RUN='+result['branch'])
    print('HISTORY='+result['gates']['P0_PROVENANCE'])
    for k in ('net_charge','probe_clearance','P_at_probe',
              'neutral_acceleration_over_c_squared_shape',
              'a_earthward_z_shape','field_energy_canonical',
              'unloaded_scalar_time_plus_rest_energy_canonical',
              'charged_scalar_covariant_rho_loading_relative_L2',
              'charged_scalar_covariant_J_loading_relative_L2',
              'X_positive_cloud_internal_support_Fz',
              'Y_magnetic_local_hoop_stress_L1',
              'max_abs_Gauss_X_residual',
              'max_abs_divergence_JY_sampled',
              'volume_integral_P','volume_integral_abs_P'):
        print(k.upper()+'='+str(p[k]))
    print('DOMAIN_P_REL='+str(result['domain_relative_P_difference']))
    print('DOMAIN_FORCE_REL='+str(result['domain_relative_force_difference']))
    for k,v in result['gates'].items(): print('GATE_'+k+'='+v)
    print('VERDICT='+result['verdict'])
    print('JSON='+str(dest))
    return 0 if result['gates']['P0_PROVENANCE']=='PASS' else 2

if __name__=='__main__': raise SystemExit(main())
