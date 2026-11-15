"""Execute PH9 with reproducible immutable output."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json,platform,sys
from antigravity_research.agminer import hook17_ph9_covariant_loading_gate as ph9

def main():
    root=Path.cwd(); data=ph9.run(root); now=datetime.now(timezone.utc)
    data['execution']={'utc':now.isoformat(),'python':sys.version,'platform':platform.platform(),
         'module_sha256':sha256(Path(ph9.__file__).read_bytes()).hexdigest(),
         'simulation_sha256':sha256(Path(__file__).read_bytes()).hexdigest()}
    name='032h17_ph9_covariant_loading_'+now.strftime('%Y%m%dT%H%M%S%fZ')+'.json'
    target=root/'results/data'/name;target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('x') as f:json.dump(data,f,indent=2,sort_keys=True,allow_nan=False);f.write('\n')
    p=data['primary']
    print('RUN='+data['branch'],'PROVENANCE='+data['gates']['P0_PROVENANCE'])
    for key in ('first_iteration_P_probe','loaded_P_probe','ratio_loaded_to_first_iteration_P',
                'first_iteration_metric_accel_shape','loaded_metric_accel_shape',
                'relative_gauge_rho_self_loading','relative_gauge_J_self_loading',
                'max_gauss_error','relative_ampere_error','relative_current_divergence',
                'electric_scalar_KG_EOM_residual_L2_per_field_L2'):
        print(key.upper()+'='+str(p[key]))
    print('PARTIAL_ENERGY='+str(p['canonical_energy']))
    print('VERDICT='+data['verdict']);print('JSON='+str(target))
    return 0 if data['gates']['P0_PROVENANCE']=='PASS' else 2
if __name__=='__main__':raise SystemExit(main())
