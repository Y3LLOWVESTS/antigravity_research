"""Execute PH14 neutral-source equilibrium and fail-closed gate; unique JSON."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys
from antigravity_research.agminer import hook17_ph14_neutral_composite as ph14


def main():
    root=Path.cwd()
    data=ph14.run(root)
    now=datetime.now(timezone.utc)
    data['execution']={
        'utc':now.isoformat(),'python':sys.version,'platform':platform.platform(),
        'module_sha256':sha256(Path(ph14.__file__).read_bytes()).hexdigest(),
        'runner_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    path=root/'results/data'/('032h17_ph14_neutral_composite_'+now.strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8') as out:
        json.dump(data,out,sort_keys=True,indent=2,allow_nan=False)
        out.write('\n')
    p=data['on_shell_neutral_source']
    print('RUN='+data['branch'])
    print('PROVENANCE='+data['gates']['P0_PROVENANCE'])
    for key in ('BVP_collocation_rms','omega_plus','omega_minus','f_minus_center',
                'Noether_plus','Noether_minus','relative_charge_neutrality',
                'integrated_net_gauge_charge','boundary_Gauss_flux',
                'max_abs_radial_E','total_field_plus_matter_energy',
                'free_particle_mass_threshold','binding_below_free_quanta',
                'stress_virial_relative_residual','local_radial_stress_divergence_max'):
        print(key.upper()+'='+str(p[key]))
    print('PARTIAL_ENERGY='+str(p['canonical_energy_terms']))
    print('SEPARATED_FIXED_N='+str(data['separated_lumps_same_N_comparison']))
    print('RESTRICTED_HESSIAN_MIN='+str(data['restricted_fixed_two_charge_radial']['lowest_eigenvalue']))
    print('RESTRICTED_HESSIAN_CROSSCHECK='+str(data['restricted_radial_resolution']))
    print('FROZEN_TRANSLATION='+str(data['frozen_translation_only']))
    print('SYMMETRY_NULL='+str(data['symmetric_mass_null']))
    print('PH13_TRACE_INDUCED_Y_ON_ONSHELL_SPHERICAL_COMPOSITE=ZERO_EXACT')
    for label,value in data['gates'].items():
        print('GATE_'+label+'='+value)
    print('VERDICT='+data['verdict'])
    print('JSON='+str(path))
    return 0 if data['gates']['P0_PROVENANCE']=='PASS' else 2


if __name__=='__main__':
    raise SystemExit(main())
