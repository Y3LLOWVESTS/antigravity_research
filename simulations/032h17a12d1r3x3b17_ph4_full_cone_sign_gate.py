"""PH4 executable. Frozen history read-only, unique timestamped JSON output."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys

from antigravity_research.agminer import hook17_ph4_full_cone_sign_gate as ph4


def main():
    root=Path.cwd()
    output=ph4.run(root)
    now=datetime.now(timezone.utc)
    output['execution']={
        'date_utc':now.isoformat(), 'python':sys.version,
        'platform':platform.platform(),
        'module_sha256':sha256(Path(ph4.__file__).read_bytes()).hexdigest(),
        'simulation_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    dest=root/'results/data'/(
        '032h17_ph4_full_cone_sign_'+now.strftime('%Y%m%dT%H%M%S%fZ')+'.json')
    dest.parent.mkdir(parents=True,exist_ok=True)
    with dest.open('x',encoding='utf-8') as stream:
        json.dump(output,stream,indent=2,sort_keys=True,allow_nan=False)
        stream.write('\n')
    print('RUN='+output['branch'])
    print('P0_PROVENANCE='+output['gates']['PH4_P0_PROVENANCE'])
    for label,entry in output['pre_registered_12_cases'].items():
        print('CASE='+label+' CHI='+str(entry['chi'])+
              ' K='+str(entry['A_kinetic'])+
              ' D_MIN='+str(entry['D_min_all_normals'])+
              ' VERDICT='+entry['exact_all_normals_verdict'])
    print('FARFIELD_NEGATIVE_EVEN=INWARD_R_MINUS_13_SCOPED')
    print('FARFIELD_POSITIVE_EVEN=OUTWARD_R_MINUS_13_BUT_RESTRICTED_CAUSAL_RED')
    print('PH4_VERDICT='+output['verdict'])
    print('PH4_PHYSICAL_CRAFT_LIFT=NOT_DERIVED')
    print('B11_M6=NOT_RUN')
    print('JSON='+str(dest))
    return 0 if output['gates']['PH4_P0_PROVENANCE']=='PASS' else 2

if __name__=='__main__':
    raise SystemExit(main())
