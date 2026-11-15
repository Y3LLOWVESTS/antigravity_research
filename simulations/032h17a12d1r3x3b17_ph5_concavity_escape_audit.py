"""Execute PH5 conditional theorem/counterexample; never overwrite results."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

from antigravity_research.agminer import hook17_ph5_concavity_escape_audit as ph5


def main():
    root=Path.cwd()
    result=ph5.run(root)
    now=datetime.now(timezone.utc)
    result['execution']={
        'utc':now.isoformat(),'python':sys.version,'platform':platform.platform(),
        'source_sha256':sha256(Path(ph5.__file__).read_bytes()).hexdigest(),
        'sim_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    output=root/'results/data'/('032h17_ph5_concavity_escape_'+now.strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x',encoding='utf-8') as stream:
        json.dump(result,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    print('BRANCH='+result['branch'])
    print('PH5_PROVENANCE='+result['gates']['PH5_P0_HISTORY'])
    for name,rec in result['eight_pre_registered_cases'].items():
        print('CASE='+name+' P='+str(rec['P'])+
              ' RADIAL_A_OVER_C2='+str(rec['a_radial_over_c_squared_shape_units'])+
              ' CHI='+str(rec['chi'])+' CONE='+rec['cone_gate'])
    print('PH5_VERDICT='+result['verdict'])
    print('PHYSICAL_SOURCE_EOM=NOT_SOLVED')
    print('B11_M6=NOT_RUN')
    print('WHOLE_CRAFT_LIFT=NOT_DERIVED')
    print('STRICT_ENERGY_LT10MJ=NOT_CERTIFIED')
    print('JSON='+str(output))
    return 0 if result['gates']['PH5_P0_HISTORY']=='PASS_SCOPED' else 2


if __name__=='__main__':
    raise SystemExit(main())
